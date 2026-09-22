"""Image tasks: paired, geometrically consistent teaching diagrams and research outputs."""
from common import *

CAR = 'M 0 36 L 12 30 L 29 6 Q 32 2 39 2 L 88 2 Q 95 2 100 10 L 115 30 L 132 36 Q 138 38 138 45 L 138 66 L 127 66 A 13 13 0 0 1 101 66 L 38 66 A 13 13 0 0 1 12 66 L 0 66 Z'

def scene(mode='input',sample=0):
    instance = mode == 'instance'
    sky,grass,road = ('#edf0f2',)*3 if instance else ('#c7e4f5','#9cbf86','#697781')
    b=f'<rect width="340" height="220" fill="{sky}"/><rect y="95" width="340" height="125" fill="{grass}"/><path d="M130 95 H225 L340 220 H0Z" fill="{road}"/>'
    if mode in ('input','detection'):
        b+='<path d="M177 115L173 131 M164 153L150 180 M140 200L130 220" stroke="white" stroke-width="4"/>'
    for i,(x,y,s) in enumerate([(182,105,.67),(32,133,1)] if sample==0 else [(147,98,.43),(205,121,.58),(54,131,.94)]):
        col = '#b46342' if mode=='semantic' else ['#8165bd','#d58e30','#418f88'][i] if mode in ('instance','panoptic') else (['#437fa4','#bd604b'] if sample==0 else ['#c8a043','#547989','#72975a'])[i]
        b+=f'<g transform="translate({x} {y}) scale({s})"><path d="{CAR}" fill="{col}"/>'
        if mode in ('input','detection'):
            b+='<path d="M36 9H59V29H21Z M65 9H86L102 29H65Z" fill="#d8edf1"/><circle cx="25" cy="65" r="9" fill="#243741"/><circle cx="114" cy="65" r="9" fill="#243741"/>'
        else: b+=txt(69,49,'車' if mode=='semantic' else f'車 {i+1}',16,'white')
        b+='</g>'
        if mode=='detection':
            b+=f'<rect x="{x-4}" y="{y-4}" width="{138*s+8}" height="{79*s+8}" fill="none" stroke="#9b3346" stroke-width="2"/>'+txt(x,y-9,'車',13,'#762739','start')
    if mode in ('semantic','panoptic'):
        b+=txt(40,40,'空',16)+txt(295,113,'草地',16)+txt(286,207,'道路',16,'white')
    return b

def dataset_figure(rows,output,caption):
    content='<div class="vision-data-head"><span>入力画像</span><span>'+output+'</span></div>'
    for left,right in rows:
        content+='<div class="vision-data-row">'+left+right+'</div>'
    return '<figure class="vision-dataset">'+content+'<figcaption>'+caption+'</figcaption></figure>'

def drawing(body,label):
    return svg(body,220,340,label)

def street_data(mode):
    rows=[]
    for sample in range(2):
        right=drawing(scene(mode,sample),'出力：'+mode)
        rows.append((drawing(scene(sample=sample),'街路画像：'+str(sample+2)+'台の車'),right))
    output={'detection':'枠とクラス','semantic':'種類ごとの領域','instance':'物体ごとのマスク','panoptic':'物体の個体と背景の種類'}[mode]
    return dataset_figure(rows,output,'同じ教材用データ集合の異なる2枚。上は2台、下は3台の街路画像。各タスクで同じ入力を使用。図と出力は教材用の作図で、実モデルの推論結果ではない。')

def age_data():
    rows=[]
    for index,age in [(2000,30),(2001,35)]:
        picture=f'<img class="vision-face" src="assets/utkface-train-{index}-age-{age}.jpg" alt="UTKFaceの顔画像、train行{index}" loading="lazy">'
        rows.append((picture,f'<div class="vision-answer">{age}.0 歳</div>'))
    return dataset_figure(rows,'年齢（歳）','<a href="https://susanqq.github.io/UTKFace/">UTKFace</a>の同じデータセットから2枚。右の数値はデータの年齢ラベルを出力形式に合わせて表示したもので、新たな推論結果ではない。')

def depth_pair():
    rows=[]
    for stem,alt in [('depth','街路'),('depth-bicycle','自転車')]:
        rows.append(tuple('<a href="assets/'+stem+'-'+suffix+'.jpg" target="_blank" rel="noopener"><img loading="lazy" src="assets/'+stem+'-'+suffix+'.jpg" alt="'+alt+label+'"></a>' for suffix,label in [('input','の入力写真'),('result','の相対深度マップ')]))
    return dataset_figure(rows,'深度マップ','Depth Anything V2の<a href="https://depth-anything-v2.github.io/">著者公開の同じ結果集</a>から2枚を引用。赤・橙・黄は近い側、青・紫は遠い側。色は表示用で、別の画像との色の一致は同じ実距離を意味しない。画像を押すと拡大。')

def pose_data():
    images=''.join(f'<a href="assets/blazepose-fig6-yoga{i}.png" target="_blank" rel="noopener"><img src="assets/blazepose-fig6-yoga{i}.png" alt="BlazePose論文Figure 6の姿勢推定結果：'+('両腕を上げて前後に脚を開いた人物' if i==1 else '両手を床についてしゃがんだ人物')+'" loading="lazy"></a>' for i in [1,2])
    return '<figure class="vision-dataset"><div class="vision-paper-pair">'+images+'</div><figcaption>Bazarevsky et al.（2020）, <a href="https://arxiv.org/html/2006.10204v1#S4.F6">BlazePose: On-device Real-time Body Pose tracking, Figure 6</a>のヨガ・フィットネスの結果から2枚を引用。各パネルは加工せず掲載。白い点が特徴点、色付きの線が点どうしの接続。画像を押すと拡大。</figcaption></figure>'

def pet_data():
    rows=[]
    for name,label in [('pet-dog.jpg','犬'),('pet-cat.jpg','猫')]:
        rows.append((f'<img class="vision-pet" src="assets/{name}" alt="Oxford-IIIT Petの{label}の写真" loading="lazy">',f'<div class="vision-answer">{label}</div>'))
    return dataset_figure(rows,'ラベル','<a href="https://www.robots.ox.ac.uk/~vgg/data/pets/">Oxford-IIIT Pet</a>の同じデータセットから犬と猫を1枚ずつ掲載。種別の注釈を「犬」「猫」として表示。新たな推論結果ではない。CC BY-SA 4.0。写真は加工なし。')

def body():
    out=sec('output','画像から何を知りたいか',p('画像のタスクは、画像から何を答えてほしいかで分かれます。「犬か猫か」「何歳か」「どこにあるか」「どの画素が車か」は、それぞれ異なる問いです。まず一覧で答えの形を見てから、各タスクの図を見ていきます。')+table(['タスク','入力 → 出力','実問題の例'],[
        ('<a href="#classification">画像分類</a>','画像 → ラベル','犬と猫の判別、製品の良否'),
        ('<a href="#regression">画像からの回帰</a>','画像 → 数値','顔画像からの年齢推定'),
        ('<a href="#detection">物体検出</a>','画像 → 物体の枠とクラス','歩行者や商品の位置'),
        ('<a href="#segmentation">セグメンテーション</a>','画像 → 画素ごとの領域','浸水域、臓器、道路の範囲'),
        ('<a href="#depth">深度推定</a>','画像 → 画素ごとの奥行き','障害物の遠近、3Dへの手がかり'),
        ('<a href="#pose">姿勢推定</a>','画像 → 関節などの座標','スポーツのフォーム、動作の記録')]))
    out+=sec('classification','画像分類：画像にラベルを付ける',p('画像分類（image classification）は、画像全体がどのカテゴリに当てはまるかを答えます。ここでは「犬」「猫」の2種類を見分けます。入力は写真、出力はその写真に対応する一つのラベルです。')+pet_data()+p('学習では犬の画像には「犬」、猫の画像には「猫」というラベルを付けたデータを使います。色・姿勢・背景が違う写真でも、動物の特徴から種類を見分けることが目標です。出力のラベルだけでは、画像内のどの範囲が動物なのかは表せません。')+p('このように一つのカテゴリを選ぶ設定を単一ラベル分類と呼びます。一枚に犬と猫が両方写ることを想定し、それぞれの有無を答えるなら、複数のラベルを同時に付ける設定にします。何を答えさせたいかに合わせて、ラベルとデータを用意します。'))
    out+=sec('regression','画像からの回帰：年齢を数値で推定する',p('画像からの回帰（regression）は、画像を手がかりに数値を推定するタスクです。ここでは顔画像を入力し、年齢を歳単位の数値として出力します。同じ顔画像データセットの異なる人物でも、入力と出力の形式は共通です。')+age_data()+p('「20代」「30代」のような年代のカテゴリを選ぶ設定は分類です。年齢を30.0歳や34.7歳のような数値で出す設定では、回帰として扱えます。学習では顔画像と年齢の組を使い、画像の特徴と数値の対応を学びます。')+p('写真の照明・表情・解像度や個人差によって、見た目から読み取れる年齢には曖昧さがあります。UTKFaceの年齢も推定と人による確認を経た注釈で、本人の生年月日を保証する値ではありません。ここでは、そのような数値を出力するタスクの形を見ています。'))
    out+=sec('detection','物体検出：物体の位置を枠で囲む',p('物体検出（object detection）は、画像内の物体ごとに、位置を示す長方形の枠とクラスを返します。通常は、その検出に対するスコアも付きます。一枚の画像から複数の検出結果を出せるため、「車が2台あり、それぞれここにいる」と表せます。')+street_data('detection')+p('歩行者の位置を知る、棚の商品を数える、といった用途につながります。図の枠には車体だけでなく周囲の背景も入っています。枠は物体の位置とおおよその広がりを表しますが、窓やタイヤまで含めた輪郭そのものを出すわけではありません。重なった物体や小さな物体を、一つずつ見つけることが難しい場面です。'))
    out+=sec('segmentation','セグメンテーション：画素ごとに領域を分ける',p('セグメンテーション（segmentation）は、物体や背景の領域を画素単位で表すタスクです。医用画像の臓器の輪郭、衛星画像の浸水範囲など、長方形では表しにくい形を取り出せます。何を区別するかによって、次の3種類があります。ここでは同じ街路データの2枚を使い、3種類の出力を比較します。')
    +sub('1. セマンティック：種類ごとに塗り分ける',p('semantic segmentationは、各画素に「車」「空」「草地」「道路」などのクラスを割り当てます。2台の車は同じ「車」なので同じ色です。画素がどの種類かは分かりますが、出力のラベル自体には車1・車2という個体のIDがありません。')+street_data('semantic')+p('道路として使える範囲や土地利用の割合を調べるなど、種類ごとの広がりを知りたい問題に向きます。隣り合う同種の物体を別々に数えるには、別の処理が必要です。'))
    +sub('2. インスタンス：物体を1個ずつ分ける',p('instance segmentationは、物体ごとに別々のマスクを出します。マスクとは、その対象に属する画素の集合です。図の2台は同じ車クラスでも、「車1」と「車2」で色が違います。空や道路などの背景には、この出力ではクラスを付けていません。')+street_data('instance')+p('細胞を一つずつ数えて面積を測る、複数の商品を個別に切り抜く、といった問題につながります。単に種類を付けることに加え、接している同種の物体を別の個体として分ける必要があります。ここでの番号は画像内での区別であり、動画をまたぐ追跡IDとは限りません。'))
    +sub('3. パノプティック：物体の個体と背景の種類を両方付ける',p('panoptic segmentationは、画像全体の各画素に意味を付けつつ、車や人のように数えられる物体を個体ごとに区別します。車1・車2は別の色、空・草地・道路にもそれぞれのクラスがあります。一つの画素は、一つの領域に属する形で出力をまとめます。')+street_data('panoptic')+p('街路全体を「移動できる道路」「個々の車」「背景」のように整理したいときに役立ちます。セマンティックとの違いは車の個体IDがあること、インスタンスとの違いは背景も含めて画面全体を扱うことです。')))
    out+=sec('depth','深度推定：画素ごとの奥行きを求める',p('深度推定（depth estimation）は、画像内の各位置がカメラからどれだけ離れているかを推定するタスクです。ここでは1枚の写真から推定する単眼深度推定を見ます。出力は画像と対応した数値のマップで、見やすくするために数値を色へ変換しています。')+depth_pair()+p('上段は街路、下段は自転車です。下段の車輪では、細いスポークと隙間から見える地面が異なる奥行きとして表されています。同じ深度推定でも、入力ごとに異なる値のマップを出します。')+p('上段の右手前の車、後方のバス、中央奥の建物の順に見てください。出力では手前の車が橙、バスが緑、遠方が青紫になっています。道路も手前から奥へ連続的に色が変わります。セグメンテーションと違い、同じ道路の内部でも奥行きが違えば値が変わります。')+p('相対深度は「こちらが近い」という遠近関係を表します。メートル単位の深度は、実際の距離を数値として求める設定です。一枚の写真だけでは小さい物体が近くにある場合と、大きい物体が遠くにある場合を見分けにくく、距離の尺度には曖昧さがあります。ロボットの周辺理解や3D再構成につながりますが、この色付きの図をそのまま距離計の目盛りとしては読めません。'))
    out+=sec('pose','姿勢推定：関節の位置から体の形を表す',p('姿勢推定（pose estimation）は、肩・肘・手首・腰・膝などの特徴点の座標を求めます。人物を一つの枠で囲う検出から一歩進んで、体の各部分がどの位置にあるかを表します。点をつないだ線は、関節の対応を見やすくしたものです。')+pose_data()+p('左の人物は腕を上げて脚を前後に開き、右の人物は両手を床についてしゃがんでいます。姿勢が変わっても、肩・肘・手首、股関節・膝・足首を同じ対応関係で結んでいます。出力はポーズの名前ではなく、それぞれの点の位置です。BlazePoseは顔・手・足を含む33個の特徴点を扱います。')+p('スポーツなら、肩・肘・手首の座標から肘の曲がりを調べたり、連続したフレームで手首の軌跡を見たりできます。2D姿勢は画像上の位置、3D姿勢は奥行きも含む位置です。カメラに対して体が斜めを向くと、画像上の角度と実際の関節角度は変わります。隠れた関節や左右の取り違え、動画での点の揺れも結果の読み取りに関わります。'))
    out+=sec('research-links','具体的な研究で、出力を見てみる',cards([
        ('SEGMENTATION','SAM 2','点で選んだ領域を動画で追い、途中の追加指定で修正する。既存の研究紹介へ。','research.html#sam2'),
        ('DEPTH','Depth Anything V2','細い構造や複雑な場面の奥行き。既存の研究紹介へ。','research.html#depth-v2'),
        ('POSE','MediaPipe Pose','関節の座標を動作の記録へつなぐ。公式の出力例を読む。','research.html#mediapipe')]))
    out+=refs([('Oxford-IIIT Pet データセット','https://www.robots.ox.ac.uk/~vgg/data/pets/'),('BlazePose 原論文：Figure 6','https://arxiv.org/html/2006.10204v1#S4.F6'),('Panoptic Segmentation：3種類の出力定義','https://arxiv.org/abs/1801.00868'),('SAM 2 原論文','https://arxiv.org/html/2408.00714v2'),('Depth Anything V2 原論文','https://arxiv.org/html/2406.09414v2')])
    return out
