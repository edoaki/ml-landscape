# Repository working guidelines

## Publishing requires an explicit instruction

- 通常の編集・修正・ビルド・テストはローカルで行う。
- ユーザーが明示的に指示したときだけ、GitHubへのpush、PRの作成・更新、GitHub Pagesへの公開・再公開、その他の外部アップロードを行う。
- 「修正して」「作業して」「ビルドして」などの依頼だけでは、pushや公開の許可と解釈しない。
- 過去のpush・公開の許可は、そのときの依頼に限る。後続の作業に引き継がない。
- GitHub Pagesは手動実行（workflow_dispatch）のみとし、push・スケジュール等で自動公開する設定を追加しない。
- pushだけを指示された場合は、Pagesの公開を実行しない。公開も指示された場合に手動ワークフローを実行する。

## Development

- 開発環境はNode.js 22.17以上とnpmのみ。Python環境を導入・利用しない。
- 初回は `npm ci`、本文や素材の更新後は `npm run build`、検証は `npm test` を使う。
- ブラウザ検証は初回に `npm run browser:install`、以後は `npm run test:browser` を使う。
- `dist/` は生成済みの配布物としてGit管理する。本文や素材を変更したら再生成し、公開を指示された際は正本と生成物を一緒に反映する。
- 閲覧者は `index.html` または `dist/index.html` を直接開ける状態を維持する。
- `docs/legacy-python/` は制作履歴であり、現行の開発手順では使わない。

## Navigation and validation

- Before broad inspection, identify applicable instructions, repository structure, and the likely change surface.
- Prefer targeted searches and read only the smallest useful scope.
- Identify affected files and tests before editing; validate narrowly before broadening checks.
