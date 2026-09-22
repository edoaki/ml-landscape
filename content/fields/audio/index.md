---
id: audio
title: 音声・音楽
summary: 話し声から文字へ、文章から音声や音楽へ、混ざった曲から一つの音へ。入力と出力を、短い試聴デモで比べます。
url: fields/audio.html
status: migrated
scope: 認識、合成、生成、分離
prerequisites: []
related: []
origins:
- audio.html#tasks
- audio.html#asr
- audio.html#tts
- audio.html#music
- audio.html#listen
- audio.html#representation
- audio.html#sources
- research.html#signals / Demucs｜混合音から音源を取り出す
scripts:
- content/fields/audio/components/audio.js
styles:
- content/fields/audio/components/page.css
english_title: Speech, Audio and Music
---

<section id="tasks" markdown="1">

## 音声・音楽のタスク

音声・音楽の研究には、言葉の認識、音の生成、音源の分離などがあります。

<div class="table-scroll" tabindex="0" markdown="1">

| タスク | 入力 → 出力 | 身近な用途 |
| --- | --- | --- |
| [音声認識（ASR）](page:audio#asr) | 話し声 → 文字列 | 会議の文字起こし・字幕 |
| [音声合成（TTS）](page:audio#tts) | 文章 → 話し声 | 案内の読み上げ |
| [音楽生成](page:audio#music) | 曲の説明・旋律 → 音楽 | 映像に合うBGM |
| [音源分離](page:audio#listen) | 混ざった音 → 音源ごとの波形 | 歌声と伴奏を取り出す |

</div>

</section>

<section id="asr" markdown="1">

## 音声認識

音声認識（ASR）は、話された言葉を文字にします。会議の文字起こしや字幕に使われます。

<div class="compare" markdown="1">

<div class="audio-sample" markdown="1">

### 入力：短い案内

{{component:visual-001}}

</div>

<div class="audio-sample" markdown="1">

### 対応する文章（例）

明日の会議は、午後三時からです。
{.audio-transcript}

</div>

</div>

Whisperなどが代表例です。雑音の中でも正確に聞き取ることや、多言語への対応が研究されています。

[Whisperの研究紹介・公開例 ↗](source:ref-001)

</section>

<section id="tts" markdown="1">

## 音声合成

音声合成（TTS）は、文章から話し声を作ります。発音だけでなく、抑揚や間の取り方も自然にすることが研究されています。Tacotron 2の合成音声と、同じ文章を人が読んだ録音の例です。

入力：George Washington was the first President of the United States.  
（ジョージ・ワシントンはアメリカ合衆国の初代大統領でした。）

<div class="compare" markdown="1">

<div class="audio-sample" markdown="1">

### 合成音声：Tacotron 2

{{component:visual-002}}

</div>

<div class="audio-sample" markdown="1">

### 人の音声：録音

{{component:visual-003}}

</div>

</div>

出典：[Tacotron 2 著者公開サンプル ↗](source:ref-002)

</section>

<section id="music" markdown="1">

## 音楽生成

音楽生成は、楽器や雰囲気の説明から曲を作ります。以下はMusicGenの生成例です。

<div class="compare" markdown="1">

<div class="audio-sample" markdown="1">

### ① ダンス系の曲

指示（要約）：南国風の打楽器と、覚えやすい旋律を持つ明るいダンスポップ。

{{component:visual-004}}

</div>

<div class="audio-sample" markdown="1">

### ② オーケストラの曲

指示（要約）：力強い打楽器、金管と弦楽器を使った、英雄的な戦いを思わせる壮大な曲。

{{component:visual-005}}

</div>

</div>

指示に合う曲を作ることや、長い曲の展開を自然につなぐことが研究されています。

出典：[MusicGen著者試聴ページ ↗](source:ref-003)

</section>

<section id="listen" markdown="1">

## 音源分離

音源分離は、混ざった音から歌声や楽器を取り出します。下のデモは、曲全体・旋律・伴奏の対応を示しています。

<figure markdown="1"><div class="figure-scroll" tabindex="0" markdown="1">

![8秒の旋律と伴奏。旋律は上下し、伴奏は低い位置で反復する。](media:audio-score.svg){.diagram-image}

</div>

<figcaption markdown="1">

旋律と伴奏の音の配置。
</figcaption>
</figure>

{{component:visual-006}}

{{component:visual-007}}

分離の目標を聞くデモ：混合前の旋律・伴奏を切り替えています。

Demucsなどは、重なった歌声や楽器を推定して分けます。他の音の混入や、取り出した音の欠けを減らすことが研究されています。

[Demucsの実際の分離結果を聞く（著者公開デモ） ↗](source:ref-004)

<details markdown="1">
<summary>研究例：Demucsの分離結果</summary>

Demucsの研究では、波形とスペクトログラムを組み合わせるなどして楽曲を分離します。教材の切り替えデモと違い、混合音だけから各音源を推定した結果です。著者の試聴例では、他音源の漏れと、取り出した音の歪みに耳を向けます。

[Demucs：著者実装・試聴先](source:ref-005)

</details>

</section>

<section id="representation" markdown="1">

## 波形とスペクトログラム

音声認識や音源分離のモデルは、音を数値として扱います。その代表的な表し方が波形とスペクトログラムです。下の図は、同じ8秒の曲をそれぞれの形式で表したものです。

{{component:visual-008}}

### 波形

音を時間ごとの振幅で表したものです。音が強く出るタイミングや、振動の様子が分かります。

<figure markdown="1">
[![上は8秒の混合曲の波形。下は1.02秒から1.06秒の振動を拡大。横軸は時間、縦軸は振幅。](media:audio-waveform.png)](media:audio-waveform.png)
<figcaption markdown="1">

上：曲全体の波形。下：40ミリ秒の拡大。 [画像を拡大 ↗](media:audio-waveform.png)
</figcaption>
</figure>

### スペクトログラム

音を短く区切って周波数成分を調べ、強さを色で表します。横は時間、縦は周波数で、明るいほどその成分が強いことを示します。

<figure markdown="1">
[![同じ8秒の曲のスペクトログラム。下部に低い伴奏、中央に上下する旋律、その上に倍音が見える。](media:audio-spectrogram.png)](media:audio-spectrogram.png)
<figcaption markdown="1">

同じ曲から計算。低い位置に伴奏、中央に上下する旋律、その上に倍音が見える。 [画像を拡大 ↗](media:audio-spectrogram.png)
</figcaption>
</figure>

波形では重なって見える音も、周波数ごとに分けると高さや音色の特徴を捉えやすくなります。そのため、音声認識や音源分離などのモデルへの入力に使われます。

</section>


<section id="sources" markdown="1">

## 出典・参考資料

* [短時間フーリエ変換とスペクトログラム（SciPy公式資料） ↗](source:ref-006)
* [Tacotron 2 原論文 ↗](source:ref-007)
* [Whisper 原論文 ↗](source:ref-008)
* [MusicGen 原論文 ↗](source:ref-009)
* [Demucs 著者実装 ↗](source:ref-005)

</section>
