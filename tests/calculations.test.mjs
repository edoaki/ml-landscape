import test from "node:test";
import assert from "node:assert/strict";
import {
  FEATURES,
  gatValues,
  SIGMA,
  MEANS,
  velocity,
  rk4,
} from "../scripts/example-calculations.mjs";
const close = (a, b, tolerance = 1e-7) =>
  assert.ok(Math.abs(a - b) < tolerance, `${a} != ${b}`);
test("GAT matches hand-expanded example, neighbor permutations and second head", () => {
  const v = gatValues();
  assert.deepEqual(v.z, [
    [1, 1],
    [-2, 2],
    [1, 3],
    [0, 2],
  ]);
  assert.deepEqual(v.raw, [0.5, -2, 1.5, 0]);
  assert.deepEqual(v.scores, [0.5, -0.4, 1.5, 0]);
  close(
    v.alpha.reduce((a, b) => a + b),
    1,
  );
  assert.ok(v.alpha[1] > 0);
  const d = Math.exp(0.5) + Math.exp(-0.4) + Math.exp(1.5) + 1;
  close(v.out[0], (Math.exp(0.5) - 2 * Math.exp(-0.4) + Math.exp(1.5)) / d);
  close(
    v.out[1],
    (Math.exp(0.5) + 2 * Math.exp(-0.4) + 3 * Math.exp(1.5) + 2) / d,
  );
  gatValues([0, 3, 1, 2].map((i) => FEATURES[i])).out.forEach((x, j) =>
    close(x, v.out[j]),
  );
  const second = gatValues(
    FEATURES,
    [
      [1, 0],
      [0, 1],
    ],
    [0, 1, -1, 0.5],
  );
  assert.deepEqual(second.raw, [-1, 1, -1.5, -0.5]);
  assert.notDeepEqual(second.alpha, v.alpha);
  assert.equal([...v.out, ...second.out].length, 4);
});
function density(x, t) {
  const variance = (1 - t) ** 2 + (SIGMA * t) ** 2;
  return (
    MEANS.reduce(
      (s, m) =>
        s +
        Math.exp(
          -x.reduce((v, a, j) => v + (a - t * m[j]) ** 2, 0) / (2 * variance),
        ) /
          (2 * Math.PI * variance),
      0,
    ) / 2
  );
}
test("Flow Matching velocity satisfies the continuity equation", () => {
  const eps = 1e-5;
  for (const t of [0.1, 0.5, 0.9])
    for (const x of [
      [0, 0],
      [0.4, 0.2],
      [-1.5, 0.6],
      [2, 1],
    ]) {
      const dt = (density(x, t + eps) - density(x, t - eps)) / (2 * eps);
      let divergence = 0;
      for (let j = 0; j < 2; j++) {
        const a = [...x],
          b = [...x];
        a[j] += eps;
        b[j] -= eps;
        divergence +=
          (density(a, t) * velocity(a, t)[j] -
            density(b, t) * velocity(b, t)[j]) /
          (2 * eps);
      }
      close(dt + divergence, 0);
    }
});
// Integrate the normal density with Simpson's rule, avoiding a runtime math package.
function normal(z) {
  const sign = Math.sign(z),
    a = Math.abs(z),
    n = 2000,
    h = a / n;
  let sum = 1 + Math.exp((-a * a) / 2);
  for (let i = 1; i < n; i++)
    sum += (i % 2 ? 4 : 2) * Math.exp(-((i * h) ** 2) / 2);
  return 0.5 + (sign * h * sum) / (3 * Math.sqrt(2 * Math.PI));
}
test("Flow Matching RK4 endpoints preserve mixture quantiles", () => {
  for (const start of [
    [0.6, -0.4],
    [-1, 0.4],
    [1, 2],
    [-2, -1],
    [0.01, 0.02],
  ]) {
    let x = [...start];
    for (let i = 0; i < 400; i++) x = rk4(x, i / 400, 1 / 400);
    const projection = (p) => (2 * p[0] + p[1]) / Math.sqrt(5),
      cdf =
        [-Math.sqrt(5), Math.sqrt(5)].reduce(
          (s, m) => s + normal((projection(x) - m) / SIGMA),
          0,
        ) / 2;
    close(normal(projection(start)), cdf, 1e-6);
    close(-x[0] + 2 * x[1], SIGMA * (-start[0] + 2 * start[1]), 1e-6);
  }
});
