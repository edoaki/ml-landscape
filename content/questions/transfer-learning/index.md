---
id: transfer-learning
title: 転移と適応
summary: 工場の製品検査を例に、転移・少数例・メタ学習・マルチタスク・環境への適応を、使える情報と更新対象から区別します。
url: questions/transfer-learning.html
status: ready
scope: 得た知識を別の課題・環境にどう使うか。転移、少数例、メタ学習、マルチタスク、ドメイン適応、テスト時適応
prerequisites: []
related: []
origins:
- learning.html#transfer
- learning.html#few-shot
- learning.html#meta-learning
- learning.html#multitask
scripts: []
styles:
- content/questions/transfer-learning/components/page.css
english_title: Transfer Learning and Adaptation
---

## 転移学習の目的 {#transfer-example}

写真を大量に学んだモデルを使い、工場Aの製品写真を「傷あり／なし」に分類したいとします。最初から学ぶ代わりに、既に学んだ形や模様の特徴を使うのが**転移学習**です。使える正解の量や、元の環境と何が違うかによって、調整の方法を変えます。

ここでは「写真から傷の有無を出す」を共通の目的にします。モデルの内部で学習により変わる数値を重み、工場やカメラなどデータの生まれる環境をドメインと呼びます。

<section id="transfer" markdown="1">

## 転移学習・微調整

<figure class="learning-figure" markdown="1">

{{component:visual-001}}

<figcaption markdown="1">

固定する部分と更新する部分を比較する。微調整は特徴を取り出す部分の一部だけを更新する場合もある（模式図）。
</figcaption>
</figure>

特徴を取り出す部分を固定して、傷を分類する最後の部分だけ学ぶ方法と、元の重みも一部または全体を更新する**微調整（ファインチューニング）**があります。更新する量を増やすと用途に合わせやすくなる一方、正解が数枚しかなければ、その背景に合わせすぎることもあります。

</section>

<section id="few-shot" markdown="1">

## 少数例学習（few-shot）

新しい種類や課題について、少数のお手本だけで対応することを目指します。

<figure class="learning-figure" markdown="1">

{{component:visual-002}}

<figcaption markdown="1">

製品検査を、傷あり・なし各2枚のお手本で行う例。傷の線は説明のため強調している（模式図）。
</figcaption>
</figure>

少ない例だけでゼロから学ぶのではなく、事前学習した知識などを使うことが多いです。LLMでは、お手本を文脈に入れるだけで、重みを更新しない使い方もfew-shotと呼びます。

</section>

<section id="meta-learning" markdown="1">

## メタ学習

いろいろな課題を経験し、新しい課題へ少ない練習で適応する仕方を学びます。

<figure class="learning-figure" markdown="1">

{{component:visual-003}}

<figcaption markdown="1">

MAML型のメタ学習。課題内での更新と、その結果を使う初期重みの改善を分けて示す（模式図）。
</figcaption>
</figure>

図は、適応しやすい初期の重みを学ぶ方法の例です。検査のお手本で更新した後、別の例でも当たるように元の初期値を改善します。[MAMLの研究例](source:exp-maml) few-shotが「例が少ないという条件」なのに対し、メタ学習はその条件に対応するためにも使える方法です。

</section>

<section id="multitask" markdown="1">

## マルチタスク学習

一つのモデルで複数の課題を一緒に学び、役立つ特徴を共有します。

<figure class="learning-figure" markdown="1">

{{component:visual-004}}

<figcaption markdown="1">

傷の有無と位置の両方を学び、特徴を取り出す部分を共有する（模式図）。
</figcaption>
</figure>

例えば「傷があるか」と「傷がどこにあるか」を同時に学びます。課題同士が助け合う場合もあれば、一方の学習が他方を妨げる場合もあります。

</section>

<span id="transfer-settings"></span>

## ドメイン適応とテスト時適応 {#adaptation-information}

<figure class="learning-figure" markdown="1">

{{component:visual-005}}

<figcaption>同じ傷の検査でも、移行先の写真を使える時点が異なる（模式図）。</figcaption>
</figure>

工場Bは照明が暗く、傷の見え方がAと違うとします。Bのラベルがなくても写真は使えるなら、特徴の分布を近づけたり、予測の一貫性を使ったりする**教師なしドメイン適応**が考えられます。ただし、Bでは欠陥品が多いなど、見え方以外も変わっていると単純に分布を合わせるだけではうまくいかない場合があります。

テスト時適応は、利用中のデータで更新するので、先に見た入力によって後の予測も変わり得ます。順序や更新する部品、工場を切り替えたときに重みを戻すかを記録します。Bのデータを事前にも利用時の更新にも使わず、未知のBへそのまま使うことを目指す設定は**ドメイン汎化**です。

研究では、適応して新環境がよくなる一方、元の環境で性能が落ちないかを確認します。検査のために隠した正解を調整に使うと、実際には利用できない情報で成績を上げることになるため、モデル選択用と最終評価用を分けます。
