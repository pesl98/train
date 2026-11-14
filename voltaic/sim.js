'use strict';
/* =====================================================================
   Voltaic — circuit engine
   Modified nodal analysis, trapezoidal integration for C / L,
   Newton-Raphson for diodes, transistors and op-amps.
   No DOM access in this file.
   ===================================================================== */

const GRID = 20;            // px per grid unit
const VT = 0.025852;        // thermal voltage
const GMIN = 1e-11;

const LED_COLORS = {
  red:    { vf: 1.85, rgb: [255, 70, 70] },
  orange: { vf: 2.00, rgb: [255, 150, 40] },
  yellow: { vf: 2.10, rgb: [255, 225, 60] },
  green:  { vf: 2.20, rgb: [70, 255, 130] },
  blue:   { vf: 3.00, rgb: [80, 150, 255] },
  white:  { vf: 3.10, rgb: [255, 255, 255] },
};

function newM(n) { return { v: 0, i: 0, p: 0, ti: new Array(n).fill(0) }; }

function rotPt(x, y, r) {
  r &= 3;
  for (let k = 0; k < r; k++) { const t = x; x = -y; y = t; }
  return [x, y];
}


/* ---------------------------------------------------------------------
   Microcontroller: boards, sample sketches, Arduino-style runtime
   --------------------------------------------------------------------- */
const BOARDS = {
  esp32: { name: 'ESP32', vcc: 3.3, bits: 12, pin: 'GPIO' },
  uno:   { name: 'Arduino Uno', vcc: 5, bits: 10, pin: 'D' },
};
const CPP = (typeof translateCpp === 'function') ? { isCpp, translateCpp } : require('./cpp.js');   // cpp.js: Arduino C++ -> JavaScript
const SKETCHES = {
  blink: `// Blink an LED on pin 3
const int LED = 3;

void setup() {
  pinMode(LED, OUTPUT);
}

void loop() {
  digitalWrite(LED, HIGH);
  delay(500);
  digitalWrite(LED, LOW);
  delay(500);
}
`,
  button: `// Hold a button (pin 7, wired to GND) to light the LED (pin 3)
const int LED = 3, BTN = 7;
bool wasPressed = false;

void setup() {
  pinMode(LED, OUTPUT);
  pinMode(BTN, INPUT_PULLUP);   // pin reads HIGH until the button pulls it to GND
  Serial.begin(115200);
}

void loop() {
  bool pressed = digitalRead(BTN) == LOW;
  digitalWrite(LED, pressed ? HIGH : LOW);
  if (pressed != wasPressed) {
    Serial.println(pressed ? "button pressed" : "button released");
    wasPressed = pressed;
  }
  delay(10);
}
`,
  fade: `// Breathing LED using PWM (analogWrite takes 0-255)
const int LED = 3;
int level = 0, step = 5;

void setup() {
  pinMode(LED, OUTPUT);
}

void loop() {
  analogWrite(LED, level);
  level += step;
  if (level <= 0 || level >= 255) step = -step;
  delay(20);
}
`,
  adc: `// Read a voltage on pin 2 and show it on the serial monitor.
// The LED on pin 3 gets brighter as the input rises.
// ESP32: 12-bit ADC (0..4095), 3.3 V.   Arduino Uno: 10-bit (0..1023), 5 V - change the two numbers below.
const int ADC_MAX = 4095;
const float VREF = 3.3;

void setup() {
  pinMode(3, OUTPUT);
  Serial.begin(115200);
}

void loop() {
  int raw = analogRead(2);
  float volts = raw * VREF / ADC_MAX;
  Serial.print("ADC = ");
  Serial.print(raw);
  Serial.print("   ");
  Serial.print(volts, 2);
  Serial.println(" V");
  analogWrite(3, raw * 255 / ADC_MAX);
  delay(250);
}
`,
  helper: `// Your own functions can call delay() too.
const int LED = 3;

void blinkTimes(int n, int ms) {
  for (int i = 0; i < n; i++) {
    digitalWrite(LED, HIGH);
    delay(ms);
    digitalWrite(LED, LOW);
    delay(ms);
  }
}

void setup() {
  pinMode(LED, OUTPUT);
}

void loop() {
  blinkTimes(3, 100);   // three quick blinks ...
  delay(1000);          // ... then a pause
}
`,
};

class Mcu {
  constructor(sim, el) { this.sim = sim; this.el = el; this.c = el.c; this.serial = []; this.cur = ''; this.restart(); }
  get board() { return BOARDS[this.c.p.board] || BOARDS.esp32; }
  get vcc() { return this.board.vcc; }
  restart() {
    this.mode = new Array(8).fill(0);      // 0 input, 1 output, 2 input with pull-up
    this.out = new Array(8).fill(0);
    this.pwm = new Array(8).fill(-1);      // -1 = plain digital, otherwise duty 0..1
    this.err = null; this.wake = 0; this.phase = 'setup'; this.gen = null; this.fns = null;
    this.guard = 0; this.dirty = true; this.serial.length = 0; this.cur = '';
    this.compile();
  }
  pin(p) {
    p = Math.trunc(p);
    if (!(p >= 0 && p < 8)) throw new Error('Pin ' + p + ' does not exist on this board (use 0-7)');
    return p;
  }
  read(g) { const n = this.el.ix[g + 2]; return n >= 0 ? this.sim.x[n] : 0; }
  compile() {
    const self = this, B = this.board;
    const fmt = x => typeof x === 'boolean' ? (x ? '1' : '0') : (typeof x === 'number' && !Number.isInteger(x)) ? String(+x.toFixed(4)) : String(x);
    const fmtD = (x, d) => {          // Serial.print(x, d): d = digits for decimals, or HEX / BIN / OCT / DEC for integers
      if (d && d.base) return Math.trunc(+x).toString(d.base).toUpperCase();
      if (typeof d === 'number' && isFinite(+x)) return (+x).toFixed(Math.max(0, Math.min(10, d)));
      return fmt(x);
    };
    const pwmBits = {};
    const api = {
      INPUT: 0, OUTPUT: 1, INPUT_PULLUP: 2, HIGH: 1, LOW: 0, PI: Math.PI, TWO_PI: 2 * Math.PI, HALF_PI: Math.PI / 2, LED_BUILTIN: 2,
      VCC: B.vcc, BOARD_ADC_MAX: (1 << B.bits) - 1, HEX: { base: 16 }, BIN: { base: 2 }, OCT: { base: 8 }, DEC: { base: 10 }, F: s => s,
      pinMode(p, m) { p = self.pin(p); self.mode[p] = m; if (m !== 1) self.pwm[p] = -1; self.dirty = true; },
      digitalWrite(p, v) { p = self.pin(p); self.out[p] = v ? 1 : 0; self.pwm[p] = -1; self.dirty = true; },
      digitalRead(p) { p = self.pin(p); return self.read(p) > self.vcc * 0.5 ? 1 : 0; },
      analogRead(p) { p = self.pin(p); const m = (1 << self.board.bits) - 1; return Math.max(0, Math.min(m, Math.round(self.read(p) / self.vcc * m))); },
      analogWrite(p, v) { p = self.pin(p); self.mode[p] = 1; self.pwm[p] = Math.max(0, Math.min(1, v / 255)); self.dirty = true; },
      millis() { return Math.floor(self.sim.t * 1000); },
      micros() { return Math.floor(self.sim.t * 1e6); },
      ledcAttach(p, f, bits) { p = self.pin(p); pwmBits[p] = bits || 8; self.mode[p] = 1; self.dirty = true; return 1; },
      ledcWrite(p, v) { p = self.pin(p); const m = (1 << (pwmBits[p] || 8)) - 1; self.mode[p] = 1; self.pwm[p] = Math.max(0, Math.min(1, v / m)); self.dirty = true; },
      map: (x, a, b, c, d) => (x - a) * (d - c) / (b - a) + c,
      constrain: (x, a, b) => Math.max(a, Math.min(b, x)),
      random: (a, b) => b === undefined ? Math.floor(Math.random() * a) : a + Math.floor(Math.random() * (b - a)),
      abs: Math.abs, min: Math.min, max: Math.max, sqrt: Math.sqrt, sin: Math.sin, cos: Math.cos, tan: Math.tan, atan2: Math.atan2, log: Math.log, exp: Math.exp,
      pow: Math.pow, floor: Math.floor, ceil: Math.ceil, round: Math.round, fabs: Math.abs, sq: x => x * x, radians: x => x * Math.PI / 180, degrees: x => x * 180 / Math.PI,
      Serial: {
        begin() { },
        print(x, d) { self.cur += d === undefined ? fmt(x) : fmtD(x, d); },
        println(x = '', d) { self.cur += d === undefined ? fmt(x) : fmtD(x, d); self.serial.push(self.cur); self.cur = ''; if (self.serial.length > 200) self.serial.shift(); },
      },
    };
    const names = Object.keys(api);
    let src = String(this.c.p.code || '');
    if (CPP.isCpp(src)) {            // Arduino C++ (a teaching subset): translate to JavaScript first
      try { src = CPP.translateCpp(src); } catch (e) { this.fail(e); return; }
    } else {                         // JavaScript sketch (older circuits)
      src = src.replace(/function\s+(setup|loop)\s*\(/g, 'function* $1(')
        .replace(/\bdelayMicroseconds\s*\(/g, 'yield 0.001*(')
        .replace(/\bdelay\s*\(/g, 'yield (')
        .replace(/\bwhile\s*\(/g, 'while(__g(),');
    }
    try {
      // the sketch lives in its own function scope, so it may declare names that the runtime also provides (PI, map, ...)
      const f = new Function(...names, '__g', 'return (function(){' + src + '\n;return {setup: typeof setup==="function"?setup:null, loop: typeof loop==="function"?loop:null};})();');
      this.fns = f(...names.map(n => api[n]), () => { if (++self.guard > 300000) throw new Error('Loop ran too long without delay()'); });
      this.gen = this.fns.setup ? this.fns.setup() : null;
      if (!this.gen) { this.phase = 'loop'; this.gen = this.fns.loop ? this.fns.loop() : null; }
    } catch (e) { this.fail(e); }
  }
  fail(e) {
    let m = e && e.message ? e.message : String(e);
    let r;
    if (/yield/.test(m)) m = 'delay() can only be used directly inside setup() or loop()';
    else if ((r = /^(\w+) is not defined$/.exec(m))) m = "'" + r[1] + "' is not declared: check the spelling. Libraries and functions outside the simulator's Arduino subset are not available";
    else if (e instanceof SyntaxError) m = 'syntax error: ' + m;
    this.err = m; this.gen = null;
    this.sim.warn = this.c.name + ': ' + m;
  }
  drive(g, t, dt) {
    if (this.mode[g] !== 1) return null;
    const d = this.pwm[g];
    if (d >= 0) return dt * 8 > 1e-3 ? d * this.vcc : (((t * 1000) % 1) < d ? this.vcc : 0);
    return this.out[g] ? this.vcc : 0;
  }
  tick(t) {
    if (!this.gen) return;
    let n = 0;
    while (this.wake <= t && this.gen && n++ < 400) {
      this.guard = 0;
      let r;
      try { r = this.gen.next(); } catch (e) { this.fail(e); return; }
      if (r.done) {
        if (this.phase === 'setup') this.phase = 'loop';
        this.gen = this.fns.loop ? this.fns.loop() : null;
        this.wake += 20e-6;                 // nominal cost of one loop() pass
      } else {
        const ms = +r.value; this.wake += (isFinite(ms) && ms > 0 ? ms : 0) / 1000;
      }
    }
    if (n >= 400) this.wake = t;
  }
}

/* Terminal layout (grid units, before rotation) and default parameters */
const DEFS = {
  R:     { name: 'Resistor',        pre: 'R', vert: false, t: [[-2, 0], [2, 0]],            p: { r: 1000 } },
  POT:   { name: 'Potentiometer',   pre: 'RV', vert: false, t: [[-2, 0], [2, 0], [0, -2]], p: { r: 10000, w: 0.5 } },
  C:     { name: 'Capacitor',       pre: 'C', vert: false, t: [[-2, 0], [2, 0]],            p: { c: 1e-6 } },
  L:     { name: 'Inductor',        pre: 'L', vert: false, t: [[-2, 0], [2, 0]],            p: { l: 1e-3 } },
  SW:    { name: 'Switch',          pre: 'S', vert: false, t: [[-2, 0], [2, 0]],            p: { closed: true } },
  LAMP:  { name: 'Lamp',            pre: 'LA', vert: false, t: [[-2, 0], [2, 0]],           p: { r: 100, rated: 0.25 } },
  V:     { name: 'DC Source',       pre: 'V', vert: true,  t: [[0, -2], [0, 2]],            p: { v: 5 } },
  AC:    { name: 'Signal Source',   pre: 'G', vert: true,  t: [[0, -2], [0, 2]],            p: { wave: 'sine', amp: 5, freq: 50, off: 0 } },
  I:     { name: 'Current Source',  pre: 'I', vert: true,  t: [[0, -2], [0, 2]],            p: { i: 0.01 } },
  GND:   { name: 'Ground',          pre: 'GND', vert: true, t: [[0, 0]],                    p: {} },
  D:     { name: 'Diode',           pre: 'D', vert: false, t: [[-2, 0], [2, 0]],            p: {} },
  LED:   { name: 'LED',             pre: 'LED', vert: false, t: [[-2, 0], [2, 0]],          p: { color: 'red' } },
  ZD:    { name: 'Zener Diode',     pre: 'ZD', vert: false, t: [[-2, 0], [2, 0]],           p: { vz: 5.1 } },
  NPN:   { name: 'NPN Transistor',  pre: 'Q', vert: false, t: [[-2, 0], [1, -2], [1, 2]],  p: { beta: 100 } },
  PNP:   { name: 'PNP Transistor',  pre: 'Q', vert: false, t: [[-2, 0], [1, -2], [1, 2]],  p: { beta: 100 } },
  OP:    { name: 'Op-Amp',          pre: 'U', vert: false, t: [[-3, -1], [-3, 1], [3, 0]], p: { rail: 12 } },
  MCU:   { name: 'Microcontroller', pre: 'MCU', vert: false, t: [[-4, -4], [-4, -2], [-4, 0], [-4, 2], [-4, 4], [4, -4], [4, -2], [4, 0], [4, 2], [4, 4]], p: { board: 'esp32', code: SKETCHES.blink } },
  PROBE: { name: 'Scope Probe',     pre: 'P', vert: false, t: [[0, 0]],                    p: {} },
};

function termPos(c, k) {
  const t = DEFS[c.type].t[k];
  const [x, y] = rotPt(t[0], t[1], c.rot);
  return [c.x + x, c.y + y];
}

/* ---------------------------------------------------------------------
   Formatting / parsing helpers
   --------------------------------------------------------------------- */
function fmtEng(v, unit = '', digits = 3) {
  if (!isFinite(v)) return '—';
  if (v === 0) return '0 ' + unit;
  const a = Math.abs(v);
  const pre = ['f', 'p', 'n', 'µ', 'm', '', 'k', 'M', 'G', 'T'];
  let e = Math.floor(Math.log10(a) / 3);
  e = Math.max(-5, Math.min(4, e));
  let s = Number((v / Math.pow(10, e * 3)).toPrecision(digits));
  if (Math.abs(s) >= 1000 && e < 4) { e++; s = Number((v / Math.pow(10, e * 3)).toPrecision(digits)); }
  return s + ' ' + pre[e + 5] + unit;
}

function parseVal(str) {
  const m = String(str).trim().match(/^([+-]?(?:\d+\.?\d*|\.\d+)(?:e[+-]?\d+)?)\s*(meg|[pnuµmkKMGT])?/i);
  if (!m) return NaN;
  let v = parseFloat(m[1]);
  const s = m[2];
  if (s) {
    const mult = { p: 1e-12, n: 1e-9, u: 1e-6, 'µ': 1e-6, m: 1e-3, k: 1e3, K: 1e3, M: 1e6, G: 1e9, T: 1e12 };
    if (s.toLowerCase() === 'meg') v *= 1e6; else v *= mult[s];
  }
  return v;
}

/* ---------------------------------------------------------------------
   Netlist extraction: geometry -> connectivity
   --------------------------------------------------------------------- */
function buildNet(circ) {
  const map = new Map(); const px = [], py = [];
  const pid = (x, y) => {
    const k = x + ',' + y; let i = map.get(k);
    if (i === undefined) { i = px.length; map.set(k, i); px.push(x); py.push(y); }
    return i;
  };
  const cp = circ.comps.map(c => DEFS[c.type].t.map((_, k) => { const [x, y] = termPos(c, k); return pid(x, y); }));
  const wp = circ.wires.map(w => [pid(w.x1, w.y1), pid(w.x2, w.y2)]);
  const n = px.length;
  const par = Array.from({ length: n }, (_, i) => i);
  const find = a => { while (par[a] !== a) { par[a] = par[par[a]]; a = par[a]; } return a; };
  const uni = (a, b) => { a = find(a); b = find(b); if (a !== b) par[a] = b; };

  const segs = [];
  circ.wires.forEach((w, wi) => {
    const [a, b] = wp[wi];
    const dx = w.x2 - w.x1, dy = w.y2 - w.y1, l2 = dx * dx + dy * dy;
    if (l2 === 0) return;
    const mids = [];
    for (let p = 0; p < n; p++) {
      if (p === a || p === b) continue;
      const cx = px[p] - w.x1, cy = py[p] - w.y1;
      if (cx * dy - cy * dx !== 0) continue;
      const d = cx * dx + cy * dy;
      if (d > 0 && d < l2) mids.push([d, p]);
    }
    mids.sort((u, v) => u[0] - v[0]);
    const chain = [a, ...mids.map(m => m[1]), b];
    for (let k = 0; k < chain.length - 1; k++) {
      segs.push({ a: chain[k], b: chain[k + 1], w: wi });
      uni(chain[k], chain[k + 1]);
    }
  });

  let gRoot = -1;
  circ.comps.forEach((c, i) => {
    const r = c.type === 'GND' ? cp[i][0] : c.type === 'MCU' ? cp[i][1] : -1;
    if (r < 0) return;
    if (gRoot < 0) gRoot = r; else uni(r, gRoot);
  });
  const nodeOf = new Map(); let nc = 0;
  if (gRoot >= 0) { nodeOf.set(find(gRoot), 0); nc = 1; }
  const ptNode = px.map((_, p) => {
    const r = find(p); let v = nodeOf.get(r);
    if (v === undefined) { v = nc++; nodeOf.set(r, v); }
    return v;
  });
  return { px, py, cp, wp, segs, ptNode, nodeCount: nc, noGround: gRoot < 0 };
}

/* ---------------------------------------------------------------------
   Dense Gaussian elimination with partial pivoting (destroys A, b)
   --------------------------------------------------------------------- */
function solveLinear(A, b, N, x) {
  for (let c = 0; c < N; c++) {
    let p = c, mx = Math.abs(A[c * N + c]);
    for (let r = c + 1; r < N; r++) { const v = Math.abs(A[r * N + c]); if (v > mx) { mx = v; p = r; } }
    if (mx < 1e-18) return false;
    if (p !== c) {
      for (let k = c; k < N; k++) { const t = A[c * N + k]; A[c * N + k] = A[p * N + k]; A[p * N + k] = t; }
      const t = b[c]; b[c] = b[p]; b[p] = t;
    }
    const piv = A[c * N + c];
    for (let r = c + 1; r < N; r++) {
      const f = A[r * N + c] / piv;
      if (f === 0) continue;
      for (let k = c; k < N; k++) A[r * N + k] -= f * A[c * N + k];
      b[r] -= f * b[c];
    }
  }
  for (let r = N - 1; r >= 0; r--) {
    let s = b[r];
    for (let k = r + 1; k < N; k++) s -= A[r * N + k] * x[k];
    x[r] = s / A[r * N + r];
  }
  return true;
}

/* ---------------------------------------------------------------------
   Device models
   --------------------------------------------------------------------- */
function pnjlim(vnew, vold, vt, vcrit) {
  if (vnew > vcrit && Math.abs(vnew - vold) > 2 * vt) {
    if (vold > 0) {
      const arg = 1 + (vnew - vold) / vt;
      vnew = arg > 0 ? vold + vt * Math.log(arg) : vcrit;
    } else {
      vnew = vt * Math.log(vnew / vt);
    }
  }
  return vnew;
}

function diodeModel(c) {
  let m;
  if (c.type === 'LED') {
    const vf = (LED_COLORS[c.p.color] || LED_COLORS.red).vf;
    m = { key: 'L' + c.p.color, is: 0.02 / Math.exp(vf / (2 * VT)), nvt: 2 * VT, vz: 0 };
  } else if (c.type === 'ZD') {
    m = { key: 'Z' + c.p.vz, is: 2.5e-9, nvt: 1.75 * VT, vz: Math.max(0.5, c.p.vz - 0.25), iz: 1e-6, nvz: 2 * VT };
    m.vcz = m.nvz * Math.log(m.nvz / (Math.SQRT2 * m.iz));
  } else {
    m = { key: 'D', is: 2.5e-9, nvt: 1.75 * VT, vz: 0 };
  }
  m.vc = m.nvt * Math.log(m.nvt / (Math.SQRT2 * m.is));
  return m;
}

function limitD(vraw, vold, m) {
  if (m.vz > 0 && vraw < -m.vz * 0.5) {
    const w = -vraw - m.vz, wo = -vold - m.vz;
    return -pnjlim(w, wo, m.nvz, m.vcz) - m.vz;
  }
  return pnjlim(vraw, vold, m.nvt, m.vc);
}

function srcValue(c, t) {
  const { wave, amp, freq, off } = c.p;
  const ph = ((t * freq) % 1 + 1) % 1;
  switch (wave) {
    case 'square':   return off + amp * (ph < 0.5 ? 1 : -1);
    case 'triangle': return off + amp * (ph < 0.5 ? 4 * ph - 1 : 3 - 4 * ph);
    case 'saw':      return off + amp * (2 * ph - 1);
    default:         return off + amp * Math.sin(2 * Math.PI * freq * t);
  }
}

const HIST_CAP = 6000;

/* =====================================================================
   Sim
   ===================================================================== */
class Sim {
  constructor(circ) {
    this.circ = circ;
    const net = this.net = buildNet(circ);
    this.noGround = net.noGround;
    this.warn = null;
    this.t = 0;
    this.be = 2;                      // backward-Euler steps pending (after discontinuities)

    const nv = this.nv = Math.max(0, net.nodeCount - 1);
    this.nodeV = new Float64Array(Math.max(1, net.nodeCount));

    this.segs = net.segs.map(s => {
      const x1 = net.px[s.a] * GRID, y1 = net.py[s.a] * GRID, x2 = net.px[s.b] * GRID, y2 = net.py[s.b] * GRID;
      return { a: s.a, b: s.b, w: s.w, node: net.ptNode[s.a], i: 0, ph: Math.random() * 16,
               x1, y1, x2, y2, len: Math.hypot(x2 - x1, y2 - y1) };
    });

    this.els = []; this.probes = []; this.mcus = new Map();
    let nbr = 0;
    const hist = this.hist = { cap: HIST_CAP, n: 0, t: new Float64Array(HIST_CAP), ch: new Map() };
    circ.comps.forEach((c, ci) => {
      const pins = net.cp[ci];
      const nodes = pins.map(p => net.ptNode[p]);
      if (!c.s) c.s = { v: 0, i: 0 };
      c.m = newM(DEFS[c.type].t.length);
      if (c.type === 'GND') return;
      if (c.type === 'PROBE') {
        this.probes.push({ c, node: nodes[0] });
        hist.ch.set(c.id, { v: new Float32Array(HIST_CAP), i: null });
        return;
      }
      const el = { c, type: c.type, pins, ix: nodes.map(v => v - 1), br: -1, s: c.s,
                   vdl: 0, vbe: 0, vbc: 0, g: 0, geq: 0, id: 0, mk: null, model: null, out: [0, 0, 0] };
      if (c.type === 'V' || c.type === 'AC' || c.type === 'L' || c.type === 'OP' || c.type === 'MCU') el.br = nbr++;
      if (c.type === 'MCU') { el.mcu = new Mcu(this, el); el.pg = new Float64Array(8); el.pv = new Float64Array(8); this.mcus.set(c.id, el.mcu); }
      this.els.push(el);
      hist.ch.set(c.id, { v: new Float32Array(HIST_CAP), i: new Float32Array(HIST_CAP) });
    });
    for (const el of this.els) if (el.br >= 0) el.br += nv;
    this.N = nv + nbr;
    this.A = new Float64Array(this.N * this.N);
    this.b = new Float64Array(this.N);
    this.x = new Float64Array(this.N);
    this.xn = new Float64Array(this.N);
    this.nl = this.els.some(e => ['D', 'LED', 'ZD', 'NPN', 'PNP', 'OP'].includes(e.type));
    this.limited = false;
    this._buildFlow();
    this._buildJunctions();
  }

  reset() {
    this.t = 0; this.be = 2; this.warn = null;
    this.x.fill(0); this.nodeV.fill(0);
    this.hist.n = 0;
    for (const el of this.els) { el.s.v = 0; el.s.i = 0; el.vdl = 0; el.vbe = 0; el.vbc = 0; }
    for (const c of this.circ.comps) { c.s.v = 0; c.s.i = 0; c.m = newM(DEFS[c.type].t.length); }
    for (const el of this.els) if (el.mcu) el.mcu.restart();
    for (const s of this.segs) s.i = 0;
  }

  /* --- wire-current solving (spanning forest over wire segments) --- */
  _buildFlow() {
    const n = this.net.px.length;
    const adj = Array.from({ length: n }, () => []);
    this.segs.forEach((s, k) => { adj[s.a].push([s.b, k]); adj[s.b].push([s.a, k]); });
    const seen = new Uint8Array(n);
    this.order = []; this.parSeg = new Int32Array(n).fill(-1); this.parPt = new Int32Array(n).fill(-1);
    for (let r = 0; r < n; r++) {
      if (seen[r] || adj[r].length === 0) continue;
      seen[r] = 1;
      const q = [r];
      for (let h = 0; h < q.length; h++) {
        const v = q[h]; this.order.push(v);
        for (const [u, k] of adj[v]) if (!seen[u]) { seen[u] = 1; this.parSeg[u] = k; this.parPt[u] = v; q.push(u); }
      }
    }
    this.inj = new Float64Array(n);
  }

  updateFlows() {
    const inj = this.inj; inj.fill(0);
    for (const el of this.els) {
      const ti = el.c.m.ti;
      for (let k = 0; k < el.pins.length; k++) inj[el.pins[k]] -= ti[k];
    }
    for (const s of this.segs) s.i = 0;
    for (let k = this.order.length - 1; k >= 0; k--) {
      const v = this.order[k], ps = this.parSeg[v];
      if (ps < 0) continue;
      const S = inj[v];
      const seg = this.segs[ps];
      seg.i = (seg.a === v) ? S : -S;
      inj[this.parPt[v]] += S;
    }
  }

  _buildJunctions() {
    const cnt = new Map();
    const net = this.net;
    const bump = p => cnt.set(p, (cnt.get(p) || 0) + 1);
    for (const s of this.segs) { bump(s.a); bump(s.b); }
    for (const pins of net.cp) for (const p of pins) bump(p);
    this.junctions = [];
    for (const [p, c] of cnt) if (c >= 3) this.junctions.push({ x: net.px[p] * GRID, y: net.py[p] * GRID, node: net.ptNode[p] });
  }

  /* --- MNA stamping --- */
  _stamp(dt, be, t, x) {
    const A = this.A, b = this.b, N = this.N, nv = this.nv;
    A.fill(0); b.fill(0);
    const a = (r, c, v) => { if (r >= 0 && c >= 0) A[r * N + c] += v; };
    const rs = (r, v) => { if (r >= 0) b[r] += v; };
    const gs = (p, q, g) => { a(p, p, g); a(q, q, g); a(p, q, -g); a(q, p, -g); };
    const cs = (p, q, i) => { rs(p, -i); rs(q, i); };      // constant current p -> q through element
    const V = i => (i >= 0 ? x[i] : 0);
    this.limited = false;
    for (let k = 0; k < nv; k++) A[k * N + k] += GMIN;

    for (const el of this.els) {
      const c = el.c, ix = el.ix, p = ix[0], q = ix[1];
      switch (el.type) {
        case 'R': el.g = 1 / Math.max(c.p.r, 1e-3); gs(p, q, el.g); break;
        case 'LAMP': el.g = 1 / Math.max(c.p.r, 1e-3); gs(p, q, el.g); break;
        case 'SW': el.g = c.p.closed ? 1e3 : 1e-12; gs(p, q, el.g); break;
        case 'POT': {
          const w = Math.min(1, Math.max(0, c.p.w)), r = c.p.r, wi = ix[2];
          el.r1 = Math.max(r * w, 0.01); el.r2 = Math.max(r * (1 - w), 0.01);
          gs(p, wi, 1 / el.r1); gs(q, wi, 1 / el.r2);
          break;
        }
        case 'C': {
          el.geq = (be ? 1 : 2) * Math.max(c.p.c, 1e-15) / dt;
          gs(p, q, el.geq);
          cs(p, q, -(el.geq * el.s.v + (be ? 0 : el.s.i)));
          break;
        }
        case 'L': {
          const req = (be ? 1 : 2) * Math.max(c.p.l, 1e-12) / dt, br = el.br;
          el.req = req;
          a(p, br, 1); a(q, br, -1); a(br, p, 1); a(br, q, -1); a(br, br, -req);
          rs(br, -(req * el.s.i + (be ? 0 : el.s.v)));
          break;
        }
        case 'V': case 'AC': {
          const br = el.br, E = el.type === 'V' ? c.p.v : srcValue(c, t);
          el.E = E;
          a(p, br, 1); a(q, br, -1); a(br, p, 1); a(br, q, -1); rs(br, E);
          break;
        }
        case 'I': cs(p, q, c.p.i); break;
        case 'D': case 'LED': case 'ZD': {
          const key = el.type === 'LED' ? 'L' + c.p.color : el.type === 'ZD' ? 'Z' + c.p.vz : 'D';
          if (el.mk !== key) { el.mk = key; el.model = diodeModel(c); }
          const m = el.model;
          const vraw = V(p) - V(q);
          const vd = limitD(vraw, el.vdl, m);
          if (Math.abs(vd - vraw) > 1e-9) this.limited = true;
          el.vdl = vd;
          const e = Math.exp(Math.min(vd / m.nvt, 60));
          let i = m.is * (e - 1), g = m.is * e / m.nvt;
          if (m.vz > 0) {
            const ez = Math.exp(Math.min((-vd - m.vz) / m.nvz, 60));
            i -= m.iz * (ez - 1); g += m.iz * ez / m.nvz;
          }
          g += GMIN;
          el.id = i;
          gs(p, q, g); cs(p, q, i - g * vd);
          break;
        }
        case 'NPN': case 'PNP': {
          const pol = el.type === 'NPN' ? 1 : -1;
          const B = ix[0], C = ix[1], E = ix[2];
          const bf = Math.max(c.p.beta, 1), br = 2, is = 1e-14;
          const vcrit = VT * Math.log(VT / (Math.SQRT2 * is));
          const vbe = pol * (V(B) - V(E)), vbc = pol * (V(B) - V(C));
          const vbeL = pnjlim(vbe, el.vbe, VT, vcrit), vbcL = pnjlim(vbc, el.vbc, VT, vcrit);
          if (Math.abs(vbeL - vbe) > 1e-9 || Math.abs(vbcL - vbc) > 1e-9) this.limited = true;
          el.vbe = vbeL; el.vbc = vbcL;
          const ee = Math.exp(Math.min(vbeL / VT, 60)), ec = Math.exp(Math.min(vbcL / VT, 60));
          const Icc = is * (ee - 1), Iec = is * (ec - 1);
          const gbe = is * ee / VT, gbc = is * ec / VT;
          const IB = Icc / bf + Iec / br, IC = Icc - Iec - Iec / br, IE = -(IB + IC);
          const dBe = gbe / bf, dBc = gbc / br;
          const dCe = gbe, dCc = -gbc * (1 + 1 / br);
          const dEe = -(dBe + dCe), dEc = -(dBc + dCc);
          const T = (row, I, fbe, fbc) => {
            a(row, B, fbe + fbc); a(row, E, -fbe); a(row, C, -fbc);
            rs(row, -pol * (I - fbe * vbeL - fbc * vbcL));
          };
          T(B, IB, dBe, dBc); T(C, IC, dCe, dCc); T(E, IE, dEe, dEc);
          gs(B, E, GMIN); gs(B, C, GMIN);
          el.out[0] = pol * IB; el.out[1] = pol * IC; el.out[2] = pol * IE;
          break;
        }
        case 'MCU': {
          const mcu = el.mcu, vcc = mcu.vcc, br = el.br;
          a(p, br, 1); a(br, p, 1); rs(br, vcc);
          for (let g = 0; g < 8; g++) {
            const n = ix[g + 2], tv = mcu.drive(g, t, dt);
            if (tv !== null) { a(n, n, 1 / 25); rs(n, tv / 25); el.pg[g] = 1 / 25; el.pv[g] = tv; }
            else if (mcu.mode[g] === 2) { a(n, n, 1 / 45000); rs(n, vcc / 45000); el.pg[g] = 1 / 45000; el.pv[g] = vcc; }
            else el.pg[g] = 0;
          }
          break;
        }
        case 'OP': {
          const R = c.p.rail, A0 = 1e5, br = el.br;
          const inn = ix[0], inp = ix[1], out = ix[2];
          const S = 10 * R / A0;
          const vd = V(inp) - V(inn);
          const vl = Math.max(-S, Math.min(S, vd));
          const th = Math.tanh(A0 * vl / R);
          const f = R * th, fp = A0 * (1 - th * th);
          a(out, br, 1);
          a(br, out, 1); a(br, inp, -fp); a(br, inn, fp);
          rs(br, f - fp * vl);
          break;
        }
      }
    }
  }

  step(dt) {
    const N = this.N;
    for (const el of this.els) if (el.mcu) { el.mcu.tick(this.t); if (el.mcu.dirty) { this.be = Math.max(this.be, 1); el.mcu.dirty = false; } }
    const be = this.be > 0; if (be) this.be--;
    const t1 = this.t + dt;
    const x = this.x, xn = this.xn;
    const maxIt = this.nl ? 100 : 1;
    let conv = !this.nl;
    for (let it = 0; it < maxIt; it++) {
      this._stamp(dt, be, t1, x);
      if (!solveLinear(this.A, this.b, N, xn)) {
        this.warn = 'Singular circuit — look for loops of voltage sources, shorted sources or inductor/source loops.';
        return false;
      }
      let ok = !this.limited;
      if (this.nl) {
        for (let i = 0; i < N; i++) {
          if (Math.abs(xn[i] - x[i]) > 1e-7 + 1e-5 * Math.abs(xn[i])) { ok = false; break; }
        }
      }
      if (it > 40) { for (let i = 0; i < N; i++) x[i] = 0.5 * (x[i] + xn[i]); }
      else x.set(xn);
      if (!this.nl || ok) { conv = true; break; }
    }
    if (!conv) this.warn = 'Solver is struggling to converge — try lowering the speed.';
    else if (this.warn && this.warn.startsWith('Solver')) this.warn = null;
    if (!isFinite(x[0] || 0)) { this.warn = 'Numerical blow-up — circuit reset.'; this.reset(); return false; }

    this.t = t1;
    this._outputs(dt, be);
    this._record();
    return true;
  }

  _outputs(dt, be) {
    const x = this.x, nv = this.nv;
    const V = i => (i >= 0 ? x[i] : 0);
    for (let k = 0; k < nv; k++) this.nodeV[k + 1] = x[k];
    for (const el of this.els) {
      const m = el.c.m, ix = el.ix, ti = m.ti;
      const vp = V(ix[0]), vq = V(ix[1]);
      let v = vp - vq, i = 0, pw = 0;
      switch (el.type) {
        case 'R': case 'LAMP': case 'SW':
          i = v * el.g; ti[0] = i; ti[1] = -i; pw = v * i; break;
        case 'POT': {
          const vw = V(ix[2]);
          const i0 = (vp - vw) / el.r1, i1 = (vq - vw) / el.r2;
          ti[0] = i0; ti[1] = i1; ti[2] = -i0 - i1; i = i0; pw = i0 * (vp - vw) + i1 * (vq - vw);
          break;
        }
        case 'C':
          i = el.geq * (v - el.s.v) - (be ? 0 : el.s.i);
          el.s.v = v; el.s.i = i; ti[0] = i; ti[1] = -i; pw = v * i; break;
        case 'L':
          i = x[el.br]; el.s.i = i; el.s.v = v; ti[0] = i; ti[1] = -i; pw = v * i; break;
        case 'V': case 'AC': {
          const j = x[el.br];
          ti[0] = j; ti[1] = -j; i = -j; pw = v * i; break;
        }
        case 'I':
          i = el.c.p.i; ti[0] = i; ti[1] = -i; pw = -v * i; break;
        case 'D': case 'LED': case 'ZD':
          i = el.id; ti[0] = i; ti[1] = -i; pw = v * i; break;
        case 'NPN': case 'PNP': {
          ti[0] = el.out[0]; ti[1] = el.out[1]; ti[2] = el.out[2];
          const vb = V(ix[0]), vc = V(ix[1]), ve = V(ix[2]);
          v = vc - ve; i = ti[1]; pw = vb * ti[0] + vc * ti[1] + ve * ti[2];
          break;
        }
        case 'MCU': {
          const j = x[el.br]; let sum = j; ti[0] = j;
          for (let g = 0; g < 8; g++) { const cur = el.pg[g] * (V(ix[g + 2]) - el.pv[g]); ti[g + 2] = cur; sum += cur; }
          ti[1] = -sum; v = V(ix[0]); i = -j; pw = v * i;
          break;
        }
        case 'OP': {
          const j = x[el.br];
          ti[0] = 0; ti[1] = 0; ti[2] = j; v = V(ix[2]); i = -j; pw = 0;
          break;
        }
      }
      m.v = v; m.i = i; m.p = pw;
    }
    for (const pr of this.probes) pr.c.m.v = this.nodeV[pr.node];
  }

  _record() {
    const h = this.hist, k = h.n % h.cap;
    h.t[k] = this.t;
    for (const el of this.els) { const ch = h.ch.get(el.c.id); ch.v[k] = el.c.m.v; ch.i[k] = el.c.m.i; }
    for (const pr of this.probes) h.ch.get(pr.c.id).v[k] = pr.c.m.v;
    h.n++;
  }
}

if (typeof module !== 'undefined') module.exports = { Sim, Mcu, SKETCHES, BOARDS, DEFS, GRID, fmtEng, parseVal, termPos, buildNet };
