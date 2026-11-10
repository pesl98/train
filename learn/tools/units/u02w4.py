"""Unit 2 · Week 4 (course week 7) - Maxima and minima, optimisation, mean value theorem, L'Hopital."""
import math
from nbkit import Book
import figs_u02 as F

B = Book('u02w4', 'Unit 2 · Week 4 — Maxima, minima and optimisation', 'year1/u02w4-optimisation.ipynb')
S1, S2, S3, S4 = '1 Local extrema and concavity', '2 Global extrema', '3 Optimisation', '4 Mean value theorem and L’Hôpital'

B.md(r'''
# Unit 2 · Week 4 — Maxima, minima and optimisation
*Term 1, week 7 of 12 · about 15 hours in this notebook and on paper*

**Where you are.** You can differentiate anything. This last week of the unit answers the question derivatives were invented for: **where is a quantity largest or smallest?** The cheapest design, the strongest beam, the load that receives the most power, the launch angle of longest range — all are found by setting a derivative to zero. This week shows why that works, when it does not, and how to turn a word problem into a function to optimise.

**What you will be able to do at the end of this week**
1. Find and classify the stationary points of a function (first- and second-derivative tests) and explain *why* the derivative vanishes at an interior extremum.
2. Read concavity and inflection points from $f''$.
3. Find the largest and smallest values of a function on an interval.
4. Solve optimisation word problems with a fixed six-step method.
5. State the mean value theorem and use its consequences; evaluate $\frac00$ and $\frac\infty\infty$ limits with L'Hôpital's rule.

**What is used from earlier:** all differentiation rules (weeks 1–2); solving $f'(x)=0$; the intermediate-value idea and limits (Unit 1 week 3).

Run the grey *SETUP* cell first.
''')

# =====================================================================================
B.md(r'''
---
# Part 1 — Local extrema and the shape of a graph

## 1.1 The vocabulary

- $f$ has a **local maximum** at $a$ if $f(a)\ge f(x)$ for all $x$ *near* $a$ (a hill top). A **local minimum**: $f(a)\le f(x)$ near $a$ (a valley bottom). Together: **local extrema**.
- $f$ has a **global** (or *absolute*) **maximum** at $a$ if $f(a)\ge f(x)$ for *all* $x$ in the domain considered. Likewise global minimum.
- A **stationary point** is a point where $f'(a)=0$. A **critical point** is a point where $f'(a)=0$ **or** $f'(a)$ does not exist (a corner, for instance).
''')
B.fig('extrema', F.extrema, 'A local maximum, a local minimum and, between them, an inflection point.')
B.md(r'''
## 1.2 Why the derivative is zero at an extremum

**Theorem (Fermat).** If $f$ has a local maximum or minimum at an interior point $a$, and $f'(a)$ exists, then $f'(a)=0$.

**Why you should care about the proof.** "Set the derivative to zero" is the most used recipe in applied mathematics. The proof shows exactly what it does and does not promise.

**Proof (for a local maximum).** Near $a$ we have $f(a+h)\le f(a)$, so the numerator $f(a+h)-f(a)$ of the difference quotient is $\le0$ for all small $h$ of either sign.

- For $h>0$: $\;\dfrac{f(a+h)-f(a)}{h}=\dfrac{(\le0)}{(>0)}\le0$. So the right-hand limit is $\le0$.
- For $h<0$: $\;\dfrac{f(a+h)-f(a)}{h}=\dfrac{(\le0)}{(<0)}\ge0$. So the left-hand limit is $\ge0$.

$f'(a)$ exists, so both one-sided limits equal $f'(a)$. A number that is both $\le0$ and $\ge0$ is $0$. $\blacksquare$

*In pictures:* just left of a hill top the secants slope up, just right of it they slope down; the tangent at the top is squeezed between them and must be horizontal.

**What the theorem does NOT say.** It says: extremum ⇒ $f'=0$. It does **not** say: $f'=0$ ⇒ extremum.
Counter-example: $f(x)=x^3$ has $f'(0)=0$, but the graph rises on both sides — a flat spot, not an extremum.

So the stationary points are only the **candidates**. Each must be tested.

## 1.3 The first-derivative test

**Build.** Recall (week 1, §4.3): where $f'>0$ the function rises, where $f'<0$ it falls. (A proof of this "obvious" fact comes from the mean value theorem in Part 4.) So look at the **sign of $f'$ on each side** of a candidate $a$:

| sign of $f'$ left of $a$ | right of $a$ | $f$ does this | so at $a$ |
|---|---|---|---|
| $+$ | $-$ | rises, then falls | **local maximum** |
| $-$ | $+$ | falls, then rises | **local minimum** |
| same sign on both sides | | keeps rising (or falling) | **no extremum** |

**The procedure.**
1. Compute $f'$ and **factor** it.
2. Solve $f'(x)=0$ (and note where $f'$ does not exist): the candidates.
3. The candidates cut the number line into intervals. On each, $f'$ keeps one sign (it can only change sign at a candidate). Find that sign by testing **one** point in each interval — or by looking at the signs of the factors.
4. Read off the behaviour.

**Worked example 1.** $f(x)=x^3-3x$.
1. $f'(x)=3x^2-3=3(x-1)(x+1)$.
2. Candidates: $x=-1$ and $x=1$.
3. Sign chart:

| interval | $x<-1$ | $-1<x<1$ | $x>1$ |
|---|---|---|---|
| test point | $-2$ | $0$ | $2$ |
| $f'$ | $3(-3)(-1)=+9$ | $3(-1)(1)=-3$ | $3(1)(3)=+9$ |
| $f$ | rising | falling | rising |

4. At $x=-1$: $+$ to $-$, a **local maximum**, $f(-1)=2$. At $x=1$: $-$ to $+$, a **local minimum**, $f(1)=-2$.

**Worked example 2 (from your diagnostic).** $f(x)=x\,e^{-x}$.
1. $f'(x)=(1-x)\,e^{-x}$ (last week).
2. $e^{-x}>0$ always, so the only candidate is $x=1$, and the sign of $f'$ is the sign of $(1-x)$.
3. $x<1$: $f'>0$, rising. $x>1$: $f'<0$, falling.
4. **Local maximum** at $x=1$, value $f(1)=e^{-1}\approx0.368$. Since $f$ rises all the way up to it and falls ever after, it is also the global maximum.

**Worked example 3 — a candidate that is not an extremum.** $f(x)=x^4-4x^3$.
1. $f'(x)=4x^3-12x^2=4x^2(x-3)$.
2. Candidates: $x=0$ and $x=3$.
3. The factor $4x^2$ is never negative, so the sign of $f'$ is the sign of $(x-3)$: negative for $x<3$ (on **both** sides of $0$), positive for $x>3$.
4. At $x=0$: no sign change, **no extremum** (a flat spot on the way down). At $x=3$: $-$ to $+$, a **local minimum**, $f(3)=81-108=-27$.
''')
B.ask(r'''$f'(x)=(x-2)(x+5)$. At which $x$ does $f$ have a local **minimum**?''', 'num', 2,
      r'''Candidates $-5$ and $2$. Signs of $f'$: for $x<-5$ both factors are negative, product $+$; between, $-$; for $x>2$, $+$. At $x=2$ the sign goes from $-$ to $+$: falling then rising, a minimum. (At $-5$: $+$ to $-$, a maximum.)''',
      r'''Make a sign chart for $f'$ with the candidates $-5$ and $2$. A minimum is where $f'$ goes from negative to positive.''')
B.ask(r'''Find the $x$-coordinate of the local **maximum** of $f(x)=x^3-12x$.''', 'num', -2,
      r'''$f'(x)=3x^2-12=3(x-2)(x+2)$. Sign: $+$ for $x<-2$, $-$ between, $+$ for $x>2$. Maximum where $+\to-$: $x=-2$ (value $16$).''',
      r'''$f'(x)=3(x-2)(x+2)$. Which candidate has $f'$ changing from $+$ to $-$?''')

B.md(r'''
## 1.4 The second derivative: concavity

**Build.** $f''$ is the derivative of $f'$: it tells you whether the **slope** is increasing or decreasing.
''')
B.fig('concavity', F.concavity, 'Left: the tangents turn upwards as you move right. Right: they turn downwards.')
B.md(r'''
- $f''>0$: the slope increases; the graph bends upwards like a cup $\cup$. It is called **concave up**.
- $f''<0$: the slope decreases; the graph bends downwards like a cap $\cap$: **concave down**.
- A point where the concavity changes is an **inflection point**. Candidates: where $f''=0$ (and, as before, you must check that the sign of $f''$ really changes).

**In words, with motion:** $f'$ is the velocity and $f''$ the acceleration. "Sales are still rising, but more and more slowly" means $f'>0$ and $f''<0$. An inflection point is where growth turns from speeding up to slowing down.

**Worked example.** $f(x)=x^3-3x$: $f''(x)=6x$. Negative for $x<0$ (concave down), positive for $x>0$ (concave up). Inflection point at $x=0$ — see the figure in §1.1.

## 1.5 The second-derivative test

**Build.** At a stationary point the tangent is horizontal. If the graph is a cup there, the point is the bottom of the cup; if a cap, the top.

> Suppose $f'(a)=0$.
> - If $f''(a)>0$: **local minimum**.
> - If $f''(a)<0$: **local maximum**.
> - If $f''(a)=0$: **no conclusion** — use the first-derivative test.

*Why:* near $a$, $f(a+h)\approx f(a)+f'(a)h+\frac12f''(a)h^2$ (last week, §3.2). With $f'(a)=0$ that is $f(a)+\frac12f''(a)h^2$: a parabola, opening upwards if $f''(a)>0$.

**Worked example.** $f(x)=x^3-3x$, stationary points $x=\pm1$, $f''(x)=6x$.
$f''(-1)=-6<0$: local maximum ✓. $f''(1)=6>0$: local minimum ✓. (Same as the sign chart, with less work.)

**The inconclusive case is real.** $x^4$, $-x^4$ and $x^3$ all have $f'(0)=f''(0)=0$, and they have a minimum, a maximum and neither.

**Which test?** The second-derivative test is quicker when $f''$ is easy. The first-derivative test always works and also tells you the behaviour between the candidates.
''')
B.ask(r'''$f(x)=x^3-6x^2+5$. At which $x$ is the inflection point?''', 'num', 2,
      r'''$f'(x)=3x^2-12x$, $f''(x)=6x-12$, zero at $x=2$; negative before and positive after, so the concavity really changes.''',
      r'''Differentiate twice and solve $f''(x)=0$.''')
B.ask(r'''$f(x)=x^2+\dfrac{16}{x}$ for $x>0$ has a stationary point at $x=2$. Compute $f''(2)$.''', 'num', 6,
      r'''$f'(x)=2x-\dfrac{16}{x^2}$ (zero at $x=2$ ✓). $f''(x)=2+\dfrac{32}{x^3}$, so $f''(2)=2+4=6>0$: a local minimum.''',
      r'''$f'(x)=2x-16x^{-2}$. Differentiate once more: $2+32x^{-3}$.''')

B.md(r'''
### Experiment 1 — read a graph through its derivatives
The cell shows $f$, $f'$ and $f''$ for $f(x)=x^4-4x^3$ (worked example 3), with a movable point.

**Predict first:** at $x=0$, what are $f'$ and $f''$? Is it an extremum? Where is the graph concave down? Then move the slider through $x=0$, $2$ and $3$ and watch the signs.
''')
B.code(r'''
def f(u):   return u**4 - 4 * u**3
def f1(u):  return 4 * u**3 - 12 * u**2
def f2(u):  return 12 * u**2 - 24 * u

def inspect(a=1.0):
    xs = np.linspace(-1.2, 4.3, 400)
    fig, axs = plt.subplots(1, 3, figsize=(11, 3.4))
    for ax, g, name in zip(axs, (f, f1, f2), ("f", "f '", "f ''")):
        ax.plot(xs, g(xs)); ax.axhline(0, color='k', lw=0.8); ax.plot([a], [g(a)], 'ro'); ax.set_title(name); ax.set_ylim(-45, 60)
    m = f1(a); axs[0].plot([a - 0.7, a + 0.7], [f(a) - 0.7 * m, f(a) + 0.7 * m], 'r', lw=1.5)
    plt.show()
    shape = 'concave up (cup)' if f2(a) > 0 else ('concave down (cap)' if f2(a) < 0 else 'f\'\' = 0')
    trend = 'rising' if m > 0 else ('falling' if m < 0 else 'horizontal tangent')
    print(f"x = {a:.2f}:   f = {f(a):.3f}   f ' = {m:.3f} ({trend})   f '' = {f2(a):.3f} ({shape})")

explore(inspect, a=(-1, 4, 0.25, 1))
''')

# =====================================================================================
B.md(r'''
---
# Part 2 — The largest and smallest value on an interval

**Why.** In practice the variable is restricted: a length between 0 and 6 cm, an angle between $0$ and $90^\circ$. Then the extreme value may sit at an **end** of the interval, where the derivative is not zero at all.

**Theorem (extreme value theorem).** A function that is **continuous** on a **closed** interval $[a,b]$ has a largest and a smallest value there.

*(Like the intermediate value theorem, this rests on the fine structure of the real numbers; we use it without proof. Both conditions matter: $\frac1x$ on $(0,1]$ has no largest value — the interval is not closed at 0.)*

**Where can the extreme values be?** Either at an interior point — then, by Fermat's theorem, at a critical point — or at an end point. That gives a complete, mechanical method.

**The closed-interval method.**
1. Find the critical points of $f$ inside $(a,b)$.
2. Compute $f$ at those points **and at both end points**.
3. The largest of these numbers is the global maximum, the smallest the global minimum.

No sign charts, no second derivatives — just a short list of values to compare.

**Worked example.** $f(x)=x^3-3x$ on $[0,3]$.
1. $f'(x)=3(x-1)(x+1)=0$ at $x=\pm1$; only $x=1$ lies inside $(0,3)$.
2. Values: $f(0)=0$, $\;f(1)=-2$, $\;f(3)=27-9=18$.
3. Global minimum $-2$ at $x=1$; global maximum $18$ at the **end point** $x=3$.

The maximum is at a point where $f'(3)=24\ne0$. "Set the derivative to zero" alone would have missed it.
''')
B.ask(r'''What is the largest value of $f(x)=x^2-4x+1$ on the interval $[0,5]$?''', 'num', 6,
      r'''$f'(x)=2x-4=0$ at $x=2$. Values: $f(0)=1$, $f(2)=-3$, $f(5)=6$. Largest: $6$, at the end point $x=5$.''',
      r'''Candidates: the critical point $x=2$ and the end points $0$ and $5$. Compare the three values.''')

# =====================================================================================
B.md(r'''
---
# Part 3 — Optimisation

## 3.1 The method

**Why.** Real problems do not arrive as "maximise $f(x)=\ldots$". They arrive as words. Most of the work — and nearly all of the mistakes — lies in turning the words into a function of **one** variable.

**The six steps.**

1. **Sketch and name.** Draw the situation. Give letters to the quantities that can vary.
2. **Objective.** Write a formula for the quantity $Q$ to be maximised or minimised.
3. **Constraint.** If the formula has more than one variable, find the equation that links them (a fixed perimeter, a fixed volume, …) and use it to **eliminate** all but one.
4. **Domain.** Which values of the remaining variable make physical sense?
5. **Optimise.** Solve $Q'=0$; compare with the end points of the domain, or use a derivative test, to be sure it is the kind of extremum you want.
6. **Answer the question asked** (the dimensions? the maximum value?) with units, and check that it is plausible.

## 3.2 Worked example — the fence

*A farmer has 100 m of fencing for a rectangular field along a straight river; the river side needs no fence. Which dimensions give the largest area?*

1. **Sketch and name.** Let $x$ be the length of each of the two sides running away from the river and $y$ the side parallel to it.
2. **Objective.** Area $A=x\,y$.
3. **Constraint.** Fence used: $2x+y=100$, so $y=100-2x$. Then $A(x)=x(100-2x)=100x-2x^2$.
4. **Domain.** $x>0$ and $y=100-2x>0$: $\;0<x<50$. At both ends the area is $0$.
5. **Optimise.** $A'(x)=100-4x=0\Rightarrow x=25$. $A''=-4<0$: a maximum.
6. **Answer.** $x=25$ m, $y=50$ m, area $1250$ m². *Plausible:* the side along the river is twice the others — the river "pays for" one long side.

## 3.3 Worked example — the open box

*From a square sheet of 12 cm by 12 cm, a square of side $x$ is cut from each corner and the flaps are folded up to make an open box. Which $x$ gives the largest volume?*
''')
B.fig('box_fold', F.box_fold, 'Cutting corners of side x leaves a base of side 12 − 2x; the height is x.')
B.md(r'''
1. **Name.** $x$ = side of the cut-out squares = height of the box.
2. **Objective.** $V=\text{base}\times\text{height}=(12-2x)^2\,x$. Only one variable: no constraint needed.
3. —
4. **Domain.** $0<x<6$ (at $x=6$ nothing is left of the base). $V=0$ at both ends.
5. **Optimise.** Product rule, with the chain rule on the square:
$$\begin{aligned}
V'(x)&=\underbrace{2(12-2x)\cdot(-2)}_{\text{derivative of }(12-2x)^2}\cdot x+(12-2x)^2\cdot1\\
&=(12-2x)\big[-4x+(12-2x)\big] &&\text{(take out the common factor)}\\
&=(12-2x)(12-6x).
\end{aligned}$$
$V'=0$ at $x=6$ (the end of the domain, volume 0) or $x=2$. Since $V$ is $0$ at both ends and positive between, the interior stationary point $x=2$ must be the maximum.
6. **Answer.** Cut squares of **2 cm**. The box is $8\times8\times2$ cm, volume $128$ cm³.

### Experiment 2 — the box
**Predict first:** is the volume curve symmetric about its maximum? Roughly what is the volume for $x=1$? For $x=4$?
''')
B.code(r'''
def box(cut=1.0):
    xs = np.linspace(0, 6, 300)
    V = lambda u: (12 - 2 * u)**2 * u
    plt.figure(figsize=(7, 3.6))
    plt.plot(xs, V(xs)); plt.plot([cut], [V(cut)], 'ro'); plt.plot([2], [V(2)], 'g^', ms=9, label='maximum, x = 2')
    plt.xlabel('cut x (cm)'); plt.ylabel('volume (cm³)'); plt.legend(); plt.show()
    print(f'cut {cut:.2f} cm:  base {12 - 2 * cut:.2f} × {12 - 2 * cut:.2f} cm, height {cut:.2f} cm, volume {V(cut):.2f} cm³')

explore(box, cut=(0.25, 5.75, 0.25, 1))
''')
B.md(r'''
## 3.4 Worked example — the cheapest can

*A cylindrical can must hold 1 litre (1000 cm³). Which radius uses the least metal?*

1. **Name.** Radius $r$, height $h$ (cm).
2. **Objective.** Surface: top and bottom $2\pi r^2$, plus the side (a rectangle of width $2\pi r$ and height $h$): $\;S=2\pi r^2+2\pi rh$.
3. **Constraint.** Volume $\pi r^2h=1000$, so $h=\dfrac{1000}{\pi r^2}$. Then
$$S(r)=2\pi r^2+2\pi r\cdot\frac{1000}{\pi r^2}=2\pi r^2+\frac{2000}{r}.$$
4. **Domain.** $r>0$. As $r\to0$ the can becomes an infinitely tall needle ($S\to\infty$); as $r\to\infty$ an infinitely wide pancake ($S\to\infty$). So a minimum exists in between.
5. **Optimise.** $S'(r)=4\pi r-\dfrac{2000}{r^2}=0\ \Rightarrow\ 4\pi r^3=2000\ \Rightarrow\ r=\sqrt[3]{\dfrac{500}{\pi}}\approx5.42$ cm.
$S''(r)=4\pi+\dfrac{4000}{r^3}>0$: a minimum ✓.
6. **Answer.** $r\approx5.42$ cm, and $h=\dfrac{1000}{\pi r^2}\approx10.84$ cm. Notice $h=2r$: **the best can is as tall as it is wide.** (Real cans deviate from this because the top and bottom cost more and the seams waste material.)

## 3.5 Worked example — maximum power transfer

*A source of voltage $V$ with internal resistance $r$ drives a load resistor $R$. Which $R$ receives the most power?* This is a classic result of electrical engineering (matching a loudspeaker to an amplifier, an antenna to a receiver).
''')
B.fig('power_transfer', F.power_transfer, 'A real source: an ideal voltage V in series with an internal resistance r.')
B.md(r'''
1. **Name.** The load $R$ varies; $V$ and $r$ are fixed.
2. **Objective.** Current (Ohm's law, resistors in series): $I=\dfrac{V}{R+r}$. Power in the load:
$$P(R)=I^2R=\frac{V^2R}{(R+r)^2}.$$
4. **Domain.** $R>0$. For $R\to0$ (a short circuit) $P\to0$: plenty of current, but no voltage across the load. For $R\to\infty$ (open circuit) $P\to0$: plenty of voltage, no current. A maximum lies between.
5. **Optimise.** Quotient rule with $u=R$, $v=(R+r)^2$:
$$\frac{dP}{dR}=V^2\,\frac{1\cdot(R+r)^2-R\cdot2(R+r)}{(R+r)^4}=V^2\,\frac{(R+r)-2R}{(R+r)^3}=V^2\,\frac{r-R}{(R+r)^3}.$$
Zero exactly when $R=r$. Positive for $R<r$, negative for $R>r$: a maximum.
6. **Answer.** $\boxed{R=r}$: **the load should equal the internal resistance.** Then $P_{\max}=\dfrac{V^2r}{(2r)^2}=\dfrac{V^2}{4r}$.

*Worth noticing:* at the optimum, half of the total power is burnt inside the source — maximum power is not maximum efficiency.

### Experiment 3 — power against load
**Predict first:** for $V=12$ V and $r=4\ \Omega$, what is the maximum power? Is the curve symmetric about $R=r$? If you plot against $R$ on a logarithmic axis?
''')
B.code(r'''
def power(R=1.0, r=4.0, V=12.0):
    Rs = np.logspace(-1, 2.3, 300)
    P = lambda u: V**2 * u / (u + r)**2
    plt.figure(figsize=(7, 3.6))
    plt.semilogx(Rs, P(Rs)); plt.plot([R], [P(R)], 'ro'); plt.axvline(r, color='g', ls=':', label='R = r')
    plt.xlabel('load R (Ω), logarithmic scale'); plt.ylabel('power in the load (W)'); plt.legend(); plt.show()
    print(f'R = {R:.2f} Ω:  current {V / (R + r):.3f} A,  load power {P(R):.3f} W,  efficiency {100 * R / (R + r):.0f} %')

explore(power, R=(0.5, 40, 0.5, 1), r=(1, 10, 1, 4))
''')
B.md(r'''
## 3.6 Worked example — the best launch angle

*A ball is thrown from the ground with speed $v$ at an angle $\theta$ above the horizontal. Ignoring air resistance, which angle gives the longest range?*

1. **Motion.** The launch velocity has horizontal part $v\cos\theta$ and vertical part $v\sin\theta$ (Unit 1: adjacent and opposite). With gravity $g$ acting downwards only:
$$x(t)=v\cos\theta\cdot t,\qquad y(t)=v\sin\theta\cdot t-\tfrac12gt^2 .$$
2. **Landing.** $y=0$: $\;t\left(v\sin\theta-\tfrac12gt\right)=0$, so $t=\dfrac{2v\sin\theta}{g}$ (the other root, $t=0$, is the launch).
3. **Objective.** Range $=x$ at that time:
$$R(\theta)=v\cos\theta\cdot\frac{2v\sin\theta}{g}=\frac{v^2}{g}\cdot2\sin\theta\cos\theta=\frac{v^2}{g}\sin2\theta$$
(the double-angle formula from Unit 1 week 2).
4. **Domain.** $0\le\theta\le\frac\pi2$; the range is $0$ at both ends.
5. **Optimise.** $R'(\theta)=\dfrac{v^2}{g}\cdot2\cos2\theta=0\ \Rightarrow\ 2\theta=\dfrac\pi2\ \Rightarrow\ \theta=\dfrac\pi4$.
6. **Answer.** $45^\circ$, with range $\dfrac{v^2}{g}$. (Here calculus was not even needed: $\sin2\theta$ is at most 1, when $2\theta=90^\circ$.)

**And with air resistance?** Then there is no formula for the range — but there is a simulator. That is the lab task at the end of this notebook.
''')
B.ask(r'''A rectangle has perimeter $40$ m. What is the largest area it can have (m²)?''', 'num', 100,
      r'''Sides $x$ and $y$ with $2x+2y=40$, so $y=20-x$. $A=x(20-x)=20x-x^2$, $A'=20-2x=0$ at $x=10$. Then $y=10$: a square, area $100$ m².''',
      r'''Constraint: $2x+2y=40$. Eliminate $y$, then maximise $A(x)=x(20-x)$.''', fmt='m²')
B.ask(r'''For $x>0$, what is the smallest value of $x+\dfrac{9}{x}$?''', 'num', 6,
      r'''$f'(x)=1-\dfrac{9}{x^2}=0\Rightarrow x^2=9\Rightarrow x=3$ ($x>0$). $f(3)=3+3=6$. $f''(x)=\dfrac{18}{x^3}>0$: a minimum.''',
      r'''Differentiate: $1-9x^{-2}$. Set to zero, solve for positive $x$, then compute the *value*.''')

# =====================================================================================
B.md(r'''
---
# Part 4 — Two theorems that tidy things up

## 4.1 The mean value theorem

**Theorem (MVT).** If $f$ is continuous on $[a,b]$ and differentiable on $(a,b)$, then there is at least one point $c$ between $a$ and $b$ where
$$f'(c)=\frac{f(b)-f(a)}{b-a}.$$
In words: **somewhere, the instantaneous rate of change equals the average rate of change.** In pictures: somewhere the tangent is parallel to the secant.
''')
B.fig('mvt', F.mvt, 'Somewhere between a and b the tangent has the same slope as the secant.')
B.md(r'''
**An everyday version.** If you drive 150 km in 1.5 hours, your average speed is 100 km/h — so at some instant your speedometer showed exactly 100 km/h. (Average-speed cameras rely on this.)

**Why it is true (sketch).** Tilt the picture so that the secant becomes horizontal: consider $g(x)=f(x)-\big[\text{the secant line}\big]$. Then $g(a)=g(b)=0$. By the extreme value theorem $g$ has a maximum and a minimum on $[a,b]$. If both are at the end points, $g$ is constant ($=0$) and $g'=0$ everywhere. Otherwise one is at an interior point $c$, and by Fermat's theorem $g'(c)=0$. Either way $g'(c)=0$ for some $c$, which says $f'(c)$ equals the slope of the secant.

**Why it matters — three facts you have been using.** Each follows in one line.

1. **If $f'(x)>0$ on an interval, $f$ is increasing there.** Take any $x_1<x_2$ in the interval. By the MVT, $f(x_2)-f(x_1)=f'(c)\,(x_2-x_1)$, a product of two positive numbers. So $f(x_2)>f(x_1)$. (This is the proof promised in §1.3.)
2. **If $f'(x)=0$ on an interval, $f$ is constant there.** Same line: $f(x_2)-f(x_1)=0\cdot(x_2-x_1)=0$.
3. **If two functions have the same derivative on an interval, they differ by a constant.** Apply fact 2 to their difference: $(f-g)'=0$, so $f-g$ is constant.

Fact 3 looks innocent. It is the foundation of the next unit: it is the reason every antiderivative comes with "$+\,C$" and nothing more.
''')
B.ask(r'''For $f(x)=x^2$ on $[1,3]$: at which $c$ does the tangent have the same slope as the secant from $x=1$ to $x=3$?''', 'num', 2,
      r'''Secant slope: $\dfrac{9-1}{3-1}=4$. $f'(c)=2c=4\Rightarrow c=2$.''',
      r'''First the average slope $\dfrac{f(3)-f(1)}{3-1}$; then solve $f'(c)=$ that number.''')

B.md(r'''
## 4.2 L'Hôpital's rule

**Why.** In Unit 1 week 3 every $\frac00$ limit needed its own trick: factor, conjugate, a squeeze. With derivatives there is one rule that handles most of them.

**The rule.** If $f(a)=0$ and $g(a)=0$ (so that $\frac{f(x)}{g(x)}$ is of the form $\frac00$ at $a$), then
$$\lim_{x\to a}\frac{f(x)}{g(x)}=\lim_{x\to a}\frac{f'(x)}{g'(x)},$$
provided the limit on the right exists. The same holds for the form $\frac\infty\infty$, and for $x\to\infty$.

**Why it is true (the idea).** Near $a$, each function is nearly its tangent line, and both tangent lines pass through height $0$ at $a$:
$$f(x)\approx f'(a)\,(x-a),\qquad g(x)\approx g'(a)\,(x-a).$$
In the quotient the factor $(x-a)$ cancels:
$$\frac{f(x)}{g(x)}\approx\frac{f'(a)\,(x-a)}{g'(a)\,(x-a)}=\frac{f'(a)}{g'(a)}.$$
**The ratio of two quantities that both go to zero is the ratio of the rates at which they go there.**

**Worked examples.**

**(a)** $\displaystyle\lim_{x\to0}\frac{e^x-1}{x}$. Form $\frac00$. Differentiate top and bottom **separately**: $\dfrac{e^x}{1}\to1$.

**(b)** $\displaystyle\lim_{x\to1}\frac{\ln x}{x-1}$. Form $\frac00$. $\;\dfrac{1/x}{1}\to1$.

**(c)** $\displaystyle\lim_{x\to0}\frac{1-\cos x}{x^2}$. Form $\frac00$. First application: $\dfrac{\sin x}{2x}$ — still $\frac00$. Apply the rule again: $\dfrac{\cos x}{2}\to\dfrac12$. (The value found with much more effort in Unit 1.)

**(d) The form $\frac\infty\infty$.** $\displaystyle\lim_{x\to\infty}\frac{x}{e^x}$: $\;\dfrac{1}{e^x}\to0$. And $\displaystyle\lim_{x\to\infty}\frac{x^2}{e^x}$: twice, $\dfrac{2x}{e^x}$ then $\dfrac{2}{e^x}\to0$. In general, **$e^x$ grows faster than any power of $x$**. That is why $x\,e^{-x}=\dfrac{x}{e^x}\to0$ as $x\to\infty$: the graph of worked example 2 dies away.

**(e)** $\displaystyle\lim_{x\to\infty}\frac{\ln x}{x}$: $\;\dfrac{1/x}{1}\to0$. **The logarithm grows more slowly than any power.**

**Three warnings.**
1. **Check the form first.** The rule is only for $\frac00$ or $\frac\infty\infty$. Applied to $\lim_{x\to0}\frac{x+1}{x+2}$ (which is simply $\frac12$) it gives the wrong answer $1$.
2. **Differentiate top and bottom separately.** It is *not* the quotient rule.
3. A note on logic: using L'Hôpital on $\frac{\sin x}{x}$ gives $\frac{\cos x}{1}\to1$ — correct, but not a *proof* of that limit, because the derivative of $\sin$ was itself derived from it. It is a fine way to *remember* it.
''')
B.ask(r'''Compute $\displaystyle\lim_{x\to0}\frac{\sin3x}{2x}$ with L'Hôpital's rule.''', 'num', 1.5,
      r'''Form $\frac00$. Derivatives: $\dfrac{3\cos3x}{2}\to\dfrac32$.''',
      r'''Top: $3\cos3x$ (chain rule). Bottom: $2$. Then let $x\to0$.''')
B.ask(r'''Compute $\displaystyle\lim_{x\to\infty}\frac{3x^2+1}{e^x}$.''', 'num', 0,
      r'''$\frac\infty\infty$. Once: $\dfrac{6x}{e^x}$; twice: $\dfrac{6}{e^x}\to0$. Exponentials beat powers.''',
      r'''Apply the rule twice.''')

B.md(r'''
## 4.3 Putting it all together: sketching a graph

**Why.** You can always ask a computer to plot. But knowing *what the plot must look like* — and noticing when a computed plot is wrong, or misses a feature outside its window — is an engineering skill.

**Checklist.** (1) Domain. (2) Intercepts. (3) Behaviour at the ends ($x\to\pm\infty$, asymptotes). (4) $f'$: rising/falling, extrema. (5) $f''$: concavity, inflection points. (6) Sketch.

**Worked example.** $f(x)=x\,e^{-x}$.
1. **Domain:** all real $x$.
2. **Intercepts:** $f(0)=0$, and $f(x)=0$ only at $x=0$.
3. **Ends:** as $x\to\infty$, $\frac{x}{e^x}\to0$ (L'Hôpital): the $x$-axis is a horizontal asymptote. As $x\to-\infty$: $x$ is large negative and $e^{-x}$ is huge: $f\to-\infty$.
4. **$f'=(1-x)e^{-x}$:** rising for $x<1$, falling for $x>1$; maximum at $(1,\,e^{-1})\approx(1,\,0.37)$.
5. **$f''$:** product rule on $(1-x)e^{-x}$: $\;-e^{-x}+(1-x)(-e^{-x})=(x-2)\,e^{-x}$. Negative for $x<2$ (concave down), positive for $x>2$ (concave up). Inflection point at $(2,\,2e^{-2})\approx(2,\,0.27)$.
6. **Sketch:** comes up steeply from $-\infty$, passes through the origin, peaks at $x=1$, turns from cap to cup at $x=2$, and creeps down to the axis.

**Sketch it on paper from these six lines, then run the cell.**
''')
B.code(r'''
xs = np.linspace(-1, 7, 400)
plt.plot(xs, xs * np.exp(-xs))
plt.plot([1], [exp(-1)], 'ro', label='maximum (1, 1/e)'); plt.plot([2], [2 * exp(-2)], 'g^', label='inflection (2, 2/e²)')
plt.axhline(0, color='k', lw=0.8); plt.ylim(-1, 0.6); plt.legend(); plt.show()
''')

B.md(r'''
## Week summary — everything on one page

**Finding extrema.**
- Interior extremum ⇒ $f'=0$ (or $f'$ undefined). **Not** the other way round: test every candidate.
- First-derivative test: $f'$ from $+$ to $-$: max; $-$ to $+$: min; no change: neither.
- Second-derivative test: $f'(a)=0$ and $f''(a)>0$: min; $<0$: max; $=0$: no conclusion.
- $f''>0$: concave up; $f''<0$: concave down; sign change of $f''$: inflection point.
- On $[a,b]$: compare $f$ at the critical points **and at the end points**.

**Optimisation.** Sketch and name → objective → constraint (eliminate to one variable) → domain → $Q'=0$ and check → answer the question.

**Results worth remembering.** Rectangle of given perimeter: the square. Best closed can: $h=2r$. Maximum power transfer: $R=r$, $P_{\max}=\frac{V^2}{4r}$. Longest range without drag: $45^\circ$, $\frac{v^2}{g}$.

**Mean value theorem.** $f'(c)=\dfrac{f(b)-f(a)}{b-a}$ for some $c$. Hence: $f'>0$ ⇒ increasing; $f'=0$ ⇒ constant; equal derivatives ⇒ functions differ by a constant.

**L'Hôpital.** For $\frac00$ or $\frac\infty\infty$: $\lim\frac fg=\lim\frac{f'}{g'}$. Exponentials beat powers; powers beat logarithms.
''')

# =====================================================================================
B.md(r'''
---
# Problems

Paper first. First attempt counts. `hint(n)` → `solution(n)` → `mistake(n, '...')`.

### Local extrema and concavity
''')
B.problem(S1, r'Find all stationary points of $f(x)=x^4-8x^2$. Give the three $x$-values.', 'set', [-2, 0, 2],
          [r"$f'(x)=4x^3-16x$. Factor it completely."],
          r'''$f'(x)=4x^3-16x=4x(x^2-4)=4x(x-2)(x+2)$.

Zero at $x=-2,\ 0,\ 2$.

(Sign chart: $-,+,-,+$. So minima at $x=\pm2$ with $f=-16$, and a local maximum at $x=0$ with $f=0$.)''', fmt='a list, e.g. `[-1, 0, 1]`')
B.problem(S1, r'At which $x$ does $f(x)=x^3-3x^2-9x+2$ have its local **minimum**?', 'num', 3,
          [r"$f'(x)=3x^2-6x-9=3(x^2-2x-3)$. Factor.", r"$f'(x)=3(x-3)(x+1)$. Use $f''$ or a sign chart to decide which candidate is the minimum."],
          r'''$f'(x)=3x^2-6x-9=3(x-3)(x+1)$: candidates $x=-1$ and $x=3$.

$f''(x)=6x-6$: $f''(-1)=-12<0$ (local maximum), $f''(3)=12>0$ (local **minimum**).

Answer: $x=$ **3** (where $f(3)=27-27-27+2=-25$).''')
B.problem(S1, r'What is the **maximum value** of $f(x)=x\,e^{-x}$? *(From your diagnostic.)*', 'num', math.exp(-1),
          [r"$f'(x)=(1-x)e^{-x}$.", r'The maximum is at $x=1$. The question asks for the value $f(1)$.'],
          r'''$f'(x)=(1-x)e^{-x}=0$ at $x=1$; rising before, falling after: a maximum.

$f(1)=1\cdot e^{-1}=\dfrac1e\approx$ **0.368**.''', fmt='a number; you can type `exp(-1)`')
B.problem(S1, r'$f(x)=x^2\ln x$ for $x>0$ has exactly one stationary point. Find its $x$-coordinate.', 'num', math.exp(-0.5),
          [r"Product rule: $f'(x)=2x\ln x+x^2\cdot\frac1x$.", r"$f'(x)=x(2\ln x+1)$. Since $x>0$, solve $2\ln x+1=0$."],
          r'''$f'(x)=2x\ln x+x=x\,(2\ln x+1)$.

For $x>0$: $2\ln x+1=0\Rightarrow\ln x=-\frac12\Rightarrow x=e^{-1/2}\approx$ **0.607**.

$f''(x)=2\ln x+2+1=2\ln x+3$; at $e^{-1/2}$ it is $-1+3=2>0$: a minimum.''', fmt='a number; you can type `exp(-1/2)`')
B.problem(S1, r'At which $x$ does $f(x)=x^4-6x^2$ change from concave up to concave down? (Give the negative one of its two inflection points.)', 'num', -1,
          [r"$f''(x)=12x^2-12$."],
          r'''$f'(x)=4x^3-12x$, $f''(x)=12x^2-12=12(x-1)(x+1)$.

$f''>0$ for $x<-1$, $f''<0$ for $-1<x<1$, $f''>0$ for $x>1$. Inflection points at $x=\pm1$; the change from up to down is at $x=$ **−1**.''')
B.md(r'''
### Global extrema
''')
B.problem(S2, r'Find the smallest and the largest value of $f(x)=x^3-3x$ on $[0,2]$. Give `(min, max)`.', 'tuple', [-2, 2],
          [r'Candidates: critical points inside $(0,2)$, and the end points $0$ and $2$.', r'$f(0)=0$, $f(1)=-2$, $f(2)=2$.'],
          r'''$f'(x)=3(x-1)(x+1)$; inside $(0,2)$ only $x=1$.

$f(0)=0,\quad f(1)=-2,\quad f(2)=8-6=2$.

Minimum **−2** (at $x=1$), maximum **2** (at the end point $x=2$).''', fmt='a tuple `(min, max)`')
B.problem(S2, r'What is the largest value of $f(x)=2x^3-9x^2+12x$ on $[0,3]$?', 'num', 9,
          [r"$f'(x)=6x^2-18x+12=6(x-1)(x-2)$.", r'Compare $f(0)$, $f(1)$, $f(2)$, $f(3)$.'],
          r'''$f'(x)=6(x-1)(x-2)$: critical points $1$ and $2$, both inside.

$f(0)=0,\quad f(1)=5,\quad f(2)=16-36+24=4,\quad f(3)=54-81+36=9$.

Largest: **9**, at the end point $x=3$ — larger than the local maximum $5$.''')
B.md(r'''
### Optimisation
''')
B.problem(S3, r'A farmer has $80$ m of fencing for a rectangular field along a river (no fence on the river side). What is the largest possible area (m²)?', 'num', 800,
          [r'Sides: two of length $x$, one of length $y$, with $2x+y=80$.', r'$A(x)=x(80-2x)$.'],
          r'''$y=80-2x$, $A(x)=x(80-2x)=80x-2x^2$, $A'(x)=80-4x=0\Rightarrow x=20$.

$y=40$, area $20\cdot40=$ **800 m²**. ($A''=-4<0$: a maximum.)''', fmt='m²')
B.problem(S3, r'From a square sheet of $30$ cm by $30$ cm, squares of side $x$ are cut from the corners and the sides folded up. What is the largest possible volume of the box (cm³)?', 'num', 2000,
          [r'$V(x)=x(30-2x)^2$ for $0<x<15$.', r"$V'(x)=(30-2x)(30-6x)$."],
          r'''$V(x)=x(30-2x)^2$.

$V'(x)=(30-2x)^2+x\cdot2(30-2x)(-2)=(30-2x)(30-2x-4x)=(30-2x)(30-6x)$.

Zero at $x=15$ (volume 0) and $x=5$.

$V(5)=5\cdot20^2=$ **2000 cm³**.''', fmt='cm³')
B.problem(S3, r'A closed cylindrical can must hold $500$ cm³. Which **radius** (cm) minimises the surface area?', 'num', (250 / math.pi) ** (1 / 3),
          [r'$S=2\pi r^2+2\pi rh$ with $\pi r^2h=500$, so $S(r)=2\pi r^2+\dfrac{1000}{r}$.', r"$S'(r)=4\pi r-\dfrac{1000}{r^2}=0\Rightarrow r^3=\dfrac{250}{\pi}$."],
          r'''$h=\dfrac{500}{\pi r^2}$, so $S(r)=2\pi r^2+2\pi r\cdot\dfrac{500}{\pi r^2}=2\pi r^2+\dfrac{1000}{r}$.

$S'(r)=4\pi r-\dfrac{1000}{r^2}=0\Rightarrow r^3=\dfrac{250}{\pi}\Rightarrow r=\sqrt[3]{\dfrac{250}{\pi}}\approx$ **4.30 cm**.

Then $h=\dfrac{500}{\pi r^2}\approx8.60$ cm $=2r$, as always for the best closed can.''', fmt='cm; you can type `(250/pi)**(1/3)`')
B.problem(S3, r'A battery of $12$ V with internal resistance $4\ \Omega$ drives a load resistor. What is the **maximum power** (W) the load can receive?', 'num', 9,
          [r'Maximum power transfer: $R=r$.', r'$P_{\max}=\dfrac{V^2}{4r}$.'],
          r'''The load power $P=\dfrac{V^2R}{(R+r)^2}$ is greatest for $R=r=4\ \Omega$.

$I=\dfrac{12}{8}=1.5$ A, $P=I^2R=2.25\cdot4=$ **9 W** $\left(=\dfrac{V^2}{4r}=\dfrac{144}{16}\right)$.''', fmt='watts')
B.problem(S3, r'Which point on the curve $y=\sqrt{x}$ is closest to the point $(3,0)$? Give its $x$-coordinate.', 'num', 2.5,
          [r'Minimise the **square** of the distance — same minimiser, no root: $D(x)=(x-3)^2+(\sqrt{x})^2$.', r"$D(x)=(x-3)^2+x$, $D'(x)=2(x-3)+1$."],
          r'''Distance squared from $(x,\sqrt{x})$ to $(3,0)$: $D(x)=(x-3)^2+x$.

$D'(x)=2(x-3)+1=2x-5=0\Rightarrow x=$ **2.5**. ($D''=2>0$: a minimum.)

*Trick to remember:* minimising a distance is the same as minimising its square, which avoids differentiating a square root.''')
B.problem(S3, r'A ball is thrown at $20$ m/s. Ignoring air resistance and taking $g=10$ m/s², what is the greatest horizontal range (m)?', 'num', 40,
          [r'$R(\theta)=\dfrac{v^2}{g}\sin2\theta$.'],
          r'''$R(\theta)=\dfrac{v^2}{g}\sin2\theta$ is greatest when $\sin2\theta=1$, i.e. $\theta=45^\circ$:
$$R_{\max}=\frac{v^2}{g}=\frac{400}{10}=40\ \text{m}.$$''', fmt='metres')
B.md(r'''
### Mean value theorem and L'Hôpital
''')
B.problem(S4, r'For $f(x)=x^3$ on $[0,3]$, find the point $c$ in $(0,3)$ promised by the mean value theorem.', 'num', math.sqrt(3),
          [r'Average slope: $\dfrac{27-0}{3-0}=9$.', r'Solve $3c^2=9$ for positive $c$.'],
          r'''Average slope $=\dfrac{f(3)-f(0)}{3}=9$.

$f'(c)=3c^2=9\Rightarrow c=\sqrt3\approx$ **1.732**.''', fmt='a number; you can type `sqrt(3)`')
B.problem(S4, r'$\displaystyle\lim_{x\to0}\frac{e^x-1-x}{x^2}$', 'num', 0.5,
          [r"Form $\frac00$. Apply L'Hôpital; check the form again.", r'After one step: $\dfrac{e^x-1}{2x}$, still $\frac00$. Once more.'],
          r'''$\frac00$. First: $\dfrac{e^x-1}{2x}$ — still $\frac00$. Second: $\dfrac{e^x}{2}\to$ **1/2**.

(So $e^x\approx1+x+\frac12x^2$ for small $x$: the next term after the linear approximation. Unit 4 continues the pattern.)''')
B.problem(S4, r'$\displaystyle\lim_{x\to0}\frac{\sin x-x}{x^3}$', 'num', -1 / 6,
          [r"Apply L'Hôpital repeatedly, checking for $\frac00$ each time.", r'$\dfrac{\cos x-1}{3x^2}\to\dfrac{-\sin x}{6x}\to\dfrac{-\cos x}{6}$.'],
          r'''$$\frac{\sin x-x}{x^3}\ \to\ \frac{\cos x-1}{3x^2}\ \to\ \frac{-\sin x}{6x}\ \to\ \frac{-\cos x}{6}\ \xrightarrow[x\to0]{}\ -\frac16 .$$
(Each step was $\frac00$.) So $\sin x\approx x-\dfrac{x^3}{6}$: the first correction to the small-angle approximation.''', fmt='a number, e.g. `-1/6`')
B.problem(S4, r'$\displaystyle\lim_{x\to\infty}x^2e^{-x}$', 'num', 0,
          [r'Write it as $\dfrac{x^2}{e^x}$: the form $\frac\infty\infty$.'],
          r'''$x^2e^{-x}=\dfrac{x^2}{e^x}\ \to\ \dfrac{2x}{e^x}\ \to\ \dfrac{2}{e^x}\ \to\ $ **0**.

Exponential growth beats every power.''')
B.code(r'''
# scratch cell
''')

B.md(r'''
---
# Finish the week — and the unit

### 1 · Report
''')
B.code(r'''
report()
''')
B.md(r'''
### 2 · Teach-back (30 minutes, from memory)
1. Why must $f'(a)=0$ at an interior maximum? (Give the argument with the signs of the difference quotient.)
2. Give an example where $f'(a)=0$ but there is no extremum.
3. The six steps of an optimisation problem.
4. Derive the maximum-power-transfer result $R=r$.
5. Why do two functions with the same derivative differ only by a constant?

*Your answers:*

&nbsp;

### 3 · Physics strand — the best launch angle *with* air resistance (1 hour)
Without drag the best angle is $45^\circ$ and the range is $\frac{v^2}{g}$ (§3.6). With drag there is no formula. Optimise **experimentally**, as an engineer would.

The simulator starts with drag $k=0.01$ and $v_0=25$ m/s. **Predict first:** will the best angle be above or below $45^\circ$? Why? Then measure the range for $30^\circ,35^\circ,40^\circ,45^\circ,50^\circ$ (press *Reset* after changing the angle; the range is shown when the ball lands), plot your five points on paper, and estimate the optimum. Repeat with $k=0.03$.
''')
B.code(r'''
lab('physics', exp='proj', k=0.01, v0=25, ang=45)
''')
B.md(r'''
*Explain:* drag slows the ball most where it is fastest and for as long as it is in the air. A flatter throw spends less time in the air, so the best angle is **below** $45^\circ$, the more so the stronger the drag.

### 4 · Unit 2 review
Run `report()` in all four notebooks of this unit, or look at the course map.

- Every week at ≥ 80 % first time → **Unit 3 (integrals)** starts.
- Otherwise redo the missed problems on a different day. Typical weak spots to tell your tutor about: forgetting the inner derivative in the chain rule; sign errors in the quotient rule; putting numbers in before differentiating (related rates); forgetting end points (global extrema).

**What comes next.** Differentiation takes a function and returns its rate of change. Unit 3 runs the film backwards: given the rate of change, recover the function — and discovers that this is the same problem as finding the area under a curve.
''')

if __name__ == '__main__':
    B.write()
