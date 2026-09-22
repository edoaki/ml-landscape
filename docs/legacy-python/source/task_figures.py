"""Concrete input/output pairs for the application pages."""
from common import *
from decision import pair, panel


def tracking():
    def frame(later):
        b='<rect x="15" y="55" width="310" height="155" rx="8" fill="#e8eedf"/>'
        for name,x,y,c in [('ID 1',225 if later else 85,112,BLUE),('ID 2',105 if later else 240,153,ORANGE)]:
            b+=f'<circle cx="{x}" cy="{y-20}" r="11" fill="{c}"/><path d="M{x} {y-8}v31m0-16l-17 12m17-12l17 12m-17 4l-12 23m12-23l12 23" stroke="{c}" stroke-width="5"/>'+txt(x,y-40,name,14,c)
        return panel(b,'時刻 t＋1：位置が入れ替わる' if later else '時刻 t：2人にIDを付ける')
    return pair(frame(False),frame(True),'教材用の追跡図。同じ色・同じIDが同じ人物を表す。左右の並び順をIDにすると、入れ替わった時に取り違える。')


def audio():
    def wave(freqs,title):
        b=line(15,130,325,130,arrow=False,width=1)
        pts=[]
        for i in range(311):
            v=sum(math.sin(i*f/310*math.pi*2) for f in freqs)/len(freqs)
            pts.append(f'{15+i},{130-v*50}')
        b+='<polyline points="'+' '.join(pts)+f'" fill="none" stroke="{BLUE}" stroke-width="2"/>'
        return panel(b+txt(170,222,'横軸：時間 ／ 縦方向：振幅',13),title)
    return pair(wave([3,9],'入力：二つの成分を混ぜた波形'),wave([3],'目標の一つ：低い成分の波形'),'教材用の合成波形。右は左の元成分の一つで、分離モデルを実行した結果ではない。もう一つの高い成分も取り出す対象になる。')


def retrieval():
    b=box(15,65,310,65,'質問：見学会の受付は何時？','必要な文書を検索',BLUE)
    b+=box(15,160,310,65,'文書：受付は9時30分から','検索で取得した記述')
    c=box(15,65,310,65,'質問＋取得文書をLLMへ','文書を文脈に入れる')
    c+=box(15,160,310,65,'回答：9時30分です［1］','［1］見学会の案内',ORANGE)
    return pair(panel(b,'入力：質問と文書'),panel(c,'出力：文書に基づく回答'),'教材用の回答例。検索で取得した「9時30分」が回答を支える。同じ質問でも誤った文書を取得すれば、回答の根拠を失う。')


def graph_tasks():
    def network(output):
        pts=[(65,95),(170,65),(275,108),(108,198),(235,204)]
        b=''
        for a,c in [(0,1),(1,2),(0,3),(3,4),(2,4)]:b+=line(*pts[a],*pts[c],arrow=False)
        for i,(x,y) in enumerate(pts):
            color=ORANGE if i==4 else BLUE
            b+=f'<circle cx="{x}" cy="{y}" r="23" fill="{color if output or i!=4 else "#e0e6de"}"/>'+txt(x,y+5,'AI' if output and i==4 else '?' if i==4 else str(i+1),14,'white' if output or i!=4 else GREEN)
        return panel(b,'出力：未分類の論文の分野' if output else '入力：論文と引用の関係')
    return pair(network(False),network(True),'ノード分類の教材例。点が論文、線が引用関係（方向は省略）。未知の点に分野「AI」を予測する。グラフ全体に一つのラベルを付けるタスクとは異なる。')


def science():
    return pair(panel(box(15,65,310,68,'入力：分子の構造','原子の種類と結合',BLUE)+line(170,140,170,162)+box(15,175,310,68,'出力：性質の推定値','例：水への溶けやすさ'),'予測：構造から性質へ',280),panel(box(15,65,310,68,'入力：欲しい性質','例：水に溶けやすい',ORANGE)+line(170,140,170,162)+box(15,175,310,68,'出力：条件に合う候補構造','実験で性質を確かめる'),'設計：性質から候補へ',280),'同じ分子でも、予測と設計では入力と出力の向きが変わる。教材用の模式図。条件を満たす分子が一つに決まるとは限らない。')
