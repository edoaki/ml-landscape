"""Offline layout, static fallback, and numerical/interaction checks for new pages and the consolidated decision-making page."""
import argparse
import asyncio
import json
from pathlib import Path
import sys

from playwright.async_api import async_playwright

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0,str(ROOT/'scripts'))
from render_content import read_page
urls={read_page(p)[0]['id']:read_page(p)[0]['url'] for p in (ROOT/'content').glob('*/*/index.md')}
IDS = 'probabilistic-inference llm recommendation decision-making federated-learning safety fundamentals information-geometry causal-inference evaluation'.split()
DEMOS = {
    'llm': '#ar-demo',
    'decision-making': '#agents-demo',
}


async def check(site, output):
    output.mkdir(parents=True, exist_ok=True)
    report = {'site': str(site), 'offline': True, 'views': [], 'interactions': [], 'errors': []}
    async with async_playwright() as api:
        browser = await api.chromium.launch()
        for js in [False, True]:
            for width in [320, 390, 1440]:
                context = await browser.new_context(viewport={'width': width, 'height': 1000}, java_script_enabled=js, offline=True, reduced_motion='reduce')
                page = await context.new_page()
                page.on('pageerror', lambda error: report['errors'].append(str(error)))
                for id in IDS:
                    await page.goto((site / urls[id]).as_uri())
                    assert await page.locator('main h1').count() == 1, id
                    assert await page.locator('main h2').count() >= (4 if id == 'causal-inference' else 5), id
                    if id == 'causal-inference':
                        assert await page.locator('#causal-demo').count() == 0
                    assert not await page.locator('.publication-status').count(), id
                    assert not await page.evaluate('document.documentElement.scrollWidth > innerWidth + 2'), (id, js, width)
                    assert not await page.locator('.katex-error').count(), id
                    if id == 'probabilistic-inference':
                        assert await page.locator('#bayes-demo button').count() == 0
                        assert await page.locator('#bayes-demo .bf-bar-row > strong').all_text_contents() == ['6.5%', '34.8%', '58.7%']
                        for figure in await page.locator('.bayes-figure').all():
                            assert await figure.locator('figcaption').is_visible()
                            for chart in await figure.locator('svg').all():
                                assert await chart.get_attribute('aria-label')
                                assert await chart.is_visible()
                            if width == 390 and not js:
                                name = await figure.get_attribute('id')
                                await figure.screenshot(path=str(output / f'{name}-390-static.png'))
                    if id == 'information-geometry':
                        for figure in await page.locator('.ig-figure').all():
                            assert await figure.locator('figcaption').is_visible()
                            for chart in await figure.locator('svg').all():
                                assert await chart.get_attribute('aria-label')
                                assert await chart.is_visible()
                            if width == 390 and not js:
                                name = await figure.get_attribute('id')
                                await figure.screenshot(path=str(output / f'{name}-390-static.png'))
                    if id in DEMOS:
                        demo = page.locator(DEMOS[id])
                        assert await demo.locator('figcaption').is_visible(), id
                        assert await demo.locator('.ld-controls').is_visible() == js, id
                        if width == 390 and not js:
                            await demo.screenshot(path=str(output / f'{id}-390-static.png'))
                report['views'].append({'javascript': js, 'width': width, 'pages': len(IDS)})
                await context.close()

        context = await browser.new_context(viewport={'width': 1440, 'height': 1000}, offline=True, reduced_motion='reduce')
        page = await context.new_page()
        page.on('pageerror', lambda error: report['errors'].append(str(error)))

        async def visit(id):
            await page.goto((site / urls[id]).as_uri())

        async def capture(id):
            await page.locator(DEMOS[id]).screenshot(path=str(output / f'{id}-1440-result.png'))

        await visit('llm')
        for _ in range(5):
            await page.locator('[data-next]').click()
        assert await page.locator('.ld-token').all_text_contents() == ['私は', '猫', 'が', '好き', 'です', '終了']
        assert await page.locator('[data-next]').is_disabled()
        assert await page.locator('[data-play]').is_disabled()
        await capture('llm')
        await page.locator('[data-reset]').click()
        await page.locator('#ar-demo select').select_option('犬')
        await page.locator('[data-play]').click()
        assert await page.locator('.ld-token').all_text_contents() == ['私は', '犬']
        assert '80%' in await page.locator('.ld-candidate').inner_text()
        assert await page.locator('[data-play]').get_attribute('aria-pressed') == 'false'
        report['interactions'].append('Autoregression: full sequence, EOS stop, reset, alternate context, reduced-motion step')

        await visit('decision-making')
        await page.locator('[data-move="alone"]').click()
        load = page.locator('[data-load]')
        assert await load.get_attribute('x1') == '235' and await load.get_attribute('x2') == '100'
        await page.locator('[data-move="together"]').click()
        assert await load.get_attribute('x1') == await load.get_attribute('x2') == '420'
        await capture('decision-making')
        await page.locator('[data-reset]').click()
        assert await load.get_attribute('x1') == await load.get_attribute('x2') == '100'
        report['interactions'].append('Agents: alone/together/reset and immediate reduced-motion result')

        await visit('federated-learning')
        assert await page.locator('.fed-figure').count() == 1
        assert await page.locator('#fed-demo .fed-step').count() == 3
        assert await page.locator('#fed-demo button').count() == 0
        assert '設備記録は、各工場の外へ出さない。' in await page.locator('#fed-demo').inner_text()
        await page.locator('#fed-demo').screenshot(path=str(output / 'federated-learning-1440-static.png'))
        report['interactions'].append('Federated: three stages visible without controls; records remain in each factory')

        await context.close()

        # Test real timed animation separately from reduced-motion behavior.
        context = await browser.new_context(offline=True, reduced_motion='no-preference')
        page = await context.new_page()
        page.on('pageerror', lambda error: report['errors'].append(str(error)))
        await visit('llm')
        await page.locator('[data-play]').click()
        await page.wait_for_function('document.querySelectorAll(".ld-token").length >= 2')
        await page.locator('[data-play]').click()
        count = await page.locator('.ld-token').count()
        await page.wait_for_timeout(1600)
        assert await page.locator('.ld-token').count() == count
        await page.locator('[data-reset]').click()
        await page.locator('[data-play]').click()
        await page.wait_for_function('document.querySelector("[data-next]").disabled', timeout=12000)
        assert await page.locator('[data-play]').get_attribute('aria-pressed') == 'false'
        await visit('decision-making')
        await page.locator('[data-move="together"]').click()
        await page.wait_for_function('document.querySelector("[data-load]").getAttribute("x1") === "420"')
        report['interactions'].append('Timed animation: token play/pause/completion; robots reach target')
        await context.close()
        await browser.close()

    (output / 'browser-results.json').write_text(json.dumps(report, ensure_ascii=False, indent=2))
    print(json.dumps(report, ensure_ascii=False, indent=2))
    assert not report['errors'], report['errors']


if __name__ == '__main__':
    parser = argparse.ArgumentParser()
    parser.add_argument('--site', type=Path, default=ROOT/'dist')
    parser.add_argument('--output', type=Path, default=ROOT / 'docs/verification/new-pages-2026-09-20')
    args = parser.parse_args()
    asyncio.run(check(args.site.resolve(), args.output.resolve()))
