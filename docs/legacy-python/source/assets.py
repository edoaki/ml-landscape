"""Original explanatory SVGs and synthetic audio. Does not fetch external assets."""
from common import *
import base64,wave,struct

def save(name,body,h=250,label='教材用の模式図'):(ROOT/'assets'/name).write_text(svg(body,h,label=label),encoding='utf-8')
def build():
 b=txt(180,27,'汎化：訓練と検証',18)+txt(590,27,'最適化：学習率と更新',18)
 for ox in [35,440]:
  b+=line(ox+35,230,ox+320,230,arrow=False)+line(ox+35,230,ox+35,55,arrow=False)
 b+=txt(205,265,'学習の進行 →',13)+txt(58,50,'誤差',12)+txt(615,265,'重み w →',13)+txt(462,50,'損失',12)
 def path(points,color,dash=False):return '<polyline points="'+' '.join(f'{x:.1f},{y:.1f}' for x,y in points)+f'" fill="none" stroke="{color}" stroke-width="3"'+(' stroke-dasharray="6 4"' if dash else '')+'/>'
 b+=path([(70+i*9,210-145*math.exp(-i/7)) for i in range(31)],GREEN)+path([(70+i*9,180-110*math.exp(-i/7)-max(0,i-12)*3.5) for i in range(31)],ORANGE)+txt(280,217,'訓練',12,GREEN)+txt(283,111,'検証',12,ORANGE)
 b+=path([(475+i*9,220-((i-15)/15)**2*150) for i in range(31)],'#a0aca0')
 for pts,col in [([(740,87),(595,191),(627,219),(610,218)],ORANGE), ([(500,116),(552,185),(580,211),(600,220)],GREEN)]:
  for (x,y),(xx,yy) in zip(pts,pts[1:]):b+=line(x,y,xx,yy,col)
 b+=txt(680,62,'大きな歩幅',12,ORANGE)+txt(529,84,'小さな歩幅',12,GREEN)
 save('reliability.svg',b,290,'訓練と検証の誤差、および更新経路の教材用概念図')
 b=txt(400,28,'将来予測：ここから先が未知',18)+f'<rect x="525" y="47" width="225" height="135" fill="{ORANGE}" opacity=".07"/>'+line(45,180,760,180,arrow=False)+line(525,45,525,185,dash=True,arrow=False)+txt(290,207,'観測して入力に使う区間',13,BLUE)+txt(636,207,'将来区間',13,ORANGE)
 vals=[110-30*math.sin(i*.32)-i*.22 for i in range(60)];b+=path([(50+i*8,vals[i]) for i in range(60)],BLUE)+path([(530+i*8,110-30*math.sin((i+60)*.32)-(i+60)*.22) for i in range(28)],ORANGE,dash=True)
 b+=txt(400,260,'異常検知：観測からスコアを作る',18)+line(45,380,760,380,arrow=False)+line(45,304,760,304,ORANGE,dash=True,arrow=False)+txt(720,294,'閾値',12,ORANGE)
 score=[.12+.04*math.sin(i*.8)+.7*math.exp(-((i-48)/2.5)**2) for i in range(88)];b+=path([(50+i*8,370-v*115) for i,v in enumerate(score)],GREEN)+txt(350,413,'スコアが閾値を越える区間を候補にする',13)
 save('timeseries.svg',b,440,'予測区間と異常スコア、閾値を対応付ける合成系列の模式図')
 # A computed routing example: two feasible tours on the same fixed cities.
 pts=[(40,105),(90,35),(180,55),(245,125),(210,215),(110,235)];orders=[[0,2,4,1,3,5,0],[0,1,2,3,4,5,0]];b=''
 for ox,order,title in [(30,orders[0],'訪問順序 A'),(425,orders[1],'訪問順序 B')]:
  distance=0
  for i,j in zip(order,order[1:]):
   x,y=pts[i];xx,yy=pts[j];distance+=math.hypot(x-xx,y-yy);b+=line(ox+x,40+y,ox+xx,40+yy,ORANGE if ox==30 else GREEN,arrow=False)
  for i,(x,y) in enumerate(pts):b+=f'<circle cx="{ox+x}" cy="{40+y}" r="9" fill="{BLUE}"/>'+txt(ox+x+17,40+y+4,str(i+1),12)
  b+=txt(ox+155,25,title,18)+txt(ox+155,325,f'総距離 {distance:.1f} 座標単位',14)
 save('routing.svg',b,350,'同じ6都市を回る2つの訪問順序と計算した総距離')
 # Original pose comparison, not a model output.
 b=''
 for ox,shift,title in [(30,0,'時刻 t'),(425,26,'時刻 t+1')]:
  coords=[(155,65),(155,112),(115,122),(195,122),(85,160-shift),(222,156+shift),(165,182),(129,230),(205,220)]
  for a,c in [(0,1),(1,2),(1,3),(2,4),(3,5),(1,6),(6,7),(6,8)]:x,y=coords[a];xx,yy=coords[c];b+=line(ox+x,y,ox+xx,yy,GREEN,arrow=False,width=5)
  for x,y in coords:b+=f'<circle cx="{ox+x}" cy="{y}" r="7" fill="{ORANGE}"/>'
  b+=txt(ox+155,28,title,18)
 save('pose.svg',b,260,'姿勢推定の出力である関節点と、その時刻間の変化を示す模式図')
 # Short synthetic sound components, amplitude limited with edge fades.
 rate=16000;duration=2.4
 for name,components in [('low.wav',[(220,.20)]),('high.wav',[(660,.15)]),('mix.wav',[(220,.20),(660,.15)])]:
  with wave.open(str(ROOT/'assets'/name),'wb') as f:
   f.setnchannels(1);f.setsampwidth(2);f.setframerate(rate)
   samples=[]
   for i in range(int(rate*duration)):
    t=i/rate;fade=min(1,t/.06,(duration-t)/.06);v=sum(a*math.sin(2*math.pi*hz*t) for hz,a in components)*fade;samples.append(struct.pack('<h',round(v*32767)))
   f.writeframes(b''.join(samples))
