/** Fail when the committed index.html or dist/ differ from a fresh build. */
import { execFileSync } from "node:child_process";
import { build } from "../build.mjs";
import { ROOT } from "./render-content.mjs";

build();
const changes = execFileSync(
  "git",
  ["status", "--porcelain", "--untracked-files=all", "--", "index.html", "dist"],
  { cwd: ROOT, encoding: "utf8" },
).trim();
if (changes) {
  console.error("Generated files are out of date; run npm run build and commit:\n" + changes);
  process.exit(1);
}
console.log("index.html and dist/ match the sources.");
