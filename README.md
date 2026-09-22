# 機械学習の全体像

[教材を開く](index.html)

clone後、プロジェクト直下の `index.html` または `dist/index.html` をブラウザで直接開けます。生成済みの `dist/` をGitに含めているため、閲覧にNode.js・npm・Pythonのインストール、ビルド、サーバー、ネット接続は不要です。本文・数式・静止図はJavaScript無効時も読めます。操作部品にはJavaScriptを使います。外部論文・外部配信動画には接続が必要で、音声・動画は再生操作をしたときに再生します。

目次は「はじめに → 基礎 → 分野・タスク → 横断研究 → モデル」です。「準備中」は本文未公開、「拡充予定」は既存説明があり、計画上の追加範囲が残るページです。詳説の分量を一律にはそろえていません。

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
| 共有素材・履歴 | `assets/`、`content/shared/media-provenance.md` |
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

メタデータの `status` は `planned`（本文未公開）、`partial`（既存内容あり・拡充予定）、`migrated`（既存内容移行）、`ready`（本文整備済み）。収録決定と完成度を区別し、`scope`に予定範囲、`origins`に移行元を記録します。`prerequisites`と`related`は編集用メタデータです。ページ移動と大まかな読む順序はサイドバーにまとめ、本文には教材の案内・次に読むページ・自動の関連リンク一覧を付けません。新規ページを実装するときは、このページ内のファイルと目次だけで作業できます。

出典は本文の `source:` と `sources.yml` のキーを対応させます。元URL、書誌・図番号・版・加工・利用条件・確認日を、確認できた範囲で記録します。移行した出典の未確認事項を、確認済みに書き換えないでください。既存素材の詳細な履歴は [素材記録](content/shared/media-provenance.md) を引き継ぎ、各図のキャプションにも条件を残しています。共有素材とJavaScriptから参照する素材は `assets/`、単独ページだけで使う素材は `media/` に配置しています。元の素材は削除していません。

## ビルドと検証

開発に必要なのは **Node.js 22.17以上とnpmだけ**です。Python・pip・仮想環境は使いません。

初回はロックファイルどおりに依存パッケージを導入します。

```sh
npm ci
npm run build
npm test
```

本文・素材を編集した後は `npm run build` を実行し、正本とともに直下の `index.html` と `dist/` の更新もコミットしてください。閲覧者はこの生成済みHTMLを使います。`node_modules/` と検証結果の `test-results/` はGitに含めません。パッケージ導入後のビルドはオフラインで実行できます。

ビルドはMarkdown、目次、テンプレート、同梱KaTeXからHTMLを生成し、重複ID・内部リンク・アンカー・素材を検証します。画像生成や研究モデルの実行は行わず、保存済みの素材を使います。別の出力先は `npm run build -- --output <フォルダ>` で指定できます。出力先は配布専用フォルダを指定してください。

ブラウザ検証はnpm版Playwrightを使います。Chromiumの導入は初回だけ必要です。

```sh
npm run browser:install
npm run test:browser
```

`file://`・オフラインで、全ページの画面幅320/390/1440px、JavaScript有効／無効、操作部品、音声・動画の再生を検証します。結果は `test-results/browser/` に保存します。別の配布フォルダには `npm run test:browser -- --site <フォルダ>` を使います。

旧Python製のビルド・検証・作図コードは [制作履歴](docs/legacy-python/README.md) に保管しています。現行の開発からは呼び出しません。本文はMarkdown、図や操作は各ページの `components/`、画像等は `media/` を編集してください。

## 設計と今回の確認

既存の拡充予定25ページを、具体例を中心に整備しました。8か所の操作図を追加しました。[拡充内容と検証記録](docs/expansion-report.md)を参照してください。新規の操作検証は `npm run test:browser` で再実行できます。

[再構成設計](docs/restructure-design.md) / [収録項目計画](docs/content-plan.md) / [移行結果と残作業](docs/migration-report.md)

[QA.md](QA.md)は過去の制作記録を含みます。今回の検証は日付付きの移行記録に分けています。B3相当の読者による試読と読了時間の計測は未実施です。

## GitHub Pagesへの公開

公開先は https://edoaki.github.io/ml-landscape/ です。GitHub Pagesには生成済みの `dist/` を配信します。

**pushと公開は、ユーザーが明示的に指示したときだけ行います。** 通常の編集・ビルド・テストではアップロードしません。詳細は [AGENTS.md](AGENTS.md) を参照してください。

公開を指示された際はビルド・検証後にGitHubへpushし、Actionsの「Publish GitHub Pages (manual)」を `main` で手動実行します。pushしただけでは公開されません。
