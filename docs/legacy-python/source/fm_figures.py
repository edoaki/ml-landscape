"""Exact conditional-flow example: a Gaussian transported to two Gaussian modes.

All velocities are analytic conditional expectations (the population regression
optimum), not fitted network outputs. Generation uses RK4 without paired targets.
"""
import math
import random
from common import figure, svg, txt, line, BLUE, GREEN, ORANGE, PURPLE
SIGMA = .35
MEANS = [(-2., -1.), (2., 1.)]


def velocity(x, t):
    variance = (1-t)**2 + (SIGMA*t)**2
    logits = [-sum((x[j]-t*m[j])**2 for j in range(2))/(2*variance) for m in MEANS]
    weights = [math.exp(z-max(logits)) for z in logits]
    weights = [w/sum(weights) for w in weights]
    rate = (t*SIGMA**2-(1-t))/variance
    individual = [[m[j]+rate*(x[j]-t*m[j]) for j in range(2)] for m in MEANS]
    return [sum(weights[k]*individual[k][j] for k in range(2)) for j in range(2)], weights, individual


def rk4(x, t, h):
    k1=velocity(x,t)[0]
    k2=velocity([x[j]+h*k1[j]/2 for j in range(2)],t+h/2)[0]
    k3=velocity([x[j]+h*k2[j]/2 for j in range(2)],t+h/2)[0]
    k4=velocity([x[j]+h*k3[j] for j in range(2)],t+h)[0]
    return [x[j]+h*(k1[j]+2*k2[j]+2*k3[j]+k4[j])/6 for j in range(2)]


def simulation():
    rng=random.Random(31)
    starts=[[.6,-.4]]+[[rng.gauss(0,1),rng.gauss(0,1)] for _ in range(159)]
    # Highlight an intentionally unrepresentative random pairing; the rest are independent draws.
    targets=[[-2.,-1.]]
    for _ in starts[1:]:
        m=rng.choice(MEANS)
        targets.append([m[j]+rng.gauss(0,SIGMA) for j in range(2)])
    x=[p[:] for p in starts];frames=[]
    for i in range(401):
        t=i/400
        if i%20==0:
            frames.append({'t':t,'paired':[[(1-t)*a[j]+t*b[j] for j in range(2)] for a,b in zip(starts,targets)],'generated':[p[:] for p in x]})
        if i<400:x=[rk4(p,t,1/400) for p in x]
    return {'frames':frames,'starts':starts,'targets':targets}


def dot(x,y,color=BLUE,r=2.4,extra=''):
    return f'<circle cx="{x:.3f}" cy="{y:.3f}" r="{r}" fill="{color}" {extra}/>'


def panel(points, cx, cy, scale=36):
    b=line(cx-125,cy,cx+125,cy,arrow=False,width=1,color='#d5ddd6')+line(cx,cy-105,cx,cy+105,arrow=False,width=1,color='#d5ddd6')
    for j,p in reversed(list(enumerate(points))):b+=dot(cx+scale*p[0],cy-scale*p[1],'#c94737' if j==0 else BLUE,4.5 if j==0 else 2.4)
    return b


def destination(data):
    b=''
    for i,idx in enumerate([0,10,20]):
        cx=135+i*265;frame=data['frames'][idx]
        b+=txt(cx,30,['ランダムなノイズ','途中の分布','作りたいデータ分布'][i],17)
        b+=panel(frame['generated'],cx,160,34)
        b+=txt(cx,292,f't = {frame["t"]:.1f}',17,GREEN)
    return figure(svg(b,315,label='一つの丸い分布を、二つの山を持つ分布へ変える'), 'このページでは同じ2次元の例を最後まで使います。青い1点が1サンプル、赤点は追跡する1サンプル。両端と途中は同じ縮尺です。ノイズはN(0,I)。データは中心(−2,−1)と(2,1)、各方向の標準偏差0.35の正規分布を半分ずつ混ぜたもの。途中・終点の点群は後述の理想速度を数値積分した結果です。')


def crossings(data):
    b=txt(400,26,'ランダムに結んだ学習用の経路は、行き先が交錯する',19)
    for j in range(18):
        a=data['starts'][j];c=data['targets'][j]
        y0=155-36*a[0];y1=155-36*c[0]
        color=BLUE if c[0]<0 else ORANGE
        b+=line(90,y0,710,y1,color,arrow=False,width=1)
        b+=dot(90,y0,color,3)+dot(710,y1,color,3)
    b+=txt(90,300,'t = 0：ノイズ',17)+txt(400,300,'時間 →',17)+txt(710,300,'t = 1：データ',17)
    return figure(svg(b,325,label='時間を横軸に、横座標の値を縦軸に表示した18本の独立なペアの直線'), 'ここだけ横軸は時間、縦方向はサンプルの第1成分です。見やすく18ペアを表示。青線は左の山、橙線は右の山へ向かうペアです。この投影での交差が、2次元でも同じ位置を通ることを意味するわけではありません。重要なのは、近い途中状態にも異なる行き先のペアが混ざることです。')


def average():
    t=.5;x=[.4,.2];v,w,u=velocity(x,t)
    b=txt(400,26,'t = 0.5、位置 x = (0.4, 0.2) に注目',19)
    b+=line(235,204,235+48*u[0][0],204-48*u[0][1],BLUE,width=2)
    b+=line(235,204,235+48*u[1][0],204-48*u[1][1],ORANGE,width=2)
    b+=line(235,204,235+48*v[0],204-48*v[1],GREEN,width=5)+dot(235,204,'#c94737',7)
    b+=txt(130,324,'左の山へ向かう速度',14,BLUE)+txt(350,75,'右の山へ向かう速度',14,ORANGE)
    for i,(label,value,color) in enumerate([
        ('この場所に来る割合',f'左 {w[0]*100:.1f}% ／ 右 {w[1]*100:.1f}%',GREEN),
        ('左側の経路の平均速度',f'({u[0][0]:.2f}, {u[0][1]:.2f})',BLUE),
        ('右側の経路の平均速度',f'({u[1][0]:.2f}, {u[1][1]:.2f})',ORANGE),
        ('両方を合わせた速度',f'({v[0]:.2f}, {v[1]:.2f})',GREEN)]):
        b+=txt(610,65+i*65,label,15,color)+txt(610,89+i*65,value,19,color)
    return figure(svg(b,335,label='その時刻・位置に来る割合で重み付けした速度の平均'), '薄い2本は各山へ向かう経路の条件付き平均速度、太い緑はそれらを混ぜた速度。同じ時刻・位置に来る確率に応じて重み付けします。山自体の割合は半分ずつでも、この場所では右の山に向かう経路の方が多くなります。数値は本文の分布から厳密に計算しています。')


def transport(data):
    frames=data['frames'];body=''
    for k,frame in enumerate(frames):
        t=frame['t'];b=''
        for col,key in enumerate(['paired','generated']):
            cx=200+400*col;cy=190;scale=39
            b+=txt(cx,28,['学習用：各ペアの直線','生成：その場の平均速度で進む'][col],17)
            if col==1:
                for xx in [-2,-1,0,1,2]:
                    for yy in [-2,-1,0,1,2]:
                        v=velocity([xx,yy],t)[0]
                        b+=line(cx+scale*xx,cy-scale*yy,cx+scale*(xx+.08*v[0]),cy-scale*(yy+.08*v[1]),'#b5c1b7',width=1)
            # A handful of histories make trajectories visible without hiding the cloud.
            for j in [0,1,2,3,4,5]:
                pts=' '.join(f'{cx+scale*f[key][j][0]:.2f},{cy-scale*f[key][j][1]:.2f}' for f in frames[:k+1])
                b+=f'<polyline points="{pts}" fill="none" stroke="{"#c94737" if j==0 else "#afbbb2"}" stroke-width="{2 if j==0 else 1}"/>'
            b+=panel(frame[key],cx,cy,scale)
            b+=txt(cx,347,['終点を使って位置を作る','終点を渡さず、速度を積分'][col],16)
        a=frame['paired'][0];c=frame['generated'][0]
        label=f't = {t:.2f}'
        body+=f'<div class="fm-frame"><h4>{label}</h4>'+figure(svg(b,375,label=f'{label}：ペアの直線と平均速度の流れの比較'),f'赤点の位置：学習用 ({a[0]:.2f}, {a[1]:.2f}) ／ 生成 ({c[0]:.2f}, {c[1]:.2f})。'+('出発点は同じ。生成側には、左図のペアの終点を教えていません。' if k==0 else '同じ赤点の行き先は違っても、集まり全体では同じ時刻の分布を表します。'))+'</div>'
    return '<div class="fm-comic fm-demo" data-comic="transport"><h3>同じノイズから出発して、二つの動き方を比較する</h3><div class="fm-controls" hidden><button type="button" data-action="play">自動でめくる</button><button type="button" data-action="prev">前のコマ</button><button type="button" data-action="next">次のコマ</button><button type="button" data-action="reset">最初に戻す</button></div><p class="fm-status" role="status">全21コマを順に読めます。</p>'+body+'<p>左は独立なノイズとデータの直線補間（赤の1ペアのみ、行き先の違いを追える固定例）。右は、回帰が理想的に学べる平均速度を解析式で計算し、RK4法・刻み幅0.0025で積分した160サンプルです。ニューラルネットワークを訓練した結果ではありません。表示はtを0.05ずつ進めます。有限個の点なので、左右の点の配置まで一致するわけではありません。</p></div>'
