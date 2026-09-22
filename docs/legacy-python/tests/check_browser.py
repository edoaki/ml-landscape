"""Optional Chromium verification: file://, offline, static fallback and live controls."""
import argparse,asyncio,json
from pathlib import Path
import sys
from playwright.async_api import async_playwright
ROOT=Path(__file__).resolve().parents[1]
sys.path.insert(0,str(ROOT/'scripts'))
from render_content import read_page

async def check(output,site):
 output.mkdir(parents=True,exist_ok=True)
 pages=[read_page(p)[0] for p in sorted((ROOT/'content').glob('*/*/index.md'))]
 urls={meta['id']:meta['url'] for meta in pages}
 report={'site':str(site),'mode':'file://; network offline','pages':len(pages),'views':[],'interactions':[],'errors':[]}
 async with async_playwright() as api:
  browser=await api.chromium.launch()
  for js,width in [(True,1440),(True,390),(False,390),(False,1440)]:
   context=await browser.new_context(viewport={'width':width,'height':1000},java_script_enabled=js,offline=True,reduced_motion='reduce')
   page=await context.new_page();errors=[]
   page.on('pageerror',lambda e:errors.append(str(e)))
   for meta in pages:
    await page.goto((site/meta['url']).as_uri());await page.wait_for_timeout(30)
    assert await page.locator('h1').count()==1,meta['id']
    assert await page.locator('h1').is_visible(),meta['id']
    if not js:
     assert await page.locator('.sidenav').is_visible(),meta['id']
     if meta['id']=='llm':assert await page.locator('.tf-static').is_visible()
    overflow=await page.evaluate('document.documentElement.scrollWidth > innerWidth + 2')
    if overflow:report['errors'].append(f"{meta['id']} / JS={js} / width={width}: document overflow")
    if errors:report['errors'].extend([f"{meta['id']}: {e}" for e in errors]);errors.clear()
    if not js and meta['id'] in ['cnn','llm','gnn','ssm','flow-matching','life-science','video','audio']:
     assert await page.locator('main svg,main img').count()>0,meta['id']
     if meta['id'] in ['cnn','gnn']:assert await page.locator('.katex-mathml math').count()>0,meta['id']
    if (js,width,meta['id']) in [(True,1440,'llm'),(True,1440,'cnn'),(True,1440,'life-science'),(True,390,'recommendation'),(False,390,'llm'),(False,390,'audio'),(True,390,'video')]:
     target={'llm':'#representations','cnn':'#convolution','life-science':'#protein','recommendation':'#rec-netflix','audio':'#tts','video':'#video'}[meta['id']]
     await page.locator(target).scroll_into_view_if_needed();await page.screenshot(path=str(output/f"{meta['id']}-{width}-js{js}.png"))
   report['views'].append({'javascript':js,'width':width,'pages_checked':len(pages)})
   await context.close()
  (output/'browser-results.json').write_text(json.dumps(report,ensure_ascii=False,indent=2))
  assert not report['errors'],report['errors']
  context=await browser.new_context(viewport={'width':1440,'height':1000},offline=True,reduced_motion='reduce');page=await context.new_page()
  page.on('pageerror',lambda e:report['errors'].append(str(e)))
  async def visit(id):await page.goto((site/urls[id]).as_uri())
  async def change(selector,value):
   await page.locator(selector).evaluate('(n,v)=>{n.value=v;n.dispatchEvent(new Event("input",{bubbles:true}));}',str(value))
  await visit('cnn');await page.locator('.conv-stride').select_option('2');await page.locator('.conv-padding').select_option('1')
  assert await page.locator('.conv-output .cell').count()>0
  report['interactions'].append('CNN: stride/padding recalculation')
  await visit('llm');await page.locator('[data-layer="6"]').click()
  assert await page.locator('.tf-counter').inner_text()=='NEXT TOKEN'
  await page.locator('[data-layer="1"]').click();assert await page.locator('.tf-counter').inner_text()=='EMBEDDING'
  report['interactions'].append('LLM: next-token stage and embedding stage')
  await visit('gnn');await page.locator('.gnn-replay').first.click();await page.wait_for_function('!document.querySelector(".gnn-replay").disabled')
  report['interactions'].append('GNN: calculation replay with reduced motion')
  await visit('timeseries');await page.locator('#ts-method').select_option('last');await page.locator('#ts-reveal').click()
  assert await page.locator('#ts-reveal').get_attribute('aria-pressed')=='true'
  await page.locator('#ts-event').select_option('shift');await change('#ts-threshold',5)
  assert '5' in await page.locator('#ts-threshold-value').inner_text()
  report['interactions'].append('Timeseries: forecast selection, observations, anomaly pattern and threshold')
  await visit('audio');await page.locator('[data-track="melody"]').click()
  assert 'melody' in await page.locator('.audio-switch audio').get_attribute('src')
  assert await page.locator('[data-track="melody"]').get_attribute('aria-pressed')=='true'
  await page.locator('.audio-switch audio').evaluate('(a)=>a.load()');await page.wait_for_timeout(200)
  assert await page.locator('.audio-switch audio').evaluate('(a)=>a.readyState')>=1
  await page.locator('.audio-switch audio').evaluate('(a)=>a.play()')
  await page.wait_for_timeout(250)
  at=await page.locator('.audio-switch audio').evaluate('(a)=>a.currentTime')
  assert at>0
  await page.locator('[data-track="backing"]').click();await page.wait_for_timeout(150)
  resumed=await page.locator('.audio-switch audio').evaluate('(a)=>a.currentTime')
  assert abs(resumed-at)<1
  await page.locator('.audio-switch audio').evaluate('(a)=>a.pause()')
  report['interactions'].append('Audio: offline playback, melody/backing switch and position continuity')
  await visit('ssm');await page.locator('.ssm-next').last.click();await page.locator('.ssm-reset').last.click()
  report['interactions'].append('SSM: next/reset; detailed timeline tested by test_ssm_animation.cjs')
  await visit('flow-matching');before=await page.locator('.fm-status').inner_text();await page.locator('[data-action="next"]').click()
  assert before!=await page.locator('.fm-status').inner_text()
  await page.locator('[data-action="reset"]').click();report['interactions'].append('Flow Matching: frame advance/reset')
  await visit('video')
  if await page.locator('[data-frame-step="1"]').count():
   await page.locator('[data-frame-step="1"]').first.click();assert '30' in await page.locator('.frame-status').first.inner_text()
   report['interactions'].append('Video: stored result frame switching')
  await visit('spatial');video=page.locator('video').first
  await video.evaluate('(v)=>v.load()')
  await page.wait_for_function('document.querySelector("video").readyState >= 2')
  await video.evaluate('(v)=>v.play()');await page.wait_for_timeout(250)
  assert await video.evaluate('(v)=>v.currentTime')>0
  await video.evaluate('(v)=>v.pause()');report['interactions'].append('NeRF: offline video decode and playback')
  await visit('life-science');before=await page.locator('.protein-plot').inner_html();await change('[data-demo="protein"] input',60)
  assert before!=await page.locator('.protein-plot').inner_html();report['interactions'].append('Protein: coordinate rotation')
  await visit('science');await change('.science-progress',80)
  assert await page.locator('.science-motion-status').inner_text();report['interactions'].append('Science: wave animation slider')
  await context.close();await browser.close()
 (output/'browser-results.json').write_text(json.dumps(report,ensure_ascii=False,indent=2))
 print(json.dumps(report,ensure_ascii=False,indent=2));assert not report['errors'],report['errors']

if __name__=='__main__':
 parser=argparse.ArgumentParser();parser.add_argument('--output',type=Path,default=ROOT/'docs/verification/restructure-2026-09-20');parser.add_argument('--site',type=Path,default=ROOT/'dist');args=parser.parse_args();asyncio.run(check(args.output,args.site.resolve()))
