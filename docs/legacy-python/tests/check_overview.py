"""Check optional detail disclosure, direct anchors and responsive layout offline."""
from pathlib import Path
import asyncio,json
from playwright.async_api import async_playwright
R=Path(__file__).resolve().parents[1];out=R/'docs/verification/overview-2026-09-20'
async def main():
 out.mkdir(parents=True,exist_ok=True)
 report=[]
 async with async_playwright() as p:
  browser=await p.chromium.launch()
  for js in [True,False]:
   for width in [1440,390]:
    ctx=await browser.new_context(viewport={'width':width,'height':1000},java_script_enabled=js,offline=True,reduced_motion='reduce')
    page=await ctx.new_page()
    for url in ['basics/learning','basics/fundamentals','fields/decision-making','fields/language','questions/efficiency','questions/representation-learning','fields/science']:
     await page.goto((R/'dist'/(url+'.html')).as_uri())
     for summary in await page.locator('main details > summary').all():
      # Open outer details before nested controls.
      await summary.click()
     assert not await page.evaluate('document.documentElement.scrollWidth > innerWidth+2'),(url,js,width)
     assert await page.locator('main details:not([open])').count()==0,(url,js,width)
     report.append([url,js,width,'details open; no page overflow'])
    await page.goto((R/'dist/questions/efficiency.html').as_uri()+'#longformer')
    if js: assert await page.locator('#longformer').is_visible()
    if js and width==1440:
     await page.screenshot(path=str(out/'efficiency-detail-desktop.png'))
     await page.goto((R/'dist/basics/learning.html').as_uri())
     await page.screenshot(path=str(out/'learning-overview-desktop.png'))
     await page.goto((R/'dist/fields/language.html').as_uri());await page.locator('#language-evaluation').scroll_into_view_if_needed()
     await page.screenshot(path=str(out/'language-overview-desktop.png'))
    if js and width==390:
     await page.goto((R/'dist/fields/decision-making.html').as_uri());await page.locator('#logs-task').scroll_into_view_if_needed()
     await page.screenshot(path=str(out/'decision-overview-mobile.png'))
    await ctx.close()
  await browser.close()
 (out/'supplement-results.json').write_text(json.dumps(report,ensure_ascii=False,indent=2));print('Passed',len(report),'supplement views and JS fragment links')
asyncio.run(main())
