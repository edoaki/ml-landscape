"""Computed distribution contours and explicit reversible arithmetic."""
import math
from common import figure, svg, txt, line, BLUE, GREEN, ORANGE, PURPLE


def stages(a,b):
    return [(a,b),(a,1.5*b),(a,1.5*b+.6*a*a-.6),(1.5*b+.6*a*a-.6,a)]


def distributions():
    b=txt(500,28,'生成：同じ点に演算を順番に適用する →',20,GREEN)
    colors=[BLUE,GREEN,PURPLE,ORANGE]
    centers=[125,375,625,875]
    titles=['① 正規分布 z','② 縦に1.5倍','③ 位置に応じて曲げる','④ 座標を入れ替える']
    for k,(cx,color,title) in enumerate(zip(centers,colors,titles)):
        b+=txt(cx,69,title,17,color)
        b+=line(cx-100,214,cx+100,214,arrow=False,width=1,color='#d1d8d3')
        b+=line(cx,110,cx,300,arrow=False,width=1,color='#d1d8d3')
        for r in [2.4,1.9,1.4,.9,.4]:
            points=[]
            for j in range(161):
                a,c=stages(r*math.cos(j*math.tau/160),r*math.sin(j*math.tau/160))[k]
                points.append(f'{cx+24*a:.2f},{214-24*c:.2f}')
            b+=f'<polygon points="{" ".join(points)}" fill="{color}" fill-opacity=".13" stroke="{color}" stroke-opacity=".35" stroke-width="1"/>'
        a,c=stages(.5,.5)[k]
        b+=f'<circle cx="{cx+24*a}" cy="{214-24*c}" r="5" fill="#c94737" stroke="white" stroke-width="1.5"/>'
        b+=txt(cx,326,['(0.5, 0.5)','(0.5, 0.75)','(0.5, 0.3)','(0.3, 0.5)'][k],15,'#c94737')
        if k<3:
            b+=line(cx+96,171,cx+151,171,GREEN)
            b+=line(cx+151,262,cx+96,262,ORANGE)
    b+=txt(500,371,'逆変換：最後の演算から、逆の順番で戻す ←',20,ORANGE)
    operations=[('① ⇄ ②','進む：b × 1.5','戻る：b ÷ 1.5'),('② ⇄ ③','進む：b ＋ 0.6a² − 0.6','戻る：b − 0.6a² ＋ 0.6'),('③ ⇄ ④','進む：(a, b) → (b, a)','戻る：もう一度入れ替える')]
    for i,(title,forward,back) in enumerate(operations):
        cx=170+i*330
        b+=txt(cx,416,title,16)+txt(cx,446,forward,15,GREEN)+txt(cx,475,back,15,ORANGE)
    return figure(svg(b,505,w=1000,label='正規分布を拡大、非線形に変形、座標交換し、逆演算で戻す'), '2次元の分布を実際に上記の演算で変換した図。濃い部分ほど確率密度が高く、線は等密度線。全パネルは同じ座標尺度。赤点は同じサンプルの移動です。②→③ではaを保ったままbを変えるため、曲げても逆に戻せます。係数は説明用の固定値で、学習結果ではありません。')


def density():
    b=''
    for k,cx in enumerate([200,600]):
        color=[BLUE,ORANGE][k];base=225
        b+=txt(cx,34,['z：標準正規分布','x = 2z + 3：幅が2倍'][k],19,color)
        b+=line(cx-165,base,cx+165,base,arrow=False)
        pts=[]
        for j in range(241):
            x=-6+j*16/240
            z=x if k==0 else (x-3)/2
            pdf=math.exp(-z*z/2)/math.sqrt(2*math.pi)/(1 if k==0 else 2)
            pts.append(f'{cx-165+(x+6)*20:.2f},{base-390*pdf:.2f}')
        b+=f'<polygon points="{cx-165},225 {" ".join(pts)} {cx+155},225" fill="{color}" fill-opacity=".18"/>'
        b+=f'<polyline points="{" ".join(pts)}" fill="none" stroke="{color}" stroke-width="3"/>'
        for tick in [-4,0,3,8]:
            xx=cx-165+(tick+6)*20
            b+=line(xx,225,xx,230,arrow=False,width=1)+txt(xx,248,tick,12)
        b+=txt(cx,282,['中心 0・標準偏差 1','中心 3・標準偏差 2'][k],15,color)
    b+=txt(400,320,'横幅が2倍なら、高さは1/2。曲線の下の面積はどちらも1。',16)
    return figure(svg(b,345,label='同じ尺度で比較した正規分布の拡大と移動'), '横軸は値、縦方向は確率密度。左右は同じ尺度で描画しています。平行移動では高さは変わらず、拡大した分だけ密度を下げる必要があります。')


def coupling():
    b=txt(400,29,'一部を残せば、倍率と移動量を同じ条件で計算できる',19)
    for row,y in enumerate([120,290]):
        inverse=row==1
        b+=txt(67,y-43,'逆変換' if inverse else '順変換',17,ORANGE if inverse else GREEN)
        b+=txt(80,y,'a = 1',18)+line(125,y-5,715,y-5,BLUE)+txt(750,y,'a = 1',18)
        b+=txt(410,y-18,'a はそのまま通す',14,BLUE)
        b+=txt(80,y+65,'b = 7' if inverse else 'b = 2',18)
        b+=txt(750,y+65,'b = 2' if inverse else 'b = 7',18)
        for x,label in [(320,'− 3' if inverse else '× 2'),(520,'÷ 2' if inverse else '＋ 3')]:
            b+=f'<circle cx="{x}" cy="{y+59}" r="27" fill="white" stroke="{ORANGE if inverse else GREEN}" stroke-width="2"/>'+txt(x,y+65,label,17)
        b+=line(125,y+59,285,y+59)+line(351,y+59,485,y+59)+line(551,y+59,706,y+59)
    b+=txt(400,416,'a をNNに入力して、倍率2・移動量3を計算した場合の例',16,PURPLE)
    b+=txt(400,445,'逆でも a = 1 が残るので、同じNNから同じ2と3を得られる',15)
    return figure(svg(b,470,label='Affine couplingの掛け算足し算と引き算割り算による逆変換'), '例ではexp(s(1)) = 2、t(1) = 3。NN自体を逆向きに解く必要はありません。残したaから同じ倍率と移動量を再計算し、bに施した演算だけを逆にします。次の層では成分の役割を交換し、両方を変換します。')
