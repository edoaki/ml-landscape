/** Offline file:// verification; run npm run browser:install once beforehand. */
import assert from "node:assert/strict";
import fs from "node:fs";
import path from "node:path";
import { pathToFileURL } from "node:url";
import { parseArgs } from "node:util";
import { chromium } from "playwright";
import { ROOT, pageFiles, readPage } from "../scripts/render-content.mjs";
import { lowContrastText } from "./contrast.mjs";
const { values } = parseArgs({
  options: {
    site: { type: "string", default: path.join(ROOT, "dist") },
    output: {
      type: "string",
      default: path.join(ROOT, "test-results/browser"),
    },
  },
});
const site = path.resolve(values.site),
  output = path.resolve(values.output);
fs.mkdirSync(output, { recursive: true });
const pages = pageFiles().map((f) => readPage(f)[0]),
  urls = Object.fromEntries(pages.map((m) => [m.id, m.url]));
const report = {
  mode: "file://; offline",
  pages: pages.length,
  views: [],
  interactions: [],
  errors: [],
};
// CHROMIUM_PATH lets preinstalled Chromium builds run the same checks.
const browser = await chromium.launch(
  process.env.CHROMIUM_PATH ? { executablePath: process.env.CHROMIUM_PATH } : {},
);
try {
  for (const js of [true, false])
    for (const width of [1440, 390, 320]) {
      const ctx = await browser.newContext({
        viewport: { width, height: 1000 },
        javaScriptEnabled: js,
        offline: true,
        reducedMotion: "reduce",
      });
      const page = await ctx.newPage();
      page.on("pageerror", (e) => report.errors.push(String(e)));
      for (const meta of pages) {
        await page.goto(pathToFileURL(path.join(site, meta.url)).href);
        assert.equal(await page.locator("h1").count(), 1, meta.id);
        assert.ok(await page.locator("h1").isVisible(), meta.id);
        assert.ok(
          !(await page.evaluate(
            () => document.documentElement.scrollWidth > innerWidth + 2,
          )),
          `${meta.id}: overflow ${width} JS=${js}`,
        );
        assert.equal(await page.locator(".katex-error").count(), 0, meta.id);
        if (!js) {
          assert.ok(await page.locator(".sidenav").isVisible());
          if (meta.id === "llm")
            assert.ok(await page.locator(".tf-static").isVisible());
        }
        // Open all optional explanations and verify their responsive layout too.
        for (const summary of await page
          .locator("main details > summary")
          .all())
          if (await summary.isVisible()) await summary.click();
        assert.ok(
          !(await page.evaluate(
            () => document.documentElement.scrollWidth > innerWidth + 2,
          )),
          `${meta.id}: expanded overflow ${width} JS=${js}`,
        );
        if (
          ["introduction", "information-geometry", "transformer"].includes(
            meta.id,
          ) &&
          width === 390 &&
          !js
        )
          await page.screenshot({
            path: path.join(output, `${meta.id}-390-static.png`),
          });
      }
      report.views.push({ javascript: js, width, pages: pages.length });
      console.log(
        `Checked ${pages.length} pages: width=${width}, JavaScript=${js}`,
      );
      await ctx.close();
    }
  const ctx = await browser.newContext({
    viewport: { width: 1440, height: 1000 },
    offline: true,
    reducedMotion: "reduce",
  });
  const page = await ctx.newPage();
  page.on("pageerror", (e) => report.errors.push(String(e)));
  const visit = async (id) => {
    await page.goto(pathToFileURL(path.join(site, urls[id])).href);
    for (const detail of await page.locator("main details").all())
      if ((await detail.getAttribute("open")) === null)
        await detail.locator(":scope > summary").click();
  };
  const change = async (selector, value) =>
    page.locator(selector).evaluate((n, v) => {
      n.value = v;
      n.dispatchEvent(new Event("input", { bubbles: true }));
    }, String(value));
  // Both repository and standalone distribution entry points must work directly.
  for (const entry of [
    path.join(ROOT, "index.html"),
    path.join(site, "index.html"),
  ]) {
    await page.goto(pathToFileURL(entry).href);
    assert.equal(await page.locator("h1").innerText(), "機械学習とは");
    assert.equal(await page.locator(".intro-figure").count(), 4);
    for (const [animal, scene, expected, correct] of [
      ["cat", "indoor", "猫", true],
      ["cat", "outdoor", "犬", false],
      ["dog", "indoor", "猫", false],
      ["dog", "outdoor", "犬", true],
    ]) {
      await page.locator(`[data-select-animal="${animal}"]`).click();
      await page.locator(`[data-select-scene="${scene}"]`).click();
      assert.equal(
        await page.locator("[data-background-result]").innerText(),
        expected + (correct ? " · 正解" : " · 不正解"),
      );
      assert.equal(
        await page.locator("[data-shape-result]").innerText(),
        (animal === "cat" ? "猫" : "犬") + " · 正解",
      );
    }
  }
  report.interactions.push(
    "Both entry points; all introduction animal/background states",
  );
  await visit("cnn");
  await page.locator(".conv-stride").selectOption("2");
  await page.locator(".conv-padding").selectOption("1");
  assert.ok((await page.locator(".conv-output .cell").count()) > 0);
  await visit("llm");
  await page.locator('[data-layer="6"]').click();
  assert.equal(await page.locator(".tf-counter").innerText(), "NEXT TOKEN");
  await page.locator('[data-layer="1"]').click();
  assert.equal(await page.locator(".tf-counter").innerText(), "EMBEDDING");
  for (let i = 0; i < 5; i++) await page.locator("[data-next]").click();
  assert.deepEqual(await page.locator(".ld-token").allTextContents(), [
    "私は",
    "猫",
    "が",
    "好き",
    "です",
    "終了",
  ]);
  assert.ok(await page.locator("[data-next]").isDisabled());
  assert.ok(await page.locator("[data-play]").isDisabled());
  await page.locator("[data-reset]").click();
  await page.locator("#ar-demo select").selectOption("犬");
  await page.locator("[data-play]").click();
  assert.deepEqual(await page.locator(".ld-token").allTextContents(), [
    "私は",
    "犬",
  ]);
  assert.ok((await page.locator(".ld-candidate").innerText()).includes("80%"));
  await visit("gnn");
  await page.locator(".gnn-replay").first().click();
  await page.waitForFunction(
    () => !document.querySelector(".gnn-replay").disabled,
  );
  await visit("timeseries");
  await page.locator("#ts-method").selectOption("last");
  await page.locator("#ts-reveal").click();
  assert.equal(
    await page.locator("#ts-reveal").getAttribute("aria-pressed"),
    "true",
  );
  await page.locator("#ts-event").selectOption("shift");
  await change("#ts-threshold", 5);
  assert.ok(
    (await page.locator("#ts-threshold-value").innerText()).includes("5"),
  );
  await visit("ssm");
  await page.locator(".ssm-next").last().click();
  await page.locator(".ssm-reset").last().click();
  await visit("flow-matching");
  const before = await page.locator(".fm-status").innerText();
  await page.locator('[data-action="next"]').click();
  assert.notEqual(before, await page.locator(".fm-status").innerText());
  await page.locator('[data-action="reset"]').click();
  await visit("life-science");
  const protein = await page.locator(".protein-plot").innerHTML();
  await change('[data-demo="protein"] input', 60);
  assert.notEqual(protein, await page.locator(".protein-plot").innerHTML());
  await visit("science");
  await change(".science-progress", 80);
  assert.ok(await page.locator(".science-motion-status").innerText());
  report.interactions.push(
    "CNN, LLM, GNN, timeseries, SSM, Flow Matching, protein and science controls",
  );
  await visit("audio");
  await page.locator('[data-track="melody"]').click();
  const audio = page.locator(".audio-switch audio");
  assert.ok((await audio.getAttribute("src")).includes("melody"));
  await audio.evaluate((a) => a.load());
  await page.waitForFunction(
    () => document.querySelector(".audio-switch audio").readyState >= 2,
  );
  await audio.evaluate((a) => a.play());
  await page.waitForFunction(
    () => document.querySelector(".audio-switch audio").currentTime > 0,
  );
  const at = await audio.evaluate((a) => a.currentTime);
  assert.ok(at > 0);
  await page.locator('[data-track="backing"]').click();
  await page.waitForTimeout(150);
  assert.ok(Math.abs((await audio.evaluate((a) => a.currentTime)) - at) < 1);
  await audio.evaluate((a) => a.pause());
  await visit("spatial");
  // Open-source Chromium builds ship without H.264; playback cannot be checked there.
  const h264 = await page.evaluate(
    () =>
      document
        .createElement("video")
        .canPlayType('video/mp4; codecs="avc1.42E01E"') !== "",
  );
  if (h264) {
    const video = page.locator("video").first();
    await video.evaluate((v) => v.play());
    await page.waitForTimeout(250);
    assert.ok((await video.evaluate((v) => v.currentTime)) > 0);
    await video.evaluate((v) => v.pause());
  } else report.skipped = ["H.264 video playback (browser lacks the codec)"];
  await visit("video");
  if (await page.locator('[data-frame-step="1"]').count()) {
    await page.locator('[data-frame-step="1"]').first().click();
    assert.ok(
      (await page.locator(".frame-status").first().innerText()).includes("30"),
    );
  }
  report.interactions.push(
    "Offline audio/video playback, track continuity and stored video frames",
  );
  for (const [id, count] of Object.entries({
    language: 3,
    "decision-making": 3,
    "world-models": 4,
  })) {
    await visit(id);
    for (const detail of await page.locator("main details").all())
      if (
        (await detail.locator(".exp-demo").count()) &&
        (await detail.getAttribute("open")) === null
      )
        await detail.locator(":scope > summary").click();
    const root = page.locator(".exp-stepper");
    assert.ok(await root.locator('[data-exp="prev"]').isDisabled());
    for (let i = 1; i < count; i++) {
      await root.locator('[data-exp="next"]').click();
      assert.ok(
        (await root.locator(".exp-counter").innerText()).startsWith(
          `${i + 1} / ${count}`,
        ),
      );
      assert.equal(await root.locator(".exp-stage:visible").count(), 1);
    }
    assert.ok(await root.locator('[data-exp="next"]').isDisabled());
    await root.locator('[data-exp="prev"]').click();
    assert.ok(
      (await root.locator(".exp-counter").innerText()).startsWith(
        `${count - 1} / ${count}`,
      ),
    );
    await root.locator('[data-exp="reset"]').click();
    assert.ok(
      (await root.locator(".exp-counter").innerText()).startsWith(
        `1 / ${count}`,
      ),
    );
  }
  await visit("fundamentals");
  const optimization = page.locator(".exp-optimization");
  for (const [rate, expected] of [
    ["0.1", "1.28"],
    ["0.75", "0.5"],
    ["1.1", "2.88"],
  ]) {
    await optimization.locator(".exp-rate").selectOption(rate);
    for (let i = 0; i < 2; i++)
      await optimization.locator('[data-exp="next"]').click();
    assert.ok(
      (await optimization.locator(".exp-result").innerText()).includes(
        `w＝${expected}、`,
      ),
    );
  }
  for (let i = 0; i < 6; i++)
    await optimization.locator('[data-exp="next"]').click();
  assert.ok(await optimization.locator('[data-exp="next"]').isDisabled());
  await optimization.locator('[data-exp="reset"]').click();
  assert.ok(
    (await optimization.locator(".exp-result").innerText()).includes(
      "w＝2、損失＝4",
    ),
  );
  await visit("uncertainty-unknowns");
  assert.equal(await page.locator(".unc-figure").count(), 4);
  const abstention = page.locator(".exp-abstention");
  for (const [threshold, accepted, incorrect] of [
    [50, 10, 4],
    [55, 10, 4],
    [60, 9, 3],
    [65, 8, 3],
    [70, 7, 2],
    [75, 7, 2],
    [80, 6, 2],
    [85, 5, 1],
    [90, 4, 1],
    [95, 3, 1],
    [100, 0, 0],
  ]) {
    await abstention.locator("input").fill(String(threshold));
    assert.equal(
      await abstention.locator(".unc-accepted .exp-case").count(),
      accepted,
    );
    assert.equal(
      await abstention.locator(".unc-held-cases .exp-case").count(),
      10 - accepted,
    );
    assert.equal(
      await abstention.locator('.unc-accepted [data-correct="0"]').count(),
      incorrect,
    );
    const text = await abstention.locator(".exp-result").innerText();
    assert.ok(text.includes(`自動回答${accepted}/10件`));
    assert.ok(
      text.includes(
        accepted
          ? Number(((incorrect / accepted) * 100).toFixed(1)) + "%"
          : "計算できません",
      ),
    );
  }
  await abstention.locator("input").focus();
  await page.keyboard.press("ArrowLeft");
  assert.equal(await abstention.locator("input").inputValue(), "95");
  for (const preset of ["50", "100", "80"]) {
    await abstention.locator(`[data-threshold="${preset}"]`).click();
    assert.equal(await abstention.locator("input").inputValue(), preset);
    assert.equal(
      await abstention
        .locator(`[data-threshold="${preset}"]`)
        .getAttribute("aria-pressed"),
      "true",
    );
  }
  report.interactions.push(
    "Stepper boundaries/reset, exact optimization results, all 11 abstention thresholds and keyboard/presets",
  );
  await visit("decision-making");
  await page.locator('[data-move="alone"]').click();
  const robot = page.locator("[data-load]");
  assert.equal(await robot.getAttribute("x1"), "235");
  assert.equal(await robot.getAttribute("x2"), "100");
  await page.locator('[data-move="together"]').click();
  assert.equal(await robot.getAttribute("x1"), "420");
  assert.equal(await robot.getAttribute("x2"), "420");
  await page.locator("[data-reset]").click();
  assert.equal(await robot.getAttribute("x1"), "100");
  await visit("federated-learning");
  assert.equal(await page.locator(".fed-figure").count(), 1);
  assert.equal(await page.locator("#fed-demo .fed-step").count(), 3);
  assert.equal(await page.locator("#fed-demo button").count(), 0);
  await visit("probabilistic-inference");
  assert.deepEqual(
    await page.locator("#bayes-demo .bf-bar-row > strong").allTextContents(),
    ["6.5%", "34.8%", "58.7%"],
  );
  await page.goto(
    pathToFileURL(path.join(site, urls.efficiency)).href + "#longformer",
  );
  assert.ok(await page.locator("#longformer").isVisible());
  report.interactions.push(
    "Robot states/reset, federated static stages, Bayesian values, direct disclosure anchor",
  );
  // Offline search: the index loads over file://, results link to section anchors.
  await visit("introduction");
  await page.keyboard.press("/");
  assert.ok(await page.locator("#search-input").isVisible());
  await page.locator("#search-input").fill("Self-Attention");
  await page.waitForFunction(
    () => document.querySelectorAll(".search-results a").length > 0,
  );
  const hit = page.locator(".search-results a").first();
  assert.match(await hit.getAttribute("href"), /\.html#/);
  await hit.click();
  await page.waitForLoadState();
  assert.ok((await page.locator("main").innerText()).includes("Self-Attention"));
  await page.locator(".search-toggle").click();
  await page.locator("#search-input").fill("存在しない語句ぬぬぬ");
  await page.waitForFunction(() =>
    document.querySelector(".search-status").textContent.includes("見つかりません"),
  );
  await page.keyboard.press("Escape");
  assert.ok(await page.locator(".search-panel").isHidden());
  // Theme toggle remembers an explicit choice across pages.
  await page.locator(".theme-toggle").click();
  assert.equal(await page.locator("html").getAttribute("data-theme"), "dark");
  await visit("cnn");
  assert.equal(await page.locator("html").getAttribute("data-theme"), "dark");
  await page.locator(".theme-toggle").click();
  assert.equal(await page.locator("html").getAttribute("data-theme"), "light");
  report.interactions.push("Search (keyboard, results, anchors, no-hit, Escape) and theme toggle");
  await ctx.close();
  // A dark OS and legacy saved preference must still start with the white design.
  const defaults = await browser.newContext({ colorScheme: "dark" });
  await defaults.addInitScript(() => localStorage.setItem("landscape-theme", "dark"));
  const defaultView = await defaults.newPage();
  await defaultView.goto(pathToFileURL(path.join(site, "index.html")).href);
  assert.equal(await defaultView.locator("html").getAttribute("data-theme"), "light");
  assert.equal(await defaultView.evaluate(() => getComputedStyle(document.documentElement).backgroundColor), "rgb(255, 255, 255)");
  await defaultView.emulateMedia({ colorScheme: "light" });
  await defaultView.emulateMedia({ colorScheme: "dark" });
  assert.equal(await defaultView.locator("html").getAttribute("data-theme"), "light");
  await defaultView.locator(".theme-toggle").click();
  await defaultView.reload();
  assert.equal(await defaultView.locator("html").getAttribute("data-theme"), "dark");
  await defaults.close();
  report.interactions.push("White default despite dark OS and legacy preference; explicit dark choice persists");
  // Text contrast in both explicitly selected themes, with optional explanations expanded.
  for (const colorScheme of ["light", "dark"]) {
    const themed = await browser.newContext({
      viewport: { width: 1440, height: 1000 },
      offline: true,
      reducedMotion: "reduce",
      colorScheme,
    });
    await themed.addInitScript((theme) => localStorage.setItem("landscape-theme-v2", theme), colorScheme);
    const view = await themed.newPage();
    for (const meta of pages) {
      await view.goto(pathToFileURL(path.join(site, meta.url)).href);
      await view.evaluate(() =>
        document.querySelectorAll("details").forEach((d) => (d.open = true)),
      );
      assert.equal(
        await view.locator("html").getAttribute("data-theme"),
        colorScheme,
      );
      assert.deepEqual(
        await view.evaluate(lowContrastText, 3),
        [],
        `${meta.id}: low contrast (${colorScheme})`,
      );
    }
    await themed.close();
  }
  report.interactions.push("Text contrast ≥ 3:1 on all pages in light and dark themes");
  const timed = await browser.newContext({
      offline: true,
      reducedMotion: "no-preference",
    }),
    animation = await timed.newPage();
  animation.on("pageerror", (e) => report.errors.push(String(e)));
  await animation.goto(pathToFileURL(path.join(site, urls.llm)).href);
  await animation.locator("[data-play]").click();
  await animation.waitForFunction(
    () => document.querySelectorAll(".ld-token").length >= 2,
  );
  await animation.locator("[data-play]").click();
  const count = await animation.locator(".ld-token").count();
  await animation.waitForTimeout(1600);
  assert.equal(await animation.locator(".ld-token").count(), count);
  await animation.locator("[data-reset]").click();
  await animation.locator("[data-play]").click();
  await animation.waitForFunction(
    () => document.querySelector("[data-next]").disabled,
    {},
    { timeout: 12000 },
  );
  assert.equal(
    await animation.locator("[data-play]").getAttribute("aria-pressed"),
    "false",
  );
  await animation.goto(
    pathToFileURL(path.join(site, urls["decision-making"])).href,
  );
  await animation.locator('[data-move="together"]').click();
  await animation.waitForFunction(
    () => document.querySelector("[data-load]").getAttribute("x1") === "420",
  );
  await timed.close();
  report.interactions.push(
    "Timed token play/pause/EOS and robot animation completion",
  );
  assert.deepEqual(report.errors, []);
} catch (error) {
  report.errors.push(String(error));
  throw error;
} finally {
  await browser.close();
  fs.writeFileSync(
    path.join(output, "browser-results.json"),
    JSON.stringify(report, null, 2) + "\n",
  );
}
console.log(
  `Passed ${report.views.length * pages.length} offline page views and ${report.interactions.length} interaction groups.` +
    (report.skipped ? ` Skipped: ${report.skipped.join("; ")}.` : ""),
);
