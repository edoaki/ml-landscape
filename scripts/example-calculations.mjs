/** Arithmetic underlying the stored teaching figures, independent of old generators. */
export const FEATURES = [
  [1, 0],
  [0, 2],
  [2, 1],
  [1, 1],
];
export function gatValues(
  features = FEATURES,
  w = [
    [1, -1],
    [1, 1],
  ],
  a = [-1, 0, 1, 0.5],
) {
  const z = features.map((h) =>
    w.map((row) => row.reduce((s, v, j) => s + v * h[j], 0)),
  );
  const raw = z.map((u) =>
    [...z[0], ...u].reduce((s, v, j) => s + v * a[j], 0),
  );
  const scores = raw.map((s) => Math.max(s, 0.2 * s)),
    exps = scores.map(Math.exp),
    sum = exps.reduce((a, b) => a + b, 0),
    alpha = exps.map((v) => v / sum);
  const parts = z.map((u, i) => u.map((v) => v * alpha[i])),
    out = [0, 1].map((j) => parts.reduce((s, u) => s + u[j], 0));
  return { z, raw, scores, exps, alpha, parts, out };
}
export const SIGMA = 0.35,
  MEANS = [
    [-2, -1],
    [2, 1],
  ];
export function velocity(x, t) {
  const variance = (1 - t) ** 2 + (SIGMA * t) ** 2;
  const logits = MEANS.map(
    (m) => -x.reduce((s, v, j) => s + (v - t * m[j]) ** 2, 0) / (2 * variance),
  );
  const weights = logits.map((z) => Math.exp(z - Math.max(...logits))),
    sum = weights.reduce((a, b) => a + b, 0);
  const rate = (t * SIGMA ** 2 - (1 - t)) / variance;
  return [0, 1].map((j) =>
    MEANS.reduce(
      (s, m, k) => s + (weights[k] / sum) * (m[j] + rate * (x[j] - t * m[j])),
      0,
    ),
  );
}
export function rk4(x, t, h) {
  const k1 = velocity(x, t),
    k2 = velocity(
      x.map((v, j) => v + (h * k1[j]) / 2),
      t + h / 2,
    ),
    k3 = velocity(
      x.map((v, j) => v + (h * k2[j]) / 2),
      t + h / 2,
    ),
    k4 = velocity(
      x.map((v, j) => v + h * k3[j]),
      t + h,
    );
  return x.map((v, j) => v + (h * (k1[j] + 2 * k2[j] + 2 * k3[j] + k4[j])) / 6);
}
