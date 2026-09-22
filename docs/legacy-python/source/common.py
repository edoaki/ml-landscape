"""Render chapter HTML/SVG, with local KaTeX for display equations."""
from html import escape as esc
from pathlib import Path
from functools import lru_cache
import math
import subprocess
ROOT = Path(__file__).resolve().parents[1]
PAGES=[]
GREEN='#35664d'; BLUE='#4d7897'; ORANGE='#ba7147'; PURPLE='#85709f'
def p(s):return '<p>'+s+'</p>'
def note(title,s):return f'<aside class="note"><strong>{title}</strong>{p(s)}</aside>'
@lru_cache(maxsize=None)
def render_math(tex):
 result = subprocess.run(
  ['node', str(ROOT/'source/render-math.cjs')], input=tex,
  text=True, capture_output=True, check=True,
 )
 return result.stdout
def eq(s,explain):
 return '<div class="equation" tabindex="0" aria-label="数式（横にスクロールできます）">'+render_math(s)+'</div>'+p(explain)
def table(headers,rows):return '<div class="table-scroll" tabindex="0"><table><thead><tr>'+''.join(f'<th scope="col">{h}</th>' for h in headers)+'</tr></thead><tbody>'+''.join('<tr>'+''.join(f'<td>{c}</td>' for c in row)+'</tr>' for row in rows)+'</tbody></table></div>'
def sec(id,title,body):return f'<section id="{id}"><h2>{title}</h2>{body}</section>'
def sub(title,body):return f'<h3>{title}</h3>{body}'
def ref(url,label):return f'<a href="{url}">{label} ↗</a>'
def refs(items):return sec('sources','出典・さらに詳しい説明','<ul class="references">'+''.join(f'<li>{ref(url,label)}</li>' for label,url in items)+'</ul>')
def bullets(items):return '<ul>'+''.join('<li>'+s+'</li>' for s in items)+'</ul>'
def cards(items):return '<div class="cards">'+''.join(f'<a class="card" href="{url}"><span class="card-kicker">{tag}</span><h3>{title}<span aria-hidden="true">↗</span></h3><p>{body}</p></a>' for tag,title,body,url in items)+'</div>'
def figure(svg,caption):return '<figure><div class="figure-scroll" tabindex="0" aria-label="図（狭い画面では横にスクロールできます）">'+svg+'</div><figcaption>'+caption+'</figcaption></figure>'
def svg(body,h=230,w=800,label='構造と情報の流れ'):
 return f'<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 {w} {h}" role="img" aria-label="{esc(label)}"><title>{esc(label)}</title><defs><marker id="arrow" viewBox="0 0 10 10" refX="9" refY="5" markerWidth="7" markerHeight="7" orient="auto-start-reverse"><path d="M0 0L10 5L0 10" fill="#738679"/></marker></defs>{body}</svg>'
def txt(x,y,t,size=15,color='#294337',anchor='middle'):
 return f'<text x="{x}" y="{y}" text-anchor="{anchor}" fill="{color}" font-size="{size}" font-family="system-ui,sans-serif">{esc(str(t))}</text>'
def box(x,y,w,h,title,detail='',color=GREEN):
 return f'<rect x="{x}" y="{y}" width="{w}" height="{h}" rx="9" fill="{color}" fill-opacity=".08" stroke="{color}" stroke-opacity=".45"/>'+txt(x+w/2,y+(h/2+5 if not detail else h/2-4),title,16,color)+(txt(x+w/2,y+h/2+20,detail,12,color) if detail else '')
def line(x,y,xx,yy,color='#738679',dash=False,arrow=True,width=2):return f'<path d="M{x} {y} L{xx} {yy}" fill="none" stroke="{color}" stroke-width="{width}"'+(' stroke-dasharray="5 5"' if dash else '')+(' marker-end="url(#arrow)"' if arrow else '')+'/>'
def flow(nodes,caption,labels=None):
 n=len(nodes); width=(760-(n-1)*26)/n; b=''
 for i,node in enumerate(nodes):
  title,detail,*c=node;x=20+i*(width+26);b+=box(x,42,width,76,title,detail,c[0] if c else GREEN)
  if i<n-1:b+=line(x+width+3,80,x+width+23,80)
  if labels and i<len(labels):b+=txt(x+width/2,151,labels[i],12)
 return figure(svg(b,180,label=caption),caption)
def dual(a,b,caption):return '<div class="compare">'+a+b+'</div>'+p(caption)
def page(slug,title,group,kicker,lead,body):
 PAGES.append(dict(slug=slug,title=title,group=group,kicker=kicker,lead=lead,body=body))
def img(name,alt,caption):
 if name.endswith('.svg'):
  return f'<figure><div class="figure-scroll" tabindex="0" aria-label="図（狭い画面では横にスクロールできます）"><img class="diagram-image" src="assets/{name}" alt="{alt}" loading="lazy"></div><figcaption>{caption}</figcaption></figure>'
 return f'<figure><a href="assets/{name}" target="_blank" rel="noopener"><img src="assets/{name}" alt="{alt}" loading="lazy"></a><figcaption>{caption} <a href="assets/{name}" target="_blank" rel="noopener">画像を拡大 ↗</a></figcaption></figure>'

def graph(kind='gcn',hop=1):
 coords=[(150,125),(70,45),(290,65),(290,200),(440,45),(455,200)];features=['A (1, 0)','B (0, 2)','C (2, 1)','D (1, 1)','E (0, 1)','F (2, 0)'];edges=[(0,1),(0,2),(0,3),(2,4),(3,5)];b=''
 for i,j in edges:
  x,y=coords[i];xx,yy=coords[j];b+=line(x,y,xx,yy,BLUE if i==0 else '#abb8ad',dash=kind=='sage' and j==3,arrow=False,width=3)
 for i,(x,y) in enumerate(coords):
  c=GREEN if i==0 else BLUE if i<4 else ORANGE
  if kind in ('gcn','gat'):
   b+=f'<path d="M{x+9} {y-18} C{x+44} {y-44} {x+48} {y+6} {x+21} {y}" fill="none" stroke="{c}" stroke-width="1.7" marker-end="url(#arrow)"/>'
  b+=f'<circle cx="{x}" cy="{y}" r="20" fill="{c}"/>'+txt(x,y+5,chr(65+i),15,'white')+txt(x,y+39,features[i],13)
 b+=box(530,35,245,64,{'gcn':'GCN · 次数で重み付け','gat':'GAT · 特徴から重み付け','sage':'GraphSAGE · 近隣を選ぶ','base':'1層で1-hopの情報'}[kind],{'gcn':'自己ループ込みの次数を使う','gat':'近隣内で係数の和は1','sage':'この例は B・C をサンプル','base':'2層で E・F の情報も届く'}[kind])
 b+=txt(650,143,{'gcn':'A: 1/4   B: 1/√8','gat':'A: .197  B: .072','sage':'mean(B, C) = (1, 1.5)','base':'A → ノード分類'}[kind],15)+txt(650,172,{'gcn':'C・D: 1/√12','gat':'C: .534  D: .197','sage':'concat(A, mean) → 共有 W','base':'全ノード → readout → 性質'}[kind],15)+txt(650,219,'青：1-hop　橙：2-hop',12)
 return figure(svg(b,260,label=kind+'の近隣集約'), '共通の6ノードグラフ。特徴は教材用の数値。'+('点線の D はこの更新でサンプルされない。' if kind=='sage' else '実験結果ではなく、情報の流れを表す図。'))
