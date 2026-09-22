---
id: gan
title: GAN
summary: 本物と見分けるモデルを、生成するモデルの学習信号に使う。更新する重みと、勾配が通る経路を分けて見ます。
url: models/gan.html
status: migrated
scope: ページ。生成器・識別器と学習
prerequisites: []
related: []
origins:
- gan.html#why
- gan.html#two-networks
- gan.html#loss
- gan.html#use
- gan.html#limits
- gan.html#sources
scripts: []
styles: []
english_title: Generative Adversarial Networks
---

<section id="why" markdown="1">

## GANの基本

複雑な画像の分布を学ぶとき、各画像の確率を計算したり、見えない潜在変数を推定したりする処理が難しくなることがあります。そこで「本物のデータと見分けがつかないものを作れれば、その分布を学べるのではないか」と考えます。GANは、本物と生成物を区別する識別器を学習し、その判定を生成器の学習信号にしました。生成器の厳密な確率密度を直接計算せずに、データを作る能力を学ぶための設計です。

</section>

<section id="two-networks" markdown="1">

## 生成器と識別器

GAN（generative adversarial network）は生成器Gと識別器Dを組み合わせます。Gはノイズからデータを作り、Dは実データと生成データを見分けます。GはDを通して「どこを変えると本物と判定されやすいか」という勾配を受け取ります。

<figure markdown="1">

{{component:visual-001}}

<figcaption markdown="1">

ネットワークの形は固定ではない。画像ならCNN、条件付き生成ならクラスや元画像も入力する。
</figcaption>
</figure>

</section>

<section id="loss" markdown="1">

## 生成器・識別器の学習

$$
\begin{aligned} L_D &= -\mathbb E_x[\log D(x)] \\ &\quad -\mathbb E_z[\log(1-D(G(z)))] \\ L_G &= -\mathbb E_z[\log D(G(z))] \end{aligned}
$$

Dは本物を1、生成を0と判定するよう学ぶ。Gは生成物をDが1と判定するよう学ぶ。Gには広く使うnon-saturating損失を表示しており、原論文のminimax式そのものとは区別する。

<div class="table-scroll" tabindex="0" markdown="1">

| 段階 | 固定する重み | 更新する重み・必要な計算 |
| --- | --- | --- |
| Dを学習 | G | 本物と、Gから切り離した生成物でDの損失を下げる |
| Gを学習 | D | Dを通った入力への勾配は計算し、それをGへ戻す |
| 画像を生成 | Gも更新しない | z→G(z)だけ。Dは使わない |

</div>

D(G(z))が0.2ならGの損失−log(0.2)≈1.61、0.8なら≈0.22。Gはこの損失を下げる方向へ変わります。Dも変化するため、固定した一つの損失面を下る状況とは異なります。

</section>

<section id="use" markdown="1">

## 画像生成と画像変換

<figure markdown="1">

{{component:visual-002}}

<figcaption markdown="1">

通常のGANの生成経路。入力条件を与えるconditional GANは、画像変換などへ利用できる。
</figcaption>
</figure>

画像変換では元画像と目標側の画像を用い、見た目やドメインを変えます。超解像では細部をもっともらしく補うことがありますが、生成した細部が元の場面に本当にあったとは限りません。自然さと内容の正確さは別々に評価します。

</section>

<section id="limits" markdown="1">

## 生成品質と多様性

生成器が少数の似た画像ばかり出しても、その一枚は自然に見えるかもしれません。これがmode collapse（生成の多様性の崩壊）の問題です。またDが強すぎるなどの理由でGが有効な勾配を得にくい場合があります。損失の値だけで画質・多様性を判断せず、複数の評価を使います。

GANは通常、各画像の厳密な尤度を直接は計算しません。次のNormalizing Flowは可逆性を制約として、密度を計算できる方向から生成を考えます。DiffusionやFlow Matchingは反復的な生成過程を学ぶ別の方向です。

</section>

<section id="sources" markdown="1">

## 出典・参考資料

* [Generative Adversarial Networks（2014） ↗](source:ref-001)
* [pix2pix：Image-to-Image Translation（2016） ↗](source:ref-002)

</section>
