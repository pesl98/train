/* AI & ML Lab — machine-learning core, written from scratch (no libraries) so every line can be read and tested.
   Used by the lab page (globals) and by the Node tests (module.exports).

   rng(seed)                      seeded random numbers: r() uniform in [0,1), r.gauss() standard normal
   makeData(kind, n, noise, seed) 2-D classification sets: {X: [[x,y]...], Y: [0|1 ...]}
   expandFeatures(X, mode)        'xy' -> [x, y];  'quad' -> [x, y, x², y², xy]
   Net(sizes, opts)               fully connected network trained with back-propagation
   Optim                          update rules: sgd, momentum, rmsprop, adam (on plain arrays of numbers)
   kmeansStep(points, centres)    one assignment + update step of k-means */

function rng(seed) {
  let a = (seed >>> 0) || 1;
  const r = () => { a |= 0; a = (a + 0x6D2B79F5) | 0; let t = Math.imul(a ^ (a >>> 15), 1 | a); t = (t + Math.imul(t ^ (t >>> 7), 61 | t)) ^ t; return ((t ^ (t >>> 14)) >>> 0) / 4294967296; };
  r.gauss = () => { let u = 0, v = 0; while (u === 0) u = r(); v = r(); return Math.sqrt(-2 * Math.log(u)) * Math.cos(2 * Math.PI * v); };
  return r;
}

/* ---------------- data sets (points roughly inside [-1, 1]²) ---------------- */
function makeData(kind, n, noise, seed) {
  const r = rng(seed), X = [], Y = [];
  const add = (x, y, c) => { X.push([x + noise * r.gauss(), y + noise * r.gauss()]); Y.push(c); };
  for (let i = 0; i < n; i++) {
    const c = i % 2;
    if (kind === 'blobs') { add(c ? 0.45 : -0.45, c ? 0.35 : -0.35, c); X[X.length - 1][0] += 0.22 * r.gauss(); X[X.length - 1][1] += 0.22 * r.gauss(); }
    else if (kind === 'circle') {
      const rad = c ? 0.45 * Math.sqrt(r()) : 0.7 + 0.25 * r(), th = 2 * Math.PI * r();
      add(rad * Math.cos(th), rad * Math.sin(th), c);
    } else if (kind === 'xor') {
      let x = 2 * r() - 1, y = 2 * r() - 1;
      if (Math.abs(x) < 0.08) x += Math.sign(x || 1) * 0.08; if (Math.abs(y) < 0.08) y += Math.sign(y || 1) * 0.08;
      add(x * 0.95, y * 0.95, (x > 0) === (y > 0) ? 1 : 0);
    } else if (kind === 'moons') {
      const th = Math.PI * r();
      if (c) add(0.55 * Math.cos(th) - 0.25, 0.55 * Math.sin(th) - 0.1, 1);
      else add(0.55 - 0.55 * Math.cos(th) - 0.25 + 0.0, -0.55 * Math.sin(th) + 0.18, 0);
    } else if (kind === 'spiral') {
      const t = r(), ang = t * 3.2 * Math.PI + (c ? Math.PI : 0), rad = 0.08 + 0.85 * t;
      add(rad * Math.cos(ang), rad * Math.sin(ang), c);
    } else throw new Error('unknown data set ' + kind);
  }
  return { X, Y };
}
function expandFeatures(X, mode) { return mode === 'quad' ? X.map(([x, y]) => [x, y, x * x, y * y, x * y]) : X.map(p => p.slice()); }
function splitData(D, testFrac, seed) {
  const r = rng(seed + 991), idx = D.X.map((_, i) => i);
  for (let i = idx.length - 1; i > 0; i--) { const j = Math.floor(r() * (i + 1)); [idx[i], idx[j]] = [idx[j], idx[i]]; }
  const nt = Math.round(idx.length * testFrac), te = idx.slice(0, nt), tr = idx.slice(nt);
  const pick = ids => ({ X: ids.map(i => D.X[i]), Y: ids.map(i => D.Y[i]) });
  return { train: pick(tr), test: pick(te) };
}

/* ---------------- activation functions (derivative written in terms of the output a) ---------------- */
const ACT = {
  tanh: { f: Math.tanh, d: a => 1 - a * a },
  relu: { f: z => (z > 0 ? z : 0), d: a => (a > 0 ? 1 : 0) },
  sigmoid: { f: z => 1 / (1 + Math.exp(-z)), d: a => a * (1 - a) },
  linear: { f: z => z, d: () => 1 },
};

/* ---------------- optimisers: update params p in place from gradient g ---------------- */
const Optim = {
  sgd(p, g, st, h) { for (let i = 0; i < p.length; i++) p[i] -= h.lr * g[i]; },
  momentum(p, g, st, h) { const v = st.v || (st.v = new Float64Array(p.length)), b = h.beta ?? 0.9; for (let i = 0; i < p.length; i++) { v[i] = b * v[i] + (1 - b) * g[i]; p[i] -= h.lr * v[i]; } },   // v = running average of gradients
  rmsprop(p, g, st, h) { const s = st.s || (st.s = new Float64Array(p.length)), b = h.beta2 ?? 0.9; for (let i = 0; i < p.length; i++) { s[i] = b * s[i] + (1 - b) * g[i] * g[i]; p[i] -= h.lr * g[i] / (Math.sqrt(s[i]) + 1e-8); } },
  adam(p, g, st, h) {
    const m = st.m || (st.m = new Float64Array(p.length)), s = st.s || (st.s = new Float64Array(p.length)), b1 = 0.9, b2 = 0.999;
    st.t = (st.t || 0) + 1; const c1 = 1 - Math.pow(b1, st.t), c2 = 1 - Math.pow(b2, st.t);
    for (let i = 0; i < p.length; i++) { m[i] = b1 * m[i] + (1 - b1) * g[i]; s[i] = b2 * s[i] + (1 - b2) * g[i] * g[i]; p[i] -= h.lr * (m[i] / c1) / (Math.sqrt(s[i] / c2) + 1e-8); }
  },
};

/* ---------------- a fully connected network ----------------
   sizes = [inputs, hidden..., outputs].  W[l] is a (sizes[l+1] × sizes[l]) matrix stored row by row.
   output 'sigmoid' + loss 'bce' for classification; output 'linear' + loss 'mse' for regression. */
class Net {
  constructor(sizes, { act = 'tanh', out = 'sigmoid', loss = 'bce', seed = 1 } = {}) {
    this.sizes = sizes; this.act = act; this.out = out; this.loss = loss;
    const r = rng(seed); this.W = []; this.b = []; this.st = [];
    for (let l = 0; l < sizes.length - 1; l++) {
      const nin = sizes[l], nout = sizes[l + 1], sc = act === 'relu' ? Math.sqrt(2 / nin) : Math.sqrt(1 / nin);
      const W = new Float64Array(nout * nin); for (let k = 0; k < W.length; k++) W[k] = sc * r.gauss();
      const b = new Float64Array(nout).fill(act === 'relu' ? 0.05 : 0);
      this.W.push(W); this.b.push(b); this.st.push({ W: {}, b: {} });
    }
  }
  get nParams() { return this.W.reduce((s, w, l) => s + w.length + this.b[l].length, 0); }
  forward(x) {                       // returns the activations of every layer, a[0] = input
    const A = [Float64Array.from(x)], L = this.W.length;
    for (let l = 0; l < L; l++) {
      const nin = this.sizes[l], nout = this.sizes[l + 1], W = this.W[l], b = this.b[l], a = A[l], z = new Float64Array(nout);
      const f = ACT[l === L - 1 ? this.out : this.act].f;
      for (let j = 0; j < nout; j++) { let s = b[j]; for (let i = 0; i < nin; i++) s += W[j * nin + i] * a[i]; z[j] = f(s); }
      A.push(z);
    }
    return A;
  }
  predict(x) { const A = this.forward(x); return A[A.length - 1][0]; }
  lossOf(X, Y) {
    if (!X.length) return NaN; let s = 0;
    for (let k = 0; k < X.length; k++) {
      const p = this.predict(X[k]), y = Y[k];
      if (this.loss === 'bce') { const q = Math.min(1 - 1e-12, Math.max(1e-12, p)); s += -(y * Math.log(q) + (1 - y) * Math.log(1 - q)); }
      else s += 0.5 * (p - y) * (p - y);
    }
    return s / X.length;
  }
  accuracy(X, Y) { if (!X.length) return NaN; let c = 0; for (let k = 0; k < X.length; k++) c += ((this.predict(X[k]) > 0.5 ? 1 : 0) === Y[k]); return c / X.length; }
  /* gradient of the mean loss (plus ½·l2·|W|²) over a batch, by back-propagation */
  gradients(X, Y, l2 = 0) {
    const L = this.W.length, gW = this.W.map(w => new Float64Array(w.length)), gb = this.b.map(b => new Float64Array(b.length));
    for (let k = 0; k < X.length; k++) {
      const A = this.forward(X[k]), out = A[L], y = Y[k];
      // output error: for sigmoid + cross-entropy and for linear + squared error it is simply (prediction − target)
      let delta = new Float64Array(out.length);
      for (let j = 0; j < out.length; j++) {
        const e = out[j] - (Array.isArray(y) ? y[j] : y);
        delta[j] = (this.loss === 'bce' && this.out === 'sigmoid') || (this.loss === 'mse' && this.out === 'linear') ? e : e * ACT[this.out].d(out[j]);
      }
      for (let l = L - 1; l >= 0; l--) {
        const nin = this.sizes[l], nout = this.sizes[l + 1], a = A[l], W = this.W[l];
        for (let j = 0; j < nout; j++) { gb[l][j] += delta[j]; for (let i = 0; i < nin; i++) gW[l][j * nin + i] += delta[j] * a[i]; }
        if (l > 0) {
          const prev = new Float64Array(nin), d = ACT[this.act].d;
          for (let i = 0; i < nin; i++) { let s = 0; for (let j = 0; j < nout; j++) s += W[j * nin + i] * delta[j]; prev[i] = s * d(a[i]); }
          delta = prev;
        }
      }
    }
    const n = X.length || 1;
    for (let l = 0; l < L; l++) { for (let i = 0; i < gW[l].length; i++) gW[l][i] = gW[l][i] / n + l2 * this.W[l][i]; for (let i = 0; i < gb[l].length; i++) gb[l][i] /= n; }
    return { gW, gb };
  }
  trainBatch(X, Y, { lr = 0.03, l2 = 0, opt = 'adam' } = {}) {
    const { gW, gb } = this.gradients(X, Y, l2), h = { lr };
    for (let l = 0; l < this.W.length; l++) { Optim[opt](this.W[l], gW[l], this.st[l].W, h); Optim[opt](this.b[l], gb[l], this.st[l].b, h); }
  }
}

/* ---------------- k-means ---------------- */
function kmeansAssign(P, C) { return P.map(p => { let best = 0, bd = Infinity; C.forEach((c, k) => { const d = (p[0] - c[0]) ** 2 + (p[1] - c[1]) ** 2; if (d < bd) { bd = d; best = k; } }); return best; }); }
function kmeansUpdate(P, C, lab) {
  return C.map((c, k) => { let sx = 0, sy = 0, n = 0; P.forEach((p, i) => { if (lab[i] === k) { sx += p[0]; sy += p[1]; n++; } }); return n ? [sx / n, sy / n] : c.slice(); });
}
function inertia(P, C, lab) { return P.reduce((s, p, i) => s + (p[0] - C[lab[i]][0]) ** 2 + (p[1] - C[lab[i]][1]) ** 2, 0); }

if (typeof module !== 'undefined' && module.exports) module.exports = { rng, makeData, expandFeatures, splitData, ACT, Optim, Net, kmeansAssign, kmeansUpdate, inertia };
