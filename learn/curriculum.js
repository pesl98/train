/* Year 1 curriculum map — data only. The hub (index.html) renders this.
   Shaped by the Week 0 diagnostic (17/44): strong algebra and exp/log; weak trig, derivatives, integrals;
   series, complex numbers and physics start from zero. Edit freely as progress suggests.
   A unit with `notebooks` gets one link per notebook: { id, title, path }. `id` is the notebook's own id
   (the hub reads its saved results `<id>-results.json` from the browser storage of JupyterLite and shows the score).
   A unit with a single `notebook` path gets a plain "Open notebook" link; `labs` link to simulators. */
const LAB = {
  volt: ['Voltaic', 'voltaic/index.html'],
  phys: ['Physics Lab', 'physics/index.html'],
  rob: ['Robotics Lab', 'robotics/index.html'],
};
const CURRICULUM = [
  {
    title: 'Term 0 — Diagnostic', desc: 'Done: 17/44. Solid: algebra, exp/log. Weak: trig, derivatives, integrals, limits. From zero: series, complex numbers, physics.',
    units: [
      { id: 'w0', title: 'Week 0 — Diagnostic', weeks: 'week 0', topics: '44 problems across 11 topics. Result sets the pace and emphasis of everything after.', notebook: 'year1/w00-diagnostic.ipynb', deliverables: ['nb'] },
    ],
  },
  {
    title: 'Term 1 — Calculus rebuilt', desc: 'Weeks 1–12. Rhythm per week (20 h): 6 reading, 6 paper problems, 3 notebook/simulator, 3 physics strand, 2 error review.',
    units: [
      { id: 'u1', title: 'Functions, trig & limits', weeks: 'weeks 1–3', notebooks: [
          { id: 'u01w1', title: 'Week 1 — Functions, radians, the unit circle', path: 'year1/u01w1-functions-radians-circle.ipynb' },
          { id: 'u01w2', title: 'Week 2 — Identities, inverse trig, sinusoids', path: 'year1/u01w2-identities-sinusoids.ipynb' },
          { id: 'u01w3', title: 'Week 3 — Limits and continuity', path: 'year1/u01w3-limits-continuity.ipynb' },
        ], topics: 'Function families and graphs, radians, unit circle, trig identities, inverse trig, limits and continuity. Daily 15-minute drill on the unit circle and identities.', labs: [LAB.phys] },
      { id: 'u2', title: 'Derivatives', weeks: 'weeks 4–7', notebooks: [
          { id: 'u02w1', title: 'Week 4 — The derivative from first principles', path: 'year1/u02w1-derivative-definition.ipynb' },
          { id: 'u02w2', title: 'Week 5 — The rules: product, quotient, chain', path: 'year1/u02w2-rules-of-differentiation.ipynb' },
          { id: 'u02w3', title: 'Week 6 — Implicit, related rates, Newton’s method', path: 'year1/u02w3-implicit-rates-newton.ipynb' },
          { id: 'u02w4', title: 'Week 7 — Maxima, minima and optimisation', path: 'year1/u02w4-optimisation.ipynb' },
        ], topics: 'Definition, power/product/quotient/chain rules, trig/exp/log derivatives, implicit differentiation, optimisation, velocity and acceleration. Four weeks: 2/6 in the diagnostic.', labs: [LAB.phys, LAB.volt] },
      { id: 'u3', title: 'Integrals', weeks: 'weeks 8–10', topics: 'Riemann sums, fundamental theorem, substitution, by parts, work and energy as integrals.', labs: [LAB.volt, LAB.phys] },
      { id: 'u4', title: 'Series & Taylor expansions', weeks: 'weeks 11–12', topics: 'Taught from scratch: convergence, geometric series, power series, Taylor polynomials, small-angle approximation.', labs: [LAB.phys] },
      { id: 'p1', title: 'Physics strand (parallel, 3 h/week)', weeks: 'weeks 1–12', topics: 'Units and dimensional analysis, vectors in physics, kinematics, Newton\'s laws, energy, Ohm and Kirchhoff. Light on maths; grows as calculus arrives.', labs: [LAB.phys, LAB.volt] },
    ],
  },
  {
    title: 'Term 2 — ODEs, linear algebra & dynamics', desc: 'Weeks 13–26. First-order ODEs now follow solid derivatives and integrals.',
    units: [
      { id: 'u5', title: 'First-order ODEs & numerical solution', weeks: 'weeks 13–15', topics: 'Separable equations, exponential growth/decay, RC circuits, Euler vs Runge–Kutta, error and step size.', labs: [LAB.volt, LAB.phys] },
      { id: 'u6', title: 'Complex numbers & phasors', weeks: 'weeks 16–17', topics: 'Rectangular and polar form, Euler\'s formula, roots, impedance. Taught from scratch.', labs: [LAB.volt] },
      { id: 'u7', title: 'Vectors, matrices & linear systems', weeks: 'weeks 18–20', topics: 'Gaussian elimination, determinants, matrix algebra — the same method Voltaic uses to solve a circuit.', labs: [LAB.volt] },
      { id: 'u8', title: 'Eigenvalues & diagonalisation', weeks: 'weeks 21–22', topics: 'Eigenvectors, stability, normal modes of coupled oscillators.', labs: [LAB.phys] },
      { id: 'u9', title: 'Second-order ODEs & oscillators', weeks: 'weeks 23–24', topics: 'Damped and driven oscillation, resonance, transients.', labs: [LAB.phys] },
      { id: 'u10', title: 'Newtonian mechanics', weeks: 'weeks 25–26', topics: 'Forces, energy, momentum, central forces, Kepler orbits.', labs: [LAB.phys, LAB.rob] },
    ],
  },
  {
    title: 'Term 3 — Circuits & signals', desc: 'Weeks 27–36. AC circuits and the mathematics of waves.',
    units: [
      { id: 'u11', title: 'AC steady state & RLC circuits', weeks: 'weeks 27–31', topics: 'Impedance, transient and steady-state response, resonance, filters, circuit analysis methods.', labs: [LAB.volt] },
      { id: 'u12', title: 'Fourier series & signals', weeks: 'weeks 32–36', topics: 'Periodic signals, harmonics, frequency content, first look at control.', labs: [LAB.volt, LAB.rob] },
    ],
  },
];
