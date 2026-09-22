---
id: combinatorial-optimization
title: 組合せ最適化
summary: 経路・仕事の割り当て・スケジューリングを例に、制約と目的を区別します。探索と学習の役割、解の品質と計算時間の評価も扱います。
url: fields/combinatorial-optimization.html
status: ready
scope: 経路、割り当て、スケジューリング
prerequisites: []
related: []
origins:
- decision-science.html#problem
- research.html#design-control / 配送経路｜都市の集合から訪問順序へ
scripts: []
styles:
- content/fields/combinatorial-optimization/components/page.css
english_title: Combinatorial Optimization
---

## 制約と目的関数 {#discrete-choice}

3件の配達をどの順で回るか、2人にどの仕事を割り当てるか、機械でどの作業を先に行うか。**組合せ最適化**は、このような離散的な選択を組み合わせ、条件を守る候補の中から目的に合うものを探す問題です。

「守らなければならない条件」が**制約**、「小さくしたい距離や時間」が**目的関数**です。例えば「全配達先を一回ずつ訪問」は制約、「移動距離の合計を最小化」は目的です。短くても1件を訪れ忘れた経路は、よい解の候補に入りません。

<section id="problem" markdown="1">

## 組合せ最適化の例

まず、何を選び、どの条件を守る問題なのかを比べます。

<div class="optimization-part" id="tsp" markdown="1">

### 巡回セールスマン問題（TSP）

<figure class="task-example" markdown="1">

{{component:visual-001}}

<figcaption markdown="1">

同じ10都市を一度ずつ訪れ、出発点へ戻る。距離は直線距離の合計（任意単位）。教材例で、最短性は保証しない。
</figcaption>
</figure>

</div>

### 仕事の割り当て {#assignment-example}

担当者A・Bに、仕事X・Yを一つずつ割り当てます。次は所要時間の架空の表です。同時に作業を始められ、中断や引き継ぎはないとします。

| 担当者 | 仕事X | 仕事Y |
| --- | --- | --- |
| A | 2時間 | 4時間 |
| B | 3時間 | 8時間 |

AにX、BにYなら作業時間の合計は10時間、両方が終わるまで8時間です。AにY、BにXなら合計7時間、終わるまで4時間です。この例では後者がどちらの目的でもよいですが、合計時間と全体の完了時刻は異なる指標です。仕事の重複や未割り当てを許さないという制約も確認します。

スケジューリングでは、さらに開始時刻や順序を選びます。「A1が終わってからA2」「同じ機械で二つの作業を同時にしない」など、満たす条件が増えます。次の工程図と合わせ、棒が短いだけでなく、前後関係を守っているかを見てください。

<div class="optimization-part" id="scheduling" markdown="1">

### スケジューリング

青の仕事Aは A1 → A2、橙の仕事Bは B1 → B2 の順。同じ機械で作業が重ならないように予定を組みます。

<figure class="task-example" markdown="1">

{{component:visual-003}}

<figcaption markdown="1">

行は機械、横軸は時刻（分）、棒の幅は処理時間。A1＝3分、他は2分。時刻0から開始可能、中断・段取り替え・運搬時間は省略。
</figcaption>
</figure>

機械が空いていても、前の工程が終わるまで始められない仕事があります。順序と開始時刻を一緒に考える必要があります。

</div>

</section>

## 厳密解法・ヒューリスティクス・学習 {#solvers-and-learning}

配達先が増えると、訪問順の候補は急速に増えます。**厳密解法**は、探索や数学的な条件を使い、最適性の証明を目指します。**ヒューリスティクス**は、例えば近い未訪問先へ進むなど、短い時間でよい候補を探す工夫です。速く候補を出せても、最適とは限りません。

機械学習は、よさそうな次の配達先を予測したり、既存の解法で調べる候補の順番を提案したりできます。利用時に一から探索する費用を減らす狙いがありますが、訓練時より大きい都市数でも使えるかは別に確認します。正解の経路で学ぶ方法も、距離を報酬にして学ぶ方法もあり、強化学習だけに限定されません。

**学習の最適化**はモデルの重みを更新する問題、ここでの最適化は配送順や割り当てを選ぶ問題です。学習したモデルを使って組合せ最適化を解く場合、両方が登場します。

比較では、制約を満たした割合、解の距離・時間、解を得るまでの計算時間をそろえて測ります。最適値が分かる小さな問題なら、最適値からどれだけ離れたかも計算できます。最適値が分からない場合は、既知のよい解との差を、最適性の証明と取り違えないようにします。

<div class="optimization-part" id="learn-routing" markdown="1">

## 学習による経路の生成

<figure class="route-generation" markdown="1">

{{component:visual-002}}

<figcaption markdown="1">

都市の位置・現在地・訪問済みの情報を入力し、未訪問の都市を一つ選ぶ。これを繰り返し、最後に出発点へ戻る。
</figcaption>
</figure>

**生成：**次の都市を選ぶ操作を繰り返すと、経路ができます。  
**学習：**総距離 L に対して報酬を −L とし、短い経路を作れる選択ルールを強化学習で学びます。

[Koolら（ICLR 2019）](source:ref-001)は、Attentionを使うモデルに、短い経路ほど高い報酬を与えて選択ルールを学習させます。REINFORCEはその更新に使う強化学習の方法です。図はその考え方を簡略化したものです。

</div>

<section id="research-12" markdown="1">

### 原論文の配送経路の図

<figure markdown="1">
[![4段階で都市3、1、2、4を選ぶTSPのデコーダ](media:kool2019-tsp-decoder.png)](media:kool2019-tsp-decoder.png)
<figcaption markdown="1">

Koolら（ICLR 2019）の[Figure 2, p.4](source:ref-003)を引用。図領域を切り出し。選択手順の説明図。[画像を拡大 ↗](media:kool2019-tsp-decoder.png)
</figcaption>
</figure>

図では、訪問済みの都市を除きながら次の都市を選ぶ流れを見ます。都市数が変わった場合にも使えるか、解の品質と計算時間がどう変わるかが研究の問いです。

[著者実装と原論文 ↗](source:ref-004)

</section>

工程を一つずつ割り付け、全作業が早く終わるほど高い報酬を与える研究もあります。[スケジューリングの研究例：Zhangら（2020）](source:ref-002)。
