---
id: diffusion
title: Diffusion
summary: 猫がノイズへ崩れ、ノイズから猫が現れる。予測器の内部、学習の正解、文章による条件付けを順に見ます。
url: models/diffusion.html
status: migrated
scope: ページ。ノイズを使う学習と生成過程
prerequisites: []
related: []
origins:
- diffusion.html#why
- diffusion.html#forward
- diffusion.html#training
- diffusion.html#network
- diffusion.html#conditional
- diffusion.html#sampling
- diffusion.html#sources
scripts: []
styles: []
english_title: Diffusion Models
---

<section id="why" markdown="1">

## Diffusionの基本

単純なノイズから複雑な画像を一度に作るのは難しい問題です。拡散モデルは、データを少しずつノイズへ崩す過程を用意し、それに対応する逆向きの変化を学びます。DDPMでは、各ノイズ段階で「どんなノイズが混ざっているか」を予測する学習から、段階的な画像生成につなげます。

</section>

<section id="forward" markdown="1">

## ノイズの付加

ここではDDPMのノイズ予測を例にします。時刻tが大きいほど元の信号が少なくなるよう、ノイズの強さを決めます。

<figure markdown="1">

{{component:visual-001}}

<figcaption markdown="1">

写真風の猫で段階を表したAI生成の説明図。実際のDDPMの中間出力や、式を数値計算した画像ではありません。
</figcaption>
</figure>

$$
x_t = \sqrt{\bar\alpha_t}\,x_0 + \sqrt{1-\bar\alpha_t}\,\varepsilon,\quad \varepsilon\sim\mathcal N(0,I)
$$

x₀は元画像、εは画像と同じ形のランダムな数値です。ᾱₜは元画像の信号をどれだけ残すかを決める係数。例えばᾱₜ=0.64なら、xₜ=0.8x₀+0.6εです。N(0,I)は各成分が独立な平均0・分散1の正規分布を表します。

このノイズ付加には学習は必要ありません。式とスケジュールが分かれば、x₀から好きな時刻tのxₜを直接作れます。学ぶのは、ノイズ付きの画像を見て逆向きの更新に必要な量を予測する部分です。

</section>

<section id="training" markdown="1">

## ノイズ予測の学習

**正解のノイズは自分で加えたものなので、分かっています。**訓練画像を選び、時刻tとノイズεをランダムに選びます。式でxₜを作り、予測器にはxₜとtを与えます。

<figure markdown="1">

{{component:visual-002}}

<figcaption markdown="1">

青：学習例を作る入力。橙の点線：損失から予測器へ戻す勾配。x₀や正解εを、答えとして予測器へ渡すことはしません。猫は説明用のAI生成画像。
</figcaption>
</figure>

$$
L_{\mathrm{simple}}=\mathbb E_{x_0,t,\varepsilon}\left[\lVert\varepsilon-\varepsilon_\theta(x_t,t)\rVert^2\right]
$$

予測εθと、実際に加えたεの差を、画素・チャネルごとに二乗して集計します。その損失を小さくする方向へ、逆伝播で重みθを更新します。これはDDPMの代表的な簡略化損失です。

例えば、ある成分に加えたノイズが0.6、予測が0.2なら、その成分の二乗誤差は(0.6−0.2)²=0.16です。画像・時刻・ノイズを変えながら多くの例で繰り返すと、同じ予測器が、ノイズの少ない段階から多い段階まで担当できるようになります。

**通常のこの学習では、生成の全ステップを毎回実行しません。**ミニバッチ内の各画像で時刻を選び、その時刻の予測をまとめて学習します。一方、学習後の生成では予測と更新を何度も繰り返します。

一枚のxₜから、元画像や加えたノイズを常に一意に特定できるわけではありません。予測器は多くの訓練例から画像の構造を学び、入力に応じた予測をします。以下はノイズ予測で説明しますが、元画像x₀や、信号とノイズを組み合わせたvを予測する定式化もあります。

</section>

<section id="network" markdown="1">

## ノイズ予測器の構造

**U-NetやTransformerが担当するのは、各時刻の「ノイズの予測」です。**例えばRGB画像なら、入力xₜが64×64×3のとき、予測するノイズも64×64×3です。「猫である確率」を一つ返す分類器ではなく、各位置・各チャネルの数値を出力します。

<figure markdown="1">

{{component:visual-003}}

<figcaption markdown="1">

ニューラルネットワークによる予測と、サンプラによる状態の更新を分けて考える。生成中は同じ重みθを繰り返し使う。
</figcaption>
</figure>

### U-Netによるノイズ予測

<figure markdown="1">

{{component:visual-004}}

<figcaption markdown="1">

模式図。スキップ接続はノイズ付き入力から抽出した特徴を渡します。学習時のきれいな正解画像を生成時に渡す経路ではありません。
</figcaption>
</figure>

縮小側では畳み込みで特徴を抽出し、空間の解像度を下げて、広い範囲の配置を捉えます。拡大側では解像度を戻し、同じ解像度の縮小側の特徴をスキップ接続で受け取ります。これにより、全体の形を踏まえながら、輪郭や毛並みのような細かな位置情報を利用できます。

時刻tもベクトルへ変換し、各ブロックに加えたり、特徴のスケールや偏りを調整したりします。同じ猫らしい模様でも、強いノイズの段階と仕上げの段階では必要な予測が違うためです。拡散モデルのU-NetにはAttentionを組み込む設計もあります。

### Transformer・DiTによるノイズ予測

<figure markdown="1">

{{component:visual-005}}

<figcaption markdown="1">

代表例としてクラス条件付きDiTの考え方を簡略化。図はノイズ予測の経路に絞り、原論文の分散予測の出力は省略しています。
</figcaption>
</figure>

画像、または圧縮した潜在表現を小さなパッチに区切り、それぞれをベクトルにします。位置情報を加え、Self-Attentionで離れたパッチの関係を、FFNで各パッチの特徴を処理します。最後にパッチごとの予測を空間上に並べ直します。

原論文のDiTでは、時刻とクラスの埋め込みから正規化の係数などを調整する方式（adaLN）を使います。文章を扱うモデルではcross-attentionなどの設計もあります。U-Netの縮小・拡大の段数やTransformerの層数は「1回の予測の深さ」、拡散ステップ数は「その予測器を呼ぶ回数」です。

</section>

<section id="conditional" markdown="1">

## 条件付き生成

無条件生成は、学んだ画像の分布から画像を作ります。条件付き生成では、クラス「猫」、文章「座っている茶トラ猫」、輪郭画像などを条件cとして与え、その条件に合う画像の分布を学びます。同じ条件でも初期ノイズが違えば、異なる画像を作れます。

<figure markdown="1">

{{component:visual-006}}

<figcaption markdown="1">

文章条件を使うLDM型の例。Qは画像の特徴、K・Vは文章の特徴から作ります。画像の各位置が、条件文のどの語を参照するかを学びます。
</figcaption>
</figure>

文章はテキストencoderでベクトル列へ変換します。cross-attentionでは、画像側の各位置が文章中の語を参照し、その情報を画像の特徴へ取り込みます。条件は最後に画像へ貼り付けるものではなく、各段階のノイズ予測に影響します。

### 条件付き生成の学習

文章から生成したければ、画像x₀とその内容を説明するキャプションcをペアで用意します。画像へノイズを加え、予測器にはxₜ・t・cを渡します。元のキャプションには通常、画像と同じガウスノイズを加えません。正解は無条件の場合と同じく、自分で加えたεです。

$$
L_{\mathrm{cond}}=\mathbb E_{(x_0,c),t,\varepsilon}\left[\lVert\varepsilon-\varepsilon_\theta(x_t,t,c)\rVert^2\right]
$$

条件に合う画像でのノイズ予測を繰り返し練習することで、条件の意味と画像の構造を結び付けます。予測器の重みを更新し、テキストencoderを固定するか同時に学習するかは設計によります。

### 文章を条件とする生成

訓練画像x₀は渡さず、新しいノイズxTと条件cを用意します。各時刻で同じcを予測器へ渡し、条件に沿った予測を使って状態を更新します。条件付き生成には、内容の対応した学習データが必要です。文章を入力欄に追加するだけで、未学習の対応を自由に扱えるわけではありません。

### Classifier-Free Guidance

CFGを使うための学習では、一部の例で条件を空の条件∅へ置き換え、同じ予測器に条件あり・条件なしの両方を練習させます。生成時には同じxₜとtで両方を予測し、その差を使います。

$$
\hat\varepsilon=\varepsilon_\theta(x_t,t,\varnothing)+s\left[\varepsilon_\theta(x_t,t,c)-\varepsilon_\theta(x_t,t,\varnothing)\right]
$$

この書き方ではs=0が条件なし、s=1が通常の条件付き予測、s>1が条件方向の強調です。合成した予測をサンプラへ渡します。

CFGは別の分類器を使わずに条件への追従を調整する方法です。sを大きくしすぎると、多様性の低下や不自然な画像につながることがあります。条件付き生成そのものとCFGは区別しましょう。

</section>

<section id="sampling" markdown="1">

## 反復によるサンプリング

<figure markdown="1">

{{component:visual-007}}

<figcaption markdown="1">

写真風の猫で段階を表したAI生成の説明図。実際のDDPMの中間出力や、式を数値計算した画像ではありません。生成は新しいノイズから始めます。上の元画像を保存して逆再生する処理ではありません。
</figcaption>
</figure>

最初のxTは、画像と同じ形のランダムなノイズです。予測器が返すε̂をそのまま一度引くだけではなく、サンプラが時刻ごとの係数を使ってxₜを更新します。DDPMでは途中の更新に確率的なノイズも加えます。別のサンプラでは更新式やステップ数が変わります。

生成中は重みθを固定し、変わるのは画像の状態xₜと時刻tです。学習済みの予測器を繰り返し使い、最終的な画像を得ます。生成の速さは、解像度、予測器の大きさ、呼び出す回数などで変わります。

### Latent Diffusion

<figure markdown="1">

{{component:visual-008}}

<figcaption markdown="1">

学習時は画像をAEのencoderで潜在へ変換し、その潜在にノイズを加える。新規生成時は潜在のノイズから開始し、最後にdecoderを使う。
</figcaption>
</figure>

ピクセル空間の高解像度計算を減らすため、あらかじめ学んだAEの潜在表現に拡散過程を適用します。この場合、予測するノイズの形状も潜在と同じです。潜在の各成分はRGB画素ではないため、途中の潜在をそのまま猫の写真として見ることはできません。

</section>

<section id="sources" markdown="1">

## 出典・参考資料

* [DDPM：ノイズ予測による学習と生成 ↗](source:ref-001)
* [Latent Diffusion：潜在空間とcross-attention ↗](source:ref-002)
* [DiT：Transformerを予測器にする ↗](source:ref-003)
* [Classifier-Free Diffusion Guidance ↗](source:ref-004)

</section>
