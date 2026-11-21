"""Unit 5 · Week 3 (course week 15) - Solving ODEs numerically: Euler, Heun, Runge-Kutta, error, stability, systems."""
import math
from nbkit import Book
import figs_u05 as F

B = Book('u05w3', 'Unit 5 · Week 3 — Solving differential equations numerically', 'year1/u05w3-numerical-odes.ipynb')
S1, S2, S3, S4 = "1 Euler's method", '2 Better methods', '3 Stability', '4 Systems'

B.md(r'''
# Unit 5 · Week 3 — Solving differential equations numerically
*Term 2, week 15 · about 15 hours in this notebook and on paper*

**Where you are.** Two weeks of formulas: separable and linear equations. But change one detail — quadratic drag instead of linear, a pendulum instead of a spring, a diode in the circuit — and no formula exists. Yet the Physics Lab, the Robotics Lab and the circuit simulator solve such equations thousands of times per second. This week you build the methods they use, and learn the two questions every simulation engineer must ask: **how accurate is it, and will it stay stable?**

**What you will be able to do at the end of this week**
1. Derive Euler's method from the tangent line, implement it, and explain (and measure) why its error is proportional to the step size $h$.
2. Explain and implement Heun's method and the classical Runge–Kutta method (RK4), with errors $\propto h^2$ and $\propto h^4$.
3. Find the stability limit of Euler's method for $y'=-ky$, and connect it to the learning-rate limit of gradient descent.
4. Turn a second-order equation (a pendulum) into a system of first-order ones and solve it with the same code.

**What is used from earlier:** the linear approximation $f(a+h)\approx f(a)+f'(a)h$ (Unit 2), the Taylor remainder (Unit 4), the trapezoid and Simpson rules (Unit 3 week 2), and the exact solutions of weeks 13–14 (to check the numbers).

Run the grey *SETUP* cell first.
''')

# =====================================================================================
B.md(r'''
---
# Part 1 — Euler's method

## 1.1 Follow the tangent

**Build.** We want $y(t)$ with $y'=f(t,y)$ and $y(t_0)=y_0$. The equation gives the **slope** at the start: $f(t_0,y_0)$. Over a short step $h$ the curve is nearly its tangent (Unit 2, linear approximation):
$$y(t_0+h)\approx y_0+h\,f(t_0,y_0).$$
Then repeat from the new point:
$$\boxed{\,t_{n+1}=t_n+h,\qquad y_{n+1}=y_n+h\,f(t_n,y_n)\,}\qquad\textbf{Euler's method}$$
''')
B.fig('euler_steps', F.euler_steps, 'Four Euler steps for y′ = y. Each uses the slope at the start of the step, so it falls behind a curve that keeps steepening.')
B.md(r'''
**Worked example by hand.** $y'=y$, $y(0)=1$ (exact: $e^t$), $h=0.5$.

| $n$ | $t_n$ | $y_n$ | slope $f=y_n$ | $y_{n+1}=y_n+0.5\cdot f$ | exact $e^{t_{n+1}}$ |
|---|---|---|---|---|---|
| 0 | 0 | 1 | 1 | 1.5 | 1.649 |
| 1 | 0.5 | 1.5 | 1.5 | 2.25 | 2.718 |
| 2 | 1.0 | 2.25 | 2.25 | 3.375 | 4.482 |
| 3 | 1.5 | 3.375 | 3.375 | 5.0625 | 7.389 |

Euler gives $5.06$ for $e^2=7.39$. Notice $y_n=(1.5)^n=(1+h)^n$: with $h=\frac2n$ steps up to $t=2$, Euler computes $\left(1+\frac2n\right)^n$ — which tends to $e^2$ as $n\to\infty$ (Unit 1). Euler's method *is* the compound-interest limit.

You met this method already, without the name: the "small steps" simulations of the thrown ball (Unit 2) and the parachutist (Unit 3).

### Experiment 1 — write Euler's method
Complete one line. `f(t, y)` is the right-hand side of the equation.
''')
B.code(r'''
def euler(f, t0, y0, h, n):
    """n Euler steps of size h from (t0, y0). Returns the lists of t and y values."""
    ts, ys = [t0], [y0]
    for k in range(n):
        t, y = ts[-1], ys[-1]
        ys.append(...)              # one Euler step: y + h * (slope at the start)
        ts.append(t + h)
    return ts, ys


# ---------- tests: do not change ----------
def test_euler():
    good = 0
    try:
        ts, ys = euler(lambda t, y: y, 0.0, 1.0, 0.5, 4)
        ok = abs(ys[-1] - 5.0625) < 1e-12; good += ok; print('✓' if ok else '✗', "y' = y, h = 0.5, 4 steps ->", ys[-1], '  (expected 5.0625, the table above)')
        ts, ys = euler(lambda t, y: t, 0.0, 0.0, 0.1, 10)
        ok = abs(ys[-1] - 0.45) < 1e-12; good += ok; print('✓' if ok else '✗', "y' = t from 0 to 1, h = 0.1 ->", ys[-1], '  (expected 0.45: a left Riemann sum!)')
    except Exception as err:
        print('✗ not working yet (have you replaced the ... ?)', type(err).__name__)
    print('\nAll tests passed.' if good == 2 else '\nNot there yet: the step is  y + h * f(t, y).')

test_euler()
''', ref=r'''
def euler(f, t0, y0, h, n):
    ts, ys = [t0], [y0]
    for k in range(n):
        t, y = ts[-1], ys[-1]
        ys.append(y + h * f(t, y))
        ts.append(t + h)
    return ts, ys
print(euler(lambda t, y: y, 0.0, 1.0, 0.5, 4)[1][-1])
''')
B.md(r'''
*Remark on the second test:* for $y'=f(t)$ (no $y$ on the right) solving the ODE is just integrating, and Euler's method becomes the **left Riemann sum** of Unit 3. Numerical ODE solvers are numerical integrators in disguise — which is why the better methods below look like the trapezoid and Simpson rules.

## 1.2 How large is the error?

**Build.**

**Local error (one step).** By Taylor (Unit 4), $y(t+h)=y(t)+h\,y'(t)+\frac{h^2}{2}y''(\xi)$. Euler keeps the first two terms, so each step makes an error of about $\frac{h^2}{2}|y''|$ — proportional to $h^2$.

**Global error (after reaching a fixed time $T$).** That needs $\frac{T}{h}$ steps. Roughly, the errors add up: $\frac Th\times h^2\propto h$. So
$$\text{global error of Euler's method}\ \propto\ h .$$
Halve the step, halve the error — and double the work. A method whose error is $\propto h^p$ is called **order $p$**: Euler is order 1. *(The "roughly" hides that errors made early are also carried along — and can be amplified or damped by the equation itself; Part 3.)*

### Experiment 2 — measure the order
Solve $y'=y$ from 0 to 1 and compare with $e$. **Predict first:** when $h$ is divided by 10, by what factor does the error shrink?
''')
B.code(r'''
rows = []
for n in [10, 100, 1000, 10000]:
    h = 1 / n
    y = 1.0
    for k in range(n): y = y + h * y          # Euler for y' = y
    rows.append([h, y, abs(y - e), abs(y - e) / h])
table(['h', 'Euler y(1)', 'error', 'error / h'], rows, fmt='%.6g')
''')
B.md(r'''
*Explain:* ten times smaller $h$, ten times smaller error; the last column settles near $1.36=\frac e2$. To get 6 correct digits Euler needs about a million steps. That is the motivation for better methods.
''')
B.ask(r'''Do one Euler step by hand for $y'=t+y$, $y(0)=1$, with $h=0.1$. What is $y_1$?''', 'num', 1.1,
      r'''Slope at the start: $f(0,1)=0+1=1$. $y_1=1+0.1\cdot1=1.1$.''',
      r'''$y_1=y_0+h\,f(t_0,y_0)$.''')
B.ask(r'''Euler's method gives an error of 0.02 with $h=0.01$. Roughly what error do you expect with $h=0.0025$?''', 'num', 0.005,
      r'''Order 1: four times smaller step, four times smaller error: $0.005$.''',
      r'''Euler's global error is proportional to $h$.''')

# =====================================================================================
B.md(r'''
---
# Part 2 — Better methods: Heun and Runge–Kutta

## 2.1 Heun's method (improved Euler)

**Build.** Euler uses only the slope at the *start* of the step. Better: average the slopes at the start and at the end — the trapezoid rule of Unit 3 instead of the left Riemann sum. The slope at the end needs the value at the end, which we do not have yet — so estimate it with an Euler step first:
$$\begin{aligned}
k_1&=f(t_n,\,y_n) &&\text{slope at the start}\\
k_2&=f(t_n+h,\,y_n+h\,k_1) &&\text{slope at the end, at the Euler estimate}\\
y_{n+1}&=y_n+\frac h2\,(k_1+k_2) &&\text{average slope}
\end{aligned}$$
Two evaluations of $f$ per step, and the error is $\propto h^2$ (order 2), just as the trapezoid rule beat the rectangle rule.

## 2.2 The classical Runge–Kutta method (RK4)

**Build.** Sample the slope four times across the step and take a weighted average:
$$\begin{aligned}
k_1&=f(t_n,\,y_n) &&\text{at the start}\\
k_2&=f\!\left(t_n+\tfrac h2,\ y_n+\tfrac h2k_1\right) &&\text{at the middle, using }k_1\\
k_3&=f\!\left(t_n+\tfrac h2,\ y_n+\tfrac h2k_2\right) &&\text{at the middle again, using the better }k_2\\
k_4&=f\!\left(t_n+h,\ y_n+h\,k_3\right) &&\text{at the end}\\
y_{n+1}&=y_n+\frac h6\left(k_1+2k_2+2k_3+k_4\right)
\end{aligned}$$
''')
B.fig('rk4_stages', F.rk4_stages, 'One RK4 step of length 1 for y′ = y: four slopes, combined with weights 1, 2, 2, 1.')
B.md(r'''
**Where do the weights $1,2,2,1$ come from?** For $y'=f(t)$ (no $y$ on the right), $k_2=k_3$ and the formula becomes $\frac h6\left(f_0+4f_{1/2}+f_1\right)$ — exactly **Simpson's rule** (Unit 3), whose error is $\propto h^4$ globally. For general $f$ the four stages are chosen so that the step agrees with the Taylor series of the true solution up to the $h^4$ term (a long but mechanical calculation). RK4 is **order 4**: halve the step, divide the error by 16.

**Worked example: one RK4 step by hand.** $y'=y$, $y(0)=1$, $h=1$ (one giant step to $t=1$):
$k_1=1$; $\;k_2=1+\frac12\cdot1=1.5$; $\;k_3=1+\frac12\cdot1.5=1.75$; $\;k_4=1+1\cdot1.75=2.75$.
$y_1=1+\frac16(1+3+3.5+2.75)=1+\frac{10.25}{6}=2.7083$ — against $e=2.7183$. One step, error $0.01$; Euler with $h=1$ gives $2$.

**This is what the labs use.** The Physics Lab integrates every experiment with RK4 at a fixed small step (2 ms for the projectile, 1 ms for the double pendulum) — as its Theory panels say.

### Experiment 3 — write one RK4 step
''')
B.code(r'''
def rk4_step(f, t, y, h):
    """One classical Runge-Kutta step. Returns the new y."""
    k1 = f(t, y)
    k2 = f(t + h / 2, y + h / 2 * k1)
    k3 = ...                         # (1) slope at the middle, using k2
    k4 = ...                         # (2) slope at the end, using k3
    return y + h / 6 * (k1 + 2 * k2 + 2 * k3 + k4)


# ---------- tests: do not change ----------
def test_rk4():
    good = 0
    try:
        r = float(rk4_step(lambda t, y: y, 0.0, 1.0, 1.0))
        ok = abs(r - 2.708333333333333) < 1e-12; good += ok; print('✓' if ok else '✗', "one step of y' = y with h = 1 ->", r, ' (expected 2.70833…)')
        y = 1.0
        for k in range(10): y = rk4_step(lambda t, y: -2 * t * y, k * 0.1, y, 0.1)
        ok = abs(y - exp(-1)) < 1e-6; good += ok; print('✓' if ok else '✗', "y' = -2ty to t = 1 ->", y, '  exact e^(-1) =', exp(-1))
    except Exception as err:
        print('✗ not working yet (have you replaced the ... ?)', type(err).__name__)
    print('\nAll tests passed.' if good == 2 else '\nNot there yet: k3 = f(t + h/2, y + h/2*k2),  k4 = f(t + h, y + h*k3).')

test_rk4()
''', ref=r'''
def rk4_step(f, t, y, h):
    k1 = f(t, y)
    k2 = f(t + h / 2, y + h / 2 * k1)
    k3 = f(t + h / 2, y + h / 2 * k2)
    k4 = f(t + h, y + h * k3)
    return y + h / 6 * (k1 + 2 * k2 + 2 * k3 + k4)
print(rk4_step(lambda t, y: y, 0.0, 1.0, 1.0))
''')
B.md(r'''
### Experiment 4 — Euler, Heun and RK4 side by side
All three solve $y'=y$ to $t=1$ with the same number of steps. **Predict first:** with 100 steps, roughly how many correct digits does each give?
''')
B.code(r'''
def solve(method, n):
    h, y = 1 / n, 1.0
    f = lambda t, y: y
    for k in range(n):
        t = k * h
        if method == 'euler':
            y = y + h * f(t, y)
        elif method == 'heun':
            k1 = f(t, y); k2 = f(t + h, y + h * k1); y = y + h / 2 * (k1 + k2)
        else:
            k1 = f(t, y); k2 = f(t + h/2, y + h/2*k1); k3 = f(t + h/2, y + h/2*k2); k4 = f(t + h, y + h*k3)
            y = y + h / 6 * (k1 + 2*k2 + 2*k3 + k4)
    return abs(y - e)

ns = [5, 10, 20, 50, 100, 200, 500]
errs = {m: [solve(m, n) for n in ns] for m in ['euler', 'heun', 'rk4']}
table(['steps', 'Euler error', 'Heun error', 'RK4 error'], [[n] + [errs[m][i] for m in errs] for i, n in enumerate(ns)], fmt='%.2e')
hs = [1 / n for n in ns]
for m, mk in zip(errs, 'os^'): plt.loglog(hs, np.maximum(errs[m], 1e-17), mk + '-', label=m)
plt.xlabel('step h'); plt.ylabel('error at t = 1'); plt.gca().invert_xaxis(); plt.legend(); plt.show()
''')
B.md(r'''
*Explain:* on the log–log plot the three lines have slopes 1, 2 and 4 — the orders. With 100 steps: Euler gets about 2 correct digits, Heun about 4, RK4 about 9. RK4 costs four evaluations per step, Euler one; even so, for any accuracy you care about RK4 is far cheaper. (At extremely small $h$ RK4's error hits rounding noise, the same floor as the numerical derivative in Unit 2.)

**Adaptive steps (in one paragraph).** Professional solvers (like `scipy.integrate.solve_ivp`) estimate their own error each step — for example by comparing a 4th- and a 5th-order result — and shrink the step where the solution changes fast and enlarge it where it is smooth. The labs use fixed steps instead, because a real-time animation wants a steady pace.
''')
B.ask(r'''Do one Heun step for $y'=y$, $y(0)=1$, $h=0.5$. What is $y_1$?''', 'num', 1.625,
      r'''$k_1=1$; $k_2=f(0.5,\ 1+0.5)=1.5$; $y_1=1+0.25\cdot(1+1.5)=1.625$ (exact $1.6487$; Euler gives $1.5$).''',
      r'''$k_1=f(t_0,y_0)$, $k_2=f(t_0+h,\ y_0+h k_1)$, $y_1=y_0+\frac h2(k_1+k_2)$.''')
B.ask(r'''RK4 gives an error of $10^{-6}$ with $h=0.1$. Roughly what error do you expect with $h=0.05$?''', 'num', 1e-6 / 16,
      r'''Order 4: halve $h$, divide the error by $2^4=16$: about $6\times10^{-8}$.''',
      r'''Error $\propto h^4$.''', fmt='a number, e.g. `6.25e-8`')

# =====================================================================================
B.md(r'''
---
# Part 3 — Stability: when a simulation explodes

**Why.** A simulation can be wrong in two ways: inaccurate (small errors) or **unstable** (errors grow until the numbers explode). The second happens suddenly when the step is too large — and it is not about accuracy at all.

**Build.** Take the simplest decaying equation $y'=-ky$ ($k>0$; exact solution $y_0e^{-kt}$ decays). Euler's step:
$$y_{n+1}=y_n+h(-ky_n)=(1-hk)\,y_n\qquad\Rightarrow\qquad y_n=(1-hk)^n\,y_0 .$$
Everything depends on the **amplification factor** $1-hk$ (the geometric sequence of Unit 4):

| $hk$ | factor $1-hk$ | Euler's numbers |
|---|---|---|
| $<1$ | between 0 and 1 | decay smoothly ✓ |
| between 1 and 2 | between $-1$ and $0$ | decay, but flip sign every step |
| $=2$ | $-1$ | oscillate with constant size |
| $>2$ | below $-1$ | **grow without bound** — the simulation explodes |

$$\boxed{\,\text{Euler is stable for }y'=-ky\text{ only if }h<\frac2k\,}$$
''')
B.fig('instability', F.instability, 'The same equation, three step sizes. Past h = 2/k the numerical "solution" explodes although the true one decays.')
B.md(r'''
**The same rule as in the AI & ML Lab.** Gradient descent on a bowl-shaped loss with curvature $\lambda$ is Euler's method applied to $\theta'=-\lambda\theta$ with the learning rate as the step size. Its limit $\eta<\frac{2}{\lambda}$ (the first experiment there) is exactly this stability limit. Training a neural network *is* numerically solving a differential equation.

**Stiffness.** Trouble arises when a system contains one very fast process ($k$ large) and you want to follow a slow one: stability then forces a tiny step everywhere, even after the fast part has died out. Such equations are called **stiff** (a circuit with a 1 ns and a 1 s time constant; chemical reactions). They are solved with *implicit* methods, which use the slope at the *end* of the step and are stable for any $h$. RK4 also has a stability limit (about $hk<2.8$), larger than Euler's, but finite.

### Experiment 5 — find the limit
**Predict first:** for $k=10$, at which step size does Euler start to explode? Does RK4 survive a bit larger steps?
''')
B.code(r'''
def stability(h=0.15, k=10.0):
    n = int(3 / h)
    ye, yr, ts = [1.0], [1.0], [0.0]
    f = lambda t, y: -k * y
    for i in range(n):
        t = ts[-1]
        ye.append(ye[-1] + h * f(t, ye[-1]))
        y = yr[-1]; k1 = f(t, y); k2 = f(t + h/2, y + h/2*k1); k3 = f(t + h/2, y + h/2*k2); k4 = f(t + h, y + h*k3)
        yr.append(y + h / 6 * (k1 + 2*k2 + 2*k3 + k4)); ts.append(t + h)
    tt = np.linspace(0, 3, 300)
    plt.figure(figsize=(8, 3.4)); plt.plot(tt, np.exp(-k * tt), 'k', lw=2, label='exact')
    plt.plot(ts, ye, 'o-', ms=3, label='Euler'); plt.plot(ts, yr, 's-', ms=3, label='RK4')
    plt.ylim(-2, 2); plt.legend(); plt.xlabel('t'); plt.show()
    print(f'h·k = {h * k:.2f}    Euler factor 1 − hk = {1 - h * k:.2f}    Euler limit h < {2 / k:.3f}')

explore(stability, h=(0.01, 0.35, 0.01, 0.15), k=(2, 20, 1, 10))
''')
B.ask(r'''For $y'=-50y$, what is the largest stable Euler step size?''', 'num', 0.04,
      r'''$h<\frac2k=\frac2{50}=0.04$.''',
      r'''Stability needs $|1-hk|<1$, i.e. $h<\frac2k$.''')

# =====================================================================================
B.md(r'''
---
# Part 4 — Systems: one method for every simulator

## 4.1 From second order to first order

**Why.** Newton's law $F=ma$ involves the **second** derivative of position. A pendulum: $\theta''=-\frac gL\sin\theta$. No formula solves it (Unit 4 found only a series for its period). Our methods handle first-order equations. The trick: introduce the velocity as a second unknown.

**Build.** Let $\omega=\theta'$ (angular velocity). Then the one second-order equation becomes two first-order ones:
$$\theta'=\omega,\qquad\omega'=-\frac gL\sin\theta .$$
Write the unknowns as a vector $\mathbf y=(\theta,\omega)$ and the right-hand sides as a vector function $\mathbf f(t,\mathbf y)=\big(\omega,\,-\frac gL\sin\theta\big)$. Then the system is $\mathbf y'=\mathbf f(t,\mathbf y)$ — **the same form as before**, and Euler and RK4 work unchanged, step by step on each component. (With numpy arrays, the `rk4_step` you wrote works as it is.)

This is literally what the labs do: the Physics Lab's state for the double pendulum is the vector (θ₁, θ₂, ω₁, ω₂); the Robotics Lab integrates the joint angles and speeds of a two-link arm.

## 4.2 Energy as a test of a simulator

For the pendulum without friction, the energy $E=\frac12L^2\omega^2+gL(1-\cos\theta)$ (per unit mass) must stay constant. That gives a test that needs no exact solution: **a good simulation keeps the energy constant.** Euler's method visibly fails this test — it pumps energy into the pendulum, which then swings higher and higher.

### Experiment 6 — a pendulum, two methods
The cell uses your `rk4_step` with numpy vectors. **Predict first:** after 10 s with $h=0.05$ s, what will Euler's pendulum look like compared with RK4's?
''')
B.code(r'''
g, L = 9.81, 1.0
def pend(t, Y):                     # Y = [theta, omega]
    return np.array([Y[1], -g / L * np.sin(Y[0])])

def energy(Y): return 0.5 * L**2 * Y[1]**2 + g * L * (1 - np.cos(Y[0]))

def run(h=0.05, T=10.0):
    n = int(T / h)
    Ye = [np.array([1.0, 0.0])]; Yr = [np.array([1.0, 0.0])]
    for k in range(n):
        t = k * h
        Ye.append(Ye[-1] + h * pend(t, Ye[-1]))
        Yr.append(rk4_step(pend, t, Yr[-1], h))
    ts = np.arange(n + 1) * h; Ye, Yr = np.array(Ye), np.array(Yr)
    fig, (a1, a2) = plt.subplots(1, 2, figsize=(10.5, 3.4))
    a1.plot(ts, Ye[:, 0], label='Euler'); a1.plot(ts, Yr[:, 0], label='RK4'); a1.set_xlabel('t (s)'); a1.set_ylabel('angle (rad)'); a1.legend()
    a2.plot(ts, [energy(Y) for Y in Ye], label='Euler'); a2.plot(ts, [energy(Y) for Y in Yr], label='RK4'); a2.set_xlabel('t (s)'); a2.set_ylabel('energy per kg'); a2.legend()
    plt.show()
    print(f'energy drift after {T:.0f} s:  Euler {energy(Ye[-1]) - energy(Ye[0]):+.4f}   RK4 {energy(Yr[-1]) - energy(Yr[0]):+.2e}')

try:                                # this experiment uses YOUR rk4_step from Experiment 3
    ready = np.all(np.isfinite(rk4_step(pend, 0.0, np.array([1.0, 0.0]), 0.05)))
except Exception:
    ready = False
if ready:
    explore(run, h=(0.005, 0.1, 0.005, 0.05))
else:
    print('Complete rk4_step in Experiment 3 first, run that cell, then run this cell again.')
''')
B.md(r'''
*Explain:* Euler's pendulum swings ever wider and its energy climbs steadily; RK4's energy stays constant to many digits. Halving $h$ halves Euler's drift but never removes it. That is why the labs use RK4 — and why the Physics Lab shows an energy graph: it is the simulator's own accuracy check.
''')
B.ask(r'''Write $y''+3y'+2y=0$ as a first-order system $u_1=y$, $u_2=y'$. In $u_2'=a\,u_1+b\,u_2$, what is $a$?''', 'num', -2,
      r'''$u_1'=u_2$ and $u_2'=y''=-2y-3y'=-2u_1-3u_2$. So $a=-2$, $b=-3$.''',
      r'''Solve the equation for $y''$ and replace $y$, $y'$ by $u_1$, $u_2$.''')

B.md(r'''
## Week summary — everything on one page

- **Euler**: $y_{n+1}=y_n+h\,f(t_n,y_n)$ — the tangent line. Order 1 (error $\propto h$).
- **Heun**: average of the slopes at start and end (trapezoid). Order 2.
- **RK4**: $\frac h6(k_1+2k_2+2k_3+k_4)$ with slopes at start, middle (twice) and end (Simpson). Order 4.
- **Order $p$**: halve $h$ → error divided by $2^p$. Measure it on a log–log plot.
- **Stability** for $y'=-ky$: Euler factor $1-hk$; stable iff $h<\frac2k$. Same as $\eta<\frac2\lambda$ for gradient descent. Stiff systems need implicit methods.
- **Systems**: write $y''=\dots$ as $(y,y')'=\dots$; the same code solves it. Check simulators with conserved quantities such as energy.
''')

# =====================================================================================
B.md(r'''
---
# Problems

Paper first (or a code cell as calculator). First attempt counts. `hint(n)` → `solution(n)` → `mistake(n, '...')`.

### Euler's method
''')
B.problem(S1, r'Two Euler steps by hand for $y\,^\prime=2t$, $y(0)=0$, $h=0.5$. Give $y_2$ (an estimate of $y(1)$).', 'num', 0.5,
          [r'Step 1: slope $f(0,0)=0$. Step 2: slope $f(0.5,\ y_1)=1$.'],
          r'''$y_1=0+0.5\cdot2\cdot0=0$; $\;y_2=0+0.5\cdot2\cdot0.5=$ **0.5**.

Exact: $y=t^2$, $y(1)=1$. Euler for $y'=f(t)$ is the left Riemann sum, which underestimates a rising function.''')
B.problem(S1, r'Two Euler steps for $y\,^\prime=y-t$, $y(0)=2$, $h=0.1$. Give $y_2$.', 'num', 2.0 + 0.1 * 2 + 0.1 * (2.2 - 0.1),
          [r'$y_1=2+0.1\cdot(2-0)$.', r'$y_2=y_1+0.1\cdot(y_1-0.1)$.'],
          r'''$y_1=2+0.1\cdot(2-0)=2.2$; $\;y_2=2.2+0.1\cdot(2.2-0.1)=2.2+0.21=$ **2.41**.

(Exact: $y=e^t+t+1$, $y(0.2)=2.4214$.)''')
B.problem(S1, r'Euler with $h=0.1$ has an error of $0.04$ at $t=2$. Which step size gives an error of about $0.001$?', 'num', 0.0025,
          [r'Error ∝ h: the error must become 40 times smaller.'],
          r'''Order 1: error $\propto h$. Factor $\frac{0.04}{0.001}=40$, so $h=\frac{0.1}{40}=$ **0.0025** (800 steps instead of 20).''')
B.md(r'''
### Better methods
''')
B.problem(S2, r'One Heun step for $y\,^\prime=-2y$, $y(0)=1$, $h=0.1$. Give $y_1$.', 'num', 1 + 0.05 * (-2 + -2 * 0.8),
          [r'$k_1=f(0,1)=-2$; Euler estimate $1+0.1\cdot(-2)=0.8$; $k_2=f(0.1,\ 0.8)=-1.6$.'],
          r'''$k_1=-2$, $\;k_2=-2\cdot0.8=-1.6$, $\;y_1=1+\frac{0.1}{2}(-2-1.6)=1-0.18=$ **0.82**.

(Exact $e^{-0.2}=0.8187$; Euler gives $0.8$.)''')
B.problem(S2, r'One RK4 step for $y\,^\prime=y$, $y(0)=1$, $h=0.5$. Give $y_1$ (compare with $e^{0.5}=1.64872$).', 'num', 1 + 0.5 / 6 * (1 + 2 * 1.25 + 2 * 1.3125 + 1.65625),
          [r'$k_1=1$, $k_2=1+0.25\cdot1=1.25$, $k_3=1+0.25\cdot1.25$, $k_4=1+0.5\,k_3$.'],
          r'''$k_1=1$, $\;k_2=1.25$, $\;k_3=1+0.25\cdot1.25=1.3125$, $\;k_4=1+0.5\cdot1.3125=1.65625$.
$$y_1=1+\frac{0.5}{6}\left(1+2.5+2.625+1.65625\right)=1+\frac{0.5\cdot7.78125}{6}=1.64844 .$$
Error $0.0003$ after one big step.''')
B.problem(S2, r'For $y\,^\prime=f(t)$ (no $y$ on the right), one RK4 step reduces to which rule from Unit 3? (a) left rectangles (b) trapezoid (c) Simpson', 'choice', 'c',
          [r'When $f$ does not depend on $y$, $k_2=k_3=f(t+\frac h2)$.'],
          r'''$k_1=f(t)$, $k_2=k_3=f(t+\frac h2)$, $k_4=f(t+h)$: $\;\frac h6\left(f_0+4f_{1/2}+f_1\right)$ — **Simpson's rule (c)**. Heun becomes the trapezoid rule, Euler the left rectangle rule.''')
B.problem(S2, r'A method has error $8\times10^{-5}$ with $h=0.2$ and $5\times10^{-6}$ with $h=0.1$. What is its order $p$?', 'num', 4,
          [r'Halving h divided the error by 16. $2^p=16$.'],
          r'''$\frac{8\times10^{-5}}{5\times10^{-6}}=16=2^p\Rightarrow p=$ **4** (an RK4-like method).''')
B.md(r'''
### Stability
''')
B.problem(S3, r'A circuit has time constant $\tau=2$ ms, i.e. $v\,^\prime=-\frac{1}{\tau}v$. What is the largest stable Euler time step (in ms)?', 'num', 4,
          [r'$k=\frac1\tau$; stability needs $h<\frac2k=2\tau$.'],
          r'''$k=\frac1\tau$, so $h<\frac2k=2\tau=$ **4 ms**. (For accuracy you would choose a much smaller step, say $\frac{\tau}{20}$.)''', fmt='milliseconds')
B.problem(S3, r'Euler on $y\,^\prime=-4y$ with $h=0.3$: what is the amplification factor $1-hk$?', 'num', -0.2,
          [r'$k=4$, $h=0.3$.'],
          r'''$1-0.3\cdot4=$ **−0.2**: stable ($|{-0.2}|<1$), but the numbers flip sign every step — qualitatively wrong although they decay.''')
B.problem(S3, r'Gradient descent on the loss $L(w)=3w^2$ uses $w\leftarrow w-\eta\,L\,^\prime(w)$. Above which learning rate $\eta$ does it diverge?', 'num', 1 / 3,
          [r'$L\,^\prime(w)=6w$, so $w\leftarrow(1-6\eta)w$.', r'Need $|1-6\eta|<1$.'],
          r'''$w_{n+1}=(1-6\eta)\,w_n$: Euler for $w'=-6w$ with step $\eta$. Stable iff $\eta<\frac26=$ **1/3**.''', fmt='a number, e.g. `1/3`')
B.md(r'''
### Systems
''')
B.problem(S4, r'Write $y\,^{\prime\prime}=-9y$ as a system $u_1=y$, $u_2=y\,^\prime$ and do one Euler step from $u_1=1$, $u_2=0$ with $h=0.1$. Give the new $u_2$.', 'num', -0.9,
          [r'$u_1\,^\prime=u_2$, $u_2\,^\prime=-9u_1$.'],
          r'''$u_1'=u_2$, $u_2'=-9u_1$. Euler: $u_1\leftarrow1+0.1\cdot0=1$, $\;u_2\leftarrow0+0.1\cdot(-9\cdot1)=$ **−0.9**.''')
B.problem(S4, r'For the frictionless pendulum, the energy per kg is $E=\frac12L^2\omega^2+gL(1-\cos\theta)$. With $L=1$, $g=9.81$, released at $\theta=1$ rad from rest, what is $E$?', 'num', 9.81 * (1 - math.cos(1)),
          [r'At release $\omega=0$.'],
          r'''$E=0+9.81\,(1-\cos1)=9.81\cdot0.4597\approx$ **4.510 J/kg**. A correct simulation keeps this value for ever.''')
B.problem(S4, r'Euler on the undamped oscillator $u_1\,^\prime=u_2$, $u_2\,^\prime=-u_1$ multiplies $u_1^2+u_2^2$ by exactly $1+h^2$ each step. After 100 steps with $h=0.1$, by what factor has $u_1^2+u_2^2$ grown?', 'num', 1.01 ** 100,
          [r'$(1+h^2)^{100}$ with $h^2=0.01$.'],
          r'''$(1.01)^{100}\approx$ **2.70** — the "energy" has nearly tripled in 10 s of simulated time, although the true value is constant. (Proof of the factor: $(u_1+hu_2)^2+(u_2-hu_1)^2=(1+h^2)(u_1^2+u_2^2)$.)''')
B.code(r'''
# scratch cell
''')

B.md(r'''
---
# Finish the week — and Unit 5

### 1 · Report
''')
B.code(r'''
report()
''')
B.md(r'''
### 2 · Teach-back (30 minutes, from memory)
1. Derive Euler's method and explain why its global error is proportional to $h$.
2. What do the four slopes of RK4 measure, and why the weights $1,2,2,1$?
3. Show that Euler on $y'=-ky$ is stable only for $h<\frac2k$. Where did you meet the same inequality before?
4. How do you solve a second-order equation with a first-order method?
5. How can you test a simulator without knowing the exact solution?

*Your answers:*

&nbsp;

### 3 · Lab strand — watch a simulator check itself (1 hour)
The double pendulum in the Physics Lab is integrated with RK4 at a 1 ms step; its energy graph (with friction 0) must stay flat. **Predict first:** will the energy drift visibly in 30 s? Then observe it — and look at the "twin" pendulum: two simulations started 0.001 rad apart. Their separation grows exponentially (chaos). That is not a numerical error: it is a property of the equations, and it means that beyond a few seconds *no* method can predict this system, however accurate.
''')
B.code(r'''
lab('physics', exp='dbl')
''')
B.md(r'''
### 4 · What comes next
**Unit 6 — complex numbers and phasors.** You have seen $e^{i\theta}=\cos\theta+i\sin\theta$ (Unit 4) and solved an RC circuit with a sine input by matching sines and cosines (week 14). Complex numbers turn that page of algebra into one line — and make every AC circuit as easy as a DC one.
''')

if __name__ == '__main__':
    B.write()
