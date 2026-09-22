"""Optional, reproducible attribution experiment; not run by the HTML build.

Requires torch, torchvision, numpy, Pillow, matplotlib and scikit-image.
Uses the existing Grad-CAM photograph and torchvision's ImageNet ResNet-18.
The initial run downloads the public pretrained weights.
"""
from pathlib import Path
import json
import numpy as np
from PIL import Image
import torch
from torchvision.models import resnet18, ResNet18_Weights
from torchvision.transforms import functional as TF
from skimage.segmentation import slic, mark_boundaries
from matplotlib import colormaps

ROOT = Path(__file__).resolve().parents[1]
OUT = ROOT / 'assets'


def run():
    torch.manual_seed(42)
    torch.set_num_threads(4)
    device = torch.device('mps' if torch.backends.mps.is_available() else 'cpu')
    weights = ResNet18_Weights.IMAGENET1K_V1
    model = resnet18(weights=weights, progress=False).eval().to(device)
    for parameter in model.parameters():
        parameter.requires_grad_(False)
    pil = TF.center_crop(TF.resize(Image.open(OUT / 'gradcam-original.png').convert('RGB'), 256), 224)
    rgb = np.asarray(pil).astype(np.float32) / 255
    x = TF.to_tensor(pil).unsqueeze(0).to(device)
    mean = torch.tensor([.485, .456, .406], device=device)[None, :, None, None]
    std = torch.tensor([.229, .224, .225], device=device)[None, :, None, None]
    target = 281  # ImageNet tabby cat; fixed for all four methods.

    def predict(z):
        return model((z - mean) / std)[:, target]

    def save(name, a):
        Image.fromarray(np.uint8(np.clip(a, 0, 1) * 255)).save(OUT / ('xai-' + name + '.png'))

    save('input', rgb)
    xx = x.detach().requires_grad_(True)
    score = predict(xx)
    gradient = torch.autograd.grad(score.sum(), xx)[0]
    saliency = gradient[0].abs().amax(0).cpu().numpy()
    saliency = np.clip(saliency / np.percentile(saliency, 99), 0, 1)
    save('saliency', colormaps['magma'](saliency)[..., :3])
    print('Saliency ready', flush=True)

    # Composite trapezoid rule along the straight path from a black RGB image.
    baseline = torch.zeros_like(x)
    steps = 256
    total = torch.zeros_like(x)
    for start in range(0, steps + 1, 16):
        indices = torch.arange(start, min(start + 16, steps + 1), device=device)
        alpha = (indices / steps)[:, None, None, None]
        points = (baseline + alpha * (x - baseline)).detach().requires_grad_(True)
        grad = torch.autograd.grad(predict(points).sum(), points)[0]
        w = torch.ones(len(indices), device=device)
        w[(indices == 0) | (indices == steps)] = .5
        total += (grad * w[:, None, None, None]).sum(0, keepdim=True)
    ig = ((x - baseline) * total / steps)[0].cpu().numpy()
    ig_map = ig.sum(0)
    limit = float(np.percentile(np.abs(ig_map), 99))
    save('ig', colormaps['RdBu_r'](np.clip(ig_map / limit, -1, 1) / 2 + .5)[..., :3])
    with torch.no_grad():
        delta = float((predict(x) - predict(baseline)).item())
    print('IG ready', float(ig.sum()), 'expected', delta, flush=True)

    # Grad-CAM at the final residual block (7x7), using the same raw class logit.
    captured = []
    handle = model.layer4.register_forward_hook(lambda _m, _i, o: captured.append(o))
    xx = x.detach().requires_grad_(True)
    value = predict(xx)
    activations = captured[0]
    grads = torch.autograd.grad(value.sum(), activations)[0]
    cam = (activations * grads.mean((2, 3), keepdim=True)).sum(1, keepdim=True).relu()
    cam = torch.nn.functional.interpolate(cam, size=(224, 224), mode='bilinear', align_corners=False)
    cam = cam[0, 0].detach().cpu().numpy()
    cam /= max(float(cam.max()), 1e-12)
    save('gradcam', .55 * rgb + .45 * colormaps['inferno'](cam)[..., :3])
    handle.remove()

    # LIME-style local surrogate: SLIC groups, random binary masks, cosine
    # locality kernel, and weighted ridge regression with an unpenalized intercept.
    segments = slic(rgb, n_segments=50, compactness=10, sigma=1, start_label=0)
    n = int(segments.max()) + 1
    rng = np.random.default_rng(42)
    masks = (rng.random((1024, n)) < .85).astype(np.float64)
    masks[0] = 1
    labels = torch.from_numpy(segments.astype(np.int64)).to(device)
    scores = []
    with torch.no_grad():
        for start in range(0, len(masks), 16):
            keep = torch.tensor(masks[start:start + 16], device=device, dtype=torch.float32)[:, labels]
            samples = x * keep[:, None]  # hidden superpixels become black RGB
            scores.extend(predict(samples).cpu().numpy().tolist())
    scores = np.asarray(scores)
    distance = 1 - np.sqrt(masks.mean(1))
    w = np.sqrt(np.exp(-(distance ** 2) / .1 ** 2))
    design = np.column_stack([np.ones(len(masks)), masks])
    penalty = np.eye(n + 1)
    penalty[0, 0] = 0
    coef = np.linalg.solve(design.T @ (w[:, None] * design) + penalty, design.T @ (w * scores))
    fitted = design @ coef
    r2 = 1 - np.sum(w * (scores - fitted) ** 2) / np.sum(w * (scores - np.average(scores, weights=w)) ** 2)
    region_values = coef[1:][segments]
    scale = max(float(np.abs(coef[1:]).max()), 1e-12)
    colors = colormaps['RdBu_r'](region_values / scale / 2 + .5)[..., :3]
    save('lime', mark_boundaries(.35 * rgb + .65 * colors, segments, color=(.18, .23, .20)))
    save('segments', mark_boundaries(rgb, segments, color=(1, .85, .2)))
    metadata = dict(model='torchvision ResNet-18', weights='IMAGENET1K_V1',
                    torch=torch.__version__, device=str(device), target_index=target,
                    target_label=weights.meta['categories'][target], target_logit=float(score.item()),
                    preprocessing='Resize short side to 256 (bilinear), center crop 224, ImageNet normalization',
                    ig_steps=steps, ig_baseline='black RGB', ig_sum=float(ig.sum()),
                    ig_score_difference=delta, ig_absolute_error=abs(float(ig.sum()) - delta),
                    gradcam_layer='layer4 (7x7)', lime_segments=n, lime_samples=len(masks),
                    lime_seed=42, lime_keep_probability=.85, lime_kernel_width=.1, lime_ridge_alpha=1,
                    lime_hidden_color='black RGB', lime_weighted_r2=float(r2),
                    lime_surrogate_at_input=float(fitted[0]),
                    map_normalization='Saliency and signed IG: 99th percentile clipping; LIME: max absolute coefficient; Grad-CAM: max')
    (OUT / 'xai-results.json').write_text(json.dumps(metadata, ensure_ascii=False, indent=2) + '\n')
    np.savez_compressed(OUT / 'xai-attributions.npz', ig=ig, saliency=gradient[0].detach().cpu().numpy(),
                        gradcam=cam, segments=segments, lime_coefficients=coef)
    print(json.dumps(metadata, indent=2), flush=True)


if __name__ == '__main__':
    run()
