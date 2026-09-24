# 機械学習の全体像

[教材を開く](index.html)

clone後、プロジェクト直下の `index.html` または `dist/index.html` をブラウザで直接開けます。生成済みの `dist/` をGitに含めているため、閲覧にNode.js・npm・Pythonのインストール、ビルド、サーバー、ネット接続は不要です。本文・数式・静止図はJavaScript無効時も読めます。操作部品・本文検索・配色の切り替えにはJavaScriptを使います。外部論文・外部配信動画には接続が必要で、音声・動画は再生操作をしたときに再生します。

目次は「はじめに → 基礎 → 分野・タスク → 横断研究 → モデル」です。「準備中」は本文未公開、「拡充予定」は既存説明があり、計画上の追加範囲が残るページです。詳説の分量を一律にはそろえていません。

上部の「検索」（または `/` キー）で全ページの本文を節単位で検索できます。検索用の索引はビルド時に作る `assets/search-index.js` で、`file://`でも動きます。配色はOSの設定に従い、月のボタンで明暗を切り替えられます。暗い配色でも、図と操作部品は描画を保つため明るい下地のまま表示します。サイドバーの項目にポインタを置くと、前提となるページを表示します。

## HTMLの配置

入口の `index.html` はプロジェクト直下に置き、各ページは `dist/` 内で本文と同じ区分に配置します。`dist/index.html` も配布用の入口として生成します。

```text
index.html       # 通常の入口
dist/
├── index.html
├── basics/       # 基礎（learning.html など）
├── models/       # モデル（transformer.html など）
├── fields/       # 分野・タスク（vision.html など）
├── questions/    # 横断研究（optimization.html など）
├── assets/       # 共通スタイル・スクリプト・素材
└── content/      # ページ専用素材・操作部品
```

各ページの `url` が `dist/` 内のビルド先を指定します。リンク・画像・操作用素材は階層に対応した相対参照で、`file://`でも閲覧できます。旧構成のHTML・案内ページは削除しました。旧URLのブックマークは新しいページへ更新してください。過去の移行記録に記載したURLは当時の構成です。

## 編集する場所

本文の正本は `content/<区分>/<ページID>/index.md` です。通常の文章・見出し・表・数式・キャプションの変更にビルド処理や共通テンプレートの編集は不要です。

| 対象 | 正本 |
|---|---|
| 本文とページ情報 | 各ページの `index.md` |
| 目次・表示順・カテゴリ・ViTの親子関係 | `navigation.yml` |
| 出典URL・素材情報 | 各ページの `sources.yml` |
| 専用画像・音声・動画 | 各ページの `media/` |
| 専用の図・操作・スタイル | 各ページの `components/`、Markdown冒頭の `scripts` / `styles` |
| 共通ヘッダー・ナビゲーション | `templates/page.html`、`assets/navigation.js` |
| 共通スタイル・数式フォント | `assets/style.css`、`assets/navigation.css`、`assets/content.css`、`assets/katex.css`（フォントを内包） |
| 共有素材・履歴 | `assets/`、`content/shared/media-provenance.md`、`content/shared/media-ownership.yml` |
| 共有用画像の元図 | `source/og-image.svg` |
| HTML | ビルド成果物。直接編集しない |

ファイルの場所と表示順は独立しています。ページを別フォルダへ移しても、`page:`リンクはIDから解決されます。`url`は公開先のパスです。変更した場合は参照先も更新します。

```markdown
[Attentionの説明](page:transformer#attention)
[原論文](source:ref-001)
![図の説明](media:example.png)

## 小見出し {#stable-anchor}

$$
p(y \mid x)
$$

{{component:visual-001}}
```

既存の `<section id="…" markdown="1">` は節のアンカーと図のレイアウトを保つ囲みです。内部は普通のMarkdownとして編集できます。`{{component:…}}` は同じページの `components/…html` を読み込みます。複雑な図と操作にだけ使い、通常の本文を部品へ移さないでください。数式は同梱KaTeXでHTML・MathMLへ事前組版します。

メタデータの `status` は `planned`（本文未公開）、`partial`（既存内容あり・拡充予定）、`migrated`（既存内容移行）、`ready`（本文整備済み）。収録決定と完成度を区別し、`scope`に予定範囲、`origins`に移行元を記録します。`prerequisites`は直前に読むとよいページのIDで、ビルドが存在と循環のなさを検証し、サイドバーの項目に「前提：…」として表示します。`related`は編集用メタデータです。ページ移動と大まかな読む順序はサイドバーにまとめ、本文には教材の案内・次に読むページ・自動の関連リンク一覧を付けません。新規ページを実装するときは、このページ内のファイルと目次だけで作業できます。

出典は本文の `source:` と `sources.yml` のキーを対応させます。元URL、書誌・図番号・版・加工・利用条件・確認日を、確認できた範囲で記録します。移行した出典の未確認事項を、確認済みに書き換えないでください。既存素材の詳細な履歴は [素材記録](content/shared/media-provenance.md) を引き継ぎ、各図のキャプションにも条件を残しています。共有素材は `assets/`、単独ページだけで使う素材は `media/` に配置しています。配布物にはページから参照されるファイルだけをコピーします。ページのJavaScriptが実行時に読み込む素材は、Markdown冒頭の `runtime_assets` にページフォルダからのパターン（例：`media/sam2-input-*.jpg`）で宣言してください。どこからも参照されない画像・音声・動画や部品を置くと `npm test` が失敗します。2026-09-24に未使用の旧素材を削除しました（Git履歴から復元できます。内容は素材記録の冒頭）。

## ビルドと検証

開発に必要なのは **Node.js 22.17以上とnpmだけ**です。Python・pip・仮想環境は使いません。

初回はロックファイルどおりに依存パッケージを導入します。

```sh
npm ci
npm run build
npm test
```

本文・素材を編集した後は `npm run build` を実行し、正本とともに直下の `index.html` と `dist/` の更新もコミットしてください。閲覧者はこの生成済みHTMLを使います。`node_modules/` と検証結果の `test-results/` はGitに含めません。パッケージ導入後のビルドはオフラインで実行できます。

ビルドはMarkdown、目次、テンプレート、同梱KaTeXからHTMLを生成し、重複ID・内部リンク・アンカー・素材を検証します。画像生成や研究モデルの実行は行わず、保存済みの素材を使います。ビルドは出力先を作り直すため、削除したページや素材は残りません。15MBを超えるファイルはエラーにします。大きな動画は再圧縮してください。検索索引・`sitemap.xml`・正規URLとOGP（共有時の表示）もビルドで生成します。別の出力先は `npm run build -- --output <フォルダ>` で指定できます。出力先には、空のフォルダか以前のビルド結果を指定してください。

ブラウザ検証はnpm版Playwrightを使います。Chromiumの導入は初回だけ必要です。

```sh
npm run browser:install
npm run test:browser
```

`file://`・オフラインで、全ページの画面幅320/390/1440px、JavaScript有効／無効、操作部品、検索、配色の切り替え、明暗両方の配色での文字のコントラスト（3:1以上）、音声・動画の再生を検証します。H.264を再生できないChromium（オープンソース版など）では、動画再生の確認だけを省き、結果に記録します。導入済みの別のChromiumを使う場合は `CHROMIUM_PATH=<実行ファイル> npm run test:browser` とします。結果は `test-results/browser/` に保存します。別の配布フォルダには `npm run test:browser -- --site <フォルダ>` を使います。

その他の検証コマンドは次のとおりです。

| コマンド | 内容 |
|---|---|
| `npm run check:dist` | ビルドし直して、コミット済みの `index.html`・`dist/` と差がないか確認 |
| `npm run check:sources` | 一次資料の確認が済んでいない出典をページごとに集計（`-- --list` で一覧） |
| `npm run check:links` | 外部の出典URLに実際に接続して確認（ネット接続が必要）。到達できても内容の確認済みとは扱わない |

GitHub Actionsの「Checks」は、プルリクエストと手動実行で上の検証とブラウザ検証を行います。公開はしません。外部URLの確認は手動実行時に選べます。

旧Python製のビルド・検証・作図コードは [制作履歴](docs/legacy-python/README.md) に保管しています。現行の開発からは呼び出しません。本文はMarkdown、図や操作は各ページの `components/`、画像等は `media/` を編集してください。

## 設計と記録

[設計](docs/design.md) / [再構成設計](docs/restructure-design.md) / [収録項目計画](docs/content-plan.md)

過去の計画・移行報告・試読レビュー・QA記録は [docs/archive/](docs/archive/README.md)、日付ごとの検証結果は [docs/verification/](docs/verification/README.md) にあります。いずれも当時の記録で、現在の構成を表すものではありません。

B3相当の読者による試読と読了時間の計測は未実施です。読者からの指摘は、GitHubのIssueテンプレート「読者からの感想・指摘」で受け付けます。

## GitHub Pagesへの公開

公開先は https://edoaki.github.io/ml-landscape/ です。GitHub Pagesには生成済みの `dist/` を配信します。

**pushと公開は、ユーザーが明示的に指示したときだけ行います。** 通常の編集・ビルド・テストではアップロードしません。詳細は [AGENTS.md](AGENTS.md) を参照してください。

公開を指示された際はビルド・検証後にGitHubへpushし、Actionsの「Publish GitHub Pages (manual)」を `main` で手動実行します。pushしただけでは公開されません。
