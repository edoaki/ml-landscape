"""Original teaching diagrams; coordinates and scores are illustrative."""
from common import *
import base64


def photo(name, x, y, w, h):
    data = base64.b64encode((ROOT/'assets'/name).read_bytes()).decode()
    return f'<image x="{x}" y="{y}" width="{w}" height="{h}" preserveAspectRatio="xMidYMid meet" href="data:image/jpeg;base64,{data}"/>'


def diagram(b, h, w, label):
    return svg(b, h, w, label).replace('orient="auto-start-reverse"', 'orient="auto"')


PHOTO_CREDIT = '写真：<a href="https://www.robots.ox.ac.uk/~vgg/data/pets/">Oxford-IIIT Pet</a>（CC BY-SA 4.0）。'


def vlm():
    b = txt(125,30,'① 画像と質問を入力',18)
    b += photo('pet-cat.jpg',40,48,170,205)
    b += box(20,280,210,64,'「何色の猫ですか？」','質問文',BLUE)
    b += line(220,142,275,142)+box(285,105,190,74,'画像エンコーダ','画像 → 視覚特徴',GREEN)
    for i in range(6):
        b += f'<rect x="{294+i*29}" y="203" width="20" height="26" rx="3" fill="{GREEN}" opacity="{.25+i*.12}"/>'
    b += txt(380,252,'見た目の情報を持つベクトル列',13)
    b += line(380,180,380,196)
    b += line(480,142,535,142)+box(545,105,205,74,'接続部','LLMへ渡せる表現に変換',GREEN)
    b += line(647,182,647,277)
    b += line(235,312,300,312)+box(310,280,180,64,'文章の埋め込み','質問 → ベクトル列',BLUE)
    b += line(495,312,535,312)+box(545,280,205,64,'言語モデル（LLM）','画像と質問を一緒に使う',PURPLE)
    b += line(647,348,647,400)+box(485,410,280,72,'「茶色の猫です。」','回答文を順に生成',ORANGE)
    b += txt(240,430,'② 画像の特徴と質問を合わせる',17)
    b += txt(240,463,'③ 質問に応じた文章を出力',17)
    return figure(diagram(b,505,800,'猫の写真と色を尋ねる質問から、視覚特徴と質問の埋め込みをLLMへ渡して回答する流れ'),
        '生成型VLMの一例を教材で作図。回答は説明用で、推論結果ではありません。接続部などはモデルにより異なります。'+PHOTO_CREDIT)


def clip_space():
    b = txt(95,29,'画像',18)+txt(395,29,'共通の特徴空間',18)+txt(698,29,'候補の文章',18)
    b += photo('pet-cat.jpg',24,48,105,125)+photo('pet-dog.jpg',24,244,105,125)
    b += box(150,75,125,64,'画像エンコーダ','同じ重みを使う',GREEN)
    b += box(150,275,125,64,'画像エンコーダ','同じ重みを使う',GREEN)
    b += line(131,107,146,107)+line(131,307,146,307)
    b += '<rect x="300" y="58" width="240" height="320" rx="25" fill="#eef4f6" stroke="#c7dce3"/>'
    b += box(645,62,140,47,'「猫の写真」','',PURPLE)+box(645,259,140,47,'「犬の写真」','',ORANGE)
    b += box(615,133,170,54,'文章エンコーダ','文章 → ベクトル',BLUE)
    b += box(615,330,170,54,'文章エンコーダ','文章 → ベクトル',BLUE)
    b += line(715,112,715,128)+line(715,309,715,325)
    b += line(280,107,362,140,PURPLE)+line(610,158,417,160,PURPLE)
    b += line(280,307,425,297,ORANGE)+line(610,357,480,319,ORANGE)
    b += '<circle cx="376" cy="145" r="10" fill="#85709f"/><rect x="397" y="153" width="19" height="19" fill="#85709f"/>'
    b += '<circle cx="439" cy="298" r="10" fill="#ba7147"/><rect x="461" y="310" width="19" height="19" fill="#ba7147"/>'
    b += txt(381,204,'猫の画像と文が近い',14,PURPLE)+txt(423,270,'犬の画像と文が近い',14,ORANGE)
    b += txt(400,421,'● 画像のベクトル　　■ 文章のベクトル',15)
    return figure(diagram(b,448,800,'猫と犬の画像および文章を別々のエンコーダで共通の特徴空間へ写す。対応する画像と文が近くなる模式図'),
        '教材で作図。高次元の特徴空間を2次元で模式的に表現しており、点の位置はCLIPの実測ではありません。実際には正規化したベクトルの向きの近さを比べます。'+PHOTO_CREDIT)


def clip_scores():
    b = txt(390,30,'画像 × 文章の類似度を、表に並べる',19)
    b += txt(365,79,'「猫の写真」',16)+txt(535,79,'「犬の写真」',16)
    b += photo('pet-cat.jpg',95,100,83,98)+photo('pet-dog.jpg',95,213,83,98)
    b += txt(226,157,'猫の画像',15)+txt(226,270,'犬の画像',15)
    for row, values in enumerate(((.86,.21),(.18,.89))):
        for col, v in enumerate(values):
            x=290+col*170;y=100+row*113; diagonal=row==col
            b += f'<rect x="{x}" y="{y}" width="150" height="98" rx="7" fill="{"#4d7897" if diagonal else "#e8eef3"}"/>'
            b += txt(x+75,y+56,f'{v:.2f}',25,'white' if diagonal else BLUE)
    b += txt(680,145,'← 猫の画像では',14)+txt(680,174,'猫の文が高い',14)
    b += txt(680,259,'← 犬の画像では',14)+txt(680,288,'犬の文が高い',14)
    b += txt(391,355,'学習：対応するペアが、ほかの組み合わせより高くなるようにする',16)
    return figure(diagram(b,385,800,'猫と犬の2画像と2候補文の類似度表。正しい対応の対角成分が高い説明用数値'),
        '数値は教材用に設定した類似度で、実測値や正解確率ではありません。対応ペアを同じ順に並べたため対角線上にあります。'+PHOTO_CREDIT)


def rag():
    import math

    def paper(x, y, title, color, w=145, h=86):
        body = f'<path d="M{x} {y} h{w-17} l17 17 v{h-17} h{-w} Z" fill="white" stroke="{color}" stroke-width="1.8"/>'
        body += f'<path d="M{x+w-17} {y} v17 h17" fill="none" stroke="{color}"/>'
        body += txt(x+12,y+32,title,14,color,anchor='start')
        for i, length in enumerate((w-30,w-43,w-36)):
            body += line(x+12,y+46+i*10,x+length,y+46+i*10,color,arrow=False,width=1)
        return body

    def vector_text(x,y,angle,color):
        return txt(x,y,f'[{math.cos(math.radians(angle)):.2f}, {math.sin(math.radians(angle)):.2f}]',18,color)

    colors = [GREEN, BLUE, ORANGE]
    b = txt(400,30,'大量の文書。全部読むと、関係のない情報まで読むことになる。',18)
    # A bank of overlapping pages conveys the volume of the database.
    for i in range(10):
        x=28+i*73
        b += paper(x,58+(i%2)*8,'', '#cbd5d0',72,62)
    b += txt(400,157,'文書をベクトル化',19)
    for x,title,angle,color in zip((45,300,555),('A｜装置の点検','B｜食堂の案内','C｜旅費の精算'),(35,95,155),colors):
        b += paper(x,178,title,color)
        b += line(x+157,220,x+185,220,color)
        # Each little arrow is the same vector later overlaid below.
        ox=x+214; oy=240
        ex=ox+35*math.cos(math.radians(angle)); ey=oy-35*math.sin(math.radians(angle))
        b += line(ox,oy,ex,ey,color,width=3)
        b += vector_text(x+80,294,angle,color)
    b += '<path d="M25 328 H775" stroke="#dce3df"/>'
    b += txt(400,366,'探したいことも、ベクトル化',19)
    b += f'<path d="M55 392 h405 a12 12 0 0 1 12 12 v45 a12 12 0 0 1 -12 12 H92 l-24 17 v-17 H55 a12 12 0 0 1 -12 -12 v-45 a12 12 0 0 1 12 -12 Z" fill="#f3eef8" stroke="{PURPLE}"/>'
    b += txt(256,434,'「装置を動かす前に、何を確認する？」',17,PURPLE)
    b += line(490,427,553,427,PURPLE)
    b += vector_text(661,420,40,PURPLE)
    b += txt(661,452,'質問のベクトル',14,PURPLE)
    b += txt(400,524,'同じ空間に重ねると、向きが近い文書が見つかる',19)
    ox,oy,r=370,803,225
    b += f'<path d="M105 {oy} H645 M{ox} 835 V550" stroke="#e0e6e2" stroke-width="1.5"/>'
    b += f'<path d="M{ox} {oy} L{ox+r*math.cos(math.radians(35))} {oy-r*math.sin(math.radians(35))} A{r} {r} 0 0 0 {ox+r*math.cos(math.radians(40))} {oy-r*math.sin(math.radians(40))} Z" fill="{GREEN}" opacity=".15"/>'
    for angle,color,label,tx,ty in [(155,ORANGE,'C｜旅費の精算',147,675),(95,BLUE,'B｜食堂の案内',300,559),(35,GREEN,'A｜装置の点検',659,705),(40,PURPLE,'質問',544,619)]:
        ex=ox+r*math.cos(math.radians(angle));ey=oy-r*math.sin(math.radians(angle))
        b += line(ox,oy,ex,ey,color,width=3 if angle!=40 else 4)
        b += txt(tx,ty,label,16,color)
    b += f'<circle cx="{ox}" cy="{oy}" r="4" fill="#637569"/>'
    b += txt(365,835,'同じ始点に重ねたベクトル',13)
    b += txt(662,752,'いちばん近い',17,GREEN)
    b += txt(662,779,'Aを取り出す',17,GREEN)
    b += paper(529,864,'A｜装置の点検',GREEN,235,113)
    b += f'<rect x="537" y="905" width="218" height="63" fill="white"/>'
    b += txt(545,927,'運転開始前に、',16,GREEN,anchor='start')
    b += txt(545,953,'冷却水の流量を確認する。',16,GREEN,anchor='start')
    b += txt(253,913,'質問との向きの近さ（コサイン類似度）',14)
    b += txt(253,948,'A  0.996    B  0.574    C  −0.423',18)
    return figure(diagram(b,1000,800,'大量の文書と質問をそれぞれベクトルに変換し、始点を重ねて向きを比較する。質問に最も近い装置の点検文書Aを取り出す'),
        '2次元の説明用ベクトル。数値は図の矢印から計算した値で、実モデルの出力ではありません。RAGの検索部分を示しています。')
