---
id: normalizing-flow
title: Normalizing Flow
summary: 生成したものを逆にたどれる。変換の伸縮を計算できる。この二つを使って、複雑なデータの密度を学びます。
url: models/normalizing-flow.html
status: migrated
scope: ページ。可逆変換と密度・生成
prerequisites:
- generative-overview
related: []
origins:
- normalizing-flow.html#why
- normalizing-flow.html#invertible
- normalizing-flow.html#density
- normalizing-flow.html#coupling
- normalizing-flow.html#train-use
- normalizing-flow.html#sources
scripts: []
styles: []
english_title: Normalizing Flows
---

<section id="why" markdown="1">

## Normalizing Flowの基本

新しいデータを生成するだけでなく、観測したデータがモデルの分布でどれくらい高い密度を持つかも計算したい場面があります。GANは通常その密度を直接は返さず、VAEは扱うモデルの尤度を近似的な目的で学びます。そこで、密度が分かる単純な分布を、逆に戻せて伸縮率も計算できる変換で複雑にします。Normalizing Flowは、生成と密度計算を両立させるために、ネットワークの変換へ条件を課す方法です。

</section>

<section id="invertible" markdown="1">

## 可逆変換と分布

Normalizing Flowは、単純な分布の変数zを、可逆な変換gでデータxへ移します。逆関数f=g⁻¹があるので、観測xをzへ戻して確率密度も計算できます。ここでは有限個の可逆層を重ねる離散的なFlowを中心に説明します。

<figure markdown="1">

{{component:visual-001}}

<figcaption markdown="1">

2次元の分布を実際に上記の演算で変換した図。濃い部分ほど確率密度が高く、線は等密度線。全パネルは同じ座標尺度。赤点は同じサンプルの移動です。②→③ではaを保ったままbを変えるため、曲げても逆に戻せます。係数は説明用の固定値で、学習結果ではありません。
</figcaption>
</figure>

Flowの中心は、元に戻せる演算を何段も重ねることです。掛け算には割り算、足し算には引き算を対応させ、逆向きでは最後の演算から取り消します。途中で値を捨てたり、異なる入力を同じ出力へ潰したりすると、一意に戻せなくなります。AEのように次元を小さくするのではなく、通常は同じ次元のまま分布の形を変えます。

上の例のような一様な拡大だけでは、正規分布の形を十分に複雑にはできません。そこで、残した座標に応じて別の座標を非線形に変えたり、座標の役割を交換したりします。実際のモデルでは変形量をニューラルネットワークで計算し、その重みを学習します。

</section>

<section id="density" markdown="1">

## 変数変換と確率密度

<figure markdown="1">

{{component:visual-002}}

<figcaption markdown="1">

横軸は値、縦方向は確率密度。左右は同じ尺度で描画しています。平行移動では高さは変わらず、拡大した分だけ密度を下げる必要があります。
</figcaption>
</figure>

$$
\log p_X(x) = \log p_Z(f(x)) + \log\lvert\det J_f(x)\rvert
$$

Jfは逆変換fが各方向をどれだけ伸縮させるかを表す微分の行列（ヤコビアン）。detは行列式で、体積の倍率を表す。対数を取ると複数層の倍率の積が和になる。

1次元でx=2z+3ならf(x)=(x−3)/2、微分は1/2なのでpX(x)=pZ((x−3)/2)/2。横幅が2倍になる分、密度の高さは半分です。点が多い場所の「確率密度」と、その一点が出る確率は同じではありません。連続値の確率は区間で積分します。

</section>

<section id="coupling" markdown="1">

## Coupling層の可逆性

$$
\begin{aligned} y_a &= x_a \\ y_b &= x_b\odot\exp(s(x_a)) + t(x_a) \\ x_b &= (y_b-t(y_a))\odot\exp(-s(y_a)) \end{aligned}
$$

入力をaとbへ分け、aはそのまま渡す。aから計算した倍率と移動量でbを変換する。逆変換では残っているaから同じsとtを計算できる。s・t自体のネットワークは可逆でなくてもよい。

<figure markdown="1">

{{component:visual-003}}

<figcaption markdown="1">

例ではexp(s(1)) = 2、t(1) = 3。NN自体を逆向きに解く必要はありません。残したaから同じ倍率と移動量を再計算し、bに施した演算だけを逆にします。次の層では成分の役割を交換し、両方を変換します。
</figcaption>
</figure>

xₐ=1、xᵦ=2、s(1)=log 2、t(1)=3ならyₐ=1、yᵦ=7。逆は(7−3)/2=2。この層のヤコビアンは三角形になるので、log|det J|はsの成分の和で計算できます。単に可逆なだけでなく、この計算を容易にする設計が重要です。

</section>

<section id="train-use" markdown="1">

## 学習と利用

学習ではデータxを逆変換し、負の対数尤度−log pX(x)を小さくします。生成では基底分布からzを引いてgを通します。分類器と組み合わせてzを変え、別の予測になる画像を探す反実仮想説明にもつながります。

可逆性や密度計算のしやすさは構造の制約になります。厳密な密度を計算できても、未知の異常を必ず低密度と判定できるとは限りません。また画像の離散画素を連続密度で扱う場合はdequantizationなどの扱いも必要です。

<aside class="note" markdown="1">

**Flow Matchingとの関係**

連続時間の可逆な流れを使うContinuous Normalizing Flowもある。Flow Matchingはその速度場を学ぶ目的の一つであり、名前が似た無関係な方法でも、すべて同じ学習方法でもない。

</aside>

</section>

<section id="sources" markdown="1">

## 出典・参考資料

* [Real NVP：Affine couplingと密度推定 ↗](source:ref-001)
* [Normalizing Flows for Probabilistic Modeling and Inference ↗](source:ref-002)

</section>
