'use strict';
/* =====================================================================
   Voltaic — editor, renderer, scope, UI
   ===================================================================== */
const $ = s => document.querySelector(s);
const clamp = (v, a, b) => Math.max(a, Math.min(b, v));
const G = GRID;
const SUBSTEPS = 20;

/* ---------- icons ---------- */
const ICONS = {
  play: '<path d="M8 5v14l11-7z"/>', pause: '<path d="M7 5h4v14H7zM13 5h4v14h-4z"/>',
  step: '<path d="M6 5v14l9-7zM17 5h2v14h-2z"/>',
  reset: '<path d="M12 5V2L7 6l5 4V7a5 5 0 1 1-5 5H5a7 7 0 1 0 7-7z"/>',
  undo: '<path d="M12.5 8c-2.65 0-5.05 1-6.9 2.6L2 7v9h9l-3.62-3.62A8 8 0 0 1 12.5 11c3.04 0 5.67 1.79 6.9 4.4l2.35-.78C20.2 11.4 16.7 8 12.5 8z"/>',
  fit: '<path d="M4 4h6v2H6v4H4zM14 4h6v6h-2V6h-4zM4 14h2v4h4v2H4zM18 14h2v6h-6v-2h4z"/>',
  trash: '<path d="M6 19a2 2 0 0 0 2 2h8a2 2 0 0 0 2-2V7H6zM19 4h-3.5l-1-1h-5l-1 1H5v2h14z"/>',
  rotate: '<path d="M12 5V1L7 6l5 5V7a6 6 0 1 1-6 6H4a8 8 0 1 0 8-8z"/>',
  download: '<path d="M5 20h14v-2H5zM19 9h-4V3H9v6H5l7 7z"/>',
  upload: '<path d="M5 20h14v-2H5zM9 16h6v-6h4l-7-7-7 7h4z"/>',
  image: '<path d="M21 19V5a2 2 0 0 0-2-2H5a2 2 0 0 0-2 2v14a2 2 0 0 0 2 2h14a2 2 0 0 0 2-2zM8.5 13.5l2.5 3 3.5-4.5 4.5 6H5z"/>',
  plus: '<path d="M19 13h-6v6h-2v-6H5v-2h6V5h2v6h6z"/>',
  chev: '<path d="M7 10l5 5 5-5z"/>',
  wire: '<path d="M4 19h6v-7h4V5h6" fill="none" stroke="currentColor" stroke-width="2.4" stroke-linecap="round" stroke-linejoin="round"/><circle cx="4" cy="19" r="2"/><circle cx="20" cy="5" r="2"/>',
};
const icon = n => `<svg viewBox="0 0 24 24" fill="currentColor">${ICONS[n]}</svg>`;

/* ---------- colours ---------- */
const COL = { line: '#c9d3ff', dim: '#6b7599', accent: '#7c8cff', pos: [255, 107, 74], neg: [63, 181, 255], neu: [126, 137, 184] };
const PROBE_COLORS = ['#4ade80', '#38bdf8', '#f472b6', '#facc15', '#a78bfa', '#fb923c'];
function vcolor(v, vs, alpha = 1) {
  const t = clamp(v / vs, -1, 1), a = Math.pow(Math.abs(t), 0.75);
  const tg = t >= 0 ? COL.pos : COL.neg, n = COL.neu;
  return `rgba(${(n[0] + (tg[0] - n[0]) * a) | 0},${(n[1] + (tg[1] - n[1]) * a) | 0},${(n[2] + (tg[2] - n[2]) * a) | 0},${alpha})`;
}

/* ---------- state ---------- */
let circ = { comps: [], wires: [], nid: 1 };
let sim = null;
let running = true;
let timescale = 1;
let sel = null;                 // {k:'c'|'w', id}
let armed = null;               // component type being placed
let wireTool = false;
let placeRot = 0;
let palDrag = false;
const cam = { x: 0, y: 0, z: 1 };
const mouse = { sx: 0, sy: 0, wx: 0, wy: 0, gx: 0, gy: 0, over: false };
let drag = null;
let hoverPin = null;
let vscale = 0.5;
let spaceDown = false;

const cv = $('#cv'), ctx = cv.getContext('2d');
let dpr = 1, W = 0, H = 0;

const s2w = (sx, sy) => [(sx - cam.x) / cam.z, (sy - cam.y) / cam.z];

/* =====================================================================
   Circuit model helpers
   ===================================================================== */
const compById = id => circ.comps.find(c => c.id === id);

function addComp(type, x, y, rot = 0, props = {}) {
  const d = DEFS[type];
  let n = 1; const used = new Set(circ.comps.filter(c => c.type === type || DEFS[c.type].pre === d.pre).map(c => c.name));
  while (used.has(d.pre + n)) n++;
  const c = { id: circ.nid++, type, x, y, rot, p: Object.assign(structuredClone(d.p), props), name: d.pre + n };
  circ.comps.push(c);
  return c;
}
function addWire(x1, y1, x2, y2) {
  if (x1 === x2 && y1 === y2) return null;
  const w = { id: circ.nid++, x1, y1, x2, y2 };
  circ.wires.push(w);
  return w;
}
function addPoly(pts) { for (let i = 0; i < pts.length - 1; i++) addWire(pts[i][0], pts[i][1], pts[i + 1][0], pts[i + 1][1]); }

/* =====================================================================
   Examples
   ===================================================================== */
const PRESETS = {
  rc: { name: 'RC charging (square wave)', ts: 1,
    comps: [['AC', 10, 10, 0, { wave: 'square', amp: 5, off: 5, freq: 2 }], ['R', 16, 8, 0, { r: 1000 }], ['C', 22, 10, 1, { c: 1e-4 }], ['GND', 10, 14], ['PROBE', 12, 8], ['PROBE', 22, 8]],
    wires: [[[10, 8], [14, 8]], [[18, 8], [22, 8]], [[22, 12], [10, 12]], [[10, 12], [10, 14]]] },
  led: { name: 'LED + switch', ts: 1,
    comps: [['V', 8, 10, 0, { v: 9 }], ['SW', 14, 8, 0, { closed: true }], ['R', 20, 8, 0, { r: 330 }], ['LED', 26, 10, 1, { color: 'red' }], ['GND', 8, 14], ['PROBE', 24, 8]],
    wires: [[[8, 8], [12, 8]], [[16, 8], [18, 8]], [[22, 8], [26, 8]], [[26, 12], [8, 12]], [[8, 12], [8, 14]]] },
  rlc: { name: 'Series RLC resonance', ts: 0.005,
    comps: [['AC', 8, 10, 0, { wave: 'sine', amp: 5, freq: 500, off: 0 }], ['R', 14, 8, 0, { r: 20 }], ['L', 20, 8, 0, { l: 0.01 }], ['C', 26, 10, 1, { c: 1e-5 }], ['GND', 8, 14], ['PROBE', 10, 8], ['PROBE', 26, 8]],
    wires: [[[8, 8], [12, 8]], [[16, 8], [18, 8]], [[22, 8], [26, 8]], [[26, 12], [8, 12]], [[8, 12], [8, 14]]] },
  half: { name: 'Half-wave rectifier + filter', ts: 0.04,
    comps: [['AC', 8, 10, 0, { wave: 'sine', amp: 10, freq: 50, off: 0 }], ['D', 14, 8, 0], ['C', 20, 10, 1, { c: 1e-4 }], ['R', 26, 10, 1, { r: 1000 }], ['GND', 8, 14], ['PROBE', 10, 8], ['PROBE', 23, 8]],
    wires: [[[8, 8], [12, 8]], [[16, 8], [26, 8]], [[26, 12], [8, 12]], [[8, 12], [8, 14]]] },
  bridge: { name: 'Bridge rectifier', ts: 0.04,
    comps: [['AC', 16, 12, 3, { wave: 'sine', amp: 12, freq: 50, off: 0 }], ['D', 12, 9, 3], ['D', 12, 15, 3], ['D', 20, 9, 3], ['D', 20, 15, 3],
      ['C', 24, 12, 1, { c: 1e-4 }], ['R', 28, 12, 1, { r: 1000 }], ['GND', 16, 19], ['PROBE', 14, 12], ['PROBE', 16, 7]],
    wires: [[[12, 11], [12, 13]], [[12, 12], [14, 12]], [[20, 11], [20, 13]], [[18, 12], [20, 12]], [[12, 7], [28, 7]], [[24, 7], [24, 10]], [[28, 7], [28, 10]],
      [[12, 17], [28, 17]], [[24, 14], [24, 17]], [[28, 14], [28, 17]], [[16, 17], [16, 19]]] },
  opamp: { name: 'Inverting op-amp (gain −5)', ts: 0.0025,
    comps: [['AC', 6, 12, 0, { wave: 'sine', amp: 1, freq: 1000, off: 0 }], ['R', 12, 10, 0, { r: 1000 }], ['OP', 20, 10, 0, { rail: 12 }], ['R', 20, 5, 0, { r: 5000 }],
      ['GND', 17, 13], ['GND', 6, 16], ['PROBE', 8, 10], ['PROBE', 25, 8]],
    wires: [[[6, 10], [10, 10]], [[14, 10], [15, 10], [15, 9], [17, 9]], [[15, 9], [15, 5], [18, 5]], [[22, 5], [25, 5], [25, 10], [23, 10]], [[17, 11], [17, 13]], [[6, 14], [6, 16]]] },
  npn: { name: 'Transistor LED driver', ts: 1,
    comps: [['V', 6, 12, 0, { v: 9 }], ['SW', 10, 8, 1, { closed: true }], ['R', 10, 12, 1, { r: 10000 }], ['R', 20, 8, 1, { r: 330 }], ['LED', 20, 12, 1, { color: 'green' }],
      ['NPN', 19, 18, 0, { beta: 100 }], ['GND', 6, 18], ['PROBE', 14, 18], ['PROBE', 20, 15]],
    wires: [[[6, 10], [6, 6], [24, 6]], [[10, 14], [10, 18], [17, 18]], [[20, 14], [20, 16]], [[6, 14], [6, 22], [20, 22], [20, 20]]] },
  esp_blink: { name: 'ESP32: blink an LED', ts: 1,
    comps: [['MCU', 10, 12, 0, { board: 'esp32', code: SKETCHES.blink }], ['R', 19, 8, 0, { r: 150 }], ['LED', 24, 10, 1, { color: 'green' }], ['PROBE', 15, 8]],
    wires: [[[14, 8], [17, 8]], [[21, 8], [24, 8]], [[24, 12], [24, 20], [4, 20], [4, 10], [6, 10]]] },
  esp_button: { name: 'ESP32: button → LED', ts: 1,
    comps: [['MCU', 10, 12, 0, { board: 'esp32', code: SKETCHES.button }], ['R', 19, 8, 0, { r: 150 }], ['LED', 24, 10, 1, { color: 'red' }], ['SW', 18, 18, 1, { closed: false }], ['PROBE', 15, 8], ['PROBE', 16, 16]],
    wires: [[[14, 8], [17, 8]], [[21, 8], [24, 8]], [[24, 12], [24, 20], [4, 20], [4, 10], [6, 10]], [[14, 16], [18, 16]]] },
  esp_fade: { name: 'ESP32: PWM breathing LED', ts: 1,
    comps: [['MCU', 10, 12, 0, { board: 'esp32', code: SKETCHES.fade }], ['R', 19, 8, 0, { r: 150 }], ['LED', 24, 10, 1, { color: 'blue' }], ['PROBE', 15, 8]],
    wires: [[[14, 8], [17, 8]], [[21, 8], [24, 8]], [[24, 12], [24, 20], [4, 20], [4, 10], [6, 10]]] },
  zener: { name: 'Zener regulator', ts: 1,
    comps: [['V', 8, 10, 0, { v: 12 }], ['R', 14, 8, 0, { r: 470 }], ['ZD', 20, 10, 3, { vz: 5.1 }], ['R', 26, 10, 1, { r: 1000 }], ['GND', 8, 14], ['PROBE', 23, 8]],
    wires: [[[8, 8], [12, 8]], [[16, 8], [26, 8]], [[26, 12], [8, 12]], [[8, 12], [8, 14]]] },
};

function loadPreset(key) {
  const p = PRESETS[key]; if (!p) return;
  circ = { comps: [], wires: [], nid: 1 };
  for (const [t, x, y, r, pr] of p.comps) addComp(t, x, y, r || 0, pr || {});
  for (const poly of p.wires) addPoly(poly);
  sel = null;
  setTimescale(p.ts);
  rebuild(); fitView(); resetHistory(); renderInspector();
}

/* =====================================================================
   History / persistence
   ===================================================================== */
let hist = [], hi = -1;
const snapStr = () => JSON.stringify({ nid: circ.nid, comps: circ.comps.map(c => ({ id: c.id, type: c.type, x: c.x, y: c.y, rot: c.rot, p: c.p, name: c.name })), wires: circ.wires });
function resetHistory() { hist = [snapStr()]; hi = 0; save(); updateUndoButtons(); }
function commit(rb = true) {
  const s = snapStr();
  if (s !== hist[hi]) { hist = hist.slice(0, hi + 1); hist.push(s); if (hist.length > 150) hist.shift(); hi = hist.length - 1; }
  save(); updateUndoButtons();
  if (rb) rebuild();
}
function restore(s) {
  const o = JSON.parse(s);
  circ = { nid: o.nid, comps: o.comps, wires: o.wires };
  if (sel && !(sel.k === 'c' ? compById(sel.id) : circ.wires.find(w => w.id === sel.id))) sel = null;
  rebuild(); renderInspector();
}
function undo() { if (hi > 0) { hi--; restore(hist[hi]); save(); updateUndoButtons(); } }
function redo() { if (hi < hist.length - 1) { hi++; restore(hist[hi]); save(); updateUndoButtons(); } }
function updateUndoButtons() { $('#btnUndo').disabled = hi <= 0; $('#btnRedo').disabled = hi >= hist.length - 1; }
let deepLinked = false;   // opened as  voltaic/index.html#preset=<key>  (e.g. embedded in a notebook): do not overwrite the user's saved circuit
function save() { if (deepLinked) return; try { localStorage.setItem('voltaic.v1', JSON.stringify({ s: snapStr(), ts: timescale })); } catch (e) { } }
function loadSaved() {
  try {
    const o = JSON.parse(localStorage.getItem('voltaic.v1'));
    if (!o) return false;
    const d = JSON.parse(o.s); circ = { nid: d.nid, comps: d.comps, wires: d.wires };
    if (!circ.comps.length && !circ.wires.length) return false;
    setTimescale(o.ts || 1); return true;
  } catch (e) { return false; }
}

function rebuild() {
  sim = new Sim(circ);
  vscale = 0.5;
  setStatus();
}

/* =====================================================================
   Drawing — components (local coords in px, origin at component centre)
   ===================================================================== */
const BOX = {
  R: [0, 0, 32, 13], POT: [0, -8, 32, 24], C: [0, 0, 32, 18], L: [0, 0, 32, 13], SW: [0, 0, 32, 14], LAMP: [0, 0, 32, 20],
  MCU: [0, 0, 62, 98],
  V: [0, 0, 18, 32], AC: [0, 0, 20, 32], I: [0, 0, 20, 32], GND: [0, 8, 18, 14], D: [0, 0, 32, 14], LED: [0, 0, 32, 20], ZD: [0, 0, 32, 14],
  NPN: [-2, 0, 24, 34], PNP: [-2, 0, 24, 34], OP: [5, 0, 52, 46], PROBE: [0, 0, 10, 10],
};
const BODY = { R: 22, C: 5, L: 24, SW: 14, LAMP: 16, D: 8, LED: 8, ZD: 10, V: 5, AC: 18, I: 18 };

function line(c, x1, y1, x2, y2) { c.beginPath(); c.moveTo(x1, y1); c.lineTo(x2, y2); c.stroke(); }
function waveGlyph(c, wave, r) {
  c.beginPath();
  if (wave === 'square') { c.moveTo(-r, .5 * r); c.lineTo(-r, -.5 * r); c.lineTo(0, -.5 * r); c.lineTo(0, .5 * r); c.lineTo(r, .5 * r); }
  else if (wave === 'triangle') { c.moveTo(-r, 0); c.lineTo(-r / 2, -.55 * r); c.lineTo(r / 2, .55 * r); c.lineTo(r, 0); }
  else if (wave === 'saw') { c.moveTo(-r, .5 * r); c.lineTo(0, -.5 * r); c.lineTo(0, .5 * r); c.lineTo(r, -.5 * r); }
  else for (let i = 0; i <= 24; i++) { const x = -r + 2 * r * i / 24, y = -.55 * r * Math.sin(2 * Math.PI * i / 24); i ? c.lineTo(x, y) : c.moveTo(x, y); }
  c.stroke();
}
function arrowHead(c, x, y, ang, s = 5) {
  c.beginPath(); c.moveTo(x, y);
  c.lineTo(x - s * Math.cos(ang - .45), y - s * Math.sin(ang - .45));
  c.lineTo(x - s * Math.cos(ang + .45), y - s * Math.sin(ang + .45)); c.closePath(); c.fill();
}
function glow(c, r, rgb, a, rad = 36) {
  if (a <= 0.01) return;
  const g = c.createRadialGradient(0, 0, 2, 0, 0, rad);
  g.addColorStop(0, `rgba(${rgb[0]},${rgb[1]},${rgb[2]},${0.85 * a})`);
  g.addColorStop(0.35, `rgba(${rgb[0]},${rgb[1]},${rgb[2]},${0.35 * a})`);
  g.addColorStop(1, `rgba(${rgb[0]},${rgb[1]},${rgb[2]},0)`);
  c.fillStyle = g; c.beginPath(); c.arc(0, 0, rad, 0, 7); c.fill();
}

const DRAW = {
  R(c, k) { line(c, -40, 0, -22, 0); line(c, 22, 0, 40, 0); c.beginPath(); c.roundRect(-22, -8, 44, 16, 4); c.fillStyle = 'rgba(124,140,255,.10)'; c.fill(); c.stroke(); },
  POT(c, k) {
    DRAW.R(c, k);
    const w = k.p.w, xw = -22 + 44 * w;
    c.fillStyle = c.strokeStyle;
    line(c, 0, -40, 0, -26); line(c, 0, -26, xw, -26); line(c, xw, -26, xw, -12); arrowHead(c, xw, -9, Math.PI / 2, 5);
  },
  C(c, k) {
    line(c, -40, 0, -5, 0); line(c, 5, 0, 40, 0);
    const v = k.m ? k.m.v : 0, col = vcolor(v, Math.max(vscale, .2), 1);
    c.lineWidth = 3.2;
    c.strokeStyle = v > 0.05 * vscale ? col : c.strokeStyle; line(c, -5, -14, -5, 14);
    c.strokeStyle = v < -0.05 * vscale ? col : (v > 0.05 * vscale ? vcolor(-v * .3, vscale) : c.strokeStyle); line(c, 5, -14, 5, 14);
  },
  L(c, k) {
    line(c, -40, 0, -24, 0); line(c, 24, 0, 40, 0);
    c.beginPath(); c.moveTo(-24, 0);
    for (let i = 0; i < 4; i++) c.arc(-18 + 12 * i, 0, 6, Math.PI, 0);
    c.stroke();
  },
  SW(c, k) {
    line(c, -40, 0, -14, 0); line(c, 14, 0, 40, 0);
    c.fillStyle = c.strokeStyle; c.beginPath(); c.arc(-14, 0, 3, 0, 7); c.arc(14, 0, 3, 0, 7); c.fill();
    c.lineWidth = 2.8; if (k.p.closed) line(c, -14, 0, 14, 0); else line(c, -14, 0, 11, -15);
  },
  LAMP(c, k) {
    const P = k.m ? Math.abs(k.m.p) : 0, b = clamp(Math.pow(P / k.p.rated, 0.7), 0, 1);
    glow(c, 0, [255, 214, 120], b, 46);
    line(c, -40, 0, -16, 0); line(c, 16, 0, 40, 0);
    c.beginPath(); c.arc(0, 0, 16, 0, 7); c.fillStyle = `rgba(255,220,130,${0.05 + 0.55 * b})`; c.fill(); c.stroke();
    line(c, -11, -11, 11, 11); line(c, -11, 11, 11, -11);
  },
  V(c, k) {
    line(c, 0, -40, 0, -5); line(c, 0, 5, 0, 40);
    c.lineWidth = 3.2; line(c, -14, -5, 14, -5); line(c, -8, 5, 8, 5); c.lineWidth = 2;
    line(c, 17, -14, 25, -14); line(c, 21, -18, 21, -10);
  },
  AC(c, k) {
    line(c, 0, -40, 0, -18); line(c, 0, 18, 0, 40);
    c.beginPath(); c.arc(0, 0, 18, 0, 7); c.fillStyle = 'rgba(124,140,255,.10)'; c.fill(); c.stroke();
    c.lineWidth = 1.8; waveGlyph(c, k.p.wave, 10);
  },
  I(c, k) {
    line(c, 0, -40, 0, -18); line(c, 0, 18, 0, 40);
    c.beginPath(); c.arc(0, 0, 18, 0, 7); c.fillStyle = 'rgba(124,140,255,.10)'; c.fill(); c.stroke();
    c.fillStyle = c.strokeStyle; line(c, 0, -9, 0, 6); arrowHead(c, 0, 10, Math.PI / 2, 6);
  },
  GND(c, k) { line(c, 0, 0, 0, 10); line(c, -14, 10, 14, 10); line(c, -9, 15, 9, 15); line(c, -4, 20, 4, 20); },
  D(c, k) {
    line(c, -40, 0, -8, 0); line(c, 8, 0, 40, 0);
    c.beginPath(); c.moveTo(-8, -10); c.lineTo(-8, 10); c.lineTo(8, 0); c.closePath(); c.fillStyle = 'rgba(124,140,255,.12)'; c.fill(); c.stroke();
    c.lineWidth = 2.8; line(c, 8, -10, 8, 10);
  },
  LED(c, k) {
    const col = LED_COLORS[k.p.color] || LED_COLORS.red, i = k.m ? k.m.i : 0;
    const b = clamp(Math.sqrt(Math.max(0, i) / 0.02), 0, 1.2);
    glow(c, 0, col.rgb, Math.min(b, 1), 44);
    line(c, -40, 0, -8, 0); line(c, 8, 0, 40, 0);
    c.beginPath(); c.moveTo(-8, -10); c.lineTo(-8, 10); c.lineTo(8, 0); c.closePath();
    c.fillStyle = `rgba(${col.rgb[0]},${col.rgb[1]},${col.rgb[2]},${0.12 + 0.75 * Math.min(b, 1)})`; c.fill(); c.stroke();
    c.lineWidth = 2.8; line(c, 8, -10, 8, 10); c.lineWidth = 1.6;
    c.fillStyle = c.strokeStyle;
    line(c, -2, -12, 6, -22); arrowHead(c, 7, -23, -Math.PI / 4, 4);
    line(c, 5, -9, 13, -19); arrowHead(c, 14, -20, -Math.PI / 4, 4);
  },
  ZD(c, k) {
    line(c, -40, 0, -8, 0); line(c, 8, 0, 40, 0);
    c.beginPath(); c.moveTo(-8, -10); c.lineTo(-8, 10); c.lineTo(8, 0); c.closePath(); c.fillStyle = 'rgba(124,140,255,.12)'; c.fill(); c.stroke();
    c.lineWidth = 2.8; c.beginPath(); c.moveTo(4, -13); c.lineTo(8, -10); c.lineTo(8, 10); c.lineTo(12, 13); c.stroke();
  },
  NPN(c, k) {
    const pnp = k.type === 'PNP';
    c.beginPath(); c.arc(2, 0, 29, 0, 7); c.fillStyle = 'rgba(124,140,255,.07)'; c.fill(); c.lineWidth = 1.4; c.stroke(); c.lineWidth = 2;
    line(c, -40, 0, -10, 0); c.lineWidth = 3.2; line(c, -10, -17, -10, 17); c.lineWidth = 2;
    line(c, -10, -9, 20, -24); line(c, 20, -24, 20, -40);
    line(c, -10, 9, 20, 24); line(c, 20, 24, 20, 40);
    c.fillStyle = c.strokeStyle;
    if (!pnp) arrowHead(c, 20, 24, Math.atan2(15, 30), 7);
    else arrowHead(c, -7, 7.6, Math.atan2(-15, -30), 7);
  },
  OP(c, k) {
    c.beginPath(); c.moveTo(-50, -50); c.lineTo(60, 0); c.lineTo(-50, 50); c.closePath();
    c.fillStyle = 'rgba(124,140,255,.09)'; c.fill(); c.stroke();
    line(c, -60, -20, -50, -20); line(c, -60, 20, -50, 20);
    c.lineWidth = 1.8; line(c, -42, -20, -34, -20); line(c, -42, 20, -34, 20); line(c, -38, 16, -38, 24);
  },
  MCU(c, k) {
    const mcu = (!k.icon && sim && sim.mcus) ? sim.mcus.get(k.id) : null;
    const bd = BOARDS[k.p.board] || BOARDS.esp32;
    c.beginPath(); c.roundRect(-60, -96, 120, 192, 10);
    const gr = c.createLinearGradient(0, -96, 0, 96);
    gr.addColorStop(0, 'rgba(34,211,238,.13)'); gr.addColorStop(1, 'rgba(124,140,255,.09)');
    c.fillStyle = gr; c.fill(); c.stroke();
    c.beginPath(); c.roundRect(-14, -96, 28, 9, 3); c.fillStyle = 'rgba(255,255,255,.18)'; c.fill();     // USB notch
    c.beginPath(); c.roundRect(-16, -30, 32, 60, 6); c.fillStyle = 'rgba(0,0,0,.35)'; c.fill(); c.lineWidth = 1.4; c.stroke(); c.lineWidth = 2;
    c.lineWidth = 1.4; c.beginPath(); c.arc(-9, -22, 2.2, 0, 7); c.stroke();                                // pin-1 marker
    c.lineWidth = 2;
    DEFS.MCU.t.forEach(([gx, gy], i) => {
      const x = gx * G, y = gy * G, s = Math.sign(x);
      line(c, s * 60, y, x, y);
      if (i >= 2) {
        const g = i - 2; let col = '#4b5578';
        if (mcu) { const m = mcu.mode[g]; col = m === 1 ? (mcu.pwm[g] >= 0 ? '#fbbf24' : mcu.out[g] ? '#4ade80' : '#4b5578') : m === 2 ? '#38bdf8' : '#7a84a8'; }
        c.fillStyle = col; c.beginPath(); c.arc(s * 52, y, 3, 0, 7);
        if (col === '#4ade80' || col === '#fbbf24') { c.shadowColor = col; c.shadowBlur = 8; }
        c.fill(); c.shadowBlur = 0;
      }
    });
    if (k.icon) return;
    c.font = '600 9.5px system-ui, sans-serif'; c.textAlign = 'center'; c.textBaseline = 'middle';
    const txt = (s, x, y, col) => { c.save(); c.translate(x, y); c.rotate(-k.rot * Math.PI / 2); c.fillStyle = col; c.fillText(s, 0, 0); c.restore(); };
    DEFS.MCU.t.forEach(([gx, gy], i) => {
      const s = Math.sign(gx), name = i === 0 ? (bd.vcc === 5 ? '5V' : '3V3') : i === 1 ? 'GND' : bd.pin + (i - 2);
      txt(name, s * 35, gy * G, i === 0 ? '#ff8a6b' : i === 1 ? '#7dd3fc' : '#aab3d9');
    });
    c.font = '700 8.5px system-ui, sans-serif'; txt(bd.name.split(' ').pop().toUpperCase(), 0, 0, '#dfe5ff');
  },
  PROBE(c, k) {
    const col = PROBE_COLORS[probeIndex(k) % PROBE_COLORS.length];
    c.beginPath(); c.arc(0, 0, 6, 0, 7); c.fillStyle = col; c.shadowColor = col; c.shadowBlur = 12; c.fill(); c.shadowBlur = 0;
    c.strokeStyle = '#0a0e1e'; c.lineWidth = 1.5; c.stroke();
  },
};
const probeIndex = k => circ.comps.filter(c => c.type === 'PROBE').findIndex(c => c === k || c.id === k.id);

function drawComp(c, k, opts = {}) {
  const t = k.type === 'PNP' ? 'NPN' : k.type;
  c.save();
  c.lineCap = 'round'; c.lineJoin = 'round';
  c.strokeStyle = opts.col || COL.line; c.lineWidth = 2;
  if (opts.sel) { c.shadowColor = COL.accent; c.shadowBlur = 16; }
  DRAW[t](c, k);
  c.restore();
}

function compLabel(k) {
  const p = k.p;
  switch (k.type) {
    case 'R': return fmtEng(p.r, 'Ω');
    case 'POT': return fmtEng(p.r, 'Ω') + ' · ' + Math.round(p.w * 100) + '%';
    case 'C': return fmtEng(p.c, 'F');
    case 'L': return fmtEng(p.l, 'H');
    case 'V': return fmtEng(p.v, 'V');
    case 'AC': return fmtEng(p.amp, 'V') + ' · ' + fmtEng(p.freq, 'Hz');
    case 'I': return fmtEng(p.i, 'A');
    case 'ZD': return fmtEng(p.vz, 'V');
    case 'LAMP': return fmtEng(p.r, 'Ω');
    case 'SW': return p.closed ? 'closed' : 'open';
    default: return '';
  }
}
const isVert = k => ((DEFS[k.type].vert ? 1 : 0) ^ (k.rot & 1)) === 1;

function drawLabels(k) {
  const px = k.x * G, py = k.y * G;
  ctx.font = '11px ' + getComputedStyle(document.body).fontFamily;
  ctx.fillStyle = '#9aa3cc';
  const txt = compLabel(k);
  if (txt) {
    if (isVert(k)) { ctx.textAlign = 'left'; ctx.textBaseline = 'middle'; ctx.fillText(txt, px + 28, py - 7); ctx.fillStyle = '#5f6890'; ctx.fillText(k.name, px + 28, py + 7); }
    else { ctx.textAlign = 'center'; ctx.textBaseline = 'alphabetic'; ctx.fillText(txt, px, py + 34); ctx.fillStyle = '#5f6890'; ctx.fillText(k.name, px, py - 20); }
  } else if (k.type === 'MCU') {
    ctx.fillStyle = '#5f6890'; ctx.textAlign = 'center'; ctx.textBaseline = 'alphabetic';
    const o = (k.rot & 1) ? 0 : -106;
    ctx.fillText(k.name, px, py + (k.rot === 0 ? -106 : k.rot === 2 ? 118 : -106 + (k.rot & 1 ? -30 : 0)));
  } else if (k.type === 'NPN' || k.type === 'PNP' || k.type === 'OP') {
    ctx.fillStyle = '#5f6890'; ctx.textAlign = 'center'; ctx.textBaseline = 'alphabetic';
    ctx.fillText(k.name, px + (k.type === 'OP' ? 6 : 0), py + (k.type === 'OP' ? 64 : 52));
  }
}

function drawProbeLabel(k) {
  const px = k.x * G, py = k.y * G, i = probeIndex(k), col = PROBE_COLORS[i % PROBE_COLORS.length];
  const t = `${k.name}  ${fmtEng(k.m ? k.m.v : 0, 'V')}`;
  ctx.font = '600 11px ' + getComputedStyle(document.body).fontFamily;
  const w = ctx.measureText(t).width + 14;
  ctx.fillStyle = 'rgba(8,11,23,.85)'; ctx.strokeStyle = col; ctx.lineWidth = 1.2;
  ctx.beginPath(); ctx.roundRect(px + 9, py - 30, w, 20, 6); ctx.fill(); ctx.stroke();
  ctx.fillStyle = col; ctx.textAlign = 'left'; ctx.textBaseline = 'middle'; ctx.fillText(t, px + 16, py - 20);
}

/* flowing "current" dots */
function dots(x1, y1, x2, y2, ph, sp, i, r) {
  const L = Math.hypot(x2 - x1, y2 - y1); if (L < 1) return;
  const ux = (x2 - x1) / L, uy = (y2 - y1) / L;
  const a = clamp((Math.log10(Math.abs(i)) + 8) / 6, 0.15, 1);
  ctx.fillStyle = `rgba(255,236,150,${0.35 + 0.65 * a})`;
  ctx.beginPath();
  for (let d = ph; d < L; d += sp) { ctx.moveTo(x1 + ux * d + r, y1 + uy * d); ctx.arc(x1 + ux * d, y1 + uy * d, r, 0, 7); }
  ctx.fill();
}
const flowSpeed = i => Math.sign(i) * (22 + 60 * clamp((Math.log10(Math.abs(i)) + 7) / 6, 0, 1));
const DOT_SP = 14;

/* =====================================================================
   Hit testing
   ===================================================================== */
function hitPin(wx, wy) {
  const tol = 10 / cam.z; let best = null, bd = tol;
  for (const c of circ.comps) {
    const n = DEFS[c.type].t.length;
    for (let k = 0; k < n; k++) {
      const [tx, ty] = termPos(c, k); const d = Math.hypot(tx * G - wx, ty * G - wy);
      if (d < bd) { bd = d; best = { x: tx, y: ty, comp: c }; }
    }
  }
  for (const w of circ.wires) for (const [x, y] of [[w.x1, w.y1], [w.x2, w.y2]]) {
    const d = Math.hypot(x * G - wx, y * G - wy);
    if (d < bd - 0.01) { bd = d; best = { x, y, comp: null }; }
  }
  return best;
}
function hitComp(wx, wy) {
  for (let i = circ.comps.length - 1; i >= 0; i--) {
    const c = circ.comps[i];
    const [lx, ly] = rotPt(wx - c.x * G, wy - c.y * G, (4 - c.rot) & 3);
    const [cx, cy, hx, hy] = BOX[c.type];
    if (Math.abs(lx - cx) <= hx && Math.abs(ly - cy) <= hy) return c;
  }
  return null;
}
function hitWire(wx, wy) {
  const tol = 7 / cam.z; let best = null, bd = tol;
  for (const w of circ.wires) {
    const x1 = w.x1 * G, y1 = w.y1 * G, dx = w.x2 * G - x1, dy = w.y2 * G - y1, l2 = dx * dx + dy * dy;
    if (!l2) continue;
    const t = clamp(((wx - x1) * dx + (wy - y1) * dy) / l2, 0, 1);
    const d = Math.hypot(wx - (x1 + t * dx), wy - (y1 + t * dy));
    if (d < bd) { bd = d; best = w; }
  }
  return best;
}

/* =====================================================================
   Rendering
   ===================================================================== */
function drawGrid() {
  const step = cam.z * G < 11 ? G * 2 : G;
  const x0 = Math.floor(-cam.x / cam.z / step) * step, y0 = Math.floor(-cam.y / cam.z / step) * step;
  const x1 = (W - cam.x) / cam.z, y1 = (H - cam.y) / cam.z;
  ctx.fillStyle = 'rgba(150,165,255,.22)';
  const r = Math.max(.9, 1.15 / cam.z * Math.min(cam.z, 1.2));
  ctx.beginPath();
  for (let x = x0; x <= x1; x += step) for (let y = y0; y <= y1; y += step) ctx.rect(x - r / 2, y - r / 2, r, r);
  ctx.fill();
}

function route(sx, sy, ex, ey, flip) {
  if (sx === ex || sy === ey) return [[sx, sy], [ex, ey]];
  const hFirst = (Math.abs(ex - sx) >= Math.abs(ey - sy)) !== !!flip;
  return hFirst ? [[sx, sy], [ex, sy], [ex, ey]] : [[sx, sy], [sx, ey], [ex, ey]];
}

let lastTs = 0;
function render(dtw) {
  ctx.setTransform(dpr, 0, 0, dpr, 0, 0);
  ctx.clearRect(0, 0, W, H);
  ctx.save();
  ctx.translate(cam.x, cam.y); ctx.scale(cam.z, cam.z);
  drawGrid();
  ctx.lineCap = 'round'; ctx.lineJoin = 'round';

  // voltage scale
  let mx = 0; if (sim) for (let i = 1; i < sim.nodeV.length; i++) mx = Math.max(mx, Math.abs(sim.nodeV[i]));
  vscale = Math.max(mx, vscale * 0.985, 0.2);

  if (sim) {
    // wires
    for (const s of sim.segs) {
      const v = sim.nodeV[s.node];
      ctx.strokeStyle = vcolor(v, vscale, 0.16); ctx.lineWidth = 9; line(ctx, s.x1, s.y1, s.x2, s.y2);
    }
    for (const s of sim.segs) {
      ctx.strokeStyle = vcolor(sim.nodeV[s.node], vscale, 1); ctx.lineWidth = 2.6; line(ctx, s.x1, s.y1, s.x2, s.y2);
    }
    // selected wire
    if (sel && sel.k === 'w') {
      ctx.strokeStyle = 'rgba(255,255,255,.55)'; ctx.lineWidth = 6;
      for (const s of sim.segs) if (circ.wires[s.w] && circ.wires[s.w].id === sel.id) line(ctx, s.x1, s.y1, s.x2, s.y2);
    }
    // current dots
    for (const s of sim.segs) {
      if (Math.abs(s.i) < 1e-8) continue;
      if (running) { s.ph += flowSpeed(s.i) * dtw; s.ph = ((s.ph % DOT_SP) + DOT_SP) % DOT_SP; }
      dots(s.x1, s.y1, s.x2, s.y2, s.ph, DOT_SP, s.i, 2);
    }
    // junctions
    for (const j of sim.junctions) {
      ctx.fillStyle = vcolor(sim.nodeV[j.node], vscale, 1);
      ctx.beginPath(); ctx.arc(j.x, j.y, 4.2, 0, 7); ctx.fill();
    }
  }

  // components
  for (const k of circ.comps) {
    const isSel = sel && sel.k === 'c' && sel.id === k.id;
    ctx.save();
    ctx.translate(k.x * G, k.y * G); ctx.rotate(k.rot * Math.PI / 2);
    if (isSel) {
      const [cx, cy, hx, hy] = BOX[k.type];
      ctx.fillStyle = 'rgba(124,140,255,.10)'; ctx.strokeStyle = 'rgba(124,140,255,.55)'; ctx.lineWidth = 1; ctx.setLineDash([4, 4]);
      ctx.beginPath(); ctx.roundRect(cx - hx - 3, cy - hy - 3, hx * 2 + 6, hy * 2 + 6, 8); ctx.fill(); ctx.stroke(); ctx.setLineDash([]);
    }
    drawComp(ctx, k, { sel: isSel });
    // lead dots for 2-terminal elements
    if (sim && BODY[k.type] && k.m && Math.abs(k.m.i) > 1e-8 && DEFS[k.type].t.length === 2) {
      const bh = BODY[k.type], flipI = (k.type === 'V' || k.type === 'AC') ? -1 : 1;
      const i = k.m.i * flipI;
      k.ph = (k.ph || 0);
      if (running) { k.ph += flowSpeed(i) * dtw; k.ph = ((k.ph % DOT_SP) + DOT_SP) % DOT_SP; }
      ctx.save();
      if (DEFS[k.type].vert) ctx.rotate(-Math.PI / 2);
      // positions along t0 -> t1 axis (x axis in local frame)
      const ph = k.ph;
      ctx.fillStyle = `rgba(255,236,150,${0.35 + 0.65 * clamp((Math.log10(Math.abs(i)) + 8) / 6, .15, 1)})`;
      ctx.beginPath();
      for (let d = ph - 40; d <= 40; d += DOT_SP) {
        if (Math.abs(d) < bh) continue;
        ctx.moveTo(d + 2, 0); ctx.arc(d, 0, 2, 0, 7);
      }
      ctx.fill(); ctx.restore();
    }
    ctx.restore();
  }
  // pins
  for (const k of circ.comps) {
    const n = DEFS[k.type].t.length;
    if (k.type === 'PROBE' || k.type === 'GND') continue;
    for (let i = 0; i < n; i++) {
      const [tx, ty] = termPos(k, i);
      ctx.fillStyle = '#0a0e1e'; ctx.strokeStyle = sim && sim.nodeV ? vcolor(sim.nodeV[sim.net.ptNode[sim.net.cp[circ.comps.indexOf(k)][i]]], vscale, 1) : COL.line;
      ctx.lineWidth = 1.8; ctx.beginPath(); ctx.arc(tx * G, ty * G, 3.2, 0, 7); ctx.fill(); ctx.stroke();
    }
  }
  for (const k of circ.comps) drawLabels(k);
  for (const k of circ.comps) if (k.type === 'PROBE') drawProbeLabel(k);

  // interactive overlays
  const showPins = (!armed && !palDrag) || wireTool;
  if (hoverPin && showPins && !drag) {
    ctx.strokeStyle = '#22d3ee'; ctx.lineWidth = 2; ctx.shadowColor = '#22d3ee'; ctx.shadowBlur = 12;
    ctx.beginPath(); ctx.arc(hoverPin.x * G, hoverPin.y * G, 7, 0, 7); ctx.stroke(); ctx.shadowBlur = 0;
  }
  if (drag && drag.mode === 'wire') {
    const pts = route(drag.sx, drag.sy, mouse.gx, mouse.gy, drag.flip);
    ctx.strokeStyle = '#22d3ee'; ctx.lineWidth = 2.6; ctx.setLineDash([6, 5]);
    ctx.beginPath(); pts.forEach((p, i) => i ? ctx.lineTo(p[0] * G, p[1] * G) : ctx.moveTo(p[0] * G, p[1] * G)); ctx.stroke(); ctx.setLineDash([]);
    ctx.fillStyle = '#22d3ee'; ctx.beginPath(); ctx.arc(mouse.gx * G, mouse.gy * G, 4, 0, 7); ctx.fill();
  }
  if ((armed || palDrag) && mouse.over) {
    ctx.save(); ctx.globalAlpha = 0.7;
    ctx.translate(mouse.gx * G, mouse.gy * G); ctx.rotate(placeRot * Math.PI / 2);
    drawComp(ctx, { type: armed, rot: placeRot, p: structuredClone(DEFS[armed].p), m: null, name: '' }, { col: '#22d3ee' });
    ctx.restore();
  } else if (wireTool && mouse.over && !drag) {
    ctx.fillStyle = '#22d3ee'; ctx.beginPath(); ctx.arc(mouse.gx * G, mouse.gy * G, 4, 0, 7); ctx.fill();
  }
  ctx.restore();
}

/* =====================================================================
   Pointer interaction
   ===================================================================== */
function updateMouse(e) {
  const r = cv.getBoundingClientRect();
  mouse.sx = e.clientX - r.left; mouse.sy = e.clientY - r.top;
  mouse.over = mouse.sx >= 0 && mouse.sy >= 0 && mouse.sx <= r.width && mouse.sy <= r.height;
  [mouse.wx, mouse.wy] = s2w(mouse.sx, mouse.sy);
  mouse.gx = Math.round(mouse.wx / G); mouse.gy = Math.round(mouse.wy / G);
}
const overUI = e => !!e.target.closest && !!e.target.closest('#inspector, #scope, #top, #palette');

cv.addEventListener('contextmenu', e => e.preventDefault());
cv.addEventListener('pointerdown', e => {
  updateMouse(e); cv.setPointerCapture(e.pointerId);
  if (e.button === 1 || e.button === 2 || spaceDown) { drag = { mode: 'pan', sx: mouse.sx, sy: mouse.sy, cx: cam.x, cy: cam.y }; return; }
  if (e.button !== 0) return;
  if (armed) { placeComp(armed, mouse.gx, mouse.gy, e.shiftKey); return; }
  if (wireTool) { drag = { mode: 'wire', sx: mouse.gx, sy: mouse.gy, moved: false, flip: e.shiftKey, comp: null }; return; }
  const pin = hitPin(mouse.wx, mouse.wy);
  if (pin) { drag = { mode: 'wire', sx: pin.x, sy: pin.y, moved: false, flip: e.shiftKey, comp: pin.comp }; return; }
  const c = hitComp(mouse.wx, mouse.wy);
  if (c) {
    sel = { k: 'c', id: c.id }; renderInspector();
    const att = [];
    DEFS[c.type].t.forEach((_, k) => {
      const [tx, ty] = termPos(c, k);
      for (const w of circ.wires) {
        if (w.x1 === tx && w.y1 === ty) att.push({ w, end: 1, k });
        if (w.x2 === tx && w.y2 === ty) att.push({ w, end: 2, k });
      }
    });
    drag = { mode: 'move', c, gx: mouse.gx, gy: mouse.gy, ox: c.x, oy: c.y, att, moved: false };
    return;
  }
  const w = hitWire(mouse.wx, mouse.wy);
  if (w) { sel = { k: 'w', id: w.id }; renderInspector(); return; }
  sel = null; renderInspector();
  drag = { mode: 'pan', sx: mouse.sx, sy: mouse.sy, cx: cam.x, cy: cam.y };
});

window.addEventListener('pointermove', e => {
  updateMouse(e);
  if (!drag) {
    hoverPin = (mouse.over && !overUI(e)) ? hitPin(mouse.wx, mouse.wy) : null;
    const c = (!armed && mouse.over) ? hitComp(mouse.wx, mouse.wy) : null;
    cv.style.cursor = armed || wireTool ? 'crosshair' : hoverPin ? 'crosshair' : c ? (c.type === 'SW' ? 'pointer' : 'move') : 'default';
    return;
  }
  if (drag.mode === 'pan') { cam.x = drag.cx + (mouse.sx - drag.sx); cam.y = drag.cy + (mouse.sy - drag.sy); cv.style.cursor = 'grabbing'; }
  else if (drag.mode === 'wire') { if (mouse.gx !== drag.sx || mouse.gy !== drag.sy) drag.moved = true; drag.flip = e.shiftKey; }
  else if (drag.mode === 'move') {
    const dx = mouse.gx - drag.gx, dy = mouse.gy - drag.gy;
    const c = drag.c;
    if (!drag.moved && (dx || dy)) drag.moved = true;
    if (drag.moved) {
      c.x = drag.ox + dx; c.y = drag.oy + dy;
      for (const a of drag.att) { const [tx, ty] = termPos(c, a.k); if (a.end === 1) { a.w.x1 = tx; a.w.y1 = ty; } else { a.w.x2 = tx; a.w.y2 = ty; } }
      rebuild();
    }
  }
});

window.addEventListener('pointerup', e => {
  updateMouse(e);
  if (palDrag) {
    palDrag = false;
    if (mouse.over && !overUI(e) && armed) placeComp(armed, mouse.gx, mouse.gy, e.shiftKey);
    return;
  }
  if (!drag) return;
  const d = drag; drag = null;
  cv.style.cursor = 'default';
  if (d.mode === 'wire') {
    if (d.moved && (mouse.gx !== d.sx || mouse.gy !== d.sy)) {
      const pts = route(d.sx, d.sy, mouse.gx, mouse.gy, e.shiftKey);
      addPoly(pts); commit();
    } else if (d.comp) { sel = { k: 'c', id: d.comp.id }; renderInspector(); }
  } else if (d.mode === 'move') {
    if (d.moved) commit();
    else if (d.c.type === 'SW') { d.c.p.closed = !d.c.p.closed; sim && (sim.be = 2); commit(false); renderInspector(); }
  }
});

cv.addEventListener('wheel', e => {
  e.preventDefault(); updateMouse(e);
  const f = Math.exp(-e.deltaY * 0.0015), nz = clamp(cam.z * f, 0.3, 3.5);
  cam.x = mouse.sx - (mouse.sx - cam.x) * (nz / cam.z); cam.y = mouse.sy - (mouse.sy - cam.y) * (nz / cam.z); cam.z = nz;
}, { passive: false });

function placeComp(type, gx, gy, keep) {
  const c = addComp(type, gx, gy, placeRot);
  sel = { k: 'c', id: c.id };
  if (!keep) { armed = null; refreshPalette(); }
  commit(); renderInspector();
}

function deleteSel() {
  if (!sel) return;
  if (sel.k === 'c') circ.comps = circ.comps.filter(c => c.id !== sel.id);
  else circ.wires = circ.wires.filter(w => w.id !== sel.id);
  sel = null; commit(); renderInspector();
}
function rotateSel() {
  if (armed) { placeRot = (placeRot + 1) & 3; return; }
  if (!sel || sel.k !== 'c') return;
  const c = compById(sel.id), before = DEFS[c.type].t.map((_, k) => termPos(c, k));
  c.rot = (c.rot + 1) & 3;
  // keep attached wires glued to the pins
  DEFS[c.type].t.forEach((_, k) => {
    const [ox, oy] = before[k], [nx, ny] = termPos(c, k);
    for (const w of circ.wires) {
      if (w.x1 === ox && w.y1 === oy) { w.x1 = nx; w.y1 = ny; }
      if (w.x2 === ox && w.y2 === oy) { w.x2 = nx; w.y2 = ny; }
    }
  });
  commit();
}

window.addEventListener('keydown', e => {
  const typing = /INPUT|SELECT|TEXTAREA/.test(document.activeElement.tagName) && document.activeElement.type !== 'range';
  if (typing) { if (document.activeElement.tagName !== 'TEXTAREA' && (e.key === 'Enter' || e.key === 'Escape')) document.activeElement.blur(); return; }
  const k = e.key.toLowerCase();
  if (e.ctrlKey || e.metaKey) {
    if (k === 'z') { e.preventDefault(); e.shiftKey ? redo() : undo(); }
    else if (k === 'y') { e.preventDefault(); redo(); }
    return;
  }
  if (e.key === ' ') { e.preventDefault(); spaceDown = true; if (!e.repeat) toggleRun(); }
  else if (k === 'r') rotateSel();
  else if (k === 'w') { wireTool = !wireTool; armed = null; refreshPalette(); }
  else if (e.key === 'Delete' || e.key === 'Backspace') { e.preventDefault(); deleteSel(); }
  else if (e.key === 'Escape') { armed = null; wireTool = false; palDrag = false; drag = null; sel = null; refreshPalette(); renderInspector(); }
  else if (e.key === 'Home') fitView();
});
window.addEventListener('keyup', e => { if (e.key === ' ') spaceDown = false; });

function fitView() {
  let x0 = 1e9, y0 = 1e9, x1 = -1e9, y1 = -1e9;
  const add = (x, y) => { x0 = Math.min(x0, x); y0 = Math.min(y0, y); x1 = Math.max(x1, x); y1 = Math.max(y1, y); };
  for (const c of circ.comps) { const [cx, cy, hx, hy] = BOX[c.type]; add(c.x * G - 60, c.y * G - 60); add(c.x * G + 60, c.y * G + 60); }
  for (const w of circ.wires) { add(w.x1 * G, w.y1 * G); add(w.x2 * G, w.y2 * G); }
  if (x0 > x1) { cam.z = 1; cam.x = W / 2; cam.y = H / 2; return; }
  const scopeH = $('#scope').classList.contains('collapsed') ? 60 : 270;
  const aw = W - 320, ah = H - scopeH - 20;
  cam.z = clamp(Math.min(aw / (x1 - x0), ah / (y1 - y0)), 0.4, 1.6);
  cam.x = 20 + (aw - (x1 - x0) * cam.z) / 2 - x0 * cam.z;
  cam.y = 10 + (ah - (y1 - y0) * cam.z) / 2 - y0 * cam.z;
}

/* =====================================================================
   Palette
   ===================================================================== */
const PALETTE = [
  ['Sources', ['V', 'AC', 'I', 'GND']],
  ['Passive', ['R', 'POT', 'C', 'L', 'SW', 'LAMP']],
  ['Semiconductors', ['D', 'LED', 'ZD', 'NPN', 'PNP', 'OP']],
  ['Microcontroller', ['MCU']],
  ['Measure', ['PROBE']],
];
function iconCanvas(type, size = 56, h = 50) {
  const c = document.createElement('canvas'); c.width = size * 2; c.height = h * 2;
  const x = c.getContext('2d'); x.scale(2, 2);
  const k = { type, rot: 0, p: structuredClone(DEFS[type].p), m: null, name: '', id: -1, icon: true };
  if (type === 'LED') k.m = { i: 0.014 };
  if (type === 'LAMP') k.m = { p: 0.12 };
  const [cx, cy, hx, hy] = BOX[type];
  const sc = type === 'MCU' ? (h - 6) / 200 : Math.min((size - 8) / (type === 'OP' ? 130 : 84), (h - 6) / (hy * 2 + 8), 0.62);
  x.translate(size / 2 - cx * sc, h / 2 - cy * sc); x.scale(sc, sc);
  if (type === 'OP') x.translate(-5, 0);
  drawComp(x, k, { col: '#c9d3ff' });
  return c;
}
function buildPalette() {
  const el = $('#palette'); el.innerHTML = '';
  const wb = document.createElement('div'); wb.className = 'pitem wide'; wb.id = 'pal-wire';
  wb.innerHTML = icon('wire') + '<span>Wire tool <kbd>W</kbd></span>';
  wb.onclick = () => { wireTool = !wireTool; armed = null; refreshPalette(); };
  el.appendChild(wb);
  for (const [cat, types] of PALETTE) {
    const h = document.createElement('h4'); h.textContent = cat; el.appendChild(h);
    const g = document.createElement('div'); g.className = 'pgrid'; el.appendChild(g);
    for (const t of types) {
      const it = document.createElement('div'); it.className = 'pitem'; it.dataset.type = t; it.title = DEFS[t].name;
      it.appendChild(iconCanvas(t));
      const s = document.createElement('span'); s.textContent = DEFS[t].name.replace(' Source', '').replace(' Transistor', ''); it.appendChild(s);
      it.addEventListener('pointerdown', e => {
        e.preventDefault();
        if (armed === t && !e.target.closest('.dragging')) { /* re-click keeps armed */ }
        armed = t; wireTool = false; palDrag = true; placeRot = DEFS[t].vert ? 0 : 0; updateMouse(e); refreshPalette();
      });
      g.appendChild(it);
    }
  }
}
function refreshPalette() {
  document.querySelectorAll('.pitem[data-type]').forEach(e => e.classList.toggle('armed', e.dataset.type === armed));
  $('#pal-wire').classList.toggle('armed', wireTool);
  cv.style.cursor = armed || wireTool ? 'crosshair' : 'default';
}

/* =====================================================================
   Inspector
   ===================================================================== */
const FIELDS = {
  R: [{ k: 'r', l: 'Resistance', u: 'Ω', min: 1, max: 1e7 }],
  POT: [{ k: 'r', l: 'Total resistance', u: 'Ω', min: 100, max: 1e6 }, { k: 'w', l: 'Wiper position', min: 0, max: 1, lin: true, pct: true }],
  C: [{ k: 'c', l: 'Capacitance', u: 'F', min: 1e-9, max: 1e-2 }],
  L: [{ k: 'l', l: 'Inductance', u: 'H', min: 1e-6, max: 10 }],
  V: [{ k: 'v', l: 'Voltage', u: 'V', min: -48, max: 48, lin: true }],
  AC: [{ k: 'wave', l: 'Waveform', opts: ['sine', 'square', 'triangle', 'saw'] },
    { k: 'amp', l: 'Amplitude', u: 'V', min: 0.01, max: 100 }, { k: 'freq', l: 'Frequency', u: 'Hz', min: 0.1, max: 1e6 },
    { k: 'off', l: 'DC offset', u: 'V', min: -50, max: 50, lin: true }],
  I: [{ k: 'i', l: 'Current', u: 'A', min: -0.1, max: 0.1, lin: true }],
  SW: [{ k: 'closed', l: 'Closed', bool: true }],
  LAMP: [{ k: 'r', l: 'Resistance', u: 'Ω', min: 1, max: 1000 }, { k: 'rated', l: 'Rated power', u: 'W', min: 0.01, max: 10 }],
  LED: [{ k: 'color', l: 'Colour', opts: Object.keys(LED_COLORS) }],
  ZD: [{ k: 'vz', l: 'Zener voltage', u: 'V', min: 2, max: 30, lin: true }],
  NPN: [{ k: 'beta', l: 'Gain (β)', min: 20, max: 500, lin: true }],
  PNP: [{ k: 'beta', l: 'Gain (β)', min: 20, max: 500, lin: true }],
  OP: [{ k: 'rail', l: 'Supply rails ±', u: 'V', min: 3, max: 24, lin: true }],
  MCU: [{ k: 'board', l: 'Board', opts: ['esp32', 'uno'] }],
};
const s2v = (f, s) => f.lin ? f.min + (f.max - f.min) * s / 1000 : f.min * Math.pow(f.max / f.min, s / 1000);
const v2s = (f, v) => f.lin ? (v - f.min) / (f.max - f.min) * 1000 : Math.log(clamp(v, f.min, f.max) / f.min) / Math.log(f.max / f.min) * 1000;

function el(tag, cls, html) { const e = document.createElement(tag); if (cls) e.className = cls; if (html != null) e.innerHTML = html; return e; }
function setProp(c, k, v) { c.p[k] = v; if (sim) sim.be = 2; }

function renderInspector() {
  const root = $('#inspector'); root.innerHTML = '';
  if (!sel) {
    root.appendChild(el('h3', null, 'Circuit'));
    root.appendChild(el('div', 'sub', `${circ.comps.length} parts · ${sim ? Math.max(0, sim.net.nodeCount - (sim.noGround ? 0 : 1)) : 0} nodes`));
    root.appendChild(el('p', 'tip', 'Select a part to edit its value. Click a switch to toggle it. Drag from any pin to draw a wire; wires connect when they end on a pin or touch another wire end.'));
    root.appendChild(el('div', 'legendbar'));
    root.appendChild(el('div', 'legendrow', '<span>negative V</span><span>0</span><span>positive V</span>'));
    root.appendChild(el('p', 'tip', 'Yellow dots show conventional current flow — faster and brighter means more current.'));
    return;
  }
  if (sel.k === 'w') {
    root.appendChild(el('h3', null, 'Wire'));
    const a = el('div', 'actions'); const b = el('button', 'btn danger', icon('trash') + 'Delete'); b.onclick = deleteSel; a.appendChild(b); root.appendChild(a);
    return;
  }
  const c = compById(sel.id); if (!c) return;
  const d = DEFS[c.type];
  const head = el('div', 'ihead'); head.appendChild(iconCanvas(c.type, 48, 44));
  const hc = el('div'); hc.appendChild(el('h3', null, c.name)); hc.appendChild(el('div', 'sub', d.name)); head.appendChild(hc); root.appendChild(head);

  for (const f of FIELDS[c.type] || []) {
    const fd = el('div', 'field');
    if (f.bool) {
      const t = el('div', 'toggle' + (c.p[f.k] ? ' on' : ''), '<i></i><span>' + (c.p[f.k] ? 'Closed' : 'Open') + '</span>');
      t.onclick = () => { setProp(c, f.k, !c.p[f.k]); commit(false); renderInspector(); };
      fd.appendChild(t);
    } else if (f.opts) {
      fd.appendChild(el('label', null, f.l));
      const s = el('select'); f.opts.forEach(o => { const op = el('option', null, o); op.value = o; s.appendChild(op); }); s.value = c.p[f.k];
      s.onchange = () => { setProp(c, f.k, s.value); commit(false); renderInspector(); };
      fd.appendChild(s);
    } else {
      fd.appendChild(el('label', null, `<span>${f.l}</span>`));
      const row = el('div', 'row');
      const r = el('input'); r.type = 'range'; r.min = 0; r.max = 1000; r.value = v2s(f, c.p[f.k]);
      const t = el('input'); t.type = 'text';
      const show = () => { t.value = f.pct ? Math.round(c.p[f.k] * 100) + ' %' : f.u ? fmtEng(c.p[f.k], f.u) : String(Math.round(c.p[f.k] * 100) / 100); };
      show();
      r.oninput = () => {
        let v = s2v(f, +r.value);
        if (!f.lin || f.pct) { /* keep */ }
        if (f.k === 'beta') v = Math.round(v);
        else if (f.lin && f.u === 'V') v = Math.round(v * 10) / 10;
        else if (!f.lin) v = Number(v.toPrecision(3));
        setProp(c, f.k, v); show();
      };
      r.onchange = () => commit(false);
      t.onchange = () => {
        let v = parseVal(t.value); if (isNaN(v)) { show(); return; }
        if (f.pct) v = clamp(/%/.test(t.value) || v > 1 ? v / 100 : v, 0, 1);
        setProp(c, f.k, v); r.value = v2s(f, v); show(); commit(false);
      };
      row.appendChild(r); row.appendChild(t); fd.appendChild(row);
    }
    root.appendChild(fd);
  }
  if (c.type === 'MCU') {
    const eb = el('button', 'btn primary wide', 'Edit code…'); eb.onclick = () => openEditor(c); root.appendChild(eb);
    root.appendChild(el('div', 'sub serialh', 'Serial monitor'));
    root.appendChild(el('pre', 'serial', '')).id = 'serialBox';
    root.appendChild(el('div', 'mcuerr hidden')).id = 'mcuErr';
  }
  if (c.type !== 'GND') {
    const ro = el('div', 'readouts');
    ro.innerHTML = `<div class="r"><span>Voltage</span><span id="rv-v">—</span></div><div class="r"><span>Current</span><span id="rv-i">—</span></div><div class="r"><span id="rv-pl">Power</span><span id="rv-p">—</span></div>`;
    if (c.type === 'PROBE') ro.innerHTML = `<div class="r"><span>Node voltage</span><span id="rv-v">—</span></div>`;
    root.appendChild(ro);
  }
  const a = el('div', 'actions');
  const b1 = el('button', 'btn', icon('rotate') + 'Rotate'); b1.onclick = rotateSel;
  const b2 = el('button', 'btn danger', icon('trash') + 'Delete'); b2.onclick = deleteSel;
  a.appendChild(b1); a.appendChild(b2); root.appendChild(a);
  updateLive();
}

function updateLive() {
  if (!sel || sel.k !== 'c') return;
  const c = compById(sel.id); if (!c || !c.m) return;
  const set = (id, t) => { const e = document.getElementById(id); if (e) e.textContent = t; };
  set('rv-v', fmtEng(c.m.v, 'V')); set('rv-i', fmtEng(c.m.i, 'A')); set('rv-p', fmtEng(Math.abs(c.m.p), 'W'));
  const gen = c.type === 'V' || c.type === 'AC' || c.type === 'I' || c.type === 'MCU';
  set('rv-pl', gen ? 'Power delivered' : 'Power dissipated');
  if (c.type === 'MCU' && sim && sim.mcus.get(c.id)) {
    const m = sim.mcus.get(c.id), box = document.getElementById('serialBox'), eb = document.getElementById('mcuErr');
    if (box) { const txt = m.serial.slice(-40).join('\n') + (m.cur ? '\n' + m.cur : ''); if (box.textContent !== txt) { box.textContent = txt; box.scrollTop = box.scrollHeight; } }
    if (eb) { eb.classList.toggle('hidden', !m.err); eb.textContent = m.err || ''; }
  }
}

/* ---------- code editor ---------- */
let edComp = null;
function openEditor(c) {
  edComp = c;
  $('#edTitle').textContent = c.name + ' — sketch';
  $('#edText').value = c.p.code || '';
  $('#editor').classList.remove('hidden');
  edLang(); edMsg(); $('#edText').focus();
}
function edLang() { const t = $('#edText').value; $('#edLang').textContent = CPP.isCpp(t) ? 'C++' : 'JavaScript'; $('#edExport').hidden = !CPP.isCpp(t); }
function exportSketch() {
  const a = document.createElement('a'); a.href = URL.createObjectURL(new Blob([$('#edText').value], { type: 'text/plain' }));
  a.download = ((edComp && edComp.name) || 'sketch').replace(/\W+/g, '_') + '.ino'; a.click(); URL.revokeObjectURL(a.href); toast('Sketch downloaded (.ino)');
}
function closeEditor() { $('#editor').classList.add('hidden'); edComp = null; }
function edMsg() {
  const m = edComp && sim && sim.mcus.get(edComp.id), e = $('#edMsg');
  if (!m) { e.textContent = ''; return; }
  e.className = m.err ? 'bad' : 'good'; e.textContent = m.err ? '✗ ' + m.err : '✓ Running';
}
function applyEditor() {
  if (!edComp) return;
  edComp.p.code = $('#edText').value;
  commit(); renderInspector(); edMsg();
  const m = sim.mcus.get(edComp.id);
  if (m && !m.err) { running = true; updateRunButton(); toast('Sketch uploaded'); }
}
function wireEditor() {
  const ex = $('#edExamples'); ex.innerHTML = '<option value="">Load example…</option>';
  const names = { blink: 'Blink', button: 'Button → LED', fade: 'PWM fade', adc: 'Analog read + serial', helper: 'Own function with delay()' };
  for (const k in SKETCHES) { const o = el('option', null, names[k] || k); o.value = k; ex.appendChild(o); }
  ex.onchange = () => { if (ex.value) { $('#edText').value = SKETCHES[ex.value]; edLang(); } ex.value = ''; };
  $('#edText').addEventListener('input', edLang); $('#edExport').onclick = exportSketch;
  $('#edClose').onclick = closeEditor; $('#edApply').onclick = applyEditor;
  $('#editor').addEventListener('pointerdown', e => { if (e.target.id === 'editor') closeEditor(); });
  $('#edText').addEventListener('keydown', e => {
    if (e.key === 'Tab') { e.preventDefault(); const t = e.target, s = t.selectionStart; t.setRangeText('  ', s, t.selectionEnd, 'end'); }
    else if (e.key === 'Enter' && (e.ctrlKey || e.metaKey)) { e.preventDefault(); applyEditor(); }
    else if (e.key === 'Escape') closeEditor();
  });
}

/* =====================================================================
   Scope
   ===================================================================== */
const sc = $('#sc'), sctx = sc.getContext('2d');
let scW = 0, scH = 0, legendKey = '';

function niceTicks(lo, hi, n = 4) {
  if (!(hi > lo)) { hi = lo + 1; lo = lo - 1; }
  const raw = (hi - lo) / n, mag = Math.pow(10, Math.floor(Math.log10(raw))), f = raw / mag;
  const step = (f < 1.5 ? 1 : f < 3.5 ? 2 : f < 7.5 ? 5 : 10) * mag;
  const a = Math.floor(lo / step) * step, b = Math.ceil(hi / step) * step, t = [];
  for (let v = a; v <= b + step * 0.01; v += step) t.push(Math.abs(v) < step * 1e-6 ? 0 : v);
  return t;
}

function scopeChannels() {
  const ch = [];
  if (!sim) return ch;
  sim.probes.forEach((p) => {
    const h = sim.hist.ch.get(p.c.id);
    ch.push({ name: p.c.name, col: PROBE_COLORS[probeIndex(p.c) % PROBE_COLORS.length], data: h.v, axis: 'v', live: p.c.m.v, unit: 'V' });
  });
  if (sel && sel.k === 'c') {
    const c = compById(sel.id), h = c && sim.hist.ch.get(c.id);
    if (h && c.type !== 'PROBE') {
      ch.push({ name: c.name + ' V', col: '#e8ebff', data: h.v, axis: 'v', live: c.m.v, unit: 'V' });
      ch.push({ name: c.name + ' I', col: '#fbbf24', data: h.i, axis: 'i', live: c.m.i, unit: 'A', dash: true });
    }
  }
  return ch;
}

function drawScope() {
  const c = sctx, w = scW, h = scH;
  c.setTransform(dpr, 0, 0, dpr, 0, 0); c.clearRect(0, 0, w, h);
  if ($('#scope').classList.contains('collapsed') || !sim) return;
  const chs = scopeChannels();
  const key = chs.map(k => k.name + k.col).join('|');
  const lg = $('#scopeLegend');
  if (key !== legendKey) { legendKey = key; lg.innerHTML = chs.map((k, i) => `<span class="chip"><i style="background:${k.col}"></i>${k.name} <span data-lv="${i}"></span></span>`).join(''); }
  chs.forEach((k, i) => { const e = lg.querySelector(`[data-lv="${i}"]`); if (e) e.textContent = fmtEng(k.live, k.unit); });
  const H_ = sim.hist, n = Math.min(H_.n, H_.cap);
  const hasI = chs.some(k => k.axis === 'i');
  const L = 54, R = hasI ? 54 : 12, T = 6, B = 20, pw = w - L - R, ph = h - T - B;
  c.font = '10.5px ' + getComputedStyle(document.body).fontFamily;
  if (!chs.length || n < 2) {
    c.fillStyle = '#6b7599'; c.textAlign = 'center'; c.fillText(chs.length ? 'Waiting for data…' : 'Add a scope probe, or select a part to see its voltage & current', w / 2, h / 2); return;
  }
  const start = H_.n - n, stride = Math.max(1, Math.floor(n / pw));
  const idx = k => (start + k) % H_.cap;
  const t0 = H_.t[idx(0)], t1 = H_.t[idx(n - 1)], dtT = Math.max(t1 - t0, 1e-12);
  const range = ax => {
    let lo = 1e30, hi = -1e30;
    for (const ch of chs) if (ch.axis === ax) for (let k = 0; k < n; k += stride) { const v = ch.data[idx(k)]; if (v < lo) lo = v; if (v > hi) hi = v; }
    if (lo > hi) return null;
    if (hi - lo < 1e-9) { lo -= 0.5 * Math.max(Math.abs(lo), 1e-3); hi += 0.5 * Math.max(Math.abs(hi), 1e-3); }
    const pad = (hi - lo) * 0.08; return [lo - pad, hi + pad];
  };
  const rv = range('v'), ri = range('i');
  const X = t => L + (t - t0) / dtT * pw;
  // grid
  const drawAxis = (rg, side, col) => {
    if (!rg) return null;
    const ticks = niceTicks(rg[0], rg[1], 4), lo = ticks[0], hi = ticks[ticks.length - 1];
    const Y = v => T + ph - (v - lo) / (hi - lo) * ph;
    ticks.forEach(v => {
      const y = Y(v);
      if (side === 'l') { c.strokeStyle = v === 0 ? 'rgba(255,255,255,.22)' : 'rgba(255,255,255,.07)'; c.lineWidth = 1; c.beginPath(); c.moveTo(L, y); c.lineTo(L + pw, y); c.stroke(); }
      c.fillStyle = col; c.textAlign = side === 'l' ? 'right' : 'left'; c.textBaseline = 'middle';
      c.fillText(fmtEng(v, '', 2), side === 'l' ? L - 6 : L + pw + 6, y);
    });
    return Y;
  };
  const Yv = drawAxis(rv, 'l', '#8a93b8'), Yi = drawAxis(ri, 'r', '#c9a227');
  const tt = niceTicks(0, dtT, 5);
  c.textBaseline = 'alphabetic';
  for (const tk of tt) {
    if (tk < 0 || tk > dtT) continue;
    const x = X(t0 + tk);
    c.strokeStyle = 'rgba(255,255,255,.06)'; c.lineWidth = 1; c.beginPath(); c.moveTo(x, T); c.lineTo(x, T + ph); c.stroke();
    c.fillStyle = '#6b7599'; c.textAlign = 'center'; c.fillText(fmtEng(t0 + tk, 's', 3), x, h - 5);
  }
  // traces
  c.save(); c.beginPath(); c.rect(L, T, pw, ph); c.clip();
  for (const ch of chs) {
    const Y = ch.axis === 'v' ? Yv : Yi; if (!Y) continue;
    c.strokeStyle = ch.col; c.lineWidth = 1.7; c.lineJoin = 'round'; c.setLineDash(ch.dash ? [5, 4] : []);
    c.shadowColor = ch.col; c.shadowBlur = 6;
    c.beginPath();
    for (let k = 0; k < n; k += stride) { const x = X(H_.t[idx(k)]), y = Y(ch.data[idx(k)]); k ? c.lineTo(x, y) : c.moveTo(x, y); }
    c.stroke();
  }
  c.restore();
}

/* =====================================================================
   Top bar
   ===================================================================== */
function setTimescale(ts) {
  timescale = ts;
  const s = (Math.log10(ts) + 6) / 7 * 1000;
  $('#speed').value = clamp(s, 0, 1000);
  $('#speedLbl').textContent = fmtEng(ts, 's') + ' / s';
}
function toggleRun() { running = !running; updateRunButton(); setStatus(); }
function updateRunButton() { $('#btnRun').innerHTML = icon(running ? 'pause' : 'play') + (running ? 'Pause' : 'Run'); }
function setStatus() {
  const s = $('#status');
  let cls = 'ok', txt = running ? 'Simulating' : 'Paused';
  if (sim) {
    if (sim.warn) { cls = 'bad'; txt = sim.warn; }
    else if (!circ.comps.length) { cls = ''; txt = 'Empty — drag a part onto the canvas'; }
    else if (sim.noGround) { cls = 'warn'; txt = 'No ground — add a GND symbol'; }
    else if (!running) cls = 'warn';
  }
  s.className = 'pill ' + cls; s.textContent = txt; s.title = txt;
}
function toast(msg, bad) {
  const t = el('div', 'toast' + (bad ? ' bad' : ''), msg); $('#toasts').appendChild(t);
  setTimeout(() => t.remove(), 2800);
}

function exportJSON() {
  const blob = new Blob([snapStr()], { type: 'application/json' });
  const a = document.createElement('a'); a.href = URL.createObjectURL(blob); a.download = 'circuit.json'; a.click(); URL.revokeObjectURL(a.href);
}
function exportCSV() {
  if (!sim || sim.hist.n < 2) return toast('Run the simulation first', true);
  const H = sim.hist, n = Math.min(H.n, H.cap), st = H.n - n, cols = [], names = [];
  for (const c of circ.comps) { const h = H.ch.get(c.id); if (!h) continue;
    const nm = (c.name || c.type).replace(/[^\w.-]/g, '_'); cols.push(h.v); names.push(nm + '_V');
    if (h.i) { cols.push(h.i); names.push(nm + '_A'); } }
  const rows = ['t_s,' + names.join(',')];
  for (let k = 0; k < n; k++) { const j = (st + k) % H.cap; rows.push(H.t[j].toPrecision(7) + ',' + cols.map(a => a[j].toPrecision(6)).join(',')); }
  const a = document.createElement('a'); a.href = URL.createObjectURL(new Blob([rows.join('\n')], { type: 'text/csv' }));
  a.download = 'voltaic-data.csv'; a.click(); URL.revokeObjectURL(a.href); toast('Exported ' + n + ' samples');
}
function importJSON(file) {
  const r = new FileReader();
  r.onload = () => {
    try {
      const o = JSON.parse(r.result);
      if (!Array.isArray(o.comps) || !Array.isArray(o.wires)) throw 0;
      for (const c of o.comps) if (!DEFS[c.type]) throw 0;
      circ = { nid: o.nid || 1000, comps: o.comps, wires: o.wires }; sel = null;
      rebuild(); fitView(); resetHistory(); renderInspector(); toast('Circuit loaded');
    } catch (e) { toast('Not a valid Voltaic circuit file', true); }
  };
  r.readAsText(file);
}
function exportPNG() {
  const o = document.createElement('canvas'); o.width = cv.width; o.height = cv.height;
  const x = o.getContext('2d'); x.fillStyle = '#080b17'; x.fillRect(0, 0, o.width, o.height); x.drawImage(cv, 0, 0);
  o.toBlob(b => { const a = document.createElement('a'); a.href = URL.createObjectURL(b); a.download = 'circuit.png'; a.click(); URL.revokeObjectURL(a.href); });
}

function wireTopbar() {
  for (const [id, ic] of [['btnStep', 'step'], ['btnReset', 'reset'], ['btnUndo', 'undo'], ['btnRedo', 'undo'], ['btnFit', 'fit'], ['btnNew', 'plus'], ['btnSave', 'download'], ['btnLoad', 'upload'], ['btnPng', 'image'], ['btnScope', 'chev']])
    $('#' + id).innerHTML = icon(ic);
  updateRunButton();
  $('#btnRun').onclick = toggleRun;
  $('#btnStep').onclick = () => { running = false; updateRunButton(); stepSim(SUBSTEPS); setStatus(); };
  $('#btnReset').onclick = () => { if (sim) { sim.reset(); } };
  $('#btnUndo').onclick = undo; $('#btnRedo').onclick = redo; $('#btnFit').onclick = fitView;
  $('#btnNew').onclick = () => { circ = { comps: [], wires: [], nid: 1 }; sel = null; rebuild(); resetHistory(); renderInspector(); };
  $('#btnSave').onclick = exportJSON; $('#btnCsv').onclick = exportCSV; $('#btnTheory').onclick = openTheory; $('#btnPng').onclick = exportPNG;
  $('#btnLoad').onclick = () => $('#file').click();
  $('#file').onchange = e => { if (e.target.files[0]) importJSON(e.target.files[0]); e.target.value = ''; };
  $('#speed').oninput = e => { timescale = Math.pow(10, -6 + 7 * e.target.value / 1000); timescale = Number(timescale.toPrecision(2)); $('#speedLbl').textContent = fmtEng(timescale, 's') + ' / s'; save(); };
  $('#btnScope').onclick = () => { $('#scope').classList.toggle('collapsed'); $('#btnScope').style.transform = $('#scope').classList.contains('collapsed') ? 'rotate(180deg)' : ''; resize(); };
  const ex = $('#examples'); ex.innerHTML = '<option value="">Examples…</option>';
  for (const k in PRESETS) { const o = el('option', null, PRESETS[k].name); o.value = k; ex.appendChild(o); }
  ex.onchange = () => { if (ex.value) loadPreset(ex.value); ex.value = ''; };
}

/* =====================================================================
   Main loop
   ===================================================================== */
function stepSim(steps) {
  if (!sim) return;
  const dt = timescale / (60 * SUBSTEPS);
  for (let k = 0; k < steps; k++) {
    if (!sim.step(dt)) { running = false; updateRunButton(); setStatus(); break; }
  }
  sim.updateFlows();
}

function resize() {
  const st = $('#stage').getBoundingClientRect();
  dpr = window.devicePixelRatio || 1; W = st.width; H = st.height;
  cv.width = Math.round(W * dpr); cv.height = Math.round(H * dpr);
  const r = sc.getBoundingClientRect(); scW = r.width; scH = r.height;
  sc.width = Math.round(scW * dpr); sc.height = Math.round(scH * dpr);
  $('#hint').style.bottom = $('#scope').classList.contains('collapsed') ? '60px' : '262px';
}

let liveTimer = 0;
function frame(ts) {
  const dtw = Math.min(0.05, (ts - lastTs) / 1000) || 0.016; lastTs = ts;
  if (running && sim && sim.N >= 0) stepSim(clamp(Math.round(SUBSTEPS * dtw * 60), 1, 80));
  render(dtw);
  drawScope();
  liveTimer += dtw;
  if (liveTimer > 0.12) {
    liveTimer = 0; updateLive(); if (edComp) edMsg();
    if (sim) { $('#timeLbl').textContent = 't = ' + fmtEng(sim.t, 's'); if (sim.warn || running) setStatus(); }
  }
  requestAnimationFrame(frame);
}

function init() {
  buildPalette(); wireTopbar(); wireEditor();
  new ResizeObserver(() => { resize(); }).observe($('#stage'));
  window.addEventListener('resize', resize);
  resize();
  const hp = new URLSearchParams(location.hash.slice(1)).get('preset');
  if (hp && PRESETS[hp]) { deepLinked = true; loadPreset(hp); }
  else if (loadSaved()) { rebuild(); fitView(); resetHistory(); } else loadPreset('rc');
  renderInspector(); setStatus();
  requestAnimationFrame(frame);
  window.__voltaic = { get circ() { return circ; }, get sim() { return sim; }, loadPreset, get cam() { return cam; } };
}
init();
