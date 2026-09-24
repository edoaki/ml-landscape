# 共有素材

複数ページで使う画像・動画・スクリプト・スタイルと、ページのJavaScriptから読み込む素材を置いています。1ページだけで使う素材は各ページの `media/`、専用の図・操作は `components/` に置きます。

- 素材の出典・加工・利用条件：[素材記録](../content/shared/media-provenance.md)
- どのページがどの素材を使うか：[素材の所属](../content/shared/media-ownership.yml)
- 配布物（`dist/`）には、ページから参照されるファイルとライセンス本文だけがコピーされます。参照されない画像・動画を置くと `npm test` が失敗します。
- `og-image.png`（共有用画像）の元図は [source/og-image.svg](../source/og-image.svg) です。
