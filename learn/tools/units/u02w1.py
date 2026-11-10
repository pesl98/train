"""Unit 2 · Week 1 (course week 4) - The derivative from first principles."""
import math
from nbkit import Book
import figs_u02 as F

B = Book('u02w1', 'Unit 2 · Week 1 — The derivative from first principles', 'year1/u02w1-derivative-definition.ipynb')
S1, S2, S3, S4 = '1 The definition', '2 Power rule and linearity', '3 Meaning and use', '4 Existence and numerics'

B.md(r'''
# Unit 2 · Week 1 — The derivative from first principles
*Term 1, week 4 of 12 · about 15 hours in this notebook and on paper*

**Where you are.** In Unit 1 you learned what a limit is and computed the speed of a falling ball at one instant. That calculation *was* a derivative. This unit turns it into a general tool. Your diagnostic showed that derivatives are the weakest area (2 out of 6), so the unit takes four weeks and assumes nothing: every rule you may once have memorised is **derived here from the definition**.

**The plan for Unit 2**

| week | content |
|---|---|
| **1 (this notebook)** | what a derivative is; the definition; powers and polynomials; what it means |
| 2 | sine, cosine, exponential, logarithm; product, quotient and chain rules |
| 3 | implicit differentiation, related rates, linear approximation, Newton's method |
| 4 | maxima and minima, optimisation, curve sketching |

**What you will be able to do at the end of this week**
1. Explain the derivative as a limit of average rates of change, and as the slope of a tangent.
2. Compute a derivative directly from the definition (four steps).
3. **Prove** the power rule for whole-number powers; use it, with linearity, to differentiate any polynomial and any sum of powers.
4. Find tangent lines, velocities and accelerations; approximate a function near a point by its tangent.
5. Say where a function has no derivative, and compute a derivative numerically the way a simulator does.

**What is used from Unit 1:** limits and the "$\frac00$" techniques — expand, common denominator, conjugate (week 3, §2.2); function notation $f(a+h)$ (week 1, §1.1).

Run the grey *SETUP* cell first.
''')

# =====================================================================================
B.md(r'''
---
# Part 1 — Rates of change

## 1.1 The slope of a straight line

**Why.** The derivative is "the slope of a curve at a point". Before a curve, be completely sure what slope means for a line.

**Build.**

**Step 1 — definition.** Take two points on a line. The **run** is the horizontal change $\Delta x=x_2-x_1$, the **rise** is the vertical change $\Delta y=y_2-y_1$. ($\Delta$, "delta", means *change in*.) The slope is
$$m=\frac{\Delta y}{\Delta x}=\frac{y_2-y_1}{x_2-x_1}.$$
''')
B.fig('slope_line', F.slope_line, 'Slope = rise ÷ run.')
B.md(r'''
**Step 2 — it does not matter which two points you take.** Any two "staircase triangles" under the same line have the same angles, so they are scaled copies of each other (the argument of Unit 1, week 1, §3.1), and the ratio rise ÷ run is the same for all of them. *A line has one slope.* That is what makes it a line.

**Step 3 — what the number means.** A slope of $0.75$ says: **for every 1 unit you move right, $y$ goes up by $0.75$**. Slope is a *rate*: "units of $y$ per unit of $x$". If $x$ is time in seconds and $y$ is distance in metres, the slope is a speed in m/s. Positive slope: rising. Negative: falling. Zero: horizontal.

**Step 4 — the line through a given point with a given slope.** If a line passes through $(x_0,y_0)$ with slope $m$, then for any other point $(x,y)$ on it, $\dfrac{y-y_0}{x-x_0}=m$. Multiply by $(x-x_0)$:
$$\boxed{\,y=y_0+m\,(x-x_0)\,}$$
In words: *start at height $y_0$; for every unit you move away from $x_0$, add $m$.* You will use this formula all week for tangent lines.

**Worked example.** The line through $(2,5)$ with slope $-3$: $\;y=5-3(x-2)=11-3x$. Check: at $x=2$, $y=11-6=5$ ✓.
''')
B.ask(r'''A line passes through $(1,2)$ and $(4,11)$. What is its slope?''', 'num', 3,
      r'''$m=\dfrac{\Delta y}{\Delta x}=\dfrac{11-2}{4-1}=\dfrac93=3$.''',
      r'''Rise over run: $\dfrac{y_2-y_1}{x_2-x_1}$.''')

B.md(r'''
## 1.2 The average rate of change of a curve

**Build.** A curve has no single slope: it is steeper in some places than in others. But between two points on it we can still compute rise over run:

$$\text{average rate of change of $f$ from $a$ to $b$}=\frac{f(b)-f(a)}{b-a}.$$

Geometrically this is the slope of the straight line through the two points of the graph. Such a line is called a **secant** (Latin for "cutting").

**Worked example.** A ball falls $s(t)=5t^2$ metres in $t$ seconds. Between $t=1$ and $t=3$:
$$\frac{s(3)-s(1)}{3-1}=\frac{45-5}{2}=20\ \text{m/s}.$$
That is its *average* speed over those two seconds. Between $t=1$ and $t=2$ it is $\frac{20-5}{1}=15$ m/s. The answer depends on the interval — an average rate says nothing precise about any single moment.

## 1.3 From average to instantaneous

In Unit 1 (week 3, §1.1) you shrank the interval: the average speed from $t=1$ to $t=1+h$ came out as $10+5h$, and as $h\to0$ it tended to $10$ m/s. That limit is the speed *at* $t=1$.

Nothing in that calculation was special to falling balls. Do it for any function and any point, and you have the derivative.
''')
B.ask(r'''For $f(x)=x^2$, what is the average rate of change from $x=1$ to $x=4$?''', 'num', 5,
      r'''$\dfrac{f(4)-f(1)}{4-1}=\dfrac{16-1}{3}=5$. It is the slope of the secant through $(1,1)$ and $(4,16)$.''',
      r'''$\dfrac{f(b)-f(a)}{b-a}$ with $a=1$, $b=4$.''')

# =====================================================================================
B.md(r'''
---
# Part 2 — The definition of the derivative

## 2.1 The derivative at a point

**Build.**

**Step 1 — set up.** Fix a point $a$. Move a small step $h$ away, to $a+h$. On the graph these are the points $P=(a,f(a))$ and $Q=(a+h,f(a+h))$.
''')
B.fig('diff_quotient', F.diff_quotient, 'The run is h; the rise is f(a+h) − f(a).')
B.md(r'''
**Step 2 — the average rate over that step.** Run: $(a+h)-a=h$. Rise: $f(a+h)-f(a)$. So
$$\text{slope of the secant }PQ=\frac{f(a+h)-f(a)}{h}.$$
This expression is called the **difference quotient** (a quotient of two differences).

**Step 3 — let the step shrink.** As $h\to0$, the point $Q$ slides along the curve towards $P$, and the secant swings round towards one limiting position.
''')
B.fig('secant_tangent', F.secant_tangent, 'As h shrinks, the secants turn towards the tangent.')
B.md(r'''
**Step 4 — the definition.**

$$\boxed{\,f'(a)=\lim_{h\to0}\frac{f(a+h)-f(a)}{h}\,}$$

If this limit exists, it is called the **derivative of $f$ at $a$**, read "$f$ prime of $a$", and $f$ is said to be **differentiable** at $a$.

**Three ways to read the same number $f'(a)$:**

| reading | meaning |
|---|---|
| geometric | the **slope of the tangent line** to the graph at $x=a$. (The tangent is *defined* as the line through $P$ with this slope.) |
| physical | the **instantaneous rate of change** of $f$ at $a$: velocity if $f$ is position, current if $f$ is charge, … |
| "magnification" | near $a$, a small change in the input is multiplied by about $f'(a)$: $\ \Delta f\approx f'(a)\,\Delta x$ |

**Why we cannot just put $h=0$:** that gives $\frac{f(a)-f(a)}{0}=\frac00$. The derivative is *always* a $\frac00$ limit. All the work is in rewriting the difference quotient until the $h$ in the denominator cancels — exactly the techniques of Unit 1, week 3.

**The four-step recipe.**

1. Write down $f(a+h)$ — put $(a+h)$ in every box.
2. Subtract $f(a)$.
3. Divide by $h$ and **simplify until the $h$ in the denominator has cancelled**.
4. Let $h\to0$.

**Worked example 1.** $f(x)=x^2$ at $a=3$.

1. $f(3+h)=(3+h)^2=9+6h+h^2$.
2. $f(3+h)-f(3)=9+6h+h^2-9=6h+h^2$.
3. $\dfrac{6h+h^2}{h}=6+h$.
4. As $h\to0$: $\;f'(3)=6$.

The parabola $y=x^2$ has slope $6$ at the point $(3,9)$.

**Worked example 2.** $f(x)=x^2-4x$ at $a=1$.

1. $f(1+h)=(1+h)^2-4(1+h)=1+2h+h^2-4-4h=h^2-2h-3$.
2. $f(1)=1-4=-3$. Difference: $h^2-2h-3-(-3)=h^2-2h$.
3. $\dfrac{h^2-2h}{h}=h-2$.
4. $f'(1)=-2$. The graph is falling there, at 2 units down per unit across.

*Checkpoint for every such calculation:* after step 2, **every term without an $h$ must have cancelled**. If a term without $h$ survives, you made a slip in step 1 or forgot to subtract all of $f(a)$.
''')
B.ask(r'''Use the four steps to find $f'(2)$ for $f(x)=x^2$.''', 'num', 4,
      r'''(1) $(2+h)^2=4+4h+h^2$. (2) minus $4$: $4h+h^2$. (3) divide by $h$: $4+h$. (4) $h\to0$: $4$.''',
      r'''Step 1: expand $(2+h)^2$. Step 2: subtract $f(2)=4$. Then divide by $h$.''')
B.ask(r'''Use the four steps to find $f'(1)$ for $f(x)=3x^2+2$.''', 'num', 6,
      r'''(1) $3(1+h)^2+2=3+6h+3h^2+2$. (2) minus $f(1)=5$: $6h+3h^2$. (3) $6+3h$. (4) $6$. Notice the constant $+2$ cancelled in step 2: adding a constant does not change a slope.''',
      r'''$f(1+h)=3(1+h)^2+2$. Expand, subtract $f(1)=5$, divide by $h$.''')

B.md(r'''
## 2.2 The tangent line

**Build.** The tangent at $x=a$ is the line through the point $(a,f(a))$ with slope $f'(a)$. Put that into the line formula of §1.1 ($x_0=a$, $y_0=f(a)$, $m=f'(a)$):

$$\boxed{\,y=f(a)+f'(a)\,(x-a)\,}$$

**Worked example.** Tangent to $y=x^2$ at $x=3$. We have $f(3)=9$ and $f'(3)=6$:
$$y=9+6(x-3)=6x-9 .$$
Check: at $x=3$ the line gives $18-9=9$ ✓ (it passes through the point), and its slope is $6$ ✓.

### Experiment 1 — watch the secant become the tangent
The cell draws $f(x)=x^2$, the fixed point at $a=1$, and the secant to the point at $a+h$.

**Predict first:** what number will the secant slope approach as $h\to0$? What will it be for $h=1$, for $h=0.5$? What happens for *negative* $h$?
''')
B.code(r'''
def f(u):
    return u**2                      # try also:  u**3 / 4    or    np.sin(u)

def secant(h=1.5, a=1.0):
    xs = np.linspace(-1, 3.5, 300)
    m = (f(a + h) - f(a)) / h        # the difference quotient
    plt.figure(figsize=(7, 4.2))
    plt.plot(xs, f(xs), 'k', lw=2.2, label='y = f(x)')
    plt.plot(xs, f(a) + m * (xs - a), 'r', lw=1.5, label=f'secant, slope {m:.4f}')
    plt.plot([a, a + h], [f(a), f(a + h)], 'ro')
    plt.axhline(0, color='k', lw=0.8); plt.ylim(-2, 10); plt.legend(loc='upper left'); plt.show()
    print(f'h = {h:+.3f}     difference quotient = {m:.6f}')

explore(secant, h=(-1.5, 2, 0.05, 1.5), a=(0, 2, 0.5, 1))
''')
B.md(r'''
*Explain:* for $f(x)=x^2$ at $a=1$ the difference quotient is exactly $2+h$ (do the four steps!). It tends to $2$ from above for positive $h$ and from below for negative $h$: both one-sided limits agree, as a limit requires. (The slider cannot be exactly $0$ — there the quotient is $\frac00$.)

## 2.3 The derivative as a function

**Why.** Computing $f'(3)$, then $f'(2)$, then $f'(1)$ separately is wasteful. Do the four steps **once, with a letter $x$ instead of the number**, and you get a formula for the slope at *every* point.

**Build.** For $f(x)=x^2$, at a general point $x$:

1. $f(x+h)=(x+h)^2=x^2+2xh+h^2$.
2. $f(x+h)-f(x)=2xh+h^2$.
3. $\dfrac{2xh+h^2}{h}=2x+h$.
4. $h\to0$: $\;f'(x)=2x$.

So the slope of the parabola at any $x$ is $2x$. Check against what we found: $f'(3)=6$ ✓, $f'(2)=4$ ✓, $f'(1)=2$ ✓. During the limit, $x$ is held fixed; only $h$ moves.

**The derivative is a new function**, $f'$, made from $f$: its value at each $x$ is the slope of $f$ there.

$$f'(x)=\lim_{h\to0}\frac{f(x+h)-f(x)}{h}$$

**Notation.** There are several notations for the same thing; you must read all of them.

| notation | read | used when |
|---|---|---|
| $f'(x)$ | "$f$ prime of $x$" | the function has a name |
| $\dfrac{dy}{dx}$ | "d$y$ by d$x$" | $y=f(x)$; shows *what* is differentiated with respect to *what* |
| $\dfrac{d}{dx}\big[x^2\big]=2x$ | "the derivative of $x^2$ with respect to $x$" | applied to a formula |
| $\dot s$ | "$s$ dot" | derivative with respect to **time** (physics) |

**What $\dfrac{dy}{dx}$ means.** It is the limit of $\dfrac{\Delta y}{\Delta x}$ as $\Delta x\to0$ — where $\Delta x$ is what we called $h$, and $\Delta y=f(x+h)-f(x)$. It is **not** a fraction of two numbers $dy$ and $dx$; it is one symbol for one limit. But it was designed to *remind* you of rise over run, and it carries the units of one: if $y$ is in metres and $x$ in seconds, $\frac{dy}{dx}$ is in m/s.

To indicate the value at a particular point: $f'(3)$, or $\left.\dfrac{dy}{dx}\right|_{x=3}$.

**Reading a derivative from a graph.**
''')
B.fig('f_and_fprime', F.f_and_fprime, 'Top: a function. Bottom: its derivative — the slope of the top graph at each x.')
B.md(r'''
- Where $f$ is **rising**, the slope is positive: $f'>0$.
- Where $f$ is **falling**: $f'<0$.
- Where $f$ has a **horizontal tangent** (top of a hill, bottom of a valley): $f'=0$.
- The **steeper** $f$, the larger $|f'|$.

### Experiment 2 — draw the derivative by sliding along the curve
Move the slider. Left: the curve with its tangent at the red point. Right: the slope of that tangent, plotted against $x$ — the graph of $f'$ appears as you go.

**Predict first:** sketch on paper what the right-hand graph will look like for $f(x)=x^3-3x$. Where will it cross zero? Where is it lowest?
''')
B.code(r'''
def g(u):
    return u**3 - 3*u                # try also:  np.sin(u)   or   u**2

def slope_at(u, h=1e-5):
    return (g(u + h) - g(u - h)) / (2 * h)       # a numerical slope; Part 6 explains this formula

def tracker(a=-2.0):
    xs = np.linspace(-2.2, 2.2, 300)
    fig, (a1, a2) = plt.subplots(1, 2, figsize=(10.5, 3.8))
    m = slope_at(a)
    a1.plot(xs, g(xs), 'k', lw=2); a1.plot([a - 0.6, a + 0.6], [g(a) - 0.6 * m, g(a) + 0.6 * m], 'r', lw=2); a1.plot([a], [g(a)], 'ro')
    a1.axhline(0, color='k', lw=0.8); a1.set_title('f and its tangent'); a1.set_ylim(-5, 5)
    done = xs[xs <= a]
    a2.plot(done, slope_at(done), 'r', lw=2); a2.plot([a], [m], 'ro'); a2.axhline(0, color='k', lw=0.8)
    a2.set_xlim(-2.2, 2.2); a2.set_ylim(-4, 12); a2.set_title("the slope, plotted: f '")
    plt.show(); print(f'x = {a:.2f}    slope = {m:.3f}')

explore(tracker, a=(-2.2, 2.2, 0.1, -2.0))
''')
B.ask(r'''Do the four steps with a general $x$ for $f(x)=5x^2$. What is $f'(x)$?''', 'sym', '10*x',
      r'''(1) $5(x+h)^2=5x^2+10xh+5h^2$. (2) minus $5x^2$: $10xh+5h^2$. (3) $10x+5h$. (4) $10x$. The factor 5 simply came along: five times the function, five times the slope.''',
      r'''$f(x+h)=5(x+h)^2=5x^2+10xh+5h^2$. Subtract $5x^2$, divide by $h$, let $h\to0$.''', fmt="a formula in `x` as text, e.g. `'6*x'`")

# =====================================================================================
B.md(r'''
---
# Part 3 — Derivatives from the definition, and the power rule

**Why.** We now run the four steps on the basic functions. Each uses one of the $\frac00$ techniques from Unit 1 week 3. Then a pattern appears, and we prove it.

## 3.1 Constants and straight lines

**A constant, $f(x)=c$.** $\;\dfrac{f(x+h)-f(x)}{h}=\dfrac{c-c}{h}=0$, so $f'(x)=0$.
*Makes sense:* a horizontal line has slope 0; a quantity that does not change has rate of change 0.

**A line, $f(x)=mx+b$.** $\;\dfrac{m(x+h)+b-(mx+b)}{h}=\dfrac{mh}{h}=m$, so $f'(x)=m$.
*Makes sense:* the slope of a line is its slope, everywhere. In particular $\dfrac{d}{dx}[x]=1$.

## 3.2 $x^3$ — technique: expand

First the expansion (you will reuse it): $(x+h)^3=(x+h)^2(x+h)=(x^2+2xh+h^2)(x+h)=x^3+3x^2h+3xh^2+h^3$.

1. $f(x+h)=x^3+3x^2h+3xh^2+h^3$.
2. Subtract $x^3$: $\;3x^2h+3xh^2+h^3$.
3. Divide by $h$: $\;3x^2+3xh+h^2$.
4. $h\to0$: the last two terms vanish. $\;\dfrac{d}{dx}\big[x^3\big]=3x^2$.

## 3.3 $\dfrac1x$ — technique: common denominator

$$\begin{aligned}
\frac{f(x+h)-f(x)}{h}&=\frac1h\left(\frac{1}{x+h}-\frac1x\right)\\[3pt]
&=\frac1h\cdot\frac{x-(x+h)}{x\,(x+h)} &&\text{(common denominator $x(x+h)$)}\\[3pt]
&=\frac1h\cdot\frac{-h}{x\,(x+h)} &&\text{(the $x$'s cancel in the numerator)}\\[3pt]
&=\frac{-1}{x\,(x+h)} &&\text{(cancel $h$)}\\[3pt]
&\xrightarrow[h\to0]{}\ -\frac{1}{x^2}.
\end{aligned}$$
$$\frac{d}{dx}\left[\frac1x\right]=-\frac{1}{x^2}.$$
*Makes sense:* the graph of $\frac1x$ falls everywhere (negative slope), very steeply near $0$ and hardly at all for large $x$.

## 3.4 $\sqrt{x}$ — technique: conjugate

$$\begin{aligned}
\frac{\sqrt{x+h}-\sqrt{x}}{h}&=\frac{\sqrt{x+h}-\sqrt{x}}{h}\cdot\frac{\sqrt{x+h}+\sqrt{x}}{\sqrt{x+h}+\sqrt{x}}\\[3pt]
&=\frac{(x+h)-x}{h\,(\sqrt{x+h}+\sqrt{x})} &&\text{($(p-q)(p+q)=p^2-q^2$)}\\[3pt]
&=\frac{1}{\sqrt{x+h}+\sqrt{x}} &&\text{(the top is $h$; cancel)}\\[3pt]
&\xrightarrow[h\to0]{}\ \frac{1}{2\sqrt{x}}.
\end{aligned}$$
$$\frac{d}{dx}\big[\sqrt{x}\big]=\frac{1}{2\sqrt{x}}.$$

## 3.5 The pattern — the power rule

Collect the results, writing everything as a power of $x$ (recall $\frac1x=x^{-1}$ and $\sqrt{x}=x^{1/2}$):

| $f(x)$ | $f'(x)$ | as powers |
|---|---|---|
| $x^1$ | $1$ | $1\cdot x^0$ |
| $x^2$ | $2x$ | $2\cdot x^1$ |
| $x^3$ | $3x^2$ | $3\cdot x^2$ |
| $x^{-1}$ | $-\dfrac{1}{x^2}$ | $-1\cdot x^{-2}$ |
| $x^{1/2}$ | $\dfrac{1}{2\sqrt{x}}$ | $\frac12\cdot x^{-1/2}$ |

In every row: **the power comes down in front as a factor, and the power is reduced by 1.**

$$\boxed{\,\frac{d}{dx}\big[x^n\big]=n\,x^{n-1}\,}\qquad\textbf{the power rule}$$

**Proof for $n=1,2,3,\dots$** We need $(x+h)^n$, but only its first two terms. Write it as $n$ brackets:
$$(x+h)^n=\underbrace{(x+h)(x+h)\cdots(x+h)}_{n\text{ brackets}}.$$
To multiply out, you pick either $x$ or $h$ from each bracket, multiply your picks, and add up all the possible ways of picking.

- Pick $x$ from **every** bracket: one way, giving $x^n$.
- Pick $h$ from **exactly one** bracket and $x$ from the other $n-1$: the product is $x^{n-1}h$, and there are $n$ ways to choose which bracket supplies the $h$. Total: $n\,x^{n-1}h$.
- Pick $h$ from **two or more** brackets: every such product contains at least $h^2$.

Therefore
$$(x+h)^n=x^n+n\,x^{n-1}h+h^2\cdot(\text{other terms}).$$
(Check with $n=3$: $x^3+3x^2h+h^2(3x+h)$ ✓.) Now the four steps:
$$\frac{(x+h)^n-x^n}{h}=\frac{n\,x^{n-1}h+h^2\cdot(\ldots)}{h}=n\,x^{n-1}+h\cdot(\ldots)\ \xrightarrow[h\to0]{}\ n\,x^{n-1}.\qquad\blacksquare$$

**Other powers.** The table shows the same rule working for $n=-1$ and $n=\frac12$, which we computed directly. In fact it holds for **every real power $n$**. The general proof needs the chain rule and logarithms and comes next week (§ "the general power rule"); from now on you may use the rule for any power.

**Using the power rule: rewrite as a power first.**

| function | as a power | derivative | tidied |
|---|---|---|---|
| $x^7$ | $x^7$ | $7x^6$ | |
| $\dfrac{1}{x^3}$ | $x^{-3}$ | $-3x^{-4}$ | $-\dfrac{3}{x^4}$ |
| $\sqrt{x}$ | $x^{1/2}$ | $\frac12x^{-1/2}$ | $\dfrac{1}{2\sqrt{x}}$ |
| $\dfrac{1}{\sqrt{x}}$ | $x^{-1/2}$ | $-\frac12x^{-3/2}$ | $-\dfrac{1}{2x\sqrt{x}}$ |
| $\sqrt[3]{x^2}$ | $x^{2/3}$ | $\frac23x^{-1/3}$ | $\dfrac{2}{3\sqrt[3]{x}}$ |

Reminders: $\dfrac{1}{x^n}=x^{-n}$, $\ \sqrt[q]{x^p}=x^{p/q}$, and "reduce the power by 1" for $-3$ gives $-4$ (more negative), for $\frac12$ gives $-\frac12$.
''')
B.ask(r'''Differentiate $f(x)=x^{10}$.''', 'sym', '10*x**9',
      r'''Power down in front, power reduced by 1: $10x^9$.''',
      r'''$\dfrac{d}{dx}[x^n]=n\,x^{n-1}$ with $n=10$.''', fmt="a formula in `x` as text, e.g. `'4*x**3'`")
B.ask(r'''Differentiate $f(x)=\dfrac{1}{x^2}$.''', 'sym', '-2/x**3',
      r'''Rewrite: $x^{-2}$. Power rule: $-2x^{-3}=-\dfrac{2}{x^3}$. (Reducing $-2$ by one gives $-3$.)''',
      r'''First write $\dfrac{1}{x^2}$ as $x^{-2}$, then apply the power rule with $n=-2$.''', fmt="a formula in `x` as text, e.g. `'-3/x**4'`")

B.md(r'''
## 3.6 Linearity: constants and sums

**Why.** A polynomial is a sum of constants times powers. Two small rules reduce it to the power rule.

**Rule 1 — a constant factor comes out.** $\;\dfrac{d}{dx}\big[c\,f(x)\big]=c\,f'(x)$.

*Proof.* $\;\dfrac{c\,f(x+h)-c\,f(x)}{h}=c\cdot\dfrac{f(x+h)-f(x)}{h}\ \to\ c\,f'(x)$, by the limit law for a constant factor. $\blacksquare$

*In pictures:* stretching a graph vertically by $c$ makes every slope $c$ times steeper.

**Rule 2 — a sum is differentiated term by term.** $\;\dfrac{d}{dx}\big[f(x)+g(x)\big]=f'(x)+g'(x)$.

*Proof.* Regroup the difference quotient:
$$\frac{[f(x+h)+g(x+h)]-[f(x)+g(x)]}{h}=\frac{f(x+h)-f(x)}{h}+\frac{g(x+h)-g(x)}{h}\ \to\ f'(x)+g'(x),$$
by the limit law for sums. $\blacksquare$ The same holds for differences.

Together these two rules are called **linearity**.

**Worked example 1.** $f(x)=4x^3-5x^2+7x-2$.
$$f'(x)=4\cdot3x^2-5\cdot2x+7\cdot1-0=12x^2-10x+7 .$$

**Worked example 2.** $f(x)=3\sqrt{x}-\dfrac{2}{x^2}$. Rewrite: $3x^{1/2}-2x^{-2}$.
$$f'(x)=3\cdot\tfrac12x^{-1/2}-2\cdot(-2)x^{-3}=\frac{3}{2\sqrt{x}}+\frac{4}{x^3}.$$

**Worked example 3 — tidy first.** $f(x)=(x^2+1)^2$. There is no rule (yet) for a bracket to a power, so expand: $x^4+2x^2+1$. Then $f'(x)=4x^3+4x$.

**Worked example 4 — tidy first.** $f(x)=\dfrac{x^3-4x}{x}$. Divide each term by $x$: $x^2-4$. Then $f'(x)=2x$.

> **Warning: there is NO such rule for products or quotients.** The derivative of a product is *not* the product of the derivatives. Test: $x\cdot x=x^2$ has derivative $2x$, but the product of the derivatives is $1\cdot1=1$. The correct product, quotient and chain rules are next week's work. Until then: multiply out or divide out first, as in examples 3 and 4.
''')
B.ask(r'''Differentiate $f(x)=2x^4-3x^2+5x-9$.''', 'sym', '8*x**3 - 6*x + 5',
      r'''Term by term: $2\cdot4x^3-3\cdot2x+5-0=8x^3-6x+5$.''',
      r'''Apply the power rule to each term and keep the constant factors. The derivative of the constant $-9$ is $0$.''', fmt="a formula in `x` as text")
B.ask(r'''Differentiate $f(x)=6\sqrt{x}$ and give the value $f'(9)$.''', 'num', 1,
      r'''$6x^{1/2}\ \to\ 6\cdot\frac12x^{-1/2}=\dfrac{3}{\sqrt{x}}$. At $x=9$: $\dfrac33=1$.''',
      r'''$\sqrt{x}=x^{1/2}$, so the derivative is $6\cdot\frac12x^{-1/2}=\dfrac{3}{\sqrt{x}}$. Now put $x=9$.''')

# =====================================================================================
B.md(r'''
---
# Part 4 — What the derivative tells you

## 4.1 Motion: position, velocity, acceleration

**Build.** Let $s(t)$ be the position of an object at time $t$.

- **Velocity** is the rate of change of position: $\;v(t)=\dfrac{ds}{dt}=s'(t)$. Units: m/s. Its sign gives the direction.
- **Acceleration** is the rate of change of velocity: $\;a(t)=\dfrac{dv}{dt}=v'(t)$. Units: (m/s) per second, m/s².

Acceleration is the derivative *of the derivative* of position: the **second derivative**, written
$$a=s''(t)=\frac{d^2s}{dt^2}.$$
(The notation $\frac{d^2s}{dt^2}$ is $\frac{d}{dt}\!\left[\frac{d}{dt}s\right]$ written compactly.)

**Worked example.** A ball is thrown straight up at 20 m/s. With $g\approx10$ m/s², its height is
$$s(t)=20t-5t^2 .$$

1. Velocity: $v(t)=s'(t)=20-10t$.
2. Acceleration: $a(t)=v'(t)=-10$ m/s². Constant, and negative: gravity pulls down the whole time — even on the way up, even at the top.
3. **When is it highest?** At the top it is, for an instant, neither rising nor falling: $v=0$. Solve $20-10t=0$: $t=2$ s.
4. **How high?** $s(2)=40-20=20$ m.
5. **How fast does it land?** It lands when $s=0$: $20t-5t^2=5t(4-t)=0$, so $t=4$ s (the other root, $t=0$, is the launch). $v(4)=20-40=-20$ m/s: the same speed as the launch, downwards.

Step 3 contains an idea you will use throughout the unit: **at a highest or lowest point, the derivative is zero.**

### Experiment 3 — a simulation that only knows about small steps
A simulator does not know the formula $s=20t-5t^2$. It knows only the rules "*velocity is the rate of change of position, acceleration is the rate of change of velocity*", and applies them over tiny time steps $\Delta t$:
$$v\leftarrow v+a\,\Delta t,\qquad s\leftarrow s+v\,\Delta t .$$
This is the linear-approximation idea $\Delta s\approx s'\,\Delta t$, used thousands of times in a row. (Every lab in this course works this way; the method is called *Euler's method* and you will study its accuracy in Unit 5.)

**Predict first:** will the simulated height agree with the formula? Better or worse with a larger time step?
''')
B.code(r'''
def throw(v0=20.0, dt=0.1):
    a = -10.0
    ts, ss, vs = [0.0], [0.0], [v0]
    while ss[-1] >= 0 and ts[-1] < 10:
        v_new = vs[-1] + a * dt              # velocity changes at the rate a
        s_new = ss[-1] + vs[-1] * dt         # position changes at the rate v
        ts.append(ts[-1] + dt); vs.append(v_new); ss.append(s_new)
    ts = np.array(ts)
    fig, (a1, a2) = plt.subplots(1, 2, figsize=(10.5, 3.6))
    a1.plot(ts, ss, 'o-', ms=3, label='simulated, step by step'); a1.plot(ts, v0 * ts - 5 * ts**2, 'k--', label='formula 20t − 5t²' if v0 == 20 else 'formula')
    a1.set_xlabel('t (s)'); a1.set_ylabel('height s (m)'); a1.legend(fontsize=9)
    a2.plot(ts, vs, 'r'); a2.axhline(0, color='k', lw=0.8); a2.set_xlabel('t (s)'); a2.set_ylabel('velocity v (m/s)')
    plt.show()
    print(f'highest simulated point: {max(ss):.3f} m     exact: {v0**2 / 20:.3f} m')

explore(throw, v0=(5, 30, 5, 20), dt=(0.01, 0.5, 0.01, 0.1))
''')
B.md(r'''
*Explain:* with a small step the simulation follows the formula closely; with a large step it drifts, because over a long step the velocity is *not* constant, and the simulation pretends it is. The velocity graph is a straight line of slope $-10$: its slope is the acceleration. And the height is greatest exactly where the velocity crosses zero.
''')
B.ask(r'''A stone is thrown up with $s(t)=30t-5t^2$ (metres, seconds). What is its velocity at $t=1$?''', 'num', 20,
      r'''$v(t)=s'(t)=30-10t$, so $v(1)=20$ m/s (still rising).''',
      r'''Differentiate $s(t)$ to get $v(t)$, then put $t=1$.''', fmt='m/s')

B.md(r'''
## 4.2 The tangent line as an approximation

**Why.** Engineers constantly replace a complicated function by a straight line that is "good enough nearby": small-signal models of transistors, the small-angle pendulum, error estimates. The derivative says exactly which line.

**Build.** Zoom in on a smooth curve at a point. The more you zoom, the straighter it looks — and the line it turns into is the tangent.
''')
B.fig('tangent_zoom', F.tangent_zoom, 'The same curve and tangent in three windows. Close enough, they cannot be told apart.')
B.md(r'''
This is just the definition read backwards. For small $h$ the difference quotient is close to its limit:
$$\frac{f(a+h)-f(a)}{h}\approx f'(a)\qquad\Longrightarrow\qquad\boxed{\,f(a+h)\approx f(a)+f'(a)\,h\,}$$
"**new value ≈ old value + slope × step**". It is called the **linear approximation** of $f$ near $a$. The right-hand side is the tangent line (§2.2) evaluated at $x=a+h$.

**Worked example 1.** Estimate $\sqrt{4.1}$ without a calculator.
- Choose a nearby point where everything is easy: $a=4$, so $h=0.1$.
- $f(x)=\sqrt{x}$: $f(4)=2$. $\;f'(x)=\dfrac{1}{2\sqrt{x}}$: $f'(4)=\dfrac14$.
- $\sqrt{4.1}\approx2+\dfrac14\cdot0.1=2.025$. (True value: $2.02485\ldots$ — an error of $0.00015$.)

**Worked example 2.** Estimate $(1.02)^3$. $f(x)=x^3$, $a=1$, $h=0.02$: $f(1)=1$, $f'(1)=3$. So $(1.02)^3\approx1+3\cdot0.02=1.06$. (True: $1.061208$.)

**A general fact hiding here.** For small $h$: $(1+h)^n\approx1+nh$. A 2 % change in $x$ gives about a $2n$ % change in $x^n$. (A 1 % error in measuring a radius is a 2 % error in the area $\pi r^2$ and a 3 % error in the volume $\frac43\pi r^3$.)
''')
B.ask(r'''Use the linear approximation at $a=9$ to estimate $\sqrt{9.6}$.''', 'num', 3.1,
      r'''$f(9)=3$, $f'(9)=\dfrac{1}{2\cdot3}=\dfrac16$, $h=0.6$: $\;3+\dfrac16\cdot0.6=3.1$. (True value $3.0984$.)''',
      r'''$f(a+h)\approx f(a)+f'(a)h$ with $f=\sqrt{x}$, $a=9$, $h=0.6$, $f'(x)=\dfrac{1}{2\sqrt{x}}$.''')

B.md(r'''
## 4.3 Rising, falling, and flat

**Build.** From §2.3: $f'>0$ where $f$ rises, $f'<0$ where it falls, $f'=0$ where the tangent is horizontal. Points with $f'(x)=0$ are called **stationary points**; they are the candidates for highest and lowest points.

**Worked example.** Where is the tangent to $f(x)=x^3-3x$ horizontal, and where is $f$ rising?
1. $f'(x)=3x^2-3$.
2. Horizontal tangent: $3x^2-3=0\Rightarrow x^2=1\Rightarrow x=\pm1$.
3. Sign of $f'$: test a point in each region. $f'(-2)=9>0$ (rising for $x<-1$), $f'(0)=-3<0$ (falling between), $f'(2)=9>0$ (rising for $x>1$).

That matches the figure in §2.3: a hill top at $x=-1$, a valley at $x=1$. Week 4 of this unit develops this into a method for finding maxima and minima.
''')
B.ask(r'''At which $x$ does $f(x)=x^2-6x+1$ have a horizontal tangent?''', 'num', 3,
      r'''$f'(x)=2x-6=0\Rightarrow x=3$. (Completing the square agrees: $(x-3)^2-8$ has its lowest point at $x=3$.)''',
      r'''Horizontal tangent means $f'(x)=0$. Differentiate and solve.''')

# =====================================================================================
B.md(r'''
---
# Part 5 — When there is no derivative

**Why.** The derivative is a limit, and limits can fail to exist. You should recognise on sight where a function has no slope.

## 5.1 Differentiable implies continuous

**Theorem.** If $f$ is differentiable at $a$, then $f$ is continuous at $a$.

**Proof.** We must show $f(a+h)\to f(a)$ as $h\to0$, i.e. that the difference $f(a+h)-f(a)$ tends to $0$. Multiply and divide by $h$:
$$f(a+h)-f(a)=\frac{f(a+h)-f(a)}{h}\cdot h\ \xrightarrow[h\to0]{}\ f'(a)\cdot0=0 .\qquad\blacksquare$$

So a function with a **jump or a hole has no derivative there**. The converse is false: a function can be continuous and still have no derivative.

## 5.2 Corners and vertical tangents
''')
B.fig('not_differentiable', F.not_differentiable, 'Three ways to fail to have a derivative at 0.')
B.md(r'''
**A corner: $f(x)=|x|$ at $0$.** The difference quotient at $0$ is $\dfrac{|0+h|-|0|}{h}=\dfrac{|h|}{h}$.
- For $h>0$ it equals $\frac hh=1$. Right-hand limit: $1$.
- For $h<0$ it equals $\frac{-h}{h}=-1$. Left-hand limit: $-1$.

The two sides disagree, so the limit — the derivative — **does not exist**. Geometrically: the slope is $-1$ just left of the corner and $+1$ just right of it; at the corner there is no single tangent line.

**A vertical tangent: $f(x)=\sqrt[3]{x}=x^{1/3}$ at $0$.** The power rule gives $f'(x)=\frac13x^{-2/3}=\dfrac{1}{3\sqrt[3]{x^2}}$, which blows up as $x\to0$. The tangent at $0$ is vertical, and a vertical line has no slope.

**Summary: no derivative at** a discontinuity, a corner, or a vertical tangent. Everywhere else, the functions of this course are differentiable.
''')
B.ask(r'''For $f(x)=|x-3|$, what is the **right-hand** limit of the difference quotient at $x=3$, $\ \lim_{h\to0^+}\dfrac{f(3+h)-f(3)}{h}$?''', 'num', 1,
      r'''$f(3+h)=|h|$ and $f(3)=0$, so the quotient is $\dfrac{|h|}{h}=1$ for $h>0$. (From the left it is $-1$: a corner at $x=3$, no derivative there.)''',
      r'''$f(3+h)=|3+h-3|=|h|$. For positive $h$, $|h|=h$.''')

# =====================================================================================
B.md(r'''
---
# Part 6 — Numerical derivatives: how a computer does it

**Why.** A simulator, or an engineer with measured data, has values of a function but no formula. The derivative must be computed from the numbers.

**Build.**

**Method 1 — the forward difference.** Use the definition without taking the limit: pick a small $h$ and compute
$$f'(x)\approx\frac{f(x+h)-f(x)}{h}.$$
The error is roughly proportional to $h$. (For $x^2$ the quotient is $2x+h$: the error is exactly $h$.)

**Method 2 — the central difference.** Step both ways and divide by the total run $2h$:
$$f'(x)\approx\frac{f(x+h)-f(x-h)}{2h}.$$
This is the slope of the secant from $x-h$ to $x+h$, which is usually much more nearly parallel to the tangent. For $f(x)=x^2$:
$$\frac{(x+h)^2-(x-h)^2}{2h}=\frac{4xh}{2h}=2x\quad\text{— exact, for any $h$.}$$
In general its error is roughly proportional to $h^2$: ten times smaller $h$, a hundred times smaller error.

**So why not take $h=10^{-15}$?** Because of **cancellation** (Unit 1 week 3, Experiment 2): for a very small $h$, $f(x+h)$ and $f(x-h)$ agree in almost all their 16 stored digits, and their difference keeps only the last few, which are rounding noise. Dividing by a tiny $h$ then magnifies the noise. Two errors compete:

| | cause | behaves like |
|---|---|---|
| truncation error | not taking the limit | shrinks as $h\to0$ |
| rounding error | cancellation | **grows** as $h\to0$ |

There is a best, moderate $h$. The experiment finds it.

### Experiment 4 — write a numerical derivative, and find the best step
First complete the function: replace the `...` by the central-difference formula. The tests tell you whether it is right.
''')
B.code(r'''
def deriv(f, x0, h=1e-5):
    """Numerical derivative of f at x0 by the central difference."""
    return ...


# ---------- tests: do not change ----------
def test_deriv():
    cases = [('x³ at 2', lambda v: v**3, 2.0, 12.0), ('sin at 0', sin, 0.0, 1.0), ('√x at 4', sqrt, 4.0, 0.25), ('1/x at 2', lambda v: 1 / v, 2.0, -0.25)]
    good = 0
    for name, f, x0, true in cases:
        try:
            r = float(deriv(f, x0))
        except Exception as err:
            print('✗', name, '-> not working yet (have you replaced the ... ?)'); continue
        ok = abs(r - true) < 1e-6; good += ok
        print('✓' if ok else '✗', name, '->', r, '   exact:', true)
    print('\nAll tests passed.' if good == len(cases) else '\nNot there yet: the formula is (f(x0 + h) - f(x0 - h)) / (2 * h).')

test_deriv()
''', ref=r'''
def deriv(f, x0, h=1e-5):
    return (f(x0 + h) - f(x0 - h)) / (2 * h)
print(deriv(lambda v: v**3, 2.0))
''')
B.md(r'''
Now compare the two methods over a huge range of step sizes, for $f(x)=\sin x$ at $x=1$, where the exact derivative is $\cos1$ (you will prove that next week).

**Predict first:** which $h$ gives the smallest error for the forward difference — the smallest $h$ in the table? And for the central difference?
''')
B.code(r'''
x0, exact = 1.0, cos(1.0)
rows = []
for k in range(1, 15):
    hh = 10.0 ** (-k)
    fwd = (sin(x0 + hh) - sin(x0)) / hh
    ctr = (sin(x0 + hh) - sin(x0 - hh)) / (2 * hh)
    rows.append([hh, abs(fwd - exact), abs(ctr - exact)])
table(['h', 'error, forward difference', 'error, central difference'], rows, fmt='%.2e')

hs = np.array([r[0] for r in rows])
plt.loglog(hs, [r[1] for r in rows], 'o-', label='forward: error ~ h')
plt.loglog(hs, [max(r[2], 1e-17) for r in rows], 's-', label='central: error ~ h²')
plt.xlabel('step h'); plt.ylabel('error'); plt.legend(); plt.gca().invert_xaxis(); plt.show()
''')
B.md(r'''
*Explain:* reading the plot from left to right ($h$ getting smaller), both errors first fall — the forward one by a factor 10 per step, the central one by a factor 100 — and then **rise again** when rounding takes over. The forward difference is best near $h\approx10^{-8}$, the central difference near $h\approx10^{-5}$, where it is about a thousand times more accurate. That is why `deriv` uses the central formula with $h=10^{-5}$ by default, and why the simulators in this course never use "the smallest possible step".
''')

B.md(r'''
## Week summary — everything on one page

**Definition.** $\displaystyle f'(x)=\lim_{h\to0}\frac{f(x+h)-f(x)}{h}$ — slope of the tangent; instantaneous rate of change.
Four steps: $f(x+h)$ → subtract $f(x)$ → divide by $h$ and cancel → let $h\to0$.

**Rules proved this week.**
$$\frac{d}{dx}[c]=0,\qquad\frac{d}{dx}[x^n]=n\,x^{n-1},\qquad(c\,f)'=c\,f',\qquad(f\pm g)'=f'\pm g' .$$
Rewrite roots and fractions as powers first. **No** such rule for products or quotients.

**Using it.**
- Tangent line at $a$: $\;y=f(a)+f'(a)(x-a)$.
- Linear approximation: $\;f(a+h)\approx f(a)+f'(a)h$.
- Motion: $v=\dfrac{ds}{dt}$, $\;a=\dfrac{dv}{dt}=\dfrac{d^2s}{dt^2}$. Highest point: $v=0$.
- $f'>0$ rising, $f'<0$ falling, $f'=0$ horizontal tangent.

**No derivative** at a discontinuity, a corner, a vertical tangent. Differentiable ⇒ continuous.

**Numerically.** Central difference $\dfrac{f(x+h)-f(x-h)}{2h}$ with a moderate $h$.
''')

# =====================================================================================
B.md(r'''
---
# Problems

Paper first. First attempt counts. `hint(n)` → `solution(n)` → `mistake(n, '...')`.

### The definition
''')
B.problem(S1, r"Use the **definition** (four steps) to find $f'(2)$ for $f(x)=3x^2-x$.", 'num', 11,
          [r'$f(2+h)=3(2+h)^2-(2+h)$. Expand carefully.', r'$f(2+h)=12+12h+3h^2-2-h=10+11h+3h^2$, and $f(2)=10$.'],
          r'''1. $f(2+h)=3(2+h)^2-(2+h)=3(4+4h+h^2)-2-h=10+11h+3h^2$.
2. $f(2)=12-2=10$. Difference: $11h+3h^2$. (All terms without $h$ cancelled ✓.)
3. Divide by $h$: $11+3h$.
4. $h\to0$: $\;f'(2)=$ **11**.

*Check with the rules:* $f'(x)=6x-1$, so $f'(2)=11$ ✓.''')
B.problem(S1, r'Recognise this limit as a derivative and evaluate it without expanding: $\displaystyle\lim_{h\to0}\frac{(2+h)^5-32}{h}$.', 'num', 80,
          [r'Compare with $\dfrac{f(a+h)-f(a)}{h}$. What are $f$ and $a$? Note $32=2^5$.', r"It is $f'(2)$ for $f(x)=x^5$."],
          r'''With $f(x)=x^5$ and $a=2$: $f(a+h)=(2+h)^5$ and $f(a)=2^5=32$. So the limit is by definition $f'(2)$.

Power rule: $f'(x)=5x^4$, so $f'(2)=5\cdot16=$ **80**.

*(Expanding $(2+h)^5$ would also work, with much more effort. Recognising a limit as a derivative is a standard trick.)*''')
B.problem(S1, r"Let $f(x)=\dfrac{1}{x}$. Using the result of §3.3, what is the slope of the tangent at $x=\tfrac12$?", 'num', -4,
          [r"$f'(x)=-\dfrac{1}{x^2}$."],
          r'''$f'(x)=-\dfrac{1}{x^2}$, so $f'\!\left(\tfrac12\right)=-\dfrac{1}{1/4}=$ **−4**. The curve $\frac1x$ is steep near the origin.''')
B.md(r'''
### Power rule and linearity
''')
B.problem(S2, r'Differentiate $f(x)=4x^3-5x^2+7x-2$.', 'sym', '12*x**2 - 10*x + 7',
          [r'Term by term; constants stay as factors; the constant term disappears.'],
          r'''$$f'(x)=4\cdot3x^2-5\cdot2x+7\cdot1-0=12x^2-10x+7 .$$''', fmt="a formula in `x` as text")
B.problem(S2, r'Differentiate $f(x)=3\sqrt{x}-\dfrac{2}{x^2}$.', 'sym', '3/(2*sqrt(x)) + 4/x**3',
          [r'Rewrite as powers: $3x^{1/2}-2x^{-2}$.', r'$3\cdot\frac12x^{-1/2}-2\cdot(-2)x^{-3}$. Watch the double minus.'],
          r'''Rewrite: $f(x)=3x^{1/2}-2x^{-2}$.
$$f'(x)=3\cdot\tfrac12x^{-1/2}-2\cdot(-2)\,x^{-3}=\frac{3}{2\sqrt{x}}+\frac{4}{x^3}.$$
You can type it as `'3/(2*sqrt(x)) + 4/x**3'` or `'1.5*x**(-0.5) + 4*x**(-3)'`.''', fmt="a formula in `x` as text, e.g. `'1/(2*sqrt(x)) - 3/x**2'`")
B.problem(S2, r'Differentiate $f(x)=(x^2+3)^2$. (Expand first.)', 'sym', '4*x**3 + 12*x',
          [r'$(x^2+3)^2=x^4+6x^2+9$.'],
          r'''Expand: $(x^2+3)^2=x^4+6x^2+9$. Then
$$f'(x)=4x^3+12x .$$
*Not* $2(x^2+3)$ — that would ignore what is inside the bracket. (Next week's chain rule gives $2(x^2+3)\cdot2x=4x^3+12x$ directly.)''', fmt="a formula in `x` as text")
B.problem(S2, r'Differentiate $f(x)=\dfrac{x^4-2x^2+5x}{x}$. (Divide first.)', 'sym', '3*x**2 - 2',
          [r'Divide each term of the numerator by $x$.'],
          r'''Divide term by term: $f(x)=x^3-2x+5$ (for $x\ne0$). Then
$$f'(x)=3x^2-2 .$$''', fmt="a formula in `x` as text")
B.problem(S2, r'What is the slope of the tangent to $y=x^3-2x$ at $x=2$? *(From your diagnostic.)*', 'num', 10,
          [r"Differentiate, then put $x=2$."],
          r'''$\dfrac{dy}{dx}=3x^2-2$. At $x=2$: $3\cdot4-2=$ **10**.''')
B.md(r'''
### Meaning and use
''')
B.problem(S3, r'The tangent to $y=\dfrac1x$ at $x=2$ crosses the $y$-axis at which height?', 'num', 1,
          [r"Tangent: $y=f(2)+f'(2)(x-2)$ with $f(2)=\frac12$ and $f'(2)=-\frac14$.", r'Put $x=0$ into the tangent equation.'],
          r'''$f(2)=\frac12$, $f'(x)=-\frac{1}{x^2}$ so $f'(2)=-\frac14$.

Tangent: $y=\frac12-\frac14(x-2)=1-\frac x4$.

At $x=0$: $y=$ **1**.''')
B.problem(S3, r'At which points is the tangent to $y=x^3-12x$ horizontal? Give both $x$-values.', 'set', [-2, 2],
          [r"Horizontal means $\frac{dy}{dx}=0$."],
          r'''$\dfrac{dy}{dx}=3x^2-12=0\ \Rightarrow\ x^2=4\ \Rightarrow\ x=\pm2$.

(At $x=-2$ the curve has a hill top, $y=16$; at $x=2$ a valley, $y=-16$.)''', fmt='a list, e.g. `[-1, 1]`')
B.problem(S3, r'A ball is thrown up; its height is $s(t)=30t-5t^2$ metres. What is the **maximum height** it reaches?', 'num', 45,
          [r"At the top the velocity is zero. Find $v(t)=s'(t)$ and solve $v=0$.", r'$v=30-10t=0$ at $t=3$. Now compute $s(3)$.'],
          r'''**Velocity.** $v(t)=s'(t)=30-10t$.

**Top.** $v=0\Rightarrow t=3$ s.

**Height.** $s(3)=90-45=$ **45 m**.''', fmt='metres')
B.problem(S3, r'A particle moves with position $s(t)=t^3-6t^2+9t$ (metres, seconds). What is its **acceleration** at $t=3$?', 'num', 6,
          [r'Acceleration is the second derivative: differentiate twice.', r"$v=3t^2-12t+9$, $a=6t-12$."],
          r'''$v(t)=s'(t)=3t^2-12t+9$.

$a(t)=v'(t)=6t-12$.

$a(3)=18-12=$ **6 m/s²**.

(Interesting: $v(3)=27-36+9=0$. At $t=3$ the particle is momentarily at rest but accelerating — like the ball at the top of its flight.)''', fmt='m/s²')
B.problem(S3, r'Use the linear approximation at $a=16$ to estimate $\sqrt{16.4}$.', 'num', 4.05,
          [r"$f(a+h)\approx f(a)+f'(a)h$ with $f=\sqrt{x}$, $a=16$, $h=0.4$.", r"$f'(16)=\dfrac{1}{2\cdot4}=\dfrac18$."],
          r'''$f(16)=4$, $f'(x)=\dfrac{1}{2\sqrt{x}}$, $f'(16)=\dfrac18$, $h=0.4$.
$$\sqrt{16.4}\approx4+\frac18\cdot0.4=4.05 .$$
(True value: $4.04969\ldots$)''')
B.problem(S3, r'The radius of a metal disc is measured as $10$ cm with a possible error of $0.1$ cm. Use the linear approximation to estimate the possible error in the computed **area** $A=\pi r^2$ (in cm²).', 'num', 2 * math.pi,
          [r"$\Delta A\approx A'(r)\,\Delta r$.", r"$A'(r)=2\pi r$, so $\Delta A\approx2\pi\cdot10\cdot0.1$."],
          r'''$A(r)=\pi r^2$, so $A'(r)=2\pi r$.
$$\Delta A\approx A'(10)\cdot\Delta r=2\pi\cdot10\cdot0.1=2\pi\approx6.28\ \text{cm}^2 .$$
Relative error: $\dfrac{6.28}{314.2}=2\%$ — twice the 1 % relative error in $r$, as the rule "$(1+h)^n\approx1+nh$" predicts.

*Geometric meaning:* the extra area is a thin ring of length $2\pi r$ and width $\Delta r$.''', fmt='cm²')
B.problem(S3, r'At which point of the parabola $y=x^2$ is the tangent parallel to the line $y=3x-1$? Give the $x$-coordinate.', 'num', 1.5,
          [r'Parallel lines have equal slopes. What is the slope of $y=3x-1$?', r'Solve $2x=3$.'],
          r'''The line has slope 3. The parabola has slope $\frac{dy}{dx}=2x$. Equal when $2x=3$: $x=$ **1.5** (the point $(1.5,\,2.25)$).''')
B.md(r'''
### Existence and numerics
''')
B.problem(S4, r'For $f(x)=|x-3|$, what is the **left-hand** limit of the difference quotient at $x=3$: $\displaystyle\lim_{h\to0^-}\frac{f(3+h)-f(3)}{h}$?', 'num', -1,
          [r'$f(3+h)=|h|$, and for negative $h$, $|h|=-h$.'],
          r'''$f(3+h)=|3+h-3|=|h|$ and $f(3)=0$. The quotient is $\dfrac{|h|}{h}$.

For $h<0$: $|h|=-h$, so the quotient is $\dfrac{-h}{h}=-1$. The left-hand limit is **−1**.

The right-hand limit is $+1$; they differ, so $f$ has no derivative at 3 (a corner).''')
B.problem(S4, r"Compute the **central difference** approximation to $f'(1)$ for $f(x)=x^3$ with $h=0.1$. (Exact arithmetic; the answer is not exactly 3.)", 'num', 3.01,
          [r'$\dfrac{f(1.1)-f(0.9)}{0.2}$.', r'$1.1^3=1.331$ and $0.9^3=0.729$.'],
          r'''$$\frac{f(1.1)-f(0.9)}{2\cdot0.1}=\frac{1.331-0.729}{0.2}=\frac{0.602}{0.2}=3.01 .$$
The exact derivative is $3$; the error is $0.01=h^2$. In general for $x^3$ the central difference gives $3x^2+h^2$ (expand it and see): error proportional to $h^2$.''')
B.code(r'''
# scratch cell: use Python as a calculator here
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
1. Write the definition of $f'(x)$ and explain each piece with a sketch.
2. Derive $\frac{d}{dx}[x^2]=2x$ and $\frac{d}{dx}\!\left[\frac1x\right]=-\frac{1}{x^2}$ from the definition.
3. Explain, with the "pick $x$ or $h$ from each bracket" argument, why $\frac{d}{dx}[x^n]=nx^{n-1}$.
4. Why is the derivative zero at the top of a throw?
5. Why does a numerical derivative get *worse* if $h$ is made too small?

*Your answers:*

&nbsp;

### 3 · Physics strand — velocity is the slope of position (1 hour)
The projectile simulator plots position and velocity against time. Drag is switched off.

**Predict first:** the *height* plot is a parabola. What shape is the vertical-velocity plot `vy`, and what is its slope? At what time does `vy` cross zero, in terms of the launch speed and angle? Then run it and check: for $v_0=25$ m/s at $53^\circ$ the vertical launch speed is $25\sin53^\circ\approx20$ m/s, so this is the worked example of §4.1 — with $g=9.81$ instead of 10.
''')
B.code(r'''
lab('physics', exp='proj', k=0, v0=25, ang=53)
''')
B.md(r'''
### 4 · What comes next
**Week 2** differentiates $\sin$, $\cos$, $e^x$ and $\ln$ (using the special limits of Unit 1 week 3), and proves the three rules that this week's warning said were missing: **product**, **quotient** and **chain**. After that you can differentiate any formula you can write down.
''')

if __name__ == '__main__':
    B.write()
