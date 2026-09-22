"""Video and 3D: concrete outputs, primary-source figures, and guided media."""
from common import *
from spatial_generation import body as generation_body

RAFT = 'https://arxiv.org/abs/2003.12039v3'
ORB = 'https://arxiv.org/abs/2007.11898v2'


def body():
    b=sec('video','動画追跡（SAM 2）',
        p('SAM 2は、指定した対象の領域を動画の各フレームで推定します。元画像と、2人の服にマスクを付けた結果です。')+
        '<div class="spatial-frame-viewer" role="region" aria-label="SAM 2のフレーム切り替え" tabindex="0">'+
        '<div class="spatial-sam-pair"><div data-frame-kind="input">'+img('sam2-input-0.jpg','SAM 2の元画像、frame 0。','元画像 · <span class="frame-caption">frame 0</span>')+'</div><div data-frame-kind="track">'+img('sam2-track-0.png','SAM 2の推論結果、frame 0。','SAM 2の結果 · <span class="frame-caption">frame 0</span>')+'</div></div>'+
        '<div class="spatial-frame-controls"><button type="button" data-frame-step="-1" aria-label="前のフレーム" disabled>←</button><span class="frame-status" aria-live="polite">1 / 7 · frame 0</span><button type="button" data-frame-step="1" aria-label="次のフレーム">→</button></div></div>'+
        p('左右の矢印で、元画像と結果が同時に切り替わります。赤と緑が追跡対象の服の領域です。動いたり一部が隠れたりしても、対象の見えている部分にマスクを付けるタスクです。')+
        p('出典：'+ref('https://github.com/facebookresearch/sam2/blob/main/notebooks/video_predictor_example.ipynb','SAM 2公式ノートブックの複数対象の追跡結果')+'。保存済み出力を無加工で引用。'))
    b+=sec('optical-flow','オプティカルフロー（RAFT）',
        '<span id="raft"></span>'+
        p('RAFT（ECCV 2020）は、2枚の画像の間で各画素がどこへ動いたかを推定します。下はKITTIテストセットでの入力画像と推定結果です。')+
        '<div class="spatial-raft-pair">'+
        img('raft-input.png','RAFTへの入力画像。道路上を車が走る場面。','元画像')+
        img('raft-output.png','同じ場面のRAFTによるオプティカルフロー。','RAFTの結果')+'</div>'+
        p('出典：Teed &amp; Deng, '+ref(RAFT,'RAFT, Figure 4（PDF p.10）')+'の左下の例。前方の車と背景の動きが、異なる色で表されています。')+
        p('色は画素の動きの方向と大きさを表します。同じ色でも「同じ人物」という意味ではありません。人物だけでなく背景にも色が付くのは、カメラの動きでも画面上の位置が変わるためです。'))
    b+=sec('slam','SLAM（ORB-SLAM3）',
        '<span id="orb-slam3"></span>'+
        p('移動中のカメラ映像から、「自分がどこにいるか」と「周りに何がどこにあるか」を同時に推定します。')+
        p('<strong>入力：</strong>TUM VIの「outdoors1」で撮影した連続画像と、加速度・角速度。下は同じ走行中の2時点の右カメラ画像です。')+
        '<div class="spatial-raft-pair">'+
        img('orb-outdoors1-5-display.png','outdoors1の右カメラ画像。建物の横の歩道。','走行中の画像①')+
        img('orb-outdoors1-4-display.png','同じoutdoors1の約51秒後の右カメラ画像。建物と木々の間の歩道。','約51秒後の画像②')+'</div>'+
        p('出典：'+ref('https://vision.in.tum.de/tumvi/exported/euroc/512_16/','TUM VI：dataset-outdoors1_512_16')+'。')+
        p('<strong>出力：</strong>同じ「outdoors1」を処理して推定した移動軌跡。赤はこの走行だけで推定、青は以前の走行で作った地図も使って推定した結果です。')+
        '<figure class="spatial-slam-output"><svg viewBox="0 0 870 724" role="img" aria-labelledby="slam-output-title" style="display:block;width:100%;overflow:hidden"><title id="slam-output-title">outdoors1の推定軌跡。座標軸を除き横向きに表示。赤は単独、青は以前の地図を利用。</title><image href="assets/orb-slam3-figure6.png" width="852" height="934" transform="translate(0 724) rotate(-90) translate(-90 -18)"/></svg><figcaption>赤・青とも推定結果。青はmagistrale2の地図を利用。座標軸を除き90度回転して表示。出典：'+ref(ORB,'Figure 6')+'。</figcaption></figure>')
    b+=sec('space','3Dの再構成・新しい視点の生成',
        p('写真に写った部屋の中を移動したり、物体を別の角度から眺めたりしたい。複数の写真などから立体的な場面を復元し、撮影していない位置からの見え方を作る分野です。建物の記録、商品の立体表示、VRなどにつながります。')+
        p('3Dの場面を表す方法の一つが、位置と色を持つ点の集まりです。'))
    b+=sec('pointcloud','点群',
        p('下の部屋は、壁や床、椅子を色付きの点で表しています。各点は3D空間での位置を持つので、視点を変えて立体として眺められます。深度センサなどの計測結果にも使われる表現です。')+
        img('pointcloud-room.png','室内の椅子や壁を色付きの点で表した点群。','出典：'+ref('https://www.open3d.org/docs/release/tutorial/geometry/pointcloud.html','Open3D：点群のダウンサンプリング例')+'。公開画像を引用。'))
    b+=sec('gaussian-splatting','3D Gaussian Splatting',
        p('複数の写真から、視点を動かしても写真のように見える場面を作ります。点群の点に広がりと透明度を持たせたような、小さな色の粒の集まりを学習します。')+
        '<figure><video controls playsinline preload="metadata"><source src="assets/3dgs-bicycle.mp4" type="video/mp4"></video><figcaption>'+ref('https://repo-sam.inria.fr/fungraph/3d-gaussian-splatting/','3D Gaussian Splatting：bicycle')+'。公開結果。</figcaption></figure>'+
        p('動画は、復元した場面の中で視点を動かした結果です。自転車と奥の建物の位置関係が変わり、平面の写真を拡大するだけでは作れない見え方になります。'))
    b+=sec('novel-view','NeRF',
        '<span id="coordinate-field"></span>'+
        p('場面の見え方をNNに覚えさせる方法もあります。いろいろな角度の写真から学習し、撮影していない視点の画像を描くのがNeRFです。')+
        img('spatial-nerf-simple.svg','複数の角度の写真からNNが場面を学習し、撮影していない視点の画像を描く。','NeRF：場面をNNで表し、新しい視点から描く。教材用の模式図。')+
        p('学習するのは、その場面専用のNNです。入力に3Dの位置と見る方向を与えると、その場所の色や密度を返します。密度は、そこにどれくらい物があるかの手がかりです。')+
        p('新しい画像を作るときは、カメラから見える方向に沿ってNNへ何度も問い合わせ、返ってきた色と密度を重ね合わせます。こうして、写真に写っていた形や模様を別の角度から描きます。')+
        '<figure><video controls playsinline preload="none" poster="assets/nerf-result-poster.jpg"><source src="assets/nerf-result.mp4" type="video/mp4"></video><figcaption>'+ref('https://www.matthewtancik.com/nerf','NeRF：colorspout')+'。撮影していない視点の生成結果。</figcaption></figure>'+
        p('NNが予測するのは分類ラベルではなく、3D空間の各場所の見え方です。カメラの位置を変えて問い合わせることで、同じ物体を回り込むような映像を作れます。'))
    b+=generation_body()
    b+=refs([('Teed & Deng — RAFT: Recurrent All-Pairs Field Transforms for Optical Flow',RAFT),('RAFT 著者実装','https://github.com/princeton-vl/RAFT'),('Campos et al. — ORB-SLAM3: An Accurate Open-Source Library for Visual, Visual-Inertial and Multi-Map SLAM',ORB),('ORB-SLAM3 著者実装・動画','https://github.com/UZ-SLAMLab/ORB_SLAM3'),('NeRF 著者ページ','https://www.matthewtancik.com/nerf'),('3D Gaussian Splatting 著者ページ','https://repo-sam.inria.fr/fungraph/3d-gaussian-splatting/'),('SAM 2 著者実装','https://github.com/facebookresearch/sam2')])
    return b+'<script src="assets/spatial.js" defer></script>'
