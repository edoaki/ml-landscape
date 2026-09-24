---
id: science
title: 物理・シミュレーション（Scientific ML）
summary: 熱の伝わり方を例に、数値計算の代わりとなる代理モデル、PINNs、ニューラルオペレーターを説明します。順問題と逆問題、観測と物理法則の役割を区別します。
url: fields/science.html
status: ready
scope: 物理法則の組み込み、逆問題、PINNs、代理モデル、ニューラルオペレーター
prerequisites:
- learning
related:
- life-science
- earth-science
origins:
- science.html#science
- science.html#simulation
- science.html#inverse
scripts:
- content/fields/science/components/science.js
styles:
- content/fields/science/components/page.css
english_title: Physics, Simulation and Scientific Machine Learning
---

## 物理の順問題と逆問題 {#scientific-ml-intro}

金属の棒の左端を温めたとき、数秒後にどこが何度になるかを知りたいとします。**順問題**は、材料や温め方などの条件から結果を求める問題です。逆に、測った温度から材料の熱の伝わりやすさを推定するのが**逆問題**です。

Scientific MLでは、観測データだけでなく、既知の物理法則や数値シミュレーションも学習に使います。計算を速くする、少ない観測から未知の量を推定する、といった目的があります。

<section id="science" markdown="1">

## 数値計算の代わりを学ぶ

材料や加熱の仕方を何通りも試すと、条件ごとに数値シミュレーションを繰り返す費用がかかります。そこで、**条件と計算結果の組からニューラルネットワーク（NN）を学習し、新しい条件の結果を予測する**のが、**代理モデル**の使い方です。

学習データを作る計算と学習自体には費用がかかりますが、学習後の予測を繰り返すことで速さが役立ちます。以下では、物理法則を学習に使うPINNと、条件の分布から解の分布を求めるニューラルオペレーターを見ます。

</section>

## PINNsと物理法則 {#pinn-example}

棒の位置と時刻から温度を予測するとします。通常の教師あり学習では、予測を正解の温度と比べて学びます。**PINN**では、それに加えて、予測が**熱の伝わり方を表す物理法則にも合うように**学びます。

学習で小さくしたい誤差を**損失**と呼びます。観測した温度との誤差だけでなく、予測が物理法則から外れた分も損失に加えるのが工夫です。棒の内部で温度を測っていない場所でも、法則とのずれは調べられます。ただし、加熱を始めた時点や棒の両端の条件などは必要です。

### 熱方程式から損失を計算する

{{component:pinn-mechanism}}

図の方程式は熱の伝わり方を表します。材料係数 α は既知、θ はNNの重み・バイアスです。予測温度を位置・時刻で微分すると、方程式とのずれが求まります。[原論文](source:exp-pinn)

## ニューラルオペレーター {#operator-example}

**ニューラルオペレーター**は、温度や流れの分布など、**関数を入力して関数を返す対応**を学ぶモデルです。棒なら、様々な初期温度の分布から、10秒後の温度分布を求める規則を学びます。

{{component:operator-overview}}

図では、材料と両端の0℃を固定し、初期温度の分布だけを変えています。一本の棒について温度を一つ答えるのではなく、**初めの温度の広がり方から、後の広がり方を予測する**のが目標です。多様な初期条件と、その結果の組を学んで、この対応を身につけます。

### 各位置の情報を混ぜて分布を予測するモデル

実装では分布を格子点の値などで表しますが、固定長の全結合NNと違い、格子の取り方が変わっても同じ対応を近似できるように設計します。これは精度が自動的に保たれるという意味ではありません。[原論文](source:exp-operator)

#### モデルの例

下図は、各位置の温度を、NNが作る重みで混ぜ合わせる構成例です。フーリエ変換を使うFNOなど、別のモデルもあります。[FNOの原論文](source:exp-fno)

{{component:operator-mechanism}}

<section id="simulation" markdown="1">

## 流体シミュレーションの近似

<div class="science-io" markdown="1">

<div markdown="1">

入力**水の初めの位置と動き  
＋ 容器の形**
</div>

<div class="science-arrow" markdown="1">

例：GNS**→**
</div>

<div markdown="1">

出力**その後、水がどう動くか**
</div>

</div>

<figure class="science-video" markdown="1">

{{component:visual-001}}

<figcaption markdown="1">

[Sanchez-Gonzalez et al. (2020) 著者公開動画：Water-3D](source:ref-001)。左＝基準となるシミュレーション、右＝AIの予測。水が崩れ、広がっていく様子を比べます。
</figcaption>
</figure>

水や砂の動きを、毎回細かく計算する代わりにAIで予測します。形や条件を変えて、たくさんのパターンを試す研究に役立ちます。

</section>

<section id="inverse" markdown="1">

## 地下構造の推定

地面に振動を与え、地表のセンサーで戻ってきた波を測ります。**その記録から、直接見えない地下の層を推定する**のが、物理の逆問題の一例です。

<div class="science-io" markdown="1">

<div markdown="1">

入力**地表で測った  
揺れの記録**
</div>

<div class="science-arrow" markdown="1">

例：InversionNet**→**
</div>

<div markdown="1">

出力**地下で波が進む速さの分布  
→ 地層を知る手がかり**
</div>

</div>

{{component:visual-002}}

地下の構造が分かれば、地表の揺れを計算できます。その向きを逆にして、揺れから地下を調べるので「逆問題」です。AIでこの推定を行う研究があり、地盤や地下資源を調べる手がかりになります。 [研究例：OpenFWI / InversionNet](source:ref-002)

</section>

## 逆問題の不確実性と評価 {#scientific-validation}

温度計が一点しかなければ、違う材料や加熱条件でも似た観測になることがあります。逆問題で一つの答えを得ても、それが唯一とは限りません。観測点を増やす、既知の条件で候補を絞る、といった工夫が必要です。

研究では、温度の誤差、物理条件との整合性、未学習の初期条件での精度を測ります。速さは訓練データを作る計算・モデルの学習・学習後の予測を分けて比較します。一度しか解かない問題と、多数の条件を繰り返し解く問題では、代理モデルを作る費用の意味が変わります。
