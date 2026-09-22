"""Browser checks for the seven expansion demos; uses local files offline."""
import asyncio
import json
from pathlib import Path
import sys
from playwright.async_api import async_playwright

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0,str(ROOT/'scripts'))
from render_content import read_page
urls={read_page(p)[0]['id']:read_page(p)[0]['url'] for p in (ROOT/'content').glob('*/*/index.md')}
OUT = ROOT / 'docs/verification/expansion-2026-09-20'
STEPS = {
    'language': 3, 'decision-making': 3, 'world-models': 4,
}

async def check():
    OUT.mkdir(parents=True, exist_ok=True)
    report = {'mode': 'file://, offline', 'checks': [], 'errors': []}
    async with async_playwright() as api:
        browser = await api.chromium.launch()
        context = await browser.new_context(offline=True, viewport={'width': 1280, 'height': 1000})
        page = await context.new_page()
        page.on('pageerror', lambda e: report['errors'].append(str(e)))
        async def reveal_demos():
            for detail in await page.locator('main details').all():
                if await detail.locator('.exp-demo').count() and await detail.get_attribute('open') is None:
                    await detail.locator(':scope > summary').click()
        async def visit(id):
            await page.goto((ROOT / 'dist' / urls[id]).as_uri())
            await reveal_demos()
        for id, count in STEPS.items():
            await visit(id)
            root = page.locator('.exp-stepper')
            assert await root.locator('.exp-stage:visible').count() == 1
            assert await root.locator('[data-exp="prev"]').is_disabled()
            for i in range(1, count):
                await root.locator('[data-exp="next"]').click()
                assert (await root.locator('.exp-counter').inner_text()).startswith(f'{i+1} / {count}')
                assert await root.locator('.exp-stage:visible').count() == 1
            assert await root.locator('[data-exp="next"]').is_disabled()
            await root.locator('[data-exp="prev"]').click()
            assert (await root.locator('.exp-counter').inner_text()).startswith(f'{count-1} / {count}')
            await root.locator('[data-exp="reset"]').click()
            assert (await root.locator('.exp-counter').inner_text()).startswith(f'1 / {count}')
            if id == 'world-models':
                assert await root.locator('.exp-stage:visible .exp-position > span').all_text_contents() == ['1', '2', '3', '4', '5']
            await root.scroll_into_view_if_needed()
            await page.wait_for_timeout(350)
            await page.screenshot(path=str(OUT / f'{id}-desktop.png'))
            report['checks'].append(f'{id}: forward/back/reset and end boundaries')

        await visit('fundamentals')
        root = page.locator('.exp-optimization')
        for rate, expected in [('0.1', '1.28'), ('0.75', '0.5'), ('1.1', '2.88')]:
            await root.locator('.exp-rate').select_option(rate)
            assert '0回更新' in await root.locator('.exp-result').inner_text()
            for _ in range(2):
                await root.locator('[data-exp="next"]').click()
            assert f'w＝{expected}、' in await root.locator('.exp-result').inner_text()
        for _ in range(6):
            await root.locator('[data-exp="next"]').click()
        assert await root.locator('[data-exp="next"]').is_disabled()
        assert 'NaN' not in await root.inner_html()
        await root.locator('[data-exp="reset"]').click()
        assert 'w＝2、損失＝4' in await root.locator('.exp-result').inner_text()
        await root.scroll_into_view_if_needed()
        await page.wait_for_timeout(350)
        await page.screenshot(path=str(OUT / 'optimization-desktop.png'))
        report['checks'].append('Optimization: exact two-step results, eight-step limit, rescaling and reset')

        await visit('uncertainty-unknowns')
        root = page.locator('.exp-abstention')
        for value, accepted, error in [(50, 10, '40%'), (80, 6, '33.3%'), (95, 3, '33.3%'), (100, 0, '計算できません')]:
            await root.locator('input').evaluate('(n,v)=>{n.value=v;n.dispatchEvent(new Event("input",{bubbles:true}));}', str(value))
            text = await root.locator('.exp-result').inner_text()
            assert f'自動回答{accepted}/10件' in text and error in text, text
            assert await root.locator('.exp-held').count() == 10 - accepted
        await root.locator('input').focus()
        await page.keyboard.press('ArrowLeft')
        assert await root.locator('input').input_value() == '95'
        await root.scroll_into_view_if_needed()
        await page.screenshot(path=str(OUT / 'uncertainty-desktop.png'))
        report['checks'].append('Abstention: coverage/error counts, all-held edge case and keyboard input')
        await context.close()

        for js in [True, False]:
            context = await browser.new_context(offline=True, java_script_enabled=js,
                viewport={'width': 390, 'height': 844}, reduced_motion='reduce')
            page = await context.new_page()
            page.on('pageerror', lambda e: report['errors'].append(str(e)))
            for id in [*STEPS, 'fundamentals', 'uncertainty-unknowns']:
                await page.goto((ROOT / 'dist' / urls[id]).as_uri())
                await reveal_demos()
                assert not await page.evaluate('document.documentElement.scrollWidth > innerWidth+2'), id
                root = page.locator('.exp-demo')
                if not js:
                    assert await root.locator('.exp-controls:visible').count() == 0
                    if id in STEPS:
                        assert await root.locator('.exp-stage:visible').count() == STEPS[id]
                else:
                    if id in STEPS:
                        assert await root.locator('.exp-stage:visible').evaluate('(n)=>getComputedStyle(n).animationName') == 'none'
                if id in ['fundamentals', 'uncertainty-unknowns', 'world-models']:
                    await root.scroll_into_view_if_needed()
                    await page.screenshot(path=str(OUT / f'{id}-mobile-js{js}.png'))
            report['checks'].append(f'7 demos: mobile, reduced motion, JS={js}, no document overflow')
            await context.close()
        await browser.close()
    (OUT / 'interaction-results.json').write_text(json.dumps(report, ensure_ascii=False, indent=2))
    assert not report['errors'], report['errors']
    print(json.dumps(report, ensure_ascii=False, indent=2))

if __name__ == '__main__':
    asyncio.run(check())
