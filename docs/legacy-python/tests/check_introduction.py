"""Offline introduction diagrams, interaction states, and sidebar-only page navigation."""
import asyncio
import json
from pathlib import Path
from bs4 import BeautifulSoup
from playwright.async_api import async_playwright

ROOT = Path(__file__).resolve().parents[1]
OUT = ROOT / 'docs/verification/introduction-2026-09-20'

async def check():
    OUT.mkdir(parents=True, exist_ok=True)
    pages = [ROOT/'index.html', ROOT/'dist/index.html']
    pages += [p for group in ('basics', 'models', 'fields', 'questions') for p in (ROOT/'dist'/group).glob('*.html')]
    for path in pages:
        doc = BeautifulSoup(path.read_text(), 'html5lib')
        assert not doc.select('.pager, #related'), path
        assert not any(h.get_text() in ('この教材について', '次に読む', '関連する説明') for h in doc.select('h2,h3')), path
        assert doc.select_one('#chapter-nav a[aria-current="page"]'), path
    report = {'pages_checked': len(pages), 'views': [], 'errors': []}
    async with async_playwright() as api:
        browser = await api.chromium.launch()
        for entry in ('index.html', 'dist/index.html'):
            for width, js in ((1440, True), (390, True), (320, True), (390, False)):
                context = await browser.new_context(viewport={'width': width, 'height': 1000}, java_script_enabled=js, offline=True)
                page = await context.new_page()
                page.on('pageerror', lambda e: report['errors'].append(str(e)))
                await page.goto((ROOT/entry).as_uri())
                assert await page.locator('h1').inner_text() == '機械学習とは'
                assert await page.locator('.intro-figure').count() == 4
                assert not await page.evaluate('document.documentElement.scrollWidth > innerWidth + 2')
                for figure in await page.locator('.intro-figure').all():
                    assert await figure.evaluate('(n) => n.scrollWidth <= n.clientWidth + 2')
                if js:
                    # Same animal, different backgrounds: a background-only rule flips its answer.
                    for animal, scene, expected, correct in (
                        ('cat', 'indoor', '猫', True), ('cat', 'outdoor', '犬', False),
                        ('dog', 'indoor', '猫', False), ('dog', 'outdoor', '犬', True),
                    ):
                        await page.locator(f'[data-select-animal="{animal}"]').click()
                        await page.locator(f'[data-select-scene="{scene}"]').click()
                        assert await page.locator('[data-background-result]').inner_text() == expected + (' · 正解' if correct else ' · 不正解')
                        assert await page.locator('[data-shape-result]').inner_text() == ('猫' if animal == 'cat' else '犬') + ' · 正解'
                        assert await page.locator(f'[data-select-scene="{scene}"]').get_attribute('aria-pressed') == 'true'
                        assert await page.locator(f'[data-scene="{scene}"]').is_visible()
                    await page.locator('[data-select-animal="cat"]').click()
                    await page.locator('[data-select-scene="outdoor"]').click()
                else:
                    assert await page.locator('.intro-bias-static').is_visible()
                    assert not await page.locator('.intro-bias-controls').is_visible()
                    assert await page.locator('.intro-bias-static tbody tr').count() == 4
                if entry == 'index.html' and js and width in (1440, 390):
                    for i, figure in enumerate(await page.locator('.intro-figure').all()):
                        await figure.screenshot(path=str(OUT/f'figure-{i+1}-{width}.png'))
                report['views'].append({'entry': entry, 'width': width, 'javascript': js})
                await context.close()
        await browser.close()
    assert not report['errors'], report['errors']
    (OUT/'browser-results.json').write_text(json.dumps(report, ensure_ascii=False, indent=2))
    print(json.dumps(report, ensure_ascii=False, indent=2))

if __name__ == '__main__':
    asyncio.run(check())
