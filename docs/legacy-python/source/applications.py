from common import *
import task_figures
from decision import decision_body, optimization_body

def tasktable(rows):return table(['タスク','入力 → 出力','実問題と、違いを見る点'],rows)
def build():
 from vision import body as vision_body
 page('vision','画像 — ラベルから画素の構造へ','タスクと実問題','03 / VISION','何があるか、どこにあるか、どの画素か、どれだけ遠いか。図で比べながら、画像のタスクを一つずつ見ていきます。',vision_body())
 from spatial import body as spatial_body
 page('spatial','動画・3D — 時間と空間をつなぐ','タスクと実問題','03 / VIDEO & SPACE','動画の対象を追う、カメラの位置を知る、写真から別の視点を作る、操作に応じて次の画面を生成する。画像から広がるAIの用途を、実際の結果と映像で紹介します。',spatial_body())
 from language import body as language_body
 page('language','自然言語処理 +α — LLMとVLM','タスクと実問題','03 / LANGUAGE & MULTIMODAL','文章に資料や画像をつなぐ。VLMの回答生成とCLIPの画像・文章の照合を、具体例と図で見ていきます。',language_body())
 from audio_lesson import body as audio_body
 page('audio','音声・音楽 — 音を聞き、作り、分ける','タスクと実問題','03 / AUDIO','話し声から文字へ、文章から音声や音楽へ、混ざった曲から一つの音へ。入力と出力を、短い試聴デモで比べます。',audio_body())
 from timeseries import body as timeseries_body
 body=timeseries_body()
 from recommendation import body as recommendation_body
 body+=recommendation_body()
 body+=sec('graphs','グラフ：点、関係、全体の性質',task_figures.graph_tasks()+tasktable([('ノード分類','関係グラフ → 点の属性','文献の分野。特徴と引用の構造を合わせる。'),('リンク予測','グラフ → 未知の関係のスコア','知識グラフの補完、推薦。偽の辺をどう用意するかも評価条件。'),('グラフ全体の回帰・分類','分子グラフ → 性質','溶解度・材料特性。分子骨格の違う対象へ汎化するか。')])+p('構造は<a href="gnn.html">GNNページ</a>のreadoutへつながります。何を未知として残すかによって評価の難しさは変わります。既知グラフ内の未ラベル点と、別の分子や別のグラフへ適用する問題は同じではありません。'))
 body+=refs([('TimesFM 著者実装','https://github.com/google-research/timesfm'),('Merlion 著者実装・チュートリアル','https://github.com/salesforce/Merlion'),('GraphSAGE','https://arxiv.org/abs/1706.02216')])
 page('time-graphs','時系列・推薦・グラフ — 変化と関係を読む','タスクと実問題','03 / TIME & RELATIONS','未来を予測すること、異常を検知すること、候補を順位付けすること。関係構造と評価条件に注目します。',body)
 page('decision-science','強化学習・意思決定 — 行動と結果をつなぐ','タスクと実問題','03 / DECISION MAKING','観測から行動を選び、その結果から学ぶ。AlphaGoからゲーム、世界モデル、組合せ最適化、ロボットへ。図と動画で行動の選び方を見ます。',decision_body())
 from science import body as science_body
 page('science','科学応用 — 研究にどう役立つ？','タスクと実問題','03 / AI FOR SCIENCE','AIが科学研究で何に役立つか。「何を入れると、何が出るか」を6つの例で見ていきます。',science_body())
