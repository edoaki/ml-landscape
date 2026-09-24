---
id: gan
title: GAN
summary: 本物と見分けるモデルを、生成するモデルの学習信号に使う。更新する重みと、勾配が通る経路を分けて見ます。
url: models/gan.html
status: migrated
scope: ページ。生成器・識別器と学習、non-saturating損失、最適な識別器、評価と安定化
prerequisites:
- generative-overview
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

### non-saturating損失を使う理由 {#non-saturating}

Dの出力を、sigmoid関数σを使ってD＝σ(a)と書きます（aはsigmoidに入る前の値）。原論文のminimax式でGが下げる項log(1−D)をaで微分すると、その大きさはDです。non-saturating損失−log Dでは1−Dです。

学習の初期にDが生成物をすぐ見抜き、D(G(z))＝0.01になったとします。minimax式の勾配の大きさは0.01、non-saturating損失では0.99です。前者ではGがほとんど学習信号を受け取れません。原論文も、学習初期にはlog D(G(z))を大きくする形でGを学習することを勧めています。

</section>

<section id="optimal-d" markdown="1">

## 最適な識別器と、生成器が近づけるもの

Gを固定すると、各データxで最もよい識別器は次の形になります。p_dataは実データの確率（密度）、p_GはGが作るデータの確率です。

$
D^*(x) = \frac{p_{\mathrm{data}}(x)}{p_{\mathrm{data}}(x) + p_G(x)}
$

例えば、ある種類の画像が実データでは30%、生成物では10%の割合で現れるなら、D*＝0.3÷(0.3＋0.1)＝0.75です。逆に生成物に多すぎる種類では0.5を下回ります。Dの判定は、その種類を増やすか減らすかの手がかりになります。p_Gがp_dataと一致すれば、どのxでもD*＝1/2となり、Dは見分けられません。

原論文は、このD*のもとでminimax式の値が−log 4＋2·JSD(p_data‖p_G)になることを示しました。JSD（Jensen–Shannonダイバージェンス）は二つの分布の違いを測る量で、分布が一致したときだけ0になります。つまり理想的には、Gは実データの分布に一致したときに最もよくなります。ただし実際には、各段階でDを最適まで学習せず、ネットワークの表現力やデータ数にも限りがあるため、この理想どおりには進みません。

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

**FID**（Fréchet Inception Distance）は、学習済みの画像分類モデル（Inception）の特徴空間で、本物と生成物の特徴をそれぞれ正規分布で近似し、平均と共分散の違いを測ります。小さいほど二つの分布が近いことを表します。一つの値に画質と多様性が混ざり、標本の数や画像の前処理でも値が変わるため、同じ条件で比べます。[FID ↗](source:ref-008)

画質と多様性を分けるには、**適合率**（生成物のうち、本物の特徴が集まる範囲に入るものの割合）と**再現率**（本物のうち、生成物の範囲に覆われるものの割合）を使います。mode collapseでは、適合率が高いまま再現率が下がります。[適合率と再現率 ↗](source:ref-009)

### 学習を安定させる工夫 {#stabilizing}

<div class="table-scroll" tabindex="0" markdown="1">

| 課題 | 代表的な工夫 | 考え方 |
| --- | --- | --- |
| 画像での学習が不安定 | [DCGAN（2015）](source:ref-003) | 畳み込みと転置畳み込み、Batch Normalizationなど、学習しやすい構成を整理した |
| 本物と生成物の分布が重ならないと、勾配が乏しい | [WGAN（2017）](source:ref-004)、[WGAN-GP（2017）](source:ref-005) | JSDの代わりにWasserstein距離を近似する。識別器（critic）の傾きを、重みの切り詰めや勾配への罰則で制限する |
| 識別器の出力が急に変わる | [Spectral Normalization（2018）](source:ref-006) | 各層の重みを最大特異値で割り、入力の変化に対する識別器の変化を抑える |
| 高解像度で、生成の性質を制御したい | [StyleGAN（2019）](source:ref-007) | 潜在変数を中間の表現に写し、各解像度の生成に「スタイル」として与える |

</div>

GANは通常、各画像の厳密な尤度を直接は計算しません。次のNormalizing Flowは可逆性を制約として、密度を計算できる方向から生成を考えます。DiffusionやFlow Matchingは反復的な生成過程を学ぶ別の方向です。

</section>

<section id="sources" markdown="1">

## 出典・参考資料

* [Generative Adversarial Networks（2014） ↗](source:ref-001)
* [pix2pix：Image-to-Image Translation（2016） ↗](source:ref-002)
* [DCGAN：Unsupervised Representation Learning with Deep Convolutional GANs（2015） ↗](source:ref-003)
* [Wasserstein GAN（2017） ↗](source:ref-004)
* [WGAN-GP：Improved Training of Wasserstein GANs（2017） ↗](source:ref-005)
* [Spectral Normalization for GANs（2018） ↗](source:ref-006)
* [StyleGAN：A Style-Based Generator Architecture（2019） ↗](source:ref-007)
* [FID：GANs Trained by a Two Time-Scale Update Rule Converge to a Local Nash Equilibrium（2017） ↗](source:ref-008)
* [Improved Precision and Recall Metric for Assessing Generative Models（2019） ↗](source:ref-009)

</section>
