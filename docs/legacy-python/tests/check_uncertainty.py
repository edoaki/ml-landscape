"""Offline interaction and responsive checks for uncertainty diagrams."""
import asyncio
from pathlib import Path
from playwright.async_api import async_playwright

ROOT = Path(__file__).resolve().parents[1]
OUT = ROOT / 'docs/verification/uncertainty-2026-09-20'

async def main():
    OUT.mkdir(parents=True, exist_ok=True)
    errors = []
    async with async_playwright() as api:
        browser = await api.chromium.launch()
        for width, js in [(1280, True), (390, True), (390, False)]:
            context = await browser.new_context(viewport={'width': width, 'height': 960}, java_script_enabled=js, offline=True)
            page = await context.new_page()
            page.on('pageerror', lambda e: errors.append(str(e)))
            await page.goto((ROOT / 'dist/questions/uncertainty-unknowns.html').as_uri())
            assert not await page.evaluate('document.documentElement.scrollWidth > innerWidth')
            assert await page.locator('.unc-figure').count() == 4
            demo = page.locator('.exp-abstention')
            if js:
                expected = [(50,10,4), (55,10,4), (60,9,3), (65,8,3), (70,7,2), (75,7,2), (80,6,2), (85,5,1), (90,4,1), (95,3,1), (100,0,0)]
                for value, accepted, incorrect in expected:
                    await demo.locator('input').fill(str(value))
                    assert await demo.locator('.unc-accepted .exp-case').count() == accepted
                    assert await demo.locator('.unc-held-cases .exp-case').count() == 10-accepted
                    assert await demo.locator('.unc-accepted [data-correct="0"]').count() == incorrect
                    text = await demo.locator('.exp-result').inner_text()
                    assert f'自動回答{accepted}/10件' in text
                    rate = f'{incorrect/accepted*100:.1f}'.removesuffix('.0')+'%' if accepted else '計算できません'
                    assert rate in text
                await demo.locator('input').focus()
                await page.keyboard.press('ArrowLeft')
                assert await demo.locator('input').input_value() == '95'
                for preset in ['50','100','80']:
                    await demo.locator(f'[data-threshold="{preset}"]').click()
                    assert await demo.locator('input').input_value() == preset
                    assert await demo.locator(f'[data-threshold="{preset}"]').get_attribute('aria-pressed') == 'true'
                assert await demo.locator('.unc-accepted [data-confidence="0.8"]').count() == 1
                assert '95%' in await demo.locator('.unc-observation').inner_text()
            else:
                assert await demo.locator('.exp-controls').is_hidden()
                assert await demo.locator('.unc-accepted .exp-case').count() == 10
                assert '40%' in await demo.locator('.unc-risk').inner_text()
            await page.screenshot(path=str(OUT / f'page-{width}-js{js}.png'), full_page=True)
            await demo.screenshot(path=str(OUT / f'demo-{width}-js{js}.png'))
            for i, fig in enumerate(await page.locator('.unc-figure').all()):
                await fig.screenshot(path=str(OUT / f'figure-{i}-{width}-js{js}.png'))
            await context.close()
        await browser.close()
    assert not errors, errors
    print('PASS: all 11 thresholds, boundary inclusion, presets, keyboard, offline, 4 diagrams, mobile, JS-disabled, no overflow/errors')

if __name__ == '__main__':
    asyncio.run(main())
