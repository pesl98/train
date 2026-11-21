"""Unit 5 · Week 1 (course week 13) - Differential equations: meaning, direction fields, separable equations."""
import math
from nbkit import Book
import figs_u05 as F

B = Book('u05w1', 'Unit 5 · Week 1 — Differential equations and separable equations', 'year1/u05w1-odes-separable.ipynb')
S1, S2, S3, S4 = '1 What an ODE is', '2 Separable equations', '3 Growth, decay, cooling', '4 Logistic growth and equilibria'

B.md(r'''
# Unit 5 · Week 1 — Differential equations and separable equations
*Term 2, week 13 · about 15 hours in this notebook and on paper*

**Where you are.** Term 1 gave you the two halves of calculus: derivatives (rates) and integrals (accumulation). Term 2 starts with the reason engineers learn them: **the laws of nature and of machines are almost always statements about rates.** "A capacitor charges at a rate proportional to the remaining voltage." "A hot drink cools at a rate proportional to its temperature above the room." "A population grows at a rate proportional to its size." Each sentence is an equation that contains an unknown **function together with its derivative** — a *differential equation*. Solving it means finding the function.

**The plan for Unit 5**

| week | content |
|---|---|
| **13 (this notebook)** | what a differential equation is; direction fields; separable equations; growth, decay, cooling, logistic growth |
| 14 | linear first-order equations; RC and RL circuits; response to a sine wave (the first filter) |
| 15 | solving them numerically: Euler, Runge–Kutta, error, step size, stability — what every simulator in the labs does |

**What you will be able to do at the end of this week**
1. Translate a sentence about a rate into a differential equation, and check whether a given function solves it.
2. Read a direction field and sketch solutions from it.
3. Solve separable equations — and explain why "separate and integrate" is the chain rule, not a trick.
4. Solve and apply exponential growth/decay, Newton's law of cooling and the logistic equation; find equilibria and decide whether they are stable.

**What is used from earlier:** derivatives, especially the chain rule (Unit 2); integrals and partial fractions (Unit 3); $e^x$ and $\ln$ (Units 1–2).

Run the grey *SETUP* cell first.
''')

# =====================================================================================
B.md(r'''
---
# Part 1 — What a differential equation is

## 1.1 From a sentence about a rate to an equation

**Build.** Three laws, each turned into symbols in the same three steps: *name the quantity, name its rate, write the sentence as an equation.*

**Cooling.** "A cup of coffee cools at a rate proportional to how much hotter it is than the room."
- Quantity: temperature $T(t)$; room temperature $T_a$ (constant).
- Rate: $\frac{dT}{dt}$.
- "Proportional to": a constant $k>0$ times; "cools": the rate is negative when $T>T_a$:
$$\frac{dT}{dt}=-k\,(T-T_a).$$

**Growth.** "Bacteria multiply at a rate proportional to how many there are": $\;\dfrac{dN}{dt}=kN$.

**A falling body with air resistance.** Newton: mass × acceleration = total force. Gravity $mg$ down, drag $cv$ up (for slow motion, drag is roughly proportional to speed):
$$m\frac{dv}{dt}=mg-cv .$$

Each is an equation in which the **unknown is a function** ($T(t)$, $N(t)$, $v(t)$), and in which that function's **derivative** appears. That is a **differential equation** (ODE — *ordinary* because there is only one independent variable, here time).

**Vocabulary.**
- The **order** is the highest derivative that appears. All of this unit: first order ($y'$ only). Springs and pendulums ($y''$) come in Unit 9.
- A **solution** is a function that makes the equation true for every $t$ in some interval.

## 1.2 Checking a solution

**Build.** You do not need to know how a solution was found to check it: substitute it and see whether both sides agree.

**Worked example 1.** Is $y=e^{3t}$ a solution of $y'=3y$?
Left side: $y'=3e^{3t}$. Right side: $3y=3e^{3t}$. Equal for every $t$ ✓.

**Worked example 2.** Is $y=5e^{3t}$? $y'=15e^{3t}=3\cdot5e^{3t}=3y$ ✓. And $y=Ce^{3t}$ for **any** constant $C$: $y'=3Ce^{3t}=3y$ ✓.

**Worked example 3.** Is $y=t^2$ a solution of $y'=3y$? $y'=2t$, $3y=3t^2$; equal only at $t=0$ and $t=\frac23$, not for every $t$. Not a solution.

## 1.3 General solution and initial value

Worked example 2 shows a general fact: a first-order ODE usually has a whole **family** of solutions with one free constant — the **general solution**. That is no surprise: solving a differential equation involves integrating, and every integration brings a $+C$.
''')
B.fig('exp_family', F.exp_family, 'One equation, infinitely many solutions: one for every starting value.')
B.md(r'''
To single out one member of the family you need one extra fact, usually the starting value $y(0)=y_0$: an **initial value problem**. Physically: the law (the ODE) says how the system *changes*; the initial value says where it *starts*. Both are needed to predict the future.

**Worked example 4.** Solve $y'=3y$, $y(0)=4$. General solution $y=Ce^{3t}$. At $t=0$: $4=Ce^0=C$. So $y=4e^{3t}$.
''')
B.ask(r'''Is $y=\sin t$ a solution of $y''=-y$? (a) yes (b) no''', 'choice', 'a',
      r'''$y'=\cos t$, $y''=-\sin t=-y$ ✓. (A second-order equation — the oscillator of Unit 9.)''',
      r'''Differentiate twice and compare with $-y$.''')
B.ask(r'''$y=Ce^{-2t}$ solves $y'=-2y$. Which $C$ gives $y(0)=7$?''', 'num', 7,
      r'''$y(0)=Ce^0=C=7$.''',
      r'''Put $t=0$: $e^0=1$.''')

B.md(r'''
## 1.4 Direction fields: seeing solutions without solving

**Why.** Most differential equations cannot be solved by formula. But a first-order equation $y'=f(t,y)$ tells you the **slope** of the solution through every point $(t,y)$ — and slopes can be drawn.

**Build.** At many points of the plane, draw a short line segment with slope $f(t,y)$. This is the **direction field**. A solution curve must be tangent to the segments everywhere it passes: follow the arrows like a leaf on a stream.
''')
B.fig('direction_field', F.direction_field, 'Every solution of y′ = x − y follows the little lines; all of them approach the line y = x − 1.')
B.md(r'''
**What the picture shows for $y'=x-y$.** Wherever $y=x-1$, the slope is $x-(x-1)=1$, equal to the slope of that line itself — so the line is a solution. Above it the slope is smaller (curves bend down towards it); below it larger (curves bend up). Every solution is drawn towards that line. You have learned the long-term behaviour of every solution without solving anything.

**Isoclines** (curves of equal slope) help when drawing by hand: here, slope $m$ wherever $x-y=m$, i.e. on the lines $y=x-m$.

### Experiment 1 — direction fields with a starting point
Choose an equation and a starting value. The cell draws the field and the solution through $(0, y_0)$ (computed numerically — week 15 shows how).

**Predict first:** for $y'=y(2-y)$, what happens to solutions that start at $y_0=0.1$, at $y_0=2$, at $y_0=3$, at $y_0=-0.1$?
''')
B.code(r'''
EQS = {"y' = x − y": lambda t, y: t - y,
       "y' = y (2 − y)": lambda t, y: y * (2 - y),
       "y' = −y + sin(3t)": lambda t, y: -y + np.sin(3 * t),
       "y' = t·y": lambda t, y: t * y}

def field(eq="y' = y (2 − y)", y0=0.1):
    f = EQS[eq]
    T, Y = np.meshgrid(np.linspace(-0.5, 4, 22), np.linspace(-1.5, 3.5, 22))
    S = f(T, Y); L = np.sqrt(1 + S**2)
    plt.figure(figsize=(7.5, 4.2))
    plt.quiver(T, Y, 1 / L, S / L, color='0.6', angles='xy', headwidth=1, headlength=0, pivot='mid')
    ts = np.linspace(0, 4, 800); ys = [y0]; h = ts[1] - ts[0]
    for i in range(len(ts) - 1):                      # Runge-Kutta steps (week 15)
        t, y = ts[i], ys[-1]
        k1 = f(t, y); k2 = f(t + h/2, y + h/2*k1); k3 = f(t + h/2, y + h/2*k2); k4 = f(t + h, y + h*k3)
        ys.append(y + h/6*(k1 + 2*k2 + 2*k3 + k4))
    plt.plot(ts, ys, 'r', lw=2.5); plt.plot([0], [y0], 'ro')
    plt.xlim(-0.5, 4); plt.ylim(-1.5, 3.5); plt.xlabel('t'); plt.ylabel('y'); plt.title(eq); plt.show()

explore(field, eq=list(EQS), y0=(-1.0, 3.0, 0.1, 0.1))
''')
B.md(r'''
*Explain:* for $y'=y(2-y)$, the horizontal lines $y=0$ and $y=2$ are solutions (the slope is zero there). Solutions between them rise towards 2; above 2 they fall towards 2; below 0 they fall away from 0. The value 2 attracts, 0 repels — Part 4 makes this precise.
''')
B.ask(r'''For $y'=y(2-y)$: what is the slope of the solution curve at the point $(t,y)=(1,\,1)$?''', 'num', 1,
      r'''$f(1,1)=1\cdot(2-1)=1$.''',
      r'''The equation gives the slope directly: substitute $y=1$.''')

# =====================================================================================
B.md(r'''
---
# Part 2 — Separable equations

## 2.1 The idea

**Why.** For the cooling, growth and drag equations above, the right-hand side is a product of "something in $t$" and "something in $y$". Such equations can be solved with two ordinary integrals.

**Definition.** $\;\dfrac{dy}{dt}=g(t)\,h(y)$ is called **separable**.

**The recipe** (as usually written):
1. Separate: $\;\dfrac{1}{h(y)}\,dy=g(t)\,dt$.
2. Integrate both sides: $\;\displaystyle\int\frac{dy}{h(y)}=\int g(t)\,dt$.
3. Solve for $y$ if possible; use the initial value to find the constant.

**Why this is legitimate (the chain rule).** Treating $dy$ and $dt$ like numbers looks suspicious — $\frac{dy}{dt}$ is a limit, not a fraction (Unit 2). Here is the honest argument. Let $H(y)$ be an antiderivative of $\frac{1}{h(y)}$, so $H'(y)=\frac1{h(y)}$. If $y(t)$ solves the ODE, then by the chain rule
$$\frac{d}{dt}H\big(y(t)\big)=H'(y)\,\frac{dy}{dt}=\frac{1}{h(y)}\cdot g(t)\,h(y)=g(t).$$
So $H(y(t))$ is an antiderivative of $g(t)$: $\;H(y(t))=\int g(t)\,dt+C$. That is exactly what step 2 says. The notation of step 1 is a convenient way to remember this; the chain rule is the reason it works.

**One caution.** Dividing by $h(y)$ is not allowed where $h(y)=0$. Those values give **constant solutions** $y=$ const (the slope is zero there). Check for them separately — they are the equilibria of Part 4.

## 2.2 Worked examples

**Worked example 1.** $\;\dfrac{dy}{dt}=t\,y$, $\;y(0)=2$.
1. Separate: $\dfrac{dy}{y}=t\,dt$ (for $y\ne0$).
2. Integrate: $\ln|y|=\dfrac{t^2}{2}+C$.
3. Solve: $|y|=e^{t^2/2+C}=e^C\,e^{t^2/2}$, i.e. $y=Ae^{t^2/2}$ with $A=\pm e^C$ (and $A=0$ covers the constant solution $y=0$).
4. Initial value: $2=Ae^0$, $A=2$. **Solution:** $y=2e^{t^2/2}$.
5. *Check:* $y'=2e^{t^2/2}\cdot t=t\,y$ ✓.

**Worked example 2.** $\;\dfrac{dy}{dx}=\dfrac{x}{y}$, $\;y(0)=3$.
1. $y\,dy=x\,dx$. 2. $\dfrac{y^2}{2}=\dfrac{x^2}{2}+C$. 3. $y^2=x^2+2C$. 4. At $x=0$: $9=2C$. So $y^2=x^2+9$; $y=+\sqrt{x^2+9}$ (positive root because $y(0)=3>0$).

**Worked example 3.** $\;\dfrac{dy}{dt}=1+y^2$, $\;y(0)=0$.
$\displaystyle\int\frac{dy}{1+y^2}=\int dt\ \Rightarrow\ \arctan y=t+C$. At $t=0$: $C=0$. So $y=\tan t$. It blows up at $t=\frac\pi2$: a solution can exist only for a limited time even when the equation looks harmless — something no amount of staring at "$1+y^2$" reveals. (The direction field would have shown it: the slopes grow ever steeper.)
''')
B.code(r'''
# Check worked example 1 numerically: the slope of y = 2 e^(t²/2) against t·y
compare(lambda v: 2 * exp(v**2 / 2), lambda v: v * 2 * exp(v**2 / 2), lo=-1.5, hi=1.5)
''')
B.ask(r'''Solve $\dfrac{dy}{dt}=3t^2\,y$ with $y(0)=1$. What is $y(1)$?''', 'num', math.e,
      r'''$\frac{dy}{y}=3t^2dt\Rightarrow\ln y=t^3+C$, $y=Ae^{t^3}$, $A=1$: $y(1)=e\approx2.718$.''',
      r'''Separate: $\frac{dy}{y}=3t^2\,dt$. Integrate both sides.''', fmt='a number; you can type `e`')

# =====================================================================================
B.md(r'''
---
# Part 3 — Growth, decay and cooling

## 3.1 Exponential growth and decay: $y'=ky$

**Build.** Separate: $\frac{dy}{y}=k\,dt$, so $\ln|y|=kt+C$, so
$$\boxed{\,y(t)=y_0\,e^{kt}\,}$$
(using $y(0)=y_0$). **The rate is proportional to the amount**, and the result is exponential — the property of $e^x$ found in Unit 2 ("its slope equals its height"). $k>0$: growth; $k<0$: decay.

**Doubling time and half-life.** For growth, the time $T_2$ to double: $y_0e^{kT_2}=2y_0\Rightarrow e^{kT_2}=2\Rightarrow T_2=\dfrac{\ln2}{k}$. For decay ($y'=-\lambda y$) the **half-life**: $\;T_{1/2}=\dfrac{\ln2}{\lambda}$. Both are **independent of the starting amount**: every half-life halves whatever is there.

**Worked example — carbon dating.** Carbon-14 has a half-life of 5730 years. A bone contains 30 % of the C-14 of living tissue. How old is it?
1. $\lambda=\dfrac{\ln2}{5730}=1.21\times10^{-4}$ per year.
2. $0.30=e^{-\lambda t}\Rightarrow t=\dfrac{-\ln0.30}{\lambda}=\dfrac{1.204}{1.21\times10^{-4}}\approx9950$ years.

## 3.2 Newton's law of cooling

**Build.** $\dfrac{dT}{dt}=-k(T-T_a)$. Substitute $u=T-T_a$ (the excess temperature): $u'=T'$, so $u'=-ku$ — pure decay! Hence $u=u_0e^{-kt}$ and
$$\boxed{\,T(t)=T_a+(T_0-T_a)\,e^{-kt}\,}$$
''')
B.fig('cooling', F.cooling, 'Hot or cold, every start approaches the room temperature, exponentially.')
B.md(r'''
**Worked example.** Coffee at 90 °C in a 20 °C room is 70 °C after 10 minutes. When is it 40 °C?
1. $70=20+70e^{-10k}\Rightarrow e^{-10k}=\frac{50}{70}\Rightarrow k=\frac{\ln1.4}{10}=0.0336$ per minute.
2. $40=20+70e^{-kt}\Rightarrow e^{-kt}=\frac{20}{70}\Rightarrow t=\frac{\ln3.5}{0.0336}\approx37.3$ minutes.

**The pattern** — the same equation describes very different things:

| system | quantity | approaches |
|---|---|---|
| cooling coffee | temperature | room temperature |
| charging capacitor (week 14) | voltage | supply voltage |
| falling body with linear drag | speed | terminal speed $\frac{mg}{c}$ |
| drug in the blood with steady infusion | concentration | steady level |

## 3.3 Falling with drag: terminal velocity

$m\frac{dv}{dt}=mg-cv$, i.e. $\frac{dv}{dt}=-\frac cm\left(v-\frac{mg}{c}\right)$: the cooling equation with "room temperature" $v_\infty=\frac{mg}{c}$. Starting from rest:
$$v(t)=\frac{mg}{c}\left(1-e^{-ct/m}\right).$$
The speed approaches the **terminal velocity** $v_\infty=\frac{mg}{c}$, where drag balances weight. (Real drag at higher speeds grows like $v^2$ — the Physics Lab's projectile and the parachutist of Unit 3 used that — but the picture is the same.)
''')
B.ask(r'''A radioactive sample has a half-life of 8 days. What fraction remains after 24 days?''', 'num', 0.125,
      r'''24 days = 3 half-lives: $\left(\frac12\right)^3=\frac18$.''',
      r'''Count half-lives.''', fmt='a number, e.g. `1/8`')
B.ask(r'''Bacteria double every 3 hours. What is $k$ in $N=N_0e^{kt}$ ($t$ in hours)?''', 'num', math.log(2) / 3,
      r'''$T_2=\frac{\ln2}{k}=3\Rightarrow k=\frac{\ln2}{3}\approx0.231$ per hour.''',
      r'''$T_2=\frac{\ln 2}{k}$.''', fmt='a number; you can type `ln(2)/3`')

# =====================================================================================
B.md(r'''
---
# Part 4 — Logistic growth and equilibria

## 4.1 Limits to growth

**Why.** $y'=ky$ predicts that a population grows for ever. Real ones run out of food or space. The simplest correction: the growth rate per individual falls as the population nears a **carrying capacity** $K$:
$$\frac{dP}{dt}=r\,P\left(1-\frac PK\right).$$
For small $P$ the bracket is about 1 — nearly exponential growth. As $P\to K$ the bracket → 0 and growth stops. (The same equation describes the spread of a rumour, an epidemic's early phase, or the adoption of a new product.)

## 4.2 Solving it (partial fractions, Unit 3)

1. Separate: $\displaystyle\int\frac{dP}{P\,(1-P/K)}=\int r\,dt$.
2. Partial fractions: $\dfrac{1}{P(1-P/K)}=\dfrac{K}{P(K-P)}=\dfrac1P+\dfrac{1}{K-P}$ (check: $\frac{(K-P)+P}{P(K-P)}$ ✓).
3. Integrate: $\ln P-\ln(K-P)=rt+C$, i.e. $\ln\dfrac{P}{K-P}=rt+C$.
4. Solve: $\dfrac{P}{K-P}=Ae^{rt}$ $\Rightarrow$ $P=\dfrac{K}{1+e^{-rt}/A}$. With $P(0)=P_0$: $\frac1A=\frac{K}{P_0}-1$.
$$\boxed{\,P(t)=\frac{K}{1+\left(\frac{K}{P_0}-1\right)e^{-rt}}\,}$$
''')
B.fig('logistic', F.logistic, 'Left: S-shaped growth to the carrying capacity. Right: the sign of P′ shows where P goes.')
B.md(r'''
**Reading the S-curve.** Growth is fastest where $P'=rP(1-\frac PK)$ is largest: maximise the parabola in $P$ — at $P=\frac K2$ (the inflection point of the S). Before it growth speeds up, after it slows down.

## 4.3 Equilibria and stability — without solving

**Build.** For an **autonomous** equation $y'=f(y)$ (no explicit $t$), you can learn a great deal from the graph of $f$ alone:

1. **Equilibria** are the values where $f(y)=0$: if the system starts there, $y'=0$ and it stays there for ever.
2. **Between** equilibria, the sign of $f$ says whether $y$ rises ($f>0$) or falls ($f<0$) — arrows on the $y$-axis (the right panel above; called a *phase line*).
3. An equilibrium is **stable** if the arrows on both sides point towards it (small disturbances die out), **unstable** if they point away.

**A quick test** (from the slope of $f$): at an equilibrium $y^*$, if $f'(y^*)<0$ it is stable, if $f'(y^*)>0$ unstable. *Why:* near $y^*$, $f(y)\approx f'(y^*)(y-y^*)$ (linear approximation, Unit 2), so the deviation $u=y-y^*$ obeys $u'\approx f'(y^*)\,u$ — exponential decay if $f'(y^*)<0$, growth if $>0$.

**Worked example (logistic).** $f(P)=rP(1-P/K)$: equilibria $P=0$ and $P=K$. $f'(P)=r-\frac{2rP}{K}$: $f'(0)=r>0$ (unstable), $f'(K)=-r<0$ (stable).

**Worked example (cooling).** $f(T)=-k(T-T_a)$: one equilibrium $T=T_a$, $f'=-k<0$: stable. The room temperature attracts.
''')
B.ask(r'''Find the non-zero equilibrium of $y'=y(6-2y)$.''', 'num', 3,
      r'''$y(6-2y)=0\Rightarrow y=0$ or $y=3$.''',
      r'''Set the right-hand side to zero.''')
B.ask(r'''Is the equilibrium $y=3$ of $y'=y(6-2y)$ stable? (a) stable (b) unstable''', 'choice', 'a',
      r'''$f(y)=6y-2y^2$, $f'(y)=6-4y$, $f'(3)=-6<0$: stable. (Just below 3, $f>0$ pushes up; just above, $f<0$ pushes down.)''',
      r'''Compute $f'(3)$ for $f(y)=6y-2y^2$, or check the sign of $f$ on each side.''')

B.md(r'''
## Week summary — everything on one page

- **ODE**: an equation for an unknown function containing its derivative. Order = highest derivative. Check a solution by substituting.
- **General solution** has a constant; the **initial value** fixes it.
- **Direction field**: slope $f(t,y)$ at each point; solutions follow it.
- **Separable** $y'=g(t)h(y)$: $\int\frac{dy}{h(y)}=\int g\,dt$ — justified by the chain rule. Constant solutions where $h(y)=0$.
- $y'=ky\Rightarrow y=y_0e^{kt}$; $T_2=\frac{\ln2}{k}$, $T_{1/2}=\frac{\ln2}{\lambda}$.
- Cooling $T=T_a+(T_0-T_a)e^{-kt}$; terminal velocity $\frac{mg}{c}$.
- Logistic $P=\dfrac{K}{1+(K/P_0-1)e^{-rt}}$; fastest growth at $\frac K2$.
- Equilibria of $y'=f(y)$: $f(y^*)=0$; stable if $f'(y^*)<0$, unstable if $f'(y^*)>0$.
''')

# =====================================================================================
B.md(r'''
---
# Problems

Paper first. First attempt counts. `hint(n)` → `solution(n)` → `mistake(n, '...')`.

### What an ODE is
''')
B.problem(S1, r'For which constant $k$ is $y=e^{kt}$ a solution of $y\,^{\prime\prime}-y\,^\prime-6y=0$? Give the positive value.', 'num', 3,
          [r'Substitute: $k^2e^{kt}-ke^{kt}-6e^{kt}=0$.', r'Divide by $e^{kt}$ (never zero): $k^2-k-6=0$.'],
          r'''$y'=ke^{kt}$, $y''=k^2e^{kt}$. Substituting and dividing by $e^{kt}\ne0$: $k^2-k-6=(k-3)(k+2)=0$.

So $k=3$ or $k=-2$; the positive value is **3**. (This "try $e^{kt}$" idea solves every linear equation with constant coefficients — Unit 9.)''')
B.problem(S1, r'A tank leaks so that its volume $V$ decreases at a rate proportional to $\sqrt V$. Which equation is this? (a) $V\,^\prime=k\sqrt V$ (b) $V\,^\prime=-k\sqrt V$ (c) $V\,^\prime=-kV$, with $k>0$.', 'choice', 'b',
          [r'"Decreases" fixes the sign; "proportional to $\sqrt V$" fixes the form.'],
          r'''Decreasing: the rate is negative; proportional to $\sqrt V$: $V'=-k\sqrt V$ with $k>0$ — **(b)**. (Torricelli's law for water flowing out of a hole.)''')
B.problem(S1, r'$y=Ce^{-t}+t-1$ solves $y\,^\prime=t-y$. Find $C$ such that $y(0)=2$.', 'num', 3,
          [r'Put $t=0$: $C+0-1=2$.'],
          r'''$y(0)=C\cdot1+0-1=C-1=2\Rightarrow C=$ **3**.

Check that it solves the ODE: $y'=-Ce^{-t}+1$ and $t-y=t-Ce^{-t}-t+1=1-Ce^{-t}$ ✓ — the line $y=t-1$ of the direction field figure is the case $C=0$.''')
B.md(r'''
### Separable equations
''')
B.problem(S2, r'Solve $\dfrac{dy}{dt}=-2ty$, $y(0)=5$. Give $y(1)$.', 'num', 5 * math.exp(-1),
          [r'Separate: $\frac{dy}{y}=-2t\,dt$.', r'$\ln y=-t^2+C$, so $y=Ae^{-t^2}$.'],
          r'''$\frac{dy}{y}=-2t\,dt\Rightarrow\ln|y|=-t^2+C\Rightarrow y=Ae^{-t^2}$. $y(0)=A=5$.

$y=5e^{-t^2}$ (a bell curve), $y(1)=5e^{-1}\approx$ **1.839**.''', fmt='a number; you can type `5*exp(-1)`')
B.problem(S2, r'Solve $\dfrac{dy}{dx}=\dfrac{2x}{y}$, $y(0)=2$ (with $y>0$). Give $y(2)$.', 'num', math.sqrt(12),
          [r'$y\,dy=2x\,dx$.', r'$\frac{y^2}{2}=x^2+C$; at $x=0$: $C=2$.'],
          r'''$y\,dy=2x\,dx\Rightarrow\frac{y^2}{2}=x^2+C$. At $x=0$, $y=2$: $C=2$. So $y^2=2x^2+4$, $y=\sqrt{2x^2+4}$.

$y(2)=\sqrt{12}\approx$ **3.464**.''', fmt='a number; you can type `sqrt(12)`')
B.problem(S2, r'Solve $\dfrac{dy}{dt}=e^{-y}$, $y(0)=0$. Give $y(e-1)$.', 'num', 1,
          [r'$e^y\,dy=dt$.', r'$e^y=t+C$ with $C=1$.'],
          r'''$e^y\,dy=dt\Rightarrow e^y=t+C$. At $t=0$: $1=C$. So $y=\ln(t+1)$, and $y(e-1)=\ln e=$ **1**.''')
B.problem(S2, r'Solve $\dfrac{dy}{dt}=1+y^2$, $y(0)=1$. At what time $t$ does the solution blow up?', 'num', math.pi / 4,
          [r'$\arctan y=t+C$; $C=\arctan1=\frac\pi4$.', r'$y=\tan(t+\frac\pi4)$ blows up when $t+\frac\pi4=\frac\pi2$.'],
          r'''$\int\frac{dy}{1+y^2}=\int dt\Rightarrow\arctan y=t+C$, $C=\arctan1=\frac\pi4$.

$y=\tan\left(t+\frac\pi4\right)$, which is infinite when $t+\frac\pi4=\frac\pi2$: at $t=\frac\pi4\approx$ **0.785**.''', fmt='a number; you can type `pi/4`')
B.md(r'''
### Growth, decay and cooling
''')
B.problem(S3, r'A population of 1000 grows according to $N\,^\prime=0.05N$ ($t$ in years). How many years until it reaches 3000?', 'num', math.log(3) / 0.05,
          [r'$N=1000e^{0.05t}$; solve $e^{0.05t}=3$.'],
          r'''$1000e^{0.05t}=3000\Rightarrow0.05t=\ln3\Rightarrow t=\frac{\ln3}{0.05}\approx$ **21.97 years**.''', fmt='years')
B.problem(S3, r'Carbon-14 has a half-life of 5730 years. A sample has 25 % of the original C-14. How old is it (years)?', 'num', 11460,
          [r'25 % is two halvings.'],
          r'''$25\%=\left(\frac12\right)^2$: two half-lives, **11 460 years**. (By the formula: $t=\frac{\ln4}{\ln2}\cdot5730$.)''', fmt='years')
B.problem(S3, r'Coffee at 90 °C is placed in a 20 °C room and is 60 °C after 10 min. What is its temperature after 30 min?', 'num', 20 + 70 * (40 / 70) ** 3,
          [r'$T=20+70e^{-kt}$; from the data $e^{-10k}=\frac{40}{70}$.', r'$e^{-30k}=\left(e^{-10k}\right)^3$.'],
          r'''$60=20+70e^{-10k}\Rightarrow e^{-10k}=\frac47$.

$T(30)=20+70\left(e^{-10k}\right)^3=20+70\cdot\frac{64}{343}\approx20+13.06=$ **33.1 °C**.

(No need to compute $k$: every 10 minutes the excess over room temperature is multiplied by $\frac47$.)''', fmt='°C')
B.problem(S3, r'A skydiver ($m=80$ kg) falls with linear drag $c=16$ kg/s. What is the terminal velocity (m/s), with $g=9.81$?', 'num', 80 * 9.81 / 16,
          [r'Terminal velocity: drag = weight, $cv=mg$.'],
          r'''$v_\infty=\frac{mg}{c}=\frac{80\cdot9.81}{16}\approx$ **49.05 m/s**.''', fmt='m/s')
B.problem(S3, r'For the same skydiver (starting from rest), after how many seconds is the speed 90 % of terminal velocity?', 'num', 80 / 16 * math.log(10),
          [r'$v=v_\infty(1-e^{-ct/m})$; set the bracket to 0.9.', r'$e^{-ct/m}=0.1$.'],
          r'''$1-e^{-ct/m}=0.9\Rightarrow e^{-ct/m}=0.1\Rightarrow t=\frac mc\ln10=5\cdot2.303\approx$ **11.5 s**.''', fmt='seconds')
B.md(r'''
### Logistic growth and equilibria
''')
B.problem(S4, r'$P\,^\prime=0.4P\left(1-\dfrac{P}{500}\right)$, $P(0)=50$. What is $P$ at the moment of fastest growth?', 'num', 250,
          [r'Fastest growth where $P\,^\prime$ is largest as a function of $P$.'],
          r'''$P'$ is a downward parabola in $P$ with zeros at 0 and 500; its maximum is halfway: $P=$ **250** $=\frac K2$.''')
B.problem(S4, r'For the same equation, find $P(10)$ from the logistic formula.', 'num', 500 / (1 + 9 * math.exp(-4)),
          [r'$P=\dfrac{K}{1+(K/P_0-1)e^{-rt}}$ with $K=500$, $P_0=50$, $r=0.4$.', r'$K/P_0-1=9$ and $e^{-4}=0.0183$.'],
          r'''$$P(10)=\frac{500}{1+9e^{-4}}=\frac{500}{1+0.1648}\approx429.2 .$$''')
B.problem(S4, r'$y\,^\prime=y^2-4y+3$. Find the **stable** equilibrium.', 'num', 1,
          [r'$y^2-4y+3=(y-1)(y-3)$.', r'$f\,^\prime(y)=2y-4$: check its sign at each equilibrium.'],
          r'''Equilibria: $(y-1)(y-3)=0$, $y=1$ or $y=3$. $f'(y)=2y-4$: $f'(1)=-2<0$ (stable), $f'(3)=2>0$ (unstable).

Stable equilibrium: **y = 1**.''')
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
1. Turn "a drug is removed from the blood at a rate proportional to its concentration" into an equation and solve it.
2. Why is "separate and integrate" justified? (Use the chain rule.)
3. Why is the half-life independent of the amount?
4. How do you find equilibria and their stability without solving the equation?
5. Sketch the direction field of $y'=y(2-y)$ and three solutions.

*Your answers:*

&nbsp;

### 3 · Physics strand — terminal velocity in the simulator (1 hour)
The projectile experiment includes air drag. Launch straight up is not possible, but a steep, fast throw with strong drag shows it: **predict first** what the vertical speed does on the way down — keep growing, or level off? At what value (use $v_\infty=\sqrt{g/k}$ for the lab's quadratic drag, shown in its Theory panel)?
''')
B.code(r'''
lab('physics', exp='proj', k=0.05, v0=40, ang=85)
''')
B.md(r'''
### 4 · What comes next
**Week 14** solves every *linear* first-order equation with one formula (the integrating factor), and applies it to the RC circuit — the electrical twin of the cooling coffee — including what happens when the input is a sine wave.
''')

if __name__ == '__main__':
    B.write()
