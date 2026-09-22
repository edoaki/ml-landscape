"""Network diagrams showing what changes in each efficiency method."""
from common import figure, svg, txt, line, BLUE, GREEN, ORANGE


def network(x, y, layers, color):
    points = [[(x + i * 38, y + (j - (n - 1) / 2) * 23) for j in range(n)] for i, n in enumerate(layers)]
    drawing = ''
    for left, right in zip(points, points[1:]):
        for a in left:
            for b in right:
                drawing += line(*a, *b, color, arrow=False, width=.8)
    for layer in points:
        for cx, cy in layer:
            drawing += f'<circle cx="{cx}" cy="{cy}" r="6" fill="white" stroke="{color}" stroke-width="2"/>'
    return drawing


def distillation():
    b = txt(24, 28, '学習時：同じ画像から出した確率を比べる', 19, anchor='start')
    b += '<image href="assets/pet-cat.jpg" x="25" y="142" width="90" height="85" preserveAspectRatio="xMidYMid slice"/>'
    b += txt(70, 250, '猫の画像', 15)
    b += line(122, 180, 153, 180, arrow=False) + line(153, 180, 153, 105, arrow=False) + line(153, 180, 153, 305, arrow=False)
    b += line(153, 105, 192, 105) + line(153, 305, 192, 305)
    b += network(205, 105, [3, 5, 5, 3], BLUE) + txt(260, 48, '大きな教師：固定', 16, BLUE)
    b += network(205, 305, [3, 2, 3], ORANGE) + txt(260, 252, '小さな生徒：更新', 16, ORANGE)
    b += line(330, 105, 393, 105) + line(292, 305, 393, 305)
    for y, values, color in [(74, [80, 15, 5], BLUE), (274, [60, 30, 10], ORANGE)]:
        for i, (name, val) in enumerate(zip(['猫', '犬', '車'], values)):
            yy = y + i * 31
            b += txt(419, yy + 14, name, 15)
            b += f'<rect x="443" y="{yy}" width="{val * 2}" height="19" fill="{color}"/>'
            b += txt(615, yy + 15, f'{val}%', 14, color, anchor='start')
    b += line(535, 174, 535, 246, ORANGE, dash=True, arrow=False)
    b += txt(650, 200, '確率の差を損失にする', 15) + txt(650, 225, '生徒だけを更新', 15, ORANGE)
    b += line(25, 374, 775, 374, arrow=False)
    b += txt(24, 410, '利用時', 18, anchor='start') + txt(170, 452, '新しい画像', 16)
    b += line(230, 446, 317, 446) + network(332, 446, [3, 2, 3], ORANGE)
    b += txt(370, 500, '学習済みの生徒だけ', 15, ORANGE) + line(419, 446, 527, 446) + txt(621, 452, '予測：猫', 18)
    return figure(svg(b, 525, label='蒸留：同じ画像を教師と生徒に入力し、出力確率の差で生徒を学習する'), '棒は予測確率（架空の例）。通常は正解ラベルも使って生徒を学習する。')


def quantization():
    b = txt(400, 30, 'モデルの形はそのまま、内部で扱う数値を粗くする', 20)
    for y, color, label, values in [
        (135, BLUE, '細かい数値で計算', ['0.3746', '0.6128']),
        (355, ORANGE, '途中の数値を丸めて計算', ['0.37', '0.61']),
    ]:
        b += txt(24, y - 64, label, 18, color, anchor='start')
        b += txt(65, y + 5, '入力', 17) + line(100, y, 190, y)
        b += network(208, y, [3, 4, 4, 3], color)
        b += line(334, y, 671, y) + txt(715, y + 5, '予測', 17)
        b += txt(488, y - 38, '途中で受け渡す数値の例', 16, color)
        b += txt(488, y - 9, values[0] + ' / ' + values[1], 21, color)
    b += line(437, 164, 437, 246, ORANGE)
    b += txt(553, 205, '細かい桁を丸める', 17, ORANGE)
    b += txt(400, 424, '各部分の重みも、少ないビットの数値で保存できる', 17)
    return figure(svg(b, 449, label='同じ形のネットワークで、内部の数値を丸めて計算する量子化の模式図'), '丸めを小数で示した概念図。実際の8 bit形式とは異なる。重みだけを量子化する方法もある。')


def lora():
    b = txt(400, 30, '用途に合わせて、どこを学習し直す？', 20)
    b += txt(195, 76, 'モデル全体を調整', 20, ORANGE)
    b += txt(595, 76, 'LoRA：追加部品を調整', 20, GREEN)
    b += line(400, 90, 400, 423, arrow=False)
    for offset, color in [(0, ORANGE), (400, BLUE)]:
        b += txt(offset + 43, 204, '入力', 16) + line(offset + 70, 198, offset + 121, 198)
        b += network(offset + 135, 198, [3, 5, 5, 3], color)
        b += line(offset + 260, 198, offset + 315, 198) + txt(offset + 351, 204, '出力', 16)
    b += txt(195, 121, '多くの重みを更新する', 16, ORANGE)
    b += txt(595, 121, '学習済みの重みは固定', 16, BLUE)
    for x in [573, 611]:
        b += line(x - 18, 220, x - 18, 304, GREEN, arrow=False)
        b += line(x - 18, 304, x - 9, 304, GREEN)
        b += f'<rect x="{x-7}" y="291" width="21" height="26" rx="3" fill="{GREEN}"/>'
        b += line(x + 15, 304, x + 25, 304, GREEN, arrow=False)
        b += line(x + 25, 304, x + 25, 226, GREEN)
    b += txt(598, 349, '小さな追加部品だけを学習', 17, GREEN)
    b += txt(195, 385, '更新する量が多い', 18, ORANGE)
    b += txt(595, 385, '更新する量が少ない', 18, GREEN)
    b += txt(400, 450, '元のモデルの働きに、追加部品の補正を足す', 19)
    return figure(svg(b, 478, label='全体の重みを更新する学習と、元の重みを固定して小さな追加部品を学習するLoRAの比較'), '青は固定、緑は学習する追加部品。元のモデルの計算に、小さな補正を足す。')
