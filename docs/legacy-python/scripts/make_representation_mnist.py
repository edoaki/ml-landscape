"""Reproduce the MNIST figure. Run separately from build.py.
Requires numpy, scikit-learn, Pillow. Downloads CVDF MNIST to a temp cache.
"""
from pathlib import Path
import base64, gzip, hashlib, io, json, tempfile, urllib.request
import numpy as np
from PIL import Image
from sklearn.neural_network import MLPClassifier
from sklearn.manifold import TSNE
import sklearn

ROOT = Path(__file__).resolve().parents[1]
OUT = ROOT / 'content/questions/representation-learning/media'
CACHE = Path(tempfile.gettempdir()) / 'ml-landscape-mnist'
CACHE.mkdir(exist_ok=True); OUT.mkdir(exist_ok=True)
hashes = {}
def data(name):
    path = CACHE / name
    if not path.exists():
        urllib.request.urlretrieve('https://storage.googleapis.com/cvdf-datasets/mnist/' + name, path)
    hashes[name] = hashlib.sha256(path.read_bytes()).hexdigest()
    raw = gzip.decompress(path.read_bytes())
    if 'images' in name:
        return np.frombuffer(raw, dtype=np.uint8, offset=16).reshape(-1, 784)
    return np.frombuffer(raw, dtype=np.uint8, offset=8)
train = data('train-images-idx3-ubyte.gz'); labels = data('train-labels-idx1-ubyte.gz')
test = data('t10k-images-idx3-ubyte.gz'); targets = data('t10k-labels-idx1-ubyte.gz')
rng = np.random.RandomState(42)
train_ids = rng.choice(len(train), 15000, replace=False)
show_ids = np.concatenate([rng.choice(np.flatnonzero(targets == i), 150, replace=False) for i in range(10)])
x = train[train_ids].astype(np.float32) / 255
y = labels[train_ids]
v = test[show_ids].astype(np.float32) / 255
class RecordedMLP(MLPClassifier):
    def _initialize(self, *args, **kwargs):
        super()._initialize(*args, **kwargs)
        self.initial_weights_ = self.coefs_[0].copy()
        self.initial_bias_ = self.intercepts_[0].copy()

model = RecordedMLP(hidden_layer_sizes=(64,), random_state=42, batch_size=256, learning_rate_init=.001)
for epoch in range(20):
    model.partial_fit(x, y, classes=np.arange(10))
    print(f'epoch {epoch+1}: loss {model.loss_:.4f}', flush=True)
initial = np.maximum(0, v @ model.initial_weights_ + model.initial_bias_)
learned = np.maximum(0, v @ model.coefs_[0] + model.intercepts_[0])
coords = []
for h in [initial, learned]:
    coords.append(TSNE(n_components=2, perplexity=30, init='pca', learning_rate='auto', random_state=42).fit_transform(h))
score = float(model.score(test.astype(np.float32)/255, targets))
colors = ['#27688f','#cb6325','#389078','#b1416a','#7660a8','#927127','#247d83','#585ba2','#a64c3e','#5c7c32']
def text(x,y,t,size=17,fill='#243b30',anchor='start'):
    return f'<text x="{x}" y="{y}" font-size="{size}" fill="{fill}" text-anchor="{anchor}">{t}</text>'
def png(a):
    buf=io.BytesIO(); Image.fromarray(a.reshape(28,28)).save(buf,format='PNG')
    return 'data:image/png;base64,'+base64.b64encode(buf.getvalue()).decode()
svg=['<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 960 590" role="img" aria-label="MNISTの未学習と学習後の中間表現を同じ1500枚で比較"><rect width="960" height="590" fill="#fcfcf8"/><g font-family="system-ui, sans-serif">']
svg += [text(30,32,'1点 ＝ 手書き数字1枚 ／ 色 ＝ 正解の数字',20)]
for digit in range(10):
    idx=show_ids[np.flatnonzero(targets[show_ids]==digit)[0]]
    xx=35+digit*92
    svg += [f'<image href="{png(test[idx])}" x="{xx}" y="50" width="40" height="40"/>',text(xx+51,77,str(digit),20,colors[digit])]
for j,(xy,title,subtitle) in enumerate(zip(coords,['未学習の中間表現','数字の分類を学習した後'],['異なる数字が重なる領域がある','同じ数字がまとまり、区別しやすくなる'])):
    left=28+j*478
    svg += [text(left,132,title,22),text(left,157,subtitle,15),f'<rect x="{left}" y="175" width="448" height="365" rx="10" fill="#fff" stroke="#dfe5da"/>']
    scaled=(xy-xy.min(0))/(xy.max(0)-xy.min(0))
    for idx in rng.permutation(len(xy)):
        px,py=scaled[idx]; color=colors[int(targets[show_ids[idx]])]
        svg.append(f'<circle cx="{left+18+px*412:.2f}" cy="{193+py*329:.2f}" r="2.4" fill="{color}" opacity=".7"/>')
svg += [text(30,570,'64個の数をt-SNEで2次元に圧縮。左右の軸・向きは共通ではありません。',16),'</g></svg>']
(OUT/'mnist-representations.svg').write_text(''.join(svg))
# Reuse a real digit for the objective and translation diagrams.
idx=int(show_ids[np.flatnonzero(targets[show_ids]==5)[0]])
Image.fromarray(test[idx].reshape(28,28)).save(OUT/'mnist-five.png')
metadata={'dataset':'MNIST, CVDF mirror','seed':42,'train_count':15000,'epochs':20,'architecture':[784,64,10],'test_accuracy':score,'visualization_count':1500,'visualization_per_class':150,'projection':'Independent t-SNE on 64-dimensional ReLU hidden activations; perplexity=30, init=pca, learning_rate=auto, random_state=42','labels_used_for_projection':False,'sklearn_version':sklearn.__version__,'numpy_version':np.__version__,'source_sha256':hashes,'five_test_index':idx,'train_indices':train_ids.tolist(),'test_indices':show_ids.tolist(),'labels':targets[show_ids].tolist(),'before':coords[0].round(5).tolist(),'after':coords[1].round(5).tolist()}
(OUT/'mnist-experiment.json').write_text(json.dumps(metadata,ensure_ascii=False))
print(json.dumps({k:v for k,v in metadata.items() if k not in ['train_indices','test_indices','labels','before','after']},ensure_ascii=False,indent=2))
