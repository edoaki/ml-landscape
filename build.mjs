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
const LABELS = {
  planned: "準備中",
  partial: "既存内容を移行・拡充予定",
  migrated: "既存内容を移行",
  ready: "公開本文",
};
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
    if (!Object.hasOwn(LABELS, meta.status))
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
        const status = ["planned", "partial"].includes(meta.status)
          ? "<small>" +
            (meta.status === "planned" ? "準備中" : "拡充予定") +
            "</small>"
          : "";
        out += `<a href="${meta.url}"${item.page === current ? ' aria-current="page"' : ""}${item.parent ? ' data-parent="' + esc(item.parent) + '"' : ""}>${esc(meta.title)}${status}</a>`;
      }
      out += "</details>";
    }
    return out;
  }
  const template = read(path.join(ROOT, "templates/page.html")),
    rendered = new Map();
  for (const id of order) {
    const meta = registry[id],
      body = render(files[id], bodies[id], registry),
      $ = load(body, { scriptingEnabled: false });
    uniqueIds($, id);
    let status = "";
    if (["planned", "partial"].includes(meta.status)) {
      const message =
        meta.status === "planned"
          ? "本文はまだ公開していません。今後扱う予定の範囲を示しています。"
          : "既存の説明・素材を移行したページです。予定範囲のうち、まだ説明していない項目は今後拡充します。";
      status = `<aside class="publication-status"><strong>${LABELS[meta.status]}</strong><p>${message}</p><details><summary>予定する範囲</summary><p>${esc(meta.scope)}</p></details></aside>`;
    }
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
  fs.mkdirSync(output, { recursive: true });
  const copy = (src, dest) => {
    fs.mkdirSync(path.dirname(dest), { recursive: true });
    fs.cpSync(src, dest, {
      recursive: true,
      filter: (file) =>
        ![".DS_Store", "__pycache__"].includes(path.basename(file)),
    });
  };
  copy(path.join(ROOT, "assets"), path.join(output, "assets"));
  for (const pattern of ["content/*/*/media", "content/*/*/components"])
    for (const dir of fs.globSync(pattern, { cwd: ROOT }))
      copy(path.join(ROOT, dir), path.join(output, dir));
  for (const [dest, file] of resources)
    if (dest !== "README.md") copy(file, path.join(output, dest));
  copy(
    path.join(ROOT, "templates/README-distribution.md"),
    path.join(output, "README.md"),
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
  return registry;
}
if (
  process.argv[1] &&
  import.meta.url === pathToFileURL(path.resolve(process.argv[1])).href
) {
  const { values } = parseArgs({ options: { output: { type: "string" } } });
  build(values.output);
}
