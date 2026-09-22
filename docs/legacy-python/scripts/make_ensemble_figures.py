"""Build original static teaching diagrams; no third-party artwork."""
from pathlib import Path
from html import escape
ROOT=Path(__file__).resolve().parents[1]
OUT=ROOT/'content/questions/ensembles-experts/components'
INK='#243d3b'; MUT='#6c7b7a'; GREEN='#267668'; BLUE='#507aaa'; GOLD='#b97730'; PURPLE='#8c659d'
PALETTE=[GREEN,BLUE,GOLD,PURPLE]
def t(x,y,s,size=17,color=INK,anchor='start',weight=400):
 return f'<text x="{x}" y="{y}" font-size="{size}" fill="{color}" text-anchor="{anchor}" font-weight="{weight}">{escape(s)}</text>'
def rect(x,y,w,h,fill='#f3f6f5',stroke='none',rx=12):
 return f'<rect x="{x}" y="{y}" width="{w}" height="{h}" rx="{rx}" fill="{fill}" stroke="{stroke}"/>'
def line(x,y,X,Y,c='#b5c3bf',width=2,dash=''):
 return f'<path d="M{x} {y} L{X} {Y}" fill="none" stroke="{c}" stroke-width="{width}"'+(f' stroke-dasharray="{dash}"' if dash else '')+'/>'
def path(d,c='#9caca6',width=2,arrow=True):
 return f'<path d="{d}" fill="none" stroke="{c}" stroke-width="{width}" stroke-linecap="round" stroke-linejoin="round"'+(' marker-end="url(#ARR)"' if arrow else '')+'/>'
def dot(x,y,r,c):return f'<circle cx="{x}" cy="{y}" r="{r}" fill="{c}"/>'
def head(k,title,sub):return [t(28,34,k,12,GREEN,weight=700),t(28,67,title,24,weight=650),t(28,94,sub,15,MUT)]
def label(x,y,s,c=GREEN):return t(x,y,s,14,c,weight=650)
def token(x,y,n):
 c=PALETTE[n-1];return rect(x,y,38,40,c,rx=6)+t(x+19,y+27,str(n),18,'white','middle',600)
def network(cx,y,c,seed=0):
 pts=[[(cx-38,y+12),(cx-38,y+42)],[(cx,y),(cx,y+27),(cx,y+54)],[(cx+38,y+12),(cx+38,y+42)]]
 s=''
 for j in range(2):
  for k,(x,v) in enumerate(pts[j]):
   for l,(X,V) in enumerate(pts[j+1]):s+=line(x,v,X,V,c,1+(k+l+seed)%3)
 for ps in pts:
  for x,v in ps:s+=dot(x,v,5,'white')+f'<circle cx="{x}" cy="{v}" r="5" fill="white" stroke="{c}" stroke-width="2"/>'
 return s
def fig(id,h,a,caption,title):
 content=''.join(a).replace('#ARR',f'#{id}-arrow')
 svg=f'<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 760 {h}" role="img" aria-labelledby="{id}-title"><title id="{id}-title">{escape(title)}</title><defs><marker id="{id}-arrow" markerWidth="7" markerHeight="7" refX="6" refY="3.5" orient="auto"><path d="M0 0 L6 3.5 L0 7" fill="none" stroke="#9caca6" stroke-width="1.2"/></marker></defs><g font-family="-apple-system, BlinkMacSystemFont, sans-serif">{content}</g></svg>'
 (OUT/f'{id}.html').write_text(f'<figure class="ensemble-figure"><div class="figure-scroll">{svg}</div><figcaption>{caption}</figcaption></figure>\n')
# Average: values become lengths, avoiding a paragraph in each box.
a=head('01 / 集約','三つの予測を、一つの予測へ','同じ写真について「猫の確率」を予測')
for i,v in enumerate([.8,.6,.7]):
 y=144+i*68;c=PALETTE[i]
 a += [t(28,y+20,f'モデル {i+1}',16,c),rect(128,y,235,24,'#edf1ef',rx=5),rect(128,y,235*v,24,c,rx=5),t(383,y+21,f'{v:.1f}',21,c,weight=650),path(f'M432 {y+12} H466 V224 H503')]
a += [rect(516,153,214,146,'#e9f2ee'),label(540,183,'平均した猫の確率'),t(623,248,'0.7',52,GREEN,'middle',650),t(540,278,'(0.8＋0.6＋0.7) ÷ 3',15,MUT),line(28,340,732,340),t(28,377,'多数決なら',16,weight=600),t(178,377,'猫　・　猫　・　猫',20,GREEN),t(492,377,'→  猫が3票',18)]
fig('aggregation',407,a,'予測値は説明用の例。平均は確率を、多数決は各モデルが選んだクラスをまとめます。','三つの確率の棒グラフから平均0.7へ')
# Bagging: repeated colored data chips make resampling visible.
a=head('02 / データを変える','データを取り直し、並行して学ぶ','バギング：重複を許して、元と同じ件数を抽出')
a += [label(28,143,'元のデータ')]
for j in range(4):a += [token(290+j*46,118,j+1)]
a += [path('M380 164 V190 H142 V224'),path('M380 190 V224'),path('M380 190 H618 V224')]
for i,ns in enumerate([[1,1,3,4],[2,3,3,4],[1,2,2,4]]):
 x=28+238*i;c=PALETTE[i]
 a += [rect(x,231,228,191,'#f5f7f6')]
 for j,n in enumerate(ns):a += [token(x+25+j*45,248,n)]
 a += [path(f'M{x+114} 299 V324'),network(x+114,332,c),t(x+114,414,f'モデル {i+1}',15,c,'middle')]
a += [path('M142 431 V456 H618 V431',arrow=False),path('M380 431 V487'),rect(180,496,400,50,'#e9f2ee'),t(380,528,'利用時：三つの予測を平均・投票',18,GREEN,'middle',600)]
fig('bagging',568,a,'同じ色・番号は同じ訓練例。重複する例や含まれない例が、組ごとに変わります。','色付きデータの再抽出と三つのモデルの並列学習')
# Boost: actual gap and correction drawn to scale.
a=head('03 / 順に補正する','残った誤差を、次のモデルが補う','勾配ブースティング：来客数を予測する例')
a += [label(28,137,'学習時'),t(130,137,'正解は100人',16)]
base=330;scale=1.55
for val in [0,100]:
 y=base-val*scale;a += [line(113,y,723,y,'#c7d2cc',1,'5 5'),t(96,y+5,str(val),14,MUT,'end')]
for x,v in [(154,70),(559,90)]:a += [rect(x,base-v*scale,105,v*scale,GREEN,rx=3),t(x+52,base-v*scale-14,f'{v}人',25,GREEN,'middle',650)]
a += [rect(154,base-155,105,30*scale,'#faecd9',rx=2),t(206,281,'70人',25,'white','middle',650),t(281,235,'残差 30人',17,GOLD,weight=600),line(265,175,265,221,GOLD,2),rect(354,base-90*scale,105,20*scale,GOLD,rx=3),t(406,base-90*scale-14,'＋20人',24,GOLD,'middle',650),path('M277 282 H327'),path('M477 282 H532'),t(207,358,'現在の予測',16,INK,'middle'),t(407,358,'学んだ補正',16,INK,'middle'),t(612,358,'更新後の予測',16,INK,'middle'),rect(28,390,704,53,'#f5f7f6'),t(48,423,'残差30人を目標に学び、この例では＋20人を補正。残差は10人に。',16),t(28,479,'利用時は、学習済みモデルの出力を足し合わせる。',17,GREEN)]
fig('boosting',505,a,'二乗誤差による回帰の数値例。補正の係数は1としています。','70人の予測に20人の補正を加え90人になる棒グラフ')
# Deep ensembles: identical source data, visibly distinct networks and predictive disagreement.
a=head('04 / 初期値を変える','同じデータから、異なるNNを学ぶ','Deep Ensembles：開始時の重みなどを変える')
a += [rect(240,120,280,44,'#f0f3f1'),t(380,148,'共通の訓練データ',17,INK,'middle'),path('M380 170 V189 H145 V213'),path('M380 189 V213'),path('M380 189 H615 V213')]
for i in range(3):
 x=35+i*235;c=PALETTE[i]
 a += [rect(x,222,220,150,'#f6f8f7'),t(x+110,249,f'初期値 {i+1}',16,c,'middle',600),network(x+110,271,c,i),t(x+110,356,f'NN {i+1}',16,c,'middle'),path(f'M{x+110} 378 V401 H380 V422')]
a += [rect(224,431,312,48,'#e9f2ee'),t(380,462,'予測分布を平均',19,GREEN,'middle',600),line(28,510,732,510),t(28,544,'予測の食い違いも手がかりになる',18,weight=600)]
for row,(vs,name) in enumerate([([.9,.8,.9],'よく一致'),([.9,.1,.5],'食い違う')]):
 y=585+row*56;a += [t(28,y+5,name,16),line(255,y,650,y,'#d7dfda',3)]
 for i,v in enumerate(vs):a += [dot(255+v*395,y+(i-1)*8,6,PALETTE[i])]
a += [t(255,678,'0',13,MUT,'middle'),t(650,678,'1',13,MUT,'middle'),t(450,678,'猫の確率',14,MUT,'middle')]
fig('deep-ensembles',703,a,'色は各NNに対応。下の点は、二つの入力に対する予測の例です。','同じデータと異なる初期値による学習、予測の一致と不一致')
# Stacking: explicitly separate fitting the meta-model from prediction.
a=head('05 / まとめ方を学ぶ','予測を入力にする、もう一つのモデル','スタッキング：複数モデルの予測と正解の関係を学ぶ')
a += [label(28,143,'学習時'),t(28,172,'各モデルが学習に使わなかった例への予測',15,MUT)]
for i,s in enumerate(['モデル1','モデル2','モデル3','正解']):a += [t(95+i*109,212,s,14,MUT,'middle')]
for row,vals in enumerate([['0.8','0.6','0.7','猫'],['0.2','0.4','0.1','犬'],['0.7','0.9','0.8','猫']]):
 y=230+row*47
 a += [rect(40,y,435,40,'#f3f6f4',rx=5)]
 for i,v in enumerate(vals):a += [t(95+i*109,y+27,v,19,PALETTE[i%3] if i<3 else INK,'middle',600)]
a += [path('M484 296 H535'),rect(549,244,184,110,'#eeebf4'),t(641,282,'メタモデル',22,PURPLE,'middle',600),t(641,313,'組み合わせを学習',15,PURPLE,'middle'),line(28,397,732,397),label(28,432,'利用時'),rect(28,457,275,65,'#f3f6f4'),t(165,483,'新しい写真への予測',15,MUT,'middle'),t(165,508,'[0.8, 0.6, 0.7]',20,INK,'middle'),path('M312 490 H351'),rect(363,457,187,65,'#eeebf4'),t(456,496,'メタモデル',20,PURPLE,'middle',600),path('M560 490 H599'),t(668,486,'最終予測',16,GREEN,'middle'),t(668,516,'猫の確率',20,GREEN,'middle',600)]
fig('stacking',550,a,'予測値は説明用。利用時は正解を与えず、学習済みのメタモデルで予測します。','三つの予測と正解からメタモデルを学習し利用する')
# MoE: horizontal expert lanes; width/color encode actual weighted contributions.
a=head('06 / 入力ごとに選ぶ','選んだ専門家だけを動かす','疎なMoE（top-2）：4個のうち2個を利用')
a += [rect(28,128,200,62,'#e9f2ee'),t(128,165,'入力の特徴',21,GREEN,'middle',600),path('M238 159 H292'),rect(304,126,428,67,'#eeebf4'),t(325,153,'ルーター',18,PURPLE,weight=650),t(325,179,'専門家1を0.75、専門家3を0.25で選ぶ',17,PURPLE),t(155,226,'同じ特徴を選ばれた専門家へ',15,MUT)]
ys=[270,342,414,486]
a += [path('M128 197 V250 H75 V414',GREEN,3,False)]
for i,y in enumerate(ys):
 active=i in (0,2);c=GREEN if i==0 else BLUE if i==2 else '#a4ada9'
 if active:a += [path(f'M75 {y} H186',c,3)]
 a += [rect(198,y-23,192,47,'#e9f2ee' if i==0 else '#edf2f8' if i==2 else '#f1f3f2'),t(294,y+7,f'専門家 {i+1}',19,c,'middle',600)]
 if active:
  a += [path(f'M400 {y} H485',c,4 if i==0 else 2),t(445,y-12,'× 0.75' if i==0 else '× 0.25',16,c,'middle',600),path(f'M492 {y} H545 V342 H584',c,4 if i==0 else 2)]
 else:a += [t(421,y+6,'計算しない',15,MUT)]
a += [dot(619,342,28,GREEN),t(619,352,'＋',30,'white','middle'),t(619,401,'重み付きで合成',16,GREEN,'middle',600),path('M619 413 V533',GREEN,3),rect(458,545,274,59,'#e9f2ee'),t(595,581,'次の層へ渡す特徴',19,GREEN,'middle',600),line(28,633,732,633),t(28,665,'密なMoE',16,weight=650),t(165,665,'すべての専門家を動かし、重み付きで合成',16,MUT)]
fig('exp-moe',693,a,'重みは説明用。線は特徴の流れを示し、色の付いた専門家だけが計算します。','ルーターが専門家1と3を選び同じ特徴を処理して重み付き合成する')
# Granularity: identical token positions; colors encode selected experts.
a=head('07 / 振り分ける単位','選択を、どこまで共通にするか','同じMoE層での比較。色とE番号は選ばれる専門家。')
for row,(name,desc,groups) in enumerate([
 ('トークン単位','各位置で選ぶ',[[0,1,0,2],[1,2,0,1]]),
 ('文・系列単位','一つの系列で共通',[[0,0,0,0],[1,1,1,1]]),
 ('タスク単位','同じタスクで共通',[[0,0,0,0],[0,0,0,0]])]):
 y=134+row*169
 a += [rect(28,y,704,147,'#f6f8f7'),t(48,y+32,name,20,INK,weight=650),t(48,y+58,desc,14,MUT)]
 for j,es in enumerate(groups):
  Y=y+18+j*62;a += [t(273,Y+27,'文A' if j==0 else '文B',15,MUT,'end')]
  for k,e in enumerate(es):
   X=293+k*103;c=PALETTE[e]
   a += [rect(X,Y,87,47,c,rx=7),t(X+43,Y+18,f'位置 {k+1}',11,'white','middle'),t(X+43,Y+38,f'E{e+1}',19,'white','middle',650)]
a += [t(28,674,'文A・文Bは同じタスクの別入力。各行で選択の共通範囲が変わる。',16,MUT)]
fig('moe-granularity',697,a,'選択数を1個にした模式例。系列単位でも各トークンは個別に処理され、出力が一つにまとめられるわけではありません。','同じ二文をトークン単位、系列単位、タスク単位で振り分ける比較')
# Expert location: alternatives within one simplified transformer block.
a=head('08 / 専門家にする部品','FFNを分けるか、Attentionを分けるか','Transformerの1ブロック内での構成例')
for col in range(2):
 x=28+366*col;cx=x+169
 a += [rect(x,125,338,404,'#f6f8f7'),t(cx,158,'FFN型MoE' if col==0 else 'Attention型の例',22,INK,'middle',650),t(cx,192,'入力の特徴',16,MUT,'middle'),path(f'M{cx} 202 V229')]
 if col==0:
  a += [rect(x+29,241,280,62,'#e9eef1'),t(cx,279,'Attention',21,BLUE,'middle',600),path(f'M{cx} 314 V345'),t(cx,366,'ルーター → FFNを選択',16,GREEN,'middle',600)]
  for j in range(3):
   X=x+23+j*98;a += [rect(X,380,91,54,'#e9f2ee' if j!=1 else '#e9edeb'),t(X+45,413,f'FFN {j+1}',17,GREEN if j!=1 else MUT,'middle',600)]
  a += [t(cx,457,'選んだ出力を合成',15,GREEN,'middle')]
 else:
  a += [t(cx,241,'ルーター → ヘッドを選択',16,PURPLE,'middle',600)]
  for j in range(3):
   X=x+23+j*98;a += [rect(X,255,91,54,'#eee8f4' if j!=1 else '#e9edeb'),t(X+45,288,f'ヘッド{j+1}',16,PURPLE if j!=1 else MUT,'middle',600)]
  a += [t(cx,335,'選んだ出力を合成',15,PURPLE,'middle'),path(f'M{cx} 349 V371'),rect(x+29,383,280,62,'#e9f2ee'),t(cx,421,'FFN',21,GREEN,'middle',600)]
 a += [path(f'M{cx} 466 V486'),t(cx,516,'次のブロックへ',16,MUT,'middle')]
fig('moe-components',552,a,'正規化・残差接続を省略。右はMixture of Attention Headsの考え方を示し、Attention型すべての共通構造ではありません。','FFNを専門家にするTransformerとAttentionヘッドを選ぶTransformerの比較')
