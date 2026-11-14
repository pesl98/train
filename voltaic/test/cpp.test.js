/* Tests for the Arduino C++ translator and the microcontroller runtime.   run:  node voltaic/test/cpp.test.js */
const assert = require('assert');
const { translateCpp, isCpp } = require('../cpp.js');
const { Mcu, SKETCHES } = require('../sim.js');

let passed = 0, failed = 0;
function test(name, fn) { try { fn(); passed++; console.log('PASS', name); } catch (e) { failed++; console.log('FAIL', name, '\n     ', e.message.split('\n')[0]); } }

/* run a sketch for `seconds` of simulated time, return the microcontroller and a log of {t, pin, level} changes */
function run(code, { seconds = 3, dt = 0.001, inputs = {} } = {}) {
  const sim = { t: 0, x: [0, 0, 0, 0, 0, 0, 0, 0], warn: null };
  const el = { c: { name: 'MCU1', p: { board: 'esp32', code } }, ix: new Array(10).fill(-1) };
  for (const [pin, node] of Object.entries(inputs.nodes || {})) el.ix[+pin + 2] = node;
  Object.assign(sim.x, inputs.volts || {});
  const mcu = new Mcu(sim, el), log = []; let last = new Array(8).fill(null);
  for (let t = 0; t <= seconds; t += dt) {
    sim.t = t; mcu.tick(t);
    for (let p = 0; p < 8; p++) { const v = mcu.drive(p, t, dt); if (v !== last[p]) { log.push({ t, pin: p, v }); last[p] = v; } }
  }
  return { mcu, log, sim };
}
const toggles = (log, pin) => log.filter(e => e.pin === pin && e.v !== null).slice(1);   // drop the initial 'pin is an output at 0 V' entry
const serialOf = m => m.serial.concat(m.cur ? [m.cur] : []);

test('isCpp detects C++ and leaves JavaScript alone', () => {
  assert(isCpp('void setup() {}\nvoid loop() {}'));
  assert(!isCpp('function setup() {}\nfunction loop() {}'));
});

test('blink sketch (C++): LED toggles every 500 ms', () => {
  const { mcu, log } = run(SKETCHES.blink, { seconds: 2.2 });
  assert.strictEqual(mcu.err, null);
  const t = toggles(log, 3);
  assert(t.length >= 4, 'expected >= 4 changes, got ' + t.length);
  assert.deepStrictEqual(t.slice(0, 4).map(e => e.v), [3.3, 0, 3.3, 0]);
  assert(Math.abs(t[1].t - t[0].t - 0.5) < 0.01 && Math.abs(t[2].t - t[0].t - 1.0) < 0.01, JSON.stringify(t.slice(0, 3)));
});

test('fade sketch (C++): PWM duty rises', () => {
  const { mcu } = run(SKETCHES.fade, { seconds: 0.5 });
  assert.strictEqual(mcu.err, null);
  assert(mcu.pwm[3] > 0.2 && mcu.pwm[3] < 0.8, 'duty ' + mcu.pwm[3]);
});

test('button sketch (C++): input pull-up and bool printing', () => {
  const a = run(SKETCHES.button, { seconds: 0.3, inputs: { nodes: { 7: 0 }, volts: { 0: 0 } } });   // pin 7 held at 0 V = pressed
  assert.strictEqual(a.mcu.err, null);
  assert.strictEqual(a.mcu.out[3], 1, 'LED should be on');
  assert(serialOf(a.mcu).includes('button pressed'), JSON.stringify(serialOf(a.mcu)));
});

test('adc sketch (C++): int and float arithmetic, Serial.print(x, 2)', () => {
  const { mcu } = run(SKETCHES.adc, { seconds: 0.5, inputs: { nodes: { 2: 1 }, volts: { 1: 1.65 } } });
  assert.strictEqual(mcu.err, null);
  const line = serialOf(mcu)[0];
  assert(/ADC = 2048 {3}1\.65 V/.test(line), line);
  assert(Math.abs(mcu.pwm[3] - 127 / 255) < 0.01, 'pwm ' + mcu.pwm[3]);
});

test('helper function may call delay()', () => {
  const { mcu, log } = run(SKETCHES.helper, { seconds: 1.0 });
  assert.strictEqual(mcu.err, null);
  const t = toggles(log, 3);
  assert(t.length >= 6 && Math.abs(t[1].t - t[0].t - 0.1) < 0.005 && Math.abs(t[5].t - t[0].t - 0.5) < 0.005, JSON.stringify(t.slice(0, 7)));
});

function serialRun(body, globals = '') {
  const { mcu } = run(`${globals}\nvoid setup() { Serial.begin(115200); }\nvoid loop() {\n${body}\n delay(1000); }`, { seconds: 0.1 });
  assert.strictEqual(mcu.err, null, mcu.err);
  return serialOf(mcu);
}

test('integer division truncates, float division does not', () => {
  assert.deepStrictEqual(serialRun('int a = 7, b = 2; Serial.println(a / b); Serial.println(7 / 2.0); Serial.println(a / 2.0);'), ['3', '3.5', '3.5']);
  assert.deepStrictEqual(serialRun('int a = 7; float f = a / 2; Serial.println(f);'), ['3']);
  assert.deepStrictEqual(serialRun('int a = 7; float f = (float)a / 2; Serial.println(f);'), ['3.5']);
  assert.deepStrictEqual(serialRun('int a = 7; Serial.println(a * 3 / 2);'), ['10']);
  assert.deepStrictEqual(serialRun('int n = 9; n /= 2; Serial.println(n);'), ['4']);
});

test('int variables truncate on assignment; casts work', () => {
  assert.deepStrictEqual(serialRun('int x = 3.9; Serial.println(x); x = 2.5 * 3; Serial.println(x); Serial.println((int)7.8);'), ['3', '7', '7']);
});

test('bool prints as 0/1; true/false literals', () => {
  assert.deepStrictEqual(serialRun('bool b = 3 > 2; bool c = false; Serial.println(b); Serial.println(c);'), ['1', '0']);
});

test('#define, const, arrays, for loops, ternary', () => {
  const out = serialRun('int total = 0; for (int i = 0; i < N; i++) { total += data[i]; } Serial.println(total); Serial.println(total > 5 ? "big" : "small"); int z[3]; z[1] = 4; Serial.println(z[0] + z[1]);',
    '#define N 3\nconst int data[] = {1, 2, 3};');
  assert.deepStrictEqual(out, ['6', 'big', '4']);
});

test('user function with return value and parameters', () => {
  assert.deepStrictEqual(serialRun('Serial.println(square(5) + half(9));', 'int square(int a) { return a * a; }\nint half(int a) { return a / 2; }'), ['29']);
});

test('prototypes are accepted', () => {
  assert.deepStrictEqual(serialRun('Serial.println(twice(4));', 'int twice(int);\nint twice(int a) { return 2 * a; }'), ['8']);
});

test('strings and comments are not mangled', () => {
  assert.deepStrictEqual(serialRun('Serial.println("a / b // not a comment, int x = 3;"); /* int y = 5 / 2; */ // delay(100);\n Serial.println("done");'), ['a / b // not a comment, int x = 3;', 'done']);
});

test('while loop is guarded against an endless loop', () => {
  const { mcu } = run('void setup() { while (true) { } }\nvoid loop() {}', { seconds: 0.1 });
  assert(/too long without delay/.test(mcu.err || ''), String(mcu.err));
});

test('millis() is an integer and advances', () => {
  const out = serialRun('Serial.println(millis() >= 0 ? "ok" : "no"); unsigned long t = millis() / 10; Serial.println(t);');
  assert.strictEqual(out[0], 'ok');
});

test('user declarations may shadow runtime names (PI, map)', () => {
  assert.deepStrictEqual(serialRun('Serial.println(PI);', 'const float PI = 3.0;'), ['3']);
});

test('hex output: Serial.println(x, HEX)', () => {
  assert.deepStrictEqual(serialRun('Serial.println(255, HEX);'), ['FF']);
});

test('ESP32 PWM: ledcAttach / ledcWrite', () => {
  const { mcu } = run('void setup() { ledcAttach(3, 5000, 8); ledcWrite(3, 128); }\nvoid loop() { delay(10); }', { seconds: 0.05 });
  assert.strictEqual(mcu.err, null, mcu.err);
  assert(Math.abs(mcu.pwm[3] - 128 / 255) < 1e-6, String(mcu.pwm[3]));
});

test('JavaScript sketches still run (older circuits)', () => {
  const js = 'const LED = 3;\nfunction setup() { pinMode(LED, OUTPUT); }\nfunction loop() { digitalWrite(LED, HIGH); delay(100); digitalWrite(LED, LOW); delay(100); }';
  const { mcu, log } = run(js, { seconds: 0.5 });
  assert.strictEqual(mcu.err, null, mcu.err);
  assert(toggles(log, 3).length >= 4);
});

/* ---- unsupported constructs give an error that names the construct and the line */
function errorOf(code) { const { mcu } = run(code, { seconds: 0.01 }); return mcu.err || ''; }
const wrap = body => `void setup() {}\nvoid loop() {\n${body}\n}`;
test('error: class', () => { const e = errorOf('class A { };\n' + wrap('')); assert(/line 1.*'class'/.test(e), e); });
test('error: pointer', () => { const e = errorOf(wrap('int *p;')); assert(/line 3.*pointer/.test(e), e); });
test('error: unknown library', () => { const e = errorOf('#include <WiFi.h>\n' + wrap('')); assert(/line 1.*WiFi\.h/.test(e), e); });
test('error: static local', () => { const e = errorOf(wrap('static int n = 0;')); assert(/line 3.*static/.test(e), e); });
test('error: struct', () => { const e = errorOf(wrap('\nstruct P { int x; };')); assert(/line 4.*struct/.test(e), e); });
test('error: unknown function', () => { const e = errorOf(wrap('WiFi.begin("x");')); assert(/WiFi.*not declared/.test(e), e); });
test('error: function-like macro', () => { const e = errorOf('#define SQ(x) ((x)*(x))\n' + wrap('')); assert(/line 1.*macro/.test(e), e); });

console.log(`\n${passed} passed, ${failed} failed`);
process.exit(failed ? 1 : 0);
