---
id: gnn
title: GNN
summary: 同じグラフでGCN・GAT・GraphSAGEを比較。近隣の選び方、重み付け、自己情報の混ぜ方を図と計算で追います。
url: models/gnn.html
status: migrated
scope: ページ。グラフ上の情報の集約・更新
prerequisites:
- fundamentals
related: []
origins:
- gnn.html#basics
- gnn.html#gcn
- gnn.html#gat
- gnn.html#heads
- gnn.html#learning
- gnn.html#sage
- gnn.html#compare
- gnn.html#outputs
- gnn.html#sources
scripts:
- content/models/gnn/components/calculation.js
styles:
- content/models/gnn/components/page.css
english_title: Graph Neural Networks
---

<section id="basics" markdown="1">

## GNNの集約と更新

### GNNの目的

分子の性質は原子の種類だけでなく、どの原子がどの原子と結合しているかで変わります。画像用CNNのような一定の格子を前提にすると、点ごとに隣の数が違うデータをそのまま扱えません。また、原子に付けた番号を変えただけで分子の予測が変わっても困ります。そこで、辺でつながる相手から情報を集め、近隣を並べる順序によらず表現を更新する仕組みを使います。

グラフは点（ノード）と関係（辺）で表すデータです。分子なら原子と結合、文献なら論文と引用に対応します。GNNはグラフを使うニューラルネットワークの総称。ここでは同じ6ノードで、GCN・GAT・GraphSAGEの計算方法を比べます。

<div class="gnn-calc" markdown="1">

### 近隣ノードからの情報集約

自分の特徴だけでは分からない関係の情報を、隣の特徴から取り込みます。
{.gnn-purpose}

<div class="gnn-calc-layout" markdown="1">

<div class="gnn-graph-panel" markdown="1">

<div class="gnn-value-graph" markdown="1">

{{component:visual-001}}

</div>

</div>

<aside class="gnn-working" aria-label="計算過程" markdown="1">

ノード内の2個の数が特徴ベクトルです。線がある相手の特徴を集め、Aの数値を新しい表現へ更新します。

同じ層では、全ノードが一つ前の層の特徴を参照します。更新済みのAをすぐBの同じ層の計算に使うわけではありません。

2層にすると、E → C → A、F → D → Aと、遠くの情報も届きます。以下ではAの1回の更新を拡大します。

</aside>

</div>

</div>

</section>

<section id="gcn" markdown="1">

## GCNの集約係数

### GCNの設計

例えば論文の分野を分類するとき、本文の特徴に加えて引用関係も手がかりにできれば、ラベルが少ない論文集合でも学習を助けられます。ここで扱うKipfとWellingのGCNは、グラフ上の畳み込みを近似し、近隣の特徴を混ぜて共通の重みで変換する簡潔な層にしました。辺に沿った局所計算を使い、特徴とグラフ構造を効率よく組み合わせることが狙いです。

<div class="gnn-calc" markdown="1">

### 次数による正規化

接続数によって集約の規模が偏りすぎないように、受け手と送り手の次数で重みを調整します。
{.gnn-purpose}

<div class="gnn-calc-layout" markdown="1">

<div class="gnn-graph-panel" markdown="1">

<div class="gnn-value-graph" markdown="1">

{{component:visual-002}}

**橙・太枠：今回変わった部分**  
辺のスコア・係数を追加または変更
{.gnn-change-legend}

</div>

</div>

<aside class="gnn-working" aria-label="計算過程" markdown="1">

自己ループを加え、自分も参照先にします。自己ループ込みの次数はA=4、B=2、C=D=3、E=F=2。

$$
c_{Au}=\frac{1}{\sqrt{\tilde d_A\tilde d_u}}
$$

例：B → Aは1/√(4×2) ≈ 0.354。

図のAの左側の線は、自分を集める係数1/4です。係数は特徴値ではなく接続数から決まります。係数の合計は約1.181で、合計1の平均とは異なります。

</aside>

</div>

</div>

<div class="gnn-calc" markdown="1">

### ノードAの特徴更新

次数で重み付けした特徴を足し、近隣の情報を含む新しいAの表現を作ります。
{.gnn-purpose}

<div class="gnn-calc-layout" markdown="1">

<div class="gnn-graph-panel" markdown="1">

<div class="gnn-value-graph" markdown="1">

{{component:visual-003}}

**橙・太枠：今回変わった部分**  
ノードの数値を更新
{.gnn-change-legend}

</div>

<button class="gnn-replay" hidden type="button">数値の変化を見る ↻</button>

動きは変更前後をつなぐ表示です。途中の値は追加の演算や学習を表しません。
{.gnn-animation-note}

</div>

<aside class="gnn-working" aria-label="計算過程" markdown="1">

<div class="table-scroll" tabindex="0" markdown="1">

| 送り手 | 係数 × 特徴 |
| --- | --- |
| A | 0.250 × (1, 0) = (0.25, 0) |
| B | 0.354 × (0, 2) = (0, 0.707) |
| C | 0.289 × (2, 1) = (0.577, 0.289) |
| D | 0.289 × (1, 1) = (0.289, 0.289) |

</div>

成分ごとに足すと **(1.116, 1.284)**。この例ではW=Iなので変換後も同じで、ReLU後も変わりません。通常は共有Wを学習します。

</aside>

</div>

</div>

全ノードの更新を一括して計算するために、同じ近隣集約を行列の積で表します。

$$
H^{(\ell+1)}=\sigma(\tilde D^{-1/2}\tilde A\tilde D^{-1/2}H^{(\ell)}W^{(\ell)})
$$

全ノードをまとめた式。Hの各行がノード特徴、Ãは自己ループを追加した隣接行列、D̃はその次数を並べた対角行列です。上の局所計算を全ノードについて行います。

</section>

<section id="gat" markdown="1">

## GATのAttention係数

### GATの設計

つながっている相手が、どれも同じように予測に役立つとは限りません。GCNの次数に基づく係数だけでは、隣の特徴に応じて重みを付け分けられません。GATは近隣へのAttentionを使い、どの相手の情報を強く取り込むかを学習可能にしました。グラフ全体の複雑な行列分解を必要とせず、近隣ごとに重みを計算する設計です。

GCNの係数はグラフの次数から決まりました。GATは特徴を変換し、受け手・送り手のペアからスコアを作って係数を計算します。以下は原型GATの加法的Attentionです。TransformerのQ・Kの内積とは式が異なります。

<aside class="note" markdown="1">

**数値例の条件**

2次元特徴、1 head、自己ループあり、dropoutなし。Wとaは計算を見せるために固定した値で、学習済みモデルの結果ではありません。

</aside>

<div class="gnn-calc" markdown="1">

### 特徴の線形変換

元の特徴をそのまま使う代わりに、学習するWで予測に役立つ成分の組み合わせを作ります。
{.gnn-purpose}

<div class="gnn-calc-layout" markdown="1">

<div class="gnn-graph-panel" markdown="1">

<div class="gnn-value-graph" markdown="1">

{{component:visual-004}}

**橙・太枠：今回変わった部分**  
ノードの数値を更新
{.gnn-change-legend}

</div>

<button class="gnn-replay" hidden type="button">数値の変化を見る ↻</button>

動きは変更前後をつなぐ表示です。途中の値は追加の演算や学習を表しません。
{.gnn-animation-note}

</div>

<aside class="gnn-working" aria-label="計算過程" markdown="1">

$$
W=\begin{pmatrix}1&-1\\1&1\end{pmatrix},\quad z_u=Wh_u
$$

Wは全ノードで共有する2×2行列。特徴は列ベクトルとして掛けます。

**Bの中の数値：**  
(0, 2) → (1×0 − 1×2, 1×0 + 1×2)  
→ **(−2, 2)**

Aは(1, 1)、Cは(1, 3)、Dは(0, 2)になります。このzをスコア作りにも、最後の集約にも使います。

</aside>

</div>

</div>

<div class="gnn-calc" markdown="1">

### Attentionスコアの計算

どの隣を強く取り込むかを決めるために、Aと各送り手の特徴を一つの数へまとめます。
{.gnn-purpose}

<div class="gnn-calc-layout" markdown="1">

<div class="gnn-graph-panel" markdown="1">

<div class="gnn-value-graph" markdown="1">

{{component:visual-005}}

**橙・太枠：今回変わった部分**  
辺のスコア・係数を追加または変更
{.gnn-change-legend}

</div>

</div>

<aside class="gnn-working" aria-label="計算過程" markdown="1">

$$
s_{Au}=a^{\mathsf T}[z_A\Vert z_u],\quad a=(-1,0,1,0.5)^{\mathsf T}
$$

連結∥は2次元＋2次元を並べる操作。足し算ではありません。

**A ← B：**  
[z_A ∥ z_B] = [1, 1, −2, 2]  
s_AB = −1×1 + 0×1 + 1×(−2) + 0.5×2 = **−2**

負のスコアにも小さな傾きを残すため、LeakyReLUを使います。この例では負なら0.2倍し、非負ならそのままです。Bの−2は**−0.4**になります。

<div class="table-scroll" tabindex="0" markdown="1">

| 送り手 | 内積 s | LeakyReLU後 e |
| --- | --- | --- |
| A | 0.5 | 0.5 |
| B | -2 | -0.4 |
| C | 1.5 | 1.5 |
| D | 0 | 0 |

</div>

</aside>

</div>

</div>

<div class="gnn-calc" markdown="1">

### スコアの正規化

参照先どうしのスコアを比較できるように、指数を取り、同じ受け手の参照先内で正規化します。
{.gnn-purpose}

<div class="gnn-calc-layout" markdown="1">

<div class="gnn-graph-panel" markdown="1">

<div class="gnn-value-graph" markdown="1">

{{component:visual-006}}

**橙・太枠：今回変わった部分**  
辺のスコア・係数を追加または変更
{.gnn-change-legend}

</div>

</div>

<aside class="gnn-working" aria-label="計算過程" markdown="1">

$$
\alpha_{Au}=\frac{\exp(e_{Au})}{\sum_{k\in\{A,B,C,D\}}\exp(e_{Ak})}
$$

分母はA自身と直接の隣B・C・Dだけです。E・Fは含みません。

<div class="table-scroll" tabindex="0" markdown="1">

| 送り手 | e → exp(e) | α |
| --- | --- | --- |
| A | 0.5 → 1.649 | 0.211 |
| B | -0.4 → 0.670 | 0.086 |
| C | 1.5 → 4.482 | 0.575 |
| D | 0 → 1.000 | 0.128 |

</div>

分母 = 1.649 + 0.670 + 4.482 + 1.000 ≈ **7.801**。係数の合計は1です。Bのスコアは負でしたが、係数は0にはなりません。

</aside>

</div>

</div>

<div class="gnn-calc" markdown="1">

### 重み付き集約による更新

強く参照する相手ほど大きく寄与するように、変換後の特徴zにαを掛けて足します。
{.gnn-purpose}

<div class="gnn-calc-layout" markdown="1">

<div class="gnn-graph-panel" markdown="1">

<div class="gnn-value-graph" markdown="1">

{{component:visual-007}}

**橙・太枠：今回変わった部分**  
ノードの数値を更新
{.gnn-change-legend}

</div>

<button class="gnn-replay" hidden type="button">数値の変化を見る ↻</button>

動きは変更前後をつなぐ表示です。途中の値は追加の演算や学習を表しません。
{.gnn-animation-note}

</div>

<aside class="gnn-working" aria-label="計算過程" markdown="1">

<div class="table-scroll" tabindex="0" markdown="1">

| 送り手 | α × z |
| --- | --- |
| A | 0.211 × (1, 1) = (0.211, 0.211) |
| B | 0.086 × (-2, 2) = (-0.172, 0.172) |
| C | 0.575 × (1, 3) = (0.575, 1.724) |
| D | 0.128 × (0, 2) = (0, 0.256) |

</div>

第1成分：(0.211) + (-0.172) + (0.575) + (0.000) = **0.614**  
第2成分：0.211 + 0.172 + 1.724 + 0.256 = **2.363**

$$
h_A^\prime=\operatorname{ReLU}\left(\sum_u\alpha_{Au}z_u\right)
$$

この例は中間層の活性化としてReLUを選択。両成分が正なので値は変わりません。

Aの元の特徴(1, 0)が、変換を経て最終的に**(0.614, 2.363)**に更新されました。

</aside>

</div>

</div>

</section>

<section id="heads" markdown="1">

## 複数headの連結

<div class="gnn-calc" markdown="1">

### ノードAの表現の連結

異なるW・aで集めた複数の表現を残すため、headごとの出力を連結します。
{.gnn-purpose}

<div class="gnn-calc-layout" markdown="1">

<div class="gnn-graph-panel" markdown="1">

<div class="gnn-pipeline" markdown="1">

<div markdown="1">

**head 1のA**(0.614, 2.363)
</div>

<div markdown="1">

**head 2のA**(0.618, 1.367)
</div>

<div markdown="1">

**連結後のA：4次元**(0.614, 2.363, 0.618, 1.367)
</div>

</div>

</div>

<aside class="gnn-working" aria-label="計算過程" markdown="1">

head 1は上の計算。head 2はW₂=I、a₂=(0, 1, −1, 0.5)です。

<div class="table-scroll" tabindex="0" markdown="1">

| head 2 | A | B | C | D |
| --- | --- | --- | --- | --- |
| 内積 | -1.000 | 1.000 | -1.500 | -0.500 |
| LeakyReLU | -0.200 | 1.000 | -0.300 | -0.100 |
| softmax | 0.158 | 0.524 | 0.143 | 0.175 |

</div>

中間層では連結します。原論文の最終分類層ではheadの出力を平均してから出力の活性化を適用します。

</aside>

</div>

</div>

</section>

<section id="learning" markdown="1">

## GATの学習パラメータ

予測を正解へ近づけるため、損失から逆伝播して特徴変換とスコアのパラメータを更新します。

<div class="gnn-pipeline" markdown="1">

<div markdown="1">

**入力から計算**W・a → スコア → α → 表現
</div>

<div markdown="1">

**予測と正解を比較**出力ヘッド → 損失
</div>

<div markdown="1">

**逆伝播**W・aなどを更新
</div>

</div>

Wとaはデータから学ぶパラメータです。αそのものを辺ごとの固定パラメータとして保存するのではなく、その時の特徴とW・aから計算します。利用時には学んだW・aを固定し、新しい入力に対してαと表現を計算します。

<aside class="note" markdown="1">

**係数の読み方**

大きなαは、その集約で強く重み付けしたことを示します。予測全体の重要性や因果関係を直接示すものではありません。原型GATでは、受け手を変えれば近隣の順位が自由に入れ替わるとは限りません。

</aside>

</section>

<section id="sage" markdown="1">

## GraphSAGEの集約と更新

### GraphSAGEの設計

利用者や論文が増えるグラフでは、学習時には存在しなかった点にも予測したくなります。各ノード専用のベクトルを覚える方法だけでは、そのまま新しい点の表現を作れません。GraphSAGEは、ノードの特徴と近隣から表現を作る共通の関数を学びます。さらに近隣をサンプリングし、大きなグラフでも計算対象を抑えます。未知のノードやグラフへ適用するには、入力の特徴が同じ意味で使えることが前提です。

近隣を何層も展開すると計算対象が増えます。GraphSAGEは近隣をサンプリングして集約する枠組みです。ここでは自己特徴と近隣平均を連結するmean集約を扱います。

<div class="gnn-calc" markdown="1">

### 近隣のサンプリングと平均

大きなグラフで計算対象が増えすぎないように、近隣をサンプリングして代表的な特徴をまとめます。
{.gnn-purpose}

<div class="gnn-calc-layout" markdown="1">

<div class="gnn-graph-panel" markdown="1">

<div class="gnn-value-graph" markdown="1">

{{component:visual-008}}

**橙・太枠：今回変わった部分**  
参照する近隣を選択（点線は不採用）
{.gnn-change-legend}

</div>

</div>

<aside class="gnn-working" aria-label="計算過程" markdown="1">

Aの近隣B・C・Dから、今回はB・Cの2個を選びます。点線のDはグラフから削除したわけではありません。

<div class="gnn-pipeline" markdown="1">

<div markdown="1">

**Bの特徴**(0, 2)
</div>

<div markdown="1">

**Cの特徴**(2, 1)
</div>

<div markdown="1">

**近隣平均 m_A**((0, 2) + (2, 1)) / 2 = (1, 1.5)
</div>

</div>

平均にはAを入れません。自己情報はこの後、別に合わせます。B・Dを選んだ場合の平均は(0.5, 1.5)となります。

</aside>

</div>

</div>

<div class="gnn-calc" markdown="1">

### 自己特徴と近隣特徴の統合

自分の特徴と周囲の特徴を両方残してから、共有Wで新しい表現へ変換します。
{.gnn-purpose}

<div class="gnn-calc-layout" markdown="1">

<div class="gnn-graph-panel" markdown="1">

<div class="gnn-value-graph" markdown="1">

{{component:visual-009}}

**橙・太枠：今回変わった部分**  
ノードの数値を更新
{.gnn-change-legend}

</div>

<button class="gnn-replay" hidden type="button">数値の変化を見る ↻</button>

動きは変更前後をつなぐ表示です。途中の値は追加の演算や学習を表しません。
{.gnn-animation-note}

</div>

<aside class="gnn-working" aria-label="計算過程" markdown="1">

**連結：**  
[h_A ∥ m_A] = [1, 0, 1, 1.5]  
2次元と2次元を並べ、4次元にします。

$$
W=\begin{pmatrix}1&0&1&0\\0&1&0&1\end{pmatrix}
$$

2×4の例示用Wで、4次元を2次元へ変換します。

第1成分：1×1 + 0×0 + 1×1 + 0×1.5 = **2**  
第2成分：0×1 + 1×0 + 0×1 + 1×1.5 = **1.5**

ReLU後は**(2, 1.5)**。この値を次の図で正規化します。

</aside>

</div>

</div>

<div class="gnn-calc" markdown="1">

### ベクトルの正規化

表現の方向を保ちながら大きさをそろえるために、ベクトルを自分の長さで割ります。
{.gnn-purpose}

<div class="gnn-calc-layout" markdown="1">

<div class="gnn-graph-panel" markdown="1">

<div class="gnn-value-graph" markdown="1">

{{component:visual-010}}

**橙・太枠：今回変わった部分**  
ノードの数値を更新
{.gnn-change-legend}

</div>

<button class="gnn-replay" hidden type="button">数値の変化を見る ↻</button>

動きは変更前後をつなぐ表示です。途中の値は追加の演算や学習を表しません。
{.gnn-animation-note}

</div>

<aside class="gnn-working" aria-label="計算過程" markdown="1">

長さ = √(2² + 1.5²) = **2.5**  
(2, 1.5) / 2.5 = **(0.8, 0.6)**

元のAの(1, 0)が、近隣平均との連結・変換を経て、最終的に(0.8, 0.6)へ更新されました。

ここでは原論文のL2正規化に従います。ゼロベクトルの扱いは実装で定めます。

</aside>

</div>

</div>

</section>

<section id="compare" markdown="1">

## GCN・GAT・GraphSAGEの比較

<div class="table-scroll" tabindex="0" markdown="1">

| モデル | 係数・対象の決め方 | 自己情報 | 学ぶもの |
| --- | --- | --- | --- |
| GCN | 次数 → 係数 → 集約 | 自己ループとして含む | 共有W |
| GAT | 特徴変換 → スコア → softmax → 集約 | 自己へのAttention | headごとの共有W・a |
| GraphSAGE（mean） | 近隣を選択 → 平均 → 連結 → 変換 | 近隣平均と別に連結 | 共有Wなど |

</div>

同じグラフでも計算の設計は異なります。出力の値の大小はモデル性能の比較にはなりません。和や平均で集めるため、近隣を列挙する順序を入れ替えても結果は同じです。

</section>

<section id="outputs" markdown="1">

## ノード・辺・グラフの予測

<figure markdown="1">

{{component:visual-011}}

<figcaption markdown="1">

同じGNNの表現を、異なるタスクの出力へ変える。
</figcaption>
</figure>

* ノード分類：各ノードの特徴を分類器へ。例えば論文の研究分野。
* リンク予測：二つのノード表現の内積やMLPから関係のスコアを作る。評価時に予測対象の辺を入力へ漏らさない。
* グラフ全体の予測：全ノードの和・平均などのreadoutから分子の性質を予測する。

層を増やすと遠くまで届く一方、表現が似通うover-smoothingや、多数の遠方情報を小さなベクトルへ押し込むover-squashingが問題になります。ここで示した原型は結合の種類などの辺特徴をすべて直接使うわけではありません。分子では辺特徴や3Dの回転・並進の対称性を扱う拡張が重要です。

</section>

<section id="sources" markdown="1">

## 出典・参考資料

* [GCN：Kipf & Welling ↗](source:ref-001)
* [GAT：Veličković et al. ↗](source:ref-002)
* [GraphSAGE：Hamilton et al. ↗](source:ref-003)
* [Message Passing Neural Networks ↗](source:ref-004)

</section>
