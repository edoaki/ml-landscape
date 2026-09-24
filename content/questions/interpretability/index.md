---
id: interpretability
title: 説明可能性と内部機構
summary: AIが何を手がかりに、どう判断したかを調べます。画像の説明、判定を変える入力、内部への介入を図で見ていきます。
url: questions/interpretability.html
status: ready
scope: 判断の手がかり・反実仮想・内部機構を図と実例で説明し、個別手法の計算も同じページに置く
prerequisites:
- fundamentals
related: []
origins:
- xai-advanced.html#start
- xai-advanced.html#shapley
- xai-advanced.html#contributions
- xai-advanced.html#gradcam
- xai-advanced.html#counterfactual
- xai-advanced.html#dice
- xai-advanced.html#llm
- xai-advanced.html#arithmetic
- xai-advanced.html#planning
- xai-advanced.html#concepts
- xai-advanced.html#sources
scripts: []
styles: []
english_title: Interpretability and Mechanistic Understanding
---

<section id="start" markdown="1">

## 正解でも、見ている場所は正しいか

猫と答えたモデルが、猫の姿ではなく背景を手がかりにしているかもしれません。**説明可能性（XAI）の研究は、判断の手がかりや仕組みを、人が点検できる形で示します。**正解率だけでは見えない失敗の原因を探すためです。

</section>

<section id="gradcam" markdown="1">

## 判断の手がかりを可視化する

同じ写真に猫と犬がいても、ここで説明するのは**「猫」の予測スコア**です。説明結果の図は、そのスコアを支える場所を色で示しています。

<div class="scene-grid" markdown="1">

<figure markdown="1">
[![猫と犬がいる共通入力](assets/xai-input.png)](assets/xai-input.png)
<figcaption markdown="1">

共通入力。説明する対象は猫。 [画像を拡大 ↗](assets/xai-input.png)
</figcaption>
</figure>

<figure markdown="1">
[![Grad-CAMによる猫を支える場所](assets/xai-gradcam.png)](assets/xai-gradcam.png)
<figcaption markdown="1">

**説明結果：Grad-CAM**モデル内部の画像特徴と、猫スコアの変化しやすさを使って作った図です。黄・橙は猫スコアを支える場所。粗いマップの拡大なので、大まかな位置として読みます。[Grad-CAMの原論文 ↗](source:ref-003) [画像を拡大 ↗](assets/xai-gradcam.png)
</figcaption>
</figure>

</div>

色は予測への影響を表し、人間と同じ理由で猫と判断した証拠ではありません。背景への依存を確かめるなら、背景を替えたときの予測も調べます。

<details markdown="1">

<summary>他の可視化手法と計算条件</summary>

### 同じ予測を別の方法で調べる

説明の色が何を表すかは、手法によって違います。以下も同じ写真・ResNet-18の猫スコアを調べた結果です。

<figure markdown="1">
[![スーパーピクセルへの分割](assets/xai-segments.png)](assets/xai-segments.png)
<figcaption markdown="1">

色や位置が近い画素をまとめた領域。黄色は境界で、重要度ではありません。 [画像を拡大 ↗](assets/xai-segments.png)
</figcaption>
</figure>

<div class="scene-grid" markdown="1">

<figure markdown="1">
[![画素ごとの勾配の大きさ](assets/xai-saliency.png)](assets/xai-saliency.png)
<figcaption markdown="1">

**画素：Saliency**画素を少し変えたとき、猫スコアがどれだけ動くかを微分で調べます。明るいほど敏感な場所です。上げる・下げる方向は区別しません。 [画像を拡大 ↗](assets/xai-saliency.png)
</figcaption>
</figure>

<figure markdown="1">
[![LIME方式による領域の寄与](assets/xai-lime.png)](assets/xai-lime.png)
<figcaption markdown="1">

**領域：LIME方式**領域を隠した画像を多数入力し、スコアを簡単な足し算で近似します。赤は猫スコアを上げる側、青は下げる側の係数です。[LIMEの原論文 ↗](source:ref-002) [画像を拡大 ↗](assets/xai-lime.png)
</figcaption>
</figure>

</div>

<details markdown="1">

<summary markdown="1">

計算条件・再現用データ
</summary>

Grad-CAM論文の原写真、ResNet-18（IMAGENET1K_V1）、クラス281のsoftmax前スコア。LIME方式は38領域・黒塗り1024例のRidge近似（R²=0.83）。

[再現用コード ↗](docs/legacy-python/source/xai_image_results.py) · [計算条件 ↗](assets/xai-results.json) · [数値データ ↗](assets/xai-attributions.npz) · [モデル出典 ↗](source:ref-004)

</details>

</details>

<details markdown="1">

<summary>寄与を数値で分ける：Shapley値・SHAP・寄与度分解</summary>

<section id="shapley" markdown="1">

### Shapley値による寄与の評価

**部品を止めたときの性能低下から、その役割を調べます。**ただし、他にどの部品が動いているかで下がり幅は変わります。

<figure markdown="1">

{{component:visual-001}}

<figcaption markdown="1">

架空の性能。停止時は出力を0にし、再学習しない。この比較を除去順を変えて繰り返す。
</figcaption>
</figure>

Shapley値は、**部品を取り除く順番を変え、その部品を止めた瞬間の性能差を平均**します。多くの部品がある場合は、順番を抽出して近似します。

### 入力特徴の寄与

部品の代わりに入力の特徴を隠せば、どの特徴が予測を支えたかを調べられます。1件の予測スコアの差を各特徴に配分する代表例が**SHAP**です。

<figure markdown="1">

{{component:visual-002}}

<figcaption markdown="1">

架空の迷惑メールスコア（確率ではない）。ここでは「隠す」を「なし」に置き換える。3行は単独の比較で、SHAPでは除去順を変えて平均する。
</figcaption>
</figure>

[Lundberg & Lee（2017）：SHAP ↗](source:ref-001)

</section>

<section id="contributions" markdown="1">

### 寄与度分解

**予測スコアが、どの入力からどれだけ来たかを分けます。**計算のつながりを、出力から入力へ逆向きにたどります。

<figure markdown="1">

{{component:visual-003}}

<figcaption markdown="1">

バイアス・非線形処理のないNN、基準入力は0。橙は寄与を戻す向き（学習ではない）。
</figcaption>
</figure>

同じ入力へ戻った値を足すと、その入力の寄与になります。非線形なNNでは、寄与を配るルールも必要です。

</section>

</details>

</section>

<section id="counterfactual" markdown="1">

## 判定を変える入力を探す

反実仮想は、**どこを変えれば別の判定になるか**を示す説明です。今度は顔画像を例に、顔らしさを保ちながら、金髪スコアが上がるように画像を少しずつ変えます。

<figure markdown="1">

{{component:visual-004}}

<figcaption markdown="1">

モデルは固定し、入力側を変えて再予測する。
</figcaption>
</figure>

<figure markdown="1">
[![元画像、再構成、金髪へ変更、差分の四列](assets/counterfactual.png)](assets/counterfactual.png)
<figcaption markdown="1">

著者公開のCelebA / Glowの結果。左から元画像、再構成、金髪へ変更、画素差分。髪以外も変わりうる。 [画像を拡大 ↗](assets/counterfactual.png)
</figcaption>
</figure>

[Dombrowski et al.：著者実装・結果 ↗](source:ref-005)


画像を壊して判定だけ変えても、役立つ説明にはなりません。元の内容をなるべく保ち、変えてよい特徴を決めて探します。

<details markdown="1">

<summary>変更案を複数出す：DiCE</summary>

<section id="dice" markdown="1">

### 複数の反実仮想の生成

**変更案が複数あれば、実行しやすい案を選べます。**DiCEでは、同じ判定に至る異なる変更案を探します。図では「年収を増やす」と「希望額を減らす」を比べます。

<figure markdown="1">

{{component:visual-005}}

<figcaption markdown="1">

DiCEの考え方を示す架空の審査例。棒は金額を同じ尺度で表示。実際の審査基準やDiCEの実験結果ではない。
</figcaption>
</figure>

「年齢は固定」など、変更できる項目を指定できます。モデル上の判定変更を示すもので、現実の実行可能性は別に考えます。

[DiCE：著者解説 ↗](source:ref-006)

</section>

</details>

</section>

<section id="llm" markdown="1">

## 内部の計算へ介入する

ニューラルネットワークは、入力を何段階もの数値の表現へ変換して答えを作ります。**内部機構の研究では、途中の活動を変え、出力がどう変わるかを調べます。**よく反応する部分を見つけるだけでなく、判断に使われているかを確かめるためです。

言語モデルでも、生成した「理由」が内部の計算をそのまま表すとは限りません。次は加算を調べた例です。図の部品は、解析で見つけた特徴群を働きごとにまとめています。

<section id="arithmetic" markdown="1">

### 加算の内部処理

**一の位を扱う部分と、答えの大まかな大きさを絞る部分が並行して働きます。**2025年のClaude 3.5 Haikuで見つかった例です。

<figure markdown="1">

{{component:visual-006}}

<figcaption markdown="1">

Lindsey et al.（2025）を簡略化。灰色の配線は説明用で、実測の回路図ではない。「92の近く」は粗い特徴を表す。
</figcaption>
</figure>

本人に聞くと筆算を説明しますが、解析された内部計算とは異なりました。**生成した説明と、実際の計算は一致するとは限りません。**

[Lindsey et al.（2025）：Addition ↗](source:ref-007)

</section>

<details markdown="1">

<summary>ほかの研究例：詩の計画と多言語の意味表現</summary>

<section id="planning" markdown="1">

### 詩の生成と計画

1行目の末尾は**grab it**。これと韻を踏む2行目を作る課題です。まだ2行目を書いていない段階で、末尾候補**rabbit**の特徴が活動していました。

<figure markdown="1">

{{component:visual-007}}

<figcaption markdown="1">

Anthropic（2025）。無介入の英文は報告例。他の2文は内容の要約。greenへの操作は韻を崩すこともある。
</figcaption>
</figure>

[Anthropic（2025）：Claude 3.5 Haikuの詩の計画 ↗](source:ref-008)

</section>

<section id="concepts" markdown="1">

### 多言語間の意味表現

**英語・フランス語・中国語で反対語を尋ねると、共通の意味の処理が見つかりました。**答えの表記は、言語ごとの処理で選びます。

<figure markdown="1">

{{component:visual-008}}

<figcaption markdown="1">

Lindsey et al.（2025）の模式図。意味の処理を共有しつつ、言語ごとの表記を選ぶ。
</figcaption>
</figure>

[Lindsey et al.（2025）：Claude 3.5 Haikuの多言語回路 ↗](source:ref-009)

</section>

</details>

</section>

<section id="evaluation" markdown="1">

## 説明をどう確かめるか

見やすい説明でも、モデルの振る舞いに合っているかを確認する必要があります。示された特徴を変えると予測が変わるか、似た入力でも説明が安定するか、説明を使って人が誤りを発見できるかを調べます。

内部への介入も、一つの部品を止めた結果だけで役割を決めきれるとは限りません。別の部品が補うこともあるため、条件を変えて確かめます。

</section>

<section id="sources" markdown="1">

## 出典・参考資料

* [SHAP ↗](source:ref-001)
* [LIME ↗](source:ref-002)
* [Grad-CAM ↗](source:ref-003)
* [顔画像の反実仮想 ↗](source:ref-005)
* [DiCE ↗](source:ref-006)
* [LLMの算術・多言語 ↗](source:ref-009)
* [LLMの詩の計画 ↗](source:ref-008)

</section>

