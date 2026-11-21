"""Physics strand · Part 4 (weeks 11-12) - charge, current, voltage, power, Ohm, series/parallel, dividers, Kirchhoff."""
import math
from nbkit import Book
import figs_p01 as F

B = Book('p01w4', 'Physics 4 — Ohm and Kirchhoff', 'year1/p01w4-ohm-kirchhoff.ipynb')
S1, S2, S3, S4 = '1 Charge, current, voltage, power', '2 Ohm, series and parallel', '3 Dividers and real sources', '4 Kirchhoff laws'
qe = 1.602e-19

B.md(r'''
# Physics 4 — Ohm and Kirchhoff: DC circuits
*Physics strand, weeks 11–12 · about 6 hours, next to Unit 4*

**Why.** You are training to work with electronics. Every circuit — a sensor on an ESP32, a phone charger, the RC filter of Unit 5 — rests on four quantities (charge, current, voltage, power), one material law (Ohm) and two conservation laws (Kirchhoff). With these you can solve *any* circuit of resistors and batteries — and you will see that it comes down to solving linear equations, the subject of Unit 7.

**What you will be able to do at the end**
1. Explain current as flow of charge and voltage as energy per charge; compute power and energy cost.
2. Use Ohm's law, resistivity, and the series and parallel rules — derived, not memorised.
3. Design a voltage divider, predict what a load does to it, and handle a battery's internal resistance.
4. Apply Kirchhoff's current and voltage laws to a circuit with two sources, solve it by hand and with `numpy`, and check it in the circuit simulator.

**Maths used:** algebra and simultaneous linear equations. Energy and power from Physics 3.

Run the grey *SETUP* cell first.
''')

# =====================================================================================
B.md(r'''
---
# Part 1 — Charge, current, voltage, power

## 1.1 Charge and current

**Charge** comes in tiny packets: an electron carries $-e$ with $e=1.602\times10^{-19}$ C. In a metal wire some electrons are free to drift.

**Current** is the rate at which charge passes a point:
$$I=\frac{dQ}{dt}\qquad(\text{amperes, A}=\text{C/s}).$$
1 A means $\frac{1}{1.602\times10^{-19}}=6.24\times10^{18}$ electrons per second. By convention current is drawn in the direction **positive** charge would move — from $+$ to $-$ outside a battery — even though in wires it is electrons drifting the other way. The sign convention never changes the answers.

## 1.2 Voltage: energy per charge

**Build.** A battery does work on the charges it pushes round the circuit. The **voltage** (potential difference) between two points is the energy gained or lost per coulomb going from one to the other:
$$V=\frac{\Delta E}{Q}\qquad(\text{volts, V}=\text{J/C}).$$
A 9 V battery gives every coulomb that passes through it 9 J. **Analogy:** voltage is like height in a water system, current like the flow of water. Water only flows from high to low; a pump (battery) lifts it back up.

Voltage is always **between two points**. "The voltage at a point" means relative to a chosen zero — the **ground** (0 V).

## 1.3 Power

**Build.** Every second, $I$ coulombs pass; each one exchanges $V$ joules. So the energy per second is
$$\boxed{\,P=V\,I\,}\qquad(\text{W}=\text{J/C}\times\text{C/s}=\text{J/s}).$$

**Worked example.** A 2000 W kettle on 230 V: $I=\frac{2000}{230}=8.7$ A. Running 6 minutes uses $2000\cdot360=720$ kJ $=0.2$ kWh; at €0.30 per kWh that costs 6 cents.
''')
B.ask(r'''A phone charger delivers 2.0 A for 30 minutes. How much charge (C) has flowed?''', 'num', 3600,
      r'''$Q=It=2.0\cdot1800=3600$ C.''', r'''$Q=I\,t$ with $t$ in seconds.''', fmt='coulombs')
B.ask(r'''A USB port supplies 5.0 V at 0.9 A. What power (W) does it deliver?''', 'num', 4.5,
      r'''$P=VI=4.5$ W.''', r'''$P=VI$.''', fmt='watts')

# =====================================================================================
B.md(r'''
---
# Part 2 — Ohm's law, series and parallel

## 2.1 Resistance and Ohm's law

**Definition.** The **resistance** of a component is the voltage across it divided by the current through it: $R=\frac{V}{I}$ (ohms, Ω $=$ V/A).

**Ohm's law** (an experimental fact for metals at constant temperature): $R$ does **not** depend on $V$ or $I$ — double the voltage, double the current:
$$\boxed{\,V=I\,R\,}$$
An LED or a diode does *not* obey it (its $I$–$V$ graph is not a straight line) — Voltaic models those separately.

**What sets $R$?** A longer wire resists more, a thicker one less:
$$R=\rho\,\frac{L}{A}$$
with the **resistivity** $\rho$ a property of the material (copper $1.7\times10^{-8}\ \Omega\,$m; nichrome heater wire $1.1\times10^{-6}$).

**Power in a resistor.** Combine $P=VI$ with $V=IR$:
$$P=I^2R=\frac{V^2}{R}.$$
That energy becomes heat — useful in a kettle, a nuisance in a chip. Resistors are sold by power rating (¼ W, ½ W …).

## 2.2 Series and parallel — derived from conservation
''')
B.fig('series_parallel', F.series_parallel, 'Series: one path. Parallel: two paths between the same two points.')
B.md(r'''
**Series (one path).** *Charge is conserved* — nothing piles up — so the **same current** $I$ flows through both. *Energy is conserved* — the energy per coulomb lost in $R_1$ and in $R_2$ adds up to what the battery gives:
$$V=V_1+V_2=IR_1+IR_2=I(R_1+R_2)\qquad\Rightarrow\qquad\boxed{\,R_s=R_1+R_2\,}$$

**Parallel (two paths between the same two points).** Both resistors connect the same two points, so they have the **same voltage** $V$. Charge is conserved where the wire splits, so the currents **add**:
$$I=I_1+I_2=\frac{V}{R_1}+\frac{V}{R_2}\qquad\Rightarrow\qquad\boxed{\,\frac1{R_p}=\frac1{R_1}+\frac1{R_2}\,}\quad\text{or}\quad R_p=\frac{R_1R_2}{R_1+R_2}.$$

**Sense checks.** Series makes resistance larger than either; parallel makes it **smaller than the smallest** (an extra path can only help the current). Two equal resistors in parallel: $\frac R2$. Anything in parallel with a short circuit (0 Ω): 0 Ω.

**Worked example — reduce step by step.** $6\ \Omega$ in series with ($6\ \Omega\parallel3\ \Omega$), on 12 V.
1. $6\parallel3=\frac{18}{9}=2\ \Omega$. 2. Total $6+2=8\ \Omega$. 3. Battery current $\frac{12}{8}=1.5$ A.
4. Voltage across the parallel pair $1.5\cdot2=3$ V; so $\frac36=0.5$ A through the $6\ \Omega$ branch and $\frac33=1$ A through the $3\ \Omega$ branch. Check: $0.5+1=1.5$ ✓.
''')
B.code(r'''
def series(*R): return sum(R)
def parallel(*R): return 1 / sum(1 / r for r in R)

print(series(6, parallel(6, 3)))          # the worked example: 8 ohm
print(parallel(1000, 1000, 1000))         # three 1k in parallel
''')
B.ask(r'''What is the resistance (Ω) of 100 Ω and 300 Ω in parallel?''', 'num', 75,
      r'''$\frac{100\cdot300}{400}=75\ \Omega$ — less than the smaller one ✓.''', r'''Product over sum.''', fmt='ohms')
B.ask(r'''A 9 V battery drives 30 mA through a resistor. What is the resistance (Ω)?''', 'num', 300,
      r'''$R=\frac VI=\frac{9}{0.030}=300\ \Omega$.''', r'''$R=V/I$ with $I$ in amperes.''', fmt='ohms')

# =====================================================================================
B.md(r'''
---
# Part 3 — Voltage dividers and real sources

## 3.1 The voltage divider
''')
B.fig('divider', F.divider, 'Two resistors in series share the input voltage in proportion to their resistance.')
B.md(r'''
**Why.** You often need a smaller voltage than the supply: an ESP32's analogue input accepts at most 3.3 V; a sensor gives a resistance that must be turned into a voltage. The voltage divider is the most-used circuit in electronics.

**Build.** No current leaves at $V_{out}$ (nothing is connected yet).
1. Series current: $I=\dfrac{V_{in}}{R_1+R_2}$.
2. Voltage across $R_2$: $V_{out}=IR_2$.
$$\boxed{\,V_{out}=V_{in}\,\frac{R_2}{R_1+R_2}\,}$$
**Worked example.** Bring 5 V down to 3.3 V with $R_1=1.0\ \text{k}\Omega$: $\frac{R_2}{1+R_2}=0.66\Rightarrow R_2=1.94\ \text{k}\Omega$ (use 2.0 kΩ: 3.33 V).

## 3.2 Loading

**Build.** Now connect a load $R_L$ across $R_2$. It is **in parallel** with $R_2$, so replace $R_2$ by $R_2\parallel R_L$ — always smaller — and $V_{out}$ drops.

**Worked example.** 9 V, $R_1=2\ \text{k}\Omega$, $R_2=1\ \text{k}\Omega$: unloaded $V_{out}=3$ V. Load $R_L=1\ \text{k}\Omega$: $R_2\parallel R_L=500\ \Omega$, $V_{out}=9\cdot\frac{0.5}{2.5}=1.8$ V. A big drop. **Rule of thumb:** the divider works if $R_L\gg R_2$ (ten times or more). This is why measuring instruments have a very high input resistance.

## 3.3 A real battery: internal resistance

**Build.** A real battery behaves like an ideal source $\mathcal E$ (the EMF) in series with a small internal resistance $r$. With a load $R$:
$$I=\frac{\mathcal E}{R+r},\qquad V_{\text{terminal}}=\mathcal E-Ir .$$
The more current you draw, the more the terminal voltage sags — which is why a car's lights dim while the starter motor runs.

### Experiment 1 — divider under load
**Predict first:** $R_1=R_2=10$ kΩ on 10 V gives 5 V. Roughly what is $V_{out}$ with a 10 kΩ load? With 100 kΩ? With 1 MΩ?
''')
B.code(r'''
def divider(Vin=10.0, R1_k=10.0, R2_k=10.0, RL_k=10.0):
    R2L = parallel(R2_k, RL_k)
    v_un, v_ld = Vin * R2_k / (R1_k + R2_k), Vin * R2L / (R1_k + R2L)
    RLs = np.logspace(-1, 3, 200)
    plt.figure(figsize=(7, 3.2)); plt.semilogx(RLs, [Vin * parallel(R2_k, r) / (R1_k + parallel(R2_k, r)) for r in RLs])
    plt.axhline(v_un, color='0.6', ls='--'); plt.plot([RL_k], [v_ld], 'ro'); plt.xlabel('load resistance (kOhm)'); plt.ylabel('V_out (V)'); plt.show()
    print(f'unloaded {v_un:.3f} V    with load {v_ld:.3f} V    ({100 * (1 - v_ld / v_un):.1f} % lower)')

explore(divider, Vin=(1, 12, 0.5, 10), R1_k=(0.5, 50, 0.5, 10), R2_k=(0.5, 50, 0.5, 10), RL_k=(0.5, 1000, 0.5, 10))
''')
B.md(r'''
**Try it in the simulator.** 9 V across 2 kΩ and 1 kΩ; the probe sits at $V_{out}$. **Predict**, then close the switch to add a 1 kΩ load. Click a resistor to see its voltage and current in the scope.
''')
B.code(r'''
lab('voltaic', height=640, preset='divider')
''')
B.ask(r'''A divider has $V_{in}=12$ V, $R_1=3\ \text{k}\Omega$, $R_2=1\ \text{k}\Omega$. What is $V_{out}$ (V), unloaded?''', 'num', 3,
      r'''$12\cdot\frac{1}{4}=3$ V.''', r'''$V_{out}=V_{in}\frac{R_2}{R_1+R_2}$.''', fmt='volts')
B.ask(r'''A battery with EMF 1.5 V and internal resistance 0.5 Ω drives a 2.5 Ω lamp. What is the terminal voltage (V)?''', 'num', 1.25,
      r'''$I=\frac{1.5}{3}=0.5$ A; $V=1.5-0.5\cdot0.5=1.25$ V (or $0.5\cdot2.5$).''', r'''$I=\frac{\mathcal E}{R+r}$, then $V=\mathcal E-Ir$.''', fmt='volts')

# =====================================================================================
B.md(r'''
---
# Part 4 — Kirchhoff's laws

**Why.** Not every circuit reduces to series and parallel pieces — two batteries in different branches already break the method. Kirchhoff's two laws always work. They are nothing but the two conservation laws you already used.

## 4.1 The two laws

**Current law (KCL) — conservation of charge.** At any junction (node), the total current flowing in equals the total flowing out:
$$\sum I_{\text{in}}=\sum I_{\text{out}} .$$

**Voltage law (KVL) — conservation of energy.** Around any closed loop, the voltages add up to zero: a coulomb that goes round and comes back to its start has gained and lost the same energy.
$$\sum_{\text{loop}}\Delta V=0 .$$
**Sign rules** when walking round a loop: through a battery from $-$ to $+$: $+\mathcal E$; through a resistor **in** the direction of its assumed current: $-IR$ (going "downhill").

## 4.2 A circuit with two sources
''')
B.fig('two_loop', F.two_loop, 'Two batteries, three resistors. Not series, not parallel — Kirchhoff.')
B.md(r'''
**Method A — node voltage (usually the quickest).**
1. Choose ground: the bottom wire, 0 V. Then the battery tops are at 9 V and 5 V.
2. One unknown: the voltage $V_A$ at node $A$.
3. Currents from Ohm (assumed directions as drawn — towards $A$ through $R_1$ and $R_2$, down through $R_3$):
$$I_1=\frac{9-V_A}{1000},\qquad I_2=\frac{5-V_A}{1000},\qquad I_3=\frac{V_A}{2000}.$$
4. KCL at $A$: $I_1+I_2=I_3$:
$$\frac{9-V_A}{1}+\frac{5-V_A}{1}=\frac{V_A}{2}\quad(\text{multiply by }1000)\quad\Rightarrow\quad14=2.5\,V_A\quad\Rightarrow\quad V_A=5.6\text{ V}.$$
5. Back-substitute: $I_1=3.4$ mA, $I_2=-0.6$ mA, $I_3=2.8$ mA. Check KCL: $3.4-0.6=2.8$ ✓.

**Reading the minus sign.** $I_2$ came out negative: the current really flows the *other* way — **into** the 5 V battery's $+$ terminal. The 9 V battery is charging the 5 V one. You do not need to guess directions right; the algebra corrects you.

**Method B — loop equations (mesh currents).** Let $J_1$ circulate clockwise in the left loop and $J_2$ clockwise in the right loop; $R_3$ is shared and carries $J_1-J_2$ downwards. Careful bookkeeping is the whole difficulty, so walk each loop clockwise from its bottom-left corner:

- **Left loop:** up through the 9 V battery ($-$ to $+$: $+9$), right through $R_1$ with $J_1$ ($-1000J_1$), down through $R_3$ with its current $J_1-J_2$ ($-2000(J_1-J_2)$):
$$9-1000J_1-2000(J_1-J_2)=0 .$$
- **Right loop:** up through $R_3$ — *against* its downward current $J_1-J_2$, so uphill: $+2000(J_1-J_2)$; right through $R_2$ with $J_2$ ($-1000J_2$); down through the 5 V battery from $+$ to $-$ ($-5$):
$$2000(J_1-J_2)-1000J_2-5=0 .$$
Tidied up, two linear equations in two unknowns:
$$\begin{aligned}3000J_1-2000J_2&=9\\2000J_1-3000J_2&=5\end{aligned}$$
Solution: $J_1=3.4$ mA, $J_2=0.6$ mA; so $I_1=J_1=3.4$ mA, $I_3=J_1-J_2=2.8$ mA, and the current in $R_2$ is $J_2=0.6$ mA flowing right — into the 5 V battery. Same answer ✓.

## 4.3 A circuit is a linear system

Any resistor circuit gives a set of linear equations $A\,\vec x=\vec b$. A computer solves them by Gaussian elimination — Unit 7 — and that is exactly what Voltaic does many thousands of times per second.
''')
B.code(r'''
A = np.array([[3000, -2000],
              [2000, -3000]], dtype=float)
b = np.array([9, 5], dtype=float)
J1, J2 = np.linalg.solve(A, b)
print(f'J1 = {J1 * 1000:.2f} mA,  J2 = {J2 * 1000:.2f} mA,  I3 = J1 - J2 = {(J1 - J2) * 1000:.2f} mA,  V_A = {(J1 - J2) * 2000:.2f} V')
''')
B.md(r'''
### Code it — node voltage for any two sources
Complete the formula for $V_A$ from KCL at node $A$, for general $V_1$, $V_2$, $R_1$, $R_2$, $R_3$. (Write out $\frac{V_1-V_A}{R_1}+\frac{V_2-V_A}{R_2}=\frac{V_A}{R_3}$ and solve for $V_A$ on paper first.)
''')
B.code(r'''
def node_voltage(V1, V2, R1, R2, R3):
    VA = ...            # solve the KCL equation for VA
    return VA


# ---------- tests: do not change ----------
cases = [((9, 5, 1000, 1000, 2000), 5.6), ((12, 0, 1000, 1000, 1000), 4.0), ((10, 10, 470, 220, 1e9), 10.0)]
for args, want in cases:
    try:
        got = node_voltage(*args); ok = abs(got - want) < 1e-4
    except Exception as err:
        got, ok = err, False
    print('✓' if ok else '✗', args, '->', got, '  expected', want)
''', ref=r'''
def node_voltage(V1, V2, R1, R2, R3):
    return (V1 / R1 + V2 / R2) / (1 / R1 + 1 / R2 + 1 / R3)
for args, want in [((9, 5, 1000, 1000, 2000), 5.6), ((12, 0, 1000, 1000, 1000), 4.0), ((10, 10, 470, 220, 1e9), 10.0)]:
    assert abs(node_voltage(*args) - want) < 1e-4
print('ok')
''')
B.md(r'''
*Read your formula:* $V_A=\dfrac{V_1/R_1+V_2/R_2}{1/R_1+1/R_2+1/R_3}$ — a weighted average of the source voltages (and 0 V for the path to ground), each weighted by how easily current flows from it. The second test case is a plain divider (12 V, $R_1$ to a 1 kΩ ∥ 1 kΩ $=$ 500 Ω): 4 V ✓.

### Experiment 2 — check it in the simulator
The circuit of the figure. **Predict** the probe reading at node $A$, then click $R_2$: which way does its current flow? Change the 5 V source to 8 V — **predict** first whether the 5 V branch now delivers current.
''')
B.code(r'''
lab('voltaic', height=640, preset='kirchhoff')
''')
B.ask(r'''Three wires meet at a node. 2.0 A flows in along the first, 0.5 A flows out along the second. What current (A) flows **out** along the third?''', 'num', 1.5,
      r'''In $=$ out: $2.0=0.5+I$, $I=1.5$ A.''', r'''KCL.''', fmt='amperes')
B.ask(r'''In the two-source circuit, the 5 V battery is replaced by an 8 V battery. What is $V_A$ (V) now?''', 'num', (9 + 8) / 2.5,
      r'''KCL: $(9-V_A)+(8-V_A)=\frac{V_A}{2}$, so $17=2.5V_A$, $V_A=6.8$ V. Now $8>6.8$: both batteries deliver current.''',
      r'''Repeat the node equation with 8 instead of 5.''', fmt='volts')

B.md(r'''
## Summary — everything on one page

- $I=\frac{dQ}{dt}$ (A $=$ C/s); $V=\frac{\Delta E}{Q}$ (V $=$ J/C); $P=VI$; energy $=Pt$ (1 kWh $=3.6$ MJ).
- **Ohm:** $V=IR$; $R=\rho\frac LA$; $P=I^2R=\frac{V^2}{R}$.
- **Series:** same $I$, voltages add, $R_1+R_2$. **Parallel:** same $V$, currents add, $\frac{R_1R_2}{R_1+R_2}$.
- **Divider:** $V_{out}=V_{in}\frac{R_2}{R_1+R_2}$; a load in parallel with $R_2$ lowers it — keep $R_L\gg R_2$.
- **Real source:** $V=\mathcal E-Ir$.
- **KCL** (charge): in $=$ out at a node. **KVL** (energy): voltages round a loop sum to 0. Node method: one unknown per node. A negative current flows the other way.
- A resistor circuit is a linear system $A\vec x=\vec b$.
''')

# =====================================================================================
B.md(r'''
---
# Problems

Paper first, with a labelled circuit diagram. First attempt counts.

### Charge, current, voltage, power
''')
B.problem(S1, r'A lamp draws 2.0 A for 5.0 minutes. How much charge (C) passes through it?', 'num', 600,
          [r'$Q=It$, $t$ in seconds.'],
          r'''$2.0\cdot300=$ **600 C**.''', fmt='coulombs')
B.problem(S1, r'How many electrons per second pass a point in a wire carrying 1.0 mA?', 'num', 1e-3 / qe,
          [r'Each electron carries $1.602\times10^{-19}$ C.'],
          r'''$\frac{10^{-3}}{1.602\times10^{-19}}=$ **$6.24\times10^{15}$** per second.''', fmt='a number; you can type `6.24e15`')
B.problem(S1, r'A 60 W lamp runs on 230 V. What current (A) does it draw?', 'num', 60 / 230,
          [r'$P=VI$.'],
          r'''$I=\frac{60}{230}=$ **0.261 A**.''', fmt='amperes')
B.problem(S1, r'A 2.0 kW heater runs 3 hours a day for 30 days. Electricity costs €0.30 per kWh. What does it cost (€)?', 'num', 54,
          [r'Energy in kWh $=$ kW × hours.'],
          r'''$2.0\cdot3\cdot30=180$ kWh; $180\cdot0.30=$ **€54**.''', fmt='euros')
B.md(r'''
### Ohm, series and parallel
''')
B.problem(S2, r'A copper wire is 10 m long with a cross-section of 1.0 mm². $\rho=1.7\times10^{-8}\ \Omega\,$m. What is its resistance (Ω)?', 'num', 1.7e-8 * 10 / 1e-6,
          [r'$1\ \text{mm}^2=10^{-6}\ \text{m}^2$.', r'$R=\rho L/A$.'],
          r'''$R=\frac{1.7\times10^{-8}\cdot10}{10^{-6}}=$ **0.17 Ω**.''', fmt='ohms')
B.problem(S2, r'What is the total resistance (Ω) of a 6 Ω resistor in series with a parallel pair of 12 Ω and 4 Ω?', 'num', 9,
          [r'Parallel pair first: product over sum.'],
          r'''$12\parallel4=\frac{48}{16}=3\ \Omega$; total $6+3=$ **9 Ω**.''', fmt='ohms')
B.problem(S2, r'That network (6 Ω + (12 Ω ∥ 4 Ω)) is connected to 18 V. What current (A) flows through the 12 Ω resistor?', 'num', 0.5,
          [r'Battery current: $18/9$.', r'Voltage across the parallel pair: battery current × 3 Ω.'],
          r'''$I=\frac{18}{9}=2$ A; voltage across the pair $2\cdot3=6$ V; through 12 Ω: $\frac{6}{12}=$ **0.5 A** (and 1.5 A through 4 Ω; $0.5+1.5=2$ ✓).''', fmt='amperes')
B.problem(S2, r'A 220 Ω resistor has 9.0 V across it. What power (W) does it dissipate? (Then decide: is a ¼ W resistor enough?)', 'num', 81 / 220,
          [r'$P=V^2/R$.'],
          r'''$P=\frac{81}{220}=$ **0.368 W** — more than ¼ W: it would overheat. Use a ½ W resistor.''', fmt='watts')
B.md(r'''
### Dividers and real sources
''')
B.problem(S3, r'A divider has $V_{in}=9.0$ V, $R_1=6.8\ \text{k}\Omega$, $R_2=3.3\ \text{k}\Omega$. What is $V_{out}$ (V), unloaded?', 'num', 9 * 3.3 / 10.1,
          [r'$V_{out}=V_{in}\frac{R_2}{R_1+R_2}$.'],
          r'''$9\cdot\frac{3.3}{10.1}=$ **2.94 V**.''', fmt='volts')
B.problem(S3, r'The same divider is now loaded with $R_L=3.3\ \text{k}\Omega$ across $R_2$. What is $V_{out}$ (V)?', 'num', 9 * 1.65 / (6.8 + 1.65),
          [r'Replace $R_2$ by $R_2\parallel R_L$.'],
          r'''$R_2\parallel R_L=1.65\ \text{k}\Omega$; $V_{out}=9\cdot\frac{1.65}{8.45}=$ **1.76 V** — 40 % lower than unloaded.''', fmt='volts')
B.problem(S3, r'You need 5.0 V from 12 V with $R_1=7.0\ \text{k}\Omega$. What $R_2$ (in kΩ) do you need?', 'num', 5,
          [r'$5=12\frac{R_2}{7+R_2}$; solve for $R_2$.'],
          r'''$5(7+R_2)=12R_2\Rightarrow35=7R_2\Rightarrow R_2=$ **5.0 kΩ**.''', fmt='kΩ')
B.problem(S3, r'A 9.0 V battery with 2.0 Ω internal resistance drives a 16 Ω load. What is the terminal voltage (V)?', 'num', 8,
          [r'$I=\frac{\mathcal E}{R+r}$.'],
          r'''$I=\frac{9}{18}=0.5$ A; $V=9-0.5\cdot2=$ **8.0 V**.''', fmt='volts')
B.md(r'''
### Kirchhoff
''')
B.problem(S4, r'At a node, 3.0 A and 2.0 A flow in; 4.0 A flows out along one wire. What current (A) flows out along the remaining wire?', 'num', 1,
          [r'KCL: in $=$ out.'],
          r'''$3+2=4+I\Rightarrow I=$ **1.0 A**.''', fmt='amperes')
B.problem(S4, r'A single loop contains a 12 V battery and a 3.0 V battery connected so that they **oppose** each other, plus resistors totalling 450 Ω. What current (mA) flows?', 'num', 20,
          [r'KVL round the loop: $12-3-450I=0$.'],
          r'''Opposing EMFs subtract: $I=\frac{12-3}{450}=0.020$ A $=$ **20 mA**.''', fmt='mA')
B.problem(S4, r'In the two-source circuit of the figure, replace $R_3$ by a 1.0 kΩ resistor (the others unchanged: 9 V, 5 V, $R_1=R_2=1$ kΩ). What is $V_A$ (V)?', 'num', 14 / 3,
          [r'KCL at $A$: $(9-V_A)+(5-V_A)=V_A$ (all in kΩ, so the 1000s cancel).'],
          r'''$14=3V_A\Rightarrow V_A=$ **4.67 V**.''', fmt='volts')
B.problem(S4, r'In that modified circuit ($R_3=1$ kΩ), what is the current $I_2$ (in mA) in the direction drawn — from the 5 V battery towards node $A$?', 'num', (5 - 14 / 3),
          [r'$I_2=\frac{5-V_A}{1\ \text{k}\Omega}$.'],
          r'''$I_2=\frac{5-4.667}{1000}=+0.33$ mA — **0.33 mA**, now positive: with a smaller $R_3$ the node voltage drops below 5 V, and the 5 V battery delivers current.''', fmt='mA (with sign)')
B.problem(S4, r'Solve with loop currents (clockwise $J_1$ left, $J_2$ right) the circuit: left loop 10 V and 2 kΩ, shared middle resistor 1 kΩ, right loop 1 kΩ and no battery. Give $J_1$ in mA.', 'num', 10 / (2 + 0.5) * 1,
          [r'Left: $10-2000J_1-1000(J_1-J_2)=0$. Right: $1000(J_1-J_2)-1000J_2=0$.', r'The right equation gives $J_2=J_1/2$.'],
          r'''Right loop: $J_1-J_2=J_2\Rightarrow J_2=\frac{J_1}{2}$. Left: $10=3000J_1-1000\cdot\frac{J_1}{2}=2500J_1\Rightarrow J_1=$ **4.0 mA**.

Check by reduction: $1\,\text{k}\parallel1\,\text{k}=500\ \Omega$, total $2.5$ kΩ, $\frac{10}{2500}=4$ mA ✓.''', fmt='mA')
B.code(r'''
# scratch cell
''')

B.md(r'''
---
# Finish

### 1 · Report
''')
B.code(r'''
report()
''')
B.md(r'''
### 2 · Teach-back (20 minutes, from memory)
1. Why is $P=VI$? Explain with the units.
2. Derive the series and parallel rules from conservation of charge and energy.
3. Derive the voltage-divider formula. What does a load do to it, and why?
4. State Kirchhoff's two laws and say which conservation law each one is.
5. In the two-source circuit, what does a negative current mean?

*Your answers:*

&nbsp;

### 3 · What comes next
Term 2 builds on this directly: the RC circuit (Unit 5, week 14) is Kirchhoff's voltage law plus a capacitor; Unit 7 turns "a circuit is a linear system" into Gaussian elimination; Unit 11 replaces resistance by impedance for AC.
''')

if __name__ == '__main__':
    B.write()
