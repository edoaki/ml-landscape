"""Deterministic, schematic SVGs for the classical ML lesson.

Coordinates show the exact feature map and Lloyd assignments used in the text.
No fitted model or real-world measurements are presented as experimental data.
"""
from pathlib import Path
from html import escape
from statistics import mean

ROOT = Path(__file__).resolve().parents[1]
OUT = ROOT / 'content/basics/classical/components'
BLUE, ORANGE, INK, GRID = '#386b9b', '#a65c26', '#243b30', '#bbc6ba'


def text(x, y, value, anchor='middle', size=14, color=INK):
    return f'<text x="{x:g}" y="{y:g}" text-anchor="{anchor}" font-size="{size}" fill="{color}">{escape(value)}</text>'


def line(x1, y1, x2, y2, color=GRID, dash=''):
    return f'<path d="M{x1:g},{y1:g} L{x2:g},{y2:g}" stroke="{color}" stroke-width="1.5" stroke-dasharray="{dash}" fill="none"/>'


def point(x, y, group):
    if group:
        return f'<path d="M{x:g},{y-7:g} l7,7 l-7,7 l-7,-7 Z" fill="{ORANGE}" stroke="white" stroke-width="1.5"/>'
    return f'<circle cx="{x:g}" cy="{y:g}" r="6" fill="{BLUE}" stroke="white" stroke-width="1.5"/>'


def svg(body, label, height):
    return f'<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 340 {height}" role="img" aria-label="{escape(label)}"><g font-family="system-ui,sans-serif">{body}</g></svg>'


def panel(title, graphic, note):
    return f'<div class="classical-panel"><p class="classical-panel-title">{title}</p>{graphic}<p class="classical-panel-note">{note}</p></div>'


def kernel_map():
    panels=[]
    for transformed in (False, True):
        base=225
        body=line(35,base,315,base)
        if transformed:
            body+=line(45,25,45,base)
            for y in (1,2,3,4):
                py=base-y*42
                body+=line(42,py,315,py, '#e8ede5')+text(32,py+5,str(y),size=12)
            body+=text(48,18,'x²',anchor='start')
            body+=line(45,base-2.5*42,315,base-2.5*42,INK,'5 4')
            body+=text(170,base-2.5*42-10,'境界：x² = 2.5',size=13)
        else:
            body+=text(170,48,'両端が混雑、中央は混雑しない',size=14)
            body+=text(170,91,'一か所の区切りでは分けられない',size=13)
        for x in range(-2,3):
            px=180+58*x
            y=base-x*x*42 if transformed else base
            body+=point(px,y,abs(x)==2)
            body+=line(px,base+8,px,base+12)+text(px,base+30,str(x),size=13)
        body+=text(180,280,'x = (気温 − 22) / 4',size=13)
        title='② 特徴を (x, x²) に変換' if transformed else '① 気温の1軸で表す'
        note='横線より上の2点だけが「混雑」。' if transformed else '14・18・22・26・30℃の5日間。'
        panels.append(panel(title,svg(body,title,296),note))
    return '<figure class="classical-figure" id="kernel-feature-map"><p class="classical-legend">◆ オレンジ：混雑する　● 青：混雑しない</p><div class="classical-panels">'+''.join(panels)+'</div><figcaption>同じ5点を、別の特徴で表す教材用の例。元の気温軸では二か所の境界が必要ですが、変換後は一本の直線で分けられます。図は特徴変換の効果を示し、SVMを学習した結果ではありません。</figcaption></figure>'


def assignments(values, centers):
    return [min(range(len(centers)),key=lambda j:abs(v-centers[j])) for v in values]


def kmeans_steps():
    values=[1,2,4,8,9]
    centers=[1.,4.]
    panels=[]
    titles=['① 初めの中心で割り当て','② 中心を更新し、割り当て直す','③ 再び平均を取り、安定する']
    notes=['中心1・4。4回の人は右の組。','中心1.5・7。4回の人が左へ移る。','中心約2.33・8.5。所属は変わらない。']
    history=[]
    for i in range(3):
        groups=assignments(values,centers)
        history.append((centers[:],groups[:]))
        scale=lambda x: 34+x*28
        body=line(scale(0),100,scale(10),100)
        for v in range(11):
            px=scale(v)
            body+=line(px,100,px,106)+text(px,125,str(v),size=12)
        boundary=mean(centers)
        body+=line(scale(boundary),44,scale(boundary),165,INK,'4 4')
        body+=text(scale(boundary),31,f'境目 {boundary:.2f}'.rstrip('0').rstrip('.'),size=12)
        for v,g in zip(values,groups):
            body+=point(scale(v),100,g)
            if v==4 and i==1:
                body+=text(scale(v),72,'移動',size=13,color=BLUE)
        for c,color in zip(centers,[BLUE,ORANGE]):
            px=scale(c)
            body+=line(px-6,147,px+6,159,color)+line(px-6,159,px+6,147,color)
            body+=text(px,178,f'{c:.2f}'.rstrip('0').rstrip('.'),size=12,color=color)
        body+=text(314,205,'月の購入回数',anchor='end',size=12)
        panels.append(panel(titles[i],svg(body,notes[i],220),notes[i]))
        centers=[mean([v for v,g in zip(values,groups) if g==j]) for j in range(2)]
    assert history[0][1]==[0,0,1,1,1]
    assert history[1][0]==[1.5,7]
    assert history[1][1]==history[2][1]==[0,0,0,1,1]
    assert centers==[7/3,8.5]
    return '<figure class="classical-figure" id="kmeans-update"><p class="classical-legend">●・◆：利用者（色と形が所属）　×：中心<br>点線：二つの中心の中間</p><div class="classical-steps">'+''.join(panels)+'</div><figcaption>5人の購入回数をk=2で分ける計算例。変わるのは所属と中心で、利用者の購入回数は動きません。初期値を1・4と決めた場合の更新を、同じ目盛りで示しています。</figcaption></figure>'


if __name__=='__main__':
    OUT.mkdir(parents=True,exist_ok=True)
    (OUT/'kernel-map.html').write_text(kernel_map())
    (OUT/'kmeans-steps.html').write_text(kmeans_steps())
    print('Generated kernel-map.html and kmeans-steps.html; verified Lloyd updates.')
