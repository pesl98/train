'use strict';
/* AI & ML Lab — six experiments on one framework (the maths lives in nn.js).
   Supervised: linear regression by gradient descent · one neuron (logistic regression) · neural-network classifier ·
               function fitting.  Optimisation: optimiser race.  Unsupervised: k-means.
   Each experiment supplies: params, init, step (one training step), draw, hud, sample (for graphs), plots, scen, theory. */
const $ = s => document.querySelector(s);
const T = String.raw, TAU = 2 * Math.PI;
const COL = { cy: '#22d3ee', vi: '#a78bfa', am: '#fbbf24', gr: '#4ade80', pk: '#f472b6', bl: '#60a5fa', rd: '#f87171', mu: '#8a93b8' };
const C1 = [34, 211, 238], C0 = [244, 114, 182];            // class 1 = cyan, class 0 = pink
const cv = $('#view'), cx = cv.getContext('2d'), pl = $('#plots'), px = pl.getContext('2d');

/* ---------------- helpers ---------------- */
function fitCanvas(c, ctx) {
  const r = c.getBoundingClientRect(), d = devicePixelRatio || 1;
  if (c.width !== Math.round(r.width * d) || c.height !== Math.round(r.height * d)) { c.width = Math.round(r.width * d); c.height = Math.round(r.height * d); }
  ctx.setTransform(d, 0, 0, d, 0, 0); return [r.width, r.height];
}
function bg(c, W, H) { const g = c.createRadialGradient(W / 2, H / 2, 20, W / 2, H / 2, Math.max(W, H) * .75); g.addColorStop(0, '#12183a'); g.addColorStop(1, '#080b17'); c.fillStyle = g; c.fillRect(0, 0, W, H); }
const fm = (v, d = 3) => (!isFinite(v) ? '—' : (Math.abs(v) < 1e-12 ? 0 : v).toFixed(d));
const hudRows = rows => rows.map(r => `${r[0]} <b>${r[1]}</b>`).join('<br>');
/* a square panel showing the data plane [lo, hi]² */
function panel(x0, y0, size, lo = -1.3, hi = 1.3) {
  const s = size / (hi - lo);
  return { x0, y0, size, lo, hi, X: x => x0 + (x - lo) * s, Y: y => y0 + size - (y - lo) * s, inv: (px, py) => [lo + (px - x0) / s, lo + (y0 + size - py) / s] };
}
function frame(c, V) { c.strokeStyle = 'rgba(255,255,255,.12)'; c.lineWidth = 1; c.strokeRect(V.x0 + .5, V.y0 + .5, V.size - 1, V.size - 1); }
function axesIn(c, V) {
  c.strokeStyle = 'rgba(255,255,255,.08)'; c.beginPath();
  for (let v = Math.ceil(V.lo * 2) / 2; v <= V.hi; v += 0.5) { c.moveTo(V.X(v), V.y0); c.lineTo(V.X(v), V.y0 + V.size); c.moveTo(V.x0, V.Y(v)); c.lineTo(V.x0 + V.size, V.Y(v)); }
  c.stroke(); c.strokeStyle = 'rgba(255,255,255,.22)'; c.beginPath(); c.moveTo(V.X(0), V.y0); c.lineTo(V.X(0), V.y0 + V.size); c.moveTo(V.x0, V.Y(0)); c.lineTo(V.x0 + V.size, V.Y(0)); c.stroke();
}
/* probability field: fn(x, y) -> p in [0,1]; drawn at low resolution into a cached canvas */
const heatCv = document.createElement('canvas'), heatCx = heatCv.getContext('2d');
function heatMap(c, V, fn, res = 64) {
  heatCv.width = heatCv.height = res; const img = heatCx.createImageData(res, res);
  for (let j = 0; j < res; j++) for (let i = 0; i < res; i++) {
    const x = V.lo + (i + .5) / res * (V.hi - V.lo), y = V.hi - (j + .5) / res * (V.hi - V.lo), p = fn(x, y), k = 4 * (j * res + i);
    const conf = Math.min(1, Math.abs(p - .5) * 2), base = p >= .5 ? C1 : C0, a = .10 + .55 * conf;
    img.data[k] = base[0] * a + 14 * (1 - a); img.data[k + 1] = base[1] * a + 20 * (1 - a); img.data[k + 2] = base[2] * a + 46 * (1 - a); img.data[k + 3] = 255;
    const edge = Math.max(0, 1 - Math.abs(p - .5) / .05) * .85;           // a soft white line where p = 0.5
    if (edge > 0) for (let q = 0; q < 3; q++) img.data[k + q] = img.data[k + q] * (1 - edge) + 240 * edge;
  }
  heatCx.putImageData(img, 0, 0);
  c.imageSmoothingEnabled = true; c.drawImage(heatCv, V.x0, V.y0, V.size, V.size);
}
function dots(c, V, X, Y, hollow) {
  for (let k = 0; k < X.length; k++) {
    const x = V.X(X[k][0]), y = V.Y(X[k][1]); if (x < V.x0 || x > V.x0 + V.size || y < V.y0 || y > V.y0 + V.size) continue;
    const col = Y[k] ? '#22d3ee' : '#f472b6';
    c.beginPath(); c.arc(x, y, 3.6, 0, TAU);
    if (hollow) { c.strokeStyle = col; c.lineWidth = 1.6; c.stroke(); } else { c.fillStyle = col; c.fill(); c.strokeStyle = 'rgba(8,11,23,.9)'; c.lineWidth = 1; c.stroke(); }
  }
}
function label(c, x, y, s, col = '#8a93b8', align = 'left') { c.fillStyle = col; c.font = '12px system-ui'; c.textAlign = align; c.fillText(s, x, y); }
/* network diagram: nodes in columns, edges coloured by sign, thickness by |weight| */
function drawNet(c, net, box, names) {
  const L = net.sizes.length, colX = l => box.x + 18 + l * (box.w - 36) / (L - 1);
  const nodeY = (l, j) => { const n = net.sizes[l], gap = Math.min(34, (box.h - 30) / Math.max(1, n)); return box.y + box.h / 2 + (j - (n - 1) / 2) * gap; };
  let wmax = 1e-9; net.W.forEach(W => W.forEach(w => wmax = Math.max(wmax, Math.abs(w))));
  for (let l = 0; l < L - 1; l++) {
    const nin = net.sizes[l], nout = net.sizes[l + 1];
    for (let j = 0; j < nout; j++) for (let i = 0; i < nin; i++) {
      const w = net.W[l][j * nin + i], t = Math.abs(w) / wmax;
      c.strokeStyle = w >= 0 ? `rgba(34,211,238,${.15 + .75 * t})` : `rgba(244,114,182,${.15 + .75 * t})`; c.lineWidth = .4 + 3.6 * t;
      c.beginPath(); c.moveTo(colX(l), nodeY(l, i)); c.lineTo(colX(l + 1), nodeY(l + 1, j)); c.stroke();
    }
  }
  for (let l = 0; l < L; l++) for (let j = 0; j < net.sizes[l]; j++) {
    c.beginPath(); c.arc(colX(l), nodeY(l, j), 7, 0, TAU); c.fillStyle = l === 0 ? '#2c3566' : l === L - 1 ? '#4f46e5' : '#1e2a55'; c.fill(); c.strokeStyle = '#a5b4fc'; c.lineWidth = 1.2; c.stroke();
    if (l === 0 && names) label(c, colX(0) - 12, nodeY(0, j) + 4, names[j], '#aab2d8', 'right');
  }
  label(c, colX(0), box.y + box.h - 4, 'inputs', '#6b7599', 'center'); label(c, colX(L - 1), box.y + box.h - 4, 'output', '#6b7599', 'center');
  if (L > 2) label(c, (colX(1) + colX(L - 2)) / 2, box.y + box.h - 4, L - 2 + ' hidden layer' + (L > 3 ? 's' : ''), '#6b7599', 'center');
  label(c, box.x + 8, box.y + 12, 'weights: cyan > 0, pink < 0, thickness = size', '#6b7599', 'left');
}
const featNames = mode => (mode === 'quad' ? ['x', 'y', 'x²', 'y²', 'xy'] : ['x', 'y']);

const EXPS = {};

/* =====================================================================
   1. LINEAR REGRESSION BY GRADIENT DESCENT
   ===================================================================== */
EXPS.linreg = {
  name: 'Linear regression (gradient descent)', group: 'Supervised learning', rate: 25,
  about: 'Fit a straight line ŷ = w·x + b to noisy points by walking downhill on the loss surface. Right: the loss for every (w, b); the white path is gradient descent, the star the exact best line.',
  params: [
    { id: 'slope', l: 'True slope', min: -2, max: 2, step: .1, def: 1.2, re: 1 }, { id: 'icept', l: 'True intercept', min: -1, max: 1, step: .1, def: .3, re: 1 },
    { id: 'noise', l: 'Noise', min: 0, max: .6, step: .01, def: .15, re: 1 }, { id: 'n', l: 'Points', min: 5, max: 200, step: 1, def: 40, re: 1 },
    { id: 'lr', l: 'Learning rate', min: .005, max: 2.5, step: .005, def: .1 }, { id: 'batch', l: 'Batch', opts: ['all', '8', '1'], def: 'all' },
    { id: 'seed', l: 'Data seed', min: 1, max: 50, step: 1, def: 1, re: 1 },
  ],
  init(P) {
    const r = rng(P.seed), X = [], Y = [];
    for (let i = 0; i < P.n; i++) { const x = 2 * r() - 1; X.push(x); Y.push(P.slope * x + P.icept + P.noise * r.gauss()); }
    const n = X.length, mx = X.reduce((a, b) => a + b, 0) / n, my = Y.reduce((a, b) => a + b, 0) / n;
    const sxx = X.reduce((s, x) => s + (x - mx) ** 2, 0), ws = sxx ? X.reduce((s, x, i) => s + (x - mx) * (Y[i] - my), 0) / sxx : 0;
    return { X, Y, w: -1.5, b: 1.2, it: 0, path: [[-1.5, 1.2]], ws, bs: my - ws * mx, r: rng(P.seed + 7), grid: null, diverged: false };
  },
  loss(S, w, b) { let s = 0; for (let i = 0; i < S.X.length; i++) { const e = w * S.X[i] + b - S.Y[i]; s += e * e; } return s / S.X.length / 2; },
  step(S, P) {
    if (S.diverged) return;
    const n = S.X.length, m = P.batch === 'all' ? n : Math.min(n, +P.batch); let gw = 0, gb = 0;
    for (let k = 0; k < m; k++) { const i = m === n ? k : Math.floor(S.r() * n), e = S.w * S.X[i] + S.b - S.Y[i]; gw += e * S.X[i]; gb += e; }
    S.w -= P.lr * gw / m; S.b -= P.lr * gb / m; S.it++;
    if (!isFinite(S.w) || Math.abs(S.w) + Math.abs(S.b) > 1e3) { S.diverged = true; return; }
    if (S.it % 1 === 0) { S.path.push([S.w, S.b]); if (S.path.length > 3000) S.path.splice(1, 1); }
  },
  draw(c, S, P, W, H) {
    bg(c, W, H); const size = Math.min(H - 30, (W - 50) / 2), V = panel(16, 16, size, -1.2, 1.2), V2 = { x0: 32 + size, y0: 16, size };
    axesIn(c, V); frame(c, V);
    dots(c, V, S.X.map((x, i) => [x, S.Y[i]]), S.X.map(() => 1));
    const line = (w, b, col, dash) => { c.save(); c.beginPath(); c.rect(V.x0, V.y0, V.size, V.size); c.clip(); c.setLineDash(dash || []); c.strokeStyle = col; c.lineWidth = 2.4; c.beginPath(); c.moveTo(V.X(-1.2), V.Y(w * -1.2 + b)); c.lineTo(V.X(1.2), V.Y(w * 1.2 + b)); c.stroke(); c.restore(); };
    line(S.ws, S.bs, 'rgba(167,139,250,.9)', [6, 5]);
    if (isFinite(S.w)) line(S.w, S.b, '#fbbf24');
    label(c, V.x0 + 6, V.y0 + V.size - 8, 'data, current line (amber), best line (dashed)');
    // loss surface over (w, b)
    const wr = [-3, 3], br = [-2.5, 2.5], res = 80;
    if (!S.grid) {
      const g = document.createElement('canvas'); g.width = g.height = res; const gx = g.getContext('2d'), img = gx.createImageData(res, res);
      let lo = Infinity, hi = -Infinity; const vals = [];
      for (let j = 0; j < res; j++) for (let i = 0; i < res; i++) { const v = Math.log(this.loss(S, wr[0] + (i + .5) / res * (wr[1] - wr[0]), br[1] - (j + .5) / res * (br[1] - br[0])) + 1e-3); vals.push(v); lo = Math.min(lo, v); hi = Math.max(hi, v); }
      vals.forEach((v, k) => { const t = (v - lo) / (hi - lo), band = Math.floor(t * 14) % 2 ? .9 : 1; img.data[4 * k] = (30 + 140 * t) * band; img.data[4 * k + 1] = (40 + 60 * (1 - t)) * band; img.data[4 * k + 2] = (120 + 100 * (1 - t)) * band; img.data[4 * k + 3] = 255; });
      gx.putImageData(img, 0, 0); S.grid = g;
    }
    c.imageSmoothingEnabled = true; c.drawImage(S.grid, V2.x0, V2.y0, size, size);
    const WX = w => V2.x0 + (w - wr[0]) / (wr[1] - wr[0]) * size, BY = b => V2.y0 + (br[1] - b) / (br[1] - br[0]) * size;
    c.save(); c.beginPath(); c.rect(V2.x0, V2.y0, size, size); c.clip();
    c.strokeStyle = '#fff'; c.lineWidth = 1.6; c.beginPath(); S.path.forEach((p, k) => k ? c.lineTo(WX(p[0]), BY(p[1])) : c.moveTo(WX(p[0]), BY(p[1]))); c.stroke();
    c.fillStyle = '#fbbf24'; c.beginPath(); c.arc(WX(S.w), BY(S.b), 5, 0, TAU); c.fill();
    c.fillStyle = '#a78bfa'; c.font = '18px system-ui'; c.textAlign = 'center'; c.fillText('★', WX(S.ws), BY(S.bs) + 6); c.restore();
    c.strokeStyle = 'rgba(255,255,255,.15)'; c.strokeRect(V2.x0 + .5, V2.y0 + .5, size - 1, size - 1);
    label(c, V2.x0 + size / 2, V2.y0 + size + 14, 'slope w →   (loss surface, bands = equal loss)', '#8a93b8', 'center');
    c.save(); c.translate(V2.x0 - 6, V2.y0 + size / 2); c.rotate(-Math.PI / 2); label(c, 0, 0, 'intercept b →', '#8a93b8', 'center'); c.restore();
  },
  hud(S, P) { return hudRows([['step', S.it], ['loss', S.diverged ? 'diverged' : fm(this.loss(S, S.w, S.b), 5)], ['w', fm(S.w)], ['b', fm(S.b)], ['best w*', fm(S.ws)], ['best b*', fm(S.bs)]]); },
  sample(S) { return { loss: this.loss(S, S.w, S.b), w: S.w, b: S.b, ws: S.ws, bs: S.bs }; },
  plots: [{ title: 'Loss (log scale)', log: true, series: [{ k: 'loss', col: COL.am, label: 'loss' }] },
    { title: 'Parameters', series: [{ k: 'w', col: COL.cy, label: 'w' }, { k: 'ws', col: COL.cy, label: 'w*', dash: 1 }, { k: 'b', col: COL.pk, label: 'b' }, { k: 'bs', col: COL.pk, label: 'b*', dash: 1 }] }],
  scen: {
    'Good learning rate (0.1)': { lr: .1 }, 'Too small: very slow (0.01)': { lr: .01 }, 'Large but stable (1.5)': { lr: 1.5 },
    'Too large: it diverges (2.3)': { lr: 2.3 }, 'Stochastic: one point per step': { lr: .1, batch: '1' }, 'Very noisy data': { noise: .5 }, 'Only 5 points': { n: 5 },
  },
  theory(P, S) {
    return {
      title: 'Linear regression by gradient descent', intro: 'The simplest learning machine: two numbers, w and b, adjusted to make the line fit the data. Everything that follows in this lab is this idea scaled up.',
      sections: [
        { h: 'Model and loss', p: 'For each data point the model predicts ŷ = w x + b. The loss measures how wrong it is on average (half the mean squared error):', tex: [T`\hat y_i = w\,x_i + b \qquad L(w,b)=\frac{1}{2n}\sum_{i=1}^{n}\left(\hat y_i-y_i\right)^2`] },
        { h: 'The gradient (chain rule)', p: 'How the loss changes when w or b is nudged. Each term is the error times "how much the prediction depends on that parameter".', tex: [T`\frac{\partial L}{\partial w}=\frac1n\sum_i(\hat y_i-y_i)\,x_i \qquad \frac{\partial L}{\partial b}=\frac1n\sum_i(\hat y_i-y_i)`] },
        { h: 'Gradient descent', p: 'Step downhill: against the gradient, scaled by the learning rate η. Repeat.', tex: [T`w \leftarrow w-\eta\,\frac{\partial L}{\partial w}\qquad b \leftarrow b-\eta\,\frac{\partial L}{\partial b}`], live: `η = ${P.lr}` },
        { h: 'Why too large a learning rate explodes', p: 'The loss is a bowl (a quadratic). Along its steepest direction its curvature is λ. One step multiplies the distance to the bottom by (1 − ηλ): it shrinks only if |1 − ηλ| < 1, i.e. η < 2/λ. For x spread over [−1, 1] the curvature along b is 1, so beyond η ≈ 2 every step overshoots further.', tex: [T`e_{k+1}=(1-\eta\lambda)\,e_k \quad\Rightarrow\quad \text{converges} \iff 0<\eta<\frac{2}{\lambda}`],
          svg: Theory.plot({ f: w => this.loss(S, w, S.bs), xr: [-3, 3], xl: 'slope w (b fixed at its best value)', yl: 'loss', title: 'a cut through the bowl', point: [S.w, this.loss(S, S.w, S.bs), 'now'], vlines: [{ x: S.ws, col: COL.vi, label: 'w*' }] }) },
        { h: 'The exact answer (for checking)', p: 'For a straight line the bottom of the bowl can be found with algebra — set both derivatives to zero (least squares). Gradient descent matters because for a neural network no such formula exists.', tex: [T`w^*=\frac{\sum(x_i-\bar x)(y_i-\bar y)}{\sum (x_i-\bar x)^2}\qquad b^*=\bar y-w^*\bar x`], live: `here: w* = ${fm(S.ws)}, b* = ${fm(S.bs)}` },
      ],
    };
  },
};

/* =====================================================================
   2. ONE NEURON (LOGISTIC REGRESSION)
   ===================================================================== */
EXPS.logreg = {
  name: 'One neuron (logistic regression)', group: 'Supervised learning', rate: 30,
  about: 'A single artificial neuron: a weighted sum of the inputs, squashed by the sigmoid into a probability. Its decision boundary (white) is always a straight line in the space of its inputs — unless you give it extra features.',
  params: [
    { id: 'data', l: 'Data set', opts: ['blobs', 'circle', 'xor', 'moons'], def: 'blobs', re: 1 }, { id: 'feat', l: 'Inputs', opts: ['x, y', 'x, y, x², y², xy'], def: 'x, y', re: 1 },
    { id: 'noise', l: 'Noise', min: 0, max: .3, step: .01, def: .05, re: 1 }, { id: 'n', l: 'Points', min: 20, max: 400, step: 10, def: 200, re: 1 },
    { id: 'lr', l: 'Learning rate', min: .005, max: 1, step: .005, def: .2 }, { id: 'seed', l: 'Seed', min: 1, max: 50, step: 1, def: 1, re: 1 },
  ],
  mode: P => (P.feat === 'x, y' ? 'xy' : 'quad'),
  init(P) {
    const D = makeData(P.data, P.n, P.noise, P.seed), mode = this.mode(P);
    const net = new Net([mode === 'quad' ? 5 : 2, 1], { seed: P.seed });
    return { D, F: expandFeatures(D.X, mode), mode, net, it: 0 };
  },
  step(S, P) { S.net.trainBatch(S.F, S.D.Y, { lr: P.lr, opt: 'sgd' }); S.it++; },
  draw(c, S, P, W, H) {
    bg(c, W, H); const size = Math.min(H - 30, W - 300), V = panel(16, 16, size);
    if (!S.heat || S.heatIt !== S.it) { S.heatIt = S.it; S.heat = 1; }
    heatMap(c, V, (x, y) => S.net.predict(S.mode === 'quad' ? [x, y, x * x, y * y, x * y] : [x, y]), 90);
    axesIn(c, V); dots(c, V, S.D.X, S.D.Y); frame(c, V);
    const nf = S.net.sizes[0], w = S.net.W[0], b = S.net.b[0][0], names = featNames(S.mode);
    drawNet(c, S.net, { x: V.x0 + size + 30, y: 30, w: Math.max(140, W - size - 70), h: Math.min(260, H - 60) }, names);
    let eq = 'z = '; for (let i = 0; i < nf; i++) eq += (i ? (w[i] < 0 ? ' − ' : ' + ') : (w[i] < 0 ? '−' : '')) + Math.abs(w[i]).toFixed(2) + names[i];
    eq += (b < 0 ? ' − ' : ' + ') + Math.abs(b).toFixed(2);
    label(c, V.x0 + size + 30, Math.min(300, H - 30), eq, '#e8ebff'); label(c, V.x0 + size + 30, Math.min(320, H - 12), 'p(cyan) = σ(z) = 1 / (1 + e^(−z))', '#8a93b8');
  },
  hud(S) { return hudRows([['step', S.it], ['loss', fm(S.net.lossOf(S.F, S.D.Y), 4)], ['accuracy', fm(100 * S.net.accuracy(S.F, S.D.Y), 1) + ' %']]); },
  sample(S) { return { loss: S.net.lossOf(S.F, S.D.Y), acc: 100 * S.net.accuracy(S.F, S.D.Y) }; },
  plots: [{ title: 'Cross-entropy loss', series: [{ k: 'loss', col: COL.am, label: 'loss' }] }, { title: 'Accuracy (%)', series: [{ k: 'acc', col: COL.gr, label: 'accuracy' }] }],
  scen: {
    'Separable blobs: a line is enough': { data: 'blobs' }, 'Circle: a line cannot do it': { data: 'circle', feat: 'x, y' },
    'Circle with x² and y² as extra inputs': { data: 'circle', feat: 'x, y, x², y², xy' }, 'XOR: no single line exists': { data: 'xor', feat: 'x, y' },
    'XOR solved by the feature xy': { data: 'xor', feat: 'x, y, x², y², xy' }, 'Moons': { data: 'moons' },
  },
  theory(P, S) {
    const sg = z => 1 / (1 + Math.exp(-z));
    return {
      title: 'One neuron: logistic regression', intro: 'The building block of every neural network, trained exactly like the line of the first experiment — only the loss is different.',
      sections: [
        { h: 'The neuron', p: 'A weighted sum z of the inputs, then the sigmoid σ turns z into a probability between 0 and 1. p > 0.5 means "cyan".', tex: [T`z=w_1x_1+w_2x_2+\dots+b=\mathbf w\cdot\mathbf x+b\qquad p=\sigma(z)=\frac{1}{1+e^{-z}}`],
          svg: Theory.plot({ f: sg, xr: [-6, 6], yr: [-.05, 1.05], xl: 'z', yl: 'σ(z)', hlines: [{ y: .5, label: '0.5' }], title: 'the sigmoid' }) },
        { h: 'Cross-entropy loss', p: 'Squared error is a poor judge of probabilities. Cross-entropy punishes confident mistakes very hard: predicting p = 0.01 for a point that is really cyan costs −ln 0.01 ≈ 4.6.', tex: [T`L=-\frac1n\sum_i\Big[y_i\ln p_i+(1-y_i)\ln(1-p_i)\Big]`] },
        { h: 'The gradient is remarkably simple', p: 'Because σ′(z) = σ(z)(1 − σ(z)), the chain rule cancels neatly — the same "error × input" form as linear regression:', tex: [T`\frac{\partial L}{\partial w_j}=\frac1n\sum_i(p_i-y_i)\,x_{ij}\qquad\frac{\partial L}{\partial b}=\frac1n\sum_i(p_i-y_i)`] },
        { h: 'The decision boundary is a straight line', p: 'p = 0.5 exactly where z = 0, i.e. where w·x + b = 0: a straight line in the space of the inputs. No line separates the circle or XOR. Two cures: give the neuron better inputs (x², y², xy — the boundary becomes a curve in the x, y plane), or let the network invent its own features: hidden layers, the next experiment.', tex: [T`w_1x+w_2y+b=0`] },
      ],
    };
  },
};

/* =====================================================================
   3. NEURAL NETWORK CLASSIFIER
   ===================================================================== */
EXPS.mlp = {
  name: 'Neural network classifier', group: 'Neural networks', rate: 40,
  about: 'A multi-layer network learns its own features. Filled dots are training data, rings are test data the network never trains on. Watch the gap between training and test loss: that is overfitting.',
  params: [
    { id: 'data', l: 'Data set', opts: ['circle', 'xor', 'moons', 'spiral', 'blobs'], def: 'circle', re: 1 }, { id: 'noise', l: 'Noise', min: 0, max: .3, step: .01, def: .05, re: 1 },
    { id: 'n', l: 'Points', min: 40, max: 600, step: 10, def: 300, re: 1 }, { id: 'test', l: 'Test share', min: 0, max: 60, step: 5, def: 30, u: '%', re: 1 },
    { id: 'layers', l: 'Hidden layers', min: 1, max: 3, step: 1, def: 1, re: 1 }, { id: 'width', l: 'Neurons/layer', min: 1, max: 10, step: 1, def: 5, re: 1 },
    { id: 'act', l: 'Activation', opts: ['tanh', 'relu', 'sigmoid'], def: 'tanh', re: 1 }, { id: 'opt', l: 'Optimiser', opts: ['adam', 'sgd', 'momentum'], def: 'adam' },
    { id: 'lr', l: 'Learning rate', min: .001, max: .5, step: .001, def: .03 }, { id: 'l2', l: 'L2 regularisation', min: 0, max: .02, step: .0005, def: 0 },
    { id: 'seed', l: 'Seed', min: 1, max: 50, step: 1, def: 1, re: 1 },
  ],
  init(P) {
    const D = makeData(P.data, P.n, P.noise, P.seed), sp = splitData(D, P.test / 100, P.seed);
    const sizes = [2, ...Array(P.layers).fill(P.width), 1];
    return { D, tr: sp.train, te: sp.test, net: new Net(sizes, { act: P.act, seed: P.seed + 100 }), it: 0, heatT: 0 };
  },
  step(S, P) { S.net.trainBatch(S.tr.X, S.tr.Y, { lr: P.lr, l2: P.l2, opt: P.opt }); S.it++; },
  draw(c, S, P, W, H) {
    bg(c, W, H); const size = Math.min(H - 30, W * .58), V = panel(16, 16, size);
    heatMap(c, V, (x, y) => S.net.predict([x, y]), 90);
    axesIn(c, V); dots(c, V, S.tr.X, S.tr.Y); dots(c, V, S.te.X, S.te.Y, true); frame(c, V);
    if (W - size > 200) drawNet(c, S.net, { x: V.x0 + size + 34, y: 24, w: W - size - 80, h: H - 50 }, ['x', 'y']);
  },
  hud(S) {
    const n = S.net;
    return hudRows([['epoch', S.it], ['train loss', fm(n.lossOf(S.tr.X, S.tr.Y), 4)], ['test loss', S.te.X.length ? fm(n.lossOf(S.te.X, S.te.Y), 4) : '—'],
      ['train acc', fm(100 * n.accuracy(S.tr.X, S.tr.Y), 1) + ' %'], ['test acc', S.te.X.length ? fm(100 * n.accuracy(S.te.X, S.te.Y), 1) + ' %' : '—'], ['parameters', n.nParams]]);
  },
  sample(S) { const n = S.net; return { ltr: n.lossOf(S.tr.X, S.tr.Y), lte: n.lossOf(S.te.X, S.te.Y), atr: 100 * n.accuracy(S.tr.X, S.tr.Y), ate: 100 * n.accuracy(S.te.X, S.te.Y) }; },
  plots: [{ title: 'Loss (log scale)', log: true, series: [{ k: 'ltr', col: COL.am, label: 'train' }, { k: 'lte', col: COL.pk, label: 'test' }] },
    { title: 'Accuracy (%)', series: [{ k: 'atr', col: COL.gr, label: 'train' }, { k: 'ate', col: COL.vi, label: 'test' }] }],
  scen: {
    'Circle: one hidden layer': { data: 'circle', layers: 1, width: 4 }, 'XOR with 2 hidden neurons': { data: 'xor', layers: 1, width: 2, seed: 3 },
    'Spiral: too small a network': { data: 'spiral', layers: 1, width: 3 }, 'Spiral: deeper and wider (give it ~10 s)': { data: 'spiral', layers: 3, width: 8, lr: .03 },
    'ReLU network': { data: 'moons', act: 'relu', layers: 2, width: 6 }, 'Overfitting: few noisy points, big net': { data: 'moons', noise: .25, n: 60, test: 50, layers: 3, width: 10, l2: 0, lr: .02 },
    'Regularisation tames it': { data: 'moons', noise: .25, n: 60, test: 50, layers: 3, width: 10, l2: .01, lr: .02 }, 'Plain SGD: much slower than Adam': { data: 'spiral', layers: 3, width: 8, opt: 'sgd', lr: .03 },
  },
  theory(P, S) {
    const A = { tanh: Math.tanh, relu: z => Math.max(0, z), sigmoid: z => 1 / (1 + Math.exp(-z)) };
    return {
      title: 'Neural networks and back-propagation', intro: 'Layers of neurons. Each hidden neuron computes a feature; the next layer combines features into more complex ones. All weights are learned with gradient descent, the gradient coming from back-propagation.',
      sections: [
        { h: 'Forward pass', p: 'Layer by layer: multiply by a weight matrix, add a bias vector, apply the activation function f element by element.', tex: [T`\mathbf a^{(0)}=\mathbf x,\qquad \mathbf z^{(l)}=W^{(l)}\mathbf a^{(l-1)}+\mathbf b^{(l)},\qquad \mathbf a^{(l)}=f\big(\mathbf z^{(l)}\big)`, T`p=\sigma\big(z^{(\text{out})}\big)`] },
        { h: 'Why the activation must be non-linear', p: 'Without f, two layers collapse into one: W₂(W₁x + b₁) + b₂ is again a single matrix times x plus a vector — still only a straight boundary. The bend in f is what lets depth create curves.',
          svg: Theory.plot({ series: [{ f: A.tanh, col: COL.cy, label: 'tanh', at: .9 }, { f: A.relu, col: COL.am, label: 'ReLU', at: .78 }, { f: A.sigmoid, col: COL.vi, label: 'sigmoid', at: .62 }], xr: [-3, 3], yr: [-1.2, 2.2], xl: 'z', yl: 'f(z)', title: 'activation functions' }) },
        { h: 'Back-propagation = the chain rule, organised', p: 'Start with the error at the output and pass it backwards. δ is "how much the loss changes if this neuron’s input z changes". The weight gradient is δ times the activation feeding that weight.', tex: [T`\delta^{(\text{out})}=p-y`, T`\delta^{(l)}=\Big(W^{(l+1)\,\top}\delta^{(l+1)}\Big)\odot f'\big(\mathbf z^{(l)}\big)`, T`\frac{\partial L}{\partial W^{(l)}}=\delta^{(l)}\,\mathbf a^{(l-1)\,\top}\qquad\frac{\partial L}{\partial \mathbf b^{(l)}}=\delta^{(l)}`], live: `this network: ${S.net.sizes.join(' → ')} neurons, ${S.net.nParams} learned numbers` },
        { h: 'Training, test data and overfitting', p: 'The network only ever sees the training points. The test points measure how well it generalises. A network with many parameters and few noisy points can memorise them: training loss keeps falling while test loss rises. L2 regularisation adds λ/2·Σw² to the loss, which pulls weights towards zero and smooths the boundary.', tex: [T`L_{\text{total}}=L+\frac{\lambda}{2}\sum w^2\qquad\Rightarrow\qquad \frac{\partial L_{\text{total}}}{\partial w}=\frac{\partial L}{\partial w}+\lambda w`] },
      ],
    };
  },
};

/* =====================================================================
   4. FUNCTION FITTING (1-D REGRESSION WITH ONE HIDDEN LAYER)
   ===================================================================== */
const TARGETS = { sine: x => .8 * Math.sin(3 * x), step: x => (x > 0 ? .6 : -.6), 'abs': x => 1.3 * Math.abs(x) - .6, bump: x => 1.1 * Math.exp(-(((x - .1) / .25) ** 2)) - .3, cubic: x => 1.6 * x ** 3 - .9 * x };
EXPS.fit = {
  name: 'Function fitting (universal approximation)', group: 'Neural networks', rate: 60,
  about: 'One hidden layer learns a curve from sample points. The faint violet curves are the contributions of the individual hidden neurons; the network output (amber) is simply their sum plus a bias.',
  params: [
    { id: 'target', l: 'Target', opts: Object.keys(TARGETS), def: 'sine', re: 1 }, { id: 'n', l: 'Points', min: 4, max: 100, step: 1, def: 30, re: 1 },
    { id: 'noise', l: 'Noise', min: 0, max: .4, step: .01, def: .05, re: 1 }, { id: 'hidden', l: 'Hidden neurons', min: 1, max: 40, step: 1, def: 6, re: 1 },
    { id: 'act', l: 'Activation', opts: ['tanh', 'relu'], def: 'tanh', re: 1 }, { id: 'lr', l: 'Learning rate', min: .001, max: .1, step: .001, def: .02 },
    { id: 'l2', l: 'L2 regularisation', min: 0, max: .01, step: .0002, def: 0 }, { id: 'units', l: 'Show neurons', opts: ['on', 'off'], def: 'on' },
    { id: 'seed', l: 'Seed', min: 1, max: 50, step: 1, def: 1, re: 1 },
  ],
  init(P) {
    const r = rng(P.seed), f = TARGETS[P.target], X = [], Y = [];
    for (let i = 0; i < P.n; i++) { const x = -1 + 2 * (i + .5) / P.n + .6 / P.n * (r() - .5); X.push([x]); Y.push(f(x) + P.noise * r.gauss()); }
    const GX = [], GY = []; for (let i = 0; i <= 200; i++) { const x = -1 + 2 * i / 200; GX.push([x]); GY.push(f(x)); }
    return { X, Y, GX, GY, f, net: new Net([1, P.hidden, 1], { act: P.act, out: 'linear', loss: 'mse', seed: P.seed + 50 }), it: 0 };
  },
  step(S, P) { S.net.trainBatch(S.X, S.Y, { lr: P.lr, l2: P.l2, opt: 'adam' }); S.it++; },
  draw(c, S, P, W, H) {
    bg(c, W, H); const L = 50, R = 20, Tp = 16, B = 30, pw = W - L - R, ph = H - Tp - B;
    const X = x => L + (x + 1.1) / 2.2 * pw, Y = y => Tp + ph - (y + 1.4) / 2.8 * ph;
    c.strokeStyle = 'rgba(255,255,255,.08)'; c.beginPath(); for (let v = -1; v <= 1; v += .5) { c.moveTo(X(v), Tp); c.lineTo(X(v), Tp + ph); } for (let v = -1; v <= 1; v += .5) { c.moveTo(L, Y(v)); c.lineTo(L + pw, Y(v)); } c.stroke();
    c.strokeStyle = 'rgba(255,255,255,.25)'; c.beginPath(); c.moveTo(X(0), Tp); c.lineTo(X(0), Tp + ph); c.moveTo(L, Y(0)); c.lineTo(L + pw, Y(0)); c.stroke();
    c.save(); c.beginPath(); c.rect(L, Tp, pw, ph); c.clip();
    const n = S.net, H1 = n.sizes[1], w1 = n.W[0], b1 = n.b[0], w2 = n.W[1], f = ACT[n.act].f;
    if (P.units === 'on') {
      c.lineWidth = 1.2;
      for (let j = 0; j < H1; j++) { c.strokeStyle = 'rgba(167,139,250,.45)'; c.beginPath(); for (let i = 0; i <= 160; i++) { const x = -1.1 + 2.2 * i / 160, y = w2[j] * f(w1[j] * x + b1[j]); i ? c.lineTo(X(x), Y(y)) : c.moveTo(X(x), Y(y)); } c.stroke(); }
    }
    c.setLineDash([5, 5]); c.strokeStyle = 'rgba(255,255,255,.5)'; c.lineWidth = 1.4; c.beginPath(); for (let i = 0; i <= 200; i++) { const x = -1.1 + 2.2 * i / 200; i ? c.lineTo(X(x), Y(S.f(x))) : c.moveTo(X(x), Y(S.f(x))); } c.stroke(); c.setLineDash([]);
    c.strokeStyle = '#fbbf24'; c.lineWidth = 3; c.beginPath(); for (let i = 0; i <= 220; i++) { const x = -1.1 + 2.2 * i / 220, y = n.predict([x]); i ? c.lineTo(X(x), Y(y)) : c.moveTo(X(x), Y(y)); } c.stroke();
    for (let k = 0; k < S.X.length; k++) { c.fillStyle = '#22d3ee'; c.beginPath(); c.arc(X(S.X[k][0]), Y(S.Y[k]), 4, 0, TAU); c.fill(); }
    c.restore();
    label(c, L + 8, Tp + ph - 8, 'dashed: true function   amber: network   dots: training data' + (P.units === 'on' ? '   violet: one neuron each' : ''));
    c.fillStyle = '#6b7599'; c.font = '11px system-ui'; c.textAlign = 'center'; for (let v = -1; v <= 1; v += .5) c.fillText(v, X(v), Tp + ph + 16);
  },
  hud(S) { return hudRows([['step', S.it], ['training error', fm(S.net.lossOf(S.X, S.Y), 5)], ['error vs truth', fm(S.net.lossOf(S.GX, S.GY), 5)], ['parameters', S.net.nParams]]); },
  sample(S) { return { ltr: S.net.lossOf(S.X, S.Y), ltrue: S.net.lossOf(S.GX, S.GY) }; },
  plots: [{ title: 'Error (log scale): on the data, and against the true function', log: true, series: [{ k: 'ltr', col: COL.am, label: 'on training points' }, { k: 'ltrue', col: COL.vi, label: 'vs true function' }] }],
  scen: {
    'Sine with 6 tanh neurons': { target: 'sine', hidden: 6, act: 'tanh' }, 'Too few neurons (2)': { target: 'sine', hidden: 2 },
    'ReLU: a curve from straight pieces': { target: 'sine', hidden: 8, act: 'relu' }, 'A step from smooth neurons': { target: 'step', hidden: 6 },
    'Overfitting: 10 noisy points, 30 neurons': { target: 'sine', n: 10, noise: .25, hidden: 30, lr: .02, l2: 0, seed: 2 }, 'Same, with regularisation': { target: 'sine', n: 10, noise: .25, hidden: 30, lr: .02, l2: .005, seed: 2 },
  },
  theory(P, S) {
    return {
      title: 'Universal approximation', intro: 'Why a network can learn (almost) any curve: it builds the curve out of many simple pieces.',
      sections: [
        { h: 'The model', p: 'One hidden layer with H neurons and a linear output: a weighted sum of shifted, stretched copies of one activation function.', tex: [T`\hat y(x)=b_2+\sum_{j=1}^{H}v_j\,f\!\left(w_jx+b_j\right)`], live: `${S.net.sizes[1]} neurons → ${S.net.nParams} numbers to learn` },
        { h: 'Building blocks', p: 'With tanh each neuron is a smooth step: w_j sets how sharp, −b_j/w_j where it sits, v_j how high. With ReLU each neuron is a hinge, so the whole network is piecewise linear. Enough steps or hinges can approximate any continuous function on an interval as closely as you like — the universal approximation theorem.',
          svg: Theory.plot({ series: [{ f: x => Math.tanh(4 * (x - .3)), col: COL.cy, label: 'tanh(4(x − 0.3))', at: .2 }, { f: x => Math.max(0, 2 * (x + .2)), col: COL.am, label: 'ReLU(2(x + 0.2))', at: .85 }], xr: [-1, 1], yr: [-1.2, 2], xl: 'x', title: 'one neuron = one step or one hinge' }) },
        { h: 'Fitting is not understanding', p: 'Training minimises the error on the points only. Between and beyond the points the network may do anything. With more neurons than the data justify it threads the noise (overfitting) — the purple "error vs truth" curve then rises while the training error keeps falling. Outside the data range (|x| > 1) no network can be trusted.', tex: [T`L_{\text{train}}=\frac{1}{2n}\sum_i(\hat y(x_i)-y_i)^2\qquad\text{vs}\qquad L_{\text{true}}=\frac{1}{2}\,\overline{(\hat y(x)-f(x))^2}`] },
      ],
    };
  },
};

/* =====================================================================
   5. OPTIMISER RACE
   ===================================================================== */
const SURF = {
  'stretched bowl': { box: [-2, 2, -2, 2], start: [-1.8, 1.4], f: (x, y) => .1 * x * x + 2 * y * y, g: (x, y) => [.2 * x, 4 * y], lr: .4, lra: .05 },
  'curved valley': { box: [-2, 2, -1, 3], start: [-1.5, 2.5], f: (x, y) => (1 - x) ** 2 + 5 * (y - x * x) ** 2, g: (x, y) => [-2 * (1 - x) - 20 * x * (y - x * x), 10 * (y - x * x)], lr: .015, lra: .03 },
  'saddle': { box: [-2, 2, -2.2, 2.2], start: [1.8, .01], f: (x, y) => x * x - y * y + .25 * y ** 4 + 1, g: (x, y) => [2 * x, -2 * y + y ** 3], lr: .05, lra: .03 },
  'two wells': {
    box: [-2.5, 2.5, -2.5, 2.5], start: [2.2, 2.2],
    f: (x, y) => 1.5 - Math.exp(-((x - 1) ** 2 + (y - 1) ** 2) / .4) - 1.4 * Math.exp(-((x + 1) ** 2 + (y + .8) ** 2) / .6) + .04 * (x * x + y * y),
    g: (x, y) => { const e1 = Math.exp(-((x - 1) ** 2 + (y - 1) ** 2) / .4), e2 = 1.4 * Math.exp(-((x + 1) ** 2 + (y + .8) ** 2) / .6); return [e1 * 2 * (x - 1) / .4 + e2 * 2 * (x + 1) / .6 + .08 * x, e1 * 2 * (y - 1) / .4 + e2 * 2 * (y + .8) / .6 + .08 * y]; }, lr: .1, lra: .05,
  },
};
const OPTS = [['sgd', 'Gradient descent', COL.cy], ['momentum', 'Momentum', COL.am], ['rmsprop', 'RMSProp', COL.gr], ['adam', 'Adam', COL.vi]];
EXPS.opt = {
  name: 'Optimiser race', group: 'Optimisation', rate: 20,
  about: 'Four ways to walk downhill, started from the same point on the same loss surface. Click on the map to choose a new starting point.',
  params: [
    { id: 'surf', l: 'Surface', opts: Object.keys(SURF), def: 'stretched bowl', re: 1 },
    { id: 'lr', l: 'η: descent, momentum', min: .001, max: .6, step: .001, def: .4 }, { id: 'lra', l: 'η: RMSProp, Adam', min: .001, max: .3, step: .001, def: .05 },
    { id: 'beta', l: 'Momentum β', min: 0, max: .99, step: .01, def: .9 },
  ],
  init(P, extra) {
    const s = SURF[P.surf], start = (extra && extra.start) || s.start.slice();
    return { s, start, it: 0, runs: OPTS.map(([k]) => ({ k, p: Float64Array.from(start), st: {}, path: [start.slice()], dead: false })), grid: null };
  },
  save(S) { return { start: S.start }; },
  step(S, P) {
    S.it++;
    for (const r of S.runs) {
      if (r.dead) continue;
      const g = S.s.g(r.p[0], r.p[1]); Optim[r.k](r.p, g, r.st, { lr: r.k === 'sgd' || r.k === 'momentum' ? P.lr : P.lra, beta: P.beta });
      if (!isFinite(r.p[0]) || Math.hypot(r.p[0], r.p[1]) > 50) { r.dead = true; continue; }
      r.path.push([r.p[0], r.p[1]]); if (r.path.length > 3000) r.path.splice(1, 1);
    }
  },
  view(S, W, H) { const [x0, x1, y0, y1] = S.s.box, sz = Math.min(H - 30, W - 260), sx = sz / (x1 - x0), sy = sz / (y1 - y0); return { L: 16, Tp: 16, sz, X: x => 16 + (x - x0) * sx, Y: y => 16 + sz - (y - y0) * sy, inv: (a, b) => [x0 + (a - 16) / sx, y0 + (16 + sz - b) / sy] }; },
  draw(c, S, P, W, H) {
    bg(c, W, H); const V = this.view(S, W, H), [x0, x1, y0, y1] = S.s.box, res = 90;
    if (!S.grid) {
      const g = document.createElement('canvas'); g.width = g.height = res; const gx = g.getContext('2d'), img = gx.createImageData(res, res), vals = [];
      let lo = Infinity, hi = -Infinity;
      for (let j = 0; j < res; j++) for (let i = 0; i < res; i++) { const v = S.s.f(x0 + (i + .5) / res * (x1 - x0), y1 - (j + .5) / res * (y1 - y0)); vals.push(v); lo = Math.min(lo, v); }
      const tv = vals.map(v => Math.log(v - lo + .02)); tv.forEach(v => hi = Math.max(hi, v)); const tl = Math.log(.02);
      tv.forEach((v, k) => { const t = (v - tl) / (hi - tl), band = Math.floor(t * 16) % 2 ? .88 : 1; img.data[4 * k] = (25 + 150 * t) * band; img.data[4 * k + 1] = (35 + 70 * (1 - t)) * band; img.data[4 * k + 2] = (110 + 110 * (1 - t)) * band; img.data[4 * k + 3] = 255; });
      gx.putImageData(img, 0, 0); S.grid = g;
    }
    c.imageSmoothingEnabled = true; c.drawImage(S.grid, V.L, V.Tp, V.sz, V.sz);
    c.save(); c.beginPath(); c.rect(V.L, V.Tp, V.sz, V.sz); c.clip();
    S.runs.forEach((r, i) => {
      c.strokeStyle = OPTS[i][2]; c.lineWidth = 2; c.beginPath(); r.path.forEach((p, k) => k ? c.lineTo(V.X(p[0]), V.Y(p[1])) : c.moveTo(V.X(p[0]), V.Y(p[1]))); c.stroke();
      const q = r.path[r.path.length - 1]; c.fillStyle = OPTS[i][2]; c.beginPath(); c.arc(V.X(q[0]), V.Y(q[1]), 5, 0, TAU); c.fill();
    });
    c.fillStyle = '#fff'; c.beginPath(); c.arc(V.X(S.start[0]), V.Y(S.start[1]), 4, 0, TAU); c.fill(); c.restore();
    c.strokeStyle = 'rgba(255,255,255,.15)'; c.strokeRect(V.L + .5, V.Tp + .5, V.sz - 1, V.sz - 1);
    let y = 40; OPTS.forEach(([k, name, col], i) => { const r = S.runs[i]; c.fillStyle = col; c.fillRect(V.L + V.sz + 24, y - 9, 12, 12); label(c, V.L + V.sz + 44, y, name + (r.dead ? '  (diverged)' : '  f = ' + fm(S.s.f(r.p[0], r.p[1]), 4)), '#e8ebff'); y += 24; });
    label(c, V.L + V.sz + 24, y + 10, 'Click the map to start elsewhere.', '#8a93b8');
  },
  pointer(type, mx, my, S, P) { if (type !== 'down') return; const V = this.view(S, cv.getBoundingClientRect().width, cv.getBoundingClientRect().height); if (mx < V.L || mx > V.L + V.sz || my < V.Tp || my > V.Tp + V.sz) return; startRun({ start: V.inv(mx, my) }); },
  hud(S) { return hudRows([['step', S.it]]); },
  sample(S) { const o = {}; S.runs.forEach(r => { o[r.k] = r.dead ? NaN : S.s.f(r.p[0], r.p[1]); }); return o; },
  plots: [{ title: 'Loss f(x, y) of each optimiser (log scale)', log: true, series: OPTS.map(([k, n, col]) => ({ k, col, label: n })) }],
  onParam(id, P) { if (id === 'surf') { P.lr = SURF[P.surf].lr; P.lra = SURF[P.surf].lra; return true; } return false; },
  scen: {
    'Stretched bowl: plain descent zig-zags': { surf: 'stretched bowl', lr: .45, lra: .05 }, 'Smaller step: no zig-zag, but slow': { surf: 'stretched bowl', lr: .1, lra: .05 },
    'Curved valley (Rosenbrock)': { surf: 'curved valley', lr: .015, lra: .03 }, 'Saddle point: who escapes?': { surf: 'saddle', lr: .05, lra: .03 },
    'Two wells: which minimum?': { surf: 'two wells', lr: .1, lra: .05 }, 'Learning rate too large': { surf: 'stretched bowl', lr: .55, lra: .3 },
  },
  theory(P, S) {
    return {
      title: 'Optimisers', intro: 'Training a network means finding a low point of a loss surface with millions of dimensions. Here the surface has only two, so you can see the paths. g is the gradient, η the learning rate.',
      sections: [
        { h: 'Gradient descent', p: 'Always step straight downhill. In a long narrow valley the steepest direction points across the valley, not along it: the path zig-zags.', tex: [T`\theta\leftarrow\theta-\eta\,g`] },
        { h: 'Momentum', p: 'A heavy ball: the velocity v is a running average of past gradients. Zig-zags cancel, steady downhill components add up, and the ball can roll through small bumps and off saddle points. (Written in the averaging form, so η means the same as for plain descent.)', tex: [T`v\leftarrow\beta v+(1-\beta)\,g\qquad\theta\leftarrow\theta-\eta v`], live: `β = ${P.beta}` },
        { h: 'RMSProp', p: 'Divide each coordinate’s step by a running average of its own gradient size: steep directions get smaller steps, flat ones larger. Every parameter gets its own effective learning rate.', tex: [T`s\leftarrow\beta_2 s+(1-\beta_2)\,g^2\qquad\theta\leftarrow\theta-\eta\,\frac{g}{\sqrt{s}+\epsilon}`] },
        { h: 'Two learning rates in this experiment', p: 'For gradient descent and momentum the step is η times the gradient, so η has the units of (parameter)²/(loss). RMSProp and Adam divide by the gradient’s own size, so their step is roughly η itself, in parameter units. The same number therefore means very different things — hence two sliders.' },
        { h: 'Adam', p: 'Momentum and RMSProp combined, with a correction for the first steps (when m and s are still near zero). The default choice for training neural networks.', tex: [T`m\leftarrow\beta_1m+(1-\beta_1)g\qquad s\leftarrow\beta_2s+(1-\beta_2)g^2`, T`\theta\leftarrow\theta-\eta\,\frac{m/(1-\beta_1^t)}{\sqrt{s/(1-\beta_2^t)}+\epsilon}`] },
        { h: 'No optimiser finds "the" minimum', p: 'On the two-wells surface each method ends in whichever valley its path leads to. Which minimum you reach depends on the start, the learning rate and the method — one reason why trained networks differ from run to run.' },
      ],
    };
  },
};

/* =====================================================================
   6. K-MEANS CLUSTERING
   ===================================================================== */
EXPS.kmeans = {
  name: 'k-means clustering', group: 'Unsupervised learning', rate: 1.5,
  about: 'No labels this time: the algorithm has to find groups by itself. Each step assigns every point to its nearest centre, then moves each centre to the middle of its points.',
  params: [
    { id: 'true', l: 'Real clusters', min: 1, max: 7, step: 1, def: 4, re: 1 }, { id: 'k', l: 'k (centres)', min: 1, max: 8, step: 1, def: 4, re: 1 },
    { id: 'spread', l: 'Spread', min: .04, max: .35, step: .01, def: .12, re: 1 }, { id: 'n', l: 'Points', min: 30, max: 500, step: 10, def: 240, re: 1 },
    { id: 'init', l: 'Start', opts: ['k-means++', 'random points'], def: 'k-means++', re: 1 }, { id: 'seed', l: 'Seed', min: 1, max: 50, step: 1, def: 1, re: 1 },
  ],
  pal: ['#22d3ee', '#f472b6', '#fbbf24', '#4ade80', '#a78bfa', '#60a5fa', '#f87171', '#e8ebff'],
  init(P) {
    const r = rng(P.seed), centres = [], pts = [];
    for (let k = 0; k < P.true; k++) centres.push([1.6 * r() - .8, 1.6 * r() - .8]);
    for (let i = 0; i < P.n; i++) { const c = centres[i % P.true]; pts.push([c[0] + P.spread * r.gauss(), c[1] + P.spread * r.gauss()]); }
    const r2 = rng(P.seed + 31); let C = [];
    if (P.init === 'k-means++') {
      C.push(pts[Math.floor(r2() * pts.length)].slice());
      while (C.length < P.k) { const d = pts.map(p => Math.min(...C.map(c => (p[0] - c[0]) ** 2 + (p[1] - c[1]) ** 2))), tot = d.reduce((a, b) => a + b, 0); let u = r2() * tot, i = 0; while (u > d[i] && i < d.length - 1) u -= d[i++]; C.push(pts[i].slice()); }
    } else { for (let k = 0; k < P.k; k++) C.push(pts[Math.floor(r2() * pts.length)].slice()); }
    const lab = kmeansAssign(pts, C);
    return { pts, C, lab, it: 0, moved: Infinity, trail: C.map(c => [c.slice()]) };
  },
  step(S) {
    const C2 = kmeansUpdate(S.pts, S.C, S.lab); S.moved = Math.max(...C2.map((c, k) => Math.hypot(c[0] - S.C[k][0], c[1] - S.C[k][1])));
    S.C = C2; S.C.forEach((c, k) => S.trail[k].push(c.slice())); S.lab = kmeansAssign(S.pts, S.C); S.it++;
  },
  draw(c, S, P, W, H) {
    bg(c, W, H); const size = Math.min(H - 30, W - 40), V = panel(16, 16, size, -1.3, 1.3);
    const res = 130; heatCv.width = heatCv.height = res; const img = heatCx.createImageData(res, res);
    for (let j = 0; j < res; j++) for (let i = 0; i < res; i++) {
      const x = -1.3 + (i + .5) / res * 2.6, y = 1.3 - (j + .5) / res * 2.6; let best = 0, bd = Infinity; S.C.forEach((cc, k) => { const d = (x - cc[0]) ** 2 + (y - cc[1]) ** 2; if (d < bd) { bd = d; best = k; } });
      const hex = this.pal[best % 8], k4 = 4 * (j * res + i); img.data[k4] = parseInt(hex.slice(1, 3), 16) * .22 + 10; img.data[k4 + 1] = parseInt(hex.slice(3, 5), 16) * .22 + 14; img.data[k4 + 2] = parseInt(hex.slice(5, 7), 16) * .22 + 34; img.data[k4 + 3] = 255;
    }
    heatCx.putImageData(img, 0, 0); c.imageSmoothingEnabled = false; c.drawImage(heatCv, V.x0, V.y0, size, size); c.imageSmoothingEnabled = true;
    axesIn(c, V);
    S.pts.forEach((p, i) => { c.fillStyle = this.pal[S.lab[i] % 8]; c.beginPath(); c.arc(V.X(p[0]), V.Y(p[1]), 3.3, 0, TAU); c.fill(); });
    S.trail.forEach((tr, k) => { c.strokeStyle = 'rgba(255,255,255,.6)'; c.lineWidth = 1.2; c.beginPath(); tr.forEach((q, m) => m ? c.lineTo(V.X(q[0]), V.Y(q[1])) : c.moveTo(V.X(q[0]), V.Y(q[1]))); c.stroke(); });
    S.C.forEach((cc, k) => { c.fillStyle = this.pal[k % 8]; c.strokeStyle = '#fff'; c.lineWidth = 2.5; c.beginPath(); c.moveTo(V.X(cc[0]) - 8, V.Y(cc[1]) - 8); c.lineTo(V.X(cc[0]) + 8, V.Y(cc[1]) + 8); c.moveTo(V.X(cc[0]) + 8, V.Y(cc[1]) - 8); c.lineTo(V.X(cc[0]) - 8, V.Y(cc[1]) + 8); c.stroke(); });
    frame(c, V);
  },
  hud(S) { return hudRows([['iteration', S.it], ['inertia', fm(inertia(S.pts, S.C, S.lab), 3)], ['centres moved', S.moved < Infinity ? fm(S.moved, 4) : '—'], ['status', S.moved < 1e-9 ? 'converged' : 'moving']]); },
  sample(S) { return { J: inertia(S.pts, S.C, S.lab) }; },
  plots: [{ title: 'Inertia J (sum of squared distances to the centres)', series: [{ k: 'J', col: COL.am, label: 'J' }] }],
  scen: {
    'k equal to the real number': { true: 4, k: 4 }, 'k too small': { true: 4, k: 2 }, 'k too large': { true: 3, k: 6 },
    'Random start: stuck in a poor solution': { true: 4, k: 4, init: 'random points', seed: 1 }, 'k-means++ start': { true: 5, k: 5, init: 'k-means++', seed: 4 }, 'Overlapping clusters': { true: 4, k: 4, spread: .3 },
  },
  theory(P, S) {
    return {
      title: 'k-means clustering', intro: 'Unsupervised learning: find structure in data that has no labels. k-means looks for k groups whose points sit close to the group’s centre.',
      sections: [
        { h: 'The objective', p: 'Choose centres μ₁…μ_k and an assignment of every point to one centre so that the total squared distance (the inertia) is as small as possible.', tex: [T`J=\sum_{i=1}^{n}\big\lVert\mathbf x_i-\boldsymbol\mu_{c(i)}\big\rVert^2`] },
        { h: 'Two alternating steps', p: 'Assign: each point joins its nearest centre (this cannot increase J). Update: each centre moves to the mean of its points (the mean is exactly the point that minimises the sum of squared distances — this cannot increase J either). So J only goes down, and the algorithm stops when nothing changes.', tex: [T`c(i)=\arg\min_k\lVert\mathbf x_i-\boldsymbol\mu_k\rVert^2\qquad\boldsymbol\mu_k=\frac{1}{|C_k|}\sum_{i\in C_k}\mathbf x_i`] },
        { h: 'Its weaknesses', p: 'It stops in the nearest local minimum, so the start matters — k-means++ spreads the first centres out to avoid bad starts. You must choose k yourself: J always falls as k grows, so look for the "elbow" where adding a centre stops helping much. And it assumes round, similar-sized clusters.' },
      ],
    };
  },
};

/* =====================================================================
   FRAMEWORK
   ===================================================================== */
const CAP = 5000;
let E, P, S, running = true, curId = 'mlp', scenName = '', log, logN, stepAcc = 0, deepLinked = false;
const side = $('#side');

function defaults(e) { const p = {}; e.params.forEach(a => p[a.id] = a.def); return p; }
function allKeys(e) { const ks = []; e.plots.forEach(r => r.series.forEach(s => { if (!ks.includes(s.k)) ks.push(s.k); })); return ks; }
function resetLog() { log = { t: new Float32Array(CAP), k: {} }; allKeys(E).forEach(k => log.k[k] = new Float32Array(CAP)); logN = 0; }
function record() { const k = logN % CAP, smp = E.sample(S, P); log.t[k] = S.it; for (const key in log.k) log.k[key][k] = smp[key] ?? NaN; logN++; }
function startRun(extra) { S = E.init(P, extra); stepAcc = 0; resetLog(); record(); running = true; $('#bRun').textContent = 'Pause'; }
function selectExp(id, sc) {
  curId = id; E = EXPS[id]; $('#exp').value = id; P = defaults(E); let extra = null;
  if (sc && E.scen[sc]) { if (E.onParam && E.scen[sc].surf) { P.surf = E.scen[sc].surf; E.onParam('surf', P); } Object.assign(P, E.scen[sc]); }
  scenName = sc || ''; buildSide(); fillScen(); startRun(extra); persist();
}
function fillScen() { const s = $('#scen'); s.innerHTML = ''; s.add(new Option('— Things to try —', '')); Object.keys(E.scen).forEach(k => s.add(new Option(k, k))); s.value = scenName; }
function fmtParam(a, v) { if (a.opts) return v; const d = a.step >= 1 ? 0 : a.step >= .1 ? 1 : a.step >= .01 ? 2 : a.step >= .001 ? 3 : 4; return (+v).toFixed(d) + (a.u ? ' ' + a.u : ''); }
function buildSide() {
  let h = `<h4>${E.name}</h4><p class="about">${E.about}</p>`;
  if (['logreg', 'mlp'].includes(curId)) h += `<div class="legend"><span><i style="background:#22d3ee"></i>class 1</span><span><i style="background:#f472b6"></i>class 0</span>${curId === 'mlp' ? '<span><i style="border:2px solid #8a93b8;background:none"></i>test point</span>' : ''}<span><i style="background:#ebebeb"></i>boundary p = 0.5</span></div>`;
  h += '<h4>Settings</h4>';
  E.params.forEach(a => {
    if (a.opts) h += `<div class="row"><label>${a.l}</label><select id="p_${a.id}">${a.opts.map(o => `<option${o === P[a.id] ? ' selected' : ''}>${o}</option>`).join('')}</select></div>`;
    else h += `<div class="row"><label>${a.l}</label><input type="range" id="p_${a.id}" min="${a.min}" max="${a.max}" step="${a.step}" value="${P[a.id]}"><output id="o_${a.id}"></output></div>`;
  });
  h += `<p style="color:var(--muted);font-size:12px;margin-top:14px">Settings marked by a restart (data, network shape, seed) start training again; the others change it while it runs. <b>Theory</b> explains the maths behind this experiment. Space = start/pause.</p>`;
  side.innerHTML = h;
  E.params.forEach(a => {
    const el = $('#p_' + a.id), out = $('#o_' + a.id), show = () => { if (out) out.textContent = fmtParam(a, P[a.id]); }; show();
    el.oninput = el.onchange = () => { P[a.id] = a.opts ? el.value : parseFloat(el.value); show(); const rebuild = E.onParam && E.onParam(a.id, P); if (a.re) startRun(S && E.save ? E.save(S) : null); if (rebuild) buildSide(); persist(); };
  });
}
function advance(dt) {
  stepAcc += Math.min(dt, .1) * E.rate * parseFloat($('#speed').value);
  let n = Math.floor(stepAcc); stepAcc -= n; n = Math.min(n, 200);
  for (let i = 0; i < n; i++) { E.step(S, P); record(); }
}

/* ---- plots ---- */
function drawPlots() {
  const [W, Hh] = fitCanvas(pl, px), c = px; c.clearRect(0, 0, W, Hh);
  const n = Math.min(logN, CAP), start = logN - n, idx = k => (start + k) % CAP, rows = E.plots, L = 56, R = 12, gap = 8, rh = (Hh - gap * (rows.length + 1) - 10) / rows.length;
  c.font = '11px system-ui';
  rows.forEach((r, ri) => {
    const y0 = gap + ri * (rh + gap), pw = W - L - R; c.fillStyle = 'rgba(255,255,255,.025)'; c.fillRect(L, y0, pw, rh); c.fillStyle = '#8a93b8'; c.textAlign = 'left'; c.fillText(r.title, L + 6, y0 + 12);
    let lx = L + pw - 6; c.textAlign = 'right'; for (let i = r.series.length - 1; i >= 0; i--) { const s = r.series[i]; c.fillStyle = s.col; c.fillText(s.label, lx, y0 + 12); lx -= c.measureText(s.label).width + 12; }
    if (n < 2) return;
    const tr = v => (r.log ? Math.log10(Math.max(v, 1e-10)) : v);
    let lo = 1e30, hi = -1e30; for (const s of r.series) for (let k = 0; k < n; k++) { const v = tr(log.k[s.k][idx(k)]); if (isFinite(v)) { if (v < lo) lo = v; if (v > hi) hi = v; } }
    if (!(hi > lo)) { lo -= 1; hi += 1; } const pad = (hi - lo) * .12; lo -= pad; hi += pad;
    const t0 = log.t[idx(0)], t1 = Math.max(log.t[idx(n - 1)], t0 + 1), X = t => L + (t - t0) / (t1 - t0) * pw, Y = v => y0 + rh - 4 - (v - lo) / (hi - lo) * (rh - 20);
    c.strokeStyle = 'rgba(255,255,255,.06)'; c.fillStyle = '#6b7599'; c.textAlign = 'right';
    for (let g = 0; g <= 3; g++) { const v = lo + (hi - lo) * g / 3, yy = Y(v); c.beginPath(); c.moveTo(L, yy); c.lineTo(L + pw, yy); c.stroke(); c.fillText(r.log ? Theory.fmt(Math.pow(10, v)) : Theory.fmt(v), L - 5, yy + 3); }
    if (ri === rows.length - 1) { c.textAlign = 'center'; for (const tv of Theory.nice(t0, t1, 6)) if (X(tv) < W - 100) c.fillText(Theory.fmt(tv), X(tv), y0 + rh + 12); c.textAlign = 'right'; c.fillText('training step', W - 12, y0 + rh + 12); }
    c.save(); c.beginPath(); c.rect(L, y0, pw, rh); c.clip();
    const stride = Math.max(1, Math.floor(n / pw));
    for (const s of r.series) { c.strokeStyle = s.col; c.lineWidth = s.dash ? 1.3 : 1.8; c.setLineDash(s.dash ? [4, 4] : []); c.beginPath(); let pen = false; for (let k = 0; k < n; k += stride) { const v = tr(log.k[s.k][idx(k)]); if (!isFinite(v)) { pen = false; continue; } const xx = X(log.t[idx(k)]), yy = Y(v); pen ? c.lineTo(xx, yy) : c.moveTo(xx, yy); pen = true; } c.stroke(); }
    c.restore(); c.setLineDash([]);
  });
}

/* ---- UI wiring ---- */
const groups = {}; Object.keys(EXPS).forEach(id => (groups[EXPS[id].group] = groups[EXPS[id].group] || []).push(id));
for (const g in groups) { const og = document.createElement('optgroup'); og.label = g; groups[g].forEach(id => og.appendChild(new Option(EXPS[id].name, id))); $('#exp').appendChild(og); }
$('#exp').onchange = e => selectExp(e.target.value);
$('#scen').onchange = e => { if (e.target.value) selectExp(curId, e.target.value); };
$('#bRun').onclick = () => { running = !running; $('#bRun').textContent = running ? 'Pause' : 'Train'; };
$('#bStep').onclick = () => { running = false; $('#bRun').textContent = 'Train'; E.step(S, P); record(); };
$('#bReset').onclick = () => startRun(S && E.save ? E.save(S) : null);
$('#bTheory').onclick = () => Theory.open(E.theory(P, S));
function setStatus() {
  const s = $('#status'); let cls = running ? 'ok' : '', txt = running ? 'Training' : 'Paused';
  if (S.diverged || (S.runs && S.runs.every(r => r.dead)) || (S.net && !isFinite(S.net.W[0][0]))) { cls = 'bad'; txt = 'Diverged — lower the learning rate'; }
  else if (curId === 'kmeans' && S.moved < 1e-9) { cls = 'warn'; txt = 'Converged'; }
  s.className = 'pill ' + cls; s.textContent = txt;
}
cv.onpointerdown = e => { if (E.pointer) { const r = cv.getBoundingClientRect(); E.pointer('down', e.clientX - r.left, e.clientY - r.top, S, P); } };

/* ---- save / load / CSV ---- */
const snapshot = () => ({ lab: 'ml', v: 1, exp: curId, P, extra: E.save ? E.save(S) : null });
function persist() { if (deepLinked) return; try { localStorage.setItem('ml.v1', JSON.stringify(snapshot())); } catch (e) { } }
function download(name, text, type) { const a = document.createElement('a'); a.href = URL.createObjectURL(new Blob([text], { type })); a.download = name; a.click(); URL.revokeObjectURL(a.href); }
function toast(m) { const e = $('#toast'); e.textContent = m; e.classList.add('show'); clearTimeout(toast.t); toast.t = setTimeout(() => e.classList.remove('show'), 1800); }
function applySnap(o) { curId = o.exp in EXPS ? o.exp : 'mlp'; E = EXPS[curId]; $('#exp').value = curId; P = { ...defaults(E), ...o.P }; scenName = ''; buildSide(); fillScen(); startRun(o.extra); }
$('#bSave').onclick = () => { download(`ml-${curId}.json`, JSON.stringify(snapshot(), null, 1), 'application/json'); toast('Setup saved'); };
$('#bLoad').onclick = () => $('#file').click();
$('#file').onchange = e => { const f = e.target.files[0]; if (!f) return; const r = new FileReader(); r.onload = () => { try { const o = JSON.parse(r.result); if (o.lab !== 'ml') throw 0; applySnap(o); toast('Setup loaded'); } catch (x) { toast('Not an ML Lab file'); } }; r.readAsText(f); e.target.value = ''; };
$('#bCsv').onclick = () => {
  if (logN < 2) return toast('Train first');
  const keys = Object.keys(log.k), n = Math.min(logN, CAP), st = logN - n, rows = ['step,' + keys.join(',')];
  for (let k = 0; k < n; k++) { const j = (st + k) % CAP; rows.push(log.t[j] + ',' + keys.map(q => log.k[q][j].toPrecision(6)).join(',')); }
  download(`ml-${curId}.csv`, rows.join('\n'), 'text/csv'); toast('Exported ' + n + ' rows');
};
addEventListener('keydown', e => { if (e.key === ' ' && e.target === document.body) { e.preventDefault(); $('#bRun').click(); } });

/* ---- deep link (used by the notebooks):  ml/index.html#exp=mlp&data=spiral&layers=3  (optional scen=<name>) ---- */
function fromHash() {
  const q = new URLSearchParams(location.hash.slice(1)), id = q.get('exp'); if (!(id in EXPS)) return false;
  deepLinked = true; selectExp(id, q.get('scen') || undefined); let ch = false;
  E.params.forEach(a => {
    if (!q.has(a.id)) return; const raw = q.get(a.id);
    if (a.opts) { if (a.opts.includes(raw)) { P[a.id] = raw; ch = true; } }
    else { const v = parseFloat(raw); if (isFinite(v)) { P[a.id] = Math.min(a.max, Math.max(a.min, v)); ch = true; } }
  });
  if (ch) { buildSide(); startRun(); }
  return true;
}

/* ---- boot ---- */
let boot = null; try { const o = JSON.parse(localStorage.getItem('ml.v1')); if (o && o.lab === 'ml' && o.exp in EXPS) boot = o; } catch (e) { }
if (!fromHash()) { if (boot) applySnap(boot); else selectExp('mlp'); }
addEventListener('hashchange', fromHash);
let last = performance.now(), hudT = 0;
function loop(now) {
  const dt = (now - last) / 1000; last = now;
  try {
    if (running) advance(dt);
    const [W, H] = fitCanvas(cv, cx); E.draw(cx, S, P, W, H); drawPlots();
    hudT += dt; if (hudT > .15) { hudT = 0; $('#hud').innerHTML = E.hud(S, P); setStatus(); }
  } catch (err) { console.error(err); }
  requestAnimationFrame(loop);
}
requestAnimationFrame(loop);
window.__ml = { get E() { return E; }, get S() { return S; }, get P() { return P; }, selectExp, EXPS, get logN() { return logN; } };
