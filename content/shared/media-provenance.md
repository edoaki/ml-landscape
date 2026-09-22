# 素材と出典

> 2026-09-22: 開発環境はNode.js＋npmへ移行済みです。以下のPythonコマンド・ファイル名は過去の制作記録で、旧コードはリポジトリの `docs/legacy-python/` に保管しています。現在の手順はプロジェクトREADMEを参照してください。

確認・取得日：2026-09-12。素材はローカル保存し、外部サービスが停止しても本文を読めるようにしています。

## 著者・公式の公開結果

研究結果を説明・比較するための引用図には、本文で出典と読み方を添えています。原著者・各データセットの権利は保持されます。論文図や第三者の写真を、教材のオリジナル素材として扱いません。ソフトウェアのライセンスと、論文中の写真・データの利用条件は別に扱います。

| ファイル | 元資料・対象 | 抜粋・表示・条件 |
|---|---|---|
| `gradcam-original.png`, `gradcam-cat.png`, `gradcam-dog.png` | [Selvaraju et al., Grad-CAM](https://arxiv.org/abs/1610.02391), PDF p.3, Figure 1 (a), (c), (i) | 三つの小図を切り出し。VGG-16のcat/dogを対象にした結果。元写真はタスク比較の共通入力にも使用。解説用の枠・マスク・深度は別の模式図として明記。 |
| `counterfactual.png` | [Dombrowski et al. 著者実装](https://github.com/annahdo/counterfactuals/blob/main/results/overview_CelebA_img_1_z_Glow_save_at_0.99.png) | CelebA、Glow、髪色の二値分類器、目標クラスの確信度0.99。未加工の結果図。方法は[2021年7月23日著者資料](https://gapindnns.github.io/downloads/slides/2021-07-23-jan-gerken.pdf)のPDF p.11–13・20で確認。公開実装は後続研究も含むため2021年論文の図番号を付けない。リポジトリのApache-2.0本文は`counterfactual-license.txt`。 |
| `induction-original.png` | [Olsson et al. (2022), Key Concepts](https://transformer-circuits.pub/2022/in-context-learning-and-induction-heads/index.html) | 本文最初のinduction headの挙動図。埋め込み画像を未加工で保存。以前のXAIページで使用した素材として保存。現在のページでは使用しない。 |
| `dino-supervised.png`, `dino-self-supervised.png` | [Caron et al. (2021), Figure 4](https://arxiv.org/html/2104.14294v2#S4.F4) | 同じ画像の教師あり/DINOの小図。ViT-S/8、Attention質量60%の閾値処理、最良head。ファイル名は`fig4-sup-857mask-head1.png`と`fig4-dino-857mask-head2.png`。 |
| `depth-input.jpg`, `depth-result.jpg` | [Depth Anything V2 著者ページ](https://depth-anything-v2.github.io/) | `static/images/compare_v1_detail/17943623232_5f974cad30_k_img.jpg`と同じ接頭辞の`_v2.jpg`。著者のdetail comparisonを一組引用。モデルサイズや距離の尺度を推測しない。 |
| `sam2-result.jpg` | [SAM 2のSA-Vデータ例](https://github.com/facebookresearch/sam2/blob/main/assets/sa_v_dataset.jpg) | データセットのマスクの紹介図。モデルの推論精度を示す図とはしない。リポジトリのApache-2.0本文は`sam2-license.txt`。 |
| `pose-result.png` | [MediaPipe Pose Landmarker公式ガイド](https://ai.google.dev/edge/mediapipe/solutions/vision/pose_landmarker) | `/static/mediapipe/images/solutions/examples/pose_detector.png`。公式ガイド掲載の結果例。ガイドは特記のないコンテンツをCC BY 4.0とする。カメラの利用や新規推論はしていない。 |
| `timesfm-result.png` | [Das et al., ICML 2024, Figure 4](https://arxiv.org/html/2310.10688v3) | `visualization-4p-darts-monash.png`。Darts・Monashの予測例、下段は将来区間の拡大。リポジトリ最新モデルの性能図とはしない。 |
| `merlion-result.png` | [Merlion公式READMEの異常検知例](https://github.com/salesforce/Merlion/blob/main/figures/anom_example.png) | 黒い観測値と赤い異常スコアは別の縦軸。赤帯は異常区間。実行・再生成はしていない。リポジトリライセンスは`merlion-license.txt`。 |
| `nerf-result.mp4` | [NeRF著者ページ](https://www.matthewtancik.com/nerf)からリンクされた[colorspout映像](https://cseweb.ucsd.edu/~viscomp/projects/LF/papers/ECCV20/nerf/website_renders/colorspout_200k_rgb.mp4) | 公開された新規視点合成の短い映像を引用。ポスターは0.5秒のフレーム。著者ページの同映像のGoogle Storageミラーは404だったため、同ページ掲載の著者大学サーバを使用。 |
| `rt2-result.mp4` | [RT-2著者ページ](https://robotics-transformer2.github.io/)の`videos/rt2_teaser.mp4` | 公開のロボット操作映像。ポスターは2秒のフレーム。動画は未加工。実験全体の成功率を示すものではない。 |
| `alphafold-P69905-v6.pdb` | [AlphaFold DB：P69905](https://alphafold.ebi.ac.uk/entry/P69905), [PDB](https://alphafold.ebi.ac.uk/files/AF-P69905-F1-model_v6.pdb) | データベースAPIでv6を確認し保存。AlphaFold DBのCC BY 4.0の構造データ。PDBのCα座標とpLDDT（B-factor欄）を抽出。142残基。実験構造ではない。 |
| `protein.svg`, `protein-data.js` | 上記AlphaFoldデータ | 教材側で中心化・正射影・Cα同士を接続。色はpLDDT。表示の回転は座標変換のみ。 |

Grad-CAMの小図はPDFから切り出したもので、推論を再現した結果ではありません。図そのものの説明が主となるページに出典付きで配置しています。

## 教材オリジナルの図・音

- 画像タスクの比較図：`source/vision.py`で生成しHTMLへ埋め込む。2台の車と空・草地・道路の共通場面を用い、分類・回帰・検出と3種類のセグメンテーションを説明する。入力とマスクは同じ輪郭を共有する教材用の模式図。深度は既存の`depth-input.jpg`・`depth-result.jpg`を使用。旧`task-comparison.svg`は廃止。
- `convolution.svg`：4×4の固定入力と2×2のフィルタの積和。バイアス0、stride 1、padding 0。
- `attention-matrix.svg`：固定スコアの行softmaxと因果マスク。
- `rnn-unroll.svg`：状態と入出力・重み共有の関係。
- `latent.svg`：固定した平均・分散から描いた潜在の模式図。seed 6。
- `flow-density.svg`：`(u,v) → (u, exp(0.4u) v + 0.6 sin(2u))`で可逆変換した格子と点群。seed 11。
- `diffusion-stages.svg`：手作り8×8数字とseed 10のガウスノイズ。信号とノイズの係数を変えた計算図。表示の濃淡はクリップ。
- `transport.svg`：seed 2の始点と円周上の終点を直線経路で結ぶ20ペア。学習済み速度場ではない。
- `timeseries.svg`, `reliability.svg`：教材用の合成系列・概念曲線。学習済みモデルの精度を示す値ではない。
- `routing.svg`：固定した6都市の2経路を描画し、ユークリッド距離を合計。
- `pose.svg`：関節点の出力を説明する模式図。
- `mix.wav`, `low.wav`, `high.wav`：220 Hzと660 Hzの合成音。16 kHz、16 bit、モノラル、2.4秒。端をフェード。元成分を並べる例で、学習モデルによる分離結果ではない。
- 各HTML内の構造SVG：本文に対応した教材オリジナル。GCN・GAT・GraphSAGEは同じ6ノードと特徴を使用。GCNとGATでは自己ループを表示。

再生成元は`source/assets.py`・`source/detail_figures.py`・`source/protein.py`と各本文です。外部の重み・学習データセット全体は同梱していません。

## CNNの追加図と操作（2026-09-12）

CNNの特徴マップ図と3段のU-Net図は、ユーザー提供の参照画像を構成の参考にして、教材用に新規作図したインラインSVG。参照画像自体やキャラクター素材の転載はしていない。生成元は`source/cnn_figures.py`。画像サイズ・チャネル数・確率は説明用の設定。

畳み込みの操作も同ファイルの固定4×4入力と2×2フィルタを使う。`assets/app.js`でpadding・strideと2×2の最大/平均poolingを計算する。stride=1・padding=0が初期状態で、ReLUや学習処理は実行しない。

## 数式組版

`katex.css`・`../source/katex.min.js`は[KaTeX 0.16.22](https://github.com/KaTeX/KaTeX/releases/tag/v0.16.22)の配布版（JS・CSS・フォント）。npm公式配布物 `https://registry.npmjs.org/katex/-/katex-0.16.22.tgz` から取得。MITライセンス本文は`katex-LICENSE.txt`。CSSのフォントURLは同じ配布版のWOFF2データを埋め込む形へ変更し、既存の教材サーバーとファイルを直接開く場合の両方で表示できます。JSはビルド時だけ使用し、閲覧時は同梱CSS・フォントと生成済みHTML・MathMLを使います。

## RNN・LSTM・GRUの構造図（2026-09-12）

`source/rnn_figures.py`が生成するインラインSVG。ユーザー提供の3枚の参照画像を構成の参考に、RNNのループと時間展開、1ステップの計算、LSTM・GRUの内部経路を教材用に新規作図した。日本語のラベルと記号の凡例を付け、本文の式と対応させている。LSTMは忘却ゲートを含む標準形をPyTorch公式ドキュメントと対応させ、GRUはCho et al. (2014)の式(5)〜(8)と同じくzを過去を残す割合とする。参照画像のファイルそのものは配布物に含めない。

### Transformerの説明図（2026-09-12）

- `source/transformer_figures.py`で本文内SVGを新規作図。ユーザー提供の7枚の参考画像から、点群による表現更新、要素間の情報交換と要素内のFFN、Q・K・Vと集約の説明方法を参考にした。画像そのものの転載・切り抜きは行っていない。
- 構造と計算は[Attention Is All You Need](https://arxiv.org/abs/1706.03762)と照合。標準の埋め込み＋位置情報、LayerNorm、Attention・FFNそれぞれの残差経路を用いた。
- Tokyo等の7点は、入力から3層までの変化を説明する手動設定の座標。実モデルの隠れ状態や次元削減結果ではない。色はトークンの識別、点線の矢印は層間の変化を表す。静止状態4枚をHTMLにも保持し、JavaScript無効時と印刷時に表示する。
- Attentionの4要素の数値は固定した教材例。スコア[0, 1, −1, 2]からsoftmaxを計算し、表示を小数3桁へ丸める。Vの重心は1 headの集約だけを表す。

### AE・VAEのMNIST構造図

`source/ae_figures.py`で作成したオリジナル図。`mnist-train-00000-label-5.png`は04の同名素材から複製したMNIST訓練画像（index 0、ラベル5）。入力と復元目標に同じ画像を表示し、モデルの実行結果ではないことを図注に記載。VAE中央の正規分布は説明用の模式図。

### SSM・Mambaの概念図（2026-09-13）

`source/ssm.py`で生成する7点のインラインSVGは教材独自の模式図。Maarten Grootendorstの[A Visual Guide to Mamba and State Space Models](https://newsletter.maartengrootendorst.com/p/a-visual-guide-to-mamba-and-state)を説明順序の参考とし、原図・画像は転載していない。技術的な参照先は[Mamba論文](https://arxiv.org/abs/2312.00752)と[Mamba-1の著者実装](https://github.com/state-spaces/mamba/blob/main/mamba_ssm/modules/mamba_simple.py)。猫の名前の記憶は概念の説明用、0.8倍の状態更新は手計算の例であり、学習済みモデルの結果ではない。

### Normalizing Flowの分布と演算の図

`source/nf_figures.py`で生成するオリジナルSVG。2次元正規分布の等密度線に拡大・せん断型非線形変換・座標交換を適用。密度比較も解析式で描画。学習結果ではなく、係数を固定した説明用の計算例。

### ViT・VLM補足ページ

`source/vit.py`で作図した独自SVG（猫の模式イラスト、パッチ化、CLS分類、生成型VLMの流れ）。添付された参考図の説明順を参考に再構成。分類確率・回答・4パッチへの分割は説明用。構造はViT原論文とLLaVA著者ページを参照し、リンクを本文に掲載。

### Diffusionの猫の段階図と構造図（2026-09-13）

- `diffusion-cat-stages.png`：内蔵画像生成ツールで新規生成した写真風の説明素材。実データセットの写真、DDPMの実測中間出力、ノイズ付加式の数値計算結果ではない。5段階をSVGの表示窓で並べ、順方向は猫→ノイズ、生成方向はノイズ→猫として使用。元のPNGは変更せず同梱。
- `source/diffusion.py`：学習の正解ノイズと勾配、U-Netの縮小・拡大とスキップ接続、DiTのパッチ処理、文章条件のcross-attentionを示すオリジナルSVG。DDPM、LDM、DiT、CFGの原論文を参照し、本文末にリンクを記載。
- 従来の`diffusion-stages.svg`（手作り8×8数字）はDiffusion本文では使用しない。

画像生成の最終プロンプト（内蔵ツール、CLI不使用）：

> Use case: scientific-educational. Asset type: wide image strip for a Japanese diffusion-model textbook. Create exactly FIVE equally sized square panels in one horizontal row, minimal narrow white gutters, no text, no labels, no arrows. LEFT TO RIGHT: (1) pure dense fine-grained random RGB Gaussian-like static, no recognizable object; (2) very heavily noisy image with only a vague suggestion of a cat silhouette; (3) medium noisy photo with recognizable cat face and ears; (4) almost clean photo with slight fine grain; (5) crisp natural photograph of a single orange tabby cat sitting on a neutral beige background, centered, full ears and upper body visible. Same cat, pose, framing and background in panels 2–5. The cat should gradually emerge from the noise, no cartoon, no vector illustration, no mosaic blocks. This is an illustrative denoising sequence, not actual scientific output. Wide landscape 5-panel composition with no decoration, margins minimal.

### SSM再改訂の参照素材（2026-09-13）

| 素材 | 元URL・対象 | 掲載と加工 |
|---|---|---|
| `hippo-framework.png` | https://hazyresearch.stanford.edu/static/posts/2020-12-05-hippo/framework.png · Guほか著者解説 Figure 1 | 基底係数による履歴近似を説明するための原図引用。画像は無加工。図直下に著者・出典・読み方。オフライン閲覧用に保存。素材全体への自由利用ライセンスは付与しない。 |
| `hippo-measures.png` | https://hazyresearch.stanford.edu/static/posts/2020-12-05-hippo/instantiations.png · 同 Figure 2 | LegTとLegSの重み付けを比較する原図引用。画像は無加工、本文で左右の違いと図の長方形を説明。 |
| `mamba-copying.svg` | https://arxiv.org/html/2312.00752v2/copying.svg · Gu & Dao, Mamba v2 Figure 2 | CC BY 4.0。原図を無加工で補足に掲載。本文の日本語図ではSelective Copyingのみ取り出し、要素数・ラベル・配置を簡略化。 |
| `mamba-selection.svg` | https://arxiv.org/html/2312.00752v2/selection.svg · 同 Figure 1 | CC BY 4.0。原図を無加工で補足に掲載。本文の図では入力依存のB・C・Δと状態更新への経路を再構成。 |

再帰と畳み込みの図はMamba式(2)–(3)、計算量の比較は同§3.1、HiPPOの基底図は著者解説のOnline Function Approximationに基づく。説明順序は指定されたVisual Guideを参考にした。独自の猫の名前・物体の例は削除。HiPPO-LagTの指数重みは原論文補足D.2で確認。状態更新の移動アニメーションはユーザー指定の演出であり、論文の実験結果ではない。

2026-09-20追記：SSM本文のHiPPO節を波形・係数・更新規則の順に改稿し、比較を掲載図にあるLegT・LegSに限定。LagTの一覧は本文から除いた。原図は無加工で保持し、図中の記号・色・読む順序を本文で説明。Mamba Figure 2は各課題の入力と正解、Figure 1は状態と入力依存の係数の経路を説明し、日本語のコピー図と原図の白黒表記の違いも明記。

## 画像タスクの追加例（2026-09-13）

- `depth-bicycle-input.jpg` / `depth-bicycle-result.jpg`：Depth Anything V2 [著者ページ](https://depth-anything-v2.github.io/)のdetail comparisonより同一の自転車の例を引用。原ファイルは[`bicycle_img.jpg`](https://depth-anything-v2.github.io/static/images/compare_v1_detail/bicycle_img.jpg)と[`bicycle_v2.jpg`](https://depth-anything-v2.github.io/static/images/compare_v1_detail/bicycle_v2.jpg)。加工なし。車輪・スポークと隙間の深度を説明するため本文に掲載。推論モデルのサイズ、実距離は推測しない。
- 追加の花・基準尺・人物・姿勢の図は`source/vision.py`の教材用作図。車／花の分類、台数／高さの回帰、車／人物の検出・3種類の分割、立つ／しゃがむの特徴点の出力を比較。すべて実モデルの出力ではない。分類の出力枠にはラベル自体を表示する。

## タスクと実問題の図の追加（2026-09-13）

- `kool2019-tsp-decoder.png`：Kool, van Hoof & Welling, *Attention, Learn to Solve Routing Problems!* (ICLR 2019), [arXiv:1803.08475v3](https://arxiv.org/abs/1803.08475v3), Figure 2, PDF p.4。[取得元PDF](https://arxiv.org/pdf/1803.08475v3)。2026-09-13に本文・図番号・選択順序3→1→2→4とマスクの意味を照合。図の凡例と4段階を含む領域を216 dpiで切り出し（ページ左上基準 x=318, y=246, 幅1194, 高さ282 px）。原図の色・内容は変更せず、日本語の読み方は本文に配置。説明のための引用で、原著者の権利は保持される。実装のライセンスを論文図へ適用しない。
- `source/decision.py`：一般的なエージェント・環境ループ、10都市の巡回路と段階的な生成、ガントチャートをHTMLへ埋め込む。TSPはユーザー提供の点と矢印の図を参考に教材用に作図し、同じ都市配置で長い経路と短い経路を比較。最短性は主張しない。ガントチャートはA1=M1で3分、A2=M2で2分、B1=M2で2分、B2=M1で2分。9分と5分の両予定で工程の前後関係と機械占有の制約を確認。これらは教材独自の数値例で、論文の推論結果ではない。
- `source/task_figures.py`：追跡のID維持、RAGの質問と回答、音源分離の合成波形、論文グラフのノード分類、分子の予測と設計を対にして示す教材用SVG。音の図は周波数比1:3の模式波形で、音声ファイルのサンプルを描いたものではない。
- スケジューリングの研究説明：[Zhang et al., Learning to Dispatch for Job Shop Scheduling via Deep Reinforcement Learning (NeurIPS 2020)](https://papers.nips.cc/paper/2020/hash/11958dfee29b6709f48a9ba0387a2431-Abstract.html)。GNNによる状態表現と強化学習による優先順位規則の学習を紹介。論文図の転載はせず、2仕事・2機械の教材例と区別する。

## 年齢推定と同一タスク内のデータ比較（2026-09-13）

- `utkface-train-2000-age-30.jpg` / `utkface-train-2001-age-35.jpg`：[UTKFace公式](https://susanqq.github.io/UTKFace/)の年齢推定タスクを説明する2枚。取得元は[公開ミラー](https://huggingface.co/datasets/vtsouval/utkface-cropped)のdefault/trainの2000・2001行（revision afac20af69219e658f76532d49e3c95bc781c2a0）。取得レコードは`age-sources.json`。写真は加工なし、年齢ラベルを出力形式に合わせて30.0歳・35.0歳として表示。推論は未実施。公式は非商用研究用途限定、写真の著作権は元の権利者に帰属と記載。教材の年齢推定の説明に必要な2枚を引用。年齢注釈は推定と人による確認であり、生年月日確認済みとはしない。
- 画像タスクは入力・出力の共通列に2件をまとめ、データごとの囲みや「例1・例2」を廃止。分類・検出・分割は同じ教材用街路集合の2枚。以前追加した花／室内人物の異種用途の対比は廃止。深度は既存の写真と推定マップを維持。

## 犬・猫の分類と論文中の姿勢推定図（2026-09-13）

- `pet-dog.jpg` / `pet-cat.jpg`：[Oxford-IIIT Pet公式](https://www.robots.ox.ac.uk/~vgg/data/pets/)の犬・猫2枚。[公開ミラー](https://huggingface.co/datasets/Donghyun99/Oxford-IIIT-Pet)のdefault/train行100（species=Dog）・行0（species=Cat）から取得。詳細な取得元とラベルは`pet-sources.json`。加工なし。公式のCC BY-SA 4.0の表示を図下に記載。著作権は元の写真の権利者に帰属。推論は実施せず、種別の注釈を犬・猫として表示。
- `blazepose-fig6-yoga1.png` / `blazepose-fig6-yoga2.png`：Bazarevsky et al., *BlazePose: On-device Real-time Body Pose tracking*（2020）, [arXiv:2006.10204v1 Figure 6](https://arxiv.org/html/2006.10204v1#S4.F6)から2パネルを引用。原画像は同HTML下の`yoga1.png`と`yoga2.png`。図番号・キャプションを原論文HTMLで確認。ヨガ・フィットネスの姿勢推定結果であり、モデル構造図ではない。各パネルの加工なし。特徴点と接続の読み方を本文で説明するため掲載。論文の権利を保持した図の引用であり、教材独自の作図や自由再利用素材としては扱わない。

## 動画・3D：RAFT・ORB-SLAM3（2026-09-13）

原論文の本文・図を照合し、説明に必要な図の領域を引用。原著者および図中の画像の権利は保持される。実装のライセンスを論文図の自由利用条件として適用しない。切り出し以外の色・内容の改変はない。

| ファイル | 出典と位置 | 加工・読む対象 |
|---|---|---|
| `raft-figure1.png` | Teed & Deng, *RAFT: Recurrent All-Pairs Field Transforms for Optical Flow* (ECCV 2020), [arXiv:2003.12039v3](https://arxiv.org/pdf/2003.12039v3), Figure 1, PDF p.2 | Popplerでページ長辺2800 pxへ描画し、左上基準 `(140,144,1750,700)` の矩形を切り出し。特徴抽出、相関表、反復更新、フロー表示の原図。図注は本文に日本語で記述。 |
| `orb-slam3-figure1.png` | Campos et al., *ORB-SLAM3: An Accurate Open-Source Library for Visual, Visual-Inertial and Multi-Map SLAM* (IEEE T-RO 2021), [arXiv:2007.11898v2](https://arxiv.org/pdf/2007.11898v2), Figure 1, PDF p.5 | 長辺2800 pxのページから `(1090,186,1990,982)` を切り出し。Tracking・Atlas・Local Mapping・Loop & Map Mergingの役割を本文で解説。 |
| `orb-slam3-figure6.png` | 同論文Figure 6, PDF p.14 | 同条件で `(190,1078,1042,2012)` を切り出し。航空写真と二つの推定軌跡を含む。赤はoutdoors1単独、青はmagistrale2の後にoutdoors1を処理。青を正解軌跡と呼ばない。 |
| ORB-SLAM3動画（外部埋め込み） | [公式README](https://github.com/UZ-SLAMLab/ORB_SLAM3)掲載の[著者動画](https://www.youtube.com/watch?v=HyLNq-98LRo) | TUM-VI Stereo-Inertial, room1+magistrale1+magistrale5+slides1。上記Figure 6と別系列。ダウンロード・加工せず、利用者がボタンを押した後にYouTubeのプレーヤーを読み込む。HTML直接表示時はYouTubeへのリンクを使う。 |

`source/spatial.py`のフローの矢印・数値、部屋とカメラの図、点群・メッシュ・ボクセル・座標関数の図は教材独自の模式図。RAFTの反復値 `(0,0) → (8,1) → (11,3) → (12,3)` は説明用で、実測値ではない。NeRF動画は既存の `nerf-result.mp4` を説明の近くへ再掲し、実撮影と合成視点の違いを説明。新規モデルの推論・再学習はしていない。

## 科学応用：タスク別の論文説明図（2026-09-13）

科学ページを6つのタスクの独立節へ変更。以下は論文の説明を本文で論じるための原図引用で、教材独自の作図や推論結果ではない。各図の直下に著者・図番号・原論文リンクを掲載し、色・矢印・記号の読み方を日本語で説明する。原著者の権利を保持し、教材の他素材のライセンスをこれらの図へ適用しない。図をクリックすると同梱の画像を拡大できる。

| 保存素材 | 原論文・取得元 | 掲載範囲と加工 |
|---|---|---|
| `alphafold-fig1.png` / `alphafold-fig1e.png` | Jumper et al. (2021), [Fig. 1](https://www.nature.com/articles/s41586-021-03819-2/figures/1) · [原画像](https://media.springernature.com/full/springer-static/image/art%3A10.1038%2Fs41586-021-03819-2/MediaObjects/41586_2021_3819_Fig1_HTML.png) | 全体を保存し、モデルの説明部分eを掲載。原画像2157×1382 pxから左上基準の矩形(0,655,2157,1382)を切り出し。座標は左・上・右・下。 |
| `rfdiffusion-fig1.png` / `rfdiffusion-fig1b.png` | Watson et al. (2023), [Fig. 1](https://www.nature.com/articles/s41586-023-06415-8/figures/1) · [原画像](https://media.springernature.com/full/springer-static/image/art%3A10.1038%2Fs41586-023-06415-8/MediaObjects/41586_2023_6415_Fig1_HTML.png) | 条件による設計の違いを説明する部分bを掲載。2187×2013 pxから(1080,0,2187,1450)を切り出し。 |
| `fno-fig2.png` | Li et al., ICLR 2021, [arXiv:2010.08895v3 Fig. 2](https://arxiv.org/html/2010.08895v3#S2.F2) · [原画像](https://arxiv.org/html/2010.08895v3/figs/fourier_full_arch5.png) | 原図全体、無加工。aの入出力とbのFourier層を説明。同論文§5.5のベイズ逆問題も本文で参照。 |
| `graphcast-fig1.png` / `graphcast-fig1abc.png` | Lam et al., [arXiv:2212.12794v2 Fig. 1](https://arxiv.org/html/2212.12794v2#Sx1.F1) · [原画像](https://arxiv.org/html/2212.12794v2/figures/schematic.png) | 5166×4916 pxから入出力・予報の反復を示すa–cの(0,0,5166,2090)を切り出し。引用版を固定し、Science掲載版の図と同一とは扱わない。 |
| `scgen-fig1.png` | Lotfollahi et al. (2019), [Fig. 1](https://www.nature.com/articles/s41592-019-0494-8/figures/1) · [原画像](https://media.springernature.com/full/springer-static/image/art%3A10.1038%2Fs41592-019-0494-8/MediaObjects/41592_2019_494_Fig1_HTML.png) | 原図全体、無加工。細胞種の色、刺激前後の形、潜在空間の差分δと復号を本文で説明。 |

図の番号・キャプション・読み方は出版社の図ページまたは原論文HTMLで照合。切り出し以外の色・内容の改変なし。本文の正本は`source/science.py`。冒頭の予測／設計は既存の教材用模式図を科学ページ専用CSSで最大340 pxずつの2列（狭い画面は1列）にし、論文図の表示高を最大480 pxに制限。

### Sora・Genieの生成例（2026-09-13）

- `genie-figure1.png`：Bruce et al., *Genie: Generative Interactive Environments* (2024), [Figure 1](https://arxiv.org/html/2402.15391v1#S1.F1)。[原画像](https://arxiv.org/html/2402.15391v1/figures/platformer_trajectories.png)を無加工で引用（595×524 px）。同じ初期画像から操作ごとに異なるフレーム列ができることを説明。初代Genieの図であり、Genie 2・3の結果ではない。著者ページのGoogle画像配信は取得時403だったため、論文HTMLで図と本文を照合したものを使う。モデルの実行はしていない。
- Sora公式紹介動画：OpenAI, *Introducing Sora — OpenAI’s text-to-video model*, 2024-02-16, [YouTube](https://www.youtube.com/watch?v=HK6y8DAPN_0)。YouTube oEmbedの著者名OpenAI・公式チャンネルURLを照合。ダウンロード・加工はせず、クリック後に外部プレーヤーを読み込む。HTML直接表示時は公式動画へのリンクを使う。
- Soraの構造の説明：Brooks, Peebles, et al., [Video generation models as world simulators](https://openai.com/index/video-generation-models-as-world-simulators/)（2024-02-15）。圧縮した時空間パッチとDiffusion Transformer、物理的な状態変化の限界を参照。Sora 2や現在のサービス仕様とは区別。
- `source/spatial_generation.py`の入出力比較・Sora生成フロー・Genieの画像と操作の合流図は教材独自。犬の文章は教材用の例であり、公式映像の実プロンプトとはしていない。Genieの原論文§2.1–2.2で潜在操作・推論の条件を確認。

## 意思決定ページの動画（2026-09-13）

YouTube埋め込みを使わず、公式公開動画を教材での説明用にローカル保存。原尺を維持してH.264/MP4（yuv420p、最大960×720、音声なし）へ変換。ポスターは動画内のフレーム。権利は各著者・権利者に帰属。

- `decision-breakout.mp4`：Mnihら「Human-level control through deep reinforcement learning」（Nature 2015）の補足動画2。学習100/200/400/600エピソードの比較。元動画：https://media.springernature.com/original/springer-static/esm/art%3A10.1038%2Fnature14236/MediaObjects/41586_2015_BFnature14236_MOESM124_ESM.mov
- `decision-space-invaders.mp4`：同論文の補足動画1、DQNのSpace Invaders。元動画：https://media.springernature.com/original/springer-static/esm/art%3A10.1038%2Fnature14236/MediaObjects/41586_2015_BFnature14236_MOESM123_ESM.mov
- `decision-diamond.mp4`：DIAMOND著者ページ（https://diamond-wm.github.io/）のCS:GO世界モデルのデモ。人間の操作に応じた生成であり、自動プレイではない。元動画：https://diamond-wm.github.io/static/videos/8.mp4
- `decision-orbit.mp4`：ORBIT著者ページ（https://isaac-orbit.github.io/）のReinforcement Learningワークフロー。多数のロボット環境の並列シミュレーション。元動画：https://isaac-orbit.github.io/videos/Workflow-RL.mp4
- `decision-*-poster.jpg`：Space Invadersは12秒、他は2秒のフレーム。
- 経路生成図は「部分経路 → Transformer → 次の都市を追加」の教材図へ変更。KoolらのAttentionモデルの役割を簡略化し、論文の計算グラフそのものとは区別。

### 科学ページを入出力中心に簡略化（2026-09-13）

- 複雑なモデル構成図と内部の計算説明を本文から除き、「研究で役立つ理由」を導入へ移動。AlphaFold2→細胞応答→RFdiffusion→水の動き→画像復元→気象の順に変更。
- AlphaFoldの配列／構造対は同梱PDBの同じ142残基から作図（CαのXY投影）。異なるタンパク質の配列と形を組み合わせない。2024年ノーベル化学賞は[John Jumperの公式Facts](https://www.nobelprize.org/prizes/chemistry/2024/jumper/facts/)と[開発元の受賞記事](https://deepmind.google/blog/demis-hassabis-john-jumper-awarded-nobel-prize-in-chemistry/)を参照し、受賞者を明記。
- `rfdiffusion-binder.png`：既存のFig. 1全体から(1100,615,2187,905)を切り出し、結合相手を指定する1行だけ掲載。色・構造は改変なし。
- `gns-water.mp4`：[Learning to Simulate Complex Physics with Graph Networks（Sanchez-Gonzalez et al., ICML 2020）の著者ページ](https://sites.google.com/view/learning-to-simulate)にあるWater-3D公開動画。[元のDrive動画](https://drive.google.com/file/d/1nUSKoMbZb7EMwB6D5PcqZk602tcCHI5x/view)、取得先は同IDの`https://drive.google.com/uc?export=download&id=1nUSKoMbZb7EMwB6D5PcqZk602tcCHI5x`。原動画を無加工で保存（50.08秒）。左Ground truth＝基準のシミュレーション、右Prediction＝学習したモデルの予測。動きを比較してタスクを説明するための引用。原著者の権利を保持。
- 画像復元と気象のSVGアニメーションは教材独自の入出力イメージ。細胞形状のぼけの変化と雨域の移動を示す。AIの推論結果ではなく、科学的な数値計算の再現でもない。再生・一時停止・スライダー操作が可能。自動再生なし。動きを減らす設定では静止状態を切り替える。
- 細胞応答の棒グラフは遺伝子A/B/Cの働きの強さを表す架空の説明値。scGenの測定／予測値ではない。
- GraphCastの公式予報動画は[Google DeepMindの解説](https://deepmind.google/blog/graphcast-ai-model-for-faster-and-more-accurate-global-weather-forecasting/)が掲載する[Q6fOlW-Y_Ss](https://www.youtube.com/watch?v=Q6fOlW-Y_Ss)。10日間の700 hPaの湿度、地表温度・風速を示す。利用者がボタンを押したときだけ外部プレーヤーを読み込む。オフラインでは上の教材アニメーションを利用できる。

- 囲碁のイラスト（`source/decision.py`）：黒白の石と次の一手を示す教材独自の9路盤。実対局の棋譜ではない。AlphaGoの実対局は19路盤。対戦結果の参照：https://deepmind.google/research/alphago/ および https://blog.google/innovation-and-ai/products/alphago-machine-learning-game-go/ 。

## 動画・3Dを原図・公開映像へ統一（2026-09-13）

ユーザー指定により、このページの教材独自の模式図・箱と矢印・数値の推移例はすべて撤去。上の制作記録は履歴であり、現在は`source/spatial.py`・`source/spatial_generation.py`に自作図の生成処理を置かない。

| 素材 | 出典 | 掲載・加工 |
|---|---|---|
| `sam2-author-model.png` | [SAM 2公式GitHub](https://github.com/facebookresearch/sam2)、[原画像](https://raw.githubusercontent.com/facebookresearch/sam2/main/assets/model_diagram.png) | 無加工で引用。鶏のフレームとマスク、記憶を後のフレームで使う経路を説明。 |
| `nerf-author-rendering.png` | [NeRF著者ページ](https://www.matthewtancik.com/nerf)のAbstract & Method、[原画像](https://cdn.prod.website-files.com/51e0d73d83d06baa7a00000f/5e700ef6067b43821ed52768_pipeline_website-01.png) | 無加工で引用。光線上のサンプリング、ネットワーク、色の合成を原図に沿って説明。 |
| `genie-inference.png` | [Genie原論文Figure 7](https://arxiv.org/html/2402.15391v1#S2.F7)、[原画像](https://arxiv.org/html/2402.15391v1/figures/genie_inference.png) | 無加工で引用。過去画像と操作を条件にした反復生成を解説。 |
| `3dgs-bicycle.mp4` | [3D Gaussian Splatting著者ページ](https://repo-sam.inria.fr/fungraph/3d-gaussian-splatting/)、[元動画](https://repo-sam.inria.fr/fungraph/3d-gaussian-splatting/content/videos/bicycle.mp4) | 著者公開結果を無加工で引用。9.9099秒。自転車と背景の描画を観察する。 |

いずれも研究の説明のための引用であり、原著者・元画像等の権利は保持される。新規推論・生成結果とはしていない。

### 動画・3D：構造図から実験結果へ（2026-09-13、追加修正）

ユーザー指定によりモデル構成図はすべてページから除外。上記のモデル図・YouTube埋め込みの説明は過去の実装記録。現在は次の結果と、既存のORB-SLAM3 Figure 6、Genie Figure 1、NeRF・3DGS動画を掲載する。

- `raft-results.png`：RAFT v3 PDF p.9のFigure 3。SintelテストセットのGround Truth / VCN / IRR-PWC / Oursをすべて保持。PDFを長辺2000pxで描画し、矩形(x=150,y=100,w=1040,h=250)を抽出。図の内容は改変なし。
- `sam2-track-0.png`, `sam2-track-90.png`, `sam2-track-180.png`：[SAM 2公式動画ノートブック](https://github.com/facebookresearch/sam2/blob/main/notebooks/video_predictor_example.ipynb)の複数対象追跡の保存済みPNG出力。2026-09-13取得、セル65（0始まり）のframe 0 / 90 / 180を無加工で抽出。元ファイル：https://raw.githubusercontent.com/facebookresearch/sam2/main/notebooks/video_predictor_example.ipynb 。教材側では推論していない。
- `sora-tokyo.mp4`：[OpenAIのSora公開生成例](https://openai.com/index/sora/)のTokyo walk（2024年発表）。公式配信元：https://cdn.openai.com/sora/videos/tokyo-walk.mp4 。無加工の動画を掲載。初代Soraの研究例で、現行製品の提供状況を表すものではない。

外部プレーヤー、YouTube埋め込み、動画読み込みボタンは除去。各素材の原著者の権利を保持し、結果の比較・解説のため出典付きで引用する。


### 自然言語：LLaVAの公開回答例（2026-09-13）

- `llava-ironing.png`：https://llava-vl.github.io/images/cmp_ironing.png 。Liu et al., Visual Instruction Tuning（2023）の著者ページ「Visual Reasoning」に掲載された比較図。加工なし。入力画像と公開回答の関係を解説するための引用。写真の原出典は図内に記載されている。著者ページのデータセット・モデルの利用条件を、この比較図全体の包括的なライセンスとは扱わない。
- `language.js`：教材独自の固定回答切り替え、および語句一致検索と定型回答。外部APIや学習済みLLMを呼び出さない。資料A〜Cは架空の教材用文章。実モデルの出力は上の著者公開比較図と区別して掲載。

### 科学ページ：図の対応と研究映像を再整理（2026-09-13）
- AlphaFold2・細胞応答・RFdiffusionは、図の内部に入力／出力・文字／色／棒の説明を配置した教材独自の模式図に変更。短いアミノ酸鎖の左右は同じ順番。実モデルの結果とは表示していない。
- 逆問題はOpenFWI / InversionNet（https://openfwi-lanl.github.io/）を例に、地表の波形から地下の速度分布を推定する題材へ変更。波の伝播→計測→地下推定の模式アニメーション。波形や地層は実測・実推論ではない。
- `dgmr-rain.mp4`：DGMR著者公式解説 https://deepmind.google/blog/nowcasting-the-next-hour-of-rain/ の英国事例GIF https://storage.googleapis.com/gdm-deepmind-com-prod-public/media/original_images/6227e32e3d49b17ff5eba816_Fig202.gif から上段（550×300、Target / DGMR）を抜粋。H.264 MP4化、時間を3倍に延長。映像内の予測は変更なし。11.34秒、約361 KB。`dgmr-rain-poster.jpg` は先頭フレーム。元は55フレームの研究アニメーション。
- 原論文：Ravuri et al., Nature (2021), https://www.nature.com/articles/s41586-021-03854-z 。直前20分のレーダーを入力し、90分先までの降雨を予測。引用部分の左右・読み方・加工は映像直下に明記。動画はローカル同梱し、ネット接続なしで再生可能。

### 音声・音楽ページの試聴素材（2026-09-13）

- `audio-tts-normal.wav` / `audio-tts-fast.wav`：教材用文章「明日の会議は、午後三時からです。」をmacOSのKyoko音声で合成。`say -v Kyoko -r 170` / `-r 260`、WAVE・LEI16・22,050 Hz。TTSの出力例として掲載。ASR欄の文字は元文章で、認識モデルの推論結果ではない。
- `audio-score-mix.wav` / `audio-score-melody.wav` / `audio-score-backing.wav` / `audio-score.svg`：教材オリジナルの8秒の旋律・伴奏と音の配置図。16,000 Hz、mono、16-bit PCM。`python3 06-ml-landscape/source/audio_assets.py`で再生成。混合前の元成分を提示して分離の目標を説明する素材であり、分離モデルの出力ではない。
- `audio-musicgen-dance.mp3`：<https://ai.honu.io/papers/musicgen/samples/musicgen/000_sample.mp3>
- `audio-musicgen-orchestra.mp3`：<https://ai.honu.io/papers/musicgen/samples/musicgen/001_sample.mp3>
  - 出典：Copet et al., *Simple and Controllable Music Generation*（2023）の[著者試聴ページ](https://ai.honu.io/papers/musicgen/)、Text-to-musicのMusicGen列の先頭2例。各30秒、加工なし。入力説明は本文に日本語要約を掲載。
  - 教材本文で入力条件と生成結果を比較・説明するための引用。音声そのものの再配布ライセンスは確認できていないため、自由利用素材とは扱わない。モデル重みのライセンスを音声へ自動的に適用しない。原著者ページと[公式モデル説明](https://facebookresearch.github.io/audiocraft/docs/MUSICGEN.html)を試聴例の直下に表示。新規推論や性能比較実験ではない。

### フレーム切り替え・RAFT入力出力（2026-09-13）

- SAM 2の同じ公式ノートブック・セル65からframe 30/60/120/150の保存済みPNGも無加工で抽出。`sam2-track-{0,30,60,90,120,150,180}.png`の7枚を矢印で切り替える。
- `raft-input.png`, `raft-output.png`：RAFT v3 PDF p.10 Figure 4の左下のKITTI例。元画像とRAFT推定結果のみを表示する。長辺3200pxで描画し、(x=176,y=328,w=450,h=148)と(x=626,y=328,w=450,h=148)を抽出。モデル構成図・他手法・正解フローは表示しない。元のFigure 3には入力画像がないため、入力と結果が対で示されるFigure 4へ変更。

### 科学の3図の見た目を再制作（2026-09-13）
- AlphaFold2：同梱P69905 v6の142 Cα座標を直交投影し、補間した主鎖と奥行き陰影をSVG描画。左の全配列も同じPDBから抽出。色は信頼度ではなく奥行き。
- RFdiffusion：既存Fig.1b抜粋画像をSVGのclipPathで入力相手／最終候補の2領域に限定して表示。原図自体の構造・色は変更せず、途中生成状態と周辺の枠を除外。
- 細胞応答：6遺伝子×8細胞の模式ヒートマップ。実測・推論結果ではない旨を図下に記載。色の凡例と入力／出力の説明を添付。


### 自然言語の図への改訂（2026-09-13）

LLMの指示切り替えデモとLLaVAの原図掲載を撤去。`llava-ironing.png`は未使用の旧素材として保管。`source/language_figures.py`にVLMの入出力経路、CLIPの共通特徴空間、類似度表の3図を教材独自に作図。既存のOxford-IIIT Petの猫・犬写真を縦横比を保持して使用し、図の下にCC BY-SA 4.0と出典を表示。図中の座標・類似度・回答は説明用で、モデルの実測ではない。添付参考画像自体は転載していない。`language.js`はRAG検索デモのみを担当。

### 波形・スペクトログラム（2026-09-13）

`audio-waveform.png`・`audio-spectrogram.png`は教材オリジナルの`audio-score-mix.wav`を数値として読み取り作図。波形は8秒の全体と1.02〜1.06秒の拡大。スペクトログラムは16 kHz PCMに1024点Hann窓・128点ホップの短時間FFTを適用し、パワーを全体の最大値に対するdBで表示（−60〜0 dB、周波数0〜1200 Hz）。モデル推論ではない。再生成：プロジェクト環境で`python 06-ml-landscape/source/audio_figures.py`（NumPy、Matplotlib、日本語フォントを使用）。HTMLの再生成時には計算不要。


### XAIの同一モデル比較（2026-09-13）

`xai-input.png`, `xai-segments.png`, `xai-saliency.png`, `xai-ig.png`, `xai-lime.png`, `xai-gradcam.png`は、上記Grad-CAMの原写真を共通入力とし、torchvisionのImageNet学習済みResNet-18（IMAGENET1K_V1）で実際に計算した教材用の結果。Grad-CAM論文のVGG-16の実験結果とは別物。

対象は全てtabby（クラス281）のsoftmax前スコア。短辺256へリサイズ後、中央224角へクロップ。Saliencyは入力勾配の絶対値のRGB最大、IGは黒RGBを基準とする256分割の台形則でRGB寄与を合計、Grad-CAMはlayer4（7×7）。LIME方式はSLICの領域をランダムに残す局所サンプルに重み付きRidgeを当てはめる実装。保持確率0.85、隠す領域は黒、1,024例、seed 42、cosine距離のカーネル幅0.1、Ridge強度1、切片にペナルティなし。

`xai-results.json`に実行環境・寄与の合計と出力差・局所近似の当てはまりを、`xai-attributions.npz`に色付け前の数値を記録。再生成は`source/xai_image_results.py`（torch / torchvision / numpy / Pillow / matplotlib / scikit-imageが必要）。通常のHTML再生成では実験や重みのダウンロードを行わず、同梱の結果を使用する。

XAIのShapley、寄与度分解、IG、LLMの図は`source/xai.py`の教材用SVG。論文の回路の全体を再現するものではなく、各図に出典と簡略化した条件を表示している。

### RAGをベクトル検索の説明へ改訂（2026-09-13）

語句一致の操作デモを撤去し、`source/language_figures.py`に階層のある文書庫からのベクトル検索と回答生成の自作図を追加。`language.js`は旧デモ用の未使用ファイル。CLIPの利用時の順位付け説明も撤去。

### DiCEの反実仮想図（2026-09-13）

`dice-counterfactual.gif`：Microsoft Researchの[DiCE著者解説](https://www.microsoft.com/en-us/research/blog/open-source-library-provides-explanation-for-machine-learning-through-diverse-counterfactuals/)に掲載され、[DiCE公式ドキュメント](https://interpret.ml/DiCE/readme.html)から参照されている著者公開図。[原ファイル](https://www.microsoft.com/en-us/research/uploads/prod/2020/01/MSR-Amit_1400x788-v3-1blog.gif)を改変せず保存。青は元入力、橙は反実仮想候補、曲線は判定境界。教材の実測結果ではない。本文の図直下に著者出典を明記。素材に別途のオープンライセンスは確認していない。


### 最適化の3D動画（2026-09-13）

- `optimization-descent.webm`：Ajith Pinninti, [Gradient Descent Visualizer](https://github.com/ajithpinninti/gradient-descent-visualizer) の[公開動画](https://raw.githubusercontent.com/ajithpinninti/gradient-descent-visualizer/main/assets/demo.webm)を無加工で同梱。二変数の損失地形上でSGD・Momentum・RMSProp・Adamの更新を可視化したデモ。実ニューラルネットの学習ログではない。
- `optimization-descent-poster.jpg`：同リポジトリの `assets/demo.gif` のフレーム10をJPEG化したポスター。
- MITライセンス、Copyright (c) 2026 ajithpinninti。ライセンス全文は `optimization-descent-LICENSE.txt`。動画直下に出典と読み方を表示。

### SAM 2の元画像とGenie 3（2026-09-13）

- `sam2-input-{0,30,60,90,120,150,180}.jpg`：公式GitHubの `notebooks/videos/bedroom/{frame:05d}.jpg`。取得URL例：https://raw.githubusercontent.com/facebookresearch/sam2/main/notebooks/videos/bedroom/00000.jpg 。マスク付きノートブック出力と同じフレーム番号を対応させ、無加工で並べる。
- `genie3-library-cat.webm`：[Genie 3公式モデルページ](https://deepmind.google/models/genie/)に掲載されたLibrary catデモ。元動画：https://storage.googleapis.com/gdm-deepmind-com-prod-public/media/media/genie-3__library_cat.webm 。無加工で保存。2026-09-13に公式モデル一覧とモデルページでGenie 3を確認。初代GenieのFigure 1に代えて掲載する。動画の再生であり、この教材でモデルを実行するものではない。出典・原著者の権利を保持。

### 自然な音声合成の比較（2026-09-13）

- `audio-tacotron2-generated.wav`：<https://google.github.io/tacotron/publications/tacotron2/demos/washington_gen.wav>（Tacotron 2の合成出力）
- `audio-tacotron2-human.wav`：<https://google.github.io/tacotron/publications/tacotron2/demos/washington_gt.wav>（同じ文章を読んだ人の録音）
- 出典：Shen et al., *Natural TTS Synthesis by Conditioning WaveNet on Mel Spectrogram Predictions*、[著者公開サンプル](https://google.github.io/tacotron/publications/tacotron2/)の「Tacotron 2 or Human?」のWashington例。元ページHTMLの`_gen`・`_gt`の対応に基づいてラベルを表示。両ファイルとも加工なし。自然な音声合成を説明する比較として引用。音声の自由な再配布ライセンスは確認していない。本文には出典リンクを併記。
- TTS節の速度比較をこの比較に置換。既存Kyoko素材はASR節の入力例に継続使用。

### 3Dの順序と生成デモの整理（2026-09-13）

- `pointcloud-room.png`：Open3D 0.19 release documentationのVoxel downsampling出力。https://www.open3d.org/docs/release/_images/tutorial_geometry_pointcloud_5_1.png を無加工で引用。室内を点群として可視化した結果。
- `coordinate-field.svg`：今回のユーザーの明示的な図作成指示に基づく教材図。f(x,y,z)=x²+y²+z²−1の単位球とy=z=0の断面。これはNeRFの密度関数やSDFの実測結果ではなく、座標から値を返す関数の例。A=−1、B=0、C=1.25。
- `genie3-racetrack.webm`：Genie 3公式モデルページ掲載のBackyard racetrack。https://storage.googleapis.com/gdm-deepmind-com-prod-public/media/media/genie-3__backyard_racetrack.webm を無加工で保存。20.111秒。
- `sora-tokyo-clip.mp4`：既存の公式 `sora-tokyo.mp4` から冒頭15秒をAVFoundationで抜粋。映像内容の加工・再生成なし。

ハッシュ格子の説明はInstant-NGP（Müller et al., 2022）の公式論文・ページに基づく。原型NeRFの位置エンコーディングと区別し、NNが高周波を表現不可能という誤解や、ハッシュで不連続化するという説明を避ける。

### 3D導入の模式図（2026-09-13）

`spatial-pointcloud-simple.svg` と `spatial-nerf-simple.svg` は、ユーザー指定の簡単な導入図として作成した教材用SVG。実験結果ではない。点の位置・色と、複数の写真から場面専用NNを学習する考え方を示す。旧 `coordinate-field.svg` は本文で使用しない。

### SLAMの実画像とGenie 3再生互換性（2026-09-13）

`tum-vi-inputs.png` は https://cvg.cit.tum.de/_media/data/datasets/vi-dataset/thumbs.png の公式サンプル画像を無加工で引用。複数場面の一覧であり、同一走行の連続フレームではない。SLAMの模式図を置換。`genie3-racetrack.mp4` は既存の公式WebM映像をH.264/yuv420pへ変換しfaststartを設定。内容・尺は維持。posterはその映像の0.1秒から抽出。

### SLAM入出力の走行を統一（2026-09-13）

入力を公式アーカイブ https://vision.in.tum.de/tumvi/exported/euroc/512_16/dataset-outdoors1_512_16.tar から取り出した同一走行の実画像へ変更。`orb-outdoors1-5-display.png` は `mav0/cam1/data/1520426225439768133.png`、`orb-outdoors1-4-display.png` は `mav0/cam1/data/1520426275991342572.png`。差は約50.55秒。16bit PNGを表示用8bitグレースケールに変換しただけで、切り抜き・生成・内容変更なし。出力Figure 6もoutdoors1。赤は単独処理、青はmagistrale2で作った地図も利用した処理。旧サンプル一覧は本文から除去。
