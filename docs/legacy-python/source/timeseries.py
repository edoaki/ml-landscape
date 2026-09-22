"""Small, deterministic time-series examples; all values are teaching data."""
from common import *
import json

HISTORY = [32, 28, 26, 25, 28, 38, 52, 64, 70, 73, 75, 74, 72, 70, 69, 72, 80, 88, 84, 72, 61, 51, 43, 36]
FUTURE = [34, 30, 28, 27, 30, 41, 56, 68, 74, 78, 79, 77, 75, 74, 73, 76, 85, 94, 90, 78, 65, 55, 46, 39]
SENSOR = [50, 51, 49, 50, 52, 50, 49, 51, 50, 48, 51, 50, 51, 49, 50, 52, 50, 51, 49, 50, 51, 50, 49, 51]

def points(values, start=0, count=48, low=0, high=100):
    return ' '.join(f'{54+(i+start)*650/(count-1):.2f},{222-(v-low)*174/(high-low):.2f}' for i,v in enumerate(values))

def chart(lines, sensor=False):
    low, high, count = (40, 80, 24) if sensor else (0, 100, 48)
    b = ''
    for value in ([40,50,60,70,80] if sensor else [0,25,50,75,100]):
        y=222-(value-low)*174/(high-low)
        b+=f'<path d="M54 {y}H704" stroke="#dfe7e1"/>'+txt(43,y+4,value,12,anchor='end')
    b+=txt(54,23,'温度（℃）' if sensor else '電力需要（kW）',13,anchor='start')
    if not sensor:
        b+='<path d="M379 40V226" stroke="#738679" stroke-dasharray="4 4"/>'
        b+=txt(210,275,'昨日：入力に使える観測',13)+txt(540,275,'今日：予測してから答え合わせ',13)
        for i in [0,12,23,24,36,47]:
            b+=txt(54+i*650/47,246,f'{i%24}時',11)
    else:
        b+=txt(54,247,'1',12)+txt(393,247,'13',12)+txt(704,247,'24 時間目',12,anchor='end')
    for ident,values,color,start,dash in lines:
        b+=f'<polyline data-line="{ident}" points="{points(values,start,count,low,high)}" fill="none" stroke="{color}" stroke-width="3"'+(' stroke-dasharray="7 5"' if dash else '')+'/>'
    b+='<g data-marks=""></g>'
    return svg(b,285,w=760,label='センサの時間ごとの温度' if sensor else '昨日の電力需要と今日の予測')

def body():
    out=sec('series','時系列：同じ観測でも、問いで出力が変わる',p('時系列は、時間の順に並ぶデータです。例えば1時間ごとの電力需要や、設備の温度です。画像で「何があるか」と「どこにあるか」を分けたように、時系列でも、未来を知りたいのか、異常に気付きたいのかを分けます。')+table(['タスク','入力 → 出力','具体例'],[
        ('<a href="#forecast">将来予測</a>','過去の観測 → 未来の数値','明日の電力需要を見積もる'),
        ('<a href="#anomaly">異常検知</a>','観測 → 普段からの外れ具合・警報','設備の急な温度上昇に気付く'),
        ('<a href="#change">変化点検出</a>','観測 → 振る舞いが変わった時刻','運転モードの切り替わりを見つける'),
        ('<a href="#missing">欠測補完・状態推定</a>','不完全な観測 → 欠けた値・隠れた状態','センサの通信切れを補う')]))
    forecast=chart([('history',HISTORY,BLUE,0,False),('prediction',HISTORY,ORANGE,24,True),('truth',[],GREEN,24,False)])
    out+=sec('forecast','将来予測：今日の電力需要を、昨日から予測する',p('入力は昨日の24時間の電力需要、出力は今日の24個の予測値です。夜に下がり、夕方に上がる形があります。まず「昨日の同じ時刻を使う」と「昨日の最後の値を使う」を切り替え、今日の予測線がどう変わるかを見てください。')+f'''<figure class="ts-demo" id="ts-forecast">
<div class="ts-controls" hidden><label>予測の方法 <select id="ts-method"><option value="seasonal">昨日の同じ時刻を使う</option><option value="last">昨日の最後の値を使う</option></select></label><button id="ts-reveal" type="button" aria-pressed="false">今日の実測を表示</button></div>
{forecast}<p class="ts-legend">青の実線：昨日の観測　／　橙の破線：今日の予測　／　緑の実線：今日の実測（答え合わせ時）</p>
<p class="ts-status" role="status">今日の実測はまだ隠れています。夕方の山を予測できそうでしょうか。</p>
<figcaption>教材用の合成データ。2つの単純な基準予測をその場で計算します。学習済みの深層モデルの推論ではありません。JavaScript無効時も、昨日と同じ時刻を使う予測を表示します。</figcaption></figure>'''+p('「今日の実測を表示」を押すと、隠していた正解と予測を比べられます。MAE（平均絶対誤差）は、各時刻のずれの大きさを平均した値で、小さいほどよく当たっています。この例では昨日と似た一日の形が続くため、同じ時刻を使う方法が有利です。休日や急な天候変化で形が変われば、同じ方法でも外れます。')+p('深層学習でも「過去を入力し、未来と比べて学ぶ」という枠組みは共通です。<a href="rnn.html">RNN</a>や<a href="transformer.html">Transformer</a>などで、多数の系列から傾向や周期を学べます。予測時点で分かっている曜日や天気予報を加えることもあります。'))
    vals=SENSOR.copy();vals[12]+=20
    out+=sec('anomaly','異常検知：どれくらい外れたら知らせるか',p('設備の温度は普段50℃前後ですが、13時間目だけ急に上がりました。ここでは「50℃との差の絶対値」を異常スコアとし、しきい値を超えた点に赤い丸を付けます。しきい値を1℃、10℃、25℃へ動かしてみてください。')+f'''<figure class="ts-demo" id="ts-sensor"><div class="ts-controls" hidden>
<label>観測のパターン <select id="ts-event"><option value="spike">一瞬だけ上がる</option><option value="shift">上がったまま続く</option><option value="normal">普段どおり</option></select></label>
<label>しきい値 <input id="ts-threshold" type="range" min="1" max="25" value="10" step="1"><output id="ts-threshold-value" for="ts-threshold">10 ℃</output></label></div>
{chart([('baseline',[50]*24,GREEN,0,True),('sensor',vals,BLUE,0,False)],True)}
<p class="ts-legend">青の実線：観測　／　緑の破線：普段の基準 50℃　／　赤い丸：しきい値を超えた観測</p><p class="ts-status" role="status">13時間目は71℃。基準との差21℃が、しきい値10℃を超えます。</p>
<figcaption>教材用の合成温度と、固定した基準からの偏差による検知。故障を診断するモデルではありません。JavaScript無効時は、一瞬の上昇の観測図を表示します。</figcaption></figure>'''+p('低くすると小さな揺れにも警報が出ます。高くしすぎると大きな上昇も見逃します。実際の異常検知では、時刻や運転条件に応じた予測からのずれなどを使い、別の検証データでしきい値を決めます。スコアが大きいだけで、故障の原因まで分かるわけではありません。'))
    out+=sec('change','変化点検出：一瞬の外れと、状態の切り替わり',p('上のデモを「上がったまま続く」に切り替えてください。13時間目から温度が約70℃になり、それ以降も高い状態が続きます。異常検知は各観測に警報を出しますが、変化点検出が答えたいのは「いつから普段の状態が変わったか」です。')+table(['同じセンサの例','異常検知で見るもの','変化点検出で見るもの'],[('一瞬だけ上がる','13時間目の大きなずれ','すぐ元に戻り、持続する切り替わりとは異なる'),('上がったまま続く','13時間目以降の大きなずれ','13時間目付近で平均の水準が変わったこと')])+p('このデモの切り替わりは教材で設定した正解で、変化点を推定するアルゴリズムは実行していません。実際には複数の観測を集めて変化を判断するため、変化した時刻と検知できた時刻はずれることがあります。意図した運転モード変更なら、変化があっても故障ではありません。'))
    out+=sec('missing','欠測補完：記録されなかった値を埋める',p('通信切れで12時の温度が欠けたとします。前後の値の間を直線でつなぐと、12時を51℃と補えます。これは観測値ではなく推定値です。')+table(['時刻','11時','12時','13時'],[('入力の記録','50℃','欠測','52℃'),('前後を使った補完','50℃','51℃（推定）','52℃')])+p('13時まで記録した後の補完なら、前後の値を使えます。一方、12時の時点で判断するなら13時の観測はまだ使えません。状態推定では、ノイズのある観測から、直接見えない設備内部の温度などを推定します。<a href="ssm.html">状態空間モデル</a>の「状態を更新する」考え方につながります。'))
    out+=sec('series-evaluation','時間の順序を守って、役に立つか確かめる',p('例えば1〜7月で学習し、8月で方法やしきい値を選び、9月を最後の評価に残します。隣り合う時刻をランダムに混ぜると、実際の未来予測より簡単な条件になる場合があります。正規化の平均なども、学習期間だけから計算します。')+p('予測では時間帯ごとの誤差や、予測を何時間先まで伸ばすかを見ます。異常検知では誤警報・見逃し・検知の遅れを見ます。ほとんど正常な設備では「すべて正常」と答えても正解率が高くなるため、正解率だけでは評価できません。')+cards([('FORECASTING','TimesFMの公開結果','学習済みの時系列モデルの予測と正解を、原論文の図で比較する。','research.html#signals'),('ANOMALY DETECTION','Merlionの公開結果','観測の波形と異常スコアを、著者公開の結果で見る。','research.html#signals')]))
    return out+'<script type="application/json" id="ts-data">'+json.dumps(dict(history=HISTORY, future=FUTURE, sensor=SENSOR))+'</script><script src="assets/timeseries.js" defer></script>'
