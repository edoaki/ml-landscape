"""Original recurrent-cell diagrams, redrawn from user-provided visual references."""
from common import *


def path(d, color=GREEN, arrow=True, width=2.5):
 return f'<path d="{d}" fill="none" stroke="{color}" stroke-width="{width}" stroke-linejoin="round"'+(' marker-end="url(#arrow)"' if arrow else '')+'/>'


def op(x,y,label,color=ORANGE):
 return f'<circle cx="{x}" cy="{y}" r="20" fill="#fff7ec" stroke="{color}" stroke-width="2"/>'+txt(x,y+6,label,21,color)


def dot(x,y,color=GREEN):
 return f'<circle cx="{x}" cy="{y}" r="4" fill="{color}"/>'


def unroll():
 b=txt(125,30,'ループで省略した表現',18)+txt(600,30,'時間方向に展開すると',18)
 b+=box(65,190,120,65,'RNN')+box(65,65,120,50,'出力 yₜ',color=BLUE)+box(65,335,120,50,'入力 xₜ',color=BLUE)
 b+=line(125,335,125,259)+line(125,190,125,119)+path('M185 223 H215 V150 H35 V223 H62')+txt(125,141,'次の時刻へ hₜ',14)+txt(275,229,'＝',32)
 for x,t in [(390,'0'),(590,'1'),(790,'2')]:
  b+=txt(x,59,'時刻 '+t,15)+box(x-62,190,124,65,'RNN','同じ重み W')+box(x-62,78,124,48,'出力 y'+t,color=BLUE)+box(x-62,335,124,48,'入力 x'+t,color=BLUE)
  b+=line(x,335,x,259)+line(x,190,x,130)
  if t!='2':b+=line(x+65,223,x+135,223)+txt(x+100,208,'h'+t,15)
 b+=txt(310,278,'初期状態',12)+txt(310,296,'h₋₁ = 0',13)+path('M310 261 V223 H325')+line(854,223,886,223)+txt(880,261,'…',24)
 b+=txt(590,416,'横の矢印：過去の要約 h　／　縦の矢印：入力と出力',16)
 return figure(svg(b,440,w=920,label='RNNのループ表現と時間展開。入力は下、出力は上、状態は次の時刻へ渡す。'),'参考画像の配置に沿って新規作図。左のループは「状態を次の時刻へ渡す」ことの省略表現。右の箱は同じセルを繰り返し使う様子で、重みを時刻ごとに増やすわけではない。yはhを出力層で変換した予測。図では時刻0から始め、初期状態をh₋₁と表記。')


def step():
 b=box(20,30,150,55,'入力 xₜ',color=BLUE)+box(20,155,150,55,'前の状態 hₜ₋₁')+box(230,30,120,55,'Wₓ xₜ',color=BLUE)+box(230,155,120,55,'Wₕ hₜ₋₁')
 b+=line(174,58,226,58)+line(174,182,226,182)+path('M354 58 H410 V103')+path('M354 182 H410 V143')+op(410,123,'＋')+txt(410,205,'バイアス b も加える',13)+line(435,123,495,123)+box(500,95,115,55,'tanh')+line(620,123,690,123)+box(695,95,185,55,'新しい状態 hₜ')
 return figure(svg(b,235,w=910,label='RNNの1ステップ。入力と前の状態をそれぞれ変換し、足してtanhを通す。'),'入力の情報と過去の情報を一つのベクトルhへ混ぜ直す。Wₓ・Wₕ・bは学習するパラメータで、すべての時刻で共有する。')


def lstm():
 b='<rect x="125" y="48" width="675" height="360" rx="30" fill="#edf5e7" stroke="#93ac80" stroke-width="2"/>'
 b+=txt(60,88,'cₜ₋₁',19)+txt(861,88,'cₜ',19)+txt(450,33,'セル状態：残す情報を運ぶ経路',18,GREEN)
 b+=path('M95 100 H200')+path('M240 100 H480')+path('M520 100 H886')
 b+=path('M220 265 V123')+path('M390 265 V230 H480')+path('M500 265 V253')+path('M500 207 V123')
 b+=path('M740 100 V150')+box(704,154,72,40,'tanh')+path('M740 194 V217')+path('M650 265 V240 H717')+path('M740 263 V360 H886')+path('M785 360 V265')
 b+=txt(861,351,'hₜ',19)+txt(828,250,'出力層へ',13)+dot(740,100)+dot(785,360)
 b+=txt(59,378,'hₜ₋₁',19)+path('M95 370 H165',BLUE)+txt(110,457,'xₜ',19,BLUE)+path('M110 433 V414 H165 V370',BLUE)+dot(165,370,BLUE)+path('M165 370 H650',BLUE,False)
 for x,label,detail in [(220,'σ','忘却 fₜ'),(390,'σ','入力 iₜ'),(500,'tanh','候補 gₜ'),(650,'σ','出力 oₜ')]:
  b+=path(f'M{x} 370 V336',BLUE)+box(x-45,265,90,67,label,detail,color=BLUE)+dot(x,370,BLUE)
 b+=op(220,100,'×')+op(500,100,'＋')+op(500,230,'×')+op(740,240,'×')
 b+=txt(355,89,'残す',14)+txt(556,200,'書き込む',14)+txt(440,397,'xₜ と hₜ₋₁ を連結し、各変換へ渡す',14,BLUE)
 b+=txt(460,466,'四角：学習する変換＋活性化　　丸：成分ごとの演算　　●：分岐・合流',14)
 return figure(svg(b,495,w=920,label='LSTMの内部。上のセル状態に忘却ゲートを掛け、入力ゲートと候補の積を加え、出力ゲートでhを作る。'),'参考画像に沿った、忘却ゲートを含む標準的なLSTMの1ステップ。緑の上段がcの経路、青の下段が各ゲート・候補への入力。σの四角は「学習する線形変換＋sigmoid」、候補のtanhの四角も学習する変換を含む。cからhへのtanhには重みはない。')


def gru():
 b='<rect x="145" y="45" width="650" height="402" rx="30" fill="#edf4fa" stroke="#8baac0" stroke-width="2"/>'
 b+=txt(65,86,'hₜ₋₁',19)+txt(860,86,'hₜ',19)+txt(510,30,'古い状態を残す経路 ＋ 新しい候補を取り込む経路',17)
 b+=path('M105 95 H440')+path('M480 95 H730')+path('M770 95 H888')
 b+=path('M200 95 V210 H280')+dot(200,95)+path('M300 310 V233')+path('M323 210 H350 V265 H608 V310')
 b+=path('M460 310 V118')+dot(460,185)+path('M460 185 H560')+path('M600 185 H630')+path('M650 310 V208')+path('M674 185 H750 V118')
 b+=path('M175 95 V415 H460',BLUE,False)+dot(175,95)+path('M110 478 V455 H240 V415',BLUE)+dot(240,415,BLUE)+path('M240 455 H690 V364',BLUE)+dot(240,455,BLUE)
 for x,label in [(300,'reset rₜ'),(460,'update zₜ')]:
  b+=path(f'M{x} 415 V389',BLUE)+box(x-51,310,102,75,'σ',label,color=BLUE)+dot(x,415,BLUE)
 b+=box(595,310,110,50,'tanh',color=BLUE)+txt(720,292,'候補 h̃ₜ',16)+txt(555,253,'rₜ × hₜ₋₁',14)+txt(726,407,'入力 xₜ',14,BLUE)
 b+=op(300,210,'×',BLUE)+op(460,95,'×',BLUE)+op(580,185,'1−',BLUE)+op(650,185,'×',BLUE)+op(750,95,'＋',BLUE)
 b+=txt(369,147,'zₜ：残す割合',14)+txt(681,154,'1 − zₜ',14)+txt(100,501,'入力 xₜ',17,BLUE)+txt(480,498,'候補には、resetで調整した過去と今の入力を渡す。',15)
 return figure(svg(b,525,w=920,label='GRUの内部。resetで候補に使う過去を調整し、updateで古い状態と候補を混ぜる。'),'参考画像に沿って新規作図。zₜを古い状態に、1−zₜを候補に掛ける表記。resetは候補を作る経路だけに作用し、上段の古い状態を直接消さない。交差するだけの線は接続せず、●は分岐・合流。四角は学習する変換＋活性化、丸は成分ごとの演算。')
