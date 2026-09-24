/**
 * Report which sources.yml entries still await primary-source verification.
 * With --online, also request every external URL (for CI or a networked machine).
 * This script never edits sources.yml: a reachable URL is not a verified claim.
 */
import fs from "node:fs";
import path from "node:path";
import { parseArgs } from "node:util";
import YAML from "yaml";
import { ROOT, pageFiles, readPage } from "./render-content.mjs";

export const PENDING = /未実施|未確認/;

/** Collect every source with its page, status and whether verification is pending. */
export function collectSources() {
  const rows = [];
  for (const file of pageFiles()) {
    const [meta] = readPage(file);
    const sourceFile = path.join(path.dirname(file), "sources.yml");
    if (!fs.existsSync(sourceFile)) continue;
    const sources = YAML.parse(fs.readFileSync(sourceFile, "utf8")) || {};
    for (const [key, ref] of Object.entries(sources))
      rows.push({
        page: meta.id,
        status: meta.status,
        key,
        url: ref.url,
        pending: !ref.verification || PENDING.test(ref.verification),
      });
  }
  return rows;
}

async function probe(url) {
  const attempt = async (method) => {
    const response = await fetch(url, {
      method,
      redirect: "follow",
      signal: AbortSignal.timeout(20000),
      headers: { "user-agent": "ml-landscape source check" },
    });
    return response.status;
  };
  try {
    const status = await attempt("HEAD");
    // Some publishers reject HEAD; retry those with GET before reporting.
    return status >= 400 ? await attempt("GET") : status;
  } catch (error) {
    return error.name === "TimeoutError" ? "timeout" : error.message;
  }
}

if (import.meta.url === `file://${process.argv[1]}`) {
  const { values } = parseArgs({
    options: { online: { type: "boolean" }, list: { type: "boolean" } },
  });
  const rows = collectSources();
  const byPage = new Map();
  for (const row of rows) {
    const entry = byPage.get(row.page) || { status: row.status, total: 0, pending: 0 };
    entry.total++;
    entry.pending += row.pending;
    byPage.set(row.page, entry);
  }
  const pending = rows.filter((r) => r.pending).length;
  console.log(`Sources awaiting primary-source verification: ${pending}/${rows.length}`);
  for (const [page, { status, total, pending: count }] of [...byPage].sort(
    (a, b) => b[1].pending - a[1].pending,
  ))
    if (count) console.log(`  ${page} (${status}): ${count}/${total}`);
  if (values.list)
    for (const row of rows.filter((r) => r.pending))
      console.log(`  - ${row.page}:${row.key} ${row.url}`);
  if (values.online) {
    const external = rows.filter((r) => /^https?:/.test(r.url));
    const unique = [...new Set(external.map((r) => r.url))];
    const failures = [];
    for (const url of unique) {
      const status = await probe(url);
      if (!(typeof status === "number" && status < 400)) failures.push([url, status]);
    }
    console.log(`Checked ${unique.length} external URLs; ${failures.length} failed.`);
    for (const [url, status] of failures) console.log(`  ${status} ${url}`);
    if (failures.length) process.exitCode = 1;
  }
}
