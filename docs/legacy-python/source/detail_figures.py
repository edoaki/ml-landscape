"""Original computed illustrations; values deliberately small and labelled as examples."""
from common import *
import random

def build():
 out=ROOT/'assets'
 def save(name,b,h=300):out.joinpath(name+'.svg').write_text(svg(b,h,label='説明用の数値で計算した'+name+'の図'),encoding='utf-8')
 def grid(x,y,values,cell=29,selected=(),signed=False):
  b=''
  for i,row in enumerate(values):
   for j,v in enumerate(row):
    fill=GREEN if (i,j) in selected else BLUE
    alpha=.10+.65*(abs(v)/3 if not signed else min(abs(v),1));b+=f'<rect x="{x+j*cell}" y="{y+i*cell}" width="{cell-2}" height="{cell-2}" fill="{fill}" fill-opacity="{alpha}" rx="2"/>'+txt(x+j*cell+(cell-2)/2,y+i*cell+cell*.66,v,12)
  return b
 inp=[[1,2,0,1],[0,1,3,2],[2,0,1,0],[1,2,0,2]];kernel=[[1,0],[0,-1]];res=[[inp[i][j]-inp[i+1][j+1] for j in range(3)] for i in range(3)]
 b=txt(112,30,'入力 4 × 4',18)+grid(45,65,inp,34,[(0,0),(0,1),(1,0),(1,1)])+txt(350,30,'フィルタ 2 × 2',18)+grid(315,85,kernel,36)+txt(650,30,'出力 3 × 3',18)+grid(594,70,res,38)+line(197,132,278,132)+line(413,132,555,132)+txt(350,205,'左上：1×1 + 2×0 + 0×0 − 1×1 = 0',16)+txt(400,253,'位置を変えて同じ積和を繰り返す。重みは共有する。',14)
 save('convolution',b,280)
 # Attending to all tokens vs causal mask.
 b='';scores=[[1,.2,.6,.1],[.4,1,.3,.2],[.2,.4,1,.6],[.1,.5,.3,1]]
 for ox,masked,title in [(30,False,'両方向の参照'),(425,True,'因果マスクの参照')]:
  b+=txt(ox+160,30,title,18)
  for i in range(4):
   vals=[math.exp(scores[i][j]) if not masked or j<=i else 0 for j in range(4)];tot=sum(vals)
   b+=txt(ox+30,96+i*43,f'Q{i+1}',12)
   for j,v in enumerate(vals):
    if i==0:b+=txt(ox+82+j*48,56,f'K{j+1}',12)
    col='#35664d' if v else '#a6aba3';a=v/tot
    b+=f'<rect x="{ox+61+j*48}" y="{70+i*43}" width="44" height="39" fill="{col}" fill-opacity="{.12+a*.8}"/>'+txt(ox+83+j*48,95+i*43,f'{a:.2f}' if v else '×',12)
  b+=txt(ox+160,282,'一行の係数の和 = 1',14)
 b+=txt(400,325,'列：参照される側。行：情報を集める側。値は固定スコアから計算。',14)
 save('attention-matrix',b,350)
 # RNN as unrolled graph with per-step input and output.
 b=''
 for i,x in enumerate([75,315,555]):
  b+=box(x,105,165,65,'同じRNNセル','共有 Wₓ・Wₕ')+box(x,10,165,48,f'入力 x{i+1}',color=BLUE)+box(x,230,165,48,f'出力 y{i+1}',color=ORANGE)+line(x+82,62,x+82,98)+line(x+82,174,x+82,224)
  if i<2:b+=line(x+170,138,x+232,138)+txt(x+200,121,f'h{i+1}',14)
 b+=txt(400,316,'縦：各時刻の入力と出力。横：過去をまとめた状態。',14)
 save('rnn-unroll',b,345)
 # VAE distributions in 2D.
 rng=random.Random(6);b=txt(200,28,'AE：入力 → 一点の z',18)+txt(603,28,'VAE：入力 → 分布 q(z | x)',18)
 for ox in [20,420]:b+=line(ox+30,237,ox+345,237,arrow=False)+line(ox+30,237,ox+30,55,arrow=False)+txt(ox+330,260,'z₁',12)+txt(ox+20,50,'z₂',12)
 for i,(cx,cy,c) in enumerate([(120,106,BLUE),(268,160,ORANGE),(160,211,GREEN)]):
  b+=f'<circle cx="{cx}" cy="{cy}" r="8" fill="{c}"/>'+txt(cx+30,cy+6,f'例{i+1}',12,c)
  b+=f'<ellipse cx="{cx+400}" cy="{cy}" rx="42" ry="24" fill="{c}" fill-opacity=".12" stroke="{c}"/>'
  for _ in range(20):
   xx=cx+400+rng.gauss(0,20);yy=cy+rng.gauss(0,11);b+=f'<circle cx="{xx:.2f}" cy="{yy:.2f}" r="2.5" fill="{c}" fill-opacity=".7"/>'
 b+=txt(400,305,'右：中心が μ、広がりが σ。点はその分布からのサンプル。',14)
 save('latent',b,335)
 # Invertible affine coupling warps lines and samples, mapping (u,v) -> (u,exp(.4u)*v+.6sin(2u)).
 def transform(u,v):return u,math.exp(.4*u)*v+.6*math.sin(2*u)
 b=txt(190,27,'基底空間：単純な分布',18)+txt(610,27,'可逆なcoupling変換後',18)
 for ox,warped in [(40,False),(450,True)]:
  def coord(u,v):
   if warped:u,v=transform(u,v)
   return ox+140+u*55,166-v*30
  for axis in range(2):
   for k in [-2,-1,0,1,2]:
    pts=[coord(k,-2+j*.1) if axis==0 else coord(-2+j*.1,k) for j in range(41)]
    b+='<polyline points="'+' '.join(f'{x:.2f},{y:.2f}' for x,y in pts)+'" fill="none" stroke="#b7c8ac" stroke-width="1.5"/>'
  rng=random.Random(11)
  for _ in range(130):
   u=max(-2,min(2,rng.gauss(0,.72)));v=max(-2,min(2,rng.gauss(0,.72)));x,y=coord(u,v);b+=f'<circle cx="{x:.2f}" cy="{y:.2f}" r="2.5" fill="{BLUE if not warped else GREEN}" opacity=".6"/>'
 b+=line(333,155,437,155)+txt(400,127,'g',17)+txt(400,310,'同じ点を変換。線が混み合う所は縮み、広がる所は密度が下がる。',14)
 save('flow-density',b,340)
 # Noise schedule applied to a fixed 8x8 binary glyph; generated here, not an MNIST inference.
 glyph=['00111000','01000100','00000100','00011000','00000100','00000100','01000100','00111000'];noise=random.Random(10);eps=[[noise.gauss(0,1) for _ in range(8)] for _ in range(8)];b=''
 for n,a in enumerate([1,.64,.25,.02]):
  ox=30+n*195;b+=txt(ox+70,27,f'ᾱ = {a}',17)
  for i in range(8):
   for j in range(8):
    signal=1 if glyph[i][j]=='1' else -1;v=math.sqrt(a)*signal+math.sqrt(1-a)*eps[i][j];gray=round(max(0,min(255,(v+2)/4*255)))
    b+=f'<rect x="{ox+j*18}" y="{55+i*18}" width="18" height="18" fill="rgb({gray},{gray},{gray})"/>'
  b+=txt(ox+70,229,['元の信号','信号が多い','ノイズが増える','ほぼノイズ'][n],14)
 b+=txt(400,278,'同じ信号と同じ ε から、既知の式でノイズを混ぜた図。',14)
 save('diffusion-stages',b,305)
 # Point transport paths for Flow Matching.
 rng=random.Random(2);starts=[(rng.gauss(0,.4),rng.gauss(0,.4)) for _ in range(20)];ends=[(math.cos(i*.314),math.sin(i*.314)) for i in range(20)];b=''
 for ox,t in [(25,0),(295,.5),(565,1)]:
  b+=txt(ox+95,28,f't = {t}',18)
  for (u,v),(s,w) in zip(starts,ends):
   x=ox+95+((1-t)*u+t*s)*70;y=145+((1-t)*v+t*w)*70
   b+=f'<circle cx="{x:.2f}" cy="{y:.2f}" r="4" fill="{BLUE if t==0 else GREEN if t==.5 else ORANGE}"/>'
   if t==.5:b+=line(x,y,x+(s-u)*17,y+(w-v)*17,GREEN,width=1)
 b+=txt(400,268,'各ペアの直線経路と速度（中央の矢印）。学習済みモデルの軌道ではない。',13)
 save('transport',b,295)
