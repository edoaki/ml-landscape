"""Static information geometry diagrams with explicit concept/encoding contracts.

1. Statistical manifold: Gaussian densities vs points representing Gaussians.
2. Distinguishability: same mean shift, different spread, shared observation scale.
3. Local Fisher metric: ellipses dmu^2 + 2 dsigma^2 = epsilon^2 sigma^2.
4. Fisher geodesic: straight coordinate path vs actual Gaussian geodesic.
5. Exact Gaussian KL vs its local quadratic approximation.
6. Same linearized loss, Euclidean and Fisher steepest descent directions.
Observation strips use normal quantiles, not claimed experimental measurements.
"""
from pathlib import Path
from math import sqrt, acosh, sin, cos, pi, log, exp
from statistics import NormalDist
from html import escape

ROOT=Path(__file__).resolve().parents[1]
OUT=ROOT/'content/questions/information-geometry/components'
INK, GRID, GREEN, BLUE, ORANGE='#243b30','#9aa99d','#28735c','#386b9b','#a65c26'
Z=[NormalDist().inv_cdf((i+.5)/17) for i in range(17)]


def text(x,y,value,anchor='start',cls=''):
    return f'<text x="{x:.2f}" y="{y:.2f}" text-anchor="{anchor}" class="{cls}">{escape(value)}</text>'


def line(x1,y1,x2,y2,color=GRID,width=1.5,dash=''):
    return f'<path d="M{x1:.2f},{y1:.2f} L{x2:.2f},{y2:.2f}" fill="none" stroke="{color}" stroke-width="{width}" stroke-dasharray="{dash}"/>'


def path(points,color=GREEN,width=2.5,dash=''):
    d='M'+' L'.join(f'{x:.3f},{y:.3f}' for x,y in points)
    return f'<path d="{d}" fill="none" stroke="{color}" stroke-width="{width}" stroke-dasharray="{dash}" stroke-linejoin="round"/>'


def arrow(x1,y1,x2,y2,color=INK):
    dx,dy=x2-x1,y2-y1
    norm=sqrt(dx*dx+dy*dy); ux,uy=dx/norm,dy/norm
    head=[(x2-6*ux+4*uy,y2-6*uy-4*ux),(x2,y2),(x2-6*ux-4*uy,y2-6*uy+4*ux)]
    return line(x1,y1,x2,y2,color,2)+path(head,color,2)



def mark(x,y,color,kind='circle',radius=5):
    if kind=='square':
        return f'<rect x="{x-radius:.2f}" y="{y-radius:.2f}" width="{radius*2}" height="{radius*2}" fill="{color}"/>'
    return f'<circle cx="{x:.2f}" cy="{y:.2f}" r="{radius}" fill="{color}"/>'


def observations(mu,sigma,y,color=GREEN,kind='circle'):
    # A common standardized pattern isolates center/spread, without random noise.
    b=line(23,y+15,277,y+15)
    for i,z in enumerate(Z):
        x=150+15*(mu+sigma*z)
        b+=mark(x,y+[-14,-7,0,7,14][i%5],color,kind,2.5)
    return b


def svg(body,label,height):
    return f'<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 300 {height}" role="img" aria-label="{escape(label)}">\n{body}\n</svg>'


def panel(title,body,label,height,note):
    return f'<div class="ig-panel"><h3>{title}</h3>\n{svg(body,label,height)}\n<p class="ig-takeaway">{note}</p></div>'


def figure(id,panels,caption,legend=''):
    return f'<figure class="ig-figure" id="{id}">\n{legend}<div class="ig-panels">\n{panels}</div>\n<figcaption>{caption}</figcaption>\n</figure>\n'


def axes(xlabel='平均 →',ylabel='標準偏差 ↑',base=265):
    return arrow(30,base,280,base)+arrow(30,base,30,40)+text(30,22,ylabel)+text(280,base+31,xlabel,'end')


def make_distributions():
    coords=[('A',-2,1,GREEN),('B',2,1,BLUE),('C',-2,2,ORANGE)]
    b=''
    for name,mu,sigma,color in coords:
        base={'A':104,'B':254,'C':404}[name]
        b+=text(18,base-72,f'{name}：μ = {mu}, σ = {sigma}')
        b+=line(23,base,277,base)
        pts=[]
        for i in range(251):
            value=-8+16*i/250
            density=exp(-.5*((value-mu)/sigma)**2)/(sigma*sqrt(2*pi))
            pts.append((150+15*value,base-120*density))
        b+=path(pts,color,2.8)
        b+=line(150+15*mu,base,150+15*mu,base+5,color)
        b+=text(150+15*mu,base+23,str(mu),'middle')
    b+=text(277,461,'x →','end')
    first=panel('正規分布の確率密度',b,'正規分布A、B、Cの確率密度。AとBは中心が異なり、AとCは広がりが異なる。全て同じ軸尺度。',480,'横軸：x ／ 縦方向：確率密度 p(x)')
    b=axes('','標準偏差 ↑')+text(280,319,'平均 →','end')
    for mu in [-2,2]:
        x=150+34*mu
        b+=line(x,265,x,270)+text(x,292,str(mu),'middle')
    for sigma in [1,2]:
        y=265-82*sigma
        b+=line(25,y,30,y)+text(20,y+5,str(sigma),'end')
    b+=arrow(92,183,205,183)+arrow(82,173,82,113)
    b+=text(153,222,'平均だけ変わる','middle')+text(101,146,'標準偏差だけ変わる')
    for name,mu,sigma,color in coords:
        x,y=150+34*mu,265-82*sigma
        b+=mark(x,y,color,radius=7)+text(x+12,y-12,name,cls='ig-label')
    second=panel('パラメータ空間 (μ, σ)',b,'横軸は平均、縦軸は標準偏差。分布Aは座標(-2,1)、Bは(2,1)、Cは(-2,2)。',340,'点一つ ＝ 一つの確率分布')
    return figure('ig-distributions',first+second,'正規分布の密度曲線と、それを指定するパラメータの対応です。密度曲線はすべて共通の横軸・縦軸尺度を使っています。パラメータ空間のA・B・Cは、それぞれ一つの分布に対応します。')


def make_comparison():
    panels=''
    for sigma,names,colors in [(1,('A','B'),(GREEN,BLUE)),(2,('C','D'),(ORANGE,'#8056a0'))]:
        # Same parameter axes and displacement in both rows.
        X=lambda mu:150+40*mu
        Y=lambda sd:255-76*sd
        b=axes('μ →','σ ↑',base=255)
        for sd in [1,2]:
            b+=text(22,Y(sd)+5,str(sd),'end')
        for mu in [-2,2]:
            b+=text(X(mu),279,str(mu),'middle')
        y=Y(sigma)
        b+=arrow(X(-2)+8,y,X(2)-8,y,INK)+text(150,y+32,'Δμ = 4','middle')
        for name,mu,col in zip(names,[-2,2],colors):
            b+=mark(X(mu),y,col,radius=6)+text(X(mu),y-18,name,'middle',cls='ig-label')
        panels+=panel(f'{names[0]} → {names[1]}：パラメータ空間',b,f'標準偏差{sigma}を固定し、平均を−2から2へ動かす。',305,f'σ = {sigma}、変位は (4, 0)')
        b=axes('x →','確率密度 p(x) ↑',base=230)
        for name,mu,col in zip(names,[-2,2],colors):
            pts=[]
            for i in range(301):
                x=-8+16*i/300
                den=exp(-.5*((x-mu)/sigma)**2)/(sigma*sqrt(2*pi))
                pts.append((150+15*x,230-360*den))
            b+=path(pts,col,2.8)
            b+=text(150+15*mu,230-360/(sigma*sqrt(2*pi))-18,name,'middle',cls='ig-label')
        for x in [-6,-2,2,6]:
            b+=text(150+15*x,255,str(x),'middle')
        panels+=panel(f'{names[0]}・{names[1]}：対応する密度曲線',b,f'平均−2と2、標準偏差{sigma}の正規分布。',305,f'平均の差は標準偏差の {4/sigma:g} 倍')
    return figure('ig-comparison',panels,'上段はA・B（σ＝1）、下段はC・D（σ＝2）です。二つのパラメータ図は共通の尺度で、矢印は同じ変位を表します。二つの密度図も共通の尺度です。各組で点と曲線の記号・色を対応させています。狭い画面では、各組のパラメータ図、密度図の順に縦に並びます。')


def make_metric():
    # At each base point, ellipses are exact for the metric frozen at that point;
    # they approximate geodesic balls locally, rather than being finite balls.
    panels=''
    for sigma,title,note in [(1,'σ = 1 の分布','同じ移動で、範囲の外へ'),(2,'σ = 2 の分布','同じ移動でも、範囲の内側へ')]:
        b=axes(base=275)
        x,y=112,275-80*sigma
        eps=.28; rx=80*eps*sigma; ry=80*eps*sigma/sqrt(2)
        b+=f'<ellipse cx="{x}" cy="{y}" rx="{rx}" ry="{ry}" fill="{GREEN}" fill-opacity=".13" stroke="{GREEN}" stroke-width="1.7"/>'
        b+=mark(x,y,INK,radius=4)+arrow(x+5,y,x+34,y,BLUE)
        b+=text(150,323,'平均を同じだけ増やす','middle')
        panels+=panel(title,b,title+'でのFisher計量による局所的な変化の範囲。同じ長さの平均方向の矢印が、'+('楕円を出る。' if sigma==1 else '楕円に収まる。'),342,note)
    return figure('ig-metric',panels,'色の付いた楕円は、各点のFisher計量による同じ小さな長さの範囲（局所近似）です。二つの座標図の尺度と矢印の幅は共通です。平均だけでなく、標準偏差を変える方向の長さも計量が決めます。')


def make_paths():
    # Gaussians from (mu,sigma)=(-2,1) to (2,1).
    # Geodesic mu^2+2*sigma^2=6; the domain above sigma=0 is used.
    X=lambda mu:150+42*mu
    Y=lambda sigma:275-78*sigma
    b=axes(base=275)
    b+=line(X(-2),Y(1),X(2),Y(1),BLUE,2.6,'6 4')
    points=[]
    for i in range(181):
        mu=-2+4*i/180; sigma=sqrt((6-mu*mu)/2)
        points.append((X(mu),Y(sigma)))
    b+=path(points,GREEN,3)
    for name,mu,sigma in [('出発',-2,1),('途中',0,sqrt(3)),('到着',2,1)]:
        x,y=X(mu),Y(sigma)
        b+=mark(x,y,GREEN,radius=5)+text(x,y-15,name,'middle')
    b+=text(150,236,'中心だけを変える','middle')
    first=panel('同じ二つの分布を結ぶ',b,'破線は平均だけを変える経路。実線は途中でばらつきも変えるFisher計量による最短経路。',323,'実線の経路のほうが短い')
    b=''
    for label,mu,sigma,y in [('出発',-2,1,67),('途中',0,sqrt(3),159),('到着',2,1,251)]:
        b+=text(23,y-26,label)+observations(mu,sigma,y)
    b+=text(277,301,'読み取り値 →','end')
    second=panel('実線上での値の出方',b,'実線経路の出発、途中、到着での観測値の模式図。途中ではばらつきが大きくなる。',323,'途中では、より広く散らばる')
    legend='<div class="ig-legend"><span><i class="ig-swatch ig-straight" aria-hidden="true"></i>座標図上の直線</span><span><i class="ig-swatch ig-shortest" aria-hidden="true"></i>Fisher計量での最短経路</span></div>\n'
    return figure('ig-paths',first+second,'正規分布のFisher計量から求めた最短経路です。長さは、図上の線を定規で測るのではなく、途中の分布ごとにFisher計量で測って足し合わせます。',legend)


def gaussian_kl_scale(delta):
    # KL(N(0,1) || N(0,(1+delta)^2)).
    return log(1+delta)+1/(2*(1+delta)**2)-.5


def make_kl_local():
    panels=''
    for limit,top,title in [(.6,1.8,'標準偏差を広い範囲で変える'),(.06,.0045,'同じ分布の近くを拡大する')]:
        X=lambda d: 150+110*d/limit
        Y=lambda k: 244-184*k/top
        b=arrow(40,244,280,244)+arrow(40,244,40,40)+text(40,25,'KL ↑')
        b+=line(150,244,150,48,GRID,1,'3 4')
        for value in [-limit,0,limit]:
            b+=text(X(value),269,f'{value:g}','middle')
        b+=text(280,300,'標準偏差の変化 Δσ →','end')
        b+=text(45,58,f'{top:g}')
        pts=[-limit+2*limit*i/240 for i in range(241)]
        b+=path([(X(d),Y(gaussian_kl_scale(d))) for d in pts],GREEN,3)
        b+=path([(X(d),Y(d*d)) for d in pts],ORANGE,2.5,'6 4')
        b+=mark(150,244,INK,radius=4)
        panels+=panel(title,b,'標準偏差1の基準分布に対するKLと二次近似。'+('変化幅0.06以内では二つの曲線が近い。' if limit<.1 else '大きく動かすと二次近似から外れる。'),318,'近くでは二次近似がよく合う' if limit<.1 else '大きく動かすと、近似から外れる')
    legend='<div class="ig-legend"><span><i class="ig-swatch ig-shortest" aria-hidden="true"></i>KLの実際の値</span><span><i class="ig-swatch ig-quadratic" aria-hidden="true"></i>二次近似（Δσ）²</span></div>'
    return figure('ig-kl-local',panels,'平均0・標準偏差1の分布pを固定し、qの標準偏差を1＋Δσに変えた実計算です。Δσ＝0で同じ分布になります。右図は横軸・縦軸とも拡大しています。平均を固定したこの例では、KLの二次近似は（Δσ）²です。',legend)


def make_natural_gradient():
    panels=''
    for natural in [False,True]:
        cx,cy=135,181
        rx=90 if natural else 76
        ry=rx/sqrt(2) if natural else rx
        # Minimize linearized loss -dmu-dsigma inside the metric ball.
        vx=rx*rx/sqrt(rx*rx+ry*ry); vy=ry*ry/sqrt(rx*rx+ry*ry)
        tangent=vx+vy
        key='fisher' if natural else 'euclidean'
        b=f'<defs><clipPath id="ig-loss-clip-{key}"><rect x="36" y="52" width="232" height="215"/></clipPath></defs>'
        b+=f'<g clip-path="url(#ig-loss-clip-{key})">'
        for c in [-100,-50,0,50,tangent]:
            b+=line(36,cy+(36-cx)-c,268,cy+(268-cx)-c,GRID,1.3)
        b+='</g>'
        b+=f'<ellipse cx="{cx}" cy="{cy}" rx="{rx}" ry="{ry}" fill="{GREEN if natural else BLUE}" fill-opacity=".1" stroke="{GREEN if natural else BLUE}" stroke-width="2"/>'
        b+=arrow(36,cy,279,cy)+arrow(cx,270,cx,42)
        b+=text(20,25,'Δσ ↑')+text(279,302,'Δμ →','end')
        b+=arrow(cx,cy,cx+vx,cy-vy,GREEN if natural else BLUE)
        b+=mark(cx,cy,INK,radius=4)+text(cx-10,cy+24,'原点','end')
        b+=mark(cx+vx,cy-vy,GREEN if natural else BLUE,radius=5)
        b+=arrow(226,90,254,62,ORANGE)+text(279,42,'損失が小さくなる','end')
        panels+=panel('Fisher計量で同じ長さ' if natural else '座標上で同じ長さ',b,'同じ損失の等高線に対し、'+('Fisher計量の楕円内では、平均方向をより大きく変える自然勾配を選ぶ。' if natural else '座標上の円内では、右上45度の通常の勾配方向を選ぶ。'),322,'自然勾配：楕円内で最も損失を減らす' if natural else '通常の勾配：円内で最も損失を減らす')
    return figure('ig-natural-gradient',panels,'現在のパラメータを原点とした変位(Δμ, Δσ)の図です。斜線は一次近似した損失の等高線で、両パネルに同じ傾きを使っています。標準偏差1の正規分布のFisher計量では、平均方向と標準偏差方向の重みが1：2なので、右の楕円は縦に短くなります。円と楕円の大きさは図示用に選んでおり、矢印の長さではなく方向を比べます。')


def validate():
    for sigma in [1,2]:
        epsilon=.28
        for i in range(100):
            angle=i*2*pi/100
            dm=epsilon*sigma*cos(angle); ds=epsilon*sigma*sin(angle)/sqrt(2)
            assert abs((dm*dm+2*ds*ds)/sigma**2-epsilon**2)<1e-12
    step=4/20000; length=0
    for i in range(20000):
        mu=-2+(i+.5)*step; sigma=sqrt((6-mu*mu)/2)
        derivative=-mu/(2*sigma)
        length+=sqrt(1+2*derivative**2)/sigma*step
    exact=sqrt(2)*acosh(5)
    assert abs(length-exact)<1e-7 and length<4
    assert 34/80/1 > .28 > 34/80/2
    for delta in [.01,.001]:
        assert abs(gaussian_kl_scale(delta)/delta**2-1)<.017
    # The chosen Fisher direction maximizes dmu+dsigma over the ellipse.
    rx,ry=90,90/sqrt(2)
    vx,vy=rx*rx/sqrt(rx*rx+ry*ry),ry*ry/sqrt(rx*rx+ry*ry)
    assert abs(vx*vx/rx**2+vy*vy/ry**2-1)<1e-12
    for i in range(1000):
        angle=2*pi*i/1000
        assert rx*cos(angle)+ry*sin(angle)<=vx+vy+1e-10
    return {'kl_local_approximation':'verified','natural_gradient_direction':'verified','geodesic_length_numeric' :length,'geodesic_length_exact':exact,'coordinate_straight_length':4,'local_ellipses':'verified'}


if __name__=='__main__':
    import json
    result=validate()
    for name,fn in [('distributions',make_distributions),('comparison',make_comparison),('metric',make_metric),('paths',make_paths),('kl-local',make_kl_local),('natural-gradient',make_natural_gradient)]:
        (OUT/f'{name}.html').write_text(fn())
    print(json.dumps(result,indent=2))
