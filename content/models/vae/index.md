---
id: vae
title: VAE
summary: 入力を潜在表現へまとめ、そこから再構成する。VAEは潜在を確率分布として扱い、新しいデータを生成する経路を作ります。
url: models/vae.html
status: migrated
scope: ページ。潜在変数・生成と学習を説明し、比較に必要なAEの構造・計算も残す
prerequisites: []
related: []
origins:
- vae.html#ae
- vae.html#vae
- vae.html#loss
- vae.html#sampling
- vae.html#sources
scripts: []
styles: []
english_title: Variational Autoencoders
---

<section id="ae" markdown="1">

## AEによる再構成

### AEの目的

MNISTの手書き数字は28×28＝784個の画素値です。しかし、線の傾きや丸みなどを捉えれば、もっと少ない数値でも数字の形を表せそうです。AEの出発点は、こうした重要な特徴を、正解ラベルなしでニューラルネットワークに学ばせたいという考えです。人が特徴を一つずつ決めるのは大変で、分類用の正解ラベルがない場合もあります。そこで、入力を小さな表現へ圧縮し、そこから元に戻せるように学習します。「5と答える」のではなく「この画像を描き直す」ことを課題にすれば、入力画像そのものを正解として使えます。細い中央部分を通しても復元できるようにすることで、形を表す情報を残すように促します。これがAEの基本的な発想です。

Autoencoder（AE）は入力をencoderで潜在表現zへ変換し、decoderで元の入力へ戻します。潜在とは直接観測する入力ではなく、モデル内部で作る表現という意味です。再構成できるように学ぶことで、データの特徴を捉えます。

<figure markdown="1">

{{component:visual-001}}

<figcaption markdown="1">

丸はニューロン、線は学習する重み。実際のユニット数は省略。入力はMNIST訓練画像の5（index 0）。出力側も同じ画像を使って復元の目標を示しており、学習済みモデルの実行結果ではありません。
</figcaption>
</figure>

$$
z = f_\varphi(x),\quad \hat x = g_\theta(z),\quad L = \lVert x-\hat x\rVert^2
$$

φはencoder、θはdecoderのパラメータ。例として画素ごとの二乗誤差を足した再構成損失を示す。実際にはデータの性質に応じた損失を使う。

例えば入力[1,0,1]を[0.8,0.1,0.9]へ再構成したなら、二乗誤差の和は0.04+0.01+0.01=0.06です。AEはラベルなしで学べますが、十分大きなネットワークが単純なコピーを覚えるだけでは有用な表現になりません。次元の制約やノイズ除去などの目的を設けます。

</section>

<section id="vae" markdown="1">

## VAEの潜在分布

### VAEの目的

AEは入力を復元する方法を学びますが、それだけでは新しいデータを作るための潜在変数を、どんな分布から選べばよいかが決まりません。一方、潜在変数からデータが生まれる確率モデルを作ると、観測から潜在変数を推定する計算が難しくなります。VAEは、推定を担当するencoderと生成を担当するdecoderを用意し、難しい推定を近似しながら両方を勾配で学べるようにしました。圧縮だけでなく、潜在変数の推定と新しいデータの生成を一緒に扱うための方法です。

例えば手書きの5を復元するだけでなく、いろいろな形の数字を新しく作りたいとします。AEでは、入力を圧縮した点からの復元は練習しますが、適当に選んだ点から何が出るかまでは学習の目的に含まれません。VAEでは入力を一つの点ではなく、平均と広がりを持つ分布へ変換し、そこから選んだ値で復元を練習します。さらに、潜在分布を標準正規分布へ近づける目的を加え、生成時にも値を選べるようにします。

<figure markdown="1">

{{component:visual-002}}

<figcaption markdown="1">

丸はニューロン、線は学習する重み。実際のユニット数は省略。入力はMNIST訓練画像の5（index 0）。出力側も同じ画像を使って復元の目標を示しており、学習済みモデルの実行結果ではありません。中央は潜在変数の1成分の正規分布を模式化。縦の高さは確率密度です。
</figcaption>
</figure>

中央の山は数字のクラス確率ではなく、潜在変数zがどの値を取りやすいかを示す分布です。平均μは山の中心、標準偏差σは広がりを表します。5という正解ラベルは与えず、画像そのものから分布を推定します。

$$
\varepsilon\sim\mathcal N(0,I),\quad z = \mu_\varphi(x) + \sigma_\varphi(x)\odot\varepsilon
$$

N(0,I)は各成分の平均0・分散1の正規分布。例えばμ=2、σ=0.5、ε=−1ならz=1.5。ランダムさをεに分離する再パラメータ化により、μとσへ勾配を流せる。

通常はlog σ²を出力してσを正の値に変換します。潜在次元が2ならμとlog σ²をそれぞれ2個出します。同じxからでもεによって異なるzを得られます。

</section>

<section id="loss" markdown="1">

## 再構成と潜在分布の正則化

$$
\begin{aligned} L &= \mathbb E_{q_\varphi(z\mid x)}[-\log p_\theta(x\mid z)] \\ &\quad + D_{\mathrm{KL}}\!\left(q_\varphi(z\mid x)\,\Vert\,p(z)\right) \end{aligned}
$$

第一項は再構成に対応する負の対数尤度。第二項は潜在分布を事前分布p(z)、通常N(0,I)へ近づける制約。これは負のELBOと呼ばれる目的で、データの尤度を間接的に改善する。

KLダイバージェンスは二つの分布の違いを測る量です。0なら分布が一致し、一般に左右を交換すると値が変わるため通常の距離とは異なります。標準正規分布に対する対角ガウスのKLは、成分ごとのμ²+σ²−1−log σ²を半分にして足せます。

再構成を重視しすぎると潜在の分布が使いにくくなり、制約を強めすぎると入力固有の情報が失われます。decoderが強い場合には潜在を使わなくなるposterior collapseも研究課題です。

</section>

<section id="sampling" markdown="1">

## 潜在変数からの生成

<figure markdown="1">

{{component:visual-003}}

<figcaption markdown="1">

生成時はencoderを通らず、事前分布から潜在を引いてdecoderへ渡す。
</figcaption>
</figure>

再構成したいときは入力→encoder→decoder、新しく生成したいときは事前分布→decoderです。この経路の違いが、単なる圧縮と生成モデルを結びます。

<div class="table-scroll" tabindex="0" markdown="1">

| 用途 | 使う情報 | 注意して読む点 |
| --- | --- | --- |
| 潜在空間の探索 | zを変えたdecoder出力 | 一つの座標が必ず人間の概念に対応するとは限らない |
| 異常検知 | 再構成誤差など | 未知の異常をよく再構成してしまう場合もある |
| 細胞の応答予測 | 細胞の表現と刺激による変化 | 生成・予測した状態は実験検証が必要 |

</div>

</section>

<section id="sources" markdown="1">

## 出典・参考資料

* [Deep Learning 第14章：Autoencoders ↗](source:ref-001)
* [Kingma & Welling, Auto-Encoding Variational Bayes ↗](source:ref-002)
* [scGen：細胞の刺激応答予測 ↗](source:ref-003)

</section>
