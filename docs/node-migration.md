# Node.jsへの開発環境移行（2026-09-22）

## 開発と配布

- 開発環境はNode.js 22.17以上とnpm。`npm ci`、`npm run build`、`npm test`を使用する。
- 閲覧者はclone後に`index.html`または`dist/index.html`を直接開く。インストール・ビルド・サーバーは不要。
- `dist/`をGitの除外対象から外した。教材を変更した際は正本と生成済みHTMLを一緒にコミットする。
- `node_modules/`と`test-results/`は配布しない。

## 実装

`build.mjs`と`scripts/render-content.mjs`が、Markdown・YAML・HTMLテンプレート・同梱KaTeXを処理する。ページID、目次、ページ間リンク、出典、素材、数式、Markdownを含むHTMLブロック、見出しの属性を従来どおり扱う。日本語の強調と単独の矢印の強調も維持した。

KaTeXはNode.jsから直接呼び出す。外部プロセスやPython環境は使わない。生成物のリンクは相対パスとし、file://とサブディレクトリ配信に対応する。

静的検証・教材の数値計算・ブラウザ検証をNode.jsへ移した。ブラウザ検証はnpm版Playwrightで実行する。過去のPythonコードは`docs/legacy-python/`に移し、制作履歴として保管する。素材の実験条件を示す既存のリンクも保管先へ更新した。

## 検証

- 全51ページの生成、内部リンク・アンカー・素材・重複IDの検査。
- 移行前後の本文テキスト（空白を除く）と、見出し・表・画像・SVG・数式・詳細表示・図・リンク・太字の個数が全51ページで一致。
- Node.jsテスト9件と既存SSMアニメーションテスト。
- Git除外規則に従って別の空フォルダへファイルをコピーし、Python仮想環境・node_modulesがない状態から`npm ci`、ビルド、テストを実行。
- 別の空の配布先へ生成した583ファイルと、同梱する`dist/`の対応ファイルがバイト単位で一致。
- 画面幅320/390/1440pxとJavaScript有効／無効の306条件、および6群の操作検証（音声・動画のオフライン再生、段階操作、数値、キーボード、タイマーを含む）が成功。
- ブラウザ検証の結果は`npm run test:browser`で再生成し、`test-results/browser/browser-results.json`へ保存する。
