'use strict';
/* Physics Lab — six experiments sharing one framework.
   Mechanics: projectile with drag · double pendulum (chaos) · driven oscillator · orbits
   Electromagnetism: charged particle in E & B · electric-field sandbox
   Each experiment supplies: params, init, step, draw, sample (for graphs), scenarios, theory. */
const $ = s => document.querySelector(s);
const TAU = Math.PI * 2, D2R = Math.PI / 180, T = String.raw;
const COL = { cy: '#22d3ee', vi: '#a78bfa', am: '#fbbf24', gr: '#4ade80', pk: '#f472b6', bl: '#60a5fa', rd: '#f87171' };
const cv = $('#view'), cx = cv.getContext('2d'), pl = $('#plots'), px = pl.getContext('2d');

/* ---------------- helpers ---------------- */
function fitCanvas(c, ctx) {
  const r = c.getBoundingClientRect(), d = devicePixelRatio || 1;
  if (c.width !== Math.round(r.width * d) || c.height !== Math.round(r.height * d)) { c.width = Math.round(r.width * d); c.height = Math.round(r.height * d); }
  ctx.setTransform(d, 0, 0, d, 0, 0); return [r.width, r.height];
}
function arrow(c, x0, y0, x1, y1, col, w = 2) {
  const L = Math.hypot(x1 - x0, y1 - y0); if (L < 2) return; const a = Math.atan2(y1 - y0, x1 - x0), h = Math.min(10, L * .5);
  c.strokeStyle = c.fillStyle = col; c.lineWidth = w; c.lineCap = 'round'; c.beginPath(); c.moveTo(x0, y0); c.lineTo(x1 - h * .6 * Math.cos(a), y1 - h * .6 * Math.sin(a)); c.stroke();
  c.beginPath(); c.moveTo(x1, y1); c.lineTo(x1 - h * Math.cos(a - .4), y1 - h * Math.sin(a - .4)); c.lineTo(x1 - h * Math.cos(a + .4), y1 - h * Math.sin(a + .4)); c.closePath(); c.fill();
}
function bg(c, W, H) { const g = c.createRadialGradient(W / 2, H / 2, 20, W / 2, H / 2, Math.max(W, H) * .75); g.addColorStop(0, '#12183a'); g.addColorStop(1, '#080b17'); c.fillStyle = g; c.fillRect(0, 0, W, H); }
function rk4(f, s, h) {
  const k1 = f(s), k2 = f(s.map((v, i) => v + k1[i] * h / 2)), k3 = f(s.map((v, i) => v + k2[i] * h / 2)), k4 = f(s.map((v, i) => v + k3[i] * h));
  return s.map((v, i) => v + h / 6 * (k1[i] + 2 * k2[i] + 2 * k3[i] + k4[i]));
}
const fm = (v, d = 2) => (Math.abs(v) < 1e-9 ? 0 : v).toFixed(d);
const sub = (b, t) => `${b}<tspan font-size="10" dy="3">${t}</tspan><tspan dy="-3"></tspan>`;
const hudRows = rows => rows.map(r => `${r[0]} <b>${r[1]}</b>`).join('<br>');

const EXPS = {};

/* =====================================================================
   1. PROJECTILE
   ===================================================================== */
EXPS.proj = {
  name: 'Projectile motion', group: 'Mechanics', ts: 1, h: 0.002, win: 10, tu: 's', ld: 0.01,
  params: [
    ['v0', 'Launch speed', 5, 60, 0.5, 'm/s', 25, 1], ['ang', 'Launch angle', 5, 85, 1, '°', 45, 1], ['h0', 'Launch height', 0, 30, 0.5, 'm', 0, 1],
    ['g', 'Gravity', 1.6, 25, 0.1, 'm/s²', 9.81, 0], ['k', 'Air drag k', 0, 0.08, 0.001, '1/m', 0.01, 0],
  ],
  init(P) { const a = P.ang * D2R; return { t: 0, x: 0, y: P.h0, vx: P.v0 * Math.cos(a), vy: P.v0 * Math.sin(a), done: false, trail: [[0, P.h0]], marks: [], n: 0, range: 0, tf: 0, ymax: P.h0, vimp: 0 }; },
  step(S, P, h) {
    if (S.done) return;
    const n = rk4(s => { const sp = Math.hypot(s[2], s[3]); return [s[2], s[3], -P.k * sp * s[2], -P.g - P.k * sp * s[3]]; }, [S.x, S.y, S.vx, S.vy], h);
    S.t += h;
    if (n[1] < 0) { const fr = S.y / (S.y - n[1]); S.x += (n[0] - S.x) * fr; S.y = 0; S.vx += (n[2] - S.vx) * fr; S.vy += (n[3] - S.vy) * fr; S.done = true; S.range = S.x; S.tf = S.t - h * (1 - fr); S.vimp = Math.hypot(S.vx, S.vy); S.trail.push([S.x, 0]); return; }
    const before = Math.floor(S.t); [S.x, S.y, S.vx, S.vy] = n; S.ymax = Math.max(S.ymax, S.y);
    if (Math.floor(S.t) > before) S.marks.push([S.x, S.y, Math.floor(S.t)]);
    if (++S.n % 5 === 0) S.trail.push([S.x, S.y]);
  },
  vac(P) { const a = P.ang * D2R, vs = P.v0 * Math.sin(a), vc = P.v0 * Math.cos(a), tf = (vs + Math.sqrt(vs * vs + 2 * P.g * P.h0)) / P.g; return { tf, R: vc * tf, ymax: P.h0 + vs * vs / (2 * P.g), vc, vs }; },
  draw(c, S, P, W, H) {
    bg(c, W, H); const V = this.vac(P), xe = Math.max(V.R * 1.12, 8), ye = Math.max(V.ymax * 1.3, 4), sc = Math.min((W - 90) / xe, (H - 90) / ye), ox = 50, oy = H - 45;
    const X = x => ox + x * sc, Y = y => oy - y * sc;
    c.strokeStyle = 'rgba(255,255,255,.05)'; c.lineWidth = 1; c.beginPath(); const gs = [1, 2, 5, 10, 20, 50].find(g => g * sc > 38) || 100;
    for (let x = 0; x < xe * 1.2; x += gs) { c.moveTo(X(x), 0); c.lineTo(X(x), oy); } for (let y = 0; y < ye * 1.2; y += gs) { c.moveTo(ox, Y(y)); c.lineTo(W, Y(y)); } c.stroke();
    c.fillStyle = '#6b7599'; c.font = '11px system-ui'; c.textAlign = 'center'; for (let x = 0; x < xe * 1.1; x += gs) c.fillText(x + ' m', X(x), oy + 28);
    c.fillStyle = '#1a2447'; c.fillRect(0, oy, W, H - oy); c.strokeStyle = '#3b4a8a'; c.beginPath(); c.moveTo(0, oy); c.lineTo(W, oy); c.stroke();
    // vacuum parabola
    c.setLineDash([5, 6]); c.strokeStyle = 'rgba(167,139,250,.7)'; c.lineWidth = 1.6; c.beginPath();
    for (let i = 0; i <= 80; i++) { const t = V.tf * i / 80, x = V.vc * t, y = P.h0 + V.vs * t - .5 * P.g * t * t; i ? c.lineTo(X(x), Y(y)) : c.moveTo(X(x), Y(y)); } c.stroke(); c.setLineDash([]);
    c.fillStyle = COL.vi; c.textAlign = 'left'; c.fillText('vacuum', X(V.R * .55), Y(V.ymax) - 8);
    // actual path
    c.strokeStyle = COL.cy; c.lineWidth = 2.6; c.lineJoin = 'round'; c.beginPath(); S.trail.forEach((p, i) => i ? c.lineTo(X(p[0]), Y(p[1])) : c.moveTo(X(p[0]), Y(p[1]))); c.lineTo(X(S.x), Y(S.y)); c.stroke();
    for (const m of S.marks) { c.fillStyle = '#fbbf24'; c.beginPath(); c.arc(X(m[0]), Y(m[1]), 3.5, 0, TAU); c.fill(); c.fillStyle = '#c9b46a'; c.textAlign = 'center'; c.fillText(m[2] + ' s', X(m[0]), Y(m[1]) - 9); }
    const sp = Math.hypot(S.vx, S.vy);
    if (!S.done) { arrow(c, X(S.x), Y(S.y), X(S.x) + S.vx * sc * .2, Y(S.y) - S.vy * sc * .2, COL.am, 2); }
    c.shadowColor = COL.cy; c.shadowBlur = 14; c.fillStyle = '#fff'; c.beginPath(); c.arc(X(S.x), Y(S.y), 6, 0, TAU); c.fill(); c.shadowBlur = 0;
    if (S.done) { c.fillStyle = COL.gr; c.textAlign = 'center'; c.fillText(`range ${fm(S.range)} m`, X(S.range), oy + 14); }
    c.fillStyle = '#2c3566'; c.save(); c.translate(X(0), Y(P.h0)); c.rotate(-P.ang * D2R); c.fillRect(-6, -5, 30, 10); c.restore();
  },
  hud(S, P) { const V = this.vac(P); return hudRows([['t', fm(S.t) + ' s'], ['height', fm(S.y) + ' m'], ['speed', fm(Math.hypot(S.vx, S.vy)) + ' m/s'], ['max height', fm(S.ymax) + ' m'], [S.done ? 'range' : 'range (vacuum)', fm(S.done ? S.range : V.R) + ' m'], ['flight time', S.done ? fm(S.tf) + ' s' : '…'], ['vacuum range', fm(V.R) + ' m']]); },
  sample(S, P) { const sp = Math.hypot(S.vx, S.vy); return { x: S.x, y: S.y, vx: S.vx, vy: S.vy, sp, ke: .5 * sp * sp, pe: P.g * S.y, e: .5 * sp * sp + P.g * S.y }; },
  active: S => !S.done || true,
  plots: [
    { title: 'Position (m)', series: [{ k: 'x', col: COL.cy, label: 'x' }, { k: 'y', col: COL.vi, label: 'height' }] },
    { title: 'Velocity (m/s)', series: [{ k: 'vx', col: COL.cy, label: 'vx' }, { k: 'vy', col: COL.vi, label: 'vy' }, { k: 'sp', col: COL.am, label: 'speed' }] },
    { title: 'Energy per kg (J/kg)', series: [{ k: 'ke', col: COL.am, label: 'kinetic' }, { k: 'pe', col: COL.pk, label: 'potential' }, { k: 'e', col: COL.gr, label: 'total' }] },
  ],
  scen: {
    'Vacuum (no drag)': { k: 0 }, 'Cannonball with air drag': { v0: 50, k: 0.02 }, 'Best angle without drag (45°)': { k: 0, ang: 45 }, 'Best angle with drag (lower than 45°)': { k: 0.02, v0: 50, ang: 38 },
    'On the Moon': { g: 1.62, k: 0 }, 'Off a cliff': { h0: 25, ang: 15, k: 0.005 }, 'Straight up': { ang: 85, v0: 30, k: 0.01 },
  },
  theory(P, S) {
    const V = this.vac(P), a = P.ang * D2R;
    return {
      title: 'Projectile motion', intro: 'A point mass under gravity and quadratic air drag. Without drag the path is a parabola; drag breaks the symmetry.',
      sections: [
        { h: 'Without drag (dashed)', tex: [T`x = v_0\cos\theta\; t \qquad y = h_0 + v_0\sin\theta\; t - \tfrac12 g t^{2}`, T`R = \dfrac{v_0\cos\theta}{g}\left(v_0\sin\theta + \sqrt{v_0^{2}\sin^{2}\theta + 2gh_0}\right) \qquad R_{h_0=0} = \dfrac{v_0^{2}\sin 2\theta}{g}`, T`y_{max} = h_0 + \dfrac{v_0^{2}\sin^{2}\theta}{2g}`],
          svg: Theory.plot({ f: th => P.v0 * P.v0 * Math.sin(2 * th * D2R) / P.g, xr: [0, 90], xl: 'launch angle (°)', yl: 'range (m, h₀ = 0)', xticks: [0, 15, 30, 45, 60, 75, 90], point: [P.ang, P.v0 * P.v0 * Math.sin(2 * a) / P.g, 'you'], vlines: [{ x: 45, label: '45°' }], title: 'range is largest at 45° in vacuum' }) },
        { h: 'With quadratic drag', p: 'Drag opposes the velocity and grows with its square. There is no closed-form solution, so the simulator integrates with 4th-order Runge–Kutta every 2 ms.', tex: [T`\ddot{x} = -k\,|v|\,\dot{x} \qquad \ddot{y} = -g - k\,|v|\,\dot{y}`, T`v_{terminal} = \sqrt{g/k}`], live: `terminal speed here: ${P.k > 0 ? fm(Math.sqrt(P.g / P.k), 1) + ' m/s' : 'none (no drag)'}` },
        { h: 'Energy', p: 'Without drag the total mechanical energy stays constant. With drag the green line falls: the lost energy is heat in the air.', tex: [T`E/m = \tfrac12 v^{2} + g\,y \qquad \dfrac{dE}{dt}\Big/ m = -k\,|v|^{3}`] },
      ],
    };
  },
};

/* =====================================================================
   2. DOUBLE PENDULUM
   ===================================================================== */
EXPS.dbl = {
  name: 'Double pendulum (chaos)', group: 'Mechanics', ts: 1, h: 0.001, win: 15, tu: 's', ld: 0.01,
  params: [
    ['l1', 'Arm 1 length', 0.3, 2, 0.05, 'm', 1, 0], ['l2', 'Arm 2 length', 0.3, 2, 0.05, 'm', 1, 0], ['m1', 'Mass 1', 0.2, 5, 0.1, 'kg', 1, 0], ['m2', 'Mass 2', 0.2, 5, 0.1, 'kg', 1, 0],
    ['g', 'Gravity', 1.6, 25, 0.1, 'm/s²', 9.81, 0], ['b', 'Friction', 0, 0.5, 0.005, '', 0, 0],
    ['a1', 'Start angle 1', -180, 180, 1, '°', 120, 1], ['a2', 'Start angle 2', -180, 180, 1, '°', -10, 1], ['eps', 'Twin offset', 0, 0.02, 0.0001, 'rad', 0.001, 1],
  ],
  init(P) { const s = [P.a1 * D2R, P.a2 * D2R, 0, 0]; return { t: 0, s, s2: [s[0] + P.eps, s[1], 0, 0], tr: [], tr2: [], n: 0 }; },
  acc(P, s) {
    const [t1, t2, w1, w2] = s, { l1, l2, m1, m2, g, b } = P, d = t1 - t2, den = 2 * m1 + m2 - m2 * Math.cos(2 * d);
    const a1 = (-g * (2 * m1 + m2) * Math.sin(t1) - m2 * g * Math.sin(t1 - 2 * t2) - 2 * Math.sin(d) * m2 * (w2 * w2 * l2 + w1 * w1 * l1 * Math.cos(d))) / (l1 * den) - b * w1;
    const a2 = (2 * Math.sin(d) * (w1 * w1 * l1 * (m1 + m2) + g * (m1 + m2) * Math.cos(t1) + w2 * w2 * l2 * m2 * Math.cos(d))) / (l2 * den) - b * w2;
    return [w1, w2, a1, a2];
  },
  step(S, P, h) { const f = s => this.acc(P, s); S.s = rk4(f, S.s, h); if (P.eps > 0) S.s2 = rk4(f, S.s2, h); S.t += h; if (++S.n % 10 === 0) { S.tr.push(this.tip(P, S.s)); if (P.eps > 0) S.tr2.push(this.tip(P, S.s2)); if (S.tr.length > 700) { S.tr.shift(); S.tr2.shift(); } } },
  tip(P, s) { const x1 = P.l1 * Math.sin(s[0]), y1 = -P.l1 * Math.cos(s[0]); return [x1, y1, x1 + P.l2 * Math.sin(s[1]), y1 - P.l2 * Math.cos(s[1])]; },
  energy(P, s) { const [t1, t2, w1, w2] = s, { l1, l2, m1, m2, g } = P; return { T: .5 * (m1 + m2) * l1 * l1 * w1 * w1 + .5 * m2 * l2 * l2 * w2 * w2 + m2 * l1 * l2 * w1 * w2 * Math.cos(t1 - t2), V: -(m1 + m2) * g * l1 * Math.cos(t1) - m2 * g * l2 * Math.cos(t2) }; },
  draw(c, S, P, W, H) {
    bg(c, W, H); const sc = Math.min(W / 2, H * .46) / (P.l1 + P.l2) * .88, ox = W / 2, oy = H * .5;
    const X = x => ox + x * sc, Y = y => oy - y * sc;
    const trail = (tr, col) => { for (let i = 1; i < tr.length; i++) { c.strokeStyle = col; c.globalAlpha = i / tr.length * .8; c.lineWidth = 1.8; c.beginPath(); c.moveTo(X(tr[i - 1][2]), Y(tr[i - 1][3])); c.lineTo(X(tr[i][2]), Y(tr[i][3])); c.stroke(); } c.globalAlpha = 1; };
    trail(S.tr, COL.cy); if (P.eps > 0) trail(S.tr2, COL.vi);
    const body = (s, col, al) => { const p = this.tip(P, s); c.globalAlpha = al; c.strokeStyle = col; c.lineWidth = 5; c.lineCap = 'round'; c.beginPath(); c.moveTo(ox, oy); c.lineTo(X(p[0]), Y(p[1])); c.lineTo(X(p[2]), Y(p[3])); c.stroke(); c.fillStyle = '#fff'; c.beginPath(); c.arc(X(p[0]), Y(p[1]), 5 + P.m1 * 2.2, 0, TAU); c.fill(); c.fillStyle = col; c.beginPath(); c.arc(X(p[2]), Y(p[3]), 5 + P.m2 * 2.2, 0, TAU); c.fill(); c.globalAlpha = 1; };
    if (P.eps > 0) body(S.s2, COL.vi, .7); body(S.s, COL.cy, 1);
    c.fillStyle = '#e8ebff'; c.beginPath(); c.arc(ox, oy, 5, 0, TAU); c.fill();
    c.fillStyle = '#8a93b8'; c.font = '12px system-ui'; c.textAlign = 'right'; c.fillText(P.eps > 0 ? 'violet = identical twin, started ' + P.eps + ' rad away' : 'twin off', W - 14, 22);
  },
  hud(S, P) { const e = this.energy(P, S.s), sp = this.sep(S); return hudRows([['t', fm(S.t) + ' s'], ['θ₁', fm(S.s[0] / D2R, 1) + '°'], ['θ₂', fm(S.s[1] / D2R, 1) + '°'], ['energy', fm(e.T + e.V, 3) + ' J'], ['twin gap', P.eps > 0 ? sp.toExponential(1) + ' rad' : '—']]); },
  sep(S) { return Math.hypot(S.s[0] - S.s2[0], S.s[1] - S.s2[1]); },
  sample(S, P) { const e = this.energy(P, S.s); return { a1: S.s[0] / D2R, a2: S.s[1] / D2R, T: e.T, V: e.V, E: e.T + e.V, dv: P.eps > 0 ? Math.log10(Math.max(this.sep(S), 1e-12)) : -12 }; },
  plots: [
    { title: 'Angles (°)', series: [{ k: 'a1', col: COL.cy, label: 'θ₁' }, { k: 'a2', col: COL.vi, label: 'θ₂' }] },
    { title: 'Energy (J)', series: [{ k: 'T', col: COL.am, label: 'kinetic' }, { k: 'V', col: COL.pk, label: 'potential' }, { k: 'E', col: COL.gr, label: 'total' }] },
    { title: 'Twin separation (log₁₀ rad)', series: [{ k: 'dv', col: COL.rd, label: 'log₁₀ gap' }] },
  ],
  scen: { 'Large swing (chaotic)': {}, 'Small swing (almost regular)': { a1: 10, a2: 5, eps: 0.001 }, 'Butterfly: twin offset 1e-6': { eps: 0.000001 }, 'No twin': { eps: 0 }, 'Heavy second bob': { m2: 4, m1: 0.5 }, 'Friction damps the chaos': { b: 0.15 } },
  theory(P, S) {
    return { title: 'The double pendulum', intro: 'Two coupled pendulums. Simple rules, yet beyond a modest swing the motion is chaotic: tiny differences in the start grow exponentially.',
      sections: [
        { h: 'Equations of motion (Lagrangian)', tex: [T`L = T - V,\qquad T = \tfrac12(m_1+m_2)l_1^2\dot\theta_1^2 + \tfrac12 m_2 l_2^2\dot\theta_2^2 + m_2 l_1 l_2\dot\theta_1\dot\theta_2\cos(\theta_1-\theta_2)`, T`V = -(m_1+m_2)\,g\,l_1\cos\theta_1 - m_2\,g\,l_2\cos\theta_2`,
          T`\ddot\theta_1 = \dfrac{-g(2m_1+m_2)\sin\theta_1 - m_2 g\sin(\theta_1-2\theta_2) - 2\sin(\theta_1-\theta_2)\,m_2\left(\dot\theta_2^2 l_2 + \dot\theta_1^2 l_1\cos(\theta_1-\theta_2)\right)}{l_1\left(2m_1 + m_2 - m_2\cos(2\theta_1-2\theta_2)\right)}`] },
        { h: 'Chaos: sensitive dependence', p: 'The twin (violet) starts a tiny distance from the original. The bottom graph shows their separation: a straight rising line on a log scale means exponential growth, characterised by the Lyapunov exponent λ.', tex: [T`\delta(t) \approx \delta_0\, e^{\lambda t}`], live: 'Try "Small swing" — the gap stays small for much longer.' },
        { h: 'Energy check', p: 'With friction = 0 the total energy (green) must be constant — a good test of the numerical integrator (4th-order Runge–Kutta, 1 ms).', tex: [T`E = T + V = \text{const} \quad(b = 0)`] },
      ] };
  },
};

/* =====================================================================
   3. DRIVEN OSCILLATOR
   ===================================================================== */
EXPS.osc = {
  name: 'Driven spring–mass–damper', group: 'Mechanics', ts: 1, h: 0.002, win: 20, tu: 's', ld: 0.02,
  params: [
    ['m', 'Mass', 0.2, 5, 0.1, 'kg', 1, 0], ['k', 'Spring k', 1, 100, 1, 'N/m', 25, 0], ['c', 'Damping c', 0, 5, 0.05, 'N·s/m', 0.4, 0], ['F0', 'Drive force', 0, 20, 0.5, 'N', 5, 0],
    ['wd', 'Drive frequency', 0.1, 15, 0.05, 'rad/s', 3, 0], ['x0', 'Start position', -1.5, 1.5, 0.05, 'm', 0.5, 1],
  ],
  init(P) { return { t: 0, x: P.x0, v: 0, ext: 1.2, tr: [] }; },
  step(S, P, h) { const t0 = S.t; const r = rk4(s => [s[1], (P.F0 * Math.cos(P.wd * (t0 + (s[2] - t0))) - P.c * s[1] - P.k * s[0]) / P.m, 1], [S.x, S.v, t0], h); S.x = r[0]; S.v = r[1]; S.t += h; S.ext = Math.max(S.ext * .99995, Math.abs(S.x) * 1.15); },
  amp(P, w = P.wd) { return P.F0 / Math.hypot(P.k - P.m * w * w, P.c * w); },
  draw(c, S, P, W, H) {
    bg(c, W, H); const w0 = Math.sqrt(P.k / P.m), sc = (W * .5 - 90) / Math.max(1.2, S.ext), ox = W / 2, oy = H * .45, X = x => ox + x * sc;
    c.fillStyle = '#2c3566'; c.fillRect(30, oy - 70, 14, 140); for (let i = 0; i < 8; i++) { c.strokeStyle = '#3b4a8a'; c.beginPath(); c.moveTo(30, oy - 66 + i * 18); c.lineTo(18, oy - 54 + i * 18); c.stroke(); }
    c.strokeStyle = 'rgba(255,255,255,.07)'; c.setLineDash([4, 6]); c.beginPath(); c.moveTo(ox, oy - 90); c.lineTo(ox, oy + 90); c.stroke(); c.setLineDash([]);
    const bx = X(S.x) - 34, n = 14, x0 = 44, x1 = bx; c.strokeStyle = COL.cy; c.lineWidth = 2.4; c.lineJoin = 'round'; c.beginPath(); c.moveTo(x0, oy);
    for (let i = 0; i < n; i++) c.lineTo(x0 + (x1 - x0) * (i + .5) / n, oy + (i % 2 ? -16 : 16)); c.lineTo(x1, oy); c.stroke();
    // damper
    c.strokeStyle = '#6b7599'; c.lineWidth = 2; c.beginPath(); c.moveTo(x0, oy + 52); c.lineTo(x0 + (x1 - x0) * .5, oy + 52); c.moveTo(x0 + (x1 - x0) * .4, oy + 42); c.lineTo(x0 + (x1 - x0) * .4, oy + 62); c.lineTo(x0 + (x1 - x0) * .62, oy + 62); c.moveTo(x0 + (x1 - x0) * .4, oy + 42); c.lineTo(x0 + (x1 - x0) * .62, oy + 42); c.moveTo(x0 + (x1 - x0) * .52, oy + 52); c.lineTo(x1, oy + 52); c.stroke();
    const g = c.createLinearGradient(bx, oy - 34, bx + 68, oy + 34); g.addColorStop(0, '#4f9bff'); g.addColorStop(1, '#a78bfa'); c.fillStyle = g; c.fillRect(bx, oy - 34, 68, 68);
    c.fillStyle = '#fff'; c.font = 'bold 13px system-ui'; c.textAlign = 'center'; c.fillText(P.m.toFixed(1) + ' kg', bx + 34, oy + 5);
    const F = P.F0 * Math.cos(P.wd * S.t); arrow(c, bx + 68, oy, bx + 68 + F * 5, oy, COL.am, 3); c.fillStyle = COL.am; c.textAlign = 'left'; c.fillText('F(t)', bx + 74 + Math.max(F * 5, 0), oy - 40);
    c.fillStyle = '#6b7599'; c.font = '12px system-ui'; c.textAlign = 'center'; c.fillText('equilibrium', ox, oy - 96);
    // resonance mini-curve
    const gw = Math.min(330, W - 40), gh = 120, gx = 24, gy = H - gh - 24, wmax = Math.max(15, w0 * 2.2), pts = []; let amx = 0;
    for (let i = 0; i <= 120; i++) { const w = .05 + (wmax - .05) * i / 120, a = this.amp(P, w); pts.push([w, a]); amx = Math.max(amx, a); } amx = Math.min(amx, 20);
    c.fillStyle = 'rgba(10,14,29,.75)'; c.fillRect(gx, gy, gw, gh); c.strokeStyle = COL.vi; c.lineWidth = 2; c.beginPath(); pts.forEach((p, i) => { const x = gx + p[0] / wmax * gw, y = gy + gh - 8 - Math.min(p[1], amx) / amx * (gh - 26); i ? c.lineTo(x, y) : c.moveTo(x, y); }); c.stroke();
    c.strokeStyle = 'rgba(251,191,36,.8)'; c.setLineDash([4, 4]); c.beginPath(); c.moveTo(gx + P.wd / wmax * gw, gy); c.lineTo(gx + P.wd / wmax * gw, gy + gh); c.stroke(); c.setLineDash([]);
    c.strokeStyle = 'rgba(74,222,128,.7)'; c.beginPath(); c.moveTo(gx + w0 / wmax * gw, gy); c.lineTo(gx + w0 / wmax * gw, gy + gh); c.stroke();
    c.fillStyle = '#8a93b8'; c.font = '11px system-ui'; c.textAlign = 'left'; c.fillText('steady-state amplitude vs drive frequency', gx + 6, gy + 13); c.fillStyle = COL.gr; c.fillText('ω₀', gx + w0 / wmax * gw + 4, gy + gh - 12); c.fillStyle = COL.am; c.fillText('ω', gx + P.wd / wmax * gw + 4, gy + 26);
  },
  hud(S, P) { const w0 = Math.sqrt(P.k / P.m), Q = P.c > 0 ? Math.sqrt(P.k * P.m) / P.c : Infinity; return hudRows([['t', fm(S.t) + ' s'], ['x', fm(S.x, 3) + ' m'], ['v', fm(S.v, 3) + ' m/s'], ['ω₀ (natural)', fm(w0) + ' rad/s'], ['Q factor', isFinite(Q) ? fm(Q, 1) : '∞'], ['steady amplitude', fm(this.amp(P), 3) + ' m']]); },
  sample(S, P) { const ke = .5 * P.m * S.v * S.v, pe = .5 * P.k * S.x * S.x; return { x: S.x, fd: P.F0 * Math.cos(P.wd * S.t) / P.k, v: S.v, ke, pe, e: ke + pe }; },
  plots: [
    { title: 'Displacement (m); dashed = F/k', series: [{ k: 'x', col: COL.cy, label: 'x' }, { k: 'fd', col: COL.am, label: 'F(t)/k', dash: true }] },
    { title: 'Velocity (m/s)', series: [{ k: 'v', col: COL.vi, label: 'v' }] },
    { title: 'Energy (J)', series: [{ k: 'ke', col: COL.am, label: 'kinetic' }, { k: 'pe', col: COL.pk, label: 'spring' }, { k: 'e', col: COL.gr, label: 'total' }] },
  ],
  scen: { 'Free decay (no drive)': { F0: 0, x0: 1, c: 0.3 }, 'Resonance (drive = ω₀)': { wd: 5, c: 0.3 }, 'Beats (drive near ω₀)': { wd: 4.5, c: 0.02, x0: 0 }, 'Far above resonance': { wd: 12 }, 'Heavily damped': { c: 4, F0: 0, x0: 1 }, 'Undamped, driven': { c: 0, wd: 4 } },
  theory(P, S) {
    const w0 = Math.sqrt(P.k / P.m), wm = Math.max(15, w0 * 2.2), z = P.c / (2 * Math.sqrt(P.k * P.m));
    return { title: 'Driven damped oscillator', intro: 'A mass on a spring with a damper and a sinusoidal driving force — the model behind bridges, circuits, tuning forks and radio receivers.',
      sections: [
        { h: 'Equation of motion', tex: [T`m\ddot{x} + c\,\dot{x} + k\,x = F_0\cos(\omega t)`, T`\omega_0 = \sqrt{k/m} \qquad \zeta = \dfrac{c}{2\sqrt{km}} \qquad Q = \dfrac{\sqrt{km}}{c}`], live: `ω₀ = ${fm(w0)} rad/s   ζ = ${fm(z, 3)}   ${z < 1 ? 'underdamped (oscillates)' : z === 1 ? 'critically damped' : 'overdamped'}` },
        { h: 'Steady-state response (resonance)', p: 'After the start-up transient dies out, the mass oscillates at the drive frequency with this amplitude. It peaks near the natural frequency; less damping gives a taller, sharper peak.', tex: [T`A(\omega) = \dfrac{F_0}{\sqrt{(k - m\omega^{2})^{2} + (c\,\omega)^{2}}} \qquad \tan\varphi = \dfrac{c\,\omega}{k - m\omega^{2}}`],
          svg: Theory.plot({ f: w => Math.min(this.amp(P, w), 12), xr: [0.05, wm], yr: [0, 12], xl: 'drive frequency ω (rad/s)', yl: 'amplitude (m)', vlines: [{ x: w0, col: COL.gr, label: 'ω₀' }], point: [P.wd, Math.min(this.amp(P), 12), 'now'], title: 'resonance curve' }) },
        { h: 'Transient + steady state', p: 'The full solution is the decaying free oscillation plus the steady response. The envelope of the free part decays as e^(−ζω₀t). Near resonance with light damping you see beats between the two.', tex: [T`x(t) = \underbrace{C e^{-\zeta\omega_0 t}\cos(\omega_d t + \phi)}_{\text{transient}} + \underbrace{A\cos(\omega t - \varphi)}_{\text{steady}}`] },
      ] };
  },
};

/* =====================================================================
   4. ORBITS
   ===================================================================== */
EXPS.orb = {
  name: 'Orbits & Kepler\'s laws', group: 'Mechanics', ts: 0.5, h: 0.004, win: 3, tu: 'yr', ld: 0.0025,
  params: [['M', 'Central mass', 0.2, 5, 0.1, 'M☉', 1, 0], ['r0', 'Start distance', 0.3, 3, 0.05, 'AU', 1, 1], ['vm', 'Speed vs circular', 0.45, 1.4, 0.01, '×', 0.8, 1]],
  GM(P) { return 39.4784 * P.M; },
  init(P) { const v = Math.sqrt(this.GM(P) / P.r0) * P.vm, S = { t: 0, x: P.r0, y: 0, vx: 0, vy: v, smp: [], lastS: -1 }; const m = this.inv(S, P); S.E0 = m.E; S.L0 = m.L; return S; },
  inv(S, P) { const GM = this.GM(P), r = Math.hypot(S.x, S.y), v2 = S.vx * S.vx + S.vy * S.vy; return { r, v: Math.sqrt(v2), E: .5 * v2 - GM / r, L: S.x * S.vy - S.y * S.vx }; },
  step(S, P, h) {
    const GM = this.GM(P); let rem = h, guard = 0;
    while (rem > 1e-12 && guard++ < 20000) {
      const r = Math.hypot(S.x, S.y), v = Math.hypot(S.vx, S.vy) || 1, dt = Math.min(rem, .01 * Math.min(r / v, Math.sqrt(r * r * r / GM)));
      const n = rk4(s => { const r3 = Math.pow(Math.hypot(s[0], s[1]), 3); return [s[2], s[3], -GM * s[0] / r3, -GM * s[1] / r3]; }, [S.x, S.y, S.vx, S.vy], dt);
      [S.x, S.y, S.vx, S.vy] = n; S.t += dt; rem -= dt;
      if (S.t - S.lastS >= 0.002) { S.lastS = S.t; S.smp.push([S.t, S.x, S.y]); if (S.smp.length > 4000) S.smp.shift(); }
    }
  },
  elements(S, P) { const GM = this.GM(P), m = this.inv(S, P), p = m.L * m.L / GM, e = Math.sqrt(Math.max(0, 1 + 2 * m.E * m.L * m.L / (GM * GM))), r = m.r, rv = S.x * S.vx + S.y * S.vy, v2 = m.v * m.v; const ex = ((v2 - GM / r) * S.x - rv * S.vx) / GM, ey = ((v2 - GM / r) * S.y - rv * S.vy) / GM; return { p, e, w: Math.atan2(ey, ex), a: m.E < 0 ? -GM / (2 * m.E) : Infinity, ...m }; },
  draw(c, S, P, W, H) {
    bg(c, W, H); const el = this.elements(S, P), R = el.e < 1 ? el.a * (1 + el.e) : P.r0 * 2.5, sc = (Math.min(W, H) / 2 - 36) / Math.max(R, P.r0, .5), ox = W / 2, oy = H / 2, X = x => ox + x * sc, Y = y => oy - y * sc;
    c.strokeStyle = 'rgba(255,255,255,.04)'; for (const r of [.5, 1, 2, 3, 4, 5]) { c.beginPath(); c.arc(ox, oy, r * sc, 0, TAU); c.stroke(); c.fillStyle = '#3d4876'; c.font = '10px system-ui'; c.textAlign = 'left'; if (r * sc < Math.min(W, H) / 2) c.fillText(r + ' AU', ox + r * sc + 3, oy - 3); }
    // equal-area wedges
    if (el.e < 1 && S.smp.length > 5) {
      const Tp = TAU * Math.sqrt(el.a ** 3 / this.GM(P)), tau = Tp / 12, nW = 12;
      for (let k = 0; k < nW; k++) { const t1 = S.t - k * tau, t0 = t1 - tau; if (t0 < S.smp[0][0]) break; c.fillStyle = `hsla(${200 + k * 12},80%,60%,${.28 - k * .018})`; c.beginPath(); c.moveTo(ox, oy); for (const p of S.smp) if (p[0] >= t0 && p[0] <= t1) c.lineTo(X(p[1]), Y(p[2])); c.closePath(); c.fill(); }
    }
    // analytic conic
    if (el.e < 1) { c.setLineDash([4, 6]); c.strokeStyle = 'rgba(167,139,250,.55)'; c.lineWidth = 1.4; c.beginPath(); for (let i = 0; i <= 160; i++) { const f = TAU * i / 160, r = el.p / (1 + el.e * Math.cos(f)), a = el.w + f; i ? c.lineTo(X(r * Math.cos(a)), Y(r * Math.sin(a))) : c.moveTo(X(r * Math.cos(a)), Y(r * Math.sin(a))); } c.stroke(); c.setLineDash([]); }
    c.strokeStyle = COL.cy; c.lineWidth = 2.2; c.beginPath(); const sm = S.smp.slice(-1200); sm.forEach((p, i) => i ? c.lineTo(X(p[1]), Y(p[2])) : c.moveTo(X(p[1]), Y(p[2]))); c.stroke();
    const gl = c.createRadialGradient(ox, oy, 2, ox, oy, 38); gl.addColorStop(0, '#fff7c2'); gl.addColorStop(.3, '#fbbf24'); gl.addColorStop(1, 'rgba(251,191,36,0)'); c.fillStyle = gl; c.beginPath(); c.arc(ox, oy, 38, 0, TAU); c.fill();
    c.fillStyle = '#fff8d6'; c.beginPath(); c.arc(ox, oy, 8 + P.M * 1.5, 0, TAU); c.fill();
    const px_ = X(S.x), py_ = Y(S.y); arrow(c, px_, py_, px_ + S.vx / 6.3 * 40, py_ - S.vy / 6.3 * 40, COL.gr, 2); c.shadowColor = COL.cy; c.shadowBlur = 12; c.fillStyle = '#7dd3fc'; c.beginPath(); c.arc(px_, py_, 6, 0, TAU); c.fill(); c.shadowBlur = 0;
    c.fillStyle = '#8a93b8'; c.font = '12px system-ui'; c.textAlign = 'right'; c.fillText('coloured wedges: equal time intervals → equal areas', W - 14, 22);
  },
  hud(S, P) { const el = this.elements(S, P), Tp = el.e < 1 ? TAU * Math.sqrt(el.a ** 3 / this.GM(P)) : NaN; return hudRows([['t', fm(S.t, 2) + ' yr'], ['distance', fm(el.r, 3) + ' AU'], ['speed', fm(el.v, 2) + ' AU/yr'], ['eccentricity', fm(el.e, 3)], ['period', isFinite(Tp) ? fm(Tp, 3) + ' yr' : 'unbound'], ['semi-major axis', isFinite(el.a) ? fm(el.a, 3) + ' AU' : '∞']]); },
  sample(S, P) { const m = this.inv(S, P); return { r: m.r, v: m.v, dE: (m.E - S.E0) / Math.abs(S.E0), dL: (m.L - S.L0) / Math.abs(S.L0) }; },
  plots: [
    { title: 'Distance from the Sun (AU)', series: [{ k: 'r', col: COL.cy, label: 'r' }] },
    { title: 'Speed (AU/yr)', series: [{ k: 'v', col: COL.am, label: 'v' }] },
    { title: 'Conservation: relative drift', series: [{ k: 'dE', col: COL.gr, label: 'ΔE/E' }, { k: 'dL', col: COL.vi, label: 'ΔL/L' }] },
  ],
  scen: { 'Earth (circular)': { M: 1, r0: 1, vm: 1 }, 'Comet-like ellipse': { vm: 0.5, r0: 2 }, 'Mild ellipse': { vm: 0.8 }, 'Heavy star (M = 4)': { M: 4, r0: 1, vm: 1 }, 'Faster than circular': { vm: 1.3 }, 'Near escape speed': { vm: 1.41 } },
  theory(P, S) {
    const el = this.elements(S, P), a0 = isFinite(el.a) ? el.a : 1, pts = [];
    return { title: 'Orbital mechanics', intro: 'A planet around a heavy star, in units of AU, years and solar masses where GM = 4π²·M.',
      sections: [
        { h: 'Newton\'s law of gravitation', tex: [T`\ddot{\mathbf r} = -\dfrac{GM}{r^{3}}\,\mathbf r \qquad GM = 4\pi^{2}\,M\ \ \text{(AU³/yr²)}`, T`v_{circ} = \sqrt{GM/r} \qquad v_{esc} = \sqrt{2GM/r} = \sqrt{2}\,v_{circ}`] },
        { h: "Kepler's three laws", tex: [T`\text{1. orbits are ellipses with the Sun at one focus:}\quad r = \dfrac{p}{1 + e\cos f},\ \ p = \dfrac{L^{2}}{GM}`, T`\text{2. equal areas in equal times:}\quad \dfrac{dA}{dt} = \tfrac12 L = \text{const}`, T`\text{3. } T^{2} = \dfrac{4\pi^{2}}{GM}\,a^{3} \quad\Rightarrow\quad T^{2}[\text{yr}] = a^{3}[\text{AU}]/M`],
          live: isFinite(el.a) ? `now: a = ${fm(el.a, 3)} AU, e = ${fm(el.e, 3)}, T = ${fm(TAU * Math.sqrt(el.a ** 3 / this.GM(P)), 3)} yr` : 'now: unbound (hyperbolic) orbit' },
        { h: 'Conserved quantities', p: 'Energy and angular momentum are constant. The bottom graph shows how well the numerical integrator keeps them: drift of 10⁻⁶ or less means the simulation is trustworthy (adaptive time steps shrink near the Sun).', tex: [T`E = \tfrac12 v^{2} - \dfrac{GM}{r} \qquad L = x\,v_y - y\,v_x \qquad e = \sqrt{1 + \dfrac{2EL^{2}}{(GM)^{2}}}`],
          svg: Theory.plot({ f: a => Math.sqrt(a * a * a / P.M), xr: [0.2, 5], xl: 'semi-major axis a (AU)', yl: 'period T (yr)', point: [Math.min(a0, 5), Math.sqrt(Math.min(a0, 5) ** 3 / P.M), 'now'], title: "Kepler's 3rd law" }) },
      ] };
  },
};

/* =====================================================================
   5. CHARGED PARTICLE IN E AND B
   ===================================================================== */
EXPS.lor = {
  name: 'Charged particle in E & B fields', group: 'Electromagnetism', ts: 1, h: 0.002, win: 12, tu: 's', ld: 0.02,
  params: [
    ['qm', 'Charge / mass q/m', -3, 3, 0.05, 'C/kg', 1, 0], ['B', 'Magnetic field B (⊙ +)', -4, 4, 0.05, 'T', 2, 0], ['Ex', 'Electric field Eₓ', -5, 5, 0.05, 'V/m', 0, 0], ['Ey', 'Electric field E_y', -5, 5, 0.05, 'V/m', 0, 0],
    ['v0', 'Start speed', 0, 10, 0.1, 'm/s', 5, 1], ['ang', 'Start direction', 0, 360, 1, '°', 90, 1],
  ],
  init(P) { const a = P.ang * D2R; return { t: 0, x: 0, y: 0, vx: P.v0 * Math.cos(a), vy: P.v0 * Math.sin(a), tr: [[0, 0]], n: 0, b: [0, 0, 0, 0], cam: [0, 0], half: 6, y0: 0 }; },
  step(S, P, h) {
    const q = P.qm, hh = h / 2; let vx = S.vx + q * P.Ex * hh, vy = S.vy + q * P.Ey * hh;                    // Boris pusher: half E kick
    const t = q * P.B * hh, s = 2 * t / (1 + t * t), wx = vx + vy * t, wy = vy - vx * t;                         // rotation by B (z axis)
    vx += wy * s; vy -= wx * s; vx += q * P.Ex * hh; vy += q * P.Ey * hh;
    S.vx = vx; S.vy = vy; S.x += vx * h; S.y += vy * h; S.t += h;
    if (++S.n % 4 === 0) { S.tr.push([S.x, S.y]); if (S.tr.length > 3000) S.tr.shift(); }
    S.b[0] = Math.min(S.b[0], S.x); S.b[1] = Math.max(S.b[1], S.x); S.b[2] = Math.min(S.b[2], S.y); S.b[3] = Math.max(S.b[3], S.y);
  },
  derived(P) { const sp = Math.hypot(...[P.v0 * Math.cos(P.ang * D2R), P.v0 * Math.sin(P.ang * D2R)]), wc = P.qm * P.B; return { wc, r: Math.abs(wc) > 1e-9 ? sp / Math.abs(wc) : Infinity, T: Math.abs(wc) > 1e-9 ? TAU / Math.abs(wc) : Infinity, drift: Math.abs(P.B) > 1e-9 ? [P.Ey / P.B, -P.Ex / P.B] : [0, 0] }; },
  draw(c, S, P, W, H) {
    bg(c, W, H); const bx = S.b, tx = (bx[0] + bx[1]) / 2, ty = (bx[2] + bx[3]) / 2, need = Math.max((bx[1] - bx[0]) / 2 * (H / W < 1 ? 1 : 1), (bx[3] - bx[2]) / 2 * W / H, 3) * 1.45;
    S.cam[0] += (tx - S.cam[0]) * .08; S.cam[1] += (ty - S.cam[1]) * .08; S.half += (Math.max(6, need) - S.half) * .06;
    const s = Math.min(H / 2, W / 2) / S.half, ox = W / 2 - S.cam[0] * s, oy = H / 2 + S.cam[1] * s, X = x => ox + x * s, Y = y => oy - y * s;
    // B symbols
    const sp = [1, 2, 4, 8, 16, 32].find(g => g * s > 54) || 64; c.strokeStyle = c.fillStyle = P.B > 0 ? 'rgba(96,165,250,.35)' : 'rgba(244,114,182,.35)'; c.lineWidth = 1.4;
    if (Math.abs(P.B) > 1e-6) for (let gx = Math.floor((S.cam[0] - W / 2 / s) / sp) * sp; gx < S.cam[0] + W / 2 / s + sp; gx += sp) for (let gy = Math.floor((S.cam[1] - H / 2 / s) / sp) * sp; gy < S.cam[1] + H / 2 / s + sp; gy += sp) {
      const x = X(gx), y = Y(gy); c.beginPath(); c.arc(x, y, 6, 0, TAU); c.stroke();
      if (P.B > 0) { c.beginPath(); c.arc(x, y, 1.8, 0, TAU); c.fill(); } else { c.beginPath(); c.moveTo(x - 3.5, y - 3.5); c.lineTo(x + 3.5, y + 3.5); c.moveTo(x + 3.5, y - 3.5); c.lineTo(x - 3.5, y + 3.5); c.stroke(); }
    }
    // E arrows
    if (Math.hypot(P.Ex, P.Ey) > 1e-6) { const sp2 = sp * 2, L = Math.min(34, 10 + Math.hypot(P.Ex, P.Ey) * 5), a = Math.atan2(P.Ey, P.Ex); for (let gx = Math.floor((S.cam[0] - W / 2 / s) / sp2) * sp2 + sp / 2; gx < S.cam[0] + W / 2 / s; gx += sp2) for (let gy = Math.floor((S.cam[1] - H / 2 / s) / sp2) * sp2 + sp / 2; gy < S.cam[1] + H / 2 / s; gy += sp2) arrow(c, X(gx) - L / 2 * Math.cos(a), Y(gy) + L / 2 * Math.sin(a), X(gx) + L / 2 * Math.cos(a), Y(gy) - L / 2 * Math.sin(a), 'rgba(251,191,36,.35)', 1.6); }
    c.strokeStyle = COL.cy; c.lineWidth = 2.4; c.lineJoin = 'round'; c.beginPath(); S.tr.forEach((p, i) => i ? c.lineTo(X(p[0]), Y(p[1])) : c.moveTo(X(p[0]), Y(p[1]))); c.lineTo(X(S.x), Y(S.y)); c.stroke();
    const d = this.derived(P); if (Math.hypot(P.Ex, P.Ey) < 1e-6 && isFinite(d.r) && S.n < 2) { /* hint circle drawn by trail */ }
    const fx = P.qm * (P.Ex + S.vy * P.B), fy = P.qm * (P.Ey - S.vx * P.B), pxx = X(S.x), pyy = Y(S.y);
    arrow(c, pxx, pyy, pxx + S.vx * s * .25, pyy - S.vy * s * .25, COL.gr, 2.4); arrow(c, pxx, pyy, pxx + fx * s * .25, pyy - fy * s * .25, COL.pk, 2.4);
    c.shadowColor = P.qm >= 0 ? '#f87171' : '#60a5fa'; c.shadowBlur = 14; c.fillStyle = P.qm >= 0 ? '#f87171' : '#60a5fa'; c.beginPath(); c.arc(pxx, pyy, 7, 0, TAU); c.fill(); c.shadowBlur = 0;
    c.fillStyle = '#fff'; c.font = 'bold 11px system-ui'; c.textAlign = 'center'; c.fillText(P.qm >= 0 ? '+' : '−', pxx, pyy + 4);
    c.font = '12px system-ui'; c.textAlign = 'right'; c.fillStyle = COL.gr; c.fillText('velocity', W - 14, 22); c.fillStyle = COL.pk; c.fillText('force q(E + v × B)', W - 14, 40);
  },
  hud(S, P) { const d = this.derived(P), sp = Math.hypot(S.vx, S.vy); return hudRows([['t', fm(S.t) + ' s'], ['position', `${fm(S.x)}, ${fm(S.y)} m`], ['speed', fm(sp, 3) + ' m/s'], ['cyclotron radius', isFinite(d.r) ? fm(d.r, 3) + ' m' : '∞'], ['period', isFinite(d.T) ? fm(d.T, 3) + ' s' : '∞'], ['E×B drift', `${fm(d.drift[0], 2)}, ${fm(d.drift[1], 2)} m/s`]]); },
  sample(S, P) { const sp = Math.hypot(S.vx, S.vy); return { x: S.x, y: S.y, vx: S.vx, vy: S.vy, sp, ke: .5 * sp * sp }; },
  plots: [
    { title: 'Position (m)', series: [{ k: 'x', col: COL.cy, label: 'x' }, { k: 'y', col: COL.vi, label: 'y' }] },
    { title: 'Velocity (m/s)', series: [{ k: 'vx', col: COL.cy, label: 'vx' }, { k: 'vy', col: COL.vi, label: 'vy' }, { k: 'sp', col: COL.am, label: 'speed' }] },
    { title: 'Kinetic energy per unit mass (J/kg)', series: [{ k: 'ke', col: COL.gr, label: '½v²' }] },
  ],
  scen: { 'Cyclotron circle (B only)': { Ex: 0, Ey: 0, B: 2, qm: 1 }, 'Opposite charge turns the other way': { qm: -1, B: 2 }, 'E × B drift (cycloid)': { Ex: 2, Ey: 0, B: 2, v0: 0 }, 'Electric field only: parabola': { B: 0, Ey: 2, v0: 4, ang: 0 }, 'Helix drift: E ∥ B plane': { Ex: 0, Ey: 1, B: 1.5, v0: 3, ang: 0 }, 'Strong field, tight loops': { B: 4, qm: 3, v0: 4 } },
  theory(P, S) {
    const d = this.derived(P), Bs = [];
    return { title: 'Lorentz force', intro: 'A charged particle in electric and magnetic fields. The magnetic force does no work: it only turns the particle.',
      sections: [
        { h: 'Force and equation of motion', tex: [T`\mathbf F = q\,(\mathbf E + \mathbf v \times \mathbf B) \qquad \dot{\mathbf v} = \dfrac{q}{m}\,(\mathbf E + \mathbf v\times\mathbf B)`, T`\text{with } \mathbf B = B\hat{\mathbf z}:\quad \dot v_x = \tfrac{q}{m}(E_x + v_y B) \qquad \dot v_y = \tfrac{q}{m}(E_y - v_x B)`] },
        { h: 'Pure magnetic field: circles', tex: [T`r = \dfrac{m v}{|q| B} \qquad \omega_c = \dfrac{|q| B}{m} \qquad T = \dfrac{2\pi m}{|q| B}`], live: `now: r = ${isFinite(d.r) ? fm(d.r, 3) + ' m' : '∞'}, period = ${isFinite(d.T) ? fm(d.T, 3) + ' s' : '∞'}`,
          svg: Theory.plot({ f: B => Math.abs(B) > 0.05 ? Math.hypot(P.v0 * Math.cos(P.ang * D2R), P.v0 * Math.sin(P.ang * D2R)) / Math.abs(P.qm * B) : NaN, xr: [0.1, 4], yr: [0, 10], xl: 'B (tesla)', yl: 'radius (m)', point: [Math.abs(P.B), Math.min(10, d.r), 'now'], title: 'stronger field → tighter circle' }) },
        { h: 'Crossed fields: E × B drift', p: 'When E and B are both present the particle circles while drifting sideways at a speed independent of its charge and mass — used in mass spectrometers and plasma confinement.', tex: [T`\mathbf v_d = \dfrac{\mathbf E \times \mathbf B}{B^{2}}`], live: `now: drift = (${fm(d.drift[0], 2)}, ${fm(d.drift[1], 2)}) m/s` },
        { h: 'The numerical method', p: 'The simulator uses the Boris pusher: half an electric kick, an exact rotation by the magnetic field, then another half kick. It keeps the speed constant in a pure magnetic field to machine precision — look at the flat energy graph.', tex: [T`\mathbf v^- = \mathbf v_n + \tfrac{q}{m}\mathbf E\tfrac{h}{2},\quad \mathbf v^+ = \text{rotate}(\mathbf v^-,\ \omega_c h),\quad \mathbf v_{n+1} = \mathbf v^+ + \tfrac{q}{m}\mathbf E\tfrac{h}{2}`] },
      ] };
  },
};

/* =====================================================================
   6. ELECTRIC FIELD SANDBOX
   ===================================================================== */
EXPS.ef = {
  name: 'Electric field sandbox', group: 'Electromagnetism', ts: 1, h: 0.002, win: 10, tu: 's', ld: 0.01,
  params: [['qt', 'Test charge', -2, 2, 0.05, 'C', 1, 0], ['mt', 'Test mass', 0.1, 5, 0.1, 'kg', 1, 0], ['drag', 'Drag', 0, 2, 0.02, '1/s', 0.05, 0], ['eps', 'Softening', 0.05, 0.5, 0.01, 'm', 0.15, 0]],
  init(P, ex) {
    const e = ex || { charges: [[-1.5, 0, 1], [1.5, 0, -1]] };
    return { t: 0, ch: e.charges.map(a => ({ x: a[0], y: a[1], q: a[2] })), tp: e.tp ? { ...e.tp, on: true } : { on: false, x: 0, y: 0, vx: 0, vy: 0 }, sel: -1, aim: null, dirty: true, map: null, mapKey: '' };
  },
  save(S) { return { charges: S.ch.map(c => [c.x, c.y, c.q]), tp: S.tp.on ? { x: S.tp.x, y: S.tp.y, vx: 0, vy: 0 } : null }; },
  phi(S, P, x, y) { let v = 0; for (const c of S.ch) v += c.q / Math.sqrt((x - c.x) ** 2 + (y - c.y) ** 2 + P.eps * P.eps); return v; },
  field(S, P, x, y) { let ex = 0, ey = 0; for (const c of S.ch) { const dx = x - c.x, dy = y - c.y, r2 = dx * dx + dy * dy + P.eps * P.eps, k = c.q / (r2 * Math.sqrt(r2)); ex += k * dx; ey += k * dy; } return [ex, ey]; },
  step(S, P, h) {
    const p = S.tp; if (!p.on || S.aim) return; S.t += h;
    const n = rk4(s => { const E = this.field(S, P, s[0], s[1]); return [s[2], s[3], P.qt / P.mt * E[0] - P.drag * s[2], P.qt / P.mt * E[1] - P.drag * s[3]]; }, [p.x, p.y, p.vx, p.vy], h);
    [p.x, p.y, p.vx, p.vy] = n; if (Math.abs(p.x) > 60 || Math.abs(p.y) > 60) { p.on = false; }
  },
  view: { s: 80, ox: 0, oy: 0 },
  draw(c, S, P, W, H) {
    bg(c, W, H); const v = this.view; v.s = H / 10; v.ox = W / 2; v.oy = H / 2; const s = v.s, X = x => v.ox + x * s, Y = y => v.oy - y * s;
    // potential map
    const key = W + 'x' + H; if (S.dirty || S.mapKey !== key) { S.dirty = false; S.mapKey = key; this.buildMap(S, P, W, H); }
    if (S.map) { c.globalAlpha = .75; c.imageSmoothingEnabled = true; c.drawImage(S.map, 0, 0, W, H); c.globalAlpha = 1; }
    // field lines
    const wx = W / 2 / s + 1, wy = H / 2 / s + 1; c.lineWidth = 1.2;
    const pos = S.ch.filter(q => q.q > 0), neg = S.ch.filter(q => q.q < 0), seeds = pos.length ? pos : neg, dir = pos.length ? 1 : -1;
    for (const q of seeds) {
      const n = Math.min(32, 8 + Math.round(Math.abs(q.q) * 8));
      for (let i = 0; i < n; i++) {
        const a = TAU * i / n + .1; let x = q.x + .14 * Math.cos(a), y = q.y + .14 * Math.sin(a); const pts = [[x, y]];
        for (let k = 0; k < 700; k++) { const E = this.field(S, P, x, y), m = Math.hypot(E[0], E[1]); if (m < 1e-7) break; const st = .05; x += dir * E[0] / m * st; y += dir * E[1] / m * st; pts.push([x, y]); if (Math.abs(x) > wx || Math.abs(y) > wy) break; if (S.ch.some(o => o !== q && o.q * q.q < 0 && Math.hypot(x - o.x, y - o.y) < .14)) break; }
        c.strokeStyle = 'rgba(226,232,255,.5)'; c.beginPath(); pts.forEach((p, j) => j ? c.lineTo(X(p[0]), Y(p[1])) : c.moveTo(X(p[0]), Y(p[1]))); c.stroke();
        for (let j = 30; j < pts.length - 2; j += 70) { const a0 = pts[j], a1 = pts[j + 1]; const ang = Math.atan2(-(a1[1] - a0[1]) * dir, (a1[0] - a0[0]) * dir) * 1; const mx = X(a0[0]), my = Y(a0[1]), d = dir; const th = Math.atan2(-(a1[1] - a0[1]), a1[0] - a0[0]) + (d < 0 ? Math.PI : 0); c.fillStyle = 'rgba(226,232,255,.75)'; c.beginPath(); c.moveTo(mx + 6 * Math.cos(th), my + 6 * Math.sin(th)); c.lineTo(mx + 6 * Math.cos(th + 2.5), my + 6 * Math.sin(th + 2.5)); c.lineTo(mx + 6 * Math.cos(th - 2.5), my + 6 * Math.sin(th - 2.5)); c.fill(); }
      }
    }
    // charges
    S.ch.forEach((q, i) => { const r = 10 + Math.min(16, Math.abs(q.q) * 6); c.shadowColor = q.q > 0 ? '#f87171' : '#60a5fa'; c.shadowBlur = i === S.sel ? 22 : 10; c.fillStyle = q.q > 0 ? '#ef4444' : '#3b82f6'; c.beginPath(); c.arc(X(q.x), Y(q.y), r, 0, TAU); c.fill(); c.shadowBlur = 0; c.lineWidth = i === S.sel ? 3 : 1.5; c.strokeStyle = i === S.sel ? '#fbbf24' : '#fff'; c.stroke(); c.fillStyle = '#fff'; c.font = 'bold 12px system-ui'; c.textAlign = 'center'; c.fillText((q.q > 0 ? '+' : '−') + Math.abs(q.q).toFixed(q.q % 1 ? 1 : 0), X(q.x), Y(q.y) + 4); });
    const p = S.tp;
    if (p.on || S.aim) {
      const tx = S.aim ? S.aim.x0 : p.x, ty = S.aim ? S.aim.y0 : p.y;
      if (S.aim) arrow(c, X(tx), Y(ty), X(S.aim.x1), Y(S.aim.y1), COL.gr, 2.5);
      else { c.strokeStyle = 'rgba(251,191,36,.7)'; c.lineWidth = 2; c.beginPath(); S.trail = S.trail || []; S.trail.forEach((q, i) => i ? c.lineTo(X(q[0]), Y(q[1])) : c.moveTo(X(q[0]), Y(q[1]))); c.stroke(); arrow(c, X(p.x), Y(p.y), X(p.x) + p.vx * s * .25, Y(p.y) - p.vy * s * .25, COL.gr, 2); }
      c.shadowColor = '#fbbf24'; c.shadowBlur = 12; c.fillStyle = '#fde68a'; c.beginPath(); c.arc(X(tx), Y(ty), 6, 0, TAU); c.fill(); c.shadowBlur = 0; c.fillStyle = '#1b1530'; c.font = 'bold 10px system-ui'; c.textAlign = 'center'; c.fillText(P.qt >= 0 ? '+' : '−', X(tx), Y(ty) + 3.5);
    }
    c.fillStyle = '#8a93b8'; c.font = '12px system-ui'; c.textAlign = 'right'; c.fillText('drag charges · click empty space and drag to launch a test charge', W - 14, 22);
    // trail maintenance
    if (p.on && !S.aim) { S.trail = S.trail || []; const l = S.trail[S.trail.length - 1]; if (!l || Math.hypot(l[0] - p.x, l[1] - p.y) > .04) { S.trail.push([p.x, p.y]); if (S.trail.length > 900) S.trail.shift(); } }
  },
  buildMap(S, P, W, H) {
    const w = Math.ceil(W / 5), h = Math.ceil(H / 5), cvs = S.map && S.map.width === w && S.map.height === h ? S.map : document.createElement('canvas'); cvs.width = w; cvs.height = h;
    const g = cvs.getContext('2d'), img = g.createImageData(w, h), s = this.view.s;
    for (let j = 0; j < h; j++) for (let i = 0; i < w; i++) {
      const x = ((i + .5) * 5 - W / 2) / s, y = (H / 2 - (j + .5) * 5) / s, V = this.phi(S, P, x, y), t = Math.max(-1, Math.min(1, Math.asinh(V * 1.4) / 2.6)), a = Math.pow(Math.abs(t), .75), band = Math.floor(V / .5) & 1 ? 1.1 : 1;
      const col = t > 0 ? [239, 68, 68] : [59, 130, 246], k = (j * w + i) * 4;
      img.data[k] = Math.min(255, (12 + (col[0] - 12) * a) * band); img.data[k + 1] = Math.min(255, (16 + (col[1] - 16) * a) * band); img.data[k + 2] = Math.min(255, (36 + (col[2] - 36) * a) * band); img.data[k + 3] = 255;
    }
    g.putImageData(img, 0, 0); S.map = cvs;
  },
  hud(S, P) { const p = S.tp, rows = [['charges', S.ch.length], ['net charge', fm(S.ch.reduce((a, c) => a + c.q, 0), 1) + ' C']]; if (p.on) { const E = this.field(S, P, p.x, p.y); rows.push(['|E| at test', fm(Math.hypot(...E), 2) + ' N/C'], ['potential', fm(this.phi(S, P, p.x, p.y), 2) + ' V'], ['speed', fm(Math.hypot(p.vx, p.vy), 2) + ' m/s']); } return hudRows(rows); },
  sample(S, P) { const p = S.tp; if (!p.on) return { V: 0, ke: 0, pe: 0, e: 0, sp: 0 }; const V = this.phi(S, P, p.x, p.y), sp = Math.hypot(p.vx, p.vy), ke = .5 * P.mt * sp * sp, pe = P.qt * V; return { V, ke, pe, e: ke + pe, sp }; },
  plots: [
    { title: 'Potential at the test charge (V)', series: [{ k: 'V', col: COL.vi, label: 'V' }] },
    { title: 'Energy of test charge (J)', series: [{ k: 'ke', col: COL.am, label: 'kinetic' }, { k: 'pe', col: COL.pk, label: 'potential' }, { k: 'e', col: COL.gr, label: 'total' }] },
    { title: 'Speed (m/s)', series: [{ k: 'sp', col: COL.cy, label: 'speed' }] },
  ],
  buttons: [
    { label: '+ Positive charge', fn(S) { S.ch.push({ x: (Math.random() - .5) * 4, y: (Math.random() - .5) * 4, q: 1 }); S.sel = S.ch.length - 1; S.dirty = true; } },
    { label: '− Negative charge', fn(S) { S.ch.push({ x: (Math.random() - .5) * 4, y: (Math.random() - .5) * 4, q: -1 }); S.sel = S.ch.length - 1; S.dirty = true; } },
    { label: 'Selected: stronger (+0.5)', fn(S) { const c = S.ch[S.sel]; if (c) { c.q += c.q >= 0 ? .5 : -.5; S.dirty = true; } } },
    { label: 'Selected: weaker (−0.5)', fn(S) { const c = S.ch[S.sel]; if (c) { const n = Math.abs(c.q) - .5; if (n < .25) S.ch.splice(S.sel, 1), S.sel = -1; else c.q = Math.sign(c.q) * n; S.dirty = true; } } },
    { label: 'Delete selected', fn(S) { if (S.sel >= 0) { S.ch.splice(S.sel, 1); S.sel = -1; S.dirty = true; } } },
    { label: 'Remove test charge', fn(S) { S.tp.on = false; S.trail = []; } },
  ],
  pointer(kind, x, y, S, P) {
    const v = this.view, s = v.s, wx = (x - v.ox) / s, wy = (v.oy - y) / s;
    if (kind === 'down') {
      const i = S.ch.findIndex(c => Math.hypot(c.x - wx, c.y - wy) < (14 + Math.abs(c.q) * 6) / s + .05);
      if (i >= 0) { S.sel = i; S.drag = i; S.dirty = true; } else { S.sel = -1; S.aim = { x0: wx, y0: wy, x1: wx, y1: wy }; S.trail = []; S.tp.on = false; }
    } else if (kind === 'move') {
      if (S.drag >= 0 && S.drag != null) { S.ch[S.drag].x = wx; S.ch[S.drag].y = wy; S.dirty = true; } else if (S.aim) { S.aim.x1 = wx; S.aim.y1 = wy; }
    } else if (kind === 'up') {
      if (S.aim) { const a = S.aim; S.tp = { on: true, x: a.x0, y: a.y0, vx: (a.x1 - a.x0) * 1.5, vy: (a.y1 - a.y0) * 1.5 }; S.aim = null; }
      S.drag = null;
    }
  },
  scen: {
    'Dipole': { ex: { charges: [[-1.5, 0, 1], [1.5, 0, -1]] } },
    'Two like charges': { ex: { charges: [[-1.5, 0, 1], [1.5, 0, 1]] } },
    'Quadrupole': { ex: { charges: [[-1.5, -1.5, 1], [1.5, 1.5, 1], [-1.5, 1.5, -1], [1.5, -1.5, -1]] } },
    'Parallel plates (uniform field)': { ex: { charges: [-4, -3, -2, -1, 0, 1, 2, 3, 4].flatMap(x => [[x * .7, 2.2, 0.5], [x * .7, -2.2, -0.5]]), tp: { x: -1, y: -1.5, vx: 0, vy: 0 } } },
    'Rutherford scattering': { p: { qt: 1, mt: 1 }, ex: { charges: [[0, 0, 3]], tp: { x: -6, y: 0.9, vx: 6, vy: 0 } } },
    'Orbiting a charge': { p: { qt: -1, mt: 1, drag: 0 }, ex: { charges: [[0, 0, 3]], tp: { x: 2, y: 0, vx: 0, vy: 1.7 } } },
    'Charged line': { ex: { charges: [-5, -4, -3, -2, -1, 0, 1, 2, 3, 4, 5].map(x => [x * .6, 0, 0.5]) } },
  },
  theory(P, S) {
    const p = S.tp;
    return { title: 'Electric fields & potential', intro: 'Point charges (k = 1 in these units). Drag charges around, add more, and fire a test charge through the field.',
      sections: [
        { h: "Coulomb's law and the field", tex: [T`\mathbf F = k\,\dfrac{q_1 q_2}{r^{2}}\,\hat{\mathbf r} \qquad \mathbf E = \sum_i k\,\dfrac{q_i}{r_i^{2}}\,\hat{\mathbf r}_i \qquad \mathbf F = q\,\mathbf E`], p: 'Like charges repel, opposite charges attract. Field lines start on positive charges and end on negative ones; where they crowd together the field is stronger.' },
        { h: 'Electric potential (the coloured map)', p: 'Potential is energy per unit charge. Red is positive, blue negative; the bands are equipotential surfaces. Field lines always cross them at right angles and point downhill.', tex: [T`V = \sum_i \dfrac{k\,q_i}{r_i} \qquad \mathbf E = -\nabla V`],
          svg: Theory.plot({ f: x => Math.max(-6, Math.min(6, this.phi(S, P, x, 0))), xr: [-5, 5], yr: [-6, 6], xl: 'x along y = 0 (m)', yl: 'V (volts)', title: 'potential along the x axis', point: p.on ? [p.x, this.phi(S, P, p.x, p.y), 'test'] : undefined }) },
        { h: 'Motion of the test charge', p: 'The test charge feels F = qE. Without drag its total energy stays constant: kinetic energy rises exactly as potential energy falls (see the energy graph). Rutherford scattering is the same physics that revealed the atomic nucleus.', tex: [T`m\,\ddot{\mathbf r} = q\,\mathbf E(\mathbf r) - \gamma m\,\dot{\mathbf r} \qquad \tfrac12 m v^{2} + qV = \text{const}\ \ (\gamma = 0)`], live: 'Softening ε keeps the field finite at a charge: r² → r² + ε².' },
      ] };
  },
};

/* =====================================================================
   FRAMEWORK
   ===================================================================== */
const CAP = 6000;
let E, P, S, running = true, curId = 'proj', scenName = '', log, logN, lastLog;
const side = $('#side');

function defaults(e) { const p = {}; e.params.forEach(a => p[a[0]] = a[6]); return p; }
function allKeys(e) { const ks = []; e.plots.forEach(r => r.series.forEach(s => { if (!ks.includes(s.k)) ks.push(s.k); })); return ks; }
function resetLog() { log = { t: new Float32Array(CAP), k: {} }; allKeys(E).forEach(k => log.k[k] = new Float32Array(CAP)); logN = 0; lastLog = -1e9; }
function startRun(extra) { S = E.init(P, extra); resetLog(); running = true; $('#bRun').textContent = 'Pause'; }
function selectExp(id, sc) {
  curId = id; E = EXPS[id]; $('#exp').value = id; P = defaults(E); let extra = null;
  if (sc && E.scen[sc]) { const o = E.scen[sc]; if (o.ex) { extra = o.ex; Object.assign(P, o.p || {}); } else Object.assign(P, o); }
  scenName = sc || ''; buildSide(); fillScen(); startRun(extra); persist();
}
function fillScen() { const s = $('#scen'); s.innerHTML = ''; s.add(new Option('— Experiment scenarios —', '')); Object.keys(E.scen).forEach(k => s.add(new Option(k, k))); s.value = scenName; }
function buildSide() {
  let h = `<h4>${E.name}</h4>`;
  E.params.forEach(a => { h += `<div class="row"><label>${a[1]}</label><input type="range" id="p_${a[0]}" min="${a[2]}" max="${a[3]}" step="${a[4]}" value="${P[a[0]]}"><output id="o_${a[0]}"></output></div>`; });
  if (E.buttons) { h += '<h4>Actions</h4>'; E.buttons.forEach((b, i) => h += `<button class="btn" data-b="${i}" style="display:block;width:100%;margin:4px 0">${b.label}</button>`); }
  h += `<p style="color:var(--muted);font-size:12px;margin-top:14px">Slow down or speed up with the speed menu. Press <b>Theory</b> for the equations behind this experiment.</p>`;
  side.innerHTML = h;
  E.params.forEach(a => { const el = $('#p_' + a[0]); const out = () => $('#o_' + a[0]).textContent = (Number.isInteger(a[4]) ? (+P[a[0]]).toFixed(0) : (+P[a[0]]).toFixed(a[4] < 0.001 ? 4 : a[4] < 0.01 ? 3 : 2).replace(/0+$/, '').replace(/\.$/, '')) + ' ' + a[5]; out();
    el.oninput = () => { P[a[0]] = parseFloat(el.value); out(); if (a[7]) startRun(S && E.save ? E.save(S) : null); else if (S) S.dirty = true; persist(); }; });
  side.querySelectorAll('[data-b]').forEach(b => b.onclick = () => { E.buttons[+b.dataset.b].fn(S, P); });
}
function setHtml() { }
function record() { const k = logN % CAP, smp = E.sample(S, P); log.t[k] = S.t; for (const key in log.k) log.k[key][k] = smp[key] || 0; logN++; lastLog = S.t; }
function advance(dt) {
  const sim = Math.min(dt, 0.05) * parseFloat($('#speed').value) * E.ts, n = Math.max(1, Math.ceil(sim / E.h)), h = sim / n;
  for (let i = 0; i < n; i++) { E.step(S, P, h); if (S.t - lastLog >= E.ld) record(); }
}

/* ---- plots ---- */
function drawPlots() {
  const [W, Hh] = fitCanvas(pl, px), c = px; c.clearRect(0, 0, W, Hh);
  const n = Math.min(logN, CAP), start = logN - n, idx = k => (start + k) % CAP, rows = E.plots, L = 52, R = 10, gap = 8, rh = (Hh - gap * (rows.length + 1) - 10) / rows.length;
  c.font = '11px system-ui';
  rows.forEach((r, ri) => {
    const y0 = gap + ri * (rh + gap), pw = W - L - R; c.fillStyle = 'rgba(255,255,255,.025)'; c.fillRect(L, y0, pw, rh); c.fillStyle = '#8a93b8'; c.textAlign = 'left'; c.fillText(r.title, L + 6, y0 + 12);
    let lx = L + pw - 6; c.textAlign = 'right'; for (let i = r.series.length - 1; i >= 0; i--) { const s = r.series[i]; c.fillStyle = s.col; c.fillText(s.label, lx, y0 + 12); lx -= c.measureText(s.label).width + 12; }
    if (n < 2) return;
    const tEnd = log.t[idx(n - 1)], t0 = Math.max(0, tEnd - E.win); let k0 = 0; while (k0 < n - 1 && log.t[idx(k0)] < t0) k0++;
    let lo = 1e30, hi = -1e30; for (const s of r.series) for (let k = k0; k < n; k++) { const v = log.k[s.k][idx(k)]; if (v < lo) lo = v; if (v > hi) hi = v; }
    if (!(hi > lo)) { lo -= 1; hi += 1; } const pad = (hi - lo) * .12; lo -= pad; hi += pad;
    const span = Math.max(E.win, tEnd - t0), X = t => L + (t - t0) / span * pw, Y = v => y0 + rh - 4 - (v - lo) / (hi - lo) * (rh - 20);
    c.strokeStyle = 'rgba(255,255,255,.06)'; c.fillStyle = '#6b7599'; c.textAlign = 'right';
    for (let g = 0; g <= 3; g++) { const v = lo + (hi - lo) * g / 3, yy = Y(v); c.beginPath(); c.moveTo(L, yy); c.lineTo(L + pw, yy); c.stroke(); c.fillText(Theory.fmt(v), L - 5, yy + 3); }
    if (ri === rows.length - 1) { c.textAlign = 'center'; for (const tv of Theory.nice(t0, t0 + span, 6)) c.fillText(Theory.fmt(tv) + (tv === t0 ? '' : ''), X(tv), y0 + rh + 12); c.textAlign = 'right'; c.fillText('time (' + E.tu + ')', W - 12, y0 + rh + 12); }
    c.save(); c.beginPath(); c.rect(L, y0, pw, rh); c.clip();
    for (const s of r.series) { c.strokeStyle = s.col; c.lineWidth = s.dash ? 1.4 : 1.8; c.setLineDash(s.dash ? [4, 4] : []); c.beginPath(); for (let k = k0; k < n; k++) { const xx = X(log.t[idx(k)]), yy = Y(log.k[s.k][idx(k)]); k === k0 ? c.moveTo(xx, yy) : c.lineTo(xx, yy); } c.stroke(); }
    c.restore(); c.setLineDash([]);
  });
}

/* ---- UI wiring ---- */
const groups = {}; Object.keys(EXPS).forEach(id => (groups[EXPS[id].group] = groups[EXPS[id].group] || []).push(id));
for (const g in groups) { const og = document.createElement('optgroup'); og.label = g; groups[g].forEach(id => og.appendChild(new Option(EXPS[id].name, id))); $('#exp').appendChild(og); }
$('#exp').onchange = e => selectExp(e.target.value);
$('#scen').onchange = e => { if (e.target.value) selectExp(curId, e.target.value); };
$('#bRun').onclick = () => { running = !running; $('#bRun').textContent = running ? 'Pause' : 'Run'; };
$('#bReset').onclick = () => { startRun(S && E.save && curId === 'ef' ? E.save(S) : null); };
$('#bTheory').onclick = () => Theory.open(E.theory(P, S));
function setStatus() { const s = $('#status'); let cls = 'ok', txt = running ? 'Running' : 'Paused'; if (curId === 'proj' && S.done) { cls = 'warn'; txt = 'Landed — press Reset to fire again'; } s.className = 'pill ' + cls; s.textContent = txt; }

cv.onpointerdown = e => { if (E.pointer) { cv.setPointerCapture(e.pointerId); const r = cv.getBoundingClientRect(); E.pointer('down', e.clientX - r.left, e.clientY - r.top, S, P); } };
cv.onpointermove = e => { if (E.pointer) { const r = cv.getBoundingClientRect(); E.pointer('move', e.clientX - r.left, e.clientY - r.top, S, P); } };
cv.onpointerup = e => { if (E.pointer) { const r = cv.getBoundingClientRect(); E.pointer('up', e.clientX - r.left, e.clientY - r.top, S, P); } };

/* ---- save / load / CSV ---- */
const snapshot = () => ({ lab: 'physics', v: 1, exp: curId, P, extra: E.save ? E.save(S) : null });
function persist() { try { localStorage.setItem('physics.v1', JSON.stringify(snapshot())); } catch (e) { } }
function download(name, text, type) { const a = document.createElement('a'); a.href = URL.createObjectURL(new Blob([text], { type })); a.download = name; a.click(); URL.revokeObjectURL(a.href); }
function toast(m) { const e = $('#toast'); e.textContent = m; e.classList.add('show'); clearTimeout(toast.t); toast.t = setTimeout(() => e.classList.remove('show'), 1800); }
function applySnap(o) { curId = o.exp in EXPS ? o.exp : 'proj'; E = EXPS[curId]; $('#exp').value = curId; P = { ...defaults(E), ...o.P }; scenName = ''; buildSide(); fillScen(); startRun(o.extra); }
$('#bSave').onclick = () => { download(`physics-${curId}.json`, JSON.stringify(snapshot(), null, 1), 'application/json'); toast('Setup saved'); };
$('#bLoad').onclick = () => $('#file').click();
$('#file').onchange = e => { const f = e.target.files[0]; if (!f) return; const r = new FileReader(); r.onload = () => { try { const o = JSON.parse(r.result); if (o.lab !== 'physics') throw 0; applySnap(o); toast('Setup loaded'); } catch (x) { toast('Not a Physics Lab file'); } }; r.readAsText(f); e.target.value = ''; };
$('#bCsv').onclick = () => {
  if (logN < 2) return toast('Run the experiment first');
  const keys = Object.keys(log.k), n = Math.min(logN, CAP), st = logN - n, rows = ['t,' + keys.join(',')];
  for (let k = 0; k < n; k++) { const j = (st + k) % CAP; rows.push(log.t[j].toPrecision(7) + ',' + keys.map(q => log.k[q][j].toPrecision(6)).join(',')); }
  download(`physics-${curId}.csv`, rows.join('\n'), 'text/csv'); toast('Exported ' + n + ' samples');
};
addEventListener('keydown', e => { if (e.key === ' ' && e.target === document.body) { e.preventDefault(); $('#bRun').click(); } });

/* ---- boot ---- */
let boot = null; try { const o = JSON.parse(localStorage.getItem('physics.v1')); if (o && o.lab === 'physics' && o.exp in EXPS) boot = o; } catch (e) { }
/* deep link, used by the notebooks:  physics/index.html#exp=osc&F0=0&c=0  (optional scen=<scenario name>, then any parameter id) */
function fromHash() {
  const q = new URLSearchParams(location.hash.slice(1)), id = q.get('exp'); if (!(id in EXPS)) return false;
  selectExp(id, q.get('scen') || undefined); let ch = false;
  E.params.forEach(a => { if (q.has(a[0])) { const v = parseFloat(q.get(a[0])); if (isFinite(v)) { P[a[0]] = Math.min(a[3], Math.max(a[2], v)); ch = true; } } });
  if (ch) { buildSide(); startRun(); persist(); }
  return true;
}
if (!fromHash()) { if (boot) applySnap(boot); else selectExp('proj'); }
addEventListener('hashchange', fromHash);
let last = performance.now();
function frame(now) {
  const dt = (now - last) / 1000; last = now;
  try {
    if (running) advance(dt);
    setStatus(); const [W, H] = fitCanvas(cv, cx); E.draw(cx, S, P, W, H); $('#hud').innerHTML = E.hud(S, P); drawPlots();
  } catch (err) { console.error(err); }
  requestAnimationFrame(frame);
}
requestAnimationFrame(frame);
window.__pl = { get E() { return E; }, get S() { return S; }, get P() { return P; }, advance, selectExp, EXPS, get logN() { return logN; }, get log() { return log; } };
