"""Original Transformer teaching diagrams inspired by the supplied references."""
import json
from common import *

TOKENS = ['I', 'live', 'in', 'Tokyo', 'with']
COLORS = ['#487bb6', '#198d98', '#348761', '#9a8420', '#b2703c', '#c65165', '#a655a8']
# Illustrative positions, not hidden states or a projection of a trained model.
STATES = [
 [(40,180),(95,180),(155,180),(210,180),(300,180),(370,180),(425,180)],
 [(110,85),(335,155),(225,270),(355,80),(355,265),(105,175),(115,270)],
 [(140,110),(300,165),(250,235),(350,115),(330,260),(135,190),(170,260)],
 [(170,100),(265,150),(285,215),(365,150),(315,280),(110,220),(175,270)],
 [(190,105),(265,180),(335,225),(370,145),(255,285),(105,200),(155,275)],
]
STATES = [points[:5] for points in STATES]
STATES += [[(130,95),(235,145),(185,265),(345,100),(335,245)]]
STATES += [STATES[-1]]
STAGE_TEXT = [
 ('入力の文章', 'まずは文章を単語に分けて並べます。次に「ベクトル化」を選ぶと、単語が空間の中の点へ変わります。'),
 ('入力の表現', '各単語の埋め込みに位置情報を加えた状態。まだ、この文の他の単語の情報は取り込んでいません。'),
 ('第1層の出力', '要素間の関係から情報を集め、各要素の特徴を加工します。5語すべてに新しい表現ができます。'),
 ('第2層の出力', '第1層で更新された表現から、関係を再び計算します。前の層と同じ係数表を使い回すわけではありません。'),
 ('第3層の出力', '情報交換と特徴の加工を繰り返します。この後も同じ構造の層が続き、最終のN層へ進みます。'),
 ('第N層：最後のトークンに注目', '最終層のwithの表現を強調しています。with自身と、それ以前のI live in Tokyoの情報を取り込んだベクトルから、次のトークンを予測します。'),
 ('出力：次のトークンの確率', '最終層の最後のトークンの表現を全結合層へ渡し、語彙全体のスコアを作ります。softmaxで確率に変え、次のトークンを選びます。'),
]


def dot(x, y, color, r=7):
 return f'<circle cx="{x}" cy="{y}" r="{r}" fill="{color}"/>'


def motivation():
 b=txt(25,30,'RNN：前の状態ができてから、次を計算する',19,anchor='start')
 for i,word in enumerate(TOKENS):
  x=65+i*115
  b+=box(x-43,58,86,44,word,color=BLUE)
  if i<len(TOKENS)-1:b+=line(x+46,80,x+68,80)
 b+=txt(425,134,'離れた位置の情報も、途中の状態を経由する',16,BLUE)
 b+=txt(25,189,'Self-Attention：同じ層の入力から、各位置をまとめて更新する',19,anchor='start')
 for i,word in enumerate(TOKENS):
  x=65+i*115
  for j in range(len(TOKENS)):
   b+=line(x,303,65+j*115,235,'#dce5da',arrow=False,width=1)
  b+=dot(x,309,COLORS[i])+dot(x,229,COLORS[i])+txt(x,338,word,17,COLORS[i])
 b+=line(525,300,180,237,ORANGE,width=3)+txt(425,380,'離れた位置も直接参照できる。層から次の層へは順番に進む。',16)
 return figure(svg(b,405,w=850,label='RNNの順次処理とSelf-Attentionによる位置ごとの並列更新の比較'),'情報の経路を示す模式図。上はRNNの状態の受け渡し、下は1層のSelf-Attention。下の点は各位置の入力と更新後の表現。太線は一つの参照経路の例。')


def representation():
 plot='<ellipse cx="245" cy="190" rx="215" ry="155" fill="#f7f9f4" stroke="#d9e2d3"/>'
 plot+='<g class="tf-trails" aria-hidden="true"></g>'
 for i,((x,y),word,color) in enumerate(zip(STATES[0],TOKENS,COLORS)):
  plot+=f'<g class="tf-token{" tf-last" if i==len(TOKENS)-1 else ""}" data-token="{i}" style="transform:translate({x}px,{y}px)">'+'<circle class="tf-halo" r="22" fill="none" stroke="#ba7147" stroke-width="3"/>'+f'<rect class="tf-vector-shape" x="-8" y="-8" width="16" height="16" rx="8" fill="{color}"/>'+f'<text class="tf-word" x="13" y="5" fill="{color}" font-size="19" font-weight="650" font-family="system-ui,sans-serif" stroke="#f7f9f4" stroke-width="5" paint-order="stroke">{word}</text><text class="tf-numbers" x="0" y="5" text-anchor="middle" fill="{color}" font-size="12" font-family="monospace">[0.{i+2}, −0.{i+1}, …]</text><g class="tf-column" fill="{color}"><path d="M8 -30H3V34H8M43 -30H48V34H43" fill="none" stroke="{color}" stroke-width="1.5"/><text text-anchor="middle" font-family="monospace" font-size="12"><tspan x="25" y="-15">0.{i+2}</tspan><tspan x="25" y="5">−0.{i+1}</tspan><tspan x="25" y="25">⋮</tspan></text></g></g>'
 plot+='<g class="tf-output-chain">'+output_chain()+'</g>'
 plot+=txt(245,370,'色は単語の目印、点の位置はその時点の表現',14)
 live='<div class="tf-live" hidden><div class="tf-controls"><div class="tf-steps" role="group" aria-label="表示する層">'
 for i in range(7):
  if i==5:live+='<span class="tf-ellipsis" aria-hidden="true">…</span>'
  live+=f'<button type="button" data-layer="{i}" aria-pressed="{str(i==0).lower()}">{["文章", "ベクトル化（Word2Vec）", "第1層", "第2層", "第3層", "N層", "出力"][i]}</button>'
 live+='</div></div>'
 live+='<div class="tf-stage"><div class="tf-space">'+svg(plot,390,w=520,label='5語の表現が、Transformerの各層を通ると変わる模式図')+'</div><div class="tf-stage-copy" aria-live="polite"><p class="tf-counter">文章 → ベクトル → 各層</p><h3 class="tf-stage-title">入力の文章</h3><p class="tf-stage-description">'+STAGE_TEXT[0][1]+'</p><div class="tf-cycle"><div>ベクトル化（Word2Vec）</div><span aria-hidden="true">↓</span><div>要素間で情報交換</div><span aria-hidden="true">↓</span><div>各要素の特徴を加工</div><span aria-hidden="true">↓</span><div>次の層の入力へ</div></div></div></div>'
 static='<div class="tf-static">'
 for index,points in enumerate(STATES[1:6],start=1):
  b='<ellipse cx="245" cy="190" rx="215" ry="155" fill="#f7f9f4" stroke="#d9e2d3"/>'
  for (x,y),word,color in zip(points,TOKENS,COLORS):b+=dot(x,y,color,8)+txt(x+14,y+5,word,21,color,anchor='start')
  if index==5:
   x,y=points[-1];b+=f'<circle cx="{x}" cy="{y}" r="22" fill="none" stroke="#ba7147" stroke-width="3"/>'
  static+='<div>'+f'<strong>{STAGE_TEXT[index][0]}</strong>'+svg(b,355,w=520,label=STAGE_TEXT[index][0])+p(STAGE_TEXT[index][1])+'</div>'
 static+='<div><strong>出力：次のトークンの確率</strong>'+prediction()+'</div></div>'
 data=esc(json.dumps(dict(states=STATES,stages=STAGE_TEXT),ensure_ascii=False),quote=True)
 return '<figure class="tf-representation" data-transformer-layers="'+data+'"><div class="tf-intro"><span class="tf-kicker">CONTEXTUAL REPRESENTATIONS</span><p>文章から、文脈を含む表現へ</p></div>'+live+static+'<figcaption>値などは説明用のものです。</figcaption></figure>'


def qkv():
 b=box(15,117,155,75,'同じ入力 hᵢ','ある単語の表現',BLUE)
 for y,label,weight,detail,color in [(28,'Query qᵢ','W_Q','どんな情報を参照するか',ORANGE),(127,'Key kᵢ','W_K','照合される側の特徴',BLUE),(226,'Value vᵢ','W_V','実際に渡す情報',GREEN)]:
  b+=line(176,154,257,y+28,color)+box(265,y,130,56,weight,color=color)+line(400,y+28,461,y+28,color)+box(467,y-5,320,68,label,detail,color)
 return figure(svg(b,310,label='同じトークンの表現から、異なる学習可能な行列でQuery、Key、Valueを作る'),'全てのトークンからQ・K・Vを作る。単語ごとに役を割り振るのではなく、一つの単語が参照する側にも、参照される側にもなる。')


def scores():
 b=txt(200,29,'① QとKを照合して重みを作る',18)
 b+=txt(30,69,'query = live（固定した数値例）',15,anchor='start')
 b+=txt(76,109,'参照先',13)+txt(157,109,'スコア',13)+txt(284,109,'softmax後',13)
 weights=[.087,.237,.032,.644]
 for i,(word,score,a) in enumerate(zip(['I','live','in','Tokyo'],[0,1,-1,2],weights)):
  y=144+43*i
  b+=txt(76,y,word,17,COLORS[i])+txt(157,y,score,16)
  b+=f'<rect x="208" y="{y-16}" width="{a*145}" height="21" rx="3" fill="{GREEN}"/>'+txt(352,y,f'{a:.3f}',14)
 b+=txt(203,336,'大きいスコア → 大きい重み',15,ORANGE)
 return figure(svg(b,365,w=400,label='内積による関連度からsoftmaxで重みを作る'),'内積の値が高い = 関連度が高い。スコアは√dₖで割った後の値。関連度が高い参照先ほど、大きな重みになる。数値は説明用の例。')


def mix():
 b=txt(610,29,'② Vを重み付きで足す',18)
 weights=[.087,.237,.032,.644]
 # A numerical value-space example: output = (.881, .676).
 coords=[(455,298),(740,298),(455,93),(740,93)]
 for i,((x,y),a) in enumerate(zip(coords,weights)):
  b+=f'<circle cx="{x}" cy="{y}" r="{10+35*a}" fill="{COLORS[i]}" fill-opacity=".14"/>'+dot(x,y,COLORS[i])
  b+=txt(x,y+(-23 if y==93 else 32),['v_I (0,0)','v_live (1,0)','v_in (0,1)','v_Tokyo (1,1)'][i],13,COLORS[i])
 x=455+285*(weights[1]+weights[3]);y=298-205*(weights[2]+weights[3])
 b+=line(coords[1][0],coords[1][1],x,y,PURPLE,dash=True,width=3)
 b+=dot(x,y,PURPLE,10)+txt(x-15,y-19,'重心に移動',16,PURPLE,anchor='end')+txt(605,368,'約 (0.881, 0.676)',17,PURPLE)
 return figure(svg('<g transform="translate(-395 0)">'+b+'</g>',393,w=405,label='liveのValueから重心に移動する。関連度が高いTokyo側に重心が寄る'),'円の大きさは重みの目安。liveのVから、重み付きの重心へ移動する矢印だけを描いた。関連度が高いTokyoのVの方へ重心が寄る。1 headの重み付き和の図で、残差接続やFFNを含む層全体の移動とは異なる。')



def hidden_label(x,y,index,layer):
 return f'<text x="{x}" y="{y}" text-anchor="middle" fill="#294337" font-size="24" font-family="Georgia,serif" font-style="italic">h<tspan baseline-shift="sub" font-size="14">{index}</tspan><tspan baseline-shift="super" font-size="14">({layer})</tspan></text>'


def block():
 b=txt(380,30,'1つのTransformerブロックを、上から下へ読む',20)
 b+=txt(380,61,'横の4列は、文章中の異なるトークンの位置',16)
 xs=[190,315,440,565]
 for i,x in enumerate(xs):
  b+=txt(x,98,f'位置 {i+1}',14)+hidden_label(x,133,i+1,'ℓ−1')+line(x,149,x,176)
 b+='<rect x="120" y="184" width="515" height="155" rx="12" fill="#fff0e5" stroke="#dab599"/>'
 b+=txt(380,211,'Multi-head Attention：位置の間で情報交換',18,ORANGE)
 for x in xs:
  for xx in xs:b+=line(x,235,xx,311,'#d6a788',arrow=False,width=1)
  b+=dot(x,235,BLUE)+dot(x,311,ORANGE)+line(x,341,x,366)
 b+=box(120,372,515,50,'残差を足す → LayerNorm',color=BLUE)
 for x in xs:b+=line(x,425,x,461)
 b+='<rect x="120" y="468" width="515" height="152" rx="12" fill="#eef4e6" stroke="#aec09a"/>'
 b+=txt(380,495,'FFN：各位置の特徴を、それぞれ加工',18,GREEN)
 for x in xs:
  b+=dot(x,516,GREEN)+dot(x,599,GREEN)
  for dx in [-23,0,23]:b+=line(x,521,x+dx,556,GREEN,arrow=False)+dot(x+dx,556,GREEN,3)+line(x+dx,556,x,594,GREEN,arrow=False)
  b+=line(x,624,x,651)
 b+=box(120,658,515,50,'残差を足す → LayerNorm',color=BLUE)
 for i,x in enumerate(xs):b+=line(x,711,x,746)+hidden_label(x,781,i+1,'ℓ')
 b+='<path d="M190 162H79V397H116" fill="none" stroke="#4d7897" stroke-width="2" marker-end="url(#arrow)"/>'
 b+='<path d="M190 446H79V683H116" fill="none" stroke="#4d7897" stroke-width="2" marker-end="url(#arrow)"/>'
 b+=txt(380,824,'更新後の4つの表現を、次のブロックへ渡す',17)
 return figure(svg(b,850,w=760,label='4位置の表現がAttention、残差とLayerNorm、FFN、残差とLayerNormを順に通る'),'各列は別の処理手順ではなく、同じ文の4つの位置。hの下付きは位置、上付きの(ℓ−1)と(ℓ)は層を表す。残差経路は1列分だけ代表して描いた。原論文のPost-LN型を示し、headの並列化は省略。GPTでは因果マスクを加え、正規化の配置が異なる設計も使う。')


def overview():
 return flow([('入力のベクトル列','各位置に1つの表現',BLUE),('ブロック × N層','Attention ＋ FFN'),('文脈を含む表現','各位置の情報を更新'),('目的に合う出力層','分類・次トークン予測',ORANGE)],'同じ構造のブロックをN層重ねる。通常、各層には別々の学習可能なパラメータがある。')


def prediction():
 b=txt(250,28,'最終層の最後のトークン',18)
 b+=box(165,48,170,55,'with','文脈を含む表現',ORANGE)+line(250,107,250,133)
 b+=box(105,140,290,55,'全結合層','語彙ごとのスコアへ',BLUE)+line(250,199,250,225)
 b+=box(105,232,290,45,'softmax → 確率',color=GREEN)
 for i,(word,prob) in enumerate([('family',.52),('friend',.26),('friends',.12),('others',.06)]):
  y=322+48*i
  b+=txt(105,y,word,18,anchor='end')
  b+=f'<rect x="125" y="{y-19}" width="{prob*480}" height="25" rx="4" fill="{GREEN}" opacity="{1-i*.15}"/>'+txt(438,y,f'{prob:.0%}',16)
 b+=txt(250,514,'… その他の候補 4%',16)+txt(250,549,'確率は説明用。実際は語彙全体に出力する。',13)
 return svg(b,570,w=500,label='withの最終表現から全結合層とsoftmaxで次トークン確率を計算。family52%、friend26%、friends12%、others6%、その他4%。')



def heads():
 b=box(15,123,130,65,'入力の表現','全トークン',BLUE)
 for y,label in [(20,'head 1'),(123,'head 2'),(226,'head 3')]:
  b+=line(150,155,230,y+32)+box(237,y,225,65,label,'固有のQ・K・V → 集約',ORANGE)+line(468,y+32,553,155)
 b+=box(560,123,225,65,'連結 → W_O','複数の見方を組み合わせる',GREEN)
 return figure(svg(b,315,label='Multi-head Attention。異なる射影で並列に情報を集め、連結と出力射影で組み合わせる。'),'headは別々の学習可能な射影を使う。「場所」「人」などの役割を人が固定して割り当てるわけではない。')


def embedding():
 b=txt(400,30,'単語の特徴と、文の中の位置を組み合わせる',20)
 b+=txt(400,64,'I live in Tokyo with',19)
 for i,(word,values,pos,result) in enumerate([
  ('I','[0.2, 0.5]','[0.0, 1.0]','[0.2, 1.5]'),
  ('live','[0.8, 0.1]','[0.8, 0.5]','[1.6, 0.6]'),
  ('in','[0.3, 0.4]','[0.9, −0.4]','[1.2, 0.0]')]):
  x=155+i*245
  b+=box(x-95,98,190,43,word,color=COLORS[i])
  b+=line(x,146,x,174)+txt(x,198,values,20,COLORS[i])
  b+=txt(x,223,'単語の埋め込み',14)
  b+=txt(x,259,'＋',24)+txt(x,292,pos,20,ORANGE)
  b+=txt(x,316,f'{i+1}番目の位置ベクトル',14,ORANGE)
  b+=line(x,330,x,355)+txt(x,384,result,20,GREEN)
 b+=txt(400,426,'同じ単語でも、置かれた位置が違えば別の入力ベクトルになる',17)
 b+=line(400,441,400,479)
 b+='<ellipse cx="400" cy="630" rx="285" ry="133" fill="#f7f9f4" stroke="#d9e2d3"/>'
 for (x,y),word,color in zip(STATES[1],TOKENS,COLORS):
  b+=dot(150+x,485+y*.75,color,8)+txt(165+x,490+y*.75,word,18,color,anchor='start')
 b+=txt(400,800,'出力：位置情報を含んだ5語のベクトル → Transformerへ',18)
 return figure(svg(b,825,label='文章を埋め込みに変換し、位置ベクトルを成分ごとに足して、ベクトル列を作る'),'上は最初の3語について2成分だけ示した計算例（数値は説明用）。位置ベクトルは何番目かを数値で伝え、成分ごとに埋め込みへ足す。下は5語分の出力を点で表した模式図。図の座標自体が文章の並び順を表すわけではない。')


def encoder_decoder():
 b=txt(197,28,'Encoder：入力の表現を作る',19,BLUE)+txt(603,28,'Decoder：続きを作る',19,ORANGE)
 b+=box(57,52,280,49,'入力文：I have a cat',color=BLUE)+box(463,52,280,49,'生成途中：私は',color=ORANGE)
 for x,c in [(197,BLUE),(603,ORANGE)]:
  b+=line(x,108,x,129)+box(x-140,136,280,44,'埋め込み ＋ 位置',color=c)+line(x,187,x,214)
 b+='<rect x="42" y="220" width="310" height="221" rx="12" fill="#4d7897" fill-opacity=".04" stroke="#4d7897" stroke-dasharray="5 5"/>'
 b+='<rect x="448" y="220" width="310" height="306" rx="12" fill="#ba7147" fill-opacity=".04" stroke="#ba7147" stroke-dasharray="5 5"/>'
 b+=box(67,240,260,54,'Self-Attention','入力文の中で情報交換',BLUE)+line(197,301,197,323)
 b+=box(67,330,260,54,'Feed Forward','各位置の特徴を加工',BLUE)+txt(197,422,'このブロックをN層',14,BLUE)
 b+=box(473,240,260,54,'Self-Attention','生成途中の文の中で情報交換',ORANGE)+line(603,301,603,323)
 b+=box(473,330,260,54,'Cross-Attention','Encoderの出力を参照',PURPLE)+line(603,391,603,413)
 b+=box(473,420,260,54,'Feed Forward','各位置の特徴を加工',ORANGE)+txt(603,506,'このブロックをN層',14,ORANGE)
 b+=line(197,448,197,467)+box(57,474,280,50,'Encoderの最終出力',color=BLUE)
 b+='<path d="M337 499H395V357H466" fill="none" stroke="#4d7897" stroke-width="2.5" marker-end="url(#arrow)"/>'+txt(409,342,'K・V',14,BLUE)
 b+=line(603,533,603,555)+box(463,562,280,48,'全結合層 → 次トークンの確率',color=ORANGE)
 return figure(svg(b,630,label='EncoderはSelf-AttentionとFFN、Encoder–Decoder型のDecoderはその間にCross-Attentionを持つ'),'翻訳に使うEncoder–Decoder型の模式図。上から下へ処理する。残差接続・LayerNormは省略。各Decoder層はEncoderの最終出力を参照する。')


def attention_comparison():
 b=line(400,20,400,427,color='#d6dfd1',arrow=False)
 for offset,title in [(0,'Self-Attention'),(400,'Cross-Attention')]:
  b+=txt(offset+200,30,title,21)
 b+=box(25,61,350,59,'同じ系列の表現 H','例：生成途中の文の表現',ORANGE)
 for x,name,c in [(75,'Q',ORANGE),(200,'K',BLUE),(325,'V',GREEN)]:
  b+=line(x,127,x,162)+box(x-35,170,70,42,name,color=c)
 b+=box(425,61,140,59,'Decoder側','生成途中の表現',ORANGE)+box(585,61,190,59,'Encoder側','入力文の最終表現',BLUE)
 b+=line(495,127,495,162)+box(460,170,70,42,'Q',color=ORANGE)
 for x,name,c in [(630,'K',BLUE),(735,'V',GREEN)]:
  b+=line(x,127,x,162)+box(x-35,170,70,42,name,color=c)
 for offset,xs in [(0,[75,200,325]),(400,[495,630,735])]:
  for x in xs:b+=line(x,219,x,244)
  b+=box(offset+25,252,350,62,'QとKを照合 → Vを重み付きで足す','Attentionの計算は共通')
  b+=line(offset+200,322,offset+200,346)
 b+=box(25,354,350,53,'同じ系列から情報を取り込む',color=ORANGE)
 b+=box(425,354,350,53,'入力文の情報をDecoder側へ取り込む',color=PURPLE)
 return figure(svg(b,430,label='Self-Attentionは同じ系列からQKVを作り、Cross-AttentionはDecoderからQ、EncoderからKVを作る横並び比較'),'矢印は情報の流れ。Q・K・Vはそれぞれ別の線形層で作る。')


def output_chain():
 b=line(260,91,260,113)+box(145,119,230,44,'全結合層 → softmax',color=BLUE)
 for i,(word,prob) in enumerate([('family',.52),('friend',.26),('friends',.12),('others',.06)]):
  y=196+i*39
  b+=txt(121,y,word,16,anchor='end')
  b+=f'<rect x="137" y="{y-15}" width="{prob*430}" height="20" rx="3" fill="{GREEN}" opacity="{1-i*.15}"/>'+txt(413,y,f'{prob:.0%}',15)
 b+=txt(260,348,'… その他 4%（説明用の確率）',13)
 return b
