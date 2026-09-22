"""Transformer: motivation, contextual representations, then internal calculation."""
from common import *
import transformer_figures as diagrams


def build():
 body=sec('why','なぜTransformerが作られたのか',
  p('翻訳などで文章を扱うときは、離れた単語の関係も使いたくなります。例えば「私は家族と東京に住んでいる」なら、「住んでいる」を理解するには、誰が、誰と、どこに住むのかを結び付ける必要があります。')+
  p('前のページのRNN・LSTMは、ここまでの情報を状態にまとめ、次の単語へ渡します。ただし、<strong>次の状態を作るには、前の状態ができるのを待つ</strong>必要があります。学習でも一つの文の位置方向を並列化しにくく、離れた位置の情報は多くの更新を経由します。LSTMは記憶を保持しやすくしますが、この順次処理の制約は残ります。')+
  diagrams.motivation()+
  p('そこで、「前から順に状態を渡す代わりに、必要な位置の情報を直接参照して、それぞれの表現を更新できないか」と考えます。これを担うのが<strong>Self-Attention</strong>です。同じ層の入力がそろえば、各位置の更新を行列演算でまとめて計算できます。')+
  p('AttentionはTransformer以前から、RNNを使う翻訳モデルなどで利用されていました。2017年のTransformerは、系列に沿った再帰や畳み込みを使わず、Attentionを中心にEncoderとDecoderを組み立て、翻訳の品質と学習の並列性を両立させました。<a href="https://arxiv.org/abs/1706.03762">原論文：Attention Is All You Need</a>。')+
  note('Transformerの設計思想','要素間の関係に応じて、必要な情報を直接集める。その計算を各位置で並列に行い、層を重ねて表現を更新する。文章を生成する際の「次の単語を一つずつ出す」処理は、別に必要になる。'))

 body+=sec('structure','Transformerの構造：ブロックをN層重ねる',
  p('Transformerは、位置ごとのベクトルを受け取り、<strong>Attentionで要素間の情報を交換し、FFNで各位置の特徴を加工するブロック</strong>を重ねます。まず全体の流れと1ブロックの構造を見てから、Attentionの中の計算へ進みます。')+
  diagrams.overview()+
  sub('Attentionの後に、各位置の特徴を加工する',
   p('図は上から下へ読みます。横に並ぶ列は、文章中の位置1〜4です。Attentionでは列の間で情報を交換し、FFNでは各列を独立に加工します。残差接続とLayerNormは、情報を引き継ぎながら学習を安定させる役割を持ちます。')+
   diagrams.block()))

 body+=sec('attention','Self-Attention：関係に応じて情報を集める',
  p('Self-Attentionの「Self」は、同じ系列の中で参照し合うという意味です。「どこから、どれくらい情報を取り込むか」を、今の表現から毎回計算します。まず1 headの処理を見ます。')+
  sub('1. 同じ表現から、Q・K・Vを作る',
   diagrams.qkv()+
   p('<strong>Query（Q）</strong>は参照する側の特徴、<strong>Key（K）</strong>は照合される側の特徴、<strong>Value（V）</strong>は実際に集める内容です。例えばliveのQを各単語のKと照合し、その結果に応じて各単語のVを集めます。')+
   eq(r'Q=XW_Q,\qquad K=XW_K,\qquad V=XW_V','W_Q・W_K・W_Vはそれぞれ別の学習可能な行列。同じ層・headの中では、各位置に同じ行列を使う。QとKは内積を取れる同じ次元dₖを持つ。'))+
  sub('2. QとKの内積を、取り込む割合に変える',
   p('参照する位置iのqᵢと、参照先jのkⱼの内積を取ります。<strong>内積の値が高い = 関連度が高い</strong>と考えます。ここでの関連度は、このheadで情報を取り込むための照合の強さです。これは学習した特徴どうしの適合度で、「単語の意味が似ているか」だけを測るものではありません。')+
   eq(r's_{ij}=\frac{q_i k_j^{\mathsf T}}{\sqrt{d_k}},\qquad a_{ij}=\frac{\exp(s_{ij})}{\sum_m\exp(s_{im})}','√dₖでスコアの尺度を調整し、参照先に沿ってsoftmaxを取る。一つのqueryについて重みの和は1になる。')+
   diagrams.scores())+
  sub('3. Vの重み付き和を、全ての位置で求める',
   p('<strong>関連度が高いものほど重みが大きくなり、そのVの方へ重心が寄ります。</strong>重み付きの足し合わせを、Vの空間で「重心に移動する」と捉えたのが下の図です。')+
   diagrams.mix()+
   eq(r'z_i=\sum_j a_{ij}v_j,\qquad Z=AV','係数aᵢⱼでvⱼを重み付けし、足したものが位置iの集約結果zᵢ。全位置の計算を行列でまとめるとZ=AVになる。')+
   p('liveだけでなく、IもTokyoもwithも、それぞれ自分のQで重みを求めます。<strong>同じ層では更新前の表現から、全位置の集約結果をまとめて作ります。</strong>先に更新した単語を、その層の別の単語の計算へ順に渡すわけではありません。')+
   p('学習して保存するのは射影行列などのパラメータです。Attentionの重みaᵢⱼは入力から計算する値なので、文や層が変われば変わります。')))

 body+=sec('block','1層の中身：情報交換と、各要素の特徴の加工',
  sub('Multi-head：複数の見方で情報を集める',
   p('一つの照合だけではなく、異なるQ・K・Vの射影を使って複数の集約を並列に行います。これが<strong>Multi-head Attention</strong>です。各headの結果を連結し、出力の行列W_Oで組み合わせます。各headが「文法」「場所」などの人間の概念に一対一で対応するとは限りません。')+
   diagrams.heads())+
  sub('Attentionの後に、各位置の特徴を加工する',
   p('<strong>Attentionは要素間の情報交換、FFNは各要素の特徴の加工</strong>を担います。FFN（feed-forward network、MLPとも呼びます）は、各位置に同じ重みで適用する非線形変換です。位置同士を直接混ぜず、集めた情報から予測に役立つ特徴を作ります。')+
   eq(r'\operatorname{FFN}(h_i)=\phi(h_iW_1+b_1)W_2+b_2','φはReLUなどの非線形関数。原論文はReLUを使用。Attentionにもsoftmaxや入力依存の重みがあるので、Attention全体が単なる線形変換という意味ではない。'))+
  sub('残差接続とLayerNormが、更新を支える',
   p('<strong>残差接続</strong>は、処理の入力をその出力に足す経路です。元の情報を直接引き継ぎながら変化分を加え、深いモデルへ学習の信号を伝えやすくします。<strong>LayerNorm</strong>は各トークン内の特徴を正規化し、学習を安定させるために使います。')+
   eq(r'\begin{aligned} U&=\operatorname{LayerNorm}(H^{\ell-1}+\operatorname{MHA}(H^{\ell-1}))\\ H^\ell&=\operatorname{LayerNorm}(U+\operatorname{FFN}(U))\end{aligned}','原論文のPost-LN型を、dropoutを省いて表した式。Attention側とFFN側の両方に残差接続がある。処理の前に正規化するPre-LN型もある。')+
   p('このブロックを重ねたものがTransformerです。通常、層ごとに別のパラメータを持ちます。<a href="#representations">後半のGPTの図</a>では、このブロックを一つ通るたびに全ての点が移動します。移動はAttentionだけの重心移動ではなく、残差・正規化・FFNまで含む表現の更新を表しています。')))

 body+=sec('gpt','GPT：入力から次のトークンの確率へ',
  p('ここからはGPT型の文章生成を、入力から出力まで追います。GPTはDecoder-onlyのTransformerで、自身と過去だけを参照する因果マスクを使って、次のトークンを予測します。'))

 body+=sec('tokens','入力を、位置のあるベクトル列へ',
  p('文章を<strong>トークン</strong>と呼ぶ単位に分け、それぞれをd個の数からなる<strong>埋め込み</strong>へ変換します。次の図では分かりやすく1単語を1点にしましたが、実際のトークンは一文字や一単語と一致するとは限りません。n個のトークンの表現を行に並べると、n×dの行列Xになります。')+
  diagrams.embedding()+
  p('Self-Attentionの照合だけでは、単語の並び順を区別する手がかりがありません。そこで位置情報を加えます。原論文では埋め込みに位置を表すベクトルを足します。次の図の「ベクトル化」は、この準備が済んだ状態です。画像ならパッチなどを要素として、同様の処理へ渡せます。'))

 body+=sec('representations','要素間の関係をもとに、表現を書き換えていく',
  p('<strong>Transformerは、要素間の関係をもとに、それぞれの表現を文脈に応じて書き換えていくモデルです。</strong>ここで「表現」とは、その要素の特徴を数値にしたベクトルのことです。単語の文字列を書き換えるのではなく、その単語が文の中で持つ情報を更新します。')+
  p('入力は <strong>I live in Tokyo with</strong>。各位置が自身と過去の情報を取り込みます。最終のN層では最後のwithの表現に注目し、出力層でその次に続くトークンの確率を求めます。')+
  diagrams.representation()+
  p('一つの層では、各要素が過去の要素や自分自身から情報を集め、さらに自分の特徴を加工します。次の層では、<strong>更新された表現を使って関係を計算し直します</strong>。そのため、同じ単語でも入力文や層によって表現が変わります。このような表現を、文脈に応じた表現と呼びます。')+
  p('点の数が減って文全体が一つの点になるわけではありません。各位置の表現を残したまま更新し、生成時には最終層の最後の位置の表現を、全結合層とsoftmaxへ渡します。familyなどの候補から次のトークンを選び、入力に追加して同じ処理を繰り返します。図の横方向は単語の並び順ではなく、表現を見せるための座標です。'))

 body+=sec('train-use','文章を学ぶときと、文章を作るとき',
  p('次トークン予測の学習では、「猫 が 眠る」に対して「猫→が」「猫 が→眠る」という正解を用意します。因果マスクで未来を隠せば、用意した一つの文の各位置の予測と損失をまとめて計算できます。誤差を逆伝播し、埋め込みや各層のパラメータを更新します。')+
  flow([('猫','入力',BLUE),('次トークンを予測','P(語 | 猫)'),('「が」を選んで追加','猫 が',ORANGE),('再び次を予測','P(語 | 猫 が)')],'生成時は、選んだトークンを入力に追加して繰り返す。学習時の位置方向の並列計算と、生成時の逐次処理を区別する。')+
  p('通常の自己回帰生成では、次の入力がまだ決まっていないため一つずつ進みます。KV cacheは過去のK・Vを保存して、同じ計算の繰り返しを減らす仕組みです。')+
  p('離れた要素を直接参照できる一方、通常の密なSelf-Attentionではn×nの関係を扱うため、長い系列ほど計算が増えます。生成では過去のK・Vを保存するメモリも必要です。要素間の関係を広く扱える利点と、その計算・メモリの負担が対になっています。')+
  p('Attentionの重みは情報を集める割合であり、それだけで最終的な判断の原因を説明し切れるわけではありません。詳しくは<a href="xai-advanced.html#llm">内部への介入による分析</a>へつながります。'))

 body+=sec('masks','EncoderとDecoderを見比べる',
  p('Encoderは入力全体から各位置の表現を作り、Decoderはそれまでの出力を使って続きを予測します。翻訳のEncoder–Decoder型では、この二つをつなぎ、Decoderが入力文の情報も参照します。')+
  diagrams.encoder_decoder()+
  p('Decoderの<strong>Self-Attention</strong>は、生成途中の文の情報を集めます。続く<strong>Cross-Attention</strong>は、Encoderが作った入力文の表現から必要な情報を取り込みます。その後、Feed Forwardで各位置の特徴を加工します。')+
  table(['モデルの構成','使うブロック','出力へのつなぎ方'],[
   ('Encoder-only（BERTなど）','Self-Attention → Feed Forward','入力の表現を分類や穴埋め予測などに使う'),
   ('Decoder-only（GPTなど）','Self-Attention → Feed Forward','次のトークンを予測する。別のEncoderやCross-Attentionは持たない'),
   ('Encoder–Decoder（原論文の翻訳）','Encoder ＋ Cross-Attentionを持つDecoder','入力文を参照しながら、出力文を生成する')])+
  sub('Self-AttentionとCross-Attention：Q・K・Vの出どころが違う',
   diagrams.attention_comparison()+
   p('<strong>Self-Attention：</strong>同じ系列の表現からQ・K・Vを作ります。「self」は自分一つだけを見るという意味ではなく、同じ系列内の位置を参照するという意味です。')+
   p('<strong>Cross-Attention：</strong>QはDecoder側、KとVはEncoderの最終出力から作ります。Decoder側のQで入力文のKとの関連度を求め、その重みに応じて入力文のVを足し合わせます。結果はDecoder側の各位置の表現に取り込まれます。')+
   p('例えば「I have a cat」を訳すとき、Decoderは「私は」という生成途中の文を使いつつ、Cross-Attentionで入力文を参照して続きを予測します。入力文と出力文は、長さが同じでなくても構いません。')+
   p('どちらも「QとKの内積 → softmax → Vの重み付き和」という計算を使います。違うのは、<strong>同じ系列から集めるか、別の系列から集めるか</strong>です。'))+
  p('画像への応用は、補足ページの<a href="vit.html">ViT・VLM — Transformerを画像へ広げる</a>へ。画像のパッチを要素として扱う仕組みと、画像を見て文章で答えるまでを図で追います。'))

 body+=refs([('Attention Is All You Need（2017）：設計の背景・構造・計算','https://arxiv.org/abs/1706.03762'),('BERT（2018）','https://arxiv.org/abs/1810.04805')])
 page('transformer','Transformer — 関係をもとに表現を更新する','モデルの構造','MODEL 03 / ATTENTION','なぜ生まれたのか。要素間の関係をもとに、各要素の表現をどう書き換えるのか。全体構造から内部の計算を理解し、GPTが入力から次のトークンの確率を出すまでを図で追います。',body)
