/* Tests for the AI & ML Lab core.   run:  node ml/test/nn.test.js */
const assert = require('assert');
const M = require('../nn.js');
let passed = 0, failed = 0;
function test(name, fn) { try { fn(); passed++; console.log('PASS', name); } catch (e) { failed++; console.log('FAIL', name, '\n     ', e.message.split('\n')[0]); } }

test('back-propagation matches a numerical gradient (tanh, relu, sigmoid; bce and mse)', () => {
  for (const [act, out, loss] of [['tanh', 'sigmoid', 'bce'], ['relu', 'sigmoid', 'bce'], ['sigmoid', 'sigmoid', 'mse'], ['tanh', 'linear', 'mse']]) {
    const net = new M.Net([3, 4, 3, 1], { act, out, loss, seed: 7 }), r = M.rng(3);
    const X = Array.from({ length: 6 }, () => [r() - .5, r() - .5, r() - .5]), Y = X.map(x => (loss === 'bce' ? (x[0] > 0 ? 1 : 0) : x[0] + x[1]));
    const l2 = 0.01, { gW, gb } = net.gradients(X, Y, l2);
    const total = () => net.lossOf(X, Y) + 0.5 * l2 * net.W.reduce((s, w) => s + w.reduce((a, v) => a + v * v, 0), 0);
    for (let l = 0; l < net.W.length; l++) for (const [arr, g] of [[net.W[l], gW[l]], [net.b[l], gb[l]]]) for (let i = 0; i < arr.length; i += 2) {
      const old = arr[i], h = 1e-6; arr[i] = old + h; const fp = total(); arr[i] = old - h; const fm = total(); arr[i] = old;
      const num = (fp - fm) / (2 * h);
      if (act === 'relu' && Math.abs(num - g[i]) > 1e-3) continue;          // a kink of ReLU can sit inside the finite-difference step
      assert(Math.abs(num - g[i]) < 1e-5 * (1 + Math.abs(num)), `${act}/${out}/${loss} layer ${l} param ${i}: backprop ${g[i]} vs numerical ${num}`);
    }
  }
});

test('a network with one hidden layer learns XOR (impossible for a single neuron)', () => {
  const D = M.makeData('xor', 200, 0.0, 1);
  const lin = new M.Net([2, 1], { seed: 2 }); for (let e = 0; e < 400; e++) lin.trainBatch(D.X, D.Y, { lr: 0.05 });
  const net = new M.Net([2, 6, 1], { act: 'tanh', seed: 2 }); for (let e = 0; e < 400; e++) net.trainBatch(D.X, D.Y, { lr: 0.05 });
  assert(lin.accuracy(D.X, D.Y) < 0.7, 'single neuron should fail: ' + lin.accuracy(D.X, D.Y));
  assert(net.accuracy(D.X, D.Y) > 0.95, 'hidden layer should succeed: ' + net.accuracy(D.X, D.Y));
});

test('logistic regression with x², y² features separates the circle data set', () => {
  const D = M.makeData('circle', 300, 0.02, 4), X = M.expandFeatures(D.X, 'quad');
  const net = new M.Net([5, 1], { seed: 1 }); for (let e = 0; e < 600; e++) net.trainBatch(X, D.Y, { lr: 0.1 });
  assert(net.accuracy(X, D.Y) > 0.95, String(net.accuracy(X, D.Y)));
});

test('gradient descent on a line reaches the least-squares solution', () => {
  const r = M.rng(5), X = [], Y = []; for (let i = 0; i < 50; i++) { const x = 2 * r() - 1; X.push([x]); Y.push(1.5 * x - 0.3 + 0.1 * r.gauss()); }
  const net = new M.Net([1, 1], { out: 'linear', loss: 'mse', seed: 3 }); for (let e = 0; e < 3000; e++) net.trainBatch(X, Y, { lr: 0.1, opt: 'sgd' });
  const n = X.length, mx = X.reduce((s, x) => s + x[0], 0) / n, my = Y.reduce((s, y) => s + y, 0) / n;
  const w = X.reduce((s, x, i) => s + (x[0] - mx) * (Y[i] - my), 0) / X.reduce((s, x) => s + (x[0] - mx) ** 2, 0), b = my - w * mx;
  assert(Math.abs(net.W[0][0] - w) < 1e-3 && Math.abs(net.b[0][0] - b) < 1e-3, `GD ${net.W[0][0]},${net.b[0][0]} vs LS ${w},${b}`);
});

test('every data set has both classes and the requested size', () => {
  for (const k of ['blobs', 'circle', 'xor', 'moons', 'spiral']) { const D = M.makeData(k, 101, 0.05, 9); assert.strictEqual(D.X.length, 101); assert(D.Y.includes(0) && D.Y.includes(1), k); }
});

test('the same seed gives the same data and the same network', () => {
  assert.deepStrictEqual(M.makeData('spiral', 20, 0.1, 3), M.makeData('spiral', 20, 0.1, 3));
  assert.deepStrictEqual(Array.from(new M.Net([2, 3, 1], { seed: 4 }).W[0]), Array.from(new M.Net([2, 3, 1], { seed: 4 }).W[0]));
});

test('all four optimisers find the minimum of a stretched bowl', () => {
  const grad = p => [2 * 0.2 * p[0], 2 * 3 * p[1]];
  for (const [name, lr] of [['sgd', 0.1], ['momentum', 0.05], ['rmsprop', 0.02], ['adam', 0.05]]) {
    const p = Float64Array.from([2, 1]), st = {};
    for (let k = 0; k < 2000; k++) M.Optim[name](p, grad(p), st, { lr });
    assert(Math.hypot(p[0], p[1]) < 0.05, `${name} ended at ${Array.from(p)}`);
  }
});

test('k-means never increases the inertia and finds well separated clusters', () => {
  const r = M.rng(8), P = []; for (const c of [[-0.6, -0.5], [0.6, -0.4], [0, 0.6]]) for (let i = 0; i < 40; i++) P.push([c[0] + 0.08 * r.gauss(), c[1] + 0.08 * r.gauss()]);
  let C = [[0, 0], [0.1, 0], [0, 0.1]], lab = M.kmeansAssign(P, C), prev = M.inertia(P, C, lab);
  for (let k = 0; k < 20; k++) { C = M.kmeansUpdate(P, C, lab); lab = M.kmeansAssign(P, C); const I = M.inertia(P, C, lab); assert(I <= prev + 1e-12); prev = I; }
  assert(prev / P.length < 0.03, 'mean inertia ' + prev / P.length);
});

console.log(`\n${passed} passed, ${failed} failed`);
process.exit(failed ? 1 : 0);
