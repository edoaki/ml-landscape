---
id: vit
title: ViT
summary: Vision Transformer（ViT）は、画像を小領域の列に分け、その領域どうしの関係から表現を更新するモデルです。画像分類を例に、パッチの入力とCLSからの出力を追います。
url: models/vit.html
status: migrated
scope: 独立ページ。画像パッチと処理、パッチの大きさと計算量、データ量と前提、解像度の変更、ViTを使うモデルを説明。目次の親子関係は先行読書を要求しない
prerequisites:
- transformer
- cnn
related:
- transformer
- vlm
origins:
- vit.html#bridge
- vit.html#patches
- vit.html#cls
- vit.html#sources
scripts: []
styles:
- content/models/vit/components/page.css
english_title: Vision Transformer
---

<section id="bridge" markdown="1">

## 画像へのTransformerの適用

Transformerは、要素間の関係をもとに各要素の表現を書き換えます。要素を単語から**画像の小領域**に変えると、同じ仕組みを画像に使えます。さらに画像と文章の表現をつなぐと、画像を見て質問に答えるモデルへ進めます。

</section>

<section id="patches" markdown="1">

## ViTのパッチ埋め込み

**ViT（Vision Transformer）**は、画像を小さな領域（パッチ）に分け、Transformerで処理するモデルです。言語で使われていたTransformerを、画像認識にも適用できるかという発想から提案されました。

<figure markdown="1">

{{component:visual-001}}

<figcaption markdown="1">

値や分割数などは説明用のものです。
</figcaption>
</figure>

各パッチの画素値を一列に並べ、学習する線形層で同じ長さのベクトルに変換します。さらに**位置埋め込み**を足し、画像内の位置を区別できるようにします。

例えば224×224画素の画像を16×16画素ずつに分けると、14×14＝196パッチです。一画素ずつ渡すより系列を短くできます。CNNのような局所性の前提が少なく、原論文では大規模データでの事前学習が性能を引き出す鍵になりました。

</section>

<section id="patch-size" markdown="1">

## パッチの大きさと計算量

パッチ埋め込みは、「16×16のフィルタを16画素ずつずらす畳み込み」を一回かけるのと同じ計算です。RGB画像なら一つのパッチは16×16×3＝768個の数値で、ViT-Baseではこれを768次元のベクトルへ変換します（入力と出力の次元が同じなのは、この大きさの組み合わせでの偶然です）。モデル名の**ViT-B/16**は、Baseの大きさでパッチが16×16であることを表します。

パッチを小さくすると細部を捉えやすくなりますが、系列が長くなります。Self-Attentionは全ての位置の組を比べるため、比べる組の数は系列の長さの2乗で増えます。

<div class="table-scroll" tabindex="0" markdown="1">

| 224×224画像のパッチ | パッチ数（CLSを除く） | Attentionで比べる組の数 |
| --- | --- | --- |
| 32×32 | 7×7＝49 | 49²＝2,401 |
| 16×16 | 14×14＝196 | 196²＝38,416 |
| 8×8 | 28×28＝784 | 784²＝614,656 |

</div>

パッチの一辺を半分にすると、パッチ数は4倍、比べる組は16倍になります。細かく分けるほど計算とメモリが急に増えるため、パッチの大きさは精度と計算量の釣り合いで選びます。

</section>

<section id="cls" markdown="1">

## CLSトークンと画像分類

分類用に、学習可能な**CLS（クラストークン）**を一つ加えます。これは画像の一部分ではなく、分類に使う表現を作るための特別な位置です。196パッチなら、CLSと合わせて197個のベクトルを入力します。

<figure markdown="1">

{{component:visual-002}}

<figcaption markdown="1">

値などは説明用のものです。
</figcaption>
</figure>

Self-Attentionで各パッチとCLSが互いを参照し、FFNで各位置の特徴を加工します。この処理をN層繰り返すと、CLSにも画像全体の情報が取り込まれます。最後のCLSの表現を分類ヘッドへ渡し、softmaxでクラスごとの確率を求めます。

GPT型の文章生成では**最後のトークンの表現**から次のトークンを予測します。ここでは**最後の層のCLSの表現**から画像のクラスを予測します。図は全結合層で分類する例です。ViT原論文では事前学習時に隠れ層を持つMLPヘッドを使い、微調整時には線形層を使います。

原論文は、層の数と表現の次元を変えた三つの大きさを比べました。

<div class="table-scroll" tabindex="0" markdown="1">

| モデル | 層の数 | 表現の次元 | Attentionのhead数 | パラメータ数 |
| --- | --- | --- | --- | --- |
| ViT-Base | 12 | 768 | 12 | 約8,600万 |
| ViT-Large | 24 | 1,024 | 16 | 約3億700万 |
| ViT-Huge | 32 | 1,280 | 16 | 約6億3,200万 |

</div>

</section>

<section id="data" markdown="1">

## データの量と、構造に組み込む前提

CNNは、近くの画素をまとめて見る（局所性）、同じフィルタを位置をずらして使う（重み共有）という前提を構造に組み込んでいます。ViTでは、パッチ内の変換を除くとこの前提が弱く、パッチどうしの位置関係も位置埋め込みを通してデータから学びます。

原論文では、ImageNet（約130万枚）だけで事前学習したViTは、同程度の大きさのResNetより数ポイント低い精度にとどまりました。一方、ImageNet-21k（約1,400万枚）やJFT-300M（約3億枚）で事前学習すると差が縮まり、JFT-300MではResNetを上回りました。前提が少ない分、多くのデータから学ぶ必要がある、という読み方ができます。

その後DeiTは、ImageNetだけでも、強いデータ拡張と正則化、CNNを教師にした蒸留を組み合わせればViTを十分に学習できることを示しました。データの量の問題は、構造だけでなく学習の工夫でも補えます。[DeiT ↗](source:ref-004)

</section>

<section id="resolution" markdown="1">

## 解像度を変えるときの位置埋め込み

微調整では、事前学習より高い解像度（例えば384×384）を使うことがあります。パッチを16×16のまま変えなければ、パッチ数は14×14＝196から24×24＝576に増えます。学習した位置埋め込みは196位置分しかないため、原論文では位置埋め込みを14×14の格子として2次元で補間し、24×24の格子に広げて使いました。

</section>

<section id="after" markdown="1">

## ViTを部品として使うモデル

ViTは、画像の表現を作る部品として広く使われます。自己教師あり学習のDINOは、ラベルなしの画像からViTの表現を学びます（[表現学習](page:representation-learning)）。[CLIP](page:clip)は画像側のエンコーダにViTを使えます。[VLM](page:vlm)では、ViTが作ったパッチの表現を言語モデルへ渡します。

長い系列の計算量を抑える工夫もあります。Swin Transformerは、近くの小さな窓の中だけでAttentionを計算し、層を進むごとに隣り合うパッチをまとめて解像度を下げます。CNNに近い階層構造を持たせ、物体検出など高解像度の課題にも使いやすくしました。[Swin Transformer ↗](source:ref-005)

</section>

<section id="sources" markdown="1">

## 出典・参考資料

* [ViT：An Image is Worth 16x16 Words（2020） ↗](source:ref-001)
* [LLaVA：Visual Instruction Tuning（2023） ↗](source:ref-002)
* [CLIP：Learning Transferable Visual Models From Natural Language Supervision（2021） ↗](source:ref-003)
* [DeiT：Training data-efficient image transformers & distillation through attention（2021） ↗](source:ref-004)
* [Swin Transformer：Hierarchical Vision Transformer using Shifted Windows（2021） ↗](source:ref-005)

</section>
