import asyncio
from pathlib import Path
from playwright.async_api import async_playwright
ROOT = Path(__file__).resolve().parents[1]
async def main():
 out=(ROOT / 'docs/verification/federated-2026-09-20');out.mkdir(exist_ok=True)
 async with async_playwright() as p:
  browser=await p.chromium.launch()
  for js in [False,True]:
   for width in [320,390,1440]:
    page=await browser.new_page(viewport={'width':width,'height':1000},java_script_enabled=js,offline=True)
    errors=[]
    page.on('pageerror',lambda e: errors.append(str(e)))
    await page.goto((ROOT / 'dist/questions/federated-learning.html').as_uri())
    assert not await page.evaluate('document.documentElement.scrollWidth > innerWidth + 2')
    assert await page.locator('.fed-figure').count()==1
    assert await page.locator('.fed-step').count()==3
    for figure in await page.locator('.fed-figure').all(): assert await figure.is_visible()
    assert await page.get_by_role('button',name='次の段階').count()==0
    assert not errors,errors
    if not js and width in [390,1440]:
     for i,figure in enumerate(await page.locator('.fed-figure').all()): await figure.screenshot(style='header { visibility: hidden !important; }', path=str(out/f'figure-{i+1}-{width}.png'))
    await page.close()
  await browser.close()
 print('PASS: 320/390/1440px, JS on/off, offline, 1 figure and 3 visible stages, no overflow or JS errors')
asyncio.run(main())
