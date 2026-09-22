"""Science applications: why they help, then concrete inputs and outputs."""
from common import *
from pathlib import Path


def io(left, right, model):
    return f'<div class="science-io"><div><span>入力</span><strong>{left}</strong></div><div class="science-arrow"><small>{model}</small><b aria-hidden="true">→</b></div><div><span>出力</span><strong>{right}</strong></div></div>'


def ref(url, text):
    return f'<a href="{url}" target="_blank" rel="noopener">{text}</a>'


def svg(content, label, view='0 0 300 190'):
    return f'<svg viewBox="{view}" role="img" aria-label="{label}">{content}</svg>'


def example(left, middle, right, caption):
    return f'<figure class="science-example"><div class="science-explained"><div>{left}</div><div class="science-between">{middle}<b aria-hidden="true">→</b></div><div>{right}</div></div><figcaption>{caption}</figcaption></figure>'


def protein_pair():
    import math
    rows=[r for r in (ROOT/'assets/alphafold-P69905-v6.pdb').read_text().splitlines() if r.startswith('ATOM') and r[12:16].strip()=='CA']
    codes=dict(zip('ALA ARG ASN ASP CYS GLN GLU GLY HIS ILE LEU LYS MET PHE PRO SER THR TRP TYR VAL'.split(),'ARNDCQEGHILKMFPSTWYV'))
    seq=''.join(codes[r[17:20]] for r in rows)
    lines=''.join(f'<div><span>{i+1:03}</span><code>{seq[i:i+20]}</code></div>' for i in range(0,len(seq),20))
    xyz=[tuple(float(r[a:b]) for a,b in [(30,38),(38,46),(46,54)]) for r in rows]
    # Orthographic view of the actual C-alpha backbone, with depth shading.
    pts=[(.82*x+.57*z, -.25*x+.90*y+.36*z, -.51*x-.44*y+.74*z) for x,y,z in xyz]
    lo=[min(v[i] for v in pts) for i in range(3)];hi=[max(v[i] for v in pts) for i in range(3)]
    scale=min(260/(hi[0]-lo[0]),240/(hi[1]-lo[1]))
    pts=[(160+(x-(lo[0]+hi[0])/2)*scale,150-(y-(lo[1]+hi[1])/2)*scale,z) for x,y,z in pts]
    segments=[]
    for i in range(len(pts)-1):
        p0=pts[max(0,i-1)];p1=pts[i];p2=pts[i+1];p3=pts[min(len(pts)-1,i+2)]
        path=f'M{p1[0]:.2f},{p1[1]:.2f} C{p1[0]+(p2[0]-p0[0])/6:.2f},{p1[1]+(p2[1]-p0[1])/6:.2f} {p2[0]-(p3[0]-p1[0])/6:.2f},{p2[1]-(p3[1]-p1[1])/6:.2f} {p2[0]:.2f},{p2[1]:.2f}'
        light=30+30*((p1[2]+p2[2])/2-lo[2])/(hi[2]-lo[2])
        segments.append(((p1[2]+p2[2])/2,f'<path d="{path}" stroke="hsl(190 35% {light:.1f}%)" stroke-width="7"/><path d="{path}" stroke="white" stroke-opacity=".22" stroke-width="2"/>'))
    structure=svg('<g fill="none" stroke-linecap="round">'+''.join(seg for depth,seg in sorted(segments))+'</g>','ヘモグロビンα鎖の実際の予測座標を用いた立体構造','0 0 320 300')
    return example('<strong>入力｜アミノ酸配列</strong><div class="science-seq-panel">'+lines+'</div><p>1文字がアミノ酸1個。<br>この順番でつながっています。</p>','AlphaFold2','<strong>出力｜同じタンパク質の立体構造</strong><div class="science-structure">'+structure+'</div><p>配列に対応する鎖が、<br>どう折りたたまれるかを予測。</p>','ヘモグロビンα鎖（142残基）。左右は同じタンパク質。'+ref('https://alphafold.ebi.ac.uk/entry/P69905','AlphaFold DB：P69905 / v6')+'の予測座標から主鎖を描画。陰影は奥行きを示します。')


def cells():
    before=[[1,2,1,1,2,1,2,1],[4,3,4,4,3,4,3,4],[2,2,3,2,3,2,2,3],[1,1,2,1,1,2,1,1],[3,2,3,3,2,3,3,2],[2,1,2,2,1,2,1,2]]
    after=[[4,3,4,4,3,4,3,4],[1,2,1,1,2,1,2,1],before[2],[3,3,4,3,3,4,3,3],before[4],[1,1,1,1,1,1,1,1]]
    palette=['#edf2f1','#dce9e6','#b7d1ca','#73a69a','#2e7568']
    def heatmap(values):
        content='<text x="154" y="26" text-anchor="middle" fill="#62796f" font-size="12">細胞ごとのデータ</text>'
        for r,row in enumerate(values):
            content+=f'<text x="44" y="{58+r*27}" text-anchor="end" fill="#476056" font-size="13">{chr(65+r)}</text>'
            for c,v in enumerate(row):content+=f'<rect x="{58+c*25}" y="{41+r*27}" width="22" height="23" rx="2" fill="{palette[v]}"/>'
        content+='<text x="29" y="229" fill="#62796f" font-size="12">発現量　少</text>'
        for i,color in enumerate(palette):content+=f'<rect x="{105+i*22}" y="215" width="22" height="13" fill="{color}"/>'
        content+='<text x="225" y="228" fill="#62796f" font-size="12">多</text>'
        return svg(content,'行AからFは遺伝子、列は細胞。色が濃いほど発現量が多い','0 0 300 250')
    return '<div class="science-condition">追加の入力 <strong>与える刺激の種類</strong></div>'+example('<strong>入力｜刺激前の細胞データ</strong>'+heatmap(before)+'<p>行は遺伝子A〜F、列は細胞。<br>色で遺伝子の発現量を表します。</p>','scGen','<strong>出力｜刺激後の予測データ</strong>'+heatmap(after)+'<p>同じ行を左右で比較。<br>A・Dが増え、B・Fが減る例。</p>','入力・出力の見方を示す模式データです。色が濃いほど発現量が多く、C・Eは変わらない例。実測値やscGenの実行結果ではありません。')


def design():
    def panel(view,label):
        x,y,w,h=view.split(); clip='rf-'+x
        return svg(f'<defs><clipPath id="{clip}"><rect x="{x}" y="{y}" width="{w}" height="{h}"/></clipPath></defs><g clip-path="url(#{clip})"><image href="assets/rfdiffusion-binder.png" width="1087" height="290"/></g>',label,view)
    left='<strong>入力｜結合させたい相手</strong><div class="science-structure">'+panel('211 86 154 148','論文中の結合相手のタンパク質構造')+'</div><p><span class="science-key target"></span>青緑＝結合相手。<br>この構造と結合させたい場所を指定。</p>'
    right='<strong>出力｜新しく設計した候補</strong><div class="science-structure">'+panel('787 65 215 210','同じ青緑の相手と新たに生成されたピンクのタンパク質構造')+'</div><p><span class="science-key binder"></span>ピンク＝新しい候補。<br>青緑の相手に結合する形を生成。</p>'
    return example(left,'RFdiffusion',right,ref('https://www.nature.com/articles/s41586-023-06415-8/figures/1','Watson et al. (2023), Fig. 1b')+'の入力と最終候補を抜粋。リボンはタンパク質の鎖の折りたたみを表します。本当に結合するかは実験で確かめます。')


def inverse():
    ground='<path d="M15 45H285" stroke="#667663" stroke-width="3"/><text x="20" y="29" font-size="14">振動を起こす</text><text x="202" y="29" font-size="14">センサー</text><circle cx="65" cy="45" r="6" fill="#bf7a4d"/><rect x="236" y="36" width="14" height="10" fill="#527c9f"/><path d="M65 48L150 145L243 48" fill="none" stroke="#b2bdb3" stroke-dasharray="5 4"/><circle class="science-wave-dot" cx="243" cy="48" r="7" fill="#bf7a4d"/><text x="95" y="181" font-size="14">地下を伝わる波</text>'
    traces='<path d="M15 95H70L78 85L86 111L96 60L106 134L119 77L132 108L143 89L155 95H285" fill="none" stroke="#527c9f" stroke-width="3"/><text x="48" y="164" font-size="14">いつ・どんな揺れが届いた？</text>'
    layers='<rect x="15" y="45" width="270" height="110" fill="#e4d5b6"/><path d="M15 97Q120 67 285 111V155H15Z" fill="#7ba7b5"/><text x="60" y="68" font-size="14">波がゆっくり進む層</text><text x="80" y="140" font-size="14">速く進む層</text>'
    return '<figure class="science-example science-motion" data-science-motion="seismic"><div class="science-seismic"><div><strong>① 地面で波を測る</strong>'+svg(ground,'振動源から地下を通った波が地表のセンサーに届く')+'</div><div><strong>② 入力：揺れの記録</strong>'+svg(traces,'地表のセンサーが記録した波形')+'</div><div><strong>③ 出力：地下の構造</strong>'+svg('<g class="science-layers">'+layers+'</g>','波の進む速さの違いから推定する地下の層')+'</div></div><div class="science-controls" hidden><button type="button" class="science-play">波を測って、地下を推定する</button><label>進み方 <input aria-label="地下の推定：コマ送り" class="science-progress" type="range" min="0" max="100" value="100"></label></div><p class="science-motion-status" aria-live="polite">地表の揺れの記録から、見えない地下の構造を推定します。</p><figcaption>観測から推定までの模式アニメーション。波の経路・波形・地層は説明用で、実際の計算結果ではありません。</figcaption></figure>'


def body():
    b=sec('science','科学研究で、AIは何に役立つ？',p('新しい薬や材料を見つけるには、たくさんの実験や計算が必要です。AIで「どうなりそうか」を予測したり、「試すとよさそうな候補」を出したりすると、次に何を調べるかを絞れます。')+p('たとえば、薬の候補を全部作る前に有望なものを選ぶ。時間のかかる計算の代わりに、水の動きをすばやく予測する。<strong>AIの結果を手がかりにして、実験や詳しい計算で確かめる</strong>、という使い方です。'))
    b+=p('<strong>最初の3つの関係：</strong>細胞の中では、タンパク質がさまざまな仕事をしています。AlphaFold2はタンパク質の「形を予測」、RFdiffusionは「新しい形を設計」。細胞応答予測は、刺激を受けた「細胞の変化」を予測します。')
    b+=sec('protein','1．AlphaFold2：タンパク質の形を予測する',p('タンパク質は、アミノ酸が鎖のようにつながり、折りたたまれたものです。<strong>材料の並びから、できあがる3Dの形を予測する</strong>のがAlphaFold2です。')+protein_pair()+p('形が分かると、タンパク質の働きや、薬がどこに結びつきそうかを調べる手がかりになります。')+p('<strong>2024年ノーベル化学賞につながった研究です。</strong>AlphaFold2を開発したDemis HassabisとJohn Jumperは、タンパク質構造予測への貢献で受賞しました。 '+ref('https://www.nobelprize.org/prizes/chemistry/2024/jumper/facts/','ノーベル賞公式')))
    b+=sec('cells','2．細胞応答予測：刺激を与えると、どう変わる？',p('細胞に刺激を与えると、働く遺伝子が変わります。scGenは、<strong>刺激を与える前のデータから、与えた後の変化を予測するAI</strong>です。ここでの「細胞の状態」は、遺伝子ごとの発現量を指します。')+cells()+p('たとえば、ある刺激でどの遺伝子の働きが強まりそうかを予測します。実験で調べたい細胞や条件を選ぶ手がかりになります。')+p(ref('https://www.nature.com/articles/s41592-019-0494-8','研究例：scGen')))
    b+=sec('design','3．RFdiffusion：欲しい条件に合う候補を作る',p('RFdiffusionは、<strong>新しいタンパク質の形を作るAI</strong>です。たとえば、結合させたい相手を指定して、その相手にくっつく形の候補を作ります。')+design()+p('AlphaFold2は「この配列はどんな形？」、RFdiffusionは「この相手に結合する形を作って」という違いです。 '+ref('https://www.nature.com/articles/s41586-023-06415-8','RFdiffusionの論文')))
    b+=sec('simulation','4．物理シミュレーションの近似：水の動きを予測する',io('水の初めの位置と動き<br>＋ 容器の形','その後、水がどう動くか','例：GNS')+'<figure class="science-video"><video controls playsinline preload="metadata" aria-label="水の動きを予測するGNSの研究動画"><source src="assets/gns-water.mp4" type="video/mp4">動画を再生できません。</video><figcaption>'+ref('https://sites.google.com/view/learning-to-simulate','Sanchez-Gonzalez et al. (2020) 著者公開動画：Water-3D')+'。左＝基準となるシミュレーション、右＝AIの予測。水が崩れ、広がっていく様子を比べます。</figcaption></figure>'+p('水や砂の動きを、毎回細かく計算する代わりにAIで予測します。形や条件を変えて、たくさんのパターンを試す研究に役立ちます。'))
    b+=sec('inverse','5．逆問題：地表の揺れから、地下を調べる',p('地面に振動を与え、地表のセンサーで戻ってきた波を測ります。<strong>その記録から、直接見えない地下の層を推定する</strong>のが、物理の逆問題の一例です。')+io('地表で測った<br>揺れの記録','地下で波が進む速さの分布<br>→ 地層を知る手がかり','例：InversionNet')+inverse()+p('地下の構造が分かれば、地表の揺れを計算できます。その向きを逆にして、揺れから地下を調べるので「逆問題」です。AIでこの推定を行う研究があり、地盤や地下資源を調べる手がかりになります。 '+ref('https://openfwi-lanl.github.io/','研究例：OpenFWI / InversionNet')))
    b+=sec('weather','6．気象予測：この後、どこに雨が降る？',p('雨の予測AI「DGMR」の例です。<strong>これまでの雨雲レーダーから、この先の雨の場所と強さを予測します。</strong>')+io('直前20分の<br>雨雲レーダー画像','この先90分の<br>雨の場所と強さ','DGMR')+'<figure class="science-video"><video controls playsinline preload="metadata" poster="assets/dgmr-rain-poster.jpg" aria-label="実際の雨とDGMRの予測を比べる研究動画"><source src="assets/dgmr-rain.mp4" type="video/mp4">動画を再生できません。</video><figcaption><strong>左（Target）＝実際に観測された雨。右（DGMR）＝AIが予測した雨。</strong><br>色のついた部分が雨の範囲。左右で雨の移動や広がりがどれくらい似ているかを見てください。<br>'+ref('https://deepmind.google/blog/nowcasting-the-next-hour-of-rain/','DeepMind・Met Officeの研究公開映像（2021）')+'。英国の事例の上段2画面を抜粋し、見やすいよう3倍の時間で再生します。</figcaption></figure>'+p('短時間先の大雨を予測して、屋外作業や移動、防災の判断に役立てる研究です。 '+ref('https://www.nature.com/articles/s41586-021-03854-z','DGMRの論文')))
    return b+'<script src="assets/science.js" defer></script>'
