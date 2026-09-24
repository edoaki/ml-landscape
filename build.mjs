/** Build the portable, checked-in site using Node.js only. */
import fs from "node:fs";
import path from "node:path";
import { pathToFileURL } from "node:url";
import { parseArgs } from "node:util";
import { load } from "cheerio";
import YAML from "yaml";
import {
  ROOT,
  esc,
  read,
  readPage,
  pageFiles,
  render,
  rewriteReferences,
} from "./scripts/render-content.mjs";
import { collectSources } from "./scripts/check-sources.mjs";
export const MAX_ASSET_BYTES = 15e6;
// Public GitHub Pages address, used only for canonical/OGP URLs and the sitemap.
export const SITE_URL = "https://edoaki.github.io/ml-landscape/";
const OG_IMAGE = "assets/og-image.png";
const PROVENANCE = "content/shared/media-provenance.md";
const publicURL = (url) => SITE_URL + (url === "index.html" ? "" : url);
// label: page banner, nav: sidebar badge, message: banner text (unpublished states only).
export const STATUS = {
  planned: {
    label: "準備中",
    nav: "準備中",
    message: "本文はまだ公開していません。今後扱う予定の範囲を示しています。",
  },
  partial: {
    label: "既存内容を移行・拡充予定",
    nav: "拡充予定",
    message:
      "既存の説明・素材を移行したページです。予定範囲のうち、まだ説明していない項目は今後拡充します。",
  },
  migrated: { label: "既存内容を移行" },
  ready: { label: "公開本文" },
};
/** Reject unknown or cyclic prerequisites so the reading order stays well defined. */
export function validatePrerequisites(registry) {
  const state = {};
  const visit = (id, trail) => {
    if (state[id] === "done") return;
    if (state[id] === "active")
      throw new Error(`Cyclic prerequisites: ${[...trail, id].join(" → ")}`);
    state[id] = "active";
    for (const dep of registry[id].prerequisites || []) {
      if (!registry[dep]) throw new Error(`${id}: unknown prerequisite ${dep}`);
      visit(dep, [...trail, id]);
    }
    state[id] = "done";
  };
  for (const id of Object.keys(registry)) visit(id, []);
}
export function pageToc($) {
  const seen = new Set(),
    links = [];
  $("h2,h3").each((_, el) => {
    const heading = $(el);
    if (heading.parents("details").length) return;
    const target = heading.attr("id")
      ? heading
      : heading.parents("section[id],div[id]").first();
    const id = target.attr("id");
    if (!id || seen.has(id)) return;
    seen.add(id);
    links.push(
      `<a data-level="${el.tagName.slice(1)}" href="#${esc(id)}">${esc(heading.text())}</a>`,
    );
  });
  return links.join("");
}
const SEARCH_SKIP = "script,style,svg,noscript,.katex,.publication-status";
/** Split a page into heading-anchored chunks for the offline search index. */
export function searchEntries($, meta) {
  const entries = [];
  let current = { h: "", s: meta.title, x: [] };
  const flush = () => {
    // Markup boundaries add spaces that Japanese text does not have.
    const text = current.x
      .join("")
      .replace(/\s+/g, " ")
      .replace(/(?<=[\p{sc=Han}\p{sc=Hira}\p{sc=Kana}、。，．）」』】ー]) | (?=[\p{sc=Han}\p{sc=Hira}\p{sc=Kana}、。，．（「『【])/gu, "")
      .trim();
    if (text) entries.push({ u: meta.url, t: meta.title, s: current.s, h: current.h, x: text });
  };
  const walk = (node) => {
    if (node.type === "text") return current.x.push(node.data);
    if (node.type !== "tag") return;
    const el = $(node);
    if (el.is(SEARCH_SKIP)) return;
    if (/^h[23]$/.test(node.tagName)) {
      const target = el.attr("id")
        ? el
        : el.parents("section[id],div[id]").first();
      flush();
      current = { h: target.attr("id") || "", s: el.text().trim(), x: [] };
      return;
    }
    for (const child of node.children) walk(child);
    // Block boundaries separate words that the markup keeps apart.
    if (!/^(a|span|strong|em|b|i|u|s|q|code|sub|sup|small|mark|abbr|kbd|var|time|label)$/.test(node.tagName))
      current.x.push(" ");
  };
  for (const node of $.root().children().get()) walk(node);
  flush();
  return entries;
}
const external = (value) => /^(?:[a-z][a-z0-9+.-]*:|\/\/)/i.test(value);
function parts(value) {
  const [, pathname = "", query = "", fragment = ""] = value.match(
    /^([^?#]*)(\?[^#]*)?(#.*)?$/,
  );
  return { pathname, query, fragment };
}
function relativeRef(value, current) {
  if (external(value)) return value;
  const { pathname, query, fragment } = parts(value);
  return pathname
    ? path.posix.relative(path.posix.dirname(current), pathname) +
        query +
        fragment
    : value;
}
function uniqueIds($, label) {
  const ids = $("[id]")
    .map((_, el) => $(el).attr("id"))
    .get();
  if (new Set(ids).size !== ids.length)
    throw new Error(`${label}: duplicate IDs`);
  return new Set(ids);
}
export function validatePages(rendered, resourceRoot, onResource = () => {}) {
  const parsed = new Map(
    [...rendered].map(([url, html]) => [
      url,
      load(html, { scriptingEnabled: false }),
    ]),
  );
  const ids = new Map([...parsed].map(([url, $]) => [url, uniqueIds($, url)]));
  for (const [url, $] of parsed) {
    if ($("h1").length !== 1) throw new Error(`${url}: expected one h1`);
    if (
      /\{\{component:|\{\.[a-z][a-z-]*\}|\{#[a-z][a-z-]*\}|MLPLACEHOLDER\d+END|MLHTMLBLOCK\d+END/.test(
        $("main").text(),
      )
    )
      throw new Error(`${url}: unresolved Markdown marker`);
    $("[href],[src],[poster]").each((_, el) => {
      for (const attr of ["href", "src", "poster"]) {
        const value = $(el).attr(attr);
        if (!value || external(value)) continue;
        const { pathname, fragment } = parts(value);
        const dest = pathname
          ? path.posix.normalize(
              path.posix.join(
                path.posix.dirname(url),
                decodeURIComponent(pathname),
              ),
            )
          : url;
        if (dest.startsWith("../") || path.isAbsolute(dest))
          throw new Error(`${url}: resource outside site ${value}`);
        if (!parsed.has(dest)) {
          const resource = path.resolve(resourceRoot, dest);
          if (!fs.existsSync(resource) || !fs.statSync(resource).isFile())
            throw new Error(`${url}: missing ${value}`);
          onResource(dest, resource);
        }
        if (
          fragment &&
          parsed.has(dest) &&
          !ids.get(dest).has(decodeURIComponent(fragment.slice(1)))
        )
          throw new Error(`${url}: missing anchor ${value}`);
      }
    });
  }
}
export function build(outputArg) {
  const registry = {},
    bodies = {},
    files = {};
  for (const file of pageFiles()) {
    const [meta, body] = readPage(file),
      id = meta.id;
    if (registry[id] || !/^[a-z][a-z0-9-]*$/.test(id))
      throw new Error(`Invalid/duplicate page ID: ${id}`);
    if (!Object.hasOwn(STATUS, meta.status))
      throw new Error(`Unknown status: ${id}`);
    if (!/^(?:[a-z][a-z0-9-]*\/)*[a-z][a-z0-9-]*\.html$/.test(meta.url))
      throw new Error(`Invalid URL: ${meta.url}`);
    registry[id] = meta;
    bodies[id] = body;
    files[id] = file;
  }
  const navigation = YAML.parse(read(path.join(ROOT, "navigation.yml")));
  const order = navigation.flatMap((group) =>
    group.items.map((item) => item.page),
  );
  if (
    order.length !== new Set(order).size ||
    order.length !== Object.keys(registry).length ||
    order.some((id) => !registry[id])
  )
    throw new Error("Navigation and page IDs differ");
  if (new Set(Object.values(registry).map((m) => m.url)).size !== order.length)
    throw new Error("Duplicate URL");
  validatePrerequisites(registry);
  for (const group of navigation)
    for (const item of group.items) {
      if (item.parent && !registry[item.parent])
        throw new Error(`Unknown parent: ${item.parent}`);
      registry[item.page].group = group.title;
    }
  function navHTML(current) {
    let out = '<p class="nav-label">目次</p>';
    for (const group of navigation) {
      out +=
        "<details" +
        (registry[current].group === group.title || group.title === "はじめに"
          ? " open"
          : "") +
        "><summary>" +
        esc(group.title) +
        "</summary>";
      let category;
      for (const item of group.items) {
        const meta = registry[item.page];
        if (item.category !== category) {
          category = item.category;
          if (category)
            out += '<p class="nav-category">' + esc(category) + "</p>";
        }
        const badge = STATUS[meta.status].nav
          ? "<small>" + STATUS[meta.status].nav + "</small>"
          : "";
        const prereq = (meta.prerequisites || []).length
          ? ` title="前提：${esc(meta.prerequisites.map((p) => registry[p].title).join("、"))}"`
          : "";
        out += `<a href="${meta.url}"${prereq}${item.page === current ? ' aria-current="page"' : ""}${item.parent ? ' data-parent="' + esc(item.parent) + '"' : ""}>${esc(meta.title)}${badge}</a>`;
      }
      out += "</details>";
    }
    return out;
  }
  const template = read(path.join(ROOT, "templates/page.html")),
    rendered = new Map(),
    search = [];
  for (const id of order) {
    const meta = registry[id],
      body = render(files[id], bodies[id], registry),
      $ = load(body, { scriptingEnabled: false });
    uniqueIds($, id);
    search.push(...searchEntries($, meta));
    let status = "";
    const { label, message } = STATUS[meta.status];
    if (message)
      status = `<aside class="publication-status"><strong>${label}</strong><p>${message}</p><details><summary>予定する範囲</summary><p>${esc(meta.scope)}</p></details></aside>`;
    const scripts =
      (meta.scripts || [])
        .map((src) => `<script src="${esc(src)}" defer></script>`)
        .join("") +
      (meta.styles || [])
        .map((src) => `<link rel="stylesheet" href="${esc(src)}">`)
        .join("");
    const values = {
      id,
      title: esc(meta.title),
      description: esc(meta.summary),
      summary: esc(meta.summary),
      group:
        esc(meta.group) +
        ' · <span lang="en">' +
        esc(meta.english_title || "") +
        "</span>",
      status,
      navigation: navHTML(id),
      body,
      toc: pageToc($),
      scripts,
      canonical: esc(publicURL(meta.url)),
      ogtype: meta.url === "index.html" ? "website" : "article",
      ogimage: SITE_URL + OG_IMAGE,
    };
    let out = template.replace(/\$([a-z]+)/g, (_, key) => {
      if (!(key in values)) throw new Error(`Unknown template field ${key}`);
      return values[key];
    });
    out = out.replace(
      'data-site-root="."',
      `data-site-root="${path.posix.relative(path.posix.dirname(meta.url), ".") || "."}"`,
    );
    rendered.set(
      meta.url,
      rewriteReferences(out, (value) => relativeRef(value, meta.url)),
    );
  }
  const output = path.resolve(outputArg || path.join(ROOT, "dist"));
  if (
    output === ROOT ||
    ROOT.startsWith(output + path.sep) ||
    [
      "assets",
      "content",
      "source",
      "scripts",
      "tests",
      "docs",
      "templates",
    ].some(
      (d) =>
        output === path.join(ROOT, d) ||
        output.startsWith(path.join(ROOT, d) + path.sep),
    )
  )
    throw new Error("Output must be a dedicated distribution directory");
  const resources = new Map();
  validatePages(rendered, ROOT, (dest, file) => resources.set(dest, file));
  // Files loaded by page scripts are declared per page; license texts always ship.
  for (const id of order)
    for (const pattern of registry[id].runtime_assets || []) {
      const dir = path.relative(ROOT, path.dirname(files[id]));
      const matches = fs.globSync(path.posix.join(dir, pattern), {
        cwd: ROOT,
      });
      if (!matches.length)
        throw new Error(`${id}: runtime asset not found ${pattern}`);
      for (const file of matches)
        resources.set(file.split(path.sep).join("/"), path.join(ROOT, file));
    }
  for (const file of fs.globSync("assets/*{LICENSE,license}*.txt", {
    cwd: ROOT,
  }))
    resources.set(file, path.join(ROOT, file));
  resources.set(OG_IMAGE, path.join(ROOT, OG_IMAGE));
  // The distribution README points readers to the media record.
  resources.set(PROVENANCE, path.join(ROOT, PROVENANCE));
  resources.delete("README.md");
  for (const [dest, file] of resources) {
    const size = fs.statSync(file).size;
    if (size > MAX_ASSET_BYTES)
      throw new Error(
        `${dest}: ${(size / 1e6).toFixed(1)} MB exceeds the ${MAX_ASSET_BYTES / 1e6} MB limit`,
      );
  }
  // Rebuild from scratch so removed pages and assets do not linger.
  if (fs.existsSync(output) && fs.readdirSync(output).length) {
    if (!fs.existsSync(path.join(output, "assets/navigation.js")))
      throw new Error(`${output} is not empty and is not a previous build`);
    fs.rmSync(output, { recursive: true });
  }
  fs.mkdirSync(output, { recursive: true });
  const copy = (src, dest) => {
    fs.mkdirSync(path.dirname(dest), { recursive: true });
    fs.copyFileSync(src, dest);
  };
  for (const [dest, file] of resources) copy(file, path.join(output, dest));
  copy(
    path.join(ROOT, "templates/README-distribution.md"),
    path.join(output, "README.md"),
  );
  fs.writeFileSync(
    path.join(output, "sitemap.xml"),
    '<?xml version="1.0" encoding="UTF-8"?>\n<urlset xmlns="http://www.sitemaps.org/schemas/sitemap/0.9">\n' +
      order
        .filter((id) => registry[id].status !== "planned")
        .map((id) => `  <url><loc>${esc(publicURL(registry[id].url))}</loc></url>\n`)
        .join("") +
      "</urlset>\n",
  );
  // A script (not JSON) keeps search working when pages are opened via file://.
  fs.writeFileSync(
    path.join(output, "assets/search-index.js"),
    "window.ML_SEARCH_INDEX=" + JSON.stringify(search) + ";\n",
  );
  for (const [url, html] of rendered) {
    const dest = path.join(output, url);
    fs.mkdirSync(path.dirname(dest), { recursive: true });
    fs.writeFileSync(dest, html);
  }
  if (!outputArg) {
    let entry = rewriteReferences(rendered.get("index.html"), (value) => {
      if (external(value)) return value;
      const { pathname, query, fragment } = parts(value);
      return pathname && !["index.html", "README.md"].includes(pathname)
        ? "dist/" + pathname + query + fragment
        : value;
    });
    entry = entry.replace('data-site-root="."', 'data-site-root="dist"');
    fs.writeFileSync(path.join(ROOT, "index.html"), entry);
  }
  console.log(`Built ${order.length} pages; links, IDs and assets validated.`);
  const sources = collectSources();
  console.log(
    `Sources awaiting primary-source verification: ${sources.filter((s) => s.pending).length}/${sources.length} (npm run check:sources)`,
  );
  return registry;
}
if (
  process.argv[1] &&
  import.meta.url === pathToFileURL(path.resolve(process.argv[1])).href
) {
  const { values } = parseArgs({ options: { output: { type: "string" } } });
  build(values.output);
}
