"""Reproduce the lesson's numerical examples and inspect the built page offline."""
import asyncio
import json
import math
import sys
from pathlib import Path
from statistics import mean

ROOT = Path(__file__).resolve().parents[3]
OUT = Path(__file__).resolve().parent
sys.path.insert(0, str(ROOT/'scripts'))
from make_classical_figures import assignments


def numeric_checks():
    values = [50,70,90,110,130,150]
    sse = lambda xs: sum((x-mean(xs))**2 for x in xs)
    assert mean(values)==100 and sse(values)==7000
    assert sse(values[:2])+sse(values[2:])==2200
    assert [mean(values[i:i+2]) for i in (0,2,4)]==[60,100,140]
    assert 60+2*(26-20)+40==112
    assert abs(1/(1+math.exp(-1.10))-.75)<.001
    assert 100+.1*30==103
    values=[1,2,4,8,9]
    centers=[1,4]
    groups=assignments(values,centers)
    for expected in ([1.5,7],[7/3,8.5],[7/3,8.5]):
        centers=[mean([v for v,g in zip(values,groups) if g==j]) for j in range(2)]
        assert centers==expected
        groups=assignments(values,centers)
    assert groups==[0,0,0,1,1]
    # Feature map reproduces its kernel for every pair in the example.
    for x in range(-2,3):
        assert (x*x>2.5)==(abs(x)==2)
        for other in range(-2,3):
            assert sum(a*b for a,b in zip((x,x*x),(other,other*other)))==x*other+x*x*other*other
    # Projection keeps the parallel component and discards an orthogonal residual.
    axis=(.8,.6); original=(3,1)
    coord=sum(x*a for x,a in zip(original,axis))
    restored=[coord*a for a in axis]
    assert math.isclose(sum(a*a for a in axis),1) and math.isclose(coord,3)
    assert all(math.isclose(v,e) for v,e in zip(restored,[2.4,1.8]))
    assert abs(sum((x-y)*a for x,y,a in zip(original,restored,axis)))<1e-12
    assert 2*1+1*.5==2.5 and 2*1*1.5+1*.5*.5==3.25
    assert 1000*500==500000 and (1000+500)*10==15000
    return 'PASS: regression, tree SSE, boosting, kernel mapping, k-means updates, PCA projection, matrix/CP products'


async def browser_checks():
    from playwright.async_api import async_playwright
    results=[]
    async with async_playwright() as api:
        browser=await api.chromium.launch()
        for width,js in [(1440,True),(390,True),(390,False)]:
            errors=[]
            context=await browser.new_context(viewport={'width':width,'height':1000},java_script_enabled=js,offline=True)
            page=await context.new_page()
            page.on('pageerror',lambda e:errors.append(str(e)))
            await page.goto((ROOT/'dist/basics/classical.html').as_uri())
            await page.evaluate('document.fonts.ready')
            assert not await page.evaluate('document.documentElement.scrollWidth > innerWidth')
            assert await page.locator('main figure').count()==4
            assert await page.locator('main .katex').count()==4
            assert await page.locator('main .katex-error').count()==0
            assert not await page.locator('main').get_by_text('{{component:',exact=False).count()
            # Catch clipped labels in the new responsive SVGs.
            clipped=await page.locator('.classical-figure svg').evaluate_all('''svgs => svgs.flatMap(svg => {
              const box=svg.viewBox.baseVal;
              return [...svg.querySelectorAll('text')].filter(t => {
                const b=t.getBBox(); return b.x < -1 || b.y < -1 || b.x+b.width > box.width+1 || b.y+b.height > box.height+1;
              }).map(t => t.textContent);
            })''')
            assert not clipped,clipped
            await page.screenshot(path=str(OUT/f'intro-{width}-js{js}.png'))
            for n,fig in enumerate(await page.locator('main figure').all()):
                if js:
                    await fig.screenshot(path=str(OUT/f'figure-{n+1}-{width}.png'), style='.topbar { visibility: hidden; }')
            if js and width==1440:
                for anchor in ['prediction','decomposition-example','practice']:
                    await page.locator('#'+anchor).scroll_into_view_if_needed()
                    await page.screenshot(path=str(OUT/f'{anchor}.png'))
            assert not errors,errors
            results.append({'width':width,'javascript':js,'offline':True,'figures':4,'math':4,'document_overflow':False,'clipped_new_svg_labels':clipped,'errors':errors})
            await context.close()
        await browser.close()
    return results


if __name__=='__main__':
    report={'numeric':numeric_checks(),'browser':asyncio.run(browser_checks())}
    (OUT/'results.json').write_text(json.dumps(report,ensure_ascii=False,indent=2)+'\n')
    print(json.dumps(report,ensure_ascii=False,indent=2))
