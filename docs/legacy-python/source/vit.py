"""Transformer supplement: image tokens, classification and visual language input."""
from common import *


def cat():
 return '<rect width="160" height="160" fill="#faf7ef"/><ellipse cx="83" cy="135" rx="54" ry="7" fill="#dfe4da"/><path d="M43 103Q7 103 22 60" fill="none" stroke="#b98350" stroke-width="13" stroke-linecap="round"/><ellipse cx="71" cy="100" rx="39" ry="27" fill="#c99361"/><path d="M86 73L86 32L108 49L131 33L140 75Z" fill="#c99361"/><ellipse cx="112" cy="77" rx="32" ry="28" fill="#c99361"/><path d="M92 48L93 36L102 49M123 49L131 39L134 53" fill="#dfad9e"/><path d="M47 80L54 96M65 76L71 91M105 53L110 65M117 51L121 64" stroke="#8e603d" stroke-width="5" stroke-linecap="round"/><circle cx="103" cy="77" r="3" fill="#34483d"/><circle cx="126" cy="77" r="3" fill="#34483d"/><path d="M111 86L119 86L115 91Z" fill="#a96163"/><path d="M42 118H70M88 118H116" stroke="#c99361" stroke-width="13" stroke-linecap="round"/>'


def picture(x,y,size=140,patch=None):
 unit=160 if patch is None else 80
 dx=0 if patch is None else (patch%2)*80
 dy=0 if patch is None else (patch//2)*80
 clip=f'vit-crop-{x}-{y}'
 return f'<defs><clipPath id="{clip}"><rect x="{x}" y="{y}" width="{size}" height="{size}"/></clipPath></defs><g clip-path="url(#{clip})"><g transform="translate({x} {y}) scale({size/unit})"><g transform="translate({-dx} {-dy})">{cat()}</g></g></g><rect x="{x}" y="{y}" width="{size}" height="{size}" fill="none" stroke="#b7c4b5"/>'



def dot(x,y,label,color=BLUE):
 return f'<circle cx="{x}" cy="{y}" r="15" fill="{color}"/>'+txt(x,y+5,label,12,'white')


def patches():
 b=txt(108,30,'画像',18)+picture(28,57,160)
 b+=line(108,57,108,217,arrow=False)+line(28,137,188,137,arrow=False)
 b+=txt(108,247,'小さな領域に分割',14)+line(200,137,237,137)
 for i in range(4):
  x=259+i*127
  b+=picture(x,70,78,i)+txt(x+39,171,f'パッチ {i+1}',13)
  b+=line(x+39,183,x+39,204)+box(x+1,211,76,48,'線形射影',color=BLUE)
  b+=line(x+39,266,x+39,288)+dot(x+39,313,str(i+1))
 b+=txt(108,315,'各パッチを',15)+txt(108,337,'同じ長さのベクトルへ',15)
 b+=box(247,350,480,44,'＋ 位置埋め込み：元の画像のどこにあったか',color=GREEN)
 return figure(svg(b,415,label='猫の画像を4パッチに分割し、線形射影と位置埋め込みでベクトル列にする'),'値や分割数などは説明用のものです。')


def classifier():
 b=txt(400,27,'パッチとCLSが、層ごとに情報を交換する',18)
 for i in range(5):
  x=170+i*115;c=ORANGE if i==0 else BLUE;label='CLS' if i==0 else str(i)
  b+=dot(x,66,label,c)+line(x,85,x,117)
 b+=box(100,123,600,65,'Transformer Encoder × N層','Attentionで情報交換 → 各位置の特徴を加工')
 for i in range(5):
  x=170+i*115
  b+=line(x,194,x,219)+dot(x,241,'CLS' if i==0 else str(i),ORANGE if i==0 else PURPLE)
 b+=txt(461,281,'文脈を含んだ各パッチの表現',14,PURPLE)
 b+=line(170,261,170,307,ORANGE)+box(70,315,200,55,'全結合層 → softmax',color=ORANGE)
 b+=line(280,342,335,342)+txt(173,401,'最終層のCLSから分類',14,ORANGE)
 for i,(word,prob) in enumerate([('猫',.82),('犬',.12),('羊',.06)]):
  y=307+i*39
  b+=txt(370,y+5,word,16)+f'<rect x="397" y="{y-10}" width="{prob*300}" height="20" rx="3" fill="{GREEN}"/>'+txt(699,y+5,f'{prob:.0%}',14)
 return figure(svg(b,430,label='CLSと画像パッチをTransformerに通し、最後のCLSから猫・犬・羊の分類確率を求める'),'値などは説明用のものです。')


def multimodal():
 b=txt(197,27,'画像',18)+picture(144,46,106)+txt(568,27,'質問文',18)
 b+=box(398,64,340,64,'何のイラストですか？',color=ORANGE)
 b+=line(197,160,197,182)+box(52,190,290,55,'画像エンコーダ（ViTなど）',color=BLUE)
 b+=line(197,252,197,274)+box(52,282,290,55,'接続層（線形層・MLP）','LLMに渡せる次元・表現へ',BLUE)
 b+=line(568,136,568,274)+box(398,282,340,55,'トークン化 → 埋め込み',color=ORANGE)
 b+=line(197,345,197,368)+line(568,345,568,368)
 for i in range(4):b+=dot(103+i*63,397,str(i+1),BLUE)
 for i,t in enumerate(['何','の','…','？']):b+=dot(470+i*63,397,t,ORANGE)
 b+=txt(379,402,'＋',23)+txt(197,436,'画像由来のベクトル列',14,BLUE)+txt(568,436,'文章由来のベクトル列',14,ORANGE)
 b+=line(197,445,197,467)+line(568,445,568,467)
 b+=box(52,474,686,59,'LLM：画像と文章の関係を使い、次のトークンを予測','生成したトークンを追加して、続きを繰り返し予測する')
 b+=line(395,540,395,562)+box(155,570,480,50,'猫のイラストです。',color=GREEN)
 return figure(svg(b,640,label='画像エンコーダと接続層で作った画像ベクトルを質問文のベクトルとLLMに渡し、回答を生成する'),'LLaVA型の構成を簡略化した図。回答は説明用のものです。')


def build():
 body=sec('bridge','Transformerを、画像にも使う',
  p('<a href="transformer.html">Transformer</a>では、要素間の関係をもとに各要素の表現を書き換えました。要素を単語から<strong>画像の小領域</strong>に変えると、同じ仕組みを画像に使えます。さらに画像と文章の表現をつなぐと、画像を見て質問に答えるモデルへ進めます。'))
 body+=sec('patches','ViT：画像をパッチのベクトル列へ',
  p('<strong>ViT（Vision Transformer）</strong>は、画像を小さな領域（パッチ）に分け、Transformerで処理するモデルです。言語で使われていたTransformerを、画像認識にも適用できるかという発想から提案されました。')+
  patches()+
  p('各パッチの画素値を一列に並べ、学習する線形層で同じ長さのベクトルに変換します。さらに<strong>位置埋め込み</strong>を足し、画像内の位置を区別できるようにします。')+
  p('例えば224×224画素の画像を16×16画素ずつに分けると、14×14＝196パッチです。一画素ずつ渡すより系列を短くできます。CNNのような局所性の前提が少なく、原論文では大規模データでの事前学習が性能を引き出す鍵になりました。'))
 body+=sec('cls','CLSに情報を集めて、画像を分類する',
  p('分類用に、学習可能な<strong>CLS（クラストークン）</strong>を一つ加えます。これは画像の一部分ではなく、分類に使う表現を作るための特別な位置です。196パッチなら、CLSと合わせて197個のベクトルを入力します。')+
  classifier()+
  p('Self-Attentionで各パッチとCLSが互いを参照し、FFNで各位置の特徴を加工します。この処理をN層繰り返すと、CLSにも画像全体の情報が取り込まれます。最後のCLSの表現を分類ヘッドへ渡し、softmaxでクラスごとの確率を求めます。')+
  p('GPTの説明では<strong>最後の単語の表現</strong>から次のトークンを予測しました。ここでは<strong>最後の層のCLSの表現</strong>から画像のクラスを予測します。図は全結合層で分類する例です。ViT原論文では事前学習時に隠れ層を持つMLPヘッドを使い、微調整時には線形層を使います。'))
 body+=sec('vlm','VLM：画像と文章を使って、質問に答える',
  p('<strong>VLM（Vision-Language Model）</strong>は画像と言語を扱うモデルです。ここでは、画像を入力に加えて文章を生成する、LLaVAのような構成を見ます。')+
  multimodal()+
  sub('1. 画像を、LLMに渡せる表現にする',p('画像エンコーダがパッチごとの特徴を作り、接続層がLLMの入力に合うベクトルへ変換します。ViTで分類したときと違い、この構成ではCLS一つにまとめず、複数の画像特徴を渡します。画像の特徴と文章を結び付ける対応は、画像・文章のペアなどを使った学習で身に付けます。'))+
  sub('2. 画像と質問を条件に、次のトークンを予測する',p('質問文もトークン化してベクトルにし、画像由来のベクトル列と一緒にLLMへ渡します。LLMは両方の情報を使って次のトークンの確率を出し、選んだトークンを追加して回答を延ばします。'))+
  p('同じ画像でも、「何の動物？」なら種類、「どんな色？」なら色が回答に必要です。画像と質問の関係を扱うことで、質問に応じた回答を作ります。')+
  p('VLMには、画像と文章の一致度を測るCLIPなどもあります。画像と文章を一つの系列にする方法のほか、Cross-Attentionで接続する構成もあり、この図は生成型VLMの一例です。'))
 body+=sec('compare','入力と、読み出す表現を見比べる',table(['モデル','入力するもの','出力へのつなぎ方'],[
  ('GPT','文章のトークン列','最終層の最後の位置 → 次トークンの確率'),
  ('ViT（この分類例）','画像パッチ列＋CLS＋位置','最終層のCLS → クラスの確率'),
  ('生成型VLM（この例）','画像由来のベクトル列＋文章','画像と文章を条件に、次トークンの確率')])+p('共通するのは、ベクトルで表した要素どうしの関係を使うことです。入力の作り方と、最後の表現を何に使うかが変わります。')+p('<a href="language.html#vlm">VLMの応用・評価へ</a> · <a href="vision.html">画像認識のタスクへ</a>'))
 body+=refs([('ViT：An Image is Worth 16x16 Words（2020）','https://arxiv.org/abs/2010.11929'),('LLaVA：Visual Instruction Tuning（2023）','https://llava-vl.github.io/'),('CLIP：Learning Transferable Visual Models From Natural Language Supervision（2021）','https://arxiv.org/abs/2103.00020')])
 page('vit','ViT・VLM — Transformerを画像へ広げる','モデルの構造','TRANSFORMER / 補足','画像もベクトルの列にすれば、要素間の関係を使って処理できます。ViTの画像分類から、画像と文章を組み合わせるVLMへ進みます。',body)
