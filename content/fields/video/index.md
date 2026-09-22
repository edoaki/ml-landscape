---
id: video
title: 動画理解・生成
summary: 動画では、一枚の画像の内容に加えて、時間に沿った変化を扱います。対象の追跡、画素の動き、動画の生成を、既存の研究結果と映像で見ていきます。
url: fields/video.html
status: migrated
scope: 時間的な変化、追跡、フロー、動画生成
prerequisites: []
related: []
origins:
- spatial.html#video
- spatial.html#optical-flow
- spatial.html#video-generation
- spatial.html#sora
- spatial.html#genie
- research.html#seeing / SAM 2｜指定した対象を、動画の中で追う
scripts:
- content/fields/video/components/spatial.js
styles:
- content/fields/video/components/page.css
english_title: Video Understanding and Generation
---

<section id="video" markdown="1">

<span id="sam2"></span>

## 対象の追跡

**追跡**では、動いたり隠れたりする対象を、動画の中で引き続き見つけます。SAM 2はその一例で、指定した対象の領域を各フレームで推定します。元画像と、2人の服にマスクを付けた結果です。

<div class="spatial-frame-viewer" role="region" aria-label="SAM 2のフレーム切り替え" tabindex="0" markdown="1">

<div class="spatial-sam-pair" markdown="1">

{{component:visual-001}}

{{component:visual-002}}

</div>

<div class="spatial-frame-controls" markdown="1">

{{component:visual-003}}

<span class="frame-status">1 / 7 · frame 0</span>

{{component:visual-004}}

</div>

</div>

左右の矢印で、元画像と結果が同時に切り替わります。赤と緑が追跡対象の服の領域です。動いたり一部が隠れたりしても、対象の見えている部分にマスクを付けるタスクです。

出典：[SAM 2公式ノートブックの複数対象の追跡結果 ↗](source:ref-001)。保存済み出力を無加工で引用。

SAM 2は過去のフレームの情報を使って、指定した対象の領域を追います。

<figure markdown="1">
[![SAM 2の著者が公開したSA-Vデータセットの動画フレームと物体マスクの例](assets/sam2-result.jpg)](assets/sam2-result.jpg)
<figcaption markdown="1">

著者実装のSA-Vデータセット紹介図。色は対象のマスク。データセットの例示であり、この図全体をモデルの予測精度の証拠とは扱わない。 [画像を拡大 ↗](assets/sam2-result.jpg)
</figcaption>
</figure>

[SAM 2：著者実装・結果 ↗](source:ref-005) · [外部の操作デモ ↗](source:ref-006)

</section>

<section id="optical-flow" markdown="1">

<span id="raft"></span>

## 画素の動きの推定

**オプティカルフロー**は、画像の各位置が次の画像でどちらへどれだけ動いたかを表します。RAFT（ECCV 2020）は、2枚の画像からその動きを推定する研究例です。下はKITTIテストセットでの入力画像と推定結果です。

<div class="spatial-raft-pair" markdown="1">

<figure markdown="1">
[![RAFTへの入力画像。道路上を車が走る場面。](assets/raft-input.png)](assets/raft-input.png)
<figcaption markdown="1">

元画像 [画像を拡大 ↗](assets/raft-input.png)
</figcaption>
</figure>

<figure markdown="1">
[![同じ場面のRAFTによるオプティカルフロー。](assets/raft-output.png)](assets/raft-output.png)
<figcaption markdown="1">

RAFTの結果 [画像を拡大 ↗](assets/raft-output.png)
</figcaption>
</figure>

</div>

出典：Teed & Deng, [RAFT, Figure 4（PDF p.10） ↗](source:ref-002)の左下の例。前方の車と背景の動きが、異なる色で表されています。

色は画素の動きの方向と大きさを表します。同じ色でも「同じ人物」という意味ではありません。人物だけでなく背景にも色が付くのは、カメラの動きでも画面上の位置が変わるためです。

</section>

<section id="video-generation" markdown="1">

## 動画生成

動画を作るには、1枚の画像の見た目だけでなく、**ものがどう動き、場面が時間とともにどう変わるか**も学ぶ必要があります。人が歩くと姿勢が変わり、車が進むと周囲の景色も変わります。動画生成モデルは、多くの映像からこうした変化のパターンを学習します。

Soraは文章に合った映像を生成し、Genie 3はユーザーの操作に応じて、その先の映像を生成します。後者のような**行動に応じた環境変化を予測する世界モデル**は、候補行動の結果を考える手がかりにもなります。ただし、映像を生成できるだけで、行動の結果や物理法則を正確に予測できるとは限りません。

</section>

<section id="sora" markdown="1">

### 文章からの動画生成：Sora

<figure markdown="1">

{{component:visual-005}}

<figcaption markdown="1">

[Sora：Tokyo walk（2024） ↗](source:ref-003)。公式の生成映像から冒頭15秒を抜粋。
</figcaption>
</figure>

「ネオンが光る夜の東京を、黒いジャケットと赤いドレスの女性が歩く」という文章から生成。人物の歩行と、移り変わる街並みを一つの映像にしています。

</section>

<section id="genie" markdown="1">

### 操作に応じた生成：Genie 3

**ユーザーの入力に合わせて、次の画面を予測し続ける。**

<figure markdown="1">

{{component:visual-006}}

<figcaption markdown="1">

[Genie 3：Backyard racetrack ↗](source:ref-004)。公式の操作デモ映像。
</figcaption>
</figure>

今の画面と操作、それまでの履歴から次の画面を生成します。例えば、車を右に曲げる操作をすると、車の向きと周囲の景色が変わります。生成した画面をもとに次の操作へ応答することを繰り返すので、ゲームのように動かせます。

あらかじめ用意した3D物体を物理エンジンで動かす方式とは異なり、操作に応じた映像そのものを生成しています。ここに掲載しているのは、その操作結果を記録した動画です。

</section>






## 参考資料 {#inherited-sources}

* [RAFT 著者実装 ↗](source:inherited-ref-007)
