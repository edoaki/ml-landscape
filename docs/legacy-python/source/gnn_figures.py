"""Graph-centered GNN calculations with optional numeric transitions."""
from common import *

FEATURES = [(1, 0), (0, 2), (2, 1), (1, 1)]
W = [(1, -1), (1, 1)]
ATT = [-1, 0, 1, .5]

def vec(x):
 return '(' + ', '.join(f'{v:.3f}'.rstrip('0').rstrip('.') for v in x) + ')'

def gat_values(features=FEATURES, w=W, a=ATT):
 z = [tuple(sum(row[j]*h[j] for j in range(2)) for row in w) for h in features]
 raw = [sum(v*t for v,t in zip(a,z[0]+u)) for u in z]
 scores = [max(s,.2*s) for s in raw]
 exps = [math.exp(s) for s in scores]
 alpha = [e/sum(exps) for e in exps]
 parts = [tuple(c*v for v in u) for c,u in zip(alpha,z)]
 out = tuple(sum(u[j] for u in parts) for j in range(2))
 return z,raw,scores,exps,alpha,parts,out

def pipeline(items):
 return '<div class="gnn-pipeline">'+''.join(f'<div><strong>{title}</strong><span>{value}</span></div>' for title,value in items)+'</div>'

ALL_FEATURES = FEATURES + [(0,1),(2,0)]

def graph_values(values=None, updated=None, labels=None, active='ABCD', selected=None, center_note='Aを更新', value_name='特徴', changed_labels=False, changed_selection=False):
 """Values stay inside nodes; only genuine representation changes animate."""
 values = values or ALL_FEATURES
 updated = updated or {}
 coords=[(180,235),(85,65),(365,80),(365,385),(515,185),(515,295)]
 b=''
 for i,j in [(0,1),(0,2),(0,3),(2,4),(3,5)]:
  x,y=coords[i];xx,yy=coords[j]
  enabled=chr(65+i) in active and chr(65+j) in active
  chosen=selected is None or j in selected or i!=0
  color=BLUE if enabled and chosen else '#c4ccc1'
  if changed_selection and i==0: color='#b6531d'
  dash='' if chosen else ' stroke-dasharray="6 6"'
  b+=f'<path class="gnn-edge" d="M{xx} {yy} L{x} {y}" fill="none" stroke="{color}" stroke-width="{4 if changed_selection and i==0 else 3 if enabled and chosen else 1.5}"{dash}/>'
  if i==0 and labels:
   lx,ly=(x+xx)/2,(y+yy)/2
   b+=f'<rect x="{lx-47}" y="{ly-13}" width="94" height="26" rx="8" fill="{"#fff0df" if changed_labels else "#fff"}" stroke="{"#b6531d" if changed_labels else "#dde5d7"}" stroke-width="{2.5 if changed_labels else 1}"/>'+txt(lx,ly+5,labels[j],15,'#b6531d' if changed_labels else GREEN)
 if labels:
  b+=f'<path d="M115 215 C35 140 35 325 115 270" fill="none" stroke="{GREEN}" stroke-width="2"/>'
  b+=f'<rect x="9" y="229" width="88" height="28" rx="8" fill="{"#fff0df" if changed_labels else "#fff"}" stroke="{"#b6531d" if changed_labels else "#dde5d7"}" stroke-width="{2.5 if changed_labels else 1}"/>'+txt(53,248,labels[0],14,'#b6531d' if changed_labels else GREEN)
 for i,(x,y) in enumerate(coords):
  enabled=chr(65+i) in active
  target=updated.get(i)
  changed=target is not None and tuple(target)!=tuple(values[i])
  color=GREEN if i==0 else BLUE if enabled else '#7e8d79'
  fill='#eef5e9' if i==0 else '#f3f7fb' if enabled else '#f4f4f0'
  if changed: color,fill='#b6531d','#fff0df'
  b+=f'<g class="gnn-node"><rect x="{x-77}" y="{y-43}" width="154" height="86" rx="18" fill="{fill}" stroke="{color}" stroke-width="{3.5 if changed else 2.5 if i==0 else 1.3}"/>'
  b+=txt(x,y-23,chr(65+i),18,color)
  if target is not None:
   b+=txt(x,y-2,vec(values[i])+' →',14,'#73816e')
   attrs=f'data-from="{esc(vec(values[i]),quote=True)}" data-to="{esc(vec(target),quote=True)}" data-start="{",".join(map(str,values[i]))}" data-end="{",".join(map(str,target))}"'
   b+=f'<text {attrs} x="{x}" y="{y+23}" text-anchor="middle" fill="{color}" font-size="19" font-weight="650">{vec(target)}</text>'
  else:
   b+=txt(x,y+11,vec(values[i]),20,color)
  b+='</g>'
 b+=txt(300,463,center_note,15,GREEN)
 changes=[]
 if updated: changes.append('ノードの数値を更新')
 if changed_labels: changes.append('辺のスコア・係数を追加または変更')
 if changed_selection: changes.append('参照する近隣を選択（点線は不採用）')
 legend='<p class="gnn-change-legend"><strong>橙・太枠：今回変わった部分</strong><br>'+ '／'.join(changes) +'</p>' if changes else ''
 return '<div class="gnn-value-graph">'+svg(b,480,w=600,label=f'{value_name}をノード内に表示したグラフ。'+center_note)+legend+'</div>'

def calc(title, purpose, graphic, working, animate=False):
 button='<button type="button" class="gnn-replay" hidden>数値の変化を見る ↻</button><p class="gnn-animation-note">動きは変更前後をつなぐ表示です。途中の値は追加の演算や学習を表しません。</p>' if animate else ''
 return '<div class="gnn-calc"><h3>'+title+'</h3><p class="gnn-purpose">'+purpose+'</p><div class="gnn-calc-layout"><div class="gnn-graph-panel">'+graphic+button+'</div><aside class="gnn-working" aria-label="計算過程">'+working+'</aside></div></div>'

def basics():
 return calc('辺を通して、隣の情報を受け取る','自分の特徴だけでは分からない関係の情報を、隣の特徴から取り込みます。',graph_values(center_note='B・C・DからAへ'),p('ノード内の2個の数が特徴ベクトルです。線がある相手の特徴を集め、Aの数値を新しい表現へ更新します。')+p('同じ層では、全ノードが一つ前の層の特徴を参照します。更新済みのAをすぐBの同じ層の計算に使うわけではありません。')+p('2層にすると、E → C → A、F → D → Aと、遠くの情報も届きます。以下ではAの1回の更新を拡大します。'))

def gcn():
 coeff=[.25,1/math.sqrt(8),1/math.sqrt(12),1/math.sqrt(12)]
 parts=[tuple(c*v for v in h) for c,h in zip(coeff,FEATURES)]
 out=tuple(sum(v[j] for v in parts) for j in range(2))
 labels=['¼','1/√8','1/√12','1/√12']
 return calc('次数に応じて、取り込む量を調整する','接続数によって集約の規模が偏りすぎないように、受け手と送り手の次数で重みを調整します。',graph_values(labels=labels,center_note='線上の値が集約係数',changed_labels=True),p('自己ループを加え、自分も参照先にします。自己ループ込みの次数はA=4、B=2、C=D=3、E=F=2。')+eq(r'c_{Au}=\frac{1}{\sqrt{\tilde d_A\tilde d_u}}','例：B → Aは1/√(4×2) ≈ 0.354。')+p('図のAの左側の線は、自分を集める係数1/4です。係数は特徴値ではなく接続数から決まります。係数の合計は約1.181で、合計1の平均とは異なります。'))+calc('隣の特徴を混ぜて、Aの数値を更新する','次数で重み付けした特徴を足し、近隣の情報を含む新しいAの表現を作ります。',graph_values(updated={0:out},labels=labels,center_note='上：入力 ／ 下：更新後'),table(['送り手','係数 × 特徴'],[(n, f'{c:.3f} × {vec(h)} = {vec(v)}') for n,c,h,v in zip('ABCD',coeff,FEATURES,parts)])+p(f'成分ごとに足すと <strong>{vec(out)}</strong>。この例ではW=Iなので変換後も同じで、ReLU後も変わりません。通常は共有Wを学習します。'),True)

def gat():
 z,raw,scores,exps,alpha,parts,out=gat_values()
 transformed=z+[(-1,1),(2,2)]
 body=calc('特徴を、比較と集約に使う表現へ変換する','元の特徴をそのまま使う代わりに、学習するWで予測に役立つ成分の組み合わせを作ります。',graph_values(updated=dict(enumerate(transformed)),active='ABCDEF',center_note='上：h ／ 下：z = Wh'),eq(r'W=\begin{pmatrix}1&-1\\1&1\end{pmatrix},\quad z_u=Wh_u','Wは全ノードで共有する2×2行列。特徴は列ベクトルとして掛けます。')+p('<strong>Bの中の数値：</strong><br>(0, 2) → (1×0 − 1×2, 1×0 + 1×2)<br>→ <strong>(−2, 2)</strong>')+p('Aは(1, 1)、Cは(1, 3)、Dは(0, 2)になります。このzをスコア作りにも、最後の集約にも使います。'),True)
 body+=calc('受け手と送り手から、参照のスコアを作る','どの隣を強く取り込むかを決めるために、Aと各送り手の特徴を一つの数へまとめます。',graph_values(values=transformed,labels=[f'{v:.1f}' for v in scores],center_note='線：LeakyReLU後のスコア',value_name='変換後の特徴z',changed_labels=True),eq(r's_{Au}=a^{\mathsf T}[z_A\Vert z_u],\quad a=(-1,0,1,0.5)^{\mathsf T}','連結∥は2次元＋2次元を並べる操作。足し算ではありません。')+p('<strong>A ← B：</strong><br>[z_A ∥ z_B] = [1, 1, −2, 2]<br>s_AB = −1×1 + 0×1 + 1×(−2) + 0.5×2 = <strong>−2</strong>')+p('負のスコアにも小さな傾きを残すため、LeakyReLUを使います。この例では負なら0.2倍し、非負ならそのままです。Bの−2は<strong>−0.4</strong>になります。')+table(['送り手','内積 s','LeakyReLU後 e'],[(n,f'{s:g}',f'{e:g}') for n,s,e in zip('ABCD',raw,scores)]))
 body+=calc('スコアを、合計1の集約係数へ変える','参照先どうしのスコアを比較できるように、指数を取り、同じ受け手の参照先内で正規化します。',graph_values(values=transformed,labels=[f'{v:.3f}' for v in alpha],center_note='線：softmax後の係数α',value_name='変換後の特徴z',changed_labels=True),eq(r'\alpha_{Au}=\frac{\exp(e_{Au})}{\sum_{k\in\{A,B,C,D\}}\exp(e_{Ak})}','分母はA自身と直接の隣B・C・Dだけです。E・Fは含みません。')+table(['送り手','e → exp(e)','α'],[(n,f'{e:g} → {x:.3f}',f'{a:.3f}') for n,e,x,a in zip('ABCD',scores,exps,alpha)])+p(f'分母 = {" + ".join(f"{e:.3f}" for e in exps)} ≈ <strong>{sum(exps):.3f}</strong>。係数の合計は1です。Bのスコアは負でしたが、係数は0にはなりません。'))
 body+=calc('重み付きの特徴を集め、Aの数値を更新する','強く参照する相手ほど大きく寄与するように、変換後の特徴zにαを掛けて足します。',graph_values(values=transformed,updated={0:out},labels=[f'{v:.3f}' for v in alpha],center_note='上：z_A ／ 下：新しいh_A',value_name='変換後の特徴と更新後の特徴'),table(['送り手','α × z'],[(n,f'{c:.3f} × {vec(u)} = {vec(v)}') for n,c,u,v in zip('ABCD',alpha,z,parts)])+p(f'第1成分：{" + ".join(f"({v[0]:.3f})" for v in parts)} = <strong>{out[0]:.3f}</strong><br>第2成分：{" + ".join(f"{v[1]:.3f}" for v in parts)} = <strong>{out[1]:.3f}</strong>')+eq(r'h_A^\prime=\operatorname{ReLU}\left(\sum_u\alpha_{Au}z_u\right)','この例は中間層の活性化としてReLUを選択。両成分が正なので値は変わりません。')+p('Aの元の特徴(1, 0)が、変換を経て最終的に<strong>'+vec(out)+'</strong>に更新されました。'),True)
 return body

def heads():
 out=gat_values()[-1]
 second=gat_values(w=[(1,0),(0,1)],a=[0,1,-1,.5])
 return calc('複数のheadの結果を、Aの中に並べる','異なるW・aで集めた複数の表現を残すため、headごとの出力を連結します。',pipeline([('head 1のA',vec(out)),('head 2のA',vec(second[-1])),('連結後のA：4次元',vec(out+second[-1]))]),p('head 1は上の計算。head 2はW₂=I、a₂=(0, 1, −1, 0.5)です。')+table(['head 2','A','B','C','D'],[(label,*[f'{x:.3f}' for x in vals]) for label,vals in [('内積',second[1]),('LeakyReLU',second[2]),('softmax',second[4])]])+p('中間層では連結します。原論文の最終分類層ではheadの出力を平均してから出力の活性化を適用します。'))

def sage():
 return calc('使う隣を選び、その特徴を平均する','大きなグラフで計算対象が増えすぎないように、近隣をサンプリングして代表的な特徴をまとめます。',graph_values(active='ABC',selected=[1,2],center_note='B・Cを採用 ／ Dは今回は不使用',changed_selection=True),p('Aの近隣B・C・Dから、今回はB・Cの2個を選びます。点線のDはグラフから削除したわけではありません。')+pipeline([('Bの特徴','(0, 2)'),('Cの特徴','(2, 1)'),('近隣平均 m_A','((0, 2) + (2, 1)) / 2 = (1, 1.5)')])+p('平均にはAを入れません。自己情報はこの後、別に合わせます。B・Dを選んだ場合の平均は(0.5, 1.5)となります。'))+calc('自己情報と近隣情報を合わせ、Aを更新する','自分の特徴と周囲の特徴を両方残してから、共有Wで新しい表現へ変換します。',graph_values(updated={0:(2,1.5)},active='ABC',selected=[1,2],center_note='上：入力 ／ 下：変換・ReLU後'),p('<strong>連結：</strong><br>[h_A ∥ m_A] = [1, 0, 1, 1.5]<br>2次元と2次元を並べ、4次元にします。')+eq(r'W=\begin{pmatrix}1&0&1&0\\0&1&0&1\end{pmatrix}','2×4の例示用Wで、4次元を2次元へ変換します。')+p('第1成分：1×1 + 0×0 + 1×1 + 0×1.5 = <strong>2</strong><br>第2成分：0×1 + 1×0 + 0×1 + 1×1.5 = <strong>1.5</strong>')+p('ReLU後は<strong>(2, 1.5)</strong>。この値を次の図で正規化します。'),True)+calc('ベクトルの長さをそろえる','表現の方向を保ちながら大きさをそろえるために、ベクトルを自分の長さで割ります。',graph_values(values=[(2,1.5)]+ALL_FEATURES[1:],updated={0:(.8,.6)},active='A',center_note='上：正規化前 ／ 下：正規化後'),p('長さ = √(2² + 1.5²) = <strong>2.5</strong><br>(2, 1.5) / 2.5 = <strong>(0.8, 0.6)</strong>')+p('元のAの(1, 0)が、近隣平均との連結・変換を経て、最終的に(0.8, 0.6)へ更新されました。')+p('ここでは原論文のL2正規化に従います。ゼロベクトルの扱いは実装で定めます。'),True)

def content():
 body=sec('basics','GNN：隣の特徴を集めて、点の表現を更新する',sub('なぜGNNが必要なのか：つながりも予測に使いたい',p('分子の性質は原子の種類だけでなく、どの原子がどの原子と結合しているかで変わります。画像用CNNのような一定の格子を前提にすると、点ごとに隣の数が違うデータをそのまま扱えません。また、原子に付けた番号を変えただけで分子の予測が変わっても困ります。そこで、辺でつながる相手から情報を集め、近隣を並べる順序によらず表現を更新する仕組みを使います。'))+p('グラフは点（ノード）と関係（辺）で表すデータです。分子なら原子と結合、文献なら論文と引用に対応します。GNNはグラフを使うニューラルネットワークの総称。ここでは同じ6ノードで、GCN・GAT・GraphSAGEの計算方法を比べます。')+basics())
 body+=sec('gcn','GCN：次数から集約係数を決める',sub('なぜGCNが作られたのか：特徴と関係を、軽い計算で学習に使う',p('例えば論文の分野を分類するとき、本文の特徴に加えて引用関係も手がかりにできれば、ラベルが少ない論文集合でも学習を助けられます。ここで扱うKipfとWellingのGCNは、グラフ上の畳み込みを近似し、近隣の特徴を混ぜて共通の重みで変換する簡潔な層にしました。辺に沿った局所計算を使い、特徴とグラフ構造を効率よく組み合わせることが狙いです。'))+gcn()+p('全ノードの更新を一括して計算するために、同じ近隣集約を行列の積で表します。')+eq(r'H^{(\ell+1)}=\sigma(\tilde D^{-1/2}\tilde A\tilde D^{-1/2}H^{(\ell)}W^{(\ell)})','全ノードをまとめた式。Hの各行がノード特徴、Ãは自己ループを追加した隣接行列、D̃はその次数を並べた対角行列です。上の局所計算を全ノードについて行います。'))
 body+=sec('gat','GAT：係数ができるまでを追う',sub('なぜGATが作られたのか：隣の重要さを特徴から決めたい',p('つながっている相手が、どれも同じように予測に役立つとは限りません。GCNの次数に基づく係数だけでは、隣の特徴に応じて重みを付け分けられません。GATは近隣へのAttentionを使い、どの相手の情報を強く取り込むかを学習可能にしました。グラフ全体の複雑な行列分解を必要とせず、近隣ごとに重みを計算する設計です。'))+p('GCNの係数はグラフの次数から決まりました。GATは特徴を変換し、受け手・送り手のペアからスコアを作って係数を計算します。以下は原型GATの加法的Attentionです。TransformerのQ・Kの内積とは式が異なります。')+note('数値例の条件','2次元特徴、1 head、自己ループあり、dropoutなし。Wとaは計算を見せるために固定した値で、学習済みモデルの結果ではありません。')+gat())
 body+=sec('heads','Multi-head：別々に集めた表現を連結する',heads())
 body+=sec('learning','GATでは何を学習するのか',p('予測を正解へ近づけるため、損失から逆伝播して特徴変換とスコアのパラメータを更新します。')+pipeline([('入力から計算','W・a → スコア → α → 表現'),('予測と正解を比較','出力ヘッド → 損失'),('逆伝播','W・aなどを更新')])+p('Wとaはデータから学ぶパラメータです。αそのものを辺ごとの固定パラメータとして保存するのではなく、その時の特徴とW・aから計算します。利用時には学んだW・aを固定し、新しい入力に対してαと表現を計算します。')+note('係数の読み方','大きなαは、その集約で強く重み付けしたことを示します。予測全体の重要性や因果関係を直接示すものではありません。原型GATでは、受け手を変えれば近隣の順位が自由に入れ替わるとは限りません。'))
 body+=sec('sage','GraphSAGE：選ぶ・平均する・自己と合わせる',sub('なぜGraphSAGEが作られたのか：新しく現れる点にも表現を作りたい',p('利用者や論文が増えるグラフでは、学習時には存在しなかった点にも予測したくなります。各ノード専用のベクトルを覚える方法だけでは、そのまま新しい点の表現を作れません。GraphSAGEは、ノードの特徴と近隣から表現を作る共通の関数を学びます。さらに近隣をサンプリングし、大きなグラフでも計算対象を抑えます。未知のノードやグラフへ適用するには、入力の特徴が同じ意味で使えることが前提です。'))+p('近隣を何層も展開すると計算対象が増えます。GraphSAGEは近隣をサンプリングして集約する枠組みです。ここでは自己特徴と近隣平均を連結するmean集約を扱います。')+sage())
 body+=sec('compare','三つの違いを計算の順序で比べる',table(['モデル','係数・対象の決め方','自己情報','学ぶもの'],[('GCN','次数 → 係数 → 集約','自己ループとして含む','共有W'),('GAT','特徴変換 → スコア → softmax → 集約','自己へのAttention','headごとの共有W・a'),('GraphSAGE（mean）','近隣を選択 → 平均 → 連結 → 変換','近隣平均と別に連結','共有Wなど')])+p('同じグラフでも計算の設計は異なります。出力の値の大小はモデル性能の比較にはなりません。和や平均で集めるため、近隣を列挙する順序を入れ替えても結果は同じです。'))
 return body
