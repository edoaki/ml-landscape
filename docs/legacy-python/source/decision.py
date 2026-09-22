"""Decision making and combinatorial optimization, with worked visual examples."""
from common import *


def pair(left, right, caption):
    return '<figure class="task-example"><div class="task-pair">'+left+right+'</div><figcaption>'+caption+'</figcaption></figure>'


def panel(b, title, h=280):
    return svg(txt(170,26,title,17)+b,h,340,title)


def go_illustration():
    b='<rect x="25" y="20" width="264" height="264" rx="6" fill="#e8c58e"/>'
    for i in range(9):
        t=45+28*i
        b+=line(45,t,269,t,'#765936',arrow=False,width=.8)+line(t,45,t,269,'#765936',arrow=False,width=.8)
    for x,y in [(2,2),(6,2),(4,4),(2,6),(6,6)]:
        b+=f'<circle cx="{45+28*x}" cy="{45+28*y}" r="2.3" fill="#765936"/>'
    for color,points in [('#242827',[(2,2),(3,2),(2,3),(5,5),(6,5),(5,6)]),('#fafaf5',[(5,2),(6,2),(5,3),(2,5),(3,5),(3,6)])]:
        for x,y in points:
            b+=f'<circle cx="{45+28*x}" cy="{45+28*y}" r="12" fill="{color}" stroke="#555d51" stroke-width=".7"/>'
    b+='<circle cx="157" cy="101" r="12" fill="#242827"/><circle cx="157" cy="101" r="5" fill="none" stroke="#e8c58e" stroke-width="2"/>'
    b+=txt(450,57,'2015年10月｜欧州王者',14)
    b+=txt(450,87,'樊麾（ファン・フイ）',19)
    b+=txt(450,122,'AlphaGo  5勝0敗',22,GREEN)
    b+=line(332,151,590,151,'#dfe5da',arrow=False,width=1)
    b+=txt(450,186,'2016年3月｜世界トップ級の棋士',14)
    b+=txt(450,216,'李世乭（イ・セドル）',19)
    b+=txt(450,251,'AlphaGo  4勝1敗',22,GREEN)
    return '<figure class="go-example">'+svg(b,305,620,'囲碁盤のイラストとAlphaGoの対戦成績')+'<figcaption><a href="https://deepmind.google/research/alphago/">Google DeepMindの対局記録</a>。盤面は教材用のイラストで、実際の対局の再現ではない。</figcaption></figure>'



# Small board positions are schematic, not records of AlphaGo games.
def mini_go(x,y,size=110,moves=(),candidates=False):
    gap=size/6
    b=f'<rect x="{x}" y="{y}" width="{size}" height="{size}" rx="3" fill="#e8c58e"/>'
    for i in range(5):
        t=(i+1)*gap
        b+=line(x+gap,y+t,x+size-gap,y+t,'#80643f',arrow=False,width=.65)
        b+=line(x+t,y+gap,x+t,y+size-gap,'#80643f',arrow=False,width=.65)
    stones=[(1,1,'black'),(2,1,'white'),(1,2,'black'),(3,2,'white')]+list(moves)
    for a,c,color in stones:
        b+=f'<circle cx="{x+(a+1)*gap}" cy="{y+(c+1)*gap}" r="{gap*.42}" fill="{color}" stroke="#555" stroke-width=".6"/>'
    if candidates:
        for label,a,c in [('A',2,2),('B',1,3),('C',3,3)]:
            cx,cy=x+(a+1)*gap,y+(c+1)*gap
            b+=f'<circle cx="{cx}" cy="{cy}" r="{gap*.46}" fill="{GREEN}"/>'+txt(cx,cy+4,label,12,'white')
    return b


def go_policy():
    b=txt(115,26,'盤面から、候補手へ',17)+mini_go(25,48,180,candidates=True)
    b+=line(214,138,264,138)+box(275,101,140,74,'方策ネット','各手の確率を出す',BLUE)
    b+=line(424,138,466,138)
    b+=txt(590,28,'自己対戦の経験で更新',17)
    b+=txt(590,52,'更新前（灰）→ 更新後（緑）',12)
    for i,(label,before,after) in enumerate([('A',.3,.6),('B',.4,.25),('C',.3,.15)]):
        y=80+i*57
        b+=txt(483,y+18,label,15)
        b+=f'<rect x="505" y="{y}" width="{before*210}" height="10" fill="#b9c3ba"/>'
        b+=txt(512+before*210,y+9,f'{before:.0%}',11,anchor='start')
        b+=f'<rect x="505" y="{y+15}" width="{after*210}" height="13" fill="{GREEN}"/>'
        b+=txt(512+after*210,y+26,f'{after:.0%}',12,GREEN,anchor='start')
    b+=txt(370,266,'勝ちにつながる手を、次は選びやすくする',17)
    return figure(svg(b,290,740,'方策ネットが出す候補手の選択確率と学習による変化'),'候補をA・B・Cだけに絞った説明用の数値。確率は「その手を選ぶ確率」で、勝率ではない。盤面・数値はAlphaGoの実測ではない。')


def go_search():
    # Identical parent positions are extended by one alternating-color move per level.
    b=mini_go(315,24,110)+txt(370,16,'いまの盤面（黒の番）',14)
    for x,label,move,col in [(165,'候補A',(2,2,'black'),GREEN),(465,'候補B',(1,3,'black'),BLUE)]:
        b+=line(370,139,x+55,187,col,width=3 if label=='候補A' else 1.8)
        b+=mini_go(x,194,110,[move])+txt(x+55,325,label+'を打つ',14,col)
    leaves=[(60,165,[(2,2,'black'),(2,3,'white')]),(230,165,[(2,2,'black'),(3,1,'white')]),(400,465,[(1,3,'black'),(2,3,'white')]),(570,465,[(1,3,'black'),(3,1,'white')])]
    for x,parent,moves in leaves:
        b+=line(parent+55,333,x+55,365,GREEN if parent==165 else BLUE)
        b+=mini_go(x,373,110,moves)
        b+=txt(x+55,504,'白の応手'+('①' if x in [60,400] else '②'),13)
    b+=txt(370,552,'さらに黒の手、白の手…と先を調べ、局面を評価する',16)
    return figure(svg(b,575,740,'黒の候補手から白の応手へ枝分かれする囲碁の木探索'),'一つの枝が一手、一つの盤面がその結果。候補と応手を2通りずつに省略した教材図。有望な枝を重点的に調べつつ、ほかの枝も探索する。')


def control_loop():
    b=box(30,55,170,65,'エージェント','方策：行動の選択ルール',BLUE)
    b+=box(400,55,170,65,'環境','行動に応じて状態が変化',GREEN)
    b+=line(207,76,392,76)+txt(300,60,'行動',14)
    b+='<path d="M485 128 V178 H115 V128" fill="none" stroke="#738679" stroke-width="2" marker-end="url(#arrow)"/>'
    b+=txt(300,166,'次の観測 ＋ 報酬',14)
    return '<figure class="rl-loop">'+svg(b,210,600,'エージェントが行動し、環境から次の観測と報酬を受け取る')+'<figcaption>行動 → 結果を観測、を繰り返す。集めた経験を使い、将来も含めた報酬の合計が大きくなるように方策を更新する。</figcaption></figure>'


# User reference: ten blue cities, green directed tour. Coordinates are illustrative.
POINTS=[(54,154),(94,95),(166,69),(216,124),(240,187),(209,235),(145,270),(61,249),(108,194),(159,161)]
def distance(order):
    return sum(math.dist(POINTS[a],POINTS[b]) for a,b in zip(order,order[1:]+order[:1]))/100
BEST=(0,1,9,2,3,4,5,6,7,8)
BAD=(0,4,1,5,2,7,3,6,9,8)

def tour(order=None,title='都市の位置',partial=False):
    b='<rect x="28" y="44" width="284" height="246" fill="white" stroke="#b9c6bb"/>'
    if order:
        edges=list(zip(order,order[1:]))
        if not partial: edges.append((order[-1],order[0]))
        for a,c in edges:
            x,y=POINTS[a]; xx,yy=POINTS[c]; length=math.hypot(xx-x,yy-y)
            ux,uy=(xx-x)/length,(yy-y)/length
            b+=line(x+9*ux,y+9*uy,xx-12*ux,yy-12*uy,'#00b96b',arrow=False,width=2.8)
            tx,ty=xx-10*ux,yy-10*uy
            b+=f'<path d="M{tx-7*ux+4*uy} {ty-7*uy-4*ux} L{tx} {ty} L{tx-7*ux-4*uy} {ty-7*uy+4*ux}" fill="none" stroke="#00b96b" stroke-width="2.8"/>'
    for i,(x,y) in enumerate(POINTS):
        b+=f'<circle cx="{x}" cy="{y}" r="7" fill="#536dfe"/>'
        if partial and order and i in order:
            b+=txt(x+12,y-9,str(order.index(i)+1),12,anchor='start')
    b+=txt(170,316,('総距離 '+f'{distance(order):.2f}') if order and not partial else ('未訪問の都市から、次を選ぶ' if partial else '位置は全ての図で共通'),14)
    return panel(b,title,335)


def generation():
    model=svg(line(5,100,30,100)+box(36,66,168,70,'Transformer','未訪問の都市を評価',BLUE)+line(209,100,237,100)+txt(120,166,'次の都市を一つ選ぶ',14),220,240,'Transformerで次の都市を選ぶ')
    return '<figure class="route-generation"><div class="route-generation-row">'+tour(BEST[:2],'いまの経路',True)+model+tour(BEST[:3],'一つ先まで伸ばす',True)+'</div><figcaption>都市の位置・現在地・訪問済みの情報を入力し、未訪問の都市を一つ選ぶ。これを繰り返し、最後に出発点へ戻る。</figcaption></figure>'


def clip(name,title,caption):
    return '<figure class="decision-video"><video controls playsinline preload="none" poster="assets/decision-'+name+'-poster.jpg" aria-label="'+title+'"><source src="assets/decision-'+name+'.mp4" type="video/mp4"></video><figcaption>'+caption+'</figcaption></figure>'


def gantt(compact):
    # A: M1 3 -> M2 2; B: M2 2 -> M1 2. All times are minutes.
    tasks=[('A1',0,3,0,BLUE),('A2',3,2,1,BLUE),('B1',0 if compact else 5,2,1,ORANGE),('B2',3 if compact else 7,2,0,ORANGE)]
    b=''
    for row in range(2):
        b+=txt(40,100+row*65,'M'+str(row+1),14)
        b+=f'<rect x="65" y="75" width="252" height="42" fill="#edf0e9" transform="translate(0 {row*65})"/>'
    for t in range(10):
        x=65+t*28
        b+=line(x,68,x,185,arrow=False,width=.6,color='#c8d1c7')+txt(x,208,t,12)
    for name,start,duration,row,color in tasks:
        b+=f'<rect x="{65+start*28}" y="{75+row*65}" width="{duration*28}" height="42" rx="4" fill="{color}"/>'+txt(65+(start+duration/2)*28,101+row*65,name,14,'white')
    return panel('<g transform="translate(0 -24)">'+b+'</g>','効率的な予定：5分で完了' if compact else '非効率な予定：9分で完了',200)


def decision_body():
    body=sec('decision','意思決定：状況に応じて、行動を選ぶ',p('ゲームで次の一手を選ぶ、ロボットを動かす、配送先を回る順番を決める。意思決定では、状況に応じて行動を選び、その結果のよさを考えます。AlphaGo、ゲーム、世界モデル、組合せ最適化、ロボットの順に具体例を見ます。'))
    body+=sec('rl','強化学習：試行の結果から、選択ルールを学ぶ',p('<strong>エージェント</strong>は行動を選ぶ主体、<strong>環境</strong>は行動の対象です。エージェントは状況を観測し、<strong>方策</strong>という選択ルールに従って行動します。環境からは次の観測と、結果のよさを表す<strong>報酬</strong>が返ります。')+control_loop()+p('たとえばゲームでは、画面を見て移動や攻撃を選び、得点や勝敗を報酬として受け取ります。いろいろな行動を試した経験から、将来も含めて報酬を多く得られる方策を学びます。目の前の得点だけでなく、その後に勝てるかも選択の評価に含めます。')+p('学習では「試す → 結果を評価する → 方策を更新する」を繰り返します。利用するときは、学習した方策で行動を選びます。各状況で正解の行動を教える代わりに、行動した結果を学習の手がかりにします。詳しくは<a href="foundations.html#rl">迷路の例</a>も参照してください。')+p('基本図の参考：'+ref('https://gymnasium.farama.org/v1.0.0/introduction/basic_usage/','Gymnasium公式：エージェントと環境のやり取り')))
    body+=sec('planning','AlphaGo：囲碁でプロ棋士に勝ったAI',go_illustration()+p('AlphaGoは、<strong>方策</strong>で有望な手を絞り、<strong>価値関数</strong>で局面のよさを評価し、<strong>木探索</strong>で先の展開を調べて一手を選びます。人間の棋譜による教師あり学習と、自己対戦による強化学習を組み合わせた例です。')+sub('方策の学習｜よい手を選ぶ確率を高める',go_policy()+p('方策ネットは、盤面を見て各候補手の選択確率を出します。まず人間の棋譜から手の選び方を学び、自己対戦の勝敗を使って、期待される勝率が上がるように更新します。図では、勝ちにつながると学んだ候補Aを選ぶ確率が高まる様子を表しています。'))+sub('木探索｜自分の手と相手の応手を先読みする',go_search()+p('候補Aを打ったら、相手はどう返すか。その先で自分はどう打つか。分岐した先の局面を価値関数やシミュレーションで評価し、その結果を手前へ戻して、最初の一手を選びます。方策の確率が高い手も参考にしながら探索するため、単に確率が最大の手をそのまま打つわけではありません。')+p('<a href="https://www.nature.com/articles/nature16961">AlphaGo原論文（2016）</a>：方策ネット・価値ネット・木探索を組み合わせる。')))
    body+=sec('games','ゲーム：画面から操作を選び、得点から学ぶ',p('DQNはゲーム画面を入力し、各操作から将来得られる報酬を見積もって行動を選びます。下の動画では、学習によって操作が変わる様子を見られます。')+sub('ブロック崩し｜学習が進むと、狙い方が変わる',clip('breakout','DQNのブロック崩しの学習過程','100・200・400・600エピソード後の比較。終盤では壁の端に穴を開け、ボールを上側へ送る動きに注目。<a href="https://www.nature.com/articles/nature14236">DQN原論文・補足動画2</a>。') ))
    body+=sec('world-model','世界モデル：世界の変わり方を学び、AIがイメトレする',p('<strong>世界モデルは、「こう動くと、世界はこう変わる」という変化の仕方を学ぶモデルです。</strong>たとえば、右へ動けば見える景色が変わり、ボールを押せば転がる。その関係を経験から捉え、まだ行っていない行動の結果も予測します。')+p('<strong>この予測の中で行動を試すのが、いわば「AIのイメージトレーニング」です。</strong>実際に毎回動く代わりに、モデル内で「この行動を続けたらどうなるか」を試し、よい結果につながる行動の選び方を学びます。ここでいう「理解」は、世界の変化を予測できる関係を学ぶという意味です。')+p('下のDIAMONDの動画では、操作に応じて景色が変わる様子に注目してください。過去の画面と操作から、世界モデルが次の画面を生成しています。')+clip('diamond','DIAMONDのCS:GO世界モデル','人がキーボードとマウスで操作し、DIAMONDが応答する画面を生成した映像。元のゲームエンジンの映像や、強化学習エージェントの自動プレイではない。<a href="https://diamond-wm.github.io/">DIAMOND著者ページ</a>。')+p('このCS:GOの例は、人間のプレイ記録から世界モデルを学習したものです。同研究のAtariでは、このような世界モデルの中で強化学習を行います。こちらが「イメトレで行動を学ぶ」使い方です。画面が自然に見えても、物体やルールを誤って予測することはあります。'))
    body+=optimization_body()
    body+=sec('robotics','ロボット：仮想環境で試し、実世界で動かす',sub('並列シミュレーション｜多数のロボットから経験を集める',clip('orbit','ORBITの並列ロボットシミュレーション','多数の環境で同時に試行し、方策の学習に使う経験を集める。<a href="https://isaac-orbit.github.io/">ORBIT著者ページ：Reinforcement Learning</a>の映像。')+p('シミュレーションでは、多数のロボットを並列に動かせます。姿勢や接触などの経験を集め、目標の動作に近づくように方策を更新します。実機へ移す際は、摩擦やセンサなどの違いにも対応する必要があります。'))+sub('RT-2｜画像と指示から、物を動かす',p('「缶を拾って」という指示に答えるだけでなく、対象の位置を捉え、アームとグリッパーを動かす必要があります。RT-2は、視覚・言語の知識をロボットの行動へつなぐ研究例です。')+'<figure><video controls preload="none" poster="assets/rt2-result-poster.jpg" style="width:100%"><source src="assets/rt2-result.mp4" type="video/mp4"></video><figcaption><a href="https://robotics-transformer2.github.io/">RT-2 著者公開映像</a>。指示と、ロボットが選んだ対象・動作を対応させて見る。</figcaption></figure>'+p('実演の動作を手がかりにする模倣学習と、報酬から改善する強化学習は区別します。RT-2の映像を、そのまま強化学習の成果と捉えるわけではありません。また、シミュレーションで成功した動作が現実の摩擦やカメラの違いでも成功するか、というsim-to-realの課題があります。')))
    return body+refs([('AlphaGo 原論文','https://www.nature.com/articles/nature16961'),('RT-2 著者ページ','https://robotics-transformer2.github.io/'),('TSP：Attention, Learn to Solve Routing Problems!','https://arxiv.org/abs/1803.08475')])


def compact_section(anchor,title,body):
    return '<div class="optimization-part" id="'+anchor+'"><h3>'+title+'</h3>'+body+'</div>'


def optimization_body():
    body=p('条件を守る組合せの中から、距離や所要時間が小さいものを探します。ここでは、強化学習で選択ルールを学ぶ例を見ます。')
    body+=compact_section('tsp','TSP：全都市を回る、短い経路を探す',pair(tour(BAD,'遠回りの多い経路'),tour(BEST,'短くまとまった経路'),'同じ10都市を一度ずつ訪れ、出発点へ戻る。距離は直線距離の合計（任意単位）。教材例で、最短性は保証しない。'))
    body+=compact_section('learn-routing','経路の生成と学習：Transformerで一つずつ選ぶ',generation()+p('<strong>生成：</strong>次の都市を選ぶ操作を繰り返すと、経路ができます。<br><strong>学習：</strong>総距離 L に対して報酬を −L とし、短い経路を作れる選択ルールを強化学習で学びます。')+p('<a href="https://arxiv.org/abs/1803.08475">Koolら（ICLR 2019）</a>は、Attentionを使ったモデルとREINFORCEでこの選択ルールを学習します。図はその考え方を簡略化したものです。'))
    body+=compact_section('scheduling','スケジューリング：空きを減らし、早く終える',p('青の仕事Aは A1 → A2、橙の仕事Bは B1 → B2 の順。同じ機械で作業が重ならないように予定を組みます。')+pair(gantt(False),gantt(True),'行は機械、横軸は時刻（分）、棒の幅は処理時間。A1＝3分、他は2分。時刻0から開始可能、中断・段取り替え・運搬時間は省略。')+p('<strong>強化学習によって、制約を守りながら作業を効率よく詰め込む方法をモデルに学習させます。</strong>工程を一つずつ割り付け、全作業が早く終わるほど高い報酬を与えます。<a href="https://papers.nips.cc/paper/2020/hash/11958dfee29b6709f48a9ba0387a2431-Abstract.html">研究例：Zhangら（2020）</a>。'))
    return sec('problem','組合せ最適化：順序や割り当てを学ぶ',body)
