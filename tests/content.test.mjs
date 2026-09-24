import test from "node:test";
import assert from "node:assert/strict";
import fs from "node:fs";
import path from "node:path";
import { load } from "cheerio";
import YAML from "yaml";
import {
  ROOT,
  read,
  readPage,
  pageFiles,
  render,
} from "../scripts/render-content.mjs";
import {
  pageToc,
  validatePages,
  validatePrerequisites,
  searchEntries,
  SITE_URL,
  MAX_ASSET_BYTES,
} from "../build.mjs";

test("navigation matches page metadata and hierarchy", () => {
  const nav = YAML.parse(read(path.join(ROOT, "navigation.yml"))),
    ids = nav.flatMap((g) => g.items.map((p) => p.page));
  const expected = new Set(pageFiles().map((p) => readPage(p)[0].id));
  assert.deepEqual(new Set(ids), expected);
  assert.equal(ids.length, expected.size);
  assert.ok(expected.has("introduction"));
  assert.deepEqual(
    nav.map((g) => g.title),
    [
      "はじめに",
      "基礎と代表的な機械学習手法",
      "分野・タスクから知る",
      "横断的な研究を知る",
      "モデルの仕組みを知る",
    ],
  );
  assert.equal(
    nav.flatMap((g) => g.items).find((p) => p.page === "vit").parent,
    "transformer",
  );
  for (const file of pageFiles()) {
    const [meta, body] = readPage(file);
    assert.ok(meta.scope);
    if (meta.status === "planned") assert.equal(body.trim(), "");
    assert.ok(!(meta.scripts || []).some((s) => s.startsWith("source/")));
  }
});
test("TOC follows visible headings and excludes optional details", () => {
  const $ = load(
    '<h2 id="intro">導入</h2><section id="task"><h2>タスク</h2><section id="example"><h3>例</h3></section></section><details><summary>補足</summary><section id="detail"><h2>詳説</h2></section></details><h2 id="evaluation">評価</h2>',
  );
  const toc = load(pageToc($));
  assert.deepEqual(
    toc("a")
      .map((_, e) => toc(e).attr("href"))
      .get(),
    ["#intro", "#task", "#example", "#evaluation"],
  );
  assert.deepEqual(
    toc("a")
      .map((_, e) => toc(e).attr("data-level"))
      .get(),
    ["2", "2", "3", "2"],
  );
});
test("Markdown retains nested HTML, Japanese emphasis, math, SVG and rewritten links", () => {
  const dir = fs.mkdtempSync(path.join(ROOT, ".test-content-"));
  try {
    fs.mkdirSync(path.join(dir, "components"));
    fs.writeFileSync(
      path.join(dir, "sources.yml"),
      "paper:\n  url: https://example.org/paper\n",
    );
    fs.writeFileSync(
      path.join(dir, "components/demo.html"),
      '<figure id="static"><svg viewBox="0 0 10 10"><circle r="2"/></svg><noscript>静止図を参照</noscript></figure>',
    );
    const file = path.join(dir, "index.md"),
      body =
        '## 説明 {#idea}\n\n[別ページ](page:other#part)・[出典](source:paper)\n\n![画像](media:figure.svg)\n\n$$\np(y \\mid x)\n$$\n\n<section markdown="1">\n\n<details markdown="1">\n<summary>例</summary>\n\n**Query（Q）**を使う\n\n| a | b |\n|---|---|\n| 1 | 2 |\n\n{{component:demo}}\n\n</details>\n</section>';
    const out = render(file, body, { other: { url: "renamed.html" } }),
      $ = load(out, { scriptingEnabled: false });
    assert.equal($("h2").attr("id"), "idea");
    assert.equal($("a").first().attr("href"), "renamed.html#part");
    assert.ok(out.includes("https://example.org/paper"));
    assert.ok(out.includes(path.basename(dir) + "/media/figure.svg"));
    assert.equal($("math").length, 1);
    assert.equal($("svg").attr("viewBox"), "0 0 10 10");
    assert.equal($("noscript").text(), "静止図を参照");
    assert.equal($("section details table tbody td").length, 2);
    assert.equal($("strong").text(), "Query（Q）");
    assert.ok(!out.includes("{{"));
    for (const invalid of [
      "[x](page:missing)",
      "[x](source:missing)",
      "{{component:missing}}",
      "{{component:../../escape}}",
    ])
      assert.throws(() => render(file, invalid, {}));
  } finally {
    fs.rmSync(dir, { recursive: true, force: true });
  }
});
test("checked-in distribution is complete and independent of source/development tools", () => {
  const site = path.resolve(
    process.env.ML_LANDSCAPE_SITE || path.join(ROOT, "dist"),
  );
  const pages = new Map(
    pageFiles().map((file) => {
      const [m] = readPage(file);
      return [m.url, read(path.join(site, m.url))];
    }),
  );
  assert.ok(pages.size >= 26);
  validatePages(pages, site);
  for (const [url, html] of pages) {
    const $ = load(html, { scriptingEnabled: false });
    assert.equal($(".pager,#related").length, 0, url);
    assert.equal($('#chapter-nav a[aria-current="page"]').length, 1, url);
    $(
      'script[src],img[src],source[src],audio[src],link[rel="stylesheet"]',
    ).each((_, el) => {
      const value = $(el).attr("src") || $(el).attr("href");
      assert.ok(!/^(?:https?:)?\/\//.test(value), value);
    });
  }
  const root = load(read(path.join(ROOT, "index.html")), {
    scriptingEnabled: false,
  });
  root("[href],[src]").each((_, el) => {
    const value = root(el).attr("href") || root(el).attr("src");
    if (!/^(?:[a-z]+:|\/\/|#)/i.test(value))
      assert.ok(fs.existsSync(path.join(ROOT, value.split(/[?#]/)[0])), value);
  });
  const pdb = read(path.join(ROOT, "assets/alphafold-P69905-v6.pdb"))
    .split("\n")
    .filter((s) => s.startsWith("ATOM") && s.slice(12, 16).trim() === "CA");
  assert.equal(pdb.length, 142);
  for (const line of pdb)
    assert.ok(+line.slice(60, 66) >= 0 && +line.slice(60, 66) <= 100);
});
test("validation rejects missing files, anchors, duplicate IDs and escaped paths", () => {
  const wrap = (body) => "<h1>Title</h1><main>" + body + "</main>";
  for (const body of [
    '<a href="missing.html">x</a>',
    '<a href="#missing">x</a>',
    '<p id="a"></p><p id="a"></p>',
    '<img src="../README.md">',
    "{{component:missing}}",
  ])
    assert.throws(() =>
      validatePages(new Map([["index.html", wrap(body)]]), ROOT),
    );
});
test("source metadata and bundled fonts resolve", () => {
  for (const file of fs.globSync("content/*/*/sources.yml", { cwd: ROOT }))
    for (const [key, ref] of Object.entries(
      YAML.parse(read(path.join(ROOT, file))) || {},
    )) {
      assert.ok(ref.url && ref.label, `${file}:${key}`);
      if (!/^https?:/.test(ref.url))
        assert.ok(fs.existsSync(path.join(ROOT, ref.url)));
      if (ref.provenance)
        assert.ok(fs.existsSync(path.join(ROOT, ref.provenance)));
    }
  for (const [, value] of read(path.join(ROOT, "assets/katex.css")).matchAll(
    /url\(([^)]+)\)/g,
  ))
    if (!value.startsWith("data:"))
      assert.ok(
        fs.existsSync(
          path.join(ROOT, "assets", value.replace(/^['"]|['"]$/g, "")),
        ),
      );
});

test("prerequisites name existing pages without cycles", () => {
  const registry = Object.fromEntries(
    pageFiles().map((file) => {
      const [meta] = readPage(file);
      return [meta.id, meta];
    }),
  );
  validatePrerequisites(registry);
  for (const [id, meta] of Object.entries(registry))
    if (id !== "introduction") assert.ok(meta.prerequisites.length, id);
  assert.throws(
    () =>
      validatePrerequisites({
        a: { prerequisites: ["b"] },
        b: { prerequisites: ["a"] },
      }),
    /Cyclic/,
  );
  assert.throws(
    () => validatePrerequisites({ a: { prerequisites: ["missing"] } }),
    /unknown/,
  );
});
test("search index splits pages at anchored headings and drops markup noise", () => {
  const $ = load(
    '<p>導入の<strong>本文</strong>です。</p><section id="attn"><h2>注意機構</h2><p>Self-<em>Attention</em>は</p><div class="equation"><span class="katex">x^2</span></div><svg><text>図の文字</text></svg></section><h3 id="next">次</h3><p>続き</p>',
  );
  const entries = searchEntries($, { url: "models/x.html", title: "X" });
  assert.deepEqual(
    entries.map((e) => [e.h, e.s, e.x]),
    [
      ["", "X", "導入の本文です。"],
      ["attn", "注意機構", "Self-Attentionは"],
      ["next", "次", "続き"],
    ],
  );
});
test("distribution ships search, sitemap, OGP and only referenced media", () => {
  const site = path.resolve(
    process.env.ML_LANDSCAPE_SITE || path.join(ROOT, "dist"),
  );
  const pages = pageFiles().map((file) => readPage(file)[0]);
  global.window = {};
  new Function(read(path.join(site, "assets/search-index.js")))();
  const index = global.window.ML_SEARCH_INDEX;
  delete global.window;
  assert.deepEqual(
    new Set(index.map((e) => e.u)),
    new Set(pages.filter((m) => m.status !== "planned").map((m) => m.url)),
  );
  const sitemap = read(path.join(site, "sitemap.xml"));
  for (const meta of pages)
    assert.ok(
      sitemap.includes(
        SITE_URL + (meta.url === "index.html" ? "" : meta.url) + "<",
      ),
      meta.id,
    );
  const vit = load(read(path.join(site, "models/vit.html")));
  assert.equal(vit('link[rel="canonical"]').attr("href"), SITE_URL + "models/vit.html");
  assert.ok(fs.existsSync(path.join(site, "assets/og-image.png")));
  assert.ok(fs.existsSync(path.join(site, "assets/favicon.svg")));
  // Every asset or page media file must be shipped; only notes and raw data may stay unreferenced.
  const shipped = new Set(
    fs.globSync("**/*", { cwd: site }).map((p) => p.split(path.sep).join("/")),
  );
  const unused = fs
    .globSync(["assets/*", "content/*/*/media/*"], { cwd: ROOT })
    .map((p) => p.split(path.sep).join("/"))
    .filter((p) => !shipped.has(p) && !/\.(md|txt|json|pdb)$/.test(p));
  assert.deepEqual(unused, [], "unreferenced media: delete or reference them");
  for (const file of shipped) {
    const size = fs.statSync(path.join(site, file)).size;
    assert.ok(size <= MAX_ASSET_BYTES, file);
  }
});
test("every page component and page script/style is used by its page", () => {
  for (const file of pageFiles()) {
    const dir = path.dirname(file),
      [meta, body] = readPage(file);
    const used = new Set([
      ...[...body.matchAll(/\{\{component:([a-z0-9-]+)\}\}/g)].map((m) => m[1] + ".html"),
      ...[...(meta.scripts || []), ...(meta.styles || [])].map((p) => path.basename(p)),
    ]);
    const components = path.join(dir, "components");
    if (!fs.existsSync(components)) continue;
    for (const name of fs.readdirSync(components))
      assert.ok(used.has(name), `${path.relative(ROOT, components)}/${name} is unused`);
  }
});
