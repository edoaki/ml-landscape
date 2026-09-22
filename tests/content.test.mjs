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
import { pageToc, validatePages } from "../build.mjs";

test("navigation matches content plan, page metadata and hierarchy", () => {
  const nav = YAML.parse(read(path.join(ROOT, "navigation.yml"))),
    ids = nav.flatMap((g) => g.items.map((p) => p.page));
  const plan = read(path.join(ROOT, "docs/content-plan.md"))
    .split("## 2.")[1]
    .split("## 3.")[0];
  const expected = new Set([
    "introduction",
    ...[...plan.matchAll(/\| `([a-z][a-z-]+)` \|/g)].map((m) => m[1]),
  ]);
  assert.deepEqual(new Set(ids), expected);
  assert.equal(ids.length, expected.size);
  assert.deepEqual(
    new Set(pageFiles().map((p) => readPage(p)[0].id)),
    expected,
  );
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
  const pdb = read(path.join(site, "assets/alphafold-P69905-v6.pdb"))
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
