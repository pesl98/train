'use strict';
/* Robotics Lab — 2-link planar arm in a vertical plane.
   Engine: rigid-body dynamics (RK4, 1 kHz) + sampled joint PID with sensor noise, encoder
   quantisation, loop-rate and actuation delay. */
const $ = s => document.querySelector(s);
const D2R = Math.PI / 180;

/* ---------------- parameters ---------------- */
const SPEC = [
  ['Arm', null],
  ['l1', 'Link 1 length', 0.15, 0.40, 0.01, 'm', 0.30],
  ['l2', 'Link 2 length', 0.10, 0.40, 0.01, 'm', 0.25],
  ['m1', 'Link 1 mass', 0.1, 3, 0.05, 'kg', 1.0],
  ['m2', 'Link 2 mass', 0.1, 3, 0.05, 'kg', 0.8],
  ['pay', 'Payload (tip)', 0, 2, 0.05, 'kg', 0],
  ['b', 'Joint damping', 0, 0.5, 0.005, 'N·m·s', 0.05],
  ['g', 'Gravity', 0, 20, 0.1, 'm/s²', 9.81],
  ['tmax', 'Torque limit', 0.5, 20, 0.5, 'N·m', 8],
  ['Controller (PID per joint)', null],
  ['kp', 'Kp', 0, 150, 0.5, '', 30],
  ['ki', 'Ki', 0, 60, 0.5, '', 2],
  ['kd', 'Kd', 0, 12, 0.05, '', 2.5],
  ['Real-world effects', null],
  ['hz', 'Control rate', 10, 1000, 5, 'Hz', 200],
  ['delay', 'Actuation delay', 0, 5, 1, 'steps', 1],
  ['noise', 'Sensor noise', 0, 2, 0.01, '° rms', 0],
  ['bits', 'Encoder bits', 6, 16, 1, 'bit', 14],
  ['Trajectory (Circle mode)', null],
  ['cr', 'Radius', 0.02, 0.2, 0.005, 'm', 0.10],
  ['cp', 'Period', 1, 10, 0.1, 's', 4],
];
const DEFAULTS = {}; SPEC.forEach(s => { if (s[1] !== null) DEFAULTS[s[0]] = s[6]; });
let P = { ...DEFAULTS };
let F = { grav: true, comp: true, elbow: 1 };       // flags: elbow +1 = elbow-down config
let mode = 'ik';
let target = [0.30, 0.15];
let jref = [-30, 80];                               // degrees, used in 'joint' mode

/* ---------------- state ---------------- */
const Q0 = [-90 * D2R, 0];
let q, w, t, integ, qmPrev, wEst, tauCmd, tauApp, queue, nextCtl, running = true, diverged = false, sat = false, simErr = 0;
const CAP = 6000;                                    // log samples at 100 Hz = 60 s
let log, logN, trail;
function reset() {
  q = Q0.slice(); w = [0, 0]; t = 0; integ = [0, 0]; qmPrev = Q0.slice(); wEst = [0, 0];
  tauCmd = [0, 0]; tauApp = [0, 0]; queue = []; nextCtl = 0; diverged = false; sat = false;
  log = { t: new Float32Array(CAP), q: [new Float32Array(CAP), new Float32Array(CAP)], r: [new Float32Array(CAP), new Float32Array(CAP)],
    u: [new Float32Array(CAP), new Float32Array(CAP)], e: new Float32Array(CAP), x: new Float32Array(CAP), y: new Float32Array(CAP) };
  logN = 0; trail = []; lastLog = -1;
  setStatus();
}
let lastLog = -1;

/* ---------------- kinematics ---------------- */
const fk = (a, b) => { const x1 = P.l1 * Math.cos(a), y1 = P.l1 * Math.sin(a); return [x1, y1, x1 + P.l2 * Math.cos(a + b), y1 + P.l2 * Math.sin(a + b)]; };
function ik(x, y) {
  const d2 = x * x + y * y, l1 = P.l1, l2 = P.l2;
  let c2 = (d2 - l1 * l1 - l2 * l2) / (2 * l1 * l2), reach = true;
  if (c2 > 1 || c2 < -1) { reach = false; c2 = Math.max(-1, Math.min(1, c2)); }
  const q2 = F.elbow * Math.acos(c2);
  const q1 = Math.atan2(y, x) - Math.atan2(l2 * Math.sin(q2), l1 + l2 * Math.cos(q2));
  return { q: [q1, q2], reach };
}
const wrap = a => { while (a > Math.PI) a -= 2 * Math.PI; while (a < -Math.PI) a += 2 * Math.PI; return a; };

/* ---------------- dynamics ---------------- */
function inertia(pay) {
  const l1 = P.l1, l2 = P.l2, m1 = P.m1, mL = P.m2, m2 = mL + pay;
  const lc2 = (mL * l2 / 2 + pay * l2) / m2;
  const I1 = m1 * l1 * l1 / 12;
  const I2 = mL * l2 * l2 / 12 + mL * (l2 / 2 - lc2) ** 2 + pay * (l2 - lc2) ** 2;
  return { l1, l2, m1, m2, lc1: l1 / 2, lc2, I1, I2 };
}
function accel(qq, ww, tau, p, g) {
  const { l1, m1, m2, lc1, lc2, I1, I2 } = p;
  const c2 = Math.cos(qq[1]), s2 = Math.sin(qq[1]);
  const M11 = I1 + m1 * lc1 * lc1 + I2 + m2 * (l1 * l1 + lc2 * lc2 + 2 * l1 * lc2 * c2);
  const M12 = I2 + m2 * (lc2 * lc2 + l1 * lc2 * c2), M22 = I2 + m2 * lc2 * lc2;
  const h = m2 * l1 * lc2 * s2;
  const C1 = -h * (2 * ww[0] * ww[1] + ww[1] * ww[1]), C2 = h * ww[0] * ww[0];
  const c12 = Math.cos(qq[0] + qq[1]);
  const G1 = g * ((m1 * lc1 + m2 * l1) * Math.cos(qq[0]) + m2 * lc2 * c12), G2 = g * m2 * lc2 * c12;
  const r1 = tau[0] - P.b * ww[0] - C1 - G1, r2 = tau[1] - P.b * ww[1] - C2 - G2;
  const det = M11 * M22 - M12 * M12;
  return [(M22 * r1 - M12 * r2) / det, (M11 * r2 - M12 * r1) / det];
}
let PD = inertia(0);
function stepPhysics(h) {
  const f = (s) => { const a = accel([s[0], s[1]], [s[2], s[3]], tauApp, PD, F.grav ? P.g : 0); return [s[2], s[3], a[0], a[1]]; };
  const s0 = [q[0], q[1], w[0], w[1]];
  const add = (s, k, c) => s.map((v, i) => v + k[i] * c);
  const k1 = f(s0), k2 = f(add(s0, k1, h / 2)), k3 = f(add(s0, k2, h / 2)), k4 = f(add(s0, k3, h));
  for (let i = 0; i < 4; i++) s0[i] += h / 6 * (k1[i] + 2 * k2[i] + 2 * k3[i] + k4[i]);
  q[0] = s0[0]; q[1] = s0[1]; w[0] = s0[2]; w[1] = s0[3];
  if (!isFinite(q[0] + q[1] + w[0] + w[1]) || Math.abs(w[0]) > 400 || Math.abs(w[1]) > 400) diverged = true;
}

/* ---------------- controller ---------------- */
function gauss() { return Math.sqrt(-2 * Math.log(1 - Math.random())) * Math.cos(2 * Math.PI * Math.random()); }
let refQ = [0, 0], refXY = [0, 0], reachable = true;
function reference() {
  if (mode === 'joint') { refQ = [jref[0] * D2R, jref[1] * D2R]; const p = fk(refQ[0], refQ[1]); refXY = [p[2], p[3]]; reachable = true; return; }
  if (mode === 'traj') { const a = 2 * Math.PI * t / P.cp; const c = trajCenter(); refXY = [c[0] + P.cr * Math.cos(a), c[1] + P.cr * Math.sin(a)]; }
  else refXY = target.slice();
  const r = ik(refXY[0], refXY[1]); refQ = r.q; reachable = r.reach;
}
const trajCenter = () => [0.5 * (P.l1 + P.l2) * 0.9 * 0.85 + 0.0, 0.05];
const nomPD = () => inertia(0);
function control() {
  const Ts = 1 / P.hz, step = 2 * Math.PI / (1 << P.bits), qm = [0, 0];
  for (let i = 0; i < 2; i++) { const n = P.noise * D2R * gauss(); qm[i] = Math.round((q[i] + n) / step) * step; }
  reference();
  const tau = [0, 0]; sat = false;
  const nm = nomPD();
  const Gff = gravityTorque(qm, nm);
  for (let i = 0; i < 2; i++) {
    const v = wrap(qm[i] - qmPrev[i]) / Ts; wEst[i] += 0.3 * (v - wEst[i]); qmPrev[i] = qm[i];
    const e = wrap(refQ[i] - qm[i]);
    const k = i ? 0.3 : 1;   // joint 2 has far less inertia: scale gains
    let u = k * (P.kp * e + P.ki * integ[i] - P.kd * wEst[i]) + (F.comp && F.grav ? Gff[i] : 0);
    const us = Math.max(-P.tmax, Math.min(P.tmax, u));
    if (us === u) integ[i] += e * Ts; else sat = true;
    const lim = P.ki > 0 ? 2 * P.tmax / P.ki : 0; integ[i] = Math.max(-lim, Math.min(lim, integ[i]));
    tau[i] = us;
  }
  tauCmd = tau; queue.push(tau);
  while (queue.length > P.delay + 1) queue.shift();
  tauApp = queue.length > P.delay ? queue[0] : [0, 0];
}
function gravityTorque(qq, p) {
  const { l1, m1, m2, lc1, lc2 } = p, c12 = Math.cos(qq[0] + qq[1]);
  return [P.g * ((m1 * lc1 + m2 * l1) * Math.cos(qq[0]) + m2 * lc2 * c12), P.g * m2 * lc2 * c12];
}

/* ---------------- main loop ---------------- */
const H = 0.001;
function advance(dtReal) {
  let sim = Math.min(dtReal, 0.05) * parseFloat($('#speed').value), n = Math.round(sim / H);
  for (let i = 0; i < n && !diverged; i++) {
    if (t >= nextCtl - 1e-12) { control(); nextCtl += 1 / P.hz; if (nextCtl < t) nextCtl = t + 1 / P.hz; }
    stepPhysics(H); t += H;
    if (t - lastLog >= 0.0099) record();
  }
  if (diverged) { running = false; $('#bRun').textContent = 'Run'; }
}
function record() {
  lastLog = t; const k = logN % CAP, p = fk(q[0], q[1]);
  log.t[k] = t; for (let i = 0; i < 2; i++) { log.q[i][k] = q[i] / D2R; log.r[i][k] = refQ[i] / D2R; log.u[i][k] = tauApp[i]; }
  log.e[k] = Math.hypot(p[2] - refXY[0], p[3] - refXY[1]) * 1000; log.x[k] = p[2]; log.y[k] = p[3]; logN++;
  if (trail.length === 0 || logN % 2 === 0) { trail.push([p[2], p[3]]); if (trail.length > 300) trail.shift(); }
}

/* ---------------- rendering: arm ---------------- */
const cv = $('#view'), cx = cv.getContext('2d'), pl = $('#plots'), px = pl.getContext('2d');
let VW = 0, VH = 0, S = 400, OX = 0, OY = 0;
function fitCanvas(c, ctx) {
  const r = c.getBoundingClientRect(), d = devicePixelRatio || 1;
  if (c.width !== Math.round(r.width * d) || c.height !== Math.round(r.height * d)) { c.width = Math.round(r.width * d); c.height = Math.round(r.height * d); }
  ctx.setTransform(d, 0, 0, d, 0, 0); return [r.width, r.height];
}
const toPx = (x, y) => [OX + x * S, OY - y * S], toW = (a, b) => [(a - OX) / S, (OY - b) / S];
function drawArm() {
  [VW, VH] = fitCanvas(cv, cx);
  S = Math.max(20, Math.min(VW / 2, VH / 2) - 30) / (P.l1 + P.l2 + 0.02); OX = VW / 2; OY = VH / 2;
  const c = cx; c.clearRect(0, 0, VW, VH);
  const bg = c.createRadialGradient(OX, OY, 20, OX, OY, Math.max(VW, VH) * 0.7); bg.addColorStop(0, '#12183a'); bg.addColorStop(1, '#080b17'); c.fillStyle = bg; c.fillRect(0, 0, VW, VH);
  // grid (10 cm)
  c.lineWidth = 1; c.strokeStyle = 'rgba(255,255,255,.045)'; c.beginPath();
  for (let g = -1; g <= 1; g += 0.1) { const [a] = toPx(g, 0), [, b] = toPx(0, g); c.moveTo(a, 0); c.lineTo(a, VH); c.moveTo(0, b); c.lineTo(VW, b); }
  c.stroke();
  // workspace annulus
  const rmax = P.l1 + P.l2, rmin = Math.abs(P.l1 - P.l2);
  c.beginPath(); c.arc(OX, OY, rmax * S, 0, 7); c.arc(OX, OY, rmin * S, 0, 7, true);
  c.fillStyle = 'rgba(124,140,255,.05)'; c.fill('evenodd'); c.setLineDash([4, 6]); c.strokeStyle = 'rgba(124,140,255,.35)'; c.beginPath(); c.arc(OX, OY, rmax * S, 0, 7); c.stroke(); c.setLineDash([]);
  if (mode === 'traj') { const cc = trajCenter(), [a, b] = toPx(cc[0], cc[1]); c.strokeStyle = 'rgba(74,222,128,.4)'; c.setLineDash([3, 5]); c.beginPath(); c.arc(a, b, P.cr * S, 0, 7); c.stroke(); c.setLineDash([]); }
  // trail
  if (trail.length > 1) { c.beginPath(); trail.forEach((p, i) => { const [a, b] = toPx(p[0], p[1]); i ? c.lineTo(a, b) : c.moveTo(a, b); }); c.strokeStyle = 'rgba(251,191,36,.55)'; c.lineWidth = 2; c.stroke(); }
  // ghost (reference) arm
  const gp = fk(refQ[0], refQ[1]);
  c.strokeStyle = 'rgba(124,140,255,.35)'; c.lineWidth = 6; c.lineCap = 'round'; c.lineJoin = 'round'; c.beginPath();
  c.moveTo(OX, OY); c.lineTo(...toPx(gp[0], gp[1])); c.lineTo(...toPx(gp[2], gp[3])); c.stroke();
  // target marker
  const [tx, ty] = toPx(refXY[0], refXY[1]);
  c.strokeStyle = reachable ? '#4ade80' : '#f87171'; c.lineWidth = 2; c.beginPath(); c.arc(tx, ty, 9, 0, 7); c.moveTo(tx - 15, ty); c.lineTo(tx + 15, ty); c.moveTo(tx, ty - 15); c.lineTo(tx, ty + 15); c.stroke();
  // arm
  const p = fk(q[0], q[1]), j1 = toPx(p[0], p[1]), ee = toPx(p[2], p[3]);
  const link = (a, b, col1, col2, wd) => { const g = c.createLinearGradient(a[0], a[1], b[0], b[1]); g.addColorStop(0, col1); g.addColorStop(1, col2); c.strokeStyle = g; c.lineWidth = wd; c.lineCap = 'round'; c.beginPath(); c.moveTo(...a); c.lineTo(...b); c.stroke(); };
  c.shadowColor = 'rgba(34,211,238,.35)'; c.shadowBlur = 16;
  link([OX, OY], j1, '#22d3ee', '#4f9bff', 14); link(j1, ee, '#4f9bff', '#a78bfa', 11); c.shadowBlur = 0;
  // torque arcs (saturation indication)
  for (const [pt, i] of [[[OX, OY], 0], [j1, 1]]) {
    const u = tauApp[i] / P.tmax; if (Math.abs(u) > 0.02) { c.strokeStyle = Math.abs(u) > 0.98 ? '#f87171' : '#fbbf24'; c.lineWidth = 3; c.beginPath(); c.arc(pt[0], pt[1], 22, -Math.PI / 2, -Math.PI / 2 + u * 2.2, u < 0); c.stroke(); }
  }
  for (const pt of [[OX, OY], j1]) { c.fillStyle = '#0a0e1d'; c.strokeStyle = '#e8ebff'; c.lineWidth = 2.5; c.beginPath(); c.arc(pt[0], pt[1], 9, 0, 7); c.fill(); c.stroke(); }
  c.fillStyle = '#fbbf24'; c.beginPath(); c.arc(ee[0], ee[1], 6 + P.pay * 4, 0, 7); c.fill();
  c.fillStyle = '#2c3566'; c.fillRect(OX - 34, OY + 12, 68, 8);
  // HUD
  const err = Math.hypot(p[2] - refXY[0], p[3] - refXY[1]) * 1000;
  $('#hud').innerHTML = `t <b>${t.toFixed(2)} s</b><br>tip <b>${p[2].toFixed(3)}, ${p[3].toFixed(3)} m</b><br>error <b>${err.toFixed(1)} mm</b><br>q <b>${(q[0] / D2R).toFixed(1)}°, ${(q[1] / D2R).toFixed(1)}°</b><br>τ <b>${tauApp[0].toFixed(2)}, ${tauApp[1].toFixed(2)} N·m</b>`;
}

/* ---------------- rendering: plots ---------------- */
const WIN = 10;     // seconds shown
function drawPlots() {
  const [W, Hh] = fitCanvas(pl, px), c = px; c.clearRect(0, 0, W, Hh);
  const n = Math.min(logN, CAP), start = logN - n, idx = k => (start + k) % CAP;
  const rows = [
    { name: 'Joint angles (°)', ser: [{ d: log.q[0], col: '#22d3ee' }, { d: log.q[1], col: '#a78bfa' }, { d: log.r[0], col: '#22d3ee', dash: 1 }, { d: log.r[1], col: '#a78bfa', dash: 1 }], leg: 'q1 · q2 (dashed = ref)' },
    { name: 'Motor torque (N·m)', ser: [{ d: log.u[0], col: '#fbbf24' }, { d: log.u[1], col: '#f472b6' }], leg: 'τ1 · τ2' },
    { name: 'Tip error (mm)', ser: [{ d: log.e, col: '#4ade80' }], leg: 'distance to target' },
  ];
  const L = 50, R = 10, gap = 8, rh = (Hh - gap * 4) / 3;
  c.font = '11px system-ui';
  rows.forEach((r, ri) => {
    const y0 = gap + ri * (rh + gap), pw = W - L - R;
    c.fillStyle = 'rgba(255,255,255,.025)'; c.fillRect(L, y0, pw, rh);
    c.fillStyle = '#8a93b8'; c.textAlign = 'left'; c.fillText(r.name, L + 6, y0 + 12);
    c.textAlign = 'right'; c.fillStyle = r.ser[0].col;
    if (n < 2) return;
    const tEnd = log.t[idx(n - 1)], t0 = Math.max(0, tEnd - WIN);
    let k0 = 0; while (k0 < n - 1 && log.t[idx(k0)] < t0) k0++;
    let lo = 1e30, hi = -1e30; for (const s of r.ser) for (let k = k0; k < n; k++) { const v = s.d[idx(k)]; if (v < lo) lo = v; if (v > hi) hi = v; }
    if (!(hi > lo)) { lo -= 1; hi += 1; } const pad = (hi - lo) * 0.1; lo -= pad; hi += pad;
    const X = tt => L + (tt - t0) / WIN * pw, Y = v => y0 + rh - 4 - (v - lo) / (hi - lo) * (rh - 18);
    c.strokeStyle = 'rgba(255,255,255,.06)'; c.fillStyle = '#6b7599'; c.textAlign = 'right';
    for (let g = 0; g <= 3; g++) { const v = lo + (hi - lo) * g / 3, yy = Y(v); c.beginPath(); c.moveTo(L, yy); c.lineTo(L + pw, yy); c.stroke(); c.fillText(Math.abs(v) >= 100 ? v.toFixed(0) : v.toFixed(1), L - 5, yy + 3); }
    c.save(); c.beginPath(); c.rect(L, y0, pw, rh); c.clip();
    for (const s of r.ser) {
      c.strokeStyle = s.col; c.lineWidth = s.dash ? 1.2 : 1.8; c.setLineDash(s.dash ? [4, 4] : []); c.beginPath();
      for (let k = k0; k < n; k++) { const xx = X(log.t[idx(k)]), yy = Y(s.d[idx(k)]); k === k0 ? c.moveTo(xx, yy) : c.lineTo(xx, yy); } c.stroke();
    }
    c.restore(); c.setLineDash([]);
    c.fillStyle = '#6b7599'; c.textAlign = 'right'; c.fillText(r.leg, L + pw - 6, y0 + 12);
  });
}

/* ---------------- UI ---------------- */
const side = $('#side');
function buildSide() {
  let h = '';
  for (const s of SPEC) {
    if (s[1] === null) { h += `<h4>${s[0]}</h4>`; continue; }
    h += `<div class="row"><label>${s[1]}</label><input type="range" id="p_${s[0]}" min="${s[2]}" max="${s[3]}" step="${s[4]}"><output id="o_${s[0]}"></output></div>`;
    if (s[0] === 'g') h += `<label class="chk"><input type="checkbox" id="fGrav"> Gravity acts (vertical plane)</label>`;
    if (s[0] === 'kd') h += `<label class="chk"><input type="checkbox" id="fComp"> Gravity compensation (nominal model, ignores payload)</label>`;
  }
  h += `<h4>Joint targets (Joints mode)</h4>
    <div class="row"><label>Joint 1</label><input type="range" id="j0" min="-180" max="180" step="1"><output id="oj0"></output></div>
    <div class="row"><label>Joint 2</label><input type="range" id="j1" min="-150" max="150" step="1"><output id="oj1"></output></div>
    <label class="chk"><input type="checkbox" id="fElbow"> Elbow down (otherwise up)</label>
    <p style="color:var(--muted);font-size:12px;margin-top:14px">Click or drag in the workspace to move the target. The dashed purple arm is where the controller wants to go.</p>`;
  side.innerHTML = h;
  for (const s of SPEC) if (s[1] !== null) {
    const el = $('#p_' + s[0]); el.oninput = () => { P[s[0]] = parseFloat(el.value); syncOut(s[0]); if (['l1', 'l2', 'm1', 'm2', 'pay'].includes(s[0])) PD = inertia(P.pay); persist(); };
  }
  $('#fGrav').onchange = e => { F.grav = e.target.checked; persist(); }; $('#fComp').onchange = e => { F.comp = e.target.checked; persist(); };
  $('#fElbow').onchange = e => { F.elbow = e.target.checked ? 1 : -1; persist(); };
  for (const i of [0, 1]) $('#j' + i).oninput = e => { jref[i] = parseFloat(e.target.value); $('#oj' + i).textContent = jref[i] + '°'; setMode('joint'); persist(); };
}
function syncOut(k) { const s = SPEC.find(x => x[0] === k), v = P[k]; $('#o_' + k).textContent = (Number.isInteger(s[4]) ? v.toFixed(0) : v.toFixed(s[4] < 0.01 ? 3 : 2).replace(/0+$/, '').replace(/\.$/, '')) + (s[5] ? ' ' + s[5].split(' ')[0] : ''); }
function syncUI() {
  for (const s of SPEC) if (s[1] !== null) { $('#p_' + s[0]).value = P[s[0]]; syncOut(s[0]); }
  $('#fGrav').checked = F.grav; $('#fComp').checked = F.comp; $('#fElbow').checked = F.elbow > 0;
  for (const i of [0, 1]) { $('#j' + i).value = jref[i]; $('#oj' + i).textContent = jref[i] + '°'; }
  document.querySelectorAll('#mode .btn').forEach(b => b.classList.toggle('on', b.dataset.m === mode));
  PD = inertia(P.pay);
}
function setMode(m) { mode = m; document.querySelectorAll('#mode .btn').forEach(b => b.classList.toggle('on', b.dataset.m === m)); if (m === 'traj') { } persist(); }
document.querySelectorAll('#mode .btn').forEach(b => b.onclick = () => setMode(b.dataset.m));
function setStatus() {
  const s = $('#status');
  if (diverged) { s.className = 'pill bad'; s.textContent = 'Unstable — simulation diverged'; }
  else if (sat) { s.className = 'pill warn'; s.textContent = 'Torque saturated'; }
  else if (!reachable && mode !== 'joint') { s.className = 'pill warn'; s.textContent = 'Target out of reach'; }
  else { s.className = 'pill ok'; s.textContent = running ? 'Running' : 'Paused'; }
}
function toast(m) { const e = $('#toast'); e.textContent = m; e.classList.add('show'); clearTimeout(toast.t); toast.t = setTimeout(() => e.classList.remove('show'), 1800); }

/* pointer: set target */
let drag = false;
function pointerTarget(e) {
  const r = cv.getBoundingClientRect(), [x, y] = toW(e.clientX - r.left, e.clientY - r.top);
  target = [x, y]; if (mode !== 'ik') setMode('ik'); persist();
}
cv.onpointerdown = e => { drag = true; cv.setPointerCapture(e.pointerId); pointerTarget(e); };
cv.onpointermove = e => { if (drag) pointerTarget(e); };
cv.onpointerup = () => drag = false;

/* scenarios */
const SCEN = {
  '— Experiment scenarios —': null,
  'Step response (well tuned)': { p: {}, m: 'ik', tg: [0.30, 0.15] },
  'Gravity droop (no compensation)': { p: { ki: 0 }, f: { comp: false }, m: 'ik', tg: [0.35, 0.10] },
  'Integral action fixes droop': { p: { ki: 25 }, f: { comp: false }, m: 'ik', tg: [0.35, 0.10] },
  'Heavy payload (model mismatch)': { p: { pay: 1.2, ki: 0 }, m: 'ik', tg: [0.38, 0.05] },
  'Trace a circle': { p: {}, m: 'traj' },
  'Slow loop: 40 Hz goes unstable': { p: { hz: 40, kd: 3.5 }, m: 'ik', tg: [0.30, 0.20] },
  'Noisy, coarse encoder': { p: { noise: 0.4, bits: 8, kd: 4 }, m: 'ik', tg: [0.30, 0.20] },
  'Actuation delay of 5 steps': { p: { delay: 5, hz: 100 }, m: 'ik', tg: [0.30, 0.20] },
  'Moon gravity': { p: { g: 1.62 }, m: 'traj' },
};
const scenSel = $('#scen'); Object.keys(SCEN).forEach(k => scenSel.add(new Option(k, k)));
scenSel.onchange = () => {
  const s = SCEN[scenSel.value]; if (!s) return;
  P = { ...DEFAULTS, ...s.p }; F = { grav: true, comp: true, elbow: 1, ...(s.f || {}) }; if (s.tg) target = s.tg.slice(); mode = s.m;
  syncUI(); reset(); running = true; $('#bRun').textContent = 'Pause'; persist();
};

/* run / reset */
$('#bRun').onclick = () => { if (diverged) reset(); running = !running; $('#bRun').textContent = running ? 'Pause' : 'Run'; };
$('#bReset').onclick = () => { reset(); running = true; $('#bRun').textContent = 'Pause'; };

/* persistence / files */
const snapshot = () => ({ lab: 'robotics', v: 1, P, F, mode, target, jref });
function persist() { try { localStorage.setItem('robotics.v1', JSON.stringify(snapshot())); } catch (e) { } }
function applySnap(o) { P = { ...DEFAULTS, ...o.P }; F = { grav: true, comp: true, elbow: 1, ...o.F }; mode = o.mode || 'ik'; target = o.target || target; jref = o.jref || jref; syncUI(); reset(); }
function download(name, text, type) { const a = document.createElement('a'); a.href = URL.createObjectURL(new Blob([text], { type })); a.download = name; a.click(); URL.revokeObjectURL(a.href); }
$('#bSave').onclick = () => { download('robot-setup.json', JSON.stringify(snapshot(), null, 1), 'application/json'); toast('Setup saved'); };
$('#bLoad').onclick = () => $('#file').click();
$('#file').onchange = e => { const f = e.target.files[0]; if (!f) return; const r = new FileReader(); r.onload = () => { try { const o = JSON.parse(r.result); if (o.lab !== 'robotics') throw 0; applySnap(o); toast('Setup loaded'); } catch (x) { toast('Not a Robotics Lab file'); } }; r.readAsText(f); e.target.value = ''; };
$('#bCsv').onclick = () => {
  if (logN < 2) return toast('Run the simulation first');
  const n = Math.min(logN, CAP), st = logN - n, rows = ['t_s,q1_deg,q2_deg,ref1_deg,ref2_deg,tau1_Nm,tau2_Nm,tip_x_m,tip_y_m,tip_error_mm'];
  for (let k = 0; k < n; k++) { const j = (st + k) % CAP; rows.push([log.t[j].toFixed(3), log.q[0][j].toFixed(3), log.q[1][j].toFixed(3), log.r[0][j].toFixed(3), log.r[1][j].toFixed(3), log.u[0][j].toFixed(4), log.u[1][j].toFixed(4), log.x[j].toFixed(5), log.y[j].toFixed(5), log.e[j].toFixed(3)].join(',')); }
  download('robot-data.csv', rows.join('\n'), 'text/csv'); toast('Exported ' + n + ' samples');
};
$('#bEsp').onclick = () => {
  const f = x => (+x).toFixed(3), Ts = (1 / P.hz).toFixed(5);
  const code = `// Joint PID for a 2-link arm — generated by Robotics Lab
// Tuned in simulation: ${P.hz} Hz loop, ${P.bits}-bit encoders, torque limit ${P.tmax} N·m.
// Real hardware will differ (friction, backlash, motor dynamics): expect to re-tune.

const float KP = ${f(P.kp)}f, KI = ${f(P.ki)}f, KD = ${f(P.kd)}f;
const float TS = ${Ts}f;                 // control period [s]
const float TAU_MAX = ${f(P.tmax)}f;     // torque limit [N·m]
const float LINK1 = ${f(P.l1)}f, LINK2 = ${f(P.l2)}f;   // [m]
const bool  ELBOW_DOWN = ${F.elbow > 0};

struct Joint { float integ = 0, prev = 0, vel = 0; };
Joint jt[2];

// Replace with your encoder reads (radians) and motor driver (normalised -1..1)
float readAngle(int j)            { return 0; }
void  writeTorque(int j, float u) { /* map u * TAU_MAX to PWM / current */ }

float pid(int j, float ref, float meas, float gravityFF) {
  float v = (meas - jt[j].prev) / TS;       // finite-difference velocity
  jt[j].vel += 0.3f * (v - jt[j].vel);      // low-pass filter
  jt[j].prev = meas;
  float e = ref - meas;
  float k = j ? 0.3f : 1.0f;                // joint 2 has far less inertia
  float u = k * (KP * e + KI * jt[j].integ - KD * jt[j].vel) + gravityFF;
  float us = constrain(u, -TAU_MAX, TAU_MAX);
  if (us == u) jt[j].integ += e * TS;       // anti-windup
  return us;
}

bool inverseKinematics(float x, float y, float &q1, float &q2) {
  float c2 = (x*x + y*y - LINK1*LINK1 - LINK2*LINK2) / (2*LINK1*LINK2);
  if (c2 > 1 || c2 < -1) return false;
  q2 = (ELBOW_DOWN ? 1 : -1) * acosf(c2);
  q1 = atan2f(y, x) - atan2f(LINK2 * sinf(q2), LINK1 + LINK2 * cosf(q2));
  return true;
}

unsigned long nextTick;
void setup() { nextTick = micros(); }
void loop() {
  if ((long)(micros() - nextTick) < 0) return;
  nextTick += (unsigned long)(TS * 1e6);
  float q1r, q2r;
  if (!inverseKinematics(0.30f, 0.15f, q1r, q2r)) return;   // target [m]
  writeTorque(0, pid(0, q1r, readAngle(0), 0));
  writeTorque(1, pid(1, q2r, readAngle(1), 0));
}
`;
  download('robot_pid.ino', code, 'text/plain'); toast('Sketch downloaded');
};

/* theory */
$('#theory').innerHTML = `<h2>The mathematics</h2><p>A planar two-link arm moving in a vertical plane. Angles <b>q₁</b> (from the horizontal) and <b>q₂</b> (relative to link 1).</p>
<h5>Forward kinematics</h5><pre>x = l₁cos q₁ + l₂cos(q₁+q₂)
y = l₁sin q₁ + l₂sin(q₁+q₂)</pre>
<h5>Inverse kinematics (analytic)</h5><pre>cos q₂ = (x² + y² − l₁² − l₂²) / (2 l₁ l₂)       q₂ = ± acos(·)   (elbow up/down)
q₁ = atan2(y, x) − atan2(l₂ sin q₂, l₁ + l₂ cos q₂)</pre><p>Two solutions exist inside the reachable annulus |l₁−l₂| ≤ r ≤ l₁+l₂; outside it the target is unreachable.</p>
<h5>Equations of motion (Euler–Lagrange)</h5><pre>M(q) q̈ + C(q, q̇) q̇ + G(q) = τ − b q̇

M₁₁ = I₁ + m₁lc₁² + I₂ + m₂(l₁² + lc₂² + 2 l₁ lc₂ cos q₂)
M₁₂ = I₂ + m₂(lc₂² + l₁ lc₂ cos q₂)         M₂₂ = I₂ + m₂ lc₂²
h = m₂ l₁ lc₂ sin q₂
C q̇ = [ −h(2 q̇₁q̇₂ + q̇₂²),  h q̇₁² ]
G   = [ g((m₁lc₁ + m₂l₁)cos q₁ + m₂lc₂ cos(q₁+q₂)),  g m₂ lc₂ cos(q₁+q₂) ]</pre><p>Integrated with 4th-order Runge–Kutta at 1 kHz. A tip payload shifts link 2's centre of mass and inertia.</p>
<h5>Controller</h5><pre>τᵢ = Kp·eᵢ + Ki·∫eᵢ dt − Kd·q̇ᵢ + Gᵢ(q_measured)       clamp to ±τmax</pre><p>Computed at the control rate, held constant between samples, and applied after the actuation delay. The derivative acts on the measurement (no kick on target changes) using a filtered finite difference. The integrator stops while the output is saturated (anti-windup).</p>
<h5>Why the real world disagrees</h5><pre>Sampling   a loop that is too slow cannot damp the arm: Kd·Ts/M approaching 2 → instability
Delay      each step of delay adds phase lag that eats the damping margin
Noise      differentiating noisy, quantised angles amplifies it (resolution 2π/2ᵇⁱᵗˢ)
Mismatch   gravity compensation uses the nominal masses, so a payload leaves a steady error until Ki winds it out</pre>
<p style="margin-top:14px"><button class="btn" onclick="document.getElementById('modal').classList.remove('show')">Close</button></p>`;
$('#bTheory').onclick = () => $('#modal').classList.add('show');
$('#modal').onclick = e => { if (e.target.id === 'modal') e.target.classList.remove('show'); };
addEventListener('keydown', e => { if (e.key === 'Escape') $('#modal').classList.remove('show'); if (e.key === ' ' && e.target === document.body) { e.preventDefault(); $('#bRun').click(); } });

/* boot */
try { const o = JSON.parse(localStorage.getItem('robotics.v1')); if (o && o.lab === 'robotics') { P = { ...DEFAULTS, ...o.P }; F = { grav: true, comp: true, elbow: 1, ...o.F }; mode = o.mode || 'ik'; target = o.target || target; jref = o.jref || jref; } } catch (e) { }
buildSide(); syncUI(); reset(); reference();
let last = performance.now();
function frame(now) {
  const dt = (now - last) / 1000; last = now;
  if (running) advance(dt);
  setStatus(); drawArm(); drawPlots(); requestAnimationFrame(frame);
}
requestAnimationFrame(frame);
window.__rl = { get state() { return { t, q, w, diverged, logN, P, F, mode }; }, reset, advance, setMode };
