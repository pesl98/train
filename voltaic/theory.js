/* Voltaic theory content — equations (KaTeX), diagrams and live plots via the shared Theory panel. */
(function () {
  const T = String.raw;
  const f = (v, u) => fmtEng(v, u);
  const mv = c => c.m || { v: 0, i: 0 };
  const live = (c, extra) => { const m = mv(c); return `${c.name || c.type}:  V = ${f(m.v || 0, 'V')}   I = ${f(m.i || 0, 'A')}   P = ${f((m.v || 0) * (m.i || 0), 'W')}` + (extra ? '   ' + extra : ''); };
  const scale = mx => mx < 1e-3 ? [1e6, 'µA'] : mx < 1 ? [1e3, 'mA'] : [1, 'A'];
  const C = { cy: '#22d3ee', vi: '#a78bfa', am: '#fbbf24', gr: '#4ade80', pk: '#f472b6' };

  /* ---------- little schematic helpers (SVG paths) ---------- */
  const zv = (x, y0, y1) => { const n = 6, a = y0 + 8, b = y1 - 8, d = (b - a) / n; let p = `M${x} ${y0}V${a}`; for (let i = 0; i < n; i++) p += `L${x + (i % 2 ? -8 : 8)} ${a + d * (i + .5)}`; return p + `L${x} ${b}V${y1}`; };
  const zh = (x0, x1, y) => { const n = 6, a = x0 + 8, b = x1 - 8, d = (b - a) / n; let p = `M${x0} ${y}H${a}`; for (let i = 0; i < n; i++) p += `L${a + d * (i + .5)} ${y + (i % 2 ? -7 : 7)}`; return p + `L${b} ${y}H${x1}`; };
  const svg = (w, h, body) => `<svg viewBox="0 0 ${w} ${h}" width="${w}" role="img"><defs><marker id="ah" viewBox="0 0 10 10" refX="8" refY="5" markerWidth="7" markerHeight="7" orient="auto"><path d="M0 0L10 5L0 10z" fill="#fbbf24"/></marker></defs>${body}</svg>`;
  const gnd = (x, y) => `<path class="sym" d="M${x} ${y}V${y + 6}M${x - 11} ${y + 6}H${x + 11}M${x - 7} ${y + 11}H${x + 7}M${x - 3} ${y + 16}H${x + 3}"/>`;
  const dot = (x, y) => `<circle cx="${x}" cy="${y}" r="3.5" fill="#cfd6ff"/>`;
  const tx = (x, y, s, cls = 'lb', a = 'start') => `<text class="${cls}" x="${x}" y="${y}" text-anchor="${a}">${s}</text>`;

  const sub = (b, t) => `${b}<tspan font-size="10" dy="3">${t}</tspan><tspan dy="-3"></tspan>`;
  const dividerSvg = svg(250, 200,
    `<path class="sym" d="${zv(70, 30, 84)}${zv(70, 108, 162)}M70 84V108"/>` + dot(70, 96) +
    `<path class="sym" d="M70 20V30M70 162V170"/>` + gnd(70, 170) +
    `<path class="sym" d="M70 96H146"/><circle cx="150" cy="96" r="4" class="sym"/>` +
    tx(70, 12, sub('V', 'in'), 'lb', 'middle') + tx(90, 64, sub('R', '1')) + tx(90, 142, sub('R', '2')) + tx(160, 100, sub('V', 'out')));

  const kclSvg = svg(250, 170,
    `<path class="sym" d="M20 40H110V130H20M110 85H230"/>` + dot(110, 85) +
    `<path d="M40 40H85" stroke="#fbbf24" stroke-width="2.4" marker-end="url(#ah)"/><path d="M40 130H85" stroke="#fbbf24" stroke-width="2.4" marker-end="url(#ah)"/><path d="M135 85H190" stroke="#fbbf24" stroke-width="2.4" marker-end="url(#ah)"/>` +
    tx(62, 30, sub('i', '1'), 'lb', 'middle') + tx(62, 120, sub('i', '2'), 'lb', 'middle') + tx(162, 74, sub('i', '3'), 'lb', 'middle') +
    tx(125, 164, 'i₁ + i₂ = i₃  (in = out)', 'lbm', 'middle'));

  const kvlSvg = svg(250, 170,
    `<path class="sym" d="M40 30H96M108 30H190V50M190 50V50M190 106V140H40V30"/><path class="sym" d="${zv(190, 50, 106)}"/>` +
    `<path class="sym" d="M96 20V40M108 25V35"/>` +
    `<path d="M95 112A28 28 0 1 1 134 108" fill="none" stroke="#fbbf24" stroke-width="2.4" marker-end="url(#ah)"/>` +
    tx(102, 14, sub('V', 's'), 'lb', 'middle') + tx(206, 82, 'R', 'lb') + tx(125, 164, 'Vs − V<tspan font-size="10" dy="3">R</tspan><tspan dy="-3"> = 0 around the loop</tspan>', 'lbm', 'middle'));

  const rcSvg = svg(260, 175,
    `<path class="sym" d="M50 30H80M50 30V64M50 74V130H220V84M220 70V30H190"/><path class="sym" d="${zh(80, 190, 30)}"/>` +
    `<path class="sym" d="M38 64H62M44 74H56M208 70H232M208 84H232"/>` +
    tx(135, 18, 'R', 'lb', 'middle') + tx(244, 82, 'C', 'lb') + tx(34, 70, sub('V', 's'), 'lb', 'end') + tx(135, 156, 'τ = R · C', 'lbm', 'middle'));

  const companionSvg = svg(380, 120,
    `<path class="sym" d="M60 14V44M44 44H76M44 54H76M60 54V84"/>` + tx(86, 54, 'C', 'lb') + tx(20, 108, 'capacitor', 'lbm') +
    `<path d="M125 50H185" stroke="#fbbf24" stroke-width="2.6" marker-end="url(#ah)"/>` + tx(155, 42, 'each step', 'lbm', 'middle') +
    `<path class="sym" d="M250 22H320M250 86H320M285 22V8M285 86V100"/><path class="sym" d="${zv(250, 22, 86)}"/><circle cx="320" cy="54" r="16" class="sym"/><path class="sym" d="M320 22V38M320 70V86"/><path d="M320 63V45" stroke="#fbbf24" stroke-width="2" marker-end="url(#ah)"/>` +
    tx(266, 58, sub('G', 'eq')) + tx(342, 58, sub('I', 'eq')) + tx(285, 112, 'equivalent circuit', 'lbm', 'middle'));

  const mcuSvg = svg(300, 120,
    `<path class="sym" d="M20 30H60M60 30L92 18M96 30H125"/><path class="sym" d="${zh(125, 190, 30)}M190 30H235"/><circle cx="238" cy="30" r="4" class="sym"/>` +
    tx(20, 20, 'Vdd', 'lb') + tx(158, 16, '25 Ω', 'lbm', 'middle') + tx(248, 34, 'pin', 'lb') +
    `<path class="sym" d="M20 90H60M60 90L92 102M96 90H125"/><path class="sym" d="${zh(125, 190, 90)}M190 90H235"/><circle cx="238" cy="90" r="4" class="sym"/>` +
    tx(20, 110, 'GND', 'lb') + tx(248, 94, 'pin', 'lb') + tx(150, 62, 'HIGH  or  LOW', 'lbm', 'middle'));

  /* ---------- per-part content ---------- */
  const PART = {
    R: c => {
      const m = mv(c), R = c.p.r, vm = Math.max(Math.abs(m.v), 1) * 1.6, [k, u] = scale(vm / R);
      return { h: "Resistor — Ohm's law", p: 'Current is proportional to voltage. All of the electrical power is turned into heat.',
        tex: [T`V = I\,R`, T`P = V I = I^{2}R = \dfrac{V^{2}}{R}`, T`\text{MNA stamp: } g = \dfrac{1}{R}\ \text{added to both nodes}`],
        svg: Theory.plot({ f: v => v / R * k, xr: [-vm, vm], xl: 'V (volts)', yl: `I (${u})`, title: 'I–V characteristic', point: [m.v, m.i * k, 'now'] }),
        live: live(c, `R = ${f(R, 'Ω')}`) };
    },
    POT: c => ({ h: 'Potentiometer — adjustable voltage divider', p: 'The wiper splits the track into two resistors that always add up to the total.',
      tex: [T`R_A = w\,R \qquad R_B = (1-w)\,R \qquad R_A + R_B = R`, T`V_{wiper} = V_{in}\,\dfrac{R_B}{R_A + R_B} = V_{in}\,(1-w)`],
      svg: Theory.plot({ f: w => 1 - w, xr: [0, 1], yr: [0, 1], xl: 'wiper position w', yl: 'V_wiper / V_in', point: [c.p.w, 1 - c.p.w, `w=${(+c.p.w).toFixed(2)}`] }), live: live(c, `R = ${f(c.p.r, 'Ω')}`) }),
    C: c => ({ h: 'Capacitor', p: 'Stores energy in an electric field. Current flows only while the voltage is changing; after about five time constants it is fully charged.',
      tex: [T`i = C\,\dfrac{dv}{dt} \qquad E = \tfrac12 C v^{2}`, T`v(t) = V_s\left(1 - e^{-t/RC}\right) \quad(\text{charging}) \qquad v(t) = V_0\,e^{-t/RC} \quad(\text{discharging})`,
        T`\text{trapezoidal rule: } G_{eq} = \dfrac{2C}{h},\qquad I_{eq} = G_{eq}\,v_n + i_n`],
      svg: [Theory.plot({ series: [{ f: t => 1 - Math.exp(-t), col: C.cy, label: 'charge', at: .55 }, { f: t => Math.exp(-t), col: C.vi, label: 'discharge', at: .3 }], xr: [0, 5], yr: [0, 1.05], xl: 'time (in τ = RC)', yl: 'v / V', hlines: [{ y: .632, label: '63 %' }], vlines: [{ x: 1, label: 'τ' }], title: 'RC response' }), rcSvg],
      live: live(c, `C = ${f(c.p.c, 'F')}   E = ${f(0.5 * c.p.c * (mv(c).v || 0) ** 2, 'J')}`) }),
    L: c => ({ h: 'Inductor', p: 'Stores energy in a magnetic field. The current cannot jump — it rises gradually, which is why switching an inductor off can create large voltage spikes.',
      tex: [T`v = L\,\dfrac{di}{dt} \qquad E = \tfrac12 L i^{2}`, T`i(t) = \dfrac{V_s}{R}\left(1 - e^{-t/\tau}\right),\qquad \tau = \dfrac{L}{R}`, T`\text{trapezoidal rule: } G_{eq} = \dfrac{h}{2L},\qquad I_{eq} = i_n + G_{eq}\,v_n`],
      svg: Theory.plot({ series: [{ f: t => 1 - Math.exp(-t), col: C.cy, label: 'energise', at: .55 }, { f: t => Math.exp(-t), col: C.vi, label: 'de-energise', at: .3 }], xr: [0, 5], yr: [0, 1.05], xl: 'time (in τ = L/R)', yl: 'i / I_max', hlines: [{ y: .632, label: '63 %' }], vlines: [{ x: 1, label: 'τ' }], title: 'RL current' }),
      live: live(c, `L = ${f(c.p.l, 'H')}   E = ${f(0.5 * c.p.l * (mv(c).i || 0) ** 2, 'J')}`) }),
    SW: c => ({ h: 'Switch', p: 'An almost-ideal switch: tiny resistance when closed, enormous when open. After each toggle the solver takes one backward-Euler step to avoid numerical ringing.',
      tex: [T`R_{closed} = 1\,\text{m}\Omega \qquad R_{open} = 1\,\text{T}\Omega`], live: live(c, c.p.closed ? 'closed' : 'open') }),
    LAMP: c => { const Pr = c.p.rated, P = Math.abs(mv(c).v * mv(c).i);
      return { h: 'Lamp', p: 'A resistor whose displayed brightness follows its dissipated power relative to its rating (perception is non-linear, hence the exponent).',
        tex: [T`P = \dfrac{V^{2}}{R} \qquad \text{brightness} = \min\!\left(1,\ \left(\dfrac{P}{P_{rated}}\right)^{0.7}\right)`],
        svg: Theory.plot({ f: x => Math.min(1, Math.pow(x, .7)), xr: [0, 1.5], yr: [0, 1.1], xl: 'P / P_rated', yl: 'brightness', point: [P / Pr, Math.min(1, Math.pow(P / Pr, .7)), 'now'] }), live: live(c, `rated ${f(Pr, 'W')}`) }; },
    V: c => ({ h: 'Ideal DC voltage source', p: 'Fixes the voltage between its terminals. The current is not known in advance, so it becomes an extra unknown with its own row in the matrix.',
      tex: [T`v_{+} - v_{-} = V_s`, T`\begin{bmatrix} G & B \\ B^{T} & 0 \end{bmatrix}\begin{bmatrix} \mathbf v \\ i_s \end{bmatrix} = \begin{bmatrix} \mathbf 0 \\ V_s \end{bmatrix}`], live: live(c, `Vs = ${f(c.p.v, 'V')}`) }),
    AC: c => { const q = { p: { ...c.p } }, per = 1 / Math.max(c.p.freq, 1e-9);
      return { h: 'Signal source', p: 'A time-varying source. The waveform below is exactly what this source produces.',
        tex: [T`v(t) = V_{off} + A\,\sin(2\pi f t) \qquad T = \dfrac{1}{f}`, T`\text{square: } \pm A \qquad \text{triangle and saw: linear ramps between } -A \text{ and } +A`],
        svg: Theory.plot({ f: x => srcValue(q, x * per), xr: [0, 2], xl: 'time (periods)', yl: 'volts', title: `${c.p.wave}, ${f(c.p.freq, 'Hz')}` }), live: live(c, `A = ${f(c.p.amp, 'V')}  f = ${f(c.p.freq, 'Hz')}`) }; },
    I: c => ({ h: 'Ideal current source', p: 'Forces a fixed current through itself; the voltage across it settles wherever the circuit needs.', tex: [T`i = I_s`], live: live(c) }),
    D: c => diodeBlock(c, 'Diode — the Shockley equation', 'Current grows exponentially with forward voltage and is negligible in reverse. Because of this steep curve the solver iterates (Newton–Raphson) with SPICE voltage limiting.', T`\text{This model: } I_S = 2.5\,\text{nA},\ n = 1.75`),
    LED: c => diodeBlock(c, 'LED', 'A diode whose forward voltage depends on colour. It needs a series resistor: past the knee a tiny voltage increase causes a huge current increase.', T`R_{series} = \dfrac{V_s - V_f}{I_{wanted}}`),
    ZD: c => diodeBlock(c, 'Zener diode', 'Behaves like a normal diode forwards. In reverse it breaks down near V_z and holds the voltage almost constant — the basis of a simple regulator (the model breaks down about 0.25 V early to reproduce the soft knee).', T`R_{series} = \dfrac{V_{in} - V_z}{I_{load} + I_z}`),
    NPN: c => bjt(c, 'NPN bipolar transistor', 'A small base current controls a much larger collector current. Modelled with the Ebers–Moll equations (I_S = 10⁻¹⁴ A, β_R = 2).'),
    PNP: c => bjt(c, 'PNP bipolar transistor', 'The mirror image of the NPN: all voltages and currents reverse sign, so it conducts when the base is pulled below the emitter.'),
    OP: c => { const R = c.p.rail, A = 1e5, span = 3 * R / A * 1000;
      return { h: 'Op-amp', p: 'A differential amplifier with enormous gain that saturates smoothly at the supply rails. With negative feedback it adjusts its output until the two inputs are (almost) equal.',
        tex: [T`v_{out} = R_{rail}\,\tanh\!\left(\dfrac{A\,(v_{+}-v_{-})}{R_{rail}}\right) \qquad A = 10^{5}`, T`\text{inverting: } \dfrac{v_{out}}{v_{in}} = -\dfrac{R_f}{R_{in}} \qquad \text{non-inverting: } \dfrac{v_{out}}{v_{in}} = 1 + \dfrac{R_f}{R_g}`],
        svg: Theory.plot({ series: [{ f: x => R * Math.tanh(A * x / 1000 / R), col: C.cy }, { f: x => A * x / 1000, col: C.vi, dash: true, w: 1.4 }], xr: [-span, span], yr: [-R * 1.2, R * 1.2], xl: 'v₊ − v₋ (mV)', yl: 'v_out (V)', title: 'transfer curve (dashed = ideal gain)' }), live: live(c, `rail ±${f(R, 'V')}`) }; },
    MCU: c => ({ h: 'Microcontroller pins', p: 'Your sketch advances with simulated time. Each output is a driver switched to the supply or to ground through 25 Ω; inputs read high above half the supply; INPUT_PULLUP adds 45 kΩ to the supply.',
      tex: [T`V_{pin} = V_{dd} - I\cdot 25\,\Omega \quad(\text{HIGH}) \qquad \text{ADC} = \operatorname{round}\!\left(\dfrac{V}{V_{dd}}\,(2^{N}-1)\right)`, T`\text{PWM (averaged): } V_{avg} = \dfrac{\text{duty}}{255}\,V_{dd}`],
      svg: mcuSvg, live: live(c, c.p.board) }),
    GND: () => ({ h: 'Ground', p: 'The 0 V reference. Every voltage in the circuit is measured relative to it.', tex: [T`v_{gnd} \equiv 0`], live: '' }),
    PROBE: c => ({ h: 'Scope probe', p: "Adds this node's voltage to the oscilloscope.", live: live(c) }),
  };

  function diodeBlock(c, h, p, extraTex) {
    const m = diodeModel(c), v = mv(c).v, i = mv(c).i;
    const isZ = c.type === 'ZD', vlo = isZ ? -(c.p.vz + 1.2) : -0.5, vhi = c.type === 'LED' ? ((LED_COLORS[c.p.color] || LED_COLORS.red).vf + 0.5) : 1.0;
    const cur = x => { let y = m.is * (Math.exp(Math.min(x / m.nvt, 60)) - 1); if (m.vz > 0) y -= m.iz * (Math.exp(Math.min((-x - m.vz) / m.nvz, 60)) - 1); return y * 1000; };
    const out = { h, p, tex: [T`I = I_S\left(e^{\,V/(n V_T)} - 1\right) \qquad V_T = \dfrac{kT}{q} \approx 25.85\,\text{mV}`, extraTex,
      T`\text{Newton step: } G = \dfrac{dI}{dV},\quad I_{eq} = I - G\,V`],
      svg: Theory.plot({ f: cur, xr: [vlo, vhi], yr: [isZ ? -30 : -2, 30], xl: 'V (volts)', yl: 'I (mA)', title: 'I–V curve of this part', point: [v, i * 1000, 'now'] }),
      live: live(c, c.type === 'LED' ? `${c.p.color}, Vf≈${(LED_COLORS[c.p.color] || LED_COLORS.red).vf} V` : isZ ? `Vz = ${f(c.p.vz, 'V')}` : '') };
    return out;
  }
  function bjt(c, h, p) {
    const b = c.p.beta, ib = [20, 40, 60, 80], cols = [C.cy, C.vi, C.gr, C.am];
    return { h, p, tex: [T`I_C = I_S\left(e^{V_{BE}/V_T} - e^{V_{BC}/V_T}\right) - \dfrac{I_S}{\beta_R}\left(e^{V_{BC}/V_T} - 1\right)`, T`I_B = \dfrac{I_S}{\beta_F}\left(e^{V_{BE}/V_T} - 1\right) + \dfrac{I_S}{\beta_R}\left(e^{V_{BC}/V_T} - 1\right)`,
      T`\text{active region: } I_C \approx \beta_F I_B,\qquad I_E = I_B + I_C \qquad \text{saturation: } V_{CE} \approx 0.2\,\text{V}`],
      svg: Theory.plot({ series: ib.map((x, k) => ({ f: v => b * x * 1e-3 * (1 - Math.exp(-v / 0.15)) * (1 + v / 75), col: cols[k], label: `${x} µA`, at: .9 })), xr: [0, 10], xl: 'V_CE (volts)', yl: 'I_C (mA)', title: `idealised output curves, β = ${b}` }),
      live: live(c, `β = ${b}`) };
  }

  /* ---------- general sections ---------- */
  const newton = Theory.plot({ series: [{ f: x => Math.exp(x) - 3, col: C.cy, label: 'F(x)', at: .75 }, { f: x => (Math.exp(2) - 3) + Math.exp(2) * (x - 2), col: C.vi, dash: true, w: 1.6 }],
    xr: [0, 2.4], yr: [-4, 9], hlines: [{ y: 0, col: '#4a5486' }], points: [[2, Math.exp(2) - 3, 'x_k'], [2 - (Math.exp(2) - 3) / Math.exp(2), 0, 'x_k+1']], xl: 'unknown (a node voltage)', yl: 'residual F', title: 'Newton–Raphson' });
  const GENERAL = [
    { h: "Kirchhoff's laws", p: 'Every circuit simulator is built on two conservation laws: charge cannot pile up at a node, and energy is conserved around a loop.', tex: [T`\text{KCL: } \sum_{k} i_k = 0 \quad(\text{at every node}) \qquad \text{KVL: } \sum_{k} v_k = 0 \quad(\text{around every loop})`], svg: [kclSvg, kvlSvg] },
    { h: 'Series, parallel and dividers', tex: [T`R_{series} = R_1 + R_2 \qquad \dfrac{1}{R_{par}} = \dfrac{1}{R_1} + \dfrac{1}{R_2}`, T`V_{out} = V_{in}\,\dfrac{R_2}{R_1 + R_2} \qquad I_1 = I\,\dfrac{R_2}{R_1 + R_2}`], svg: dividerSvg },
    { h: 'How Voltaic solves a circuit — modified nodal analysis', p: 'Every wire junction becomes a node. KCL is written for each node, and elements whose current is unknown (sources, inductors, op-amps) add extra rows. The result is one linear system, solved by Gaussian elimination with partial pivoting.',
      tex: [T`\begin{bmatrix} G & B \\ C & D \end{bmatrix}\begin{bmatrix} \mathbf v \\ \mathbf j \end{bmatrix} = \begin{bmatrix} \mathbf i \\ \mathbf e \end{bmatrix}`, T`G:\ \text{conductances} \quad \mathbf v:\ \text{node voltages} \quad \mathbf j:\ \text{source/inductor currents} \quad g_{min} = 10^{-11}\,\text{S to ground}`] },
    { h: 'Time stepping — companion models', p: 'Capacitors and inductors are replaced in every time step by a resistor plus a current source whose values come from the previous step (trapezoidal rule, second-order accurate). After a sudden change, one backward-Euler step is taken (G = C/h) to remove numerical ringing.',
      tex: [T`i_{n+1} = G_{eq}\,v_{n+1} - I_{eq}`], svg: companionSvg },
    { h: 'Nonlinear parts — Newton–Raphson', p: 'Diodes and transistors are linearised around the current guess, the circuit is solved, and the process repeats until the voltages stop changing. The step is limited (SPICE “pnjlim”) so exponentials cannot overflow.',
      tex: [T`x_{k+1} = x_k - \dfrac{F(x_k)}{F'(x_k)}`], svg: newton },
    { h: 'Handy formulas', tex: [T`P = V I \qquad \tau = R C \quad(63\%\ \text{after } 1\tau,\ 99\%\ \text{after } 5\tau)`, T`f_0 = \dfrac{1}{2\pi\sqrt{LC}} \qquad X_C = \dfrac{1}{2\pi f C} \qquad X_L = 2\pi f L \qquad f_c = \dfrac{1}{2\pi R C}`] },
  ];

  window.openTheory = function () {
    let focus = null;
    if (typeof sel !== 'undefined' && sel && sel.k === 'c') { const c = compById(sel.id); if (c && PART[c.type]) { try { focus = PART[c.type](c); } catch (e) { console.error(e); } } }
    Theory.open({ title: 'The mathematics of Voltaic', intro: focus ? 'Your selected part is shown first, with its live operating point.' : 'Tip: select a part, then reopen this panel to see its own equations, curve and live values.', focus, sections: GENERAL });
  };
})();
