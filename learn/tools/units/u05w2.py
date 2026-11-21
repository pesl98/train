"""Unit 5 · Week 2 (course week 14) - Linear first-order equations, RC/RL circuits, sinusoidal response."""
import math
from nbkit import Book
import figs_u05 as F

B = Book('u05w2', 'Unit 5 · Week 2 — Linear equations and circuits', 'year1/u05w2-linear-first-order.ipynb')
S1, S2, S3, S4 = '1 Integrating factor', '2 RC and RL circuits', '3 Sinusoidal input', '4 Mixing and superposition'

B.md(r'''
# Unit 5 · Week 2 — Linear equations and circuits
*Term 2, week 14 · about 15 hours in this notebook and on paper*

**Where you are.** Last week: separable equations, and the cooling law $T'=-k(T-T_a)$. But what if the room temperature *changes* — say it follows the day–night cycle? Then the equation $T'=-k(T-T_a(t))$ is no longer separable. This week gives one method that solves every equation of the form
$$y'+p(t)\,y=q(t)$$
— the **linear first-order equation**. It covers the most important circuit of electronics, the RC circuit, including what it does to a sine wave: it is a filter.

**What you will be able to do at the end of this week**
1. Derive the integrating-factor method from the product rule and use it.
2. Split a solution into transient and steady state, and read the time constant.
3. Model RC and RL circuits from Kirchhoff's law, and predict charging curves (63 % after one τ, settled after 5τ).
4. Find the steady-state response to a sine wave — amplitude and phase lag — and explain why an RC circuit is a low-pass filter.
5. Solve mixing problems and use superposition.

**What is used from earlier:** the product rule (Unit 2), integration incl. by parts (Unit 3), $a\sin x+b\cos x=R\sin(x+\varphi)$ (Unit 1 week 2), last week's separable equations.

Run the grey *SETUP* cell first.
''')

# =====================================================================================
B.md(r'''
---
# Part 1 — The integrating factor

## 1.1 The idea: make the left side a product rule

**Build.** Take $y'+p(t)\,y=q(t)$.

**Step 1 — look at the product rule.** For any function $\mu(t)$:
$$\frac{d}{dt}\big(\mu\,y\big)=\mu\,y'+\mu'\,y .$$
Compare with $\mu$ times the left side of our equation: $\mu\,y'+\mu\,p\,y$. The two are **equal** if $\mu'=\mu\,p$.

**Step 2 — find such a $\mu$.** $\mu'=p\,\mu$ is separable (last week): $\frac{d\mu}{\mu}=p\,dt$, so $\ln\mu=\int p\,dt$ and
$$\boxed{\,\mu(t)=e^{\int p(t)\,dt}\,}\qquad\text{the integrating factor}$$
(any antiderivative will do — no constant needed).

**Step 3 — multiply the equation by $\mu$.** The left side becomes a single derivative:
$$\frac{d}{dt}\big(\mu\,y\big)=\mu\,q .$$

**Step 4 — integrate both sides** and divide by $\mu$:
$$\mu\,y=\int\mu\,q\,dt+C\qquad\Rightarrow\qquad y=\frac{1}{\mu}\left(\int\mu\,q\,dt+C\right).$$

**The procedure.**
1. Write the equation in the standard form $y'+p\,y=q$ (coefficient of $y'$ equal to 1).
2. $\mu=e^{\int p\,dt}$.
3. $(\mu y)'=\mu q$ — integrate.
4. Divide by $\mu$; apply the initial value.

**Worked example 1.** $y'+2y=6$, $y(0)=0$.
1. $p=2$, $q=6$. 2. $\mu=e^{2t}$. 3. $(e^{2t}y)'=6e^{2t}\Rightarrow e^{2t}y=3e^{2t}+C$.
4. $y=3+Ce^{-2t}$; $y(0)=0\Rightarrow C=-3$: $\;y=3\left(1-e^{-2t}\right)$.

**Worked example 2.** $y'+\dfrac{y}{t}=t^2$ ($t>0$), $y(1)=1$.
1. $p=\frac1t$. 2. $\mu=e^{\ln t}=t$. 3. $(ty)'=t^3\Rightarrow ty=\frac{t^4}{4}+C$. 4. $y=\frac{t^3}{4}+\frac Ct$; $y(1)=1\Rightarrow C=\frac34$.

**Worked example 3.** $y'-y=t$, $y(0)=0$. $\mu=e^{-t}$; $(e^{-t}y)'=te^{-t}$. By parts, $\int te^{-t}dt=-(t+1)e^{-t}$. So $e^{-t}y=-(t+1)e^{-t}+C$, $y=-(t+1)+Ce^t$; $C=1$: $y=e^t-t-1$.
''')
B.code(r'''
# Check worked example 3: y = e^t - t - 1 should satisfy y' = y + t
compare(lambda v: exp(v) - v - 1, lambda v: (exp(v) - v - 1) + v, lo=-2, hi=2)
''')
B.ask(r'''For $y'+3y=e^{t}$, what is the integrating factor $\mu(t)$? Give $\mu(1)$.''', 'num', math.exp(3),
      r'''$\mu=e^{\int3\,dt}=e^{3t}$; $\mu(1)=e^3\approx20.09$.''',
      r'''$\mu=e^{\int p\,dt}$ with $p=3$.''', fmt='a number; you can type `exp(3)`')

B.md(r'''
## 1.2 Constant coefficients: transient and steady state

**Build.** The most common case in engineering: $y'+a\,y=b$ with constants $a>0$, $b$. With $\mu=e^{at}$:
$$y(t)=\underbrace{\frac ba}_{\text{steady state}}+\underbrace{\left(y_0-\frac ba\right)e^{-at}}_{\text{transient}} .$$

- The **steady state** $\frac ba$ is where $y'=0$ — the equilibrium of last week.
- The **transient** dies away exponentially, whatever the start.
- The **time constant** $\tau=\frac1a$ sets the speed: after one $\tau$ the transient has fallen to $e^{-1}\approx37\%$, after $5\tau$ to $e^{-5}\approx0.7\%$ ("settled").

This one formula is the cooling coffee, the terminal velocity, and — next — the capacitor.
''')
B.ask(r'''$y'+0.5y=4$. What is the steady-state value?''', 'num', 8,
      r'''Set $y'=0$: $0.5y=4$, $y=8$. (And $\tau=\frac1{0.5}=2$.)''',
      r'''At steady state $y'=0$.''')

# =====================================================================================
B.md(r'''
---
# Part 2 — RC and RL circuits

## 2.1 The RC circuit from first principles
''')
B.fig('rc_circuit', F.rc_circuit, 'A source, a resistor and a capacitor in series.')
B.md(r'''
**Build.** Three facts.
1. **Kirchhoff's voltage law:** around a loop the voltages add up: $V_s=v_R+v$.
2. **Ohm's law:** $v_R=R\,i$.
3. **The capacitor:** its charge is $q=Cv$, and current is the rate of flow of charge, $i=\frac{dq}{dt}=C\frac{dv}{dt}$.

Substitute 2 and 3 into 1:
$$V_s=RC\,\frac{dv}{dt}+v\qquad\Longleftrightarrow\qquad \frac{dv}{dt}+\frac{1}{RC}\,v=\frac{V_s}{RC}.$$
A linear first-order equation with $a=\frac1{RC}$. So the **time constant** is
$$\boxed{\,\tau=RC\,}$$
(check the units: ohms × farads = $\frac{\text{V}}{\text{A}}\cdot\frac{\text{C}}{\text{V}}=\frac{\text{C}}{\text{A}}=$ seconds ✓).

**Charging** from $v(0)=0$ with constant $V_s$: steady state $V_s$, so
$$v(t)=V_s\left(1-e^{-t/RC}\right),\qquad i(t)=C\frac{dv}{dt}=\frac{V_s}{R}e^{-t/RC}.$$
**Discharging** ($V_s=0$, start at $V_0$): $v(t)=V_0e^{-t/RC}$.
''')
B.fig('rc_charge', F.rc_charge, 'After one time constant: 63 % charged (or 37 % left). After five: practically done.')
B.md(r'''
**Reading it.** At the switch-on moment the capacitor voltage is 0, so the whole supply sits across the resistor: the current starts at its maximum $\frac{V_s}{R}$. As the capacitor fills, its voltage opposes the source, the current falls, and charging slows — rate proportional to "what is left", exactly as for cooling.

**Worked example.** $R=10\ \text{k}\Omega$, $C=100\ \mu\text{F}$, $V_s=5$ V. $\tau=10^4\cdot10^{-4}=1$ s. After 1 s: $5(1-e^{-1})=3.16$ V. After 5 s: $4.97$ V. Initial current $\frac{5}{10^4}=0.5$ mA.

**Energy check (Unit 3).** The capacitor ends with $\frac12CV_s^2$. The source delivered $\int V_s\,i\,dt=V_s\cdot CV_s=CV_s^2$ (all the charge $CV_s$ passed through it at voltage $V_s$). Where is the other half? Burnt in the resistor: $\int R\,i^2\,dt=R\frac{V_s^2}{R^2}\int_0^\infty e^{-2t/RC}dt=\frac{V_s^2}{R}\cdot\frac{RC}{2}=\frac12CV_s^2$ ✓ — exactly half, *whatever* the value of $R$.

## 2.2 The RL circuit

An inductor opposes changes of current: its voltage is $v_L=L\frac{di}{dt}$. With a resistor: $V_s=Ri+L\frac{di}{dt}$, i.e.
$$\frac{di}{dt}+\frac RL\,i=\frac{V_s}{L},\qquad\tau=\frac LR,\qquad i(t)=\frac{V_s}{R}\left(1-e^{-Rt/L}\right).$$
The same curve, now for the current. (Switching off an inductor abruptly forces $\frac{di}{dt}$ to be enormous — the voltage spike that destroys transistors unless a diode is placed across relay coils.)

### Experiment 1 — the charging curve
**Predict first:** doubling $R$ — what happens to $\tau$, to the initial current, to the final voltage?
''')
B.code(r'''
def rc(R_kohm=10.0, C_uF=100.0, Vs=5.0):
    R, C = R_kohm * 1e3, C_uF * 1e-6
    tau = R * C
    ts = np.linspace(0, 6 * tau, 400)
    v = Vs * (1 - np.exp(-ts / tau)); i = Vs / R * np.exp(-ts / tau)
    fig, (a1, a2) = plt.subplots(1, 2, figsize=(10.5, 3.4))
    a1.plot(ts, v); a1.axhline(Vs, color='0.6', ls='--'); a1.axvline(tau, color='r', ls=':'); a1.set_xlabel('t (s)'); a1.set_ylabel('capacitor voltage (V)')
    a2.plot(ts, i * 1000, 'C1'); a2.axvline(tau, color='r', ls=':'); a2.set_xlabel('t (s)'); a2.set_ylabel('current (mA)')
    plt.show()
    print(f'tau = RC = {tau:.3g} s     v(tau) = {Vs * (1 - exp(-1)):.3f} V (63 %)     initial current {Vs / R * 1000:.3g} mA')

explore(rc, R_kohm=(1, 50, 1, 10), C_uF=(10, 500, 10, 100), Vs=(1, 12, 1, 5))
''')
B.ask(r'''$R=2\ \text{k}\Omega$, $C=50\ \mu\text{F}$. What is the time constant in milliseconds?''', 'num', 100,
      r'''$\tau=RC=2000\cdot50\times10^{-6}=0.1$ s $=100$ ms.''',
      r'''$\tau=RC$ in seconds, then convert.''', fmt='milliseconds')
B.ask(r'''A capacitor discharges through a resistor. What percentage of the starting voltage is left after $2\tau$?''', 'num', 100 * math.exp(-2),
      r'''$e^{-2}\approx0.135$: 13.5 %.''',
      r'''$v=V_0e^{-t/\tau}$ with $t=2\tau$.''', fmt='a number (percent)')

# =====================================================================================
B.md(r'''
---
# Part 3 — A sine wave in: the first filter

## 3.1 The equation

**Why.** Audio signals, sensor noise and radio waves are mixtures of sine waves of different frequencies. What does the RC circuit do to one sine wave? The answer explains tone controls, anti-aliasing filters, and why a scope probe has limited bandwidth.

**Build.** Input $V_s(t)=V\sin\omega t$. The equation, with $\tau=RC$:
$$\tau\,v'+v=V\sin\omega t .$$

**Step 1 — guess the form of the steady state.** A sine in, and the equation only adds derivatives (which turn $\sin$ into $\cos$ and back): so try
$$v_{ss}(t)=A\sin\omega t+B\cos\omega t .$$

**Step 2 — substitute** ($v_{ss}'=A\omega\cos\omega t-B\omega\sin\omega t$):
$$\tau\left(A\omega\cos\omega t-B\omega\sin\omega t\right)+A\sin\omega t+B\cos\omega t=V\sin\omega t .$$

**Step 3 — match** the $\sin$ and $\cos$ parts on both sides:
$$\sin:\ A-\omega\tau B=V\qquad\cos:\ \omega\tau A+B=0 .$$
From the second, $B=-\omega\tau A$; then $A(1+\omega^2\tau^2)=V$:
$$A=\frac{V}{1+\omega^2\tau^2},\qquad B=-\frac{\omega\tau V}{1+\omega^2\tau^2}.$$

**Step 4 — combine into one sinusoid** (Unit 1 week 2: $A\sin x+B\cos x=R\sin(x+\varphi)$ with $R=\sqrt{A^2+B^2}$):
$$\boxed{\,v_{ss}(t)=\frac{V}{\sqrt{1+\omega^2\tau^2}}\,\sin\!\big(\omega t-\varphi\big),\qquad\varphi=\arctan(\omega\tau)\,}$$

The full solution is this steady state **plus** a transient $Ce^{-t/\tau}$ that dies out — exactly the "transient + steady state" picture of the driven oscillator in the Physics Lab.

## 3.2 Reading the result: a low-pass filter
''')
B.fig('lowpass', F.lowpass, 'Slow input (left): passes almost unchanged. Fast input (right): small and lagging.')
B.md(r'''
| $\omega\tau$ | gain $\frac{1}{\sqrt{1+\omega^2\tau^2}}$ | lag $\arctan\omega\tau$ |
|---|---|---|
| $0.1$ (slow) | $0.995$ | $6^\circ$ |
| $1$ | $0.707$ | $45^\circ$ |
| $10$ (fast) | $0.0995$ | $84^\circ$ |

- **Low frequencies pass** almost unchanged; **high frequencies are suppressed** (gain $\approx\frac{1}{\omega\tau}$): a **low-pass filter**.
- The **cut-off frequency** is where $\omega\tau=1$: $\;\omega_c=\frac{1}{RC}$, $\;f_c=\frac{1}{2\pi RC}$. There the gain is $\frac{1}{\sqrt2}$ (half the power — the RMS idea of Unit 3).
- *Why physically:* the capacitor needs time $\sim\tau$ to charge; a fast wave reverses before it gets anywhere.

Unit 11 redoes this in one line with complex numbers ($e^{i\omega t}$, Unit 4's Euler formula). The result will be the same.

### Experiment 2 — filter a signal
The input is a slow sine plus fast "noise". The cell solves the ODE numerically.

**Predict first:** with $f_c=5$ Hz, what happens to a 1 Hz signal and to 50 Hz noise?
''')
B.code(r'''
def filt(fc=5.0):
    tau = 1 / (2 * pi * fc)
    ts = np.linspace(0, 2, 8000); dt = ts[1] - ts[0]
    vin = np.sin(2 * pi * 1 * ts) + 0.4 * np.sin(2 * pi * 50 * ts)       # 1 Hz signal + 50 Hz hum
    v = np.zeros_like(ts)
    for k in range(len(ts) - 1):                                        # tau v' + v = vin  (small Euler steps - week 15)
        v[k + 1] = v[k] + dt / tau * (vin[k] - v[k])
    plt.figure(figsize=(9, 3.4)); plt.plot(ts, vin, color='0.6', lw=1, label='input'); plt.plot(ts, v, lw=2, label='capacitor voltage')
    plt.legend(loc='upper right'); plt.xlabel('t (s)'); plt.show()
    for f in (1, 50):
        print(f'{f:3d} Hz: gain {1 / sqrt(1 + (f / fc)**2):.3f}, lag {degrees(atan(f / fc)):.0f} degrees')

explore(filt, fc=(1, 40, 1, 5))
''')
B.ask(r'''An RC filter has $R=1\ \text{k}\Omega$, $C=1\ \mu\text{F}$. What is its cut-off frequency $f_c$ in Hz?''', 'num', 1 / (2 * math.pi * 1e-3),
      r'''$f_c=\frac{1}{2\pi RC}=\frac{1}{2\pi\cdot10^{-3}}\approx159$ Hz.''',
      r'''$f_c=\frac{1}{2\pi RC}$, with $RC=10^{-3}$ s.''', fmt='Hz')
B.ask(r'''At $\omega\tau=1$, by how many degrees does the capacitor voltage lag the input?''', 'num', 45,
      r'''$\arctan1=45^\circ$.''',
      r'''$\varphi=\arctan(\omega\tau)$.''', fmt='degrees')

# =====================================================================================
B.md(r'''
---
# Part 4 — Mixing problems and superposition

## 4.1 Mixing
''')
B.fig('tank', F.tank, 'Salt water flows in; the mixture flows out at the same rate.')
B.md(r'''
**Build.** Let $S(t)$ be the grams of salt in the tank. *Rate of change = rate in − rate out.*
- In: $3\ \tfrac{\text{L}}{\text{min}}\times2\ \tfrac{\text{g}}{\text{L}}=6$ g/min.
- Out: the concentration in the tank is $\frac{S}{100}$ g/L, leaving at 3 L/min: $\frac{3S}{100}$ g/min.
$$\frac{dS}{dt}=6-0.03\,S\qquad\Rightarrow\qquad S(t)=200+(S_0-200)e^{-0.03t}.$$
Steady state 200 g (the tank ends at the inflow concentration, 2 g/L × 100 L); time constant $\frac{100}{3}\approx33$ min. Same equation as the capacitor — different units.

## 4.2 Superposition

**Build.** For a **linear** equation, responses to separate inputs **add**. If $y_1$ solves $y'+py=q_1$ and $y_2$ solves $y'+py=q_2$, then $y_1+y_2$ solves $y'+py=q_1+q_2$ (just add the two equations). So:
- the response to "signal + noise" is the response to the signal plus the response to the noise — that is why Experiment 2 could be analysed one frequency at a time;
- any solution = (one particular solution) + (the general solution of $y'+py=0$, i.e. $Ce^{-\int p}$).

Superposition is the reason linear systems are so much easier than non-linear ones (like the logistic equation), and the foundation of Fourier analysis (Unit 12). **It fails for non-linear equations** — doubling the input of $y'=y^2+q$ does not double the response.

**Drug dosing — a worked example.** A drug is infused at 2 mg/h and removed at a rate $0.25\,c$ ($c$ in mg): $c'=2-0.25c$. Steady level $\frac{2}{0.25}=8$ mg, reached (to 99 %) after $5\tau=20$ hours. Doubling the infusion rate doubles the steady level — linearity.
''')
B.ask(r'''A 50 L tank of pure water receives brine at 5 L/min with 4 g/L, and the mixture leaves at 5 L/min. What is the steady-state amount of salt (g)?''', 'num', 200,
      r'''At steady state the tank has the inflow concentration: $4\ \text{g/L}\times50\ \text{L}=200$ g. (From $S'=20-0.1S=0$.)''',
      r'''Rate in $=20$ g/min, rate out $=\frac{5S}{50}$. Set $S'=0$.''', fmt='grams')

B.md(r'''
## Week summary — everything on one page

- **Linear** $y'+p(t)y=q(t)$: $\mu=e^{\int p\,dt}$, then $(\mu y)'=\mu q$.
- **Constant coefficients** $y'+ay=b$: $y=\frac ba+(y_0-\frac ba)e^{-at}$; $\tau=\frac1a$; 37 % left after $\tau$, 0.7 % after $5\tau$.
- **RC**: $RC\,v'+v=V_s$, $\tau=RC$; $v=V_s(1-e^{-t/RC})$, $i=\frac{V_s}{R}e^{-t/RC}$; half the energy is lost in $R$.
- **RL**: $L\,i'+Ri=V_s$, $\tau=\frac LR$.
- **Sine input**: $v_{ss}=\dfrac{V}{\sqrt{1+\omega^2\tau^2}}\sin(\omega t-\arctan\omega\tau)$; low-pass, $f_c=\frac{1}{2\pi RC}$, gain $\frac1{\sqrt2}$ and lag $45^\circ$ there.
- **Mixing**: rate in − rate out. **Superposition** for linear equations.
''')

# =====================================================================================
B.md(r'''
---
# Problems

Paper first. First attempt counts. `hint(n)` → `solution(n)` → `mistake(n, '...')`.

### Integrating factor
''')
B.problem(S1, r'Solve $y\,^\prime+3y=9$, $y(0)=1$. Give $y(1)$.', 'num', 3 - 2 * math.exp(-3),
          [r'Steady state $3$; $y=3+Ce^{-3t}$.', r'$y(0)=1\Rightarrow C=-2$.'],
          r'''$y=3+Ce^{-3t}$, $y(0)=3+C=1\Rightarrow C=-2$. $y(1)=3-2e^{-3}\approx$ **2.900**.''', fmt='a number; you can type `3-2*exp(-3)`')
B.problem(S1, r'Solve $y\,^\prime+2ty=t$, $y(0)=0$. Give $y(1)$.', 'num', 0.5 * (1 - math.exp(-1)),
          [r'$\mu=e^{t^2}$.', r'$(e^{t^2}y)\,^\prime=te^{t^2}$; integrate with $u=t^2$.'],
          r'''$\mu=e^{\int2t\,dt}=e^{t^2}$. $(e^{t^2}y)'=te^{t^2}\Rightarrow e^{t^2}y=\frac12e^{t^2}+C$.

$y=\frac12+Ce^{-t^2}$, $y(0)=0\Rightarrow C=-\frac12$. $y(1)=\frac12(1-e^{-1})\approx$ **0.316**.''')
B.problem(S1, r'Solve $t\,y\,^\prime+2y=t^2$ for $t>0$ with $y(1)=0$. Give $y(2)$.', 'num', 1 - 1 / 16,
          [r'Standard form first: divide by $t$: $y\,^\prime+\frac2t y=t$.', r'$\mu=t^2$; $(t^2y)\,^\prime=t^3$.'],
          r'''Divide by $t$: $y'+\frac2ty=t$. $\mu=e^{2\ln t}=t^2$. $(t^2y)'=t^3\Rightarrow t^2y=\frac{t^4}{4}+C$, $y=\frac{t^2}{4}+\frac{C}{t^2}$.

$y(1)=\frac14+C=0\Rightarrow C=-\frac14$. $y(2)=1-\frac1{16}=$ **0.9375**.''')
B.problem(S1, r'Solve $y\,^\prime-y=e^{t}$, $y(0)=1$. Give $y(1)$.', 'num', 2 * math.e,
          [r'$\mu=e^{-t}$; then $(e^{-t}y)\,^\prime=1$.'],
          r'''$\mu=e^{-t}$: $(e^{-t}y)'=e^{-t}e^t=1\Rightarrow e^{-t}y=t+C$, $y=(t+C)e^t$. $y(0)=C=1$.

$y(1)=2e\approx$ **5.437**. (The input $e^t$ "resonates" with the natural solution $e^t$ — hence the factor $t$.)''', fmt='a number; you can type `2*e`')
B.md(r'''
### RC and RL circuits
''')
B.problem(S2, r'$R=4.7\ \text{k}\Omega$, $C=220\ \mu\text{F}$, charged from 0 by a 9 V supply. What is the capacitor voltage after 2 s?', 'num', 9 * (1 - math.exp(-2 / (4700 * 220e-6))),
          [r'$\tau=RC=1.034$ s.'],
          r'''$\tau=4700\cdot220\times10^{-6}=1.034$ s. $v(2)=9(1-e^{-2/1.034})=9(1-0.1445)\approx$ **7.70 V**.''', fmt='volts')
B.problem(S2, r'A 1000 µF capacitor at 12 V discharges through a resistor; after 3 s it is at 4.4 V. What is $R$ in ohms?', 'num', 3 / (1e-3 * math.log(12 / 4.4)),
          [r'$4.4=12e^{-3/\tau}$: solve for $\tau$, then $R=\tau/C$.'],
          r'''$e^{-3/\tau}=\frac{4.4}{12}\Rightarrow\tau=\frac{3}{\ln(12/4.4)}=\frac{3}{1.003}=2.99$ s. $R=\frac{\tau}{C}=\frac{2.99}{10^{-3}}\approx$ **2990 Ω** (about 3 kΩ).''', fmt='ohms')
B.problem(S2, r'In an RC charging circuit, how many time constants until the capacitor reaches 95 % of the supply voltage?', 'num', math.log(20),
          [r'$1-e^{-t/\tau}=0.95$.'],
          r'''$e^{-t/\tau}=0.05\Rightarrow\frac t\tau=\ln20\approx$ **3.0**.''')
B.problem(S2, r'An RL circuit: $L=0.5$ H, $R=10\ \Omega$, $V_s=12$ V, switched on at $t=0$. What is the current (A) after 50 ms?', 'num', 1.2 * (1 - math.exp(-1)),
          [r'$\tau=L/R=0.05$ s; final current $V_s/R$.'],
          r'''$\tau=\frac{0.5}{10}=0.05$ s, final current $1.2$ A. At $t=\tau$: $1.2(1-e^{-1})\approx$ **0.759 A**.''', fmt='amperes')
B.problem(S2, r'A 100 µF capacitor is charged to 10 V through a 1 kΩ resistor. How much energy (J) is dissipated in the resistor during the whole charge?', 'num', 0.5 * 100e-6 * 100,
          [r'It equals the energy finally stored in the capacitor.'],
          r'''Exactly as much as ends up in the capacitor: $\frac12CV^2=\frac12\cdot10^{-4}\cdot100=$ **0.005 J** — independent of $R$.''', fmt='joules')
B.md(r'''
### Sinusoidal input
''')
B.problem(S3, r'An RC low-pass filter has $\tau=1$ ms. What is the gain for a 1 kHz sine wave?', 'num', 1 / math.sqrt(1 + (2 * math.pi) ** 2),
          [r'$\omega=2\pi f=2000\pi$ rad/s, so $\omega\tau=2\pi$.'],
          r'''$\omega\tau=2\pi\cdot1000\cdot10^{-3}=2\pi\approx6.28$. Gain $\frac{1}{\sqrt{1+39.5}}\approx$ **0.157**.''')
B.problem(S3, r'Which $R$ (in ohms) with $C=10$ nF gives a cut-off frequency of 1 kHz?', 'num', 1 / (2 * math.pi * 1000 * 10e-9),
          [r'$f_c=\frac{1}{2\pi RC}$; solve for $R$.'],
          r'''$R=\frac{1}{2\pi f_cC}=\frac{1}{2\pi\cdot1000\cdot10^{-8}}\approx$ **15 900 Ω** (use a 16 kΩ resistor).''', fmt='ohms')
B.problem(S3, r'For $\tau v\,^\prime+v=V\sin\omega t$ at very high frequency, the gain behaves like $\frac{1}{\omega\tau}$. By what factor does the output amplitude fall when the frequency is multiplied by 10 (far above cut-off)?', 'num', 10,
          [r'Gain ∝ 1/ω.'],
          r'''Gain $\approx\frac{1}{\omega\tau}$: ten times the frequency, one tenth of the amplitude — a factor **10** (engineers say "−20 dB per decade").''')
B.md(r'''
### Mixing and superposition
''')
B.problem(S4, r'A 200 L tank holds 50 g of dye dissolved in water. Pure water flows in at 4 L/min and the mixture flows out at 4 L/min. How much dye (g) is left after 30 min?', 'num', 50 * math.exp(-0.6),
          [r'$S\,^\prime=-\frac{4}{200}S$.'],
          r'''$S'=-0.02S\Rightarrow S=50e^{-0.02t}$; $S(30)=50e^{-0.6}\approx$ **27.4 g**.''', fmt='grams')
B.problem(S4, r'If $y_1=3$ solves $y\,^\prime+y=3$ and $y_2=\sin t-\cos t$ solves $y\,^\prime+y=2\sin t$, which function solves $y\,^\prime+y=3+4\sin t$? Give its value at $t=0$.', 'num', 1,
          [r'Superposition: $y=y_1+2y_2$.'],
          r'''The input is $3+2\cdot(2\sin t)$, so $y=y_1+2y_2=3+2\sin t-2\cos t$. At $t=0$: $3-2=$ **1**.

Check: $y'=2\cos t+2\sin t$, $y'+y=3+4\sin t$ ✓.''')
B.code(r'''
# scratch cell
''')

B.md(r'''
---
# Finish the week

### 1 · Report
''')
B.code(r'''
report()
''')
B.md(r'''
### 2 · Teach-back (30 minutes, from memory)
1. Derive the integrating factor from the product rule.
2. Write down and solve the RC charging equation from Kirchhoff's law.
3. What does τ mean, and what fractions go with τ and 5τ?
4. Why is an RC circuit a low-pass filter? Give the cut-off frequency.
5. Why does half the energy end up as heat when charging a capacitor?

*Your answers:*

&nbsp;

### 3 · Lab strand — measure τ in the circuit simulator (1 hour)
The simulator opens with an RC circuit driven by a square wave (0 V ↔ 10 V, 2 Hz): $R=1\ \text{k}\Omega$, $C=100\ \mu\text{F}$.

**Predict first:** τ, the capacitor voltage 0.1 s after each rising edge, and whether the capacitor fully charges before the square wave switches back (each half-period lasts 0.25 s). Then read the oscilloscope. Change $C$ to 470 µF: **predict** the new shape before you look — it will no longer reach the top (the filter starts to smooth the square wave into a triangle-like wave: low-pass filtering in the time domain).
''')
B.code(r'''
lab('voltaic', height=680, preset='rc')
''')
B.md(r'''
### 4 · What comes next
**Week 15:** most differential equations cannot be solved with a formula. The labs nevertheless solve them, thousands of times per second. You will build those methods — Euler and Runge–Kutta — measure their errors, and see why a too-large step makes a simulation explode.
''')

if __name__ == '__main__':
    B.write()
