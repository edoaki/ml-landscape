"""Original CNN diagrams and a portable initial state for the convolution demo."""
from common import *

INPUT = [[1,2,0,1],[0,1,3,2],[2,0,1,0],[1,2,0,2]]

def stack(x,y,size,n,color):
 b=''
 for i in reversed(range(n)):
  b+=f'<rect x="{x+i*5}" y="{y-i*5}" width="{size}" height="{size}" fill="{color}" stroke="white" stroke-width="1.5" rx="2"/>'
 return b

def why_cnn():
 b=box(12,10,378,430,'','')+box(410,10,378,430,'','')
 b+=txt(200,47,'全結合のNN（MLP）',20)+txt(600,47,'CNNの畳み込み',20)
 values=[[1,0,0,0],[1,0,0,0],[0,0,1,0],[0,0,1,0]]
 def pixels(x,y,values,cell=24):
  return ''.join(f'<rect x="{x+j*cell}" y="{y+i*cell}" width="{cell-2}" height="{cell-2}" fill="{BLUE if v else "white"}" stroke="#c3cfc0"/>'+txt(x+j*cell+11,y+i*cell+16,v,12,'white' if v else GREEN) for i,row in enumerate(values) for j,v in enumerate(row))
 b+=txt(88,86,'画像 4 × 4',15)+pixels(42,111,values)+line(140,159,175,159)
 for i in range(16):
  y=100+i*9
  for z in [111,153,195,237]:b+=line(192,y+3,307,z,BLUE,arrow=False,width=.7)
  b+=f'<rect x="181" y="{y}" width="9" height="6" fill="{BLUE}"/>'
 for z in [111,153,195,237]:b+=f'<circle cx="316" cy="{z}" r="9" fill="{ORANGE}"/>'
 b+=txt(192,86,'16個に並べる',13)+txt(304,274,'出力は9個',14)+txt(304,294,'（一部を表示）',12)
 b+=txt(199,331,'各出力が全16画素とつながる',16)+txt(199,369,'重み：16 × 9 = 144個',18)
 b+=txt(199,407,'接続ごとに別の重みを学習',14)
 b+=txt(489,86,'同じ画像',15)+pixels(444,111,values)
 out=[[values[i][j]-values[i][j+1]+values[i+1][j]-values[i+1][j+1] for j in range(3)] for i in range(3)]
 b+=txt(701,86,'出力 3 × 3',15)+pixels(665,111,out)
 for x,y,col in [(442,109,GREEN),(490,157,ORANGE)]:b+=f'<rect x="{x}" y="{y}" width="49" height="49" fill="none" stroke="{col}" stroke-width="3"/>'
 for x,y,col in [(663,109,GREEN),(711,157,ORANGE)]:b+=f'<rect x="{x}" y="{y}" width="25" height="25" fill="none" stroke="{col}" stroke-width="3"/>'
 b+=line(543,120,660,120,GREEN,dash=True)+f'<path d="M543 180 H628 V215 H724 V185" fill="none" stroke="{ORANGE}" stroke-width="2" stroke-dasharray="5 5" marker-end="url(#arrow)"/>'
 b+=txt(600,236,'同じ縦線なら、どちらの位置でも「2」',14)
 b+=txt(578,270,'共通のフィルタ',14,anchor='end')+pixels(593,247,[[1,-1],[1,-1]],22)
 b+=txt(600,331,'近くの2 × 2画素だけを見る',16)+txt(600,369,'重み：2 × 2 = 4個',18)
 b+=txt(600,407,'全ての位置で同じ4個を使う',14)
 return figure(svg(b,454,label='同じ4×4画像から9個の出力を作る全結合層と畳み込み層の比較'),'同じ4×4入力から9個の値を出す1層の比較。バイアスは省略。CNNは2×2フィルタ1種類・stride=1・padding=0。緑と橙の枠には同じ縦線があり、共通のフィルタで同じ値になる。MLP側の接続・出力は一部を表示。モデル全体の性能比較ではない。')

def overview():
 b=txt(510,32,'畳み込みで特徴を増やし、poolingで縦横を小さくする',21)
 stages=[(25,75,1,BLUE,'入力画像','64 × 64 × 1'),(165,95,4,BLUE,'畳み込み + ReLU','64 × 64 × 4'),(320,65,4,GREEN,'Max pooling','32 × 32 × 4'),(462,65,8,ORANGE,'畳み込み + ReLU','32 × 32 × 8'),(600,40,8,GREEN,'Max pooling','16 × 16 × 8')]
 for x,size,n,col,title,shape in stages:
  y=195-size/2
  b+=stack(x,y,size,n,col)+txt(x+size/2+8,87,title,15)+txt(x+size/2+8,290,shape,14)
  if n==1:b+=txt(x+size/2,y+54,'7',54,'white')
 for x1,x2 in [(105,155),(283,311),(405,451),(568,591),(682,710)]:b+=line(x1,194,x2,194)
 # A local patch in the input contributes to one feature-map position.
 b+=f'<rect x="57" y="178" width="20" height="20" fill="none" stroke="#ebc15b" stroke-width="3"/>'
 b+=line(78,180,199,169,ORANGE,dash=True,arrow=False)+line(78,198,199,187,ORANGE,dash=True,arrow=False)
 b+=f'<rect x="198" y="168" width="19" height="19" fill="none" stroke="#ebc15b" stroke-width="3"/>'
 for i in range(9):b+=f'<rect x="722" y="{115+i*19}" width="13" height="13" fill="#929c94"/>'
 b+=txt(730,87,'Flatten',15)+txt(730,294,'2,048個',14)+txt(730,314,'の数へ',12)
 for y in [135,175,215,255]:
  for i in range(9):b+=line(737,121.5+i*19,779,y,BLUE,arrow=False,width=.65)
  for z in [152,195,238]:b+=line(795,y,828,z,BLUE,arrow=False,width=.8)
  b+=f'<circle cx="787" cy="{y}" r="8" fill="{BLUE}"/>'
 for y in [152,195,238]:b+=f'<circle cx="838" cy="{y}" r="10" fill="{BLUE}"/>'+line(850,y,900,y)
 b+=txt(819,87,'全結合',15)+txt(840,294,'3クラスへ',14)+txt(946,87,'分類結果',15)
 for y,label,value in [(152,'クラスA','0.1'),(195,'クラスB','0.2'),(238,'クラスC','0.7')]:b+=txt(950,y+5,label+'  '+value,15)
 b+=line(25,325,680,325,GREEN,arrow=False)+txt(352,351,'特徴抽出：四角1枚 = 1チャネルの特徴マップ',16,GREEN)
 b+=line(716,325,1005,325,ORANGE,arrow=False)+txt(860,351,'分類：画像全体の答えを作る',16,ORANGE)
 b+=txt(510,389,'poolingは各マップを縮小する。チャネル数を増やすのは畳み込みのフィルタ。',15)
 return figure(svg(b,415,w=1040,label='特徴マップの重なりと解像度の変化で見る画像分類CNN'),'説明用の画像分類CNN。数字は高さ × 幅 × チャネル数。畳み込みは3×3・stride=1・padding=1、poolingは2×2・stride=2。表示した確率は例示値。四角の面積は模式的に縮小している。')

def unet():
 b=txt(175,28,'縮小側（Encoder）',19,ORANGE)+txt(618,28,'拡大側（Decoder）',19,BLUE)
 # Three resolution levels including the bottleneck, hence two downsamples.
 for x,y,size,n,col,shape in [(115,80,90,3,ORANGE,'64 × 64'),(225,245,63,4,ORANGE,'32 × 32'),(338,409,42,5,ORANGE,'16 × 16'),(613,80,90,3,BLUE,'64 × 64'),(532,245,63,4,BLUE,'32 × 32'),(435,409,42,5,BLUE,'16 × 16')]:
  b+=stack(x,y,size,n,col)+txt(x+size/2+5,y+size+27,shape,14)
 b+=line(28,124,107,124)+txt(62,105,'入力',15)+line(717,124,787,124)+txt(754,105,'画素ごと',13)+txt(754,153,'出力',15)
 for x,y,xx,yy in [(162,205,223,265),(258,340,337,428)]:
  b+=f'<path d="M{x} {y} V{yy} H{xx}" stroke="{ORANGE}" stroke-width="2.5" fill="none" marker-end="url(#arrow)"/>'
 for x,y,xx,yy in [(490,430,565,342),(610,267,663,204)]:
  b+=f'<path d="M{x} {y} H{xx} V{yy}" stroke="{BLUE}" stroke-width="2.5" fill="none" marker-end="url(#arrow)"/>'
 b+=line(391,430,432,430)+line(229,122,605,122,GREEN,width=4)+txt(411,99,'同じ解像度の特徴を連結',16,GREEN)
 b+=line(311,272,524,272,GREEN,width=4)+txt(416,245,'skip connection',15,GREEN)
 b+=txt(110,302,'poolingで縮小 ↓',14,ORANGE)+txt(693,362,'↑ 拡大して畳み込み',14,BLUE)
 b+=txt(401,517,'3段の解像度：64 → 32 → 16 → 32 → 64',17)
 return figure(svg(b,546,label='解像度3段のU-Net。縮小と拡大をつなぐ二つのスキップ接続'),'深さは最下段を含む3段に簡略化。縮小2回・拡大2回で、同じ解像度同士をskip connectionでつなぐ。矢印先では特徴を連結して畳み込む。空間サイズを保つpaddingを使う例で、原論文の切り出し処理は省略。')

def matrix(values,kind):
 return '<div class="matrix conv-'+kind+'" style="--cols:'+str(len(values[0]))+'">'+''.join('<span class="cell">'+str(v)+'</span>' for row in values for v in row)+'</div>'

def demo():
 result=[[INPUT[r][c]-INPUT[r+1][c+1] for c in range(3)] for r in range(3)]
 return '''<div class="demo conv-demo" data-demo="conv">
 <h3>フィルタの位置を変えて計算を見る</h3>
 <p>入力の2×2の範囲とフィルタを掛けて足すと、出力の1マスになります。位置を動かして、対応する入力と出力を見比べてください。入力・重みは説明用の固定値で、バイアスは0です。</p>
 <div class="conv-controls">
 <label>padding（外側に補う0の幅）<select class="conv-padding"><option value="0">0：補わない</option><option value="1">1：周囲に1マス</option></select></label>
 <label>stride（フィルタの歩幅）<select class="conv-stride"><option value="1" selected>1：1マスずつ</option><option value="2">2：2マスずつ</option><option value="3">3：3マスずつ</option></select></label>
 <label>畳み込み後のpooling<select class="conv-pool"><option value="none">なし</option><option value="max">Max：最大値</option><option value="avg">Average：平均値</option></select></label></div>
 <p class="conv-settings">stride=1、padding=0 → 出力は3×3。</p>
 <label class="conv-position">フィルタの位置 <input type="range" min="0" max="8" value="0" aria-label="畳み込みの出力位置"><output class="conv-position-value">出力 (0, 0)</output></label>
 <div class="conv-grids"><div><strong class="conv-input-title">入力 4 × 4</strong>'''+matrix(INPUT,'input')+'''</div><div class="conv-kernel-panel"><strong>フィルタ 2 × 2</strong>'''+matrix([[1,0],[0,-1]],'kernel')+'''<small>全ての位置で同じ重み</small></div><div><strong class="conv-output-title">出力 3 × 3</strong>'''+matrix(result,'output')+'''</div><div class="conv-pool-panel" hidden><strong class="conv-pool-title">pooling後</strong><div class="matrix conv-pooled"></div></div></div>
 <p class="conv-legend">緑：フィルタが重なる入力　橙の枠：対応する出力。出力のマスを押しても位置を選べます。</p>
 <p class="result" aria-live="polite">左上の出力：1×1 + 2×0 + 0×0 + 1×(−1) = 0。</p>
 <p class="conv-pool-result" aria-live="polite"></p>
 <p>paddingは画像の周囲に値を補う操作です。ここでは0を使います。strideはフィルタを一度に何マス動かすかで、2にすると出力のマス数が減ります。</p>
 <p>poolingは近い位置の値をまとめます。ここでは畳み込みの出力を2×2ずつ、歩幅2で区切り、最大値または平均値に置き換えます。端に2×2で収まらない行や列があれば使いません。ReLUは挟まず、負の出力もそのまま集約します。</p>
 <noscript><p>上の図はstride=1・padding=0・poolingなしの計算です。操作にはJavaScriptを有効にしてください。</p></noscript>
 </div>'''
