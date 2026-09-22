"""SSM teaching diagrams adapted from cited papers and author explanations."""
from common import *
import hashlib
GUIDE = 'https://newsletter.maartengrootendorst.com/p/a-visual-guide-to-mamba-and-state'
PAPER = 'https://arxiv.org/abs/2312.00752'
HIPPO = 'https://hazyresearch.stanford.edu/blog/2020-12-05-hippo'


def details(title, body):
    return '<details class="ssm-detail"><summary>'+title+'</summary>'+body+'</details>'


def memory_figure():
    b=txt(30,32,'同じ系列を処理しても、要素のつなぎ方が違う',19,anchor='start')
    b+=txt(30,77,'Attention：全ての要素同士を参照',18,BLUE,anchor='start')+txt(757,77,'O(N²)',24,BLUE,anchor='end')
    for i in range(5):
        for j in range(5):
            b+=line(170+i*126,135,170+j*126,245,BLUE,arrow=False,width=1)
    for i in range(5):
        x=127+i*126
        b+=box(x,98,86,37,'x'+str(i+1),color=BLUE)+box(x,245,86,37,'y'+str(i+1),color=ORANGE)
    b+=txt(400,319,'N個の出力 × N個の参照先 → N²組を照合',16,BLUE)
    b+=txt(30,383,'SSM：記憶を引き継ぎながら順番に処理',18,GREEN,anchor='start')+txt(757,383,'O(N)',24,GREEN,anchor='end')
    for i in range(5):
        x=127+i*126
        b+=box(x,417,86,37,'x'+str(i+1),color=BLUE)+line(x+43,457,x+43,485)
        b+=box(x,490,86,48,'h'+str(i+1))
        if i<4:b+=line(x+89,514,x+122,514)
        b+=line(x+43,541,x+43,568)+box(x,573,86,37,'y'+str(i+1),color=ORANGE)
    b+=txt(400,650,'一歩の更新 × Nステップ → N回の処理',16,GREEN)
    return figure(svg(b,680,label='全要素間のAttentionはO(N²)、固定サイズの状態を渡す再帰SSMはO(N)'),
        'Visual Guide Part 1と'+ref(PAPER,'Mamba §3.1')+'の対比を再構成。Nは系列長、モデル幅・状態次元は固定。上は全位置を参照するAttentionの図。生成用の因果マスクでは未来への線がなくなるが、全系列の照合はO(N²)。下は再帰計算の処理量。')


def update_figure():
    b=txt(30,31,'一歩の更新：状態を作り、出力を読み、次へ渡す',19,anchor='start')
    b+='<g class="ssm-wires">'
    b+=line(165,240,214,240)+line(308,240,374,240)+line(504,240,546,240)+line(622,240,663,240)
    b+=line(440,382,440,346,BLUE)+line(440,296,440,270,BLUE)
    b+=box(219,215,85,50,'Ā')+box(402,296,76,50,'B̄',color=BLUE)+box(552,215,65,50,'C',color=ORANGE)
    b+='</g>'
    b+='<g class="ssm-prev">'+box(35,215,130,50,'h₀')+'</g>'
    b+='<g class="ssm-input">'+box(375,382,130,50,'x₁',color=BLUE)+'</g>'
    b+='<g class="ssm-a-term">'+txt(335,203,'Āh₀',14,GREEN)+'</g>'
    b+='<g class="ssm-b-term">'+txt(519,329,'B̄x₁',14,BLUE)+'</g>'
    b+='<g class="ssm-sum">'+txt(440,246,'＋',26)+'</g>'
    b+='<g class="ssm-state">'+box(375,215,130,50,'h₁')+'</g>'
    b+='<g class="ssm-output">'+box(666,215,100,50,'y₁',color=ORANGE)+'</g>'
    b+='<g class="ssm-new-input" opacity="0">'+box(375,382,130,50,'x₂',color=BLUE)+'</g>'
    for i in range(3):
        b+=f'<g class="ssm-saved-output" data-index="{i}" opacity="0">'+box(420+i*120,70,100,42,'y'+str(i+1),color=ORANGE)+'</g>'
    b+=txt(30,93,'上へ送った出力',13,ORANGE,anchor='start')
    markup=figure(svg(b,495,label='Āで前の状態を変換しB̄xを加え、Cで出力。hは左へ、yは上へ、新しいxは下から到着'),
        ref(GUIDE,'Visual Guideの再帰表現')+'と'+ref(PAPER,'Mamba式(2)')+'に基づくアニメーション。h₀=0、D=0。記号はベクトルを表し、移動は計算の受け渡しを示す。')
    return '<div class="ssm-animation">'+markup+'<div class="ssm-controls" hidden><button type="button" class="ssm-play">再生</button><button type="button" class="ssm-next">次の段階</button><button type="button" class="ssm-reset">最初から</button></div><p class="ssm-status" role="status" aria-live="polite">前の状態と入力からh₁を作り、Cを掛けてy₁を得ます。次はh₁を引き継いでx₂を読みます。</p></div>'


def basis_figure():
    b=txt(30,31,'波形そのものを保存する代わりに、基底の係数を保存する',18,anchor='start')
    for i,name in enumerate(['p₀：一定','p₁：傾き','p₂：曲がり']):
        x=30+i*250
        b+=txt(x+100,81,name,16)
        b+=line(x,178,x+200,178,arrow=False,width=1)
        points=[]
        for j in range(81):
            u=-1+2*j/80
            v=[1,u,(3*u*u-1)/2][i]
            points.append(f'{x+j*2.5},{178-v*50}')
        b+=f'<polyline points="{" ".join(points)}" fill="none" stroke="{[GREEN,BLUE,ORANGE][i]}" stroke-width="3"/>'
        b+=txt(x+100,260,'× 係数 c'+str(i),17,[GREEN,BLUE,ORANGE][i])
    b+=txt(400,310,'足し合わせて、過去の信号の形を近似する',18)
    b+=box(200,340,400,62,'状態として残すもの：[c₀, c₁, c₂, …]','基底の形は既知なので、履歴ごとに保存し直さない')
    return figure(svg(b,432,label='Legendre多項式の基底と、それに掛ける係数を保存するHiPPOの圧縮'),
        ref(HIPPO,'HiPPO著者解説のOnline Function Approximation')+'に沿った補助図。最初の3つのLegendre多項式を描画。説明のため正規化係数と時間軸の変換を省略。')


def convolution_figure():
    b=txt(30,32,'再帰を展開すると、過去の入力の重み付き和になる',18,anchor='start')
    for i,term in enumerate(['x₁','x₂','x₃','x₄']):b+=box(235+i*130,70,100,48,term,color=BLUE)
    rows=[['K₀','','',''],['K₁','K₀','',''],['K₂','K₁','K₀',''],['K₃','K₂','K₁','K₀']]
    for i,row in enumerate(rows):
        y=150+i*75
        b+=box(30,y,115,49,'y'+str(i+1),color=ORANGE)+txt(185,y+31,'＝',20)
        for j,k in enumerate(row):
            if k:
                b+=box(235+j*130,y,100,49,k+' × x'+str(j+1),color=[GREEN,BLUE,PURPLE,ORANGE][i-j])
                if j<i:b+=txt(350+j*130,y+31,'＋',17)
    b+=txt(400,487,'同じ色＝同じ距離の重み。同じカーネルを1位置ずつずらす。',15)
    b+=txt(400,522,'K₀ = CB̄　 K₁ = CĀB̄　 K₂ = CĀ²B̄　…',18)
    return figure(svg(b,552,label='SSMの更新を展開した因果畳み込み。y1からy4を同じ距離のカーネルで計算する'),
        ref(PAPER,'Mamba式(2)–(3)')+'および'+ref(GUIDE,'Visual GuideのConvolution Representation')+'を日本語で再構成。h₀=0、D=0。空欄は未来の入力なので使わない。')


def selection_figure():
    b=txt(30,32,'Selective Copying：色付きの要素だけを順に出力する',18,anchor='start')
    b+=txt(30,77,'入力',15,anchor='start')
    colors=[GREEN,BLUE,ORANGE]
    for i,v in enumerate(['■','A','■','■','B','■','C','■','合図']):
        col=colors['ABC'.index(v)] if v in 'ABC' else '#7c887e'
        b+=box(30+i*84,94,68,48,v,color=col)
    b+=txt(430,77,'■ は空白。A・B・Cの位置は毎回変わる。',14)
    b+=line(156,149,270,248,GREEN)+line(400,149,400,248,BLUE)+line(576,149,530,248,ORANGE)
    for i,v in enumerate('ABC'):b+=box(236+i*130,254,68,48,v,color=colors[i])
    b+=txt(400,340,'合図の後の正解：A → B → C',18)
    b+=txt(30,396,'固定カーネル：何ステップ前かで重みが決まる',16,BLUE,anchor='start')
    b+=txt(30,428,'選択的SSM：何が来たかに応じて、書き込み・保持を変える',16,GREEN,anchor='start')
    return figure(svg(b,460,label='Mamba論文のSelective Copying課題。空白を除き色付きの要素を入力順に出力する'),
        ref(PAPER,'Gu & Dao, Mamba, Figure 2')+'の課題を再構成（CC BY 4.0、要素数と表記を簡略化）。A・B・Cは記号の種類、■は空白。色だけに頼らず区別できるよう文字も付けた。')


def selective_parameters():
    b=txt(30,32,'入力を読むたびに、記憶の扱いを決める',19,anchor='start')
    b+=box(25,100,140,60,'今の入力 xₜ',color=BLUE)
    b+=box(245,70,205,70,'Bₜ・Δₜ','書き込み方と更新の刻み',BLUE)
    b+=box(540,70,205,70,'Cₜ','読み出し方',ORANGE)
    b+=line(167,120,238,107,BLUE)
    b+=line(94,98,94,50,BLUE,arrow=False)+line(94,50,642,50,BLUE,arrow=False)+line(642,50,642,65,BLUE)
    b+=box(25,262,140,60,'前の状態 hₜ₋₁')+box(245,252,205,80,'選択的な更新','Āₜ hₜ₋₁ + B̄ₜ xₜ')+box(540,262,205,60,'出力 yₜ','Cₜ hₜ',ORANGE)
    b+=line(169,292,239,292)+line(454,292,534,292)+line(347,144,347,246,BLUE)+line(642,144,642,256,ORANGE)
    b+=line(95,164,95,210,BLUE,arrow=False)+line(95,210,285,210,BLUE,arrow=False)+line(285,210,285,246,BLUE)
    b+=txt(400,386,'Aは共有。Δₜが変わるので、離散化後のĀₜも変わる。',16)
    return figure(svg(b,416,label='入力からB、C、Δを作り、選択的な状態更新と読み出しに使う'),
        ref(PAPER,'Mamba Figure 1・Algorithm 2')+'を、入力依存の経路に絞って再構成。')


def block_figure():
    b=box(285,20,230,48,'入力の特徴',color=BLUE)
    b+=line(400,70,400,101)+box(285,106,230,48,'正規化 → 線形変換')
    b+=line(400,156,400,179,arrow=False)+line(210,179,590,179,arrow=False)
    b+=line(210,179,210,208)+line(590,179,590,208)
    b+=box(95,213,230,68,'短い畳み込み → SiLU','近くの単語の情報を混ぜる',BLUE)
    b+=line(210,283,210,316)+box(95,321,230,82,'Selective SSM','記憶を選びながら引き継ぐ',GREEN)
    b+=box(475,213,230,68,'SiLUゲート','主経路の出力を調整する',PURPLE)
    b+=line(590,284,590,305,arrow=False)+line(590,305,750,305,arrow=False)+line(750,305,750,446,arrow=False)+line(750,446,429,446)
    b+=line(210,405,210,446,arrow=False)+line(210,446,370,446)
    b+=box(375,422,50,48,'×',color=PURPLE)+line(400,472,400,500)
    b+=box(285,505,230,48,'線形変換',color=ORANGE)+line(400,555,400,584)
    b+=box(375,589,50,48,'＋')+line(400,639,400,666)
    b+=box(285,671,230,48,'次のブロックへ',color=ORANGE)
    b+=line(285,44,40,44,arrow=False)+line(40,44,40,613,arrow=False)+line(40,613,368,613)
    b+=txt(76,544,'入力を',12)+txt(76,566,'足し戻す',12)
    b+=txt(590,379,'SSM内の選択とは別に、',13,PURPLE)+txt(590,401,'出力側にもゲートを置く。',13,PURPLE)
    return figure(svg(b,744,label='Mamba-1ブロックの主経路、ゲート経路、残差接続'),
        'Mamba-1のブロックを簡略化した独自図。×は成分ごとの積。短い畳み込みは未来を見ない因果的な処理。SSM出力には入力を直接渡すDの経路も含む。')


def build():
    body=sec('why','全ての要素を照合するか、記憶を渡していくか',
        p('系列が長くなるほど、過去の情報をどう使うかが計算量に効いてきます。Attentionは要素同士を直接照合します。SSMは過去の情報を状態にまとめ、入力を順に処理します。')+memory_figure()+
        p('系列長Nが2倍になると、密なAttentionの照合する組は約4倍になります。再帰SSMは一歩の計算をN回繰り返すため、状態の大きさが一定なら約2倍です。その代わり、必要な情報を限られた状態に残す工夫が必要です。'))
    body+=sec('state','SSM：入力の系列を、状態を介して出力へ変える',
        p('ここでは、Mamba論文と同じく<strong>線形の状態空間モデル（SSM）</strong>から始めます。入力xを読み、内部状態hを更新し、そこから出力yを作るモデルです。状態は、これまでの入力が後の出力に与える影響をまとめたベクトルです。')+
        eq(r'\frac{dh(t)}{dt}=Ah(t)+Bx(t),\qquad y(t)=Ch(t)',
           '連続時間の式。Aは状態そのものの変化、Bは入力が状態へ与える影響、Cは状態から出力への読み出しを表す。')+
        p('文章のトークンのように一つずつ来る入力では、時間幅Δごとの更新へ変換します。これを離散化と呼びます。以降は、この離散時間の式と図を対応させます。')+
        eq(r'h_t=\bar A h_{t-1}+\bar B x_t,\qquad y_t=C h_t',
           'Āは前の状態を引き継ぐ行列、B̄は新しい入力を書き込む行列、Cは読み出す行列。バーは離散化後の係数を表す。ここでは直接経路Dxₜを省略。')+
        p('入力・出力を1成分とすると、m次元の状態に対してAはm×m、Bはm×1、Cは1×mです。深層モデルでは特徴のチャネルごとにこの処理を使い、前後の射影や非線形関数と組み合わせます。')+
        p(ref(PAPER,'出典：Mamba §2、式(1)–(2)')))
    body+=sec('update','一歩の更新を、動きで追う',
        p('まずĀで前の状態を変換し、B̄で変換した入力を足してhₜを作ります。次にCを掛けてyₜを読み出します。出力を送り出したら、hₜを次の時刻の「前の状態」として左へ渡し、新しい入力xₜ₊₁を受け取ります。')+
        update_figure()+
        p('同じĀ・B̄・Cを各時刻で使い回します。入力が変わるので状態の値は変わりますが、この段階では更新の係数そのものは内容によって切り替わりません。'))
    body+=sec('hippo','HiPPO：過去の波形を、少数の係数に圧縮する',
        p('長い履歴を一定サイズで持つには、状態に何を入れるとよいでしょうか。HiPPOは<strong>過去の信号を基底の重み付き和で近似し、その係数を記憶する</strong>と考えます。入力を全点保存する代わりに、波形の近似に必要なm個の係数を持ちます。')+
        basis_figure()+
        eq(r'\hat f_t(s)=\sum_{k=0}^{m-1}c_k(t)\,p_k^{(t)}(s)',
           'sは過去の時刻、tは現在。pₖは基底関数、cₖはその係数。基底の形と時間軸の変換規則を共有し、状態として係数c(t)を保持する。mを有限にするので近似誤差は残る。')+
        img('hippo-framework.png','HiPPO著者図：黒い信号を赤と青の多項式で近似し、各時刻の係数ベクトルだけを更新する',
            '原図引用：'+ref(HIPPO,'Guほか、HiPPO著者解説 Figure 1')+'。黒が入力信号、赤と青が二つの時点での近似。下のベクトルが保存する係数。元画像のまま掲載。')+
        p('図では時間がt₀からt₁へ進んで履歴が伸びても、保存するベクトルの長さは変わりません。HiPPOは、選んだ重み付けで近似誤差が小さくなるように、これらの係数を<strong>前の係数と新しい入力だけから逐次更新する式</strong>を導きます。この式が線形SSMの形になります。')+
        sub('「最近を強く、昔を弱く」は、重み付けによって異なる',
            p('HiPPO全体が必ず指数的に昔を忘れるわけではありません。どの過去を重視するかを決める「測度（重み付け）」を先に選び、それに対応する基底と更新式を使います。')+
            table(['種類','過去への重み付け'],[
                ('LegS（scaled Legendre）','時刻0から現在tまでを一様に重み付け。過去全体を対象にする。'),
                ('LegT（translated Legendre）','直近の一定幅の窓内を一様に重み付け。窓の外は対象にしない。'),
                ('LagT（translated Laguerre）','古くなるほど指数的に重みを小さくする。最近を重視する。')])+ 
            img('hippo-measures.png','HiPPOのLegTは直近の固定窓、LegSは現在までの全履歴を一様に重み付けする',
                '原図引用：'+ref(HIPPO,'HiPPO著者解説 Figure 2')+'。左がLegT、右がLegS。色付きの長方形は、入力値ではなく過去への重み付け。')+
            p('LegSの右図では、現在tが進むと密度1/tは低くなりますが、<strong>同じ現在時刻では古い点も新しい点も同じ重み</strong>です。「古いほど重みが小さい」という図ではありません。'))+
        p('S4はHiPPO由来の構造を状態の更新行列に取り込み、長期記憶と効率的な計算を組み合わせます。学習後の深層モデルが、常に厳密な多項式の最適近似を保持しているという意味ではありません。Mamba-1の実数版は対角Aを使い、HiPPOの最適多項式近似をそのまま実行するモデルではありません。')+
        p(ref('https://papers.nips.cc/paper_files/paper/2020/file/102f0bb6efb3a6128a3c750dd16729be-Supplemental.pdf','出典：HiPPO論文 §2–3・補足D.2')+'、'+ref('https://arxiv.org/abs/2111.00396','S4論文')+'、'+ref(PAPER,'Mamba §3.6')))
    body+=sec('representations','なぜ畳み込みにするのか：学習時にまとめて計算するため',
        p('一語ずつ生成する場面では再帰が便利ですが、学習時には入力系列がそろっています。そこで、h₁ができるまでh₂を待つ計算を、入力から各出力をまとめて計算する形へ書き換えます。<strong>別のモデルに変更するのではなく、同じ線形SSMの計算方法を変えます。</strong>')+
        convolution_figure()+
        p('例えばy₃は、今の入力x₃にCB̄、一つ前のx₂にCĀB̄、二つ前のx₁にCĀ²B̄を掛けて足します。y₄でも同じ距離には同じ重みが使われます。この「同じ重み列をずらして掛けて足す」計算が畳み込みです。')+
        eq(r'K_k=C\bar A^k\bar B,\qquad y_t=\sum_{k=0}^{t-1}K_k x_{t-k}',
           'Kₖはkステップ前の入力に掛ける重み。h₀=0、固定係数を仮定。SSMのカーネルは一般に系列全体にわたり、短い局所フィルタとは異なる。')+
        p('畳み込みにすると、各出力の計算を並列に扱え、長い畳み込みにはFFTも使えます。直接の二重和はO(N²)ですが、FFTによる畳み込み部分はO(N log N)です。カーネル生成にも構造を使って効率化するのがS4の工夫です。生成時は再び状態を一歩ずつ更新します。')+
        p('<strong>重要な条件は、Ā・B̄・Cが時刻によらず共通であること。</strong>これが、次の選択的SSMで計算方法を変える理由になります。')+
        p(ref(PAPER,'出典：Mamba §2 Computation')+'、'+ref('https://arxiv.org/abs/2111.00396','S4 §3')))
    body+=sec('selective','Selective SSM：距離だけではなく、内容で選ぶ',
        p('Mamba論文は、選択が必要な理由を<strong>Selective Copying（選択的コピー）</strong>という課題で示しています。入力列にはコピーすべき記号と空白が混ざっています。最後の合図の後に、空白を除いた記号を元の順序で出力します。')+
        selection_figure()+
        p('覚える記号が毎回同じ位置にあるなら、「何ステップ前の入力を出せばよいか」で対処できます。しかしこの課題では記号の位置と間隔が毎回変わります。Aが来たら覚え、空白なら記憶を保ち、Bが来たら追加する、と<strong>入力の内容を見て記憶を変える</strong>必要があります。固定カーネルでは、同じ距離に同じ重みしか使えません。')+
        details('論文の元の比較図を見る',img('mamba-copying.svg','Mamba Figure 2：通常のCopying、Selective Copying、Induction Headsの比較',
            '原図：'+ref(PAPER,'Gu & Dao, Mamba, Figure 2')+'（CC BY 4.0）。左は間隔が一定のコピー、右上が選択的コピー、右下は文脈の対応を再利用するInduction Heads。'))+
        p('Mambaは、<strong>B・C・Δを今の入力から計算</strong>するようにします。Bは何を状態へ書き込むか、Cは何を読み出すか、Δは以前の状態を保つか新しい入力へ更新するかに関わります。これがSelective SSMです。')+
        selective_parameters()+
        details('論文の選択的SSMの原図を見る',img('mamba-selection.svg','Mamba Figure 1：入力依存のB、C、Δと選択的な状態更新', '原図：'+ref(PAPER,'Gu & Dao, Mamba, Figure 1')+'（CC BY 4.0）。上の日本語図では、原図の入力依存の経路を抜き出した。'))+
        eq(r'B_t=f_B(x_t),\quad C_t=f_C(x_t),\quad \Delta_t=\operatorname{softplus}(f_\Delta(x_t))',
           '関数fの重みを学習し、入力ごとの係数を得る。A自体は時刻間で共有する。ここでのxₜはブロック内で前処理された特徴。')+
        p('これは「記号をそのまま格納する箱」を実装するという意味ではありません。課題を解けるように、状態の数値を連続的に調整する方法を学習します。')+
        p('入力ごとに係数が変わると、全時刻で共通の畳み込みカーネルは使えません。そこで、線形更新の合成を並列にまとめる<strong>selective scan</strong>と、GPUのメモリの読み書きを減らす実装を使います。詳しい計算方法は末尾の補足で扱います。'))
    body+=sec('block','Mamba全体では、この記憶の仕組みを積み重ねる',
        p('Selective SSMはMambaの中心となる部品です。実際のブロックは、その前後にも処理を置きます。まず近くの単語を短い畳み込みで混ぜ、SSMで遠くまで記憶を伝え、別経路のゲートで出力を調整します。')+
        block_figure()+
        p('図の主経路にあるSSMが「時間方向に記憶を運ぶ」部分です。右のゲートは、その出力をどれだけ通すかを調整します。さらに入力を足し戻す残差接続を使い、このブロックを何層も重ねて、予測に役立つ特徴を作ります。SiLUは滑らかな非線形の活性化関数です。'))
    body+=sec('train-use','何が軽くなり、何が難しさとして残るか',
        p('生成時には、各層のSSMの状態と、短い畳み込みに必要な直近の特徴を保持し、新しい入力が来たら更新します。<strong>モデルの大きさを固定すれば、この記憶の容量は文章の長さによって増えません。</strong>過去の全位置を照合しないため、系列長に対する処理量を線形にできます。')+
        p('一方、状態が一定サイズであることは、すべてを正確に記憶できるという意味ではありません。Mambaは選択によって限られた状態を活用しますが、過去の細部を後から直接調べるAttentionとは得意なことが異なります。')+
        table(['','密なAttention','Mambaの選択的SSM'],[
            ('過去をどう持つか','各位置のK・Vを保持','一定サイズの状態へまとめる'),
            ('必要な情報をどう使うか','今のqueryで過去の位置を照合','書き込み・保持・読み出しを入力から調整'),
            ('長くなると','参照対象とKVキャッシュが増える','生成中に保持する状態の大きさは一定'),
            ('課題','長い系列の照合コスト','限られた状態に必要な情報を残すこと')])+
        details('実行の補足：選択すると、学習の並列化はどうなるか',
            p('入力ごとに係数が変わると、先ほどの固定カーネルの畳み込みは使えません。そこでMambaは、線形の更新をまとめて合成できる性質を使うparallel scanで計算します。')+
            eq(r'h_1=a_1h_0+b_1,\quad h_2=a_2h_1+b_2=(a_2a_1)h_0+(a_2b_1+b_2)',
               '二つの更新を、一つの更新にまとめた例。三つ以上でも、時間の順序を保ったまま「どこを先にまとめるか」を変えられる。この結合則を利用して並列に計算する。トークンの順序を入れ替えるわけではない。')+
            p('さらに、離散化・状態更新・読み出しをまとめて実行するkernel fusionや、逆伝播での中間状態の再計算により、GPU内のメモリの読み書きを減らします。理論上の計算量だけでなく、実際の装置で効率よく動くように設計しています。')+
            p('比較の条件：密なAttentionでは、系列全体の照合は長さLに対してO(L²)。KVキャッシュを使う生成では過去のK・Vを再計算せず、新しいqueryから過去への照合が一歩あたりO(L)です。Mambaの再帰生成は、モデル幅・状態次元・畳み込み幅を固定すると一歩あたりO(1)、LステップでO(L)です。これは全タスク・全装置で速度や精度が上回る保証ではありません。')))
    body+=refs([
        ('構成の参考：Maarten Grootendorst — A Visual Guide to Mamba and State Space Models',GUIDE),
        ('SSMとMambaの技術的な出典：Gu & Dao — Mamba（§2–3）',PAPER),
        ('S4：Efficiently Modeling Long Sequences with Structured State Spaces','https://arxiv.org/abs/2111.00396'),
        ('HiPPO：Recurrent Memory with Optimal Polynomial Projections','https://arxiv.org/abs/2008.07669'),
        ('HiPPOの著者解説：基底・係数・重み付け',HIPPO),
        ('Mamba-1ブロックの著者実装','https://github.com/state-spaces/mamba/blob/main/mamba_ssm/modules/mamba_simple.py')])
    version=hashlib.sha256((ROOT/'assets/ssm.js').read_bytes()).hexdigest()[:10]
    body+=f'<script src="assets/ssm.js?v={version}" defer></script>'
    page('ssm','SSM・Mamba — 状態への書き込みを選ぶ','モデルの構造','MODEL 05 / SELECTIVE STATE SPACES',
         '過去を小さな記憶にまとめるSSM。その記憶に「何を入れ、何を残すか」を入力に応じて変えるMambaを、具体例と図から理解します。',body)
