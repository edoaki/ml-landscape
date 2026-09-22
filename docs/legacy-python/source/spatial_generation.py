"""Original Genie and Sora as dated, visual research examples."""
from common import *

SORA='https://openai.com/index/video-generation-models-as-world-simulators/'
GENIE='https://deepmind.google/models/genie/'


def body():
    b=sec('video-generation','動画生成',
        p('動画を作るには、1枚の画像の見た目だけでなく、<strong>ものがどう動き、場面が時間とともにどう変わるか</strong>も学ぶ必要があります。人が歩くと姿勢が変わり、車が進むと周囲の景色も変わります。動画生成モデルは、多くの映像からこうした変化のパターンを学習します。')+
        p('この「今の状態から、次にどうなるか」を予測する考え方が<strong>世界モデル</strong>です。Soraは文章に合った動きのある映像を生成し、Genie 3はユーザーの操作に応じて、その先の映像を生成します。学んだ動きには誤りもあり、物理法則を正確に再現できるとは限りません。'))
    b+=sec('sora','Sora',
        '<figure><video controls playsinline preload="metadata"><source src="assets/sora-tokyo-clip.mp4" type="video/mp4"></video><figcaption>'+ref('https://openai.com/index/sora/','Sora：Tokyo walk（2024）')+'。公式の生成映像から冒頭15秒を抜粋。</figcaption></figure>'+
        p('「ネオンが光る夜の東京を、黒いジャケットと赤いドレスの女性が歩く」という文章から生成。人物の歩行と、移り変わる街並みを一つの映像にしています。'))
    b+=sec('genie','Genie 3',
        p('<strong>ユーザーの入力に合わせて、次の画面を予測し続ける。</strong>')+
        '<figure><video controls playsinline preload="metadata" poster="assets/genie3-racetrack-poster.jpg"><source src="assets/genie3-racetrack.mp4" type="video/mp4"></video><figcaption>'+ref(GENIE,'Genie 3：Backyard racetrack')+'。公式の操作デモ映像。</figcaption></figure>'+
        p('今の画面と操作、それまでの履歴から次の画面を生成します。例えば、車を右に曲げる操作をすると、車の向きと周囲の景色が変わります。生成した画面をもとに次の操作へ応答することを繰り返すので、ゲームのように動かせます。')+
        p('あらかじめ用意した3D物体を物理エンジンで動かす方式とは異なり、操作に応じた映像そのものを生成しています。ここに掲載しているのは、その操作結果を記録した動画です。'))
    return b
