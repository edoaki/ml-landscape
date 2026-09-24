---
id: transformer
title: Transformer
summary: Transformerは、要素どうしの関係に応じて情報を集め、各要素の表現を更新するモデルです。Attention、FFN、残差接続・正規化、位置情報、EncoderとDecoderの構造を図と計算で追います。
url: models/transformer.html
status: migrated
scope: ページ。注意機構、FFN、残差・正規化、位置情報、マスクとEncoder・Decoderの構造
prerequisites:
- fundamentals
related:
- llm
- vit
origins:
- transformer.html#why
- transformer.html#structure
- transformer.html#attention
- transformer.html#block
- transformer.html#masks
- transformer.html#sources
scripts: []
styles:
- content/models/transformer/components/page.css
english_title: Transformer
---

<section id="why" markdown="1">

## Transformerの基本

翻訳などで文章を扱うときは、離れた単語の関係も使いたくなります。例えば「私は家族と東京に住んでいる」なら、「住んでいる」を理解するには、誰が、誰と、どこに住むのかを結び付ける必要があります。

系列を順に処理するRNN・LSTMは、ここまでの情報を状態にまとめ、次の単語へ渡します。ただし、**次の状態を作るには、前の状態ができるのを待つ**必要があります。学習でも一つの文の位置方向を並列化しにくく、離れた位置の情報は多くの更新を経由します。LSTMは記憶を保持しやすくしますが、この順次処理の制約は残ります。

<figure markdown="1">

{{component:visual-001}}

<figcaption markdown="1">

情報の経路を示す模式図。上はRNNの状態の受け渡し、下は1層のSelf-Attention。下の点は各位置の入力と更新後の表現。太線は一つの参照経路の例。
</figcaption>
</figure>

そこで、「前から順に状態を渡す代わりに、必要な位置の情報を直接参照して、それぞれの表現を更新できないか」と考えます。これを担うのが**Self-Attention**です。同じ層の入力がそろえば、各位置の更新を行列演算でまとめて計算できます。

AttentionはTransformer以前から、RNNを使う翻訳モデルなどで利用されていました。2017年のTransformerは、系列に沿った再帰や畳み込みを使わず、Attentionを中心にEncoderとDecoderを組み立て、翻訳の品質と学習の並列性を両立させました。[原論文：Attention Is All You Need](source:ref-001)。

<aside class="note" markdown="1">

**Transformerの設計思想**

要素間の関係に応じて、必要な情報を直接集める。その計算を各位置で並列に行い、層を重ねて表現を更新する。文章を生成する際の「次の単語を一つずつ出す」処理は、別に必要になる。

</aside>

</section>

<section id="structure" markdown="1">

## Transformerの全体構造

Transformerは、位置ごとのベクトルを受け取り、**Attentionで要素間の情報を交換し、FFNで各位置の特徴を加工するブロック**を重ねます。まず全体の流れと1ブロックの構造を見てから、Attentionの中の計算へ進みます。

<figure markdown="1">

{{component:visual-002}}

<figcaption markdown="1">

同じ構造のブロックをN層重ねる。通常、各層には別々の学習可能なパラメータがある。
</figcaption>
</figure>

### 1ブロックの情報の流れ

図は上から下へ読みます。横に並ぶ列は、文章中の位置1〜4です。Attentionでは列の間で情報を交換し、FFNでは各列を独立に加工します。残差接続とLayerNormは、情報を引き継ぎながら学習を安定させる役割を持ちます。

<figure markdown="1">

{{component:visual-003}}

<figcaption markdown="1">

各列は別の処理手順ではなく、同じ文の4つの位置。hの下付きは位置、上付きの(ℓ−1)と(ℓ)は層を表す。残差経路は1列分だけ代表して描いた。原論文のPost-LN型を示し、headの並列化は省略。GPTでは因果マスクを加え、正規化の配置が異なる設計も使う。
</figcaption>
</figure>

</section>

<section id="attention" markdown="1">

## Self-Attention

Self-Attentionの「Self」は、同じ系列の中で参照し合うという意味です。「どこから、どれくらい情報を取り込むか」を、今の表現から毎回計算します。まず1 headの処理を見ます。

### 1. Q・K・Vへの変換

<figure markdown="1">

{{component:visual-004}}

<figcaption markdown="1">

全てのトークンからQ・K・Vを作る。単語ごとに役を割り振るのではなく、一つの単語が参照する側にも、参照される側にもなる。
</figcaption>
</figure>

**Query（Q）**は参照する側の特徴、**Key（K）**は照合される側の特徴、**Value（V）**は実際に集める内容です。例えばliveのQを各単語のKと照合し、その結果に応じて各単語のVを集めます。

$$
Q=XW_Q,\qquad K=XW_K,\qquad V=XW_V
$$

W_Q・W_K・W_Vはそれぞれ別の学習可能な行列。同じ層・headの中では、各位置に同じ行列を使う。QとKは内積を取れる同じ次元dₖを持つ。

### 2. Attention重みの計算

参照する位置iのqᵢと、参照先jのkⱼの内積を取ります。**内積の値が高い = 関連度が高い**と考えます。ここでの関連度は、このheadで情報を取り込むための照合の強さです。これは学習した特徴どうしの適合度で、「単語の意味が似ているか」だけを測るものではありません。

$$
s_{ij}=\frac{q_i k_j^{\mathsf T}}{\sqrt{d_k}},\qquad a_{ij}=\frac{\exp(s_{ij})}{\sum_m\exp(s_{im})}
$$

√dₖでスコアの尺度を調整し、参照先に沿ってsoftmaxを取る。一つのqueryについて重みの和は1になる。

<figure markdown="1">

{{component:visual-005}}

<figcaption markdown="1">

内積の値が高い = 関連度が高い。スコアは√dₖで割った後の値。関連度が高い参照先ほど、大きな重みになる。数値は説明用の例。
</figcaption>
</figure>

### 3. Vの重み付き和

**関連度が高いものほど重みが大きくなり、そのVの方へ重心が寄ります。**重み付きの足し合わせを、Vの空間で「重心に移動する」と捉えたのが下の図です。

<figure markdown="1">

{{component:visual-006}}

<figcaption markdown="1">

円の大きさは重みの目安。liveのVから、重み付きの重心へ移動する矢印だけを描いた。関連度が高いTokyoのVの方へ重心が寄る。1 headの重み付き和の図で、残差接続やFFNを含む層全体の移動とは異なる。
</figcaption>
</figure>

$$
z_i=\sum_j a_{ij}v_j,\qquad Z=AV
$$

係数aᵢⱼでvⱼを重み付けし、足したものが位置iの集約結果zᵢ。全位置の計算を行列でまとめるとZ=AVになる。

liveだけでなく、IもTokyoもwithも、それぞれ自分のQで重みを求めます。**同じ層では更新前の表現から、全位置の集約結果をまとめて作ります。**先に更新した単語を、その層の別の単語の計算へ順に渡すわけではありません。

学習して保存するのは射影行列などのパラメータです。Attentionの重みaᵢⱼは入力から計算する値なので、文や層が変われば変わります。

</section>

<section id="block" markdown="1">

## Transformerブロック

### Multi-head Attention

一つの照合だけではなく、異なるQ・K・Vの射影を使って複数の集約を並列に行います。これが**Multi-head Attention**です。各headの結果を連結し、出力の行列W_Oで組み合わせます。各headが「文法」「場所」などの人間の概念に一対一で対応するとは限りません。

<figure markdown="1">

{{component:visual-007}}

<figcaption markdown="1">

headは別々の学習可能な射影を使う。「場所」「人」などの役割を人が固定して割り当てるわけではない。
</figcaption>
</figure>

### FFNによる特徴の変換

**Attentionは要素間の情報交換、FFNは各要素の特徴の加工**を担います。FFN（feed-forward network、MLPとも呼びます）は、各位置に同じ重みで適用する非線形変換です。位置同士を直接混ぜず、集めた情報から予測に役立つ特徴を作ります。

$$
\operatorname{FFN}(h_i)=\phi(h_iW_1+b_1)W_2+b_2
$$

φはReLUなどの非線形関数。原論文はReLUを使用。Attentionにもsoftmaxや入力依存の重みがあるので、Attention全体が単なる線形変換という意味ではない。

### 残差接続とLayerNorm

**残差接続**は、処理の入力をその出力に足す経路です。元の情報を直接引き継ぎながら変化分を加え、深いモデルへ学習の信号を伝えやすくします。**LayerNorm**は各トークン内の特徴を正規化し、学習を安定させるために使います。

$$
\begin{aligned} U&=\operatorname{LayerNorm}(H^{\ell-1}+\operatorname{MHA}(H^{\ell-1}))\\ H^\ell&=\operatorname{LayerNorm}(U+\operatorname{FFN}(U))\end{aligned}
$$

原論文のPost-LN型を、dropoutを省いて表した式。Attention側とFFN側の両方に残差接続がある。処理の前に正規化するPre-LN型もある。

このブロックを重ねたものがTransformerです。通常、層ごとに別のパラメータを持ちます。[LLMページのGPTの図](page:llm#representations)では、このブロックを一つ通るたびに全ての点が移動します。移動はAttentionだけの重心移動ではなく、残差・正規化・FFNまで含む表現の更新を表しています。

</section>

<section id="masks" markdown="1">

## EncoderとDecoder

Encoderは入力全体から各位置の表現を作り、Decoderはそれまでの出力を使って続きを予測します。翻訳のEncoder–Decoder型では、この二つをつなぎ、Decoderが入力文の情報も参照します。

<figure markdown="1">

{{component:visual-008}}

<figcaption markdown="1">

翻訳に使うEncoder–Decoder型の模式図。上から下へ処理する。残差接続・LayerNormは省略。各Decoder層はEncoderの最終出力を参照する。
</figcaption>
</figure>

Decoderの**Self-Attention**は、生成途中の文の情報を集めます。続く**Cross-Attention**は、Encoderが作った入力文の表現から必要な情報を取り込みます。その後、Feed Forwardで各位置の特徴を加工します。

<div class="table-scroll" tabindex="0" markdown="1">

| モデルの構成 | 使うブロック | 出力へのつなぎ方 |
| --- | --- | --- |
| Encoder-only（BERTなど） | Self-Attention → Feed Forward | 入力の表現を分類や穴埋め予測などに使う |
| Decoder-only（[GPT](page:llm#gpt)など） | Self-Attention → Feed Forward | 次のトークンを予測する。別のEncoderやCross-Attentionは持たない |
| Encoder–Decoder（原論文の翻訳） | Encoder ＋ Cross-Attentionを持つDecoder | 入力文を参照しながら、出力文を生成する |

</div>

### Self-AttentionとCross-Attentionの違い

<figure markdown="1">

{{component:visual-009}}

<figcaption markdown="1">

矢印は情報の流れ。Q・K・Vはそれぞれ別の線形層で作る。
</figcaption>
</figure>

**Self-Attention：**同じ系列の表現からQ・K・Vを作ります。「self」は自分一つだけを見るという意味ではなく、同じ系列内の位置を参照するという意味です。

**Cross-Attention：**QはDecoder側、KとVはEncoderの最終出力から作ります。Decoder側のQで入力文のKとの関連度を求め、その重みに応じて入力文のVを足し合わせます。結果はDecoder側の各位置の表現に取り込まれます。

例えば「I have a cat」を訳すとき、Decoderは「私は」という生成途中の文を使いつつ、Cross-Attentionで入力文を参照して続きを予測します。入力文と出力文は、長さが同じでなくても構いません。

どちらも「QとKの内積 → softmax → Vの重み付き和」という計算を使います。違うのは、**同じ系列から集めるか、別の系列から集めるか**です。

画像を小領域に分けて処理する構造は[ViT](page:vit)、画像と言語をつないで答える構成例は[VLM](page:vlm)で説明します。

</section>

<section id="cost-and-interpretation" markdown="1">

## Attentionの計算量と解釈

離れた要素を直接参照できる一方、通常の密なSelf-Attentionではn×nの関係を扱うため、長い系列ほど計算が増えます。要素間の関係を広く扱える利点と、その計算・メモリの負担が対になっています。

この負担を減らす方法には、BigBirdやLongformerのように参照先を絞る方法と、FlashAttentionのようにメモリの読み書きを減らす方法があります。具体的な仕組みは[Attentionの計算を減らす](page:efficiency#sparse-attention)で説明します。

### Attentionの重みは判断の理由を表すか

Attentionの重みを色の濃さで示すと、モデルがどの単語を参照したかを見ることができます。ただし、**情報を集める割合と、最終的な予測への影響の大きさは同じではありません**。重みを掛ける相手は文脈を含んだVのベクトルであり、その後にも他のヘッド、残差接続、層を通る計算が続くからです。

この区別を示したのが、JainとWallaceの[Attention is not Explanation（2019）](source:ref-003)です。論文の映画レビューの分類例では、学習済みモデルの他のパラメータを固定し、**Attentionの重みを大きく変えても、ほぼ同じ予測を出す別の重みの分布**を見つけています。参照先の色分けが違っても結論が変わらないなら、濃く色付いた単語を指して「この単語が判断の決め手だった」と断定することはできません。

この実験は主に双方向RNNとAttentionを組み合わせたモデルを対象としており、GPTの全ヘッドについて同じ結果を示したものではありません。また、後続の[Attention is not not Explanation（Wiegreffe・Pinter, 2019）](source:ref-004)は、「説明」の定義や、重みをどう変更・学習するかによって評価が変わると指摘しました。Attentionが常に説明として無価値だと結論するのも行き過ぎです。

Transformerでも、Attentionの可視化は参照の様子を調べる手がかりになります。その参照が判断に必要だったかを確かめるには、重みや内部表現を変更したときの出力の変化なども調べます。こうした検証は[内部への介入による分析](page:interpretability#llm)で扱います。

</section>

<section id="sources" markdown="1">

## 出典・参考資料

* [Attention Is All You Need（2017）：設計の背景・構造・計算 ↗](source:ref-001)
* [BERT（2018） ↗](source:ref-002)
* [Attention is not Explanation（Jain・Wallace, 2019） ↗](source:ref-003)
* [Attention is not not Explanation（Wiegreffe・Pinter, 2019） ↗](source:ref-004)

</section>
