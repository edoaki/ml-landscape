# 基盤モデルの学習・適応：LLM中心への改稿

2026-09-20。対象は `content/questions/foundation-models/`。設計文書の対応する説明範囲も同期した。

- 算数を教えるLLMの共通例で、事前学習の次トークン予測、SFTの回答部分の損失、生成・採点・更新を繰り返す強化学習を説明。
- RLHF / RLVRという報酬の由来と、PPO / GRPOという更新方法を区別。報酬モデル・価値モデル・参照モデル・生成時の方策の役割を説明。
- GRPOの結果報酬の設定に限定した4回答の数値例を追加。報酬1, 0, 1, 0から平均0.5、母標準偏差0.5、アドバンテージ+1, −1, +1, −1を得る。数値例は研究結果ではない。
- DPO、DeepSeek-R1の多段階学習、未知問題での評価、ICL / RAGとの違いを追加・改稿。出典と確認範囲はページの `sources.yml` に記録。

## 検証

- `.venv/bin/python build.py`：51ページ生成。リンク・ID・素材参照を検証。
- `.venv/bin/python -m unittest discover -s tests -p test_content.py -v`：5件成功。
- `.venv/bin/python -m unittest discover -s tests -p test_landscape.py -v`：2件成功。
- Chromium：幅320 / 390 / 1440、JavaScript有効 / 無効の6条件をオフラインで確認。横方向のページはみ出しなし、数式3個、図5個、JavaScript例外・KaTeXエラーなし。詳細は `checks.json`。
- 幅390 / 1440で各図と全ページを保存。図のキャプチャに固定ヘッダーが重ならないよう、保存時だけヘッダーを非表示にした。本文・図のレイアウトは変更していない。
- 本文の記述だけを用いて、事前学習・SFT・RL・GRPO・DPO・ICLの目的、学習信号、例、相互の違いを短く説明できるか制作側で点検した。初学者による試読は未実施。
