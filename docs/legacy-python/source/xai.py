"""XAI lesson: small attribution examples, matched image results and LLM cases."""
import json
from common import *

BIOLOGY = 'https://transformer-circuits.pub/2025/attribution-graphs/biology.html'
TRACING = 'https://www.anthropic.com/research/tracing-thoughts-language-model'


def shapley_figure():
    b = txt(400, 28, '同じ入力・同じ評価データで、中間モジュールを止めて比べる', 18)
    for row, (title, stopped, score, change) in enumerate([
        ('① フルモデル', None, '正解率 90%', '基準'),
        ('② Bを止める', 'B', '正解率 75%', '15ポイント低下'),
        ('③ Dを止める', 'D', '正解率 85%', '5ポイント低下'),
    ]):
        y = 62 + row * 218
        b += txt(25, y, title, 18, anchor='start')
        b += box(25, y+67, 85, 48, '入力', color=BLUE)
        b += box(525, y+67, 90, 48, '出力', color=BLUE)
        b += txt(702, y+80, score, 19) + txt(702, y+111, change, 15, ORANGE)
        for i, name in enumerate('ABCD'):
            yy = y+20+i*43
            off = name == stopped
            color = '#9b9b9b' if off else GREEN
            b += line(114, y+91, 265, yy+17, color, dash=off)
            b += line(398, yy+17, 520, y+91, color, dash=off)
            b += box(270, yy, 122, 34, name + ('：停止' if off else ''), color=color)
            if off:
                b += line(274, yy+3, 388, yy+31, ORANGE, arrow=False)
    b += txt(400, 726, 'さらに A・Bだけ、B・C・Dだけ…と、残す組み合わせを変える', 17)
    b += txt(400, 759, '各組み合わせで「止める前 − 止めた後」を調べ、平均する', 18, GREEN)
    return figure(svg(b, 786, label='四つの並列モジュールがあるフルモデル、B停止、D停止の性能比較'),
                  '架空の性能。停止時は出力を0にし、再学習しない。この比較を除去順を変えて繰り返す。')


def decomposition_figure():
    b = txt(400, 28, '予測は右へ計算し、寄与は左へ戻していく', 20)
    b += txt(100, 68, '入力', 16) + txt(390, 68, '中間ニューロン', 16) + txt(695, 68, '出力', 16)
    nodes = [(100,125,'2'), (100,235,'1'), (100,345,'3'), (390,165,'4'), (390,305,'6'), (695,235,'10')]
    edges = [(0,3,'×1'), (1,3,'×2'), (1,4,'×3'), (2,4,'×1'), (3,5,'×1'), (4,5,'×1')]
    for i,j,w in edges:
        x,y,_ = nodes[i]; xx,yy,_ = nodes[j]
        b += line(x+31,y,xx-33,yy, '#b9c2b6')
        b += txt((x+xx)/2, (y+yy)/2-9, w, 13)
    for x,y,t in nodes:
        b += f'<circle cx="{x}" cy="{y}" r="30" fill="#f4f7f3" stroke="{GREEN}"/>' + txt(x,y+6,t,20)
    b += txt(400, 402, 'この例では、重みを掛けて足すだけのNNを使う', 16)
    b += txt(400, 450, '出力10を、通ってきた枝へ配り直す', 20, ORANGE)
    b += box(625, 515, 145, 65, '出力の寄与', '10', BLUE)
    b += box(330, 478, 150, 55, '上の経路：4', color=ORANGE)
    b += box(330, 610, 150, 55, '下の経路：6', color=ORANGE)
    b += box(25, 465, 150, 50, '入力①：2')
    b += box(25, 550, 150, 50, '入力②：5')
    b += box(25, 635, 150, 50, '入力③：3')
    for x,y,xx,yy in [(620,535,485,505),(620,565,485,637),(325,498,180,490),(325,520,180,565),(325,622,180,585),(325,645,180,660)]:
        b += line(x,y,xx,yy,ORANGE,width=3)
    for x,y,t in [(245,480,'2'),(245,539,'2'),(245,601,'3'),(245,641,'3')]:
        b += txt(x,y,t,17,ORANGE)
    b += txt(400, 729, '入力②には両方の経路から戻る：2 + 3 = 5', 17)
    b += txt(400, 764, '入力の寄与を足すと、出力に戻る：2 + 5 + 3 = 10', 18, GREEN)
    return figure(svg(b, 791, label='簡単なNNの出力10を中間層の4と6、入力の2と5と3へ逆向きに分解する'),
                  'バイアス・非線形処理のないNN、基準入力は0。橙は寄与を戻す向き（学習ではない）。')


def feature_shapley_figure():
    b = txt(400,28,'メールの特徴を一つ隠し、同じモデルの予測を比べる',19)
    for row,(title,hidden,score,delta) in enumerate([
        ('元の入力',None,'80','基準'),
        ('「至急」を隠す',0,'50','30低下'),
        ('リンクを隠す',1,'70','10低下'),
    ]):
        y=65+row*135
        b += txt(20,y,title,17,anchor='start')
        for i,(name,value) in enumerate([('「至急」','あり'),('リンク','あり'),('送信元','不明')]):
            x=20+i*118; off=i==hidden
            b += box(x,y+20,108,58,name,'隠す' if off else value, '#929b96' if off else GREEN)
            if off: b += line(x+5,y+25,x+103,y+73,ORANGE,arrow=False)
        b += line(369,y+49,413,y+49)
        b += box(420,y+20,150,58,'同じモデル',color=BLUE)
        b += line(577,y+49,621,y+49)
        b += box(628,y+12,150,74,'スコア '+score,delta,ORANGE)
    b += txt(400,489,'残す特徴の組み合わせを変え、スコア差を平均 → 各特徴の寄与',17)
    return figure(svg(b,519,label='メールの至急という語やリンクを隠したときの迷惑メールスコアの比較').replace('<svg ', '<svg id="feature-shapley" ', 1),
                  '架空の迷惑メールスコア（確率ではない）。ここでは「隠す」を「なし」に置き換える。3行は単独の比較で、SHAPでは除去順を変えて平均する。')


def dice_figure():
    b = txt(400,28,'同じ人でも、変える項目によって別の案になる',20)
    for x,title,income,amount,verdict,color in [
        (20,'元の申請',300,150,'否決',BLUE),
        (287,'案A：年収を変える',420,150,'承認',GREEN),
        (554,'案B：希望額を変える',300,30,'承認',ORANGE),
    ]:
        b += txt(x+113,80,title,18,color)
        b += txt(x,128,'年収',14,anchor='start') + txt(x+220,128,str(income)+'万円',18,color,anchor='end')
        b += f'<rect x="{x}" y="143" width="{income*.48}" height="24" rx="3" fill="{color}"/>'
        b += txt(x,211,'希望額',14,anchor='start') + txt(x+220,211,str(amount)+'万円',18,color,anchor='end')
        b += f'<rect x="{x}" y="226" width="{amount*.48}" height="24" rx="3" fill="{color}"/>'
        b += line(x,281,x+220,281,'#d2d9d1',arrow=False,width=1)
        b += txt(x+110,320,verdict,24,color)
    b += txt(400,376,'A：年収を120万円増やす　／　B：希望額を120万円減らす',17)
    return figure(svg(b,408,label='元の申請は否決、年収を増やす案Aと希望額を減らす案Bは承認となる比較'),
                  'DiCEの考え方を示す架空の審査例。棒は金額を同じ尺度で表示。実際の審査基準やDiCEの実験結果ではない。')


def arithmetic_figure():
    b = txt(400,28,'多数の計算がつながり、答えが出る',20)
    b += '<rect x="99" y="54" width="597" height="447" rx="12" fill="#f7f9f6" stroke="#c1cbc2"/>'
    b += box(10,251,72,58,'36+59','入力',BLUE)
    b += box(719,251,72,58,'95','出力',BLUE)
    rows = [
        (80, [('その他',''),('その他',''),('その他','')], '#98a59d'),
        (190,[('大きさを拾う','36付近・60付近'),('組み合わせを照合','近い数どうしの和'),('大まかな和','92の近く')],GREEN),
        (300,[('一の位を拾う','6 と 9'),('末尾の組を照合','6 + 9 → 末尾5'),('答えの末尾','5')],ORANGE),
        (410,[('その他',''),('その他',''),('その他','')], '#98a59d'),
    ]
    for y,nodes,color in rows:
        other = y in (80,410)
        b += line(85,280,116,y+33,color,dash=other)
        for i,(title,detail) in enumerate(nodes):
            x=120+i*200
            b += box(x,y,155,66,title,detail,color)
            if i<2: b += line(x+159,y+33,x+195,y+33,color,dash=other)
        b += line(678,y+33,714,280,color,dash=other)
    b += txt(400,535,'色付き：解析された役割　　灰色・破線：省略した計算のつながり',16)
    return figure(svg(b,566,label='入力36+59から、その他の計算と大きさ・一の位の経路が出力95につながる模式図'),
                  'Lindsey et al.（2025）を簡略化。灰色の配線は説明用で、実測の回路図ではない。「92の近く」は粗い特徴を表す。')


def planning_figure():
    b = txt(30,35,'課題：1行目と韻を踏む2行目を続ける',20,anchor='start')
    b += txt(30,87,'He saw a carrot and had to grab it,',23,BLUE,anchor='start')
    b += txt(30,116,'ニンジンを見て、つかまずにはいられなかった',14,anchor='start')
    b += txt(30,163,'grab it と音が似た rabbit（ウサギ）が、次の末尾候補になる',17,anchor='start')
    # A shared manuscript continuation branches directly to sentences; no flowchart boxes.
    b += txt(30,246,'2行目はまだ空白',17,BLUE,anchor='start')
    b += txt(30,276,'rabbit の特徴が活動',15,BLUE,anchor='start')
    for y,operation,first,last,color in [
        (232,'操作なし','His hunger was like a','starving rabbit',GREEN),
        (366,'rabbit の特徴を弱める','習慣について述べる文へ','… habit',BLUE),
        (500,'候補を抑え、green を強める','緑について述べる文へ','… green',ORANGE),
    ]:
        b += f'<path d="M220 261 C280 261 260 {y} 420 {y}" fill="none" stroke="{color}" stroke-width="2" marker-end="url(#arrow)"/>'
        b += txt(250,y-27,operation,14,color,anchor='start')
        b += txt(435,y+10,first,20,anchor='start')
        b += txt(435,y+41,last,22,color,anchor='start')
    return figure(svg(b,571,label='grab itで終わる1行目から、内部状態への操作に応じてrabbit、habit、greenへ続く詩'),
                  'Anthropic（2025）。無介入の英文は報告例。他の2文は内容の要約。greenへの操作は韻を崩すこともある。')


def multilingual_figure():
    b = txt(400,30,'同じ「反対語」の問いを、3言語で比べる',20)
    b += txt(30,77,'入力',14,anchor='start') + txt(750,77,'出力',14,anchor='end')
    b += '<rect x="250" y="92" width="300" height="240" rx="10" fill="#eef4e9"/>'
    b += txt(400,123,'共通する意味の処理',17,GREEN)
    b += txt(400,193,'小さい → 反対 → 大きい',19,GREEN)
    b += txt(400,290,'＋ 言語を選ぶ処理',15)
    for y,lang,word,answer in [(157,'英語','small','big'),(225,'フランス語','petit','grand'),(293,'中国語','小','大')]:
        b += txt(25,y,lang,13,anchor='start') + txt(175,y,word,23,BLUE)
        b += line(212,y-6,241,y-6)
        b += line(559,y-6,590,y-6)
        b += txt(674,y,answer,23,BLUE)
    return figure(svg(b,360,label='small、petit、小から共通の意味処理を通り、big、grand、大へ至る比較'),
                  'Lindsey et al.（2025）の模式図。意味の処理を共有しつつ、言語ごとの表記を選ぶ。')


def image_comparison():
    meta = json.loads((ROOT / 'assets/xai-results.json').read_text())
    result = p('<strong>同じモデルでも、説明の仕方は一つではありません。</strong>同じ写真・同じResNet-18の「猫」スコアを、3手法で調べます。')
    result += '<div class="scene-grid">' + img('xai-input.png', '猫と犬がいる共通入力', '共通入力。説明する対象は猫。') + img('xai-segments.png', 'スーパーピクセルへの分割', '色や位置が近い画素をまとめた領域。黄色は境界で、重要度ではありません。') + '</div>'
    result += '<div class="scene-grid">' + ''.join(img(name, alt, caption) for name, alt, caption in [
        ('xai-saliency.png', '画素ごとの勾配の大きさ', '<strong>① 画素：Saliency</strong><br>画素を少し変えたとき、猫スコアがどれだけ動くかを微分で調べます。明るいほど敏感な場所です。上げる・下げる方向は区別しません。'),
        ('xai-lime.png', 'LIME方式による領域の寄与', '<strong>② 領域：LIME方式</strong><br>領域を隠した画像を多数入力し、スコアを簡単な足し算で近似します。赤は猫スコアを上げる側、青は下げる側の係数です。<br>' + ref('https://arxiv.org/abs/1602.04938', 'LIMEの原論文')),
        ('xai-gradcam.png', 'Grad-CAMによる猫を支える場所', '<strong>③ 内部特徴：Grad-CAM</strong><br>猫スコアから微分を戻し、関係の強い特徴マップを重ねます。黄・橙は猫スコアを支える場所。粗いマップの拡大なので、大まかな位置として読みます。<br>' + ref('https://arxiv.org/abs/1610.02391', 'Grad-CAMの原論文')),
    ]) + '</div>'
    result += p('ヒートマップは数値を色で示す表示形式です。色の尺度は手法ごとに異なります。')
    result += '<details><summary>計算条件・再現用データ</summary>' + p(
        'Grad-CAM論文の原写真、ResNet-18（IMAGENET1K_V1）、クラス281のsoftmax前スコア。'
        f'LIME方式は{meta["lime_segments"]}領域・黒塗り{meta["lime_samples"]}例のRidge近似（R²={meta["lime_weighted_r2"]:.2f}）。') + p(
        ref('source/xai_image_results.py', '再現用コード') + ' · ' + ref('assets/xai-results.json', '計算条件') + ' · ' +
        ref('assets/xai-attributions.npz', '数値データ') + ' · ' + ref('https://docs.pytorch.org/vision/stable/models/generated/torchvision.models.resnet18.html', 'モデル出典')) + '</details>'
    return result


def build():
    body = sec('start', 'XAIとは：AIの判断の手がかりを調べる',
        p('<strong>XAI（説明可能AI）は、AIが何を手がかりに判断したかを、人が分かる形で示す方法です。</strong>例えば「猫の姿を見ているのか、背景を覚えただけなのか」を調べます。') +
        p('正解率だけでは見えない判断の仕組みを知り、誤りの原因や改善点を探すことが目的です。'))

    body += sec('shapley', 'Shapley：部品を止めると、どれくらい性能が下がる？',
        p('<strong>部品を止めたときの性能低下から、その役割を調べます。</strong>ただし、他にどの部品が動いているかで下がり幅は変わります。') +
        shapley_figure() +
        p('Shapley値は、<strong>部品を取り除く順番を変え、その部品を止めた瞬間の性能差を平均</strong>します。多くの部品がある場合は、順番を抽出して近似します。') +
        sub('入力の特徴にも、同じ考え方を使える',
            p('部品の代わりに入力の特徴を隠せば、どの特徴が予測を支えたかを調べられます。1件の予測スコアの差を各特徴に配分する代表例が<strong>SHAP</strong>です。') + feature_shapley_figure()) +
        p(ref('https://arxiv.org/abs/1705.07874', 'Lundberg & Lee（2017）：SHAP')))

    body += sec('contributions', '寄与度分解：出力から入力へ、内訳をたどる',
        p('<strong>予測スコアが、どの入力からどれだけ来たかを分けます。</strong>計算のつながりを、出力から入力へ逆向きにたどります。') +
        decomposition_figure() +
        p('同じ入力へ戻った値を足すと、その入力の寄与になります。非線形なNNでは、寄与を配るルールも必要です。'))

    body += sec('gradcam', '画像：同じモデルに、三つの説明を並べる', image_comparison())

    body += sec('counterfactual', '反実仮想①：金髪と判定される顔へ変える',
        p('反実仮想は、<strong>どこを変えれば別の判定になるか</strong>を示す説明です。ここでは顔らしさを保ちながら、金髪スコアが上がるように画像を少しずつ変えます。') +
        flow([('元の顔写真', '金髪ではない', BLUE), ('少し変更する', '金髪スコアを上げる'),
              ('顔らしさを保つ', '生成モデルを使う'), ('変更後の写真', '金髪と判定', ORANGE)],
             'モデルは固定し、入力側を変えて再予測する。') +
        img('counterfactual.png', '元画像、再構成、金髪へ変更、差分の四列',
            '著者公開のCelebA / Glowの結果。左から元画像、再構成、金髪へ変更、画素差分。髪以外も変わりうる。') +
        p(ref('https://github.com/annahdo/counterfactuals', 'Dombrowski et al.：著者実装・結果')))

    body += sec('dice', '反実仮想②：別の判定になる変更案を複数探す',
        p('<strong>変更案が複数あれば、実行しやすい案を選べます。</strong>DiCEでは、同じ判定に至る異なる変更案を探します。図では「年収を増やす」と「希望額を減らす」を比べます。') +
        dice_figure() +
        p('「年齢は固定」など、変更できる項目を指定できます。モデル上の判定変更を示すもので、現実の実行可能性は別に考えます。') +
        p(ref('https://interpret.ml/DiCE/readme.html', 'DiCE：著者解説')))

    body += sec('llm', 'LLM：内部で何をしているかを見る',
        p('<strong>答えの文章だけでなく、内部の活動や、そこへ介入したときの変化を調べます。</strong>以下の図のモジュールは、解析で見つけた特徴群を働きごとにまとめたものです。'))

    body += sec('arithmetic', 'LLM①：36＋59を、どうやって95にする？',
        p('<strong>一の位を扱う部分と、答えの大まかな大きさを絞る部分が並行して働きます。</strong>2025年のClaude 3.5 Haikuで見つかった例です。') +
        arithmetic_figure() +
        p('本人に聞くと筆算を説明しますが、解析された内部計算とは異なりました。<strong>生成した説明と、実際の計算は一致するとは限りません。</strong>') +
        p(ref(BIOLOGY + '#addition', 'Lindsey et al.（2025）：Addition')))

    body += sec('planning', 'LLM②：詩の末尾を、先に考えている？',
        p('1行目の末尾は<strong>grab it</strong>。これと韻を踏む2行目を作る課題です。まだ2行目を書いていない段階で、末尾候補<strong>rabbit</strong>の特徴が活動していました。') +
        planning_figure() +
        p(ref(TRACING, 'Anthropic（2025）：Claude 3.5 Haikuの詩の計画')))

    body += sec('concepts', 'LLM③：言語が違っても、意味の処理は共通？',
        p('<strong>英語・フランス語・中国語で反対語を尋ねると、共通の意味の処理が見つかりました。</strong>答えの表記は、言語ごとの処理で選びます。') +
        multilingual_figure() +
        p(ref(BIOLOGY, 'Lindsey et al.（2025）：Claude 3.5 Haikuの多言語回路')))

    body += refs([
        ('SHAP', 'https://arxiv.org/abs/1705.07874'),
        ('LIME', 'https://arxiv.org/abs/1602.04938'),
        ('Grad-CAM', 'https://arxiv.org/abs/1610.02391'),
        ('顔画像の反実仮想', 'https://github.com/annahdo/counterfactuals'),
        ('DiCE', 'https://interpret.ml/DiCE/readme.html'),
        ('LLMの算術・多言語', BIOLOGY),
        ('LLMの詩の計画', TRACING),
    ])
    page('xai-advanced', 'XAI — AIの判断と内部の仕組みを調べる', '横断的な研究',
         'FOCUS / EXPLAINABLE AI',
         '部品を止める、寄与に分ける、入力を変える。図と具体例で、AIの判断を調べる方法を見ます。', body)
