---
id: vit
title: ViT
summary: Vision Transformer（ViT）は、画像を小領域の列に分け、その領域どうしの関係から表現を更新するモデルです。画像分類を例に、パッチの入力とCLSからの出力を追います。
url: models/vit.html
status: migrated
scope: 独立ページ。画像パッチと処理を説明。目次の親子関係は先行読書を要求しない
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

</section>

<section id="sources" markdown="1">

## 出典・参考資料

* [ViT：An Image is Worth 16x16 Words（2020） ↗](source:ref-001)
* [LLaVA：Visual Instruction Tuning（2023） ↗](source:ref-002)
* [CLIP：Learning Transferable Visual Models From Natural Language Supervision（2021） ↗](source:ref-003)

</section>
