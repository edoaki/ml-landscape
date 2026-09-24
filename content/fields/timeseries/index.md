---
id: timeseries
title: 時系列
summary: 電力需要と設備の温度を例に、未来の予測、異常検知、変化点検出、欠測補完を比べます。時間の順序によって使える情報が変わることも説明します。
url: fields/timeseries.html
status: migrated
scope: 予測、異常検知、変化点、欠測補完
prerequisites:
- learning
related: []
origins:
- time-graphs.html#series
- time-graphs.html#forecast
- time-graphs.html#anomaly
- time-graphs.html#change
- time-graphs.html#missing
- time-graphs.html#series-evaluation
- time-graphs.html#sources
- research.html#signals / TimesFM｜多様な系列で事前学習する
- research.html#signals / Merlion｜異常スコアと評価をつなぐ
scripts:
- content/fields/timeseries/components/timeseries.js
styles:
- content/fields/timeseries/components/page.css
english_title: Time Series
---

<section id="series" markdown="1">

## 時系列のタスク

時系列は、時間の順に並ぶデータです。例えば1時間ごとの電力需要や、設備の温度です。同じ温度の記録でも、未来の値を知りたいのか、今の異常に気付きたいのかで、解く問題が変わります。

<div class="table-scroll" tabindex="0" markdown="1">

| タスク | 入力 → 出力 | 具体例 |
| --- | --- | --- |
| [将来予測](page:timeseries#forecast) | 過去の観測 → 未来の数値 | 明日の電力需要を見積もる |
| [異常検知](page:timeseries#anomaly) | 観測 → 普段からの外れ具合・警報 | 設備の急な温度上昇に気付く |
| [変化点検出](page:timeseries#change) | 観測 → 振る舞いが変わった時刻 | 運転モードの切り替わりを見つける |
| [欠測補完・状態推定](page:timeseries#missing) | 不完全な観測 → 欠けた値・隠れた状態 | センサの通信切れを補う |

</div>

</section>

<section id="forecast" markdown="1">

## 電力需要の予測

入力は昨日の24時間の電力需要、出力は今日の24個の予測値です。夜に下がり、夕方に上がる形があります。まず「昨日の同じ時刻を使う」と「昨日の最後の値を使う」を切り替え、今日の予測線がどう変わるかを見てください。

<figure class="ts-demo" id="ts-forecast" markdown="1">

{{component:visual-001}}

<figcaption markdown="1">

教材用の合成データ。2つの単純な基準予測をその場で計算します。学習済みの深層モデルの推論ではありません。JavaScript無効時も、昨日と同じ時刻を使う予測を表示します。
</figcaption>
</figure>

「今日の実測を表示」を押すと、隠していた正解と予測を比べられます。MAE（平均絶対誤差）は、各時刻のずれの大きさを平均した値で、小さいほどよく当たっています。この例では昨日と似た一日の形が続くため、同じ時刻を使う方法が有利です。休日や急な天候変化で形が変われば、同じ方法でも外れます。

深層学習でも「過去を入力し、未来と比べて学ぶ」という枠組みは共通です。[RNN](page:rnn)や[Transformer](page:transformer)などで、多数の系列から傾向や周期を学べます。予測時点で分かっている曜日や天気予報を加えることもあります。

<section id="research-5" markdown="1">

### TimesFMによる時系列予測

<figure markdown="1">
[![TimesFM原論文Figure 4のDartsとMonashの系列の予測例](media:timesfm-result.png)](media:timesfm-result.png)
<figcaption markdown="1">

Das et al.（ICML 2024）, Figure 4を引用。下段は将来の予測区間の拡大。青の正解系列と橙のTimesFM予測が、どこで一致し外れるかを見る。 [画像を拡大 ↗](media:timesfm-result.png)
</figcaption>
</figure>

2024年のTimesFMは、時系列を短い時間のまとまりに分けて扱うモデルを、多様な系列で事前学習する研究です。目的ごとにゼロから学ぶ場合と比べ、既に得た時系列の知識を新しい系列へ使えるかを問います。図の縦の境界より右は入力に混ぜず、将来の正解と予測を比べます。

[TimesFM：2024年の原論文 ↗](source:ref-001) · [著者実装（複数の版あり） ↗](source:ref-002)

</section>

</section>

<section id="anomaly" markdown="1">

## 異常検知と閾値

設備の温度は普段50℃前後ですが、13時間目だけ急に上がりました。ここでは「50℃との差の絶対値」を異常スコアとし、しきい値を超えた点に赤い丸を付けます。しきい値を1℃、10℃、25℃へ動かしてみてください。

<figure class="ts-demo" id="ts-sensor" markdown="1">

{{component:visual-002}}

<figcaption markdown="1">

教材用の合成温度と、固定した基準からの偏差による検知。故障を診断するモデルではありません。JavaScript無効時は、一瞬の上昇の観測図を表示します。
</figcaption>
</figure>

低くすると小さな揺れにも警報が出ます。高くしすぎると大きな上昇も見逃します。実際の異常検知では、時刻や運転条件に応じた予測からのずれなどを使い、別の検証データでしきい値を決めます。スコアが大きいだけで、故障の原因まで分かるわけではありません。

<section id="research-6" markdown="1">

### Merlionによる異常検知

<figure markdown="1">
[![Merlion著者実装の異常検知の出力例](media:merlion-result.png)](media:merlion-result.png)
<figcaption markdown="1">

Merlion公式READMEの異常検知図を引用。黒は観測値（左軸）、赤い線は異常スコア（右軸）、赤い帯は異常区間。両軸の尺度が違うことに注意。 [画像を拡大 ↗](media:merlion-result.png)
</figcaption>
</figure>

Merlionは単一のニューラルネットワーク名ではなく、時系列の異常検知・予測などを扱うフレームワークです。検出した区間が実際の異常と重なるか、遅れや誤警報がないかを見ます。前処理・閾値・評価の統一も研究や検証を支える仕事です。

[Merlion：著者実装とチュートリアル ↗](source:ref-003)

</section>

</section>

<section id="change" markdown="1">

## 変化点検出

上のデモを「上がったまま続く」に切り替えてください。13時間目から温度が約70℃になり、それ以降も高い状態が続きます。異常検知は各観測に警報を出しますが、変化点検出が答えたいのは「いつから普段の状態が変わったか」です。

<div class="table-scroll" tabindex="0" markdown="1">

| 同じセンサの例 | 異常検知で見るもの | 変化点検出で見るもの |
| --- | --- | --- |
| 一瞬だけ上がる | 13時間目の大きなずれ | すぐ元に戻り、持続する切り替わりとは異なる |
| 上がったまま続く | 13時間目以降の大きなずれ | 13時間目付近で平均の水準が変わったこと |

</div>

このデモの切り替わりは教材で設定した正解で、変化点を推定するアルゴリズムは実行していません。実際には複数の観測を集めて変化を判断するため、変化した時刻と検知できた時刻はずれることがあります。意図した運転モード変更なら、変化があっても故障ではありません。

</section>

<section id="missing" markdown="1">

## 欠測補完

通信切れで12時の温度が欠けたとします。前後の値の間を直線でつなぐと、12時を51℃と補えます。これは観測値ではなく推定値です。

<div class="table-scroll" tabindex="0" markdown="1">

| 時刻 | 11時 | 12時 | 13時 |
| --- | --- | --- | --- |
| 入力の記録 | 50℃ | 欠測 | 52℃ |
| 前後を使った補完 | 50℃ | 51℃（推定） | 52℃ |

</div>

13時まで記録した後の補完なら、前後の値を使えます。一方、12時の時点で判断するなら13時の観測はまだ使えません。状態推定では、ノイズのある観測から、直接見えない設備内部の温度などを推定します。[状態空間モデル](page:ssm)の「状態を更新する」考え方につながります。

</section>

<section id="series-evaluation" markdown="1">

## 時系列の評価設計

例えば1〜7月で学習し、8月で方法やしきい値を選び、9月を最後の評価に残します。隣り合う時刻をランダムに混ぜると、実際の未来予測より簡単な条件になる場合があります。正規化の平均なども、学習期間だけから計算します。

予測では時間帯ごとの誤差や、予測を何時間先まで伸ばすかを見ます。異常検知では誤警報・見逃し・検知の遅れを見ます。ほとんど正常な設備では「すべて正常」と答えても正解率が高くなるため、正解率だけでは評価できません。

</section>

{{component:visual-003}}

<section id="sources" markdown="1">

## 出典・参考資料

* [TimesFM 著者実装 ↗](source:ref-002)
* [Merlion 著者実装・チュートリアル ↗](source:ref-003)

</section>
