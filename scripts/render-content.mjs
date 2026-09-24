/** Compile page-local Markdown without a Python runtime or build-time network. */
import fs from "node:fs";
import path from "node:path";
import { fileURLToPath } from "node:url";
import { createRequire } from "node:module";
import MarkdownIt from "markdown-it";
import attrs from "markdown-it-attrs";
import cjkFriendly from "markdown-it-cjk-friendly";
import YAML from "yaml";
import { decodeHTML } from "entities";
import { load } from "cheerio";
const require = createRequire(import.meta.url);
const katex = require("../source/katex.min.cjs");
export const ROOT = path.resolve(
  path.dirname(fileURLToPath(import.meta.url)),
  "..",
);
export const esc = (value) =>
  String(value).replace(
    /[&<>"']/g,
    (c) =>
      ({
        "&": "&amp;",
        "<": "&lt;",
        ">": "&gt;",
        '"': "&quot;",
        "'": "&#x27;",
      })[c],
  );
export const read = (file) => fs.readFileSync(file, "utf8");
export function readPage(file) {
  const match = read(file).match(
    /^---\r?\n([\s\S]*?)\r?\n---(?:\r?\n|$)([\s\S]*)$/,
  );
  if (!match) throw new Error(`${file}: missing front matter`);
  return [YAML.parse(match[1]), match[2]];
}
export function pageFiles() {
  return fs
    .globSync("content/*/*/index.md", { cwd: ROOT })
    .sort()
    .map((p) => path.join(ROOT, p));
}
const md = new MarkdownIt({ html: true }).use(attrs).use(cjkFriendly);
// Python-Markdown allowed emphasis around standalone symbols such as arrows.
md.inline.ruler.before("emphasis", "symbol_strong", (state, silent) => {
  const match = state.src.slice(state.pos).match(/^\*\*([\p{S}]+)\*\*/u);
  if (!match) return false;
  if (!silent) {
    state.push("strong_open", "strong", 1);
    state.push("text", "", 0).content = match[1];
    state.push("strong_close", "strong", -1);
  }
  state.pos += match[0].length;
  return true;
});
const mathCache = new Map();
export function mathHTML(tex) {
  if (!mathCache.has(tex))
    mathCache.set(
      tex,
      '<div class="equation" tabindex="0" aria-label="数式（横にスクロールできます）">' +
        katex.renderToString(tex, {
          displayMode: true,
          output: "htmlAndMathml",
          throwOnError: true,
          strict: "error",
          trust: false,
        }) +
        "</div>",
    );
  return mathCache.get(tex);
}
// Preserve the existing md_in_html authoring syntax, including nested containers.
function markdownHTML(body) {
  const stash = [];
  const hold = (value) => {
    const key = `MLHTMLBLOCK${stash.length}END`;
    stash.push([key, value]);
    return `\n\n${key}\n\n`;
  };
  const opening = /<([a-z][a-z0-9]*)\b[^>]*\smarkdown="1"[^>]*>/i;
  for (let match; (match = opening.exec(body));) {
    const tags = new RegExp(`<\\/?${match[1]}\\b[^>]*>`, "gi");
    tags.lastIndex = match.index + match[0].length;
    let depth = 1,
      end;
    while ((end = tags.exec(body))) {
      if (end[0].startsWith("</")) depth--;
      else if (!end[0].endsWith("/>")) depth++;
      if (!depth) break;
    }
    if (depth) throw new Error(`Unclosed Markdown container: ${match[0]}`);
    const inner = body.slice(match.index + match[0].length, end.index);
    const value =
      match[0].replace(/\smarkdown="1"/, "") +
      "\n" +
      markdownHTML(inner) +
      end[0];
    body =
      body.slice(0, match.index) + hold(value) + body.slice(tags.lastIndex);
  }
  let out = md.render(body);
  for (const [key, value] of stash)
    out = out.replaceAll(`<p>${key}</p>`, value).replaceAll(key, value);
  return out;
}
export function rewriteReferences(html, fn) {
  return html.replace(
    /\b(href|src|poster)="([^"]+)"/g,
    (_, attr, value) => `${attr}="${esc(fn(decodeHTML(value)))}"`,
  );
}
// Components draw on a light ground; the dark theme keeps them light (see style.css).
function lightIsland(html) {
  const $ = load(html, null, false);
  const roots = $.root().children().not("script,style,link");
  if (!roots.length) return html;
  roots.addClass("light-island");
  return $.html();
}
export function render(file, body, registry) {
  const sourceFile = path.join(path.dirname(file), "sources.yml");
  const sources = fs.existsSync(sourceFile)
    ? YAML.parse(read(sourceFile)) || {}
    : {};
  const stash = [];
  const hold = (value) => {
    const key = `MLPLACEHOLDER${stash.length}END`;
    stash.push([key, value]);
    return `\n\n${key}\n\n`;
  };
  body = body.replace(/\{\{component:([^}]+)\}\}/g, (_, name) => {
    if (!/^[a-z0-9-]+$/.test(name))
      throw new Error(`${file}: invalid component ${name}`);
    return hold(
      lightIsland(
        read(path.join(path.dirname(file), "components", name + ".html")),
      ),
    );
  });
  body = body.replace(/^\$\$\r?\n([\s\S]*?)\r?\n\$\$$/gm, (_, tex) =>
    hold(mathHTML(tex)),
  );
  let out = markdownHTML(body);
  for (const [key, value] of stash)
    out = out.replaceAll(`<p>${key}</p>`, value).replaceAll(key, value);
  return rewriteReferences(out, (value) => {
    if (value.startsWith("page:")) {
      const [id, ...fragment] = value.slice(5).split("#");
      if (!registry[id]) throw new Error(`${file}: unknown page ${id}`);
      return (
        registry[id].url + (fragment.length ? "#" + fragment.join("#") : "")
      );
    }
    if (value.startsWith("source:")) {
      const key = value.slice(7);
      if (!sources[key]?.url) throw new Error(`${file}: unknown source ${key}`);
      return sources[key].url;
    }
    if (value.startsWith("media:"))
      return path
        .relative(ROOT, path.join(path.dirname(file), "media", value.slice(6)))
        .split(path.sep)
        .join("/");
    return value;
  });
}
