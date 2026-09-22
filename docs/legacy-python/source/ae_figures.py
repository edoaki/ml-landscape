"""Original AE/VAE network diagrams with a local MNIST example."""
import base64
import math
from common import ROOT, BLUE, GREEN, ORANGE, PURPLE, figure, svg, txt, line


def digit(x, label):
    data = base64.b64encode((ROOT/'assets/mnist-train-00000-label-5.png').read_bytes()).decode()
    return (txt(x+38, 109, label, 15)
            + f'<image href="data:image/png;base64,{data}" x="{x}" y="145" width="76" height="76" style="image-rendering:pixelated"/>'
            + txt(x+38, 247, '28 × 28 画素', 12))


def nodes(x, ys, color):
    return ''.join(f'<circle cx="{x}" cy="{y}" r="13" fill="{color}" stroke="white" stroke-width="2"/>' for y in ys)


def connect(x, ys, xx, yys):
    return ''.join(line(x+13, y, xx-13, yy, '#a8b6bc', arrow=False, width=1.2) for y in ys for yy in yys)


def architecture(variational=False):
    wide = [113, 159, 205, 251]
    narrow = [139, 182, 225]
    b = digit(14, '入力：MNIST') + digit(710, '出力：再構成')
    b += txt(232, 35, 'エンコーダ', 21, ORANGE) + txt(574, 35, 'デコーダ', 21, BLUE)
    b += txt(232, 62, '画像を小さな表現にする', 13) + txt(574, 62, '表現から画像を復元する', 13)
    b += line(94, 182, 139, 182) + line(665, 182, 704, 182)
    b += connect(154, wide, 252, narrow) + connect(552, narrow, 650, wide)
    if not variational:
        b += connect(252, narrow, 402, [157, 207]) + connect(402, [157, 207], 552, narrow)
        b += nodes(402, [157, 207], GREEN)
        b += txt(402, 108, '潜在表現 z', 18, GREEN)
        b += txt(402, 263, '少数の数値に圧縮', 14, GREEN)
        b += txt(402, 291, '一つの入力 → 一つの点', 14, GREEN)
    else:
        b += line(269, 182, 306, 182)
        b += txt(402, 99, '潜在変数の分布', 18, PURPLE)
        b += txt(402, 123, '平均 μ と広がり σ', 14, PURPLE)
        points = [(320+i, 222-70*math.exp(-0.5*((i-80)/27)**2)) for i in range(161)]
        curve = ' '.join(f'{x:.1f},{y:.1f}' for x,y in points)
        b += f'<polygon points="320,222 {curve} 480,222" fill="{PURPLE}" fill-opacity=".16"/>'
        b += f'<polyline points="{curve}" fill="none" stroke="{PURPLE}" stroke-width="3"/>'
        b += line(314, 222, 489, 222, arrow=False)
        b += line(400, 222, 400, 151, PURPLE, dash=True, arrow=False, width=1)
        b += txt(400, 242, 'μ', 14, PURPLE)
        b += f'<circle cx="433" cy="222" r="5" fill="{GREEN}"/>'
        b += line(437, 215, 534, 184, GREEN)
        b += txt(490, 157, 'z を選ぶ', 13, GREEN)
        b += txt(402, 278, '分布から一つの値をサンプルする', 14, PURPLE)
        b += txt(402, 302, '同じ入力でも z が変わる', 14, PURPLE)
    b += nodes(154, wide, ORANGE) + nodes(252, narrow, ORANGE)
    b += nodes(552, narrow, BLUE) + nodes(650, wide, BLUE)
    b += f'<path d="M52 275 V337 H748 V275" fill="none" stroke="{ORANGE}" stroke-width="1.6" stroke-dasharray="5 4"/>'
    b += txt(400, 365, '入力と再構成を比べて、両方のネットワークを学習する', 16, ORANGE)
    caption = '丸はニューロン、線は学習する重み。実際のユニット数は省略。入力はMNIST訓練画像の5（index 0）。出力側も同じ画像を使って復元の目標を示しており、学習済みモデルの実行結果ではありません。'
    if variational:
        caption += '中央は潜在変数の1成分の正規分布を模式化。縦の高さは確率密度です。'
    return figure(svg(b, 390, label=('VAE：MNISTから潜在分布を推定して数字を再構成' if variational else 'AE：MNISTを少数の特徴量へ圧縮して数字を再構成')), caption)
