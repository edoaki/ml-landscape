import asyncio,json
from pathlib import Path
from playwright.async_api import async_playwright
ROOT=Path(__file__).resolve().parents[3];OUT=Path(__file__).resolve().parent;OUT.mkdir(parents=True,exist_ok=True)
async def run():
 report={'checks':[],'errors':[]}
 async with async_playwright() as p:
  browser=await p.chromium.launch()
  for width,js in [(1440,True),(390,True),(390,False),(1440,False)]:
   ctx=await browser.new_context(viewport={'width':width,'height':1000},java_script_enabled=js,offline=True)
   page=await ctx.new_page();page.on('pageerror',lambda e:report['errors'].append(str(e)))
   for name in ['language','multimodal']:
    await page.goto((ROOT/f'dist/fields/{name}.html').as_uri())
    assert await page.locator('.lesson-visual').count()==4
    assert not await page.evaluate('document.documentElement.scrollWidth > innerWidth + 2'),(name,width,js)
    for el in await page.locator('.lesson-visual').all():
     assert await el.is_visible()
     assert await el.evaluate('(e)=>e.scrollWidth <= e.clientWidth+2')
    if js:
     await page.screenshot(path=str(OUT/f'{name}-{width}.png'),full_page=True)
     await page.locator('.lesson-visual').first.screenshot(path=str(OUT/f'{name}-figure-{width}.png'))
    if name=='language':
     await page.locator('main details summary').click()
     if js:
      root=page.locator('.exp-stepper')
      for expected in [2,3]:
       await root.locator('[data-exp="next"]').click()
       assert (await root.locator('.exp-counter').inner_text()).startswith(str(expected)+' / 3')
      await root.locator('[data-exp="reset"]').click()
      assert (await root.locator('.exp-counter').inner_text()).startswith('1 / 3')
     else: assert await page.locator('.exp-stage:visible').count()==3
    report['checks'].append(f'{name}: {width}px, JS={js}, offline, figures visible, no overflow'+(', RAG steps verified' if name=='language' else ''))
   await ctx.close()
  await browser.close()
 assert not report['errors'],report
 (OUT/'results.json').write_text(json.dumps(report,ensure_ascii=False,indent=2));print(json.dumps(report,ensure_ascii=False,indent=2))
asyncio.run(run())
