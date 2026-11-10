"""Unit 2 · Week 3 (course week 6) - Implicit differentiation, related rates, linear approximation, Newton's method."""
import math
from nbkit import Book
import figs_u02 as F

B = Book('u02w3', 'Unit 2 · Week 3 — Implicit differentiation, related rates and Newton’s method', 'year1/u02w3-implicit-rates-newton.ipynb')
S1, S2, S3, S4 = '1 Implicit differentiation', '2 Related rates', '3 Linear approximation and errors', '4 Newton’s method'

B.md(r'''
# Unit 2 · Week 3 — Implicit differentiation, related rates and Newton's method
*Term 1, week 6 of 12 · about 15 hours in this notebook and on paper*

**Where you are.** You can differentiate any formula $y=f(x)$. This week the chain rule is put to work in four situations where there is **no ready-made formula** $y=f(x)$ to differentiate.

| part | situation | example |
|---|---|---|
| 1 | $x$ and $y$ are tied together by an equation that is not solved for $y$ | the slope of a circle; the derivatives of $\arcsin$ and $\arctan$ |
| 2 | several quantities change together in time | how fast does the top of a sliding ladder fall? |
| 3 | you only need a value *near* a known one, or want to know how a measurement error spreads | $e^{0.05}\approx1.05$; error in $g$ from a pendulum experiment |
| 4 | an equation $f(x)=0$ has no formula solution | Newton's method — the solver inside the circuit simulator |

**What is used from earlier:** all the rules of last week, above all the **chain rule**; the tangent line $y=f(a)+f'(a)(x-a)$ (week 1); inverse trig functions and their ranges (Unit 1 week 2); bisection (Unit 1 week 3).

Run the grey *SETUP* cell first. `compare(f, your_derivative)` is available as last week.
''')

# =====================================================================================
B.md(r'''
---
# Part 1 — Implicit differentiation

## 1.1 The problem

**Why.** What is the slope of the circle $x^2+y^2=25$ at the point $(3,4)$? The equation is not of the form $y=f(x)$. You *could* solve for $y$: $y=\pm\sqrt{25-x^2}$, choose the right sign, and differentiate. That works here, but it is clumsy — and for a curve such as $x^3+y^3=6xy$ solving for $y$ is practically impossible. We need a way to find $\frac{dy}{dx}$ **without solving for $y$**.

An equation like $x^2+y^2=25$ defines $y$ **implicitly** (the relation between $x$ and $y$ is implied, not spelled out). A formula $y=f(x)$ defines it **explicitly**.

## 1.2 The idea

**Build.**

**Step 1 — near a point of the curve, $y$ *is* a function of $x$.** Walk along the circle near $(3,4)$: for each $x$ there is one nearby $y$. So there is a function $y(x)$, even if we do not write down its formula, and the equation says that
$$x^2+\big(y(x)\big)^2=25\qquad\text{for all $x$ near 3.}$$

**Step 2 — two functions that are equal have equal derivatives.** The left side is a function of $x$; the right side is the constant function 25. Differentiate both sides with respect to $x$.

**Step 3 — the only new thing: a $y$-term is a chain.** $\big(y(x)\big)^2$ is "something squared": outer function $u^2$, inner function $u=y(x)$. By the chain rule
$$\frac{d}{dx}\big[y^2\big]=2y\cdot\frac{dy}{dx}.$$
Compare: $\frac{d}{dx}[x^2]=2x$ — no extra factor, because the inside is $x$ itself. **Whenever you differentiate an expression in $y$ with respect to $x$, the chain rule adds a factor $\frac{dy}{dx}$.**

**Step 4 — do it.**
$$\begin{aligned}
\frac{d}{dx}\big[x^2+y^2\big]&=\frac{d}{dx}[25]\\
2x+2y\,\frac{dy}{dx}&=0\\
\frac{dy}{dx}&=-\frac{x}{y} &&\text{(solve for $\tfrac{dy}{dx}$)}
\end{aligned}$$
At $(3,4)$: $\dfrac{dy}{dx}=-\dfrac34$.
''')
B.fig('implicit_circle', F.implicit_circle, 'The tangent to the circle at (3, 4) has slope −3/4.')
B.md(r'''
**Check 1 — the explicit way.** Upper half: $y=\sqrt{25-x^2}$, so $\dfrac{dy}{dx}=\dfrac{-2x}{2\sqrt{25-x^2}}=-\dfrac{x}{\sqrt{25-x^2}}=-\dfrac xy$ ✓ — the same formula.

**Check 2 — geometry.** The radius to $(3,4)$ has slope $\frac43$. A tangent to a circle is perpendicular to the radius, and perpendicular lines have slopes whose product is $-1$: $\frac43\cdot\left(-\frac34\right)=-1$ ✓.

Notice that the answer $-\frac xy$ contains **both** $x$ and $y$. That is normal: to get a number you need a *point* on the curve, not just an $x$ (for $x=3$ the circle has two points, $(3,4)$ and $(3,-4)$, with slopes $-\frac34$ and $+\frac34$).

## 1.3 The procedure

1. Differentiate **both sides** of the equation with respect to $x$.
2. Treat $y$ as a function of $x$: every time you differentiate a term containing $y$, the chain rule gives a factor $\dfrac{dy}{dx}$ (write $y'$ for short). Products such as $xy$ need the product rule.
3. Collect the terms with $y'$ on one side and **solve for $y'$**. (This is always just a linear equation in $y'$.)

**Worked example 1.** Find the slope of $x^2+xy+y^2=7$ at $(1,2)$. (Check the point is on the curve: $1+2+4=7$ ✓.)

$$\begin{aligned}
\frac{d}{dx}[x^2]+\frac{d}{dx}[xy]+\frac{d}{dx}[y^2]&=0\\
2x+\big(1\cdot y+x\cdot y'\big)+2y\,y'&=0 &&\text{($xy$: product rule; $y^2$: chain rule)}\\
x\,y'+2y\,y'&=-2x-y &&\text{(terms with $y'$ on the left)}\\
y'\,(x+2y)&=-(2x+y)\\
y'&=-\frac{2x+y}{x+2y}.
\end{aligned}$$
At $(1,2)$: $y'=-\dfrac{2+2}{1+4}=-\dfrac45$.

**Worked example 2.** $x^3+y^3=9$ at $(1,2)$.
$$3x^2+3y^2\,y'=0\quad\Rightarrow\quad y'=-\frac{x^2}{y^2}=-\frac14 .$$

**Worked example 3 — a function of $y$.** $\sin y=x^2$.
$$\cos y\cdot y'=2x\quad\Rightarrow\quad y'=\frac{2x}{\cos y}.$$

**The classic mistakes:** forgetting the factor $y'$ on a $y$-term ($\frac{d}{dx}y^2\ne2y$), and forgetting the product rule on $xy$.
''')
B.ask(r'''Use implicit differentiation to find the slope of the circle $x^2+y^2=25$ at the point $(-4,3)$.''', 'num', 4 / 3,
      r'''$\dfrac{dy}{dx}=-\dfrac xy=-\dfrac{-4}{3}=\dfrac43$. (The radius has slope $-\frac34$; the product is $-1$ ✓.)''',
      r'''We found $\dfrac{dy}{dx}=-\dfrac xy$. Put in $x=-4$, $y=3$ and watch the signs.''', fmt='a number, e.g. `-3/4`')
B.ask(r'''For the curve $x^2+3y^2=13$, find $\dfrac{dy}{dx}$ at $(1,2)$.''', 'num', -1 / 6,
      r'''$2x+6y\,y'=0\Rightarrow y'=-\dfrac{2x}{6y}=-\dfrac{x}{3y}$. At $(1,2)$: $-\dfrac16$.''',
      r'''Differentiate term by term: $2x+3\cdot2y\cdot y'=0$. Solve for $y'$.''', fmt='a number, e.g. `-1/4`')

B.md(r'''
## 1.4 The derivatives of the inverse trigonometric functions

**Why.** $\arcsin$, $\arccos$, $\arctan$ are *defined* implicitly — as "the angle whose sine is $x$" (Unit 1 week 2, §2.1). So implicit differentiation is exactly the tool to differentiate them. The results are surprising — no trigonometry is left in them — and you will need them for integrals in Unit 3.

**Build — $\arcsin$.**

**Step 1.** $y=\arcsin x$ means: $\sin y=x$, **with $y$ in $\left[-\frac\pi2,\frac\pi2\right]$**.

**Step 2.** Differentiate $\sin y=x$ implicitly:
$$\cos y\cdot y'=1\qquad\Rightarrow\qquad y'=\frac{1}{\cos y}.$$

**Step 3 — express $\cos y$ in terms of $x$.** From $\sin^2y+\cos^2y=1$: $\cos y=\pm\sqrt{1-\sin^2y}=\pm\sqrt{1-x^2}$. Which sign? For $y$ between $-\frac\pi2$ and $\frac\pi2$ the cosine is **positive** (quadrants I and IV). So $\cos y=+\sqrt{1-x^2}$:
$$\boxed{\,\frac{d}{dx}\arcsin x=\frac{1}{\sqrt{1-x^2}}\,}\qquad(-1<x<1)$$
(The restricted range, which seemed a technicality in Unit 1, is what decides the sign here.)

**Build — $\arctan$.** $y=\arctan x$ means $\tan y=x$. Differentiate, using $\frac{d}{dy}\tan y=1+\tan^2y$ (last week, §2.2):
$$(1+\tan^2y)\cdot y'=1\qquad\Rightarrow\qquad y'=\frac{1}{1+\tan^2y}=\frac{1}{1+x^2}.$$
$$\boxed{\,\frac{d}{dx}\arctan x=\frac{1}{1+x^2}\,}$$

**And $\arccos$.** $\cos y=x$ with $y\in[0,\pi]$: $\;-\sin y\cdot y'=1$, and $\sin y=+\sqrt{1-x^2}$ on that range, so $\dfrac{d}{dx}\arccos x=-\dfrac{1}{\sqrt{1-x^2}}$. (Makes sense: $\arcsin x+\arccos x=\frac\pi2$ is constant, so their derivatives must add to zero.)

**With the chain rule:** $\dfrac{d}{dx}\arctan(g(x))=\dfrac{g'(x)}{1+g(x)^2}$. Example: $\dfrac{d}{dx}\arctan(3x)=\dfrac{3}{1+9x^2}$.
''')
B.code(r'''
# See it: the numerical slope of arctan against 1/(1 + x²)
compare(lambda v: atan(v),  lambda v: 1 / (1 + v**2), lo=-5, hi=5)
''')
B.ask(r'''What is the slope of $y=\arcsin x$ at $x=0.6$?''', 'num', 1.25,
      r'''$\dfrac{1}{\sqrt{1-0.36}}=\dfrac{1}{0.8}=1.25$.''',
      r'''$\dfrac{d}{dx}\arcsin x=\dfrac{1}{\sqrt{1-x^2}}$.''')

B.md(r'''
## 1.5 Logarithmic differentiation

**Why.** What is the derivative of $x^x$? It is neither a power function (the exponent varies) nor an exponential (the base varies), so neither rule applies.

**Build.** Take logarithms first — a logarithm turns a power into a product:
$$y=x^x\quad\Rightarrow\quad\ln y=x\ln x .$$
Now differentiate implicitly. On the left, $\ln y$ is a chain: $\frac{d}{dx}\ln y=\frac1y\,y'$. On the right, a product:
$$\frac{y'}{y}=1\cdot\ln x+x\cdot\frac1x=\ln x+1\qquad\Rightarrow\qquad y'=y\,(\ln x+1)=x^x(\ln x+1).$$

The same trick tames complicated products and quotients, because $\ln$ turns products into sums.
''')

# =====================================================================================
B.md(r'''
---
# Part 2 — Related rates

## 2.1 The idea

**Why.** A ladder slides down a wall; a balloon is inflated; water runs into a tank. In each case several quantities change *together*, linked by geometry. If you know how fast one changes, how fast does the other?

**Build.** If two quantities are linked by an equation **at every moment**, then both sides of that equation are equal *as functions of time*, so their time-derivatives are equal too. Differentiating the equation with respect to $t$ — with the chain rule, exactly as in Part 1 but with $t$ in the role of $x$ — turns a relation between **quantities** into a relation between their **rates**.

**The procedure.**

1. **Sketch.** Give a **letter** to every quantity that changes with time. Only quantities that never change may be numbers.
2. **Write the equation** that links the letters (Pythagoras, similar triangles, a volume formula, …).
3. **Differentiate both sides with respect to $t$.** Every letter is a function of $t$: the chain rule gives each its own rate, $\frac{dx}{dt}$, $\frac{dy}{dt}$, …
4. **Only now put in the numbers** for the instant in question.
5. **Solve** for the rate you want. State units, and interpret the sign.

> **The classic mistake** is to put the numbers in *before* differentiating (step 4 before step 3). A number is a constant; its derivative is zero; everything collapses to $0=0$.

**Worked example 1 — the sliding ladder.** A 5 m ladder leans against a wall. Its foot is pulled away from the wall at 1 m/s. How fast is the top sliding down when the foot is 3 m from the wall?
''')
B.fig('ladder', F.ladder, 'x and y change with time; the length 5 m does not.')
B.md(r'''
1. **Letters.** $x$ = distance of the foot from the wall; $y$ = height of the top. Both change. The length $5$ is constant. Given: $\frac{dx}{dt}=1$ m/s. Wanted: $\frac{dy}{dt}$ when $x=3$.
2. **Equation.** Pythagoras: $\;x^2+y^2=25$.
3. **Differentiate with respect to $t$** (both $x$ and $y$ are functions of $t$):
$$2x\,\frac{dx}{dt}+2y\,\frac{dy}{dt}=0 .$$
4. **Numbers.** When $x=3$: $y=\sqrt{25-9}=4$. And $\frac{dx}{dt}=1$:
$$2\cdot3\cdot1+2\cdot4\cdot\frac{dy}{dt}=0 .$$
5. **Solve.** $\dfrac{dy}{dt}=-\dfrac{6}{8}=-0.75$ m/s. The minus sign says $y$ is decreasing: the top comes **down** at 0.75 m/s.

In general $\frac{dy}{dt}=-\frac xy\frac{dx}{dt}$: as the top nears the ground ($y\to0$), its speed grows without bound. Real ladders do exactly that.

### Experiment 1 — simulate the ladder
The simulation moves the foot outward at 1 m/s in small time steps, computes the height from Pythagoras each time, and *measures* how fast the height changes.

**Predict first:** the speed of the top when the foot is at 3 m (you know it), at 4 m, and at 4.9 m. Use $\frac{dy}{dt}=-\frac xy\cdot1$.
''')
B.code(r'''
dt = 0.001
ts = np.arange(0, 1.95, dt)
xs = 3 + 1.0 * ts                       # the foot starts at 3 m and moves out at 1 m/s
ys = np.sqrt(25 - xs**2)                # the top is where Pythagoras says
speed_measured = np.diff(ys) / dt       # rise over run, step by step
speed_formula = -xs / ys * 1.0          # the related-rates result

fig, (a1, a2) = plt.subplots(1, 2, figsize=(10.5, 3.6))
a1.plot(ts, xs, label='x (foot)'); a1.plot(ts, ys, label='y (top)'); a1.set_xlabel('t (s)'); a1.legend()
a2.plot(ts[:-1], speed_measured, lw=5, alpha=0.3, label='measured dy/dt'); a2.plot(ts, speed_formula, 'r--', label='−x/y · dx/dt')
a2.set_xlabel('t (s)'); a2.set_ylim(-12, 0); a2.legend(); plt.show()
rows = [[3 + tt, float(np.sqrt(25 - (3 + tt)**2)), -(3 + tt) / float(np.sqrt(25 - (3 + tt)**2))] for tt in [0, 1, 1.9]]
table(['x (m)', 'y (m)', 'dy/dt (m/s)'], rows, fmt='%.3f')
''')
B.md(r'''
**Worked example 2 — the balloon.** A spherical balloon is inflated at $100$ cm³/s. How fast is its radius growing when the radius is $5$ cm?

1. **Letters.** $V$ = volume, $r$ = radius. Given $\frac{dV}{dt}=100$. Wanted $\frac{dr}{dt}$ when $r=5$.
2. **Equation.** $V=\frac43\pi r^3$.
3. **Differentiate w.r.t. $t$** (chain rule on $r^3$): $\;\dfrac{dV}{dt}=\frac43\pi\cdot3r^2\cdot\dfrac{dr}{dt}=4\pi r^2\,\dfrac{dr}{dt}$.
4. **Numbers.** $100=4\pi\cdot25\cdot\dfrac{dr}{dt}$.
5. **Solve.** $\dfrac{dr}{dt}=\dfrac{100}{100\pi}=\dfrac1\pi\approx0.318$ cm/s.

*Notice:* $4\pi r^2$ is the surface area of the sphere. The new air spreads as a thin layer over the whole surface; the bigger the balloon, the thinner the layer, the slower the radius grows.

**Worked example 3 — the conical tank.** Water runs at $0.5$ m³/min into a cone-shaped tank (point down) of height 4 m and top radius 2 m. How fast is the water level rising when the water is 2 m deep?
''')
B.fig('cone_tank', F.cone_tank, 'The water forms a smaller cone, similar to the tank.')
B.md(r'''
1. **Letters.** $h$ = depth of the water, $r$ = radius of the water surface, $V$ = volume of water. All three change. Given $\frac{dV}{dt}=0.5$. Wanted $\frac{dh}{dt}$ when $h=2$.
2. **Equation.** Volume of a cone: $V=\frac13\pi r^2h$. That has *two* changing letters on the right — one too many. **Eliminate $r$ with similar triangles:** the water cone has the same shape as the tank, so $\dfrac rh=\dfrac24$, i.e. $r=\dfrac h2$. Then
$$V=\frac13\pi\left(\frac h2\right)^2h=\frac{\pi}{12}h^3 .$$
3. **Differentiate w.r.t. $t$:** $\;\dfrac{dV}{dt}=\dfrac{\pi}{12}\cdot3h^2\cdot\dfrac{dh}{dt}=\dfrac{\pi}{4}h^2\,\dfrac{dh}{dt}$.
4. **Numbers.** $0.5=\dfrac\pi4\cdot4\cdot\dfrac{dh}{dt}=\pi\,\dfrac{dh}{dt}$.
5. **Solve.** $\dfrac{dh}{dt}=\dfrac{0.5}{\pi}\approx0.159$ m/min.

The lesson of this example: **reduce the equation to one changing quantity on each side before you differentiate** — and use the geometry (similar triangles) to do it.
''')
B.ask(r'''A circular ripple spreads on a pond; its radius grows at $0.5$ m/s. How fast is its **area** growing (in m²/s) when the radius is $4$ m?''', 'num', 4 * math.pi,
      r'''$A=\pi r^2\Rightarrow\dfrac{dA}{dt}=2\pi r\,\dfrac{dr}{dt}=2\pi\cdot4\cdot0.5=4\pi\approx12.57$ m²/s. ($2\pi r$ is the circumference: the new area is a thin ring.)''',
      r'''$A=\pi r^2$. Differentiate with respect to $t$ (chain rule), *then* put in $r=4$ and $\frac{dr}{dt}=0.5$.''', fmt='m²/s; you can type `4*pi`')
B.ask(r'''The side $s$ of a cube grows at $2$ cm/s. How fast is its volume growing (cm³/s) when $s=3$ cm?''', 'num', 54,
      r'''$V=s^3\Rightarrow\dfrac{dV}{dt}=3s^2\,\dfrac{ds}{dt}=3\cdot9\cdot2=54$ cm³/s.''',
      r'''$V=s^3$; chain rule: $\dfrac{dV}{dt}=3s^2\dfrac{ds}{dt}$.''', fmt='cm³/s')

# =====================================================================================
B.md(r'''
---
# Part 3 — Linear approximation and error propagation

## 3.1 The standard small-quantity approximations

**Why.** In week 1 (§4.2) you met $f(a+h)\approx f(a)+f'(a)\,h$: near a point, a curve is nearly its tangent. Engineers use a handful of these so often that they are worth knowing by heart — and each is a one-line consequence.
''')
B.fig('linear_approx', F.linear_approx, 'Near the point of contact the tangent is an excellent stand-in for the curve; further away the error grows.')
B.md(r'''
**Build.** Take $a=0$, so the approximation reads $f(x)\approx f(0)+f'(0)\,x$ for small $x$.

| $f(x)$ | $f(0)$ | $f'(x)$ | $f'(0)$ | approximation for small $x$ |
|---|---|---|---|---|
| $\sin x$ | $0$ | $\cos x$ | $1$ | $\sin x\approx x$ |
| $\cos x$ | $1$ | $-\sin x$ | $0$ | $\cos x\approx1$ |
| $\tan x$ | $0$ | $1+\tan^2x$ | $1$ | $\tan x\approx x$ |
| $e^x$ | $1$ | $e^x$ | $1$ | $e^x\approx1+x$ |
| $\ln(1+x)$ | $0$ | $\frac{1}{1+x}$ | $1$ | $\ln(1+x)\approx x$ |
| $(1+x)^n$ | $1$ | $n(1+x)^{n-1}$ | $n$ | $(1+x)^n\approx1+nx$ |

The last row with $n=\frac12$ and $n=-1$ gives two favourites: $\;\sqrt{1+x}\approx1+\dfrac x2\;$ and $\;\dfrac{1}{1+x}\approx1-x$.

$\sin x\approx x$ is the small-angle approximation of Unit 1 — which you first saw in a picture, then as a limit, and now as a tangent line. For $\cos x$ the tangent at 0 is horizontal, so to first order nothing changes; the first correction, $-\frac{x^2}{2}$, is of *second* order (Unit 4 gives the general pattern).

**Worked example.** A 3 % annual interest rate, compounded continuously for one year, multiplies your money by $e^{0.03}\approx1+0.03=1.03$. (Exact: $1.03045$.)

## 3.2 How good is the approximation?

### Experiment 2 — the error of the tangent line
**Predict first:** if $h$ is halved, by what factor does the error of $e^h\approx1+h$ shrink — 2, 4 or 8?
''')
B.code(r'''
rows = []
for hh in [0.4, 0.2, 0.1, 0.05, 0.025]:
    err = exp(hh) - (1 + hh)
    rows.append([hh, exp(hh), 1 + hh, err, err / hh**2])
table(['h', 'e^h', '1 + h', 'error', 'error / h²'], rows, fmt='%.6f')
''')
B.md(r'''
*Explain:* halving $h$ divides the error by **4**: the error is proportional to $h^2$. The last column settles near $0.5$ — which is $\frac12f''(0)$. In general
$$f(a+h)\approx f(a)+f'(a)\,h\qquad\text{with an error of about }\tfrac12f''(a)\,h^2 .$$
The second derivative measures how fast the curve bends away from its tangent. (Unit 4 proves this and continues the pattern.)

## 3.3 Error propagation

**Why.** Every measurement has an error. If you compute something from a measured value, how big is the error in the result? This is one of the most common uses of derivatives in the laboratory.

**Build.**

**Step 1 — absolute errors.** If $x$ is measured with a small error $\Delta x$, then the computed $y=f(x)$ is off by about
$$\Delta y\approx f'(x)\,\Delta x .$$
The derivative is the **magnification factor** of errors.

**Step 2 — relative (percentage) errors for powers.** For $y=c\,x^n$: $\;\Delta y\approx c\,n\,x^{n-1}\Delta x$. Divide by $y=c\,x^n$:
$$\frac{\Delta y}{y}\approx n\,\frac{\Delta x}{x}.$$
**A power $n$ multiplies the relative error by $n$.** A 1 % error in a radius gives a 2 % error in the area $\pi r^2$ and a 3 % error in the volume $\frac43\pi r^3$.

**Step 3 — several measured quantities.** For $y=c\,x^m\,z^n$, take logarithms — they turn products into sums: $\ln y=\ln c+m\ln x+n\ln z$. A small change in each term (using $\Delta\ln u\approx\frac{\Delta u}{u}$, the linear approximation of $\ln$):
$$\frac{\Delta y}{y}\approx m\,\frac{\Delta x}{x}+n\,\frac{\Delta z}{z}.$$
**Relative errors add, each weighted by its power.** If the signs of the errors are unknown, take the worst case: add the *sizes*.

**Worked example — measuring $g$ with a pendulum.** A pendulum of length $L$ has period $T=2\pi\sqrt{L/g}$, so $g=\dfrac{4\pi^2L}{T^2}=4\pi^2\,L^{1}\,T^{-2}$.
$$\frac{\Delta g}{g}\approx1\cdot\frac{\Delta L}{L}-2\cdot\frac{\Delta T}{T}.$$
If $L$ is known to 1 % and $T$ to 0.5 %, the worst case is $1\%+2\cdot0.5\%=2\%$. The period counts double because it is squared — so time many swings to measure $T$ well.
''')
B.ask(r'''Use a standard approximation to estimate $\sqrt{1.06}$.''', 'num', 1.03,
      r'''$\sqrt{1+x}\approx1+\dfrac x2$ with $x=0.06$: $1.03$. (Exact: $1.02956$.)''',
      r'''$\sqrt{1+x}\approx1+\dfrac x2$.''')
B.ask(r'''The radius of a ball is measured with a relative error of $2\%$. What is the approximate relative error (in %) of the computed volume $V=\frac43\pi r^3$?''', 'num', 6,
      r'''A power $n$ multiplies the relative error by $n$: $3\times2\%=6\%$.''',
      r'''$\dfrac{\Delta V}{V}\approx3\,\dfrac{\Delta r}{r}$.''', fmt='a number (percent)')

# =====================================================================================
B.md(r'''
---
# Part 4 — Newton's method

## 4.1 The idea: slide down the tangent

**Why.** Most equations cannot be solved by formula: $\cos x=x$, $x^5-x-1=0$, or the equation for the operating point of a circuit with a diode. In Unit 1 you solved such equations by **bisection**: safe, but slow (one binary digit per step). With derivatives you can do far better.

**Build.** We want a solution of $f(x)=0$ — a point where the graph crosses the $x$-axis.

**Step 1.** Start from a guess $x_0$. It is probably wrong: $f(x_0)\ne0$.

**Step 2.** Near $x_0$ the curve is nearly its tangent (Part 3). **Replace the curve by the tangent** — for a straight line, finding the crossing point is easy.
''')
B.fig('newton', F.newton, 'Each step: go up to the curve, slide down the tangent to the axis.')
B.md(r'''
**Step 3 — where does the tangent cross the axis?** The tangent at $x_0$ is $y=f(x_0)+f'(x_0)(x-x_0)$. Set $y=0$ and solve for $x$:
$$\begin{aligned}
0&=f(x_0)+f'(x_0)\,(x-x_0)\\
x-x_0&=-\frac{f(x_0)}{f'(x_0)}\\
x&=x_0-\frac{f(x_0)}{f'(x_0)}.
\end{aligned}$$
Call this $x_1$: a better guess.

**Step 4 — repeat** from $x_1$, then from $x_2$, …

$$\boxed{\,x_{n+1}=x_n-\frac{f(x_n)}{f'(x_n)}\,}\qquad\textbf{Newton's method}$$

**Worked example — $\sqrt2$ by hand.** $\sqrt2$ is the positive solution of $f(x)=x^2-2=0$. Here $f'(x)=2x$:
$$x_{n+1}=x_n-\frac{x_n^2-2}{2x_n}=\frac{2x_n^2-x_n^2+2}{2x_n}=\frac{x_n^2+2}{2x_n}=\frac12\left(x_n+\frac{2}{x_n}\right).$$
"*The average of your guess and 2 divided by your guess.*" Start with $x_0=1$:

| $n$ | $x_n$ | correct digits |
|---|---|---|
| 0 | $1$ | 1 |
| 1 | $\frac12(1+2)=1.5$ | 1 |
| 2 | $\frac12\left(1.5+\frac{2}{1.5}\right)=1.416666\ldots$ | 3 |
| 3 | $1.414215686\ldots$ | 6 |
| 4 | $1.414213562374\ldots$ | 12 |

The number of correct digits roughly **doubles at every step**. (This recipe for square roots was known in Babylon 3500 years ago; Newton's method is its generalisation.)

### Experiment 3 — write Newton's method
Replace the `...` by one Newton step. The tests tell you whether it works.
''')
B.code(r'''
def newton(f, fprime, x0, tol=1e-12, max_steps=50):
    """Solve f(x) = 0 starting from the guess x0. fprime is the derivative of f."""
    xn = x0
    for step in range(max_steps):
        x_new = ...                      # one Newton step from xn
        if abs(x_new - xn) < tol:        # stop when the guess no longer changes
            return x_new
        xn = x_new
    return xn


# ---------- tests: do not change ----------
def test_newton():
    cases = [('x² − 2 = 0 from 1', lambda v: v * v - 2, lambda v: 2 * v, 1.0, sqrt(2)),
             ('cos x − x = 0 from 1', lambda v: cos(v) - v, lambda v: -sin(v) - 1, 1.0, 0.7390851332151607),
             ('x³ − x − 1 = 0 from 1.5', lambda v: v**3 - v - 1, lambda v: 3 * v**2 - 1, 1.5, 1.324717957244746),
             ('eˣ − 3 = 0 from 1', lambda v: exp(v) - 3, lambda v: exp(v), 1.0, ln(3))]
    good = 0
    for name, f, fp, x0, true in cases:
        try:
            r = float(newton(f, fp, x0))
        except Exception as err:
            print('✗', name, '-> not working yet (have you replaced the ... ?)'); continue
        ok = abs(r - true) < 1e-9; good += ok
        print('✓' if ok else '✗', name, '->', r)
    print('\nAll tests passed.' if good == len(cases) else '\nNot there yet: one step is  xn - f(xn) / fprime(xn).')

test_newton()
''', ref=r'''
def newton(f, fprime, x0, tol=1e-12, max_steps=50):
    xn = x0
    for step in range(max_steps):
        x_new = xn - f(xn) / fprime(xn)
        if abs(x_new - xn) < tol:
            return x_new
        xn = x_new
    return xn
print(newton(lambda v: v * v - 2, lambda v: 2 * v, 1.0))
''')
B.md(r'''
### Experiment 4 — Newton against bisection
Both methods solve $x^3-x-1=0$. The table shows the error after each step.

**Predict first:** bisection gains one binary digit per step, i.e. about 3 decimal digits per 10 steps. How many steps will Newton need for 15 digits?
''')
B.code(r'''
f = lambda v: v**3 - v - 1
fp = lambda v: 3 * v**2 - 1
root = 1.324717957244746

a, b = 1.0, 2.0            # bisection
xn = 1.5                   # Newton
rows = []
for step in range(1, 9):
    m = (a + b) / 2
    if f(a) * f(m) <= 0: b = m
    else: a = m
    xn = xn - f(xn) / fp(xn)
    rows.append([step, abs((a + b) / 2 - root), abs(xn - root)])
table(['step', 'error of bisection', 'error of Newton'], rows, fmt='%.1e')
''')
B.md(r'''
*Explain:* bisection roughly halves its error each step. Newton **squares** it: $10^{-2}\to10^{-4}\to10^{-8}\to10^{-16}$. After four or five steps it has reached the limit of the computer's precision. That is called *quadratic convergence*, and it is why Newton's method is inside almost every engineering solver.

## 4.2 When Newton's method fails

**Build.** The speed has a price: Newton's method can go wrong, in three typical ways. All of them are visible in the formula $x_{n+1}=x_n-\dfrac{f(x_n)}{f'(x_n)}$.

1. **A horizontal tangent**, $f'(x_n)=0$: division by zero. The tangent never meets the axis. If $f'(x_n)$ is merely *small*, the next guess is thrown far away.
2. **A cycle.** For $f(x)=x^3-2x+2$ starting at $x_0=0$: $x_1=0-\frac{2}{-2}=1$, then $x_2=1-\frac{1}{1}=0$, then $1$, then $0$, … for ever.
3. **A bad start.** Too far from the root, the tangent can point the wrong way, and the guesses run off or converge to a different root.

Run the cell to watch failure 2, and what a slightly different start does.
''')
B.code(r'''
f = lambda v: v**3 - 2 * v + 2
fp = lambda v: 3 * v**2 - 2
for start in [0.0, 0.1, -2.0]:
    xn, path = start, [start]
    for step in range(8):
        xn = xn - f(xn) / fp(xn); path.append(xn)
    print(f'start {start:5.1f}:  ' + '  '.join(f'{p:8.4f}' for p in path))
''')
B.md(r'''
*Explain:* from $0$ the method bounces between 0 and 1 for ever. From $0.1$ it wanders for a while near that trap. From $-2$ it converges in a few steps to the real root $-1.7693$.

**The engineering conclusion.** Bisection: slow but cannot fail. Newton: very fast near the root but can fail far from it. Professional solvers combine them — Newton steps, with a safeguard (a bracket, or a limit on the step size) when a step looks wild.

## 4.3 Where this lives: the operating point of a diode circuit

**Build.** A battery $V$ drives a resistor $R$ in series with a diode. The current through the resistor is $\dfrac{V-v}{R}$, where $v$ is the diode voltage. The current through the diode is given by the Shockley equation $I_s\big(e^{v/V_T}-1\big)$. They are in series, so the two currents are equal:
$$\frac{V-v}{R}=I_s\big(e^{v/V_T}-1\big).$$
The unknown $v$ appears both alone and inside an exponential: **no formula solves this**. Write it as $f(v)=0$ with
$$f(v)=\frac{V-v}{R}-I_s\big(e^{v/V_T}-1\big),\qquad f'(v)=-\frac1R-\frac{I_s}{V_T}\,e^{v/V_T}$$
(chain rule on the exponential) and apply Newton. This is literally what the Voltaic simulator does, many times per second, for every diode and transistor in your circuit.

### Experiment 5 — solve the circuit
**Predict first:** silicon diodes "drop about 0.6 to 0.7 V". With $V=5$ V and $R=1\ \text{k}\Omega$, roughly what current flows? Then run. Afterwards change the starting guess from `0.6` to `0.0` and see what happens — and why simulators limit the size of a Newton step.
''')
B.code(r'''
V, R, Is, VT = 5.0, 1000.0, 1e-12, 0.02585           # volts, ohms, amperes, volts

def f(v):  return (V - v) / R - Is * (exp(v / VT) - 1)
def fp(v): return -1 / R - Is / VT * exp(v / VT)

v = 0.6                                              # starting guess  <- try 0.0 as well
for step in range(1, 13):
    v_new = v - f(v) / fp(v)
    print(f'step {step:2d}:  v = {v_new:.9f} V     change = {v_new - v:+.2e}')
    if abs(v_new - v) < 1e-12: break
    v = v_new
print(f'\ndiode voltage {v_new:.4f} V,   current {(V - v_new) / R * 1000:.3f} mA')
''')
B.md(r'''
*Explain:* from $0.6$ V the method settles in a handful of steps at about $0.574$ V and $4.43$ mA. From $0$ V the first tangent is almost flat ($e^{0}$ is tiny compared with what it will become), so the first step overshoots to about $5$ V; from there each step only comes down by about $V_T=26$ mV, and 12 steps are nowhere near enough. Circuit simulators therefore **limit the voltage change per Newton step** on every diode junction.
''')
B.ask(r'''Do **one** Newton step by hand for $f(x)=x^2-5$ starting from $x_0=2$. What is $x_1$?''', 'num', 2.25,
      r'''$f(2)=-1$, $f'(2)=4$. $\;x_1=2-\dfrac{-1}{4}=2.25$. (True root: $\sqrt5=2.2360\ldots$)''',
      r'''$x_1=x_0-\dfrac{f(x_0)}{f'(x_0)}$ with $f(2)=4-5$ and $f'(x)=2x$.''')

B.md(r'''
## Week summary — everything on one page

**Implicit differentiation.** Differentiate both sides with respect to $x$; each $y$-term gets a factor $y'$ (chain rule); solve for $y'$.
$$\frac{d}{dx}\arcsin x=\frac{1}{\sqrt{1-x^2}},\qquad\frac{d}{dx}\arccos x=-\frac{1}{\sqrt{1-x^2}},\qquad\frac{d}{dx}\arctan x=\frac{1}{1+x^2}.$$

**Related rates.** Letters for everything that changes → equation → differentiate with respect to $t$ → *then* numbers → solve.

**Linear approximation.** $f(a+h)\approx f(a)+f'(a)h$, error $\approx\frac12f''(a)h^2$.
$\sin x\approx x$, $\;e^x\approx1+x$, $\;\ln(1+x)\approx x$, $\;(1+x)^n\approx1+nx$.
Errors: $\Delta y\approx f'(x)\Delta x$; for $y=c\,x^mz^n$: $\frac{\Delta y}{y}\approx m\frac{\Delta x}{x}+n\frac{\Delta z}{z}$.

**Newton's method.** $x_{n+1}=x_n-\dfrac{f(x_n)}{f'(x_n)}$. Digits double per step near the root; can fail far from it.
''')

# =====================================================================================
B.md(r'''
---
# Problems

Paper first. First attempt counts. `hint(n)` → `solution(n)` → `mistake(n, '...')`.

### Implicit differentiation
''')
B.problem(S1, r'Find the slope of the curve $x^2+xy+y^2=7$ at the point $(2,1)$.', 'num', -1.25,
          [r"Differentiate term by term. $xy$ needs the product rule: $y+x\,y'$.", r"$2x+y+x\,y'+2y\,y'=0$. Collect the $y'$ terms."],
          r'''Check the point: $4+2+1=7$ ✓.

$$2x+(y+x\,y')+2y\,y'=0\ \Rightarrow\ y'(x+2y)=-(2x+y)\ \Rightarrow\ y'=-\frac{2x+y}{x+2y}.$$
At $(2,1)$: $y'=-\dfrac{4+1}{2+2}=-\dfrac54=$ **−1.25**.''')
B.problem(S1, r'Find $\dfrac{dy}{dx}$ at the point $(2,1)$ of the curve $x^3+y^3=9$.', 'num', -4,
          [r"$3x^2+3y^2\,y'=0$."],
          r'''Check: $8+1=9$ ✓.
$$3x^2+3y^2\,y'=0\ \Rightarrow\ y'=-\frac{x^2}{y^2}.$$
At $(2,1)$: $-\dfrac41=$ **−4**.''')
B.problem(S1, r"For $f(x)=\arctan(2x)$, find $f'\!\left(\tfrac12\right)$.", 'num', 1,
          [r"$\dfrac{d}{dx}\arctan(g)=\dfrac{g'}{1+g^2}$ with $g=2x$."],
          r'''$$f'(x)=\frac{2}{1+(2x)^2}=\frac{2}{1+4x^2},\qquad f'\!\left(\tfrac12\right)=\frac{2}{1+1}=1 .$$''')
B.problem(S1, r'Find the slope of $y=x^x$ at $x=2$. (Logarithmic differentiation.)', 'num', 4 * (math.log(2) + 1),
          [r'$\ln y=x\ln x$. Differentiate both sides.', r"$\dfrac{y'}{y}=\ln x+1$, so $y'=x^x(\ln x+1)$."],
          r'''$\ln y=x\ln x\ \Rightarrow\ \dfrac{y'}{y}=\ln x+1\ \Rightarrow\ y'=x^x(\ln x+1)$.

At $x=2$: $4(\ln2+1)\approx$ **6.773**.''', fmt='a number; you can type `4*(ln(2)+1)`')
B.md(r'''
### Related rates
''')
B.problem(S2, r'A $13$ m ladder leans against a wall. Its foot is pulled away at $0.5$ m/s. Find $\dfrac{dy}{dt}$ for the top (in m/s, **with its sign**) when the foot is $5$ m from the wall.', 'num', -5 * 0.5 / 12,
          [r'$x^2+y^2=169$. Differentiate with respect to $t$ before putting in numbers.', r'When $x=5$, $y=12$. Then $2x\,\dot x+2y\,\dot y=0$.'],
          r'''**Equation.** $x^2+y^2=169$.

**Differentiate.** $2x\dfrac{dx}{dt}+2y\dfrac{dy}{dt}=0\ \Rightarrow\ \dfrac{dy}{dt}=-\dfrac xy\,\dfrac{dx}{dt}$.

**Numbers.** $x=5\Rightarrow y=\sqrt{169-25}=12$; $\dfrac{dx}{dt}=0.5$.

$$\frac{dy}{dt}=-\frac{5}{12}\cdot0.5\approx-0.208\ \text{m/s}$$
(negative: the top moves down).''', fmt='m/s, with sign')
B.problem(S2, r'A spherical balloon is inflated at $200$ cm³/s. How fast is the radius growing (cm/s) when $r=10$ cm?', 'num', 200 / (4 * math.pi * 100),
          [r'$V=\frac43\pi r^3\Rightarrow\dfrac{dV}{dt}=4\pi r^2\dfrac{dr}{dt}$.'],
          r'''$$\frac{dV}{dt}=4\pi r^2\frac{dr}{dt}\ \Rightarrow\ \frac{dr}{dt}=\frac{200}{4\pi\cdot100}=\frac{1}{2\pi}\approx0.159\ \text{cm/s}.$$''', fmt='cm/s')
B.problem(S2, r'Water runs at $2$ m³/min into a conical tank (point down) of height $6$ m and top radius $3$ m. How fast is the water level rising (m/min) when the water is $2$ m deep?', 'num', 2 / math.pi,
          [r'Similar triangles: $\dfrac rh=\dfrac36$, so $r=\dfrac h2$. Write $V$ in terms of $h$ only.', r'$V=\dfrac{\pi}{12}h^3$, so $\dfrac{dV}{dt}=\dfrac\pi4h^2\dfrac{dh}{dt}$.'],
          r'''**Eliminate $r$.** $r=\dfrac h2$, so $V=\frac13\pi r^2h=\dfrac{\pi}{12}h^3$.

**Differentiate.** $\dfrac{dV}{dt}=\dfrac{\pi}{4}h^2\dfrac{dh}{dt}$.

**Numbers.** $2=\dfrac\pi4\cdot4\cdot\dfrac{dh}{dt}=\pi\dfrac{dh}{dt}$.

$$\frac{dh}{dt}=\frac2\pi\approx0.637\ \text{m/min}.$$''', fmt='m/min')
B.problem(S2, r'Two cars leave the same crossroads at the same time: A drives east at $60$ km/h, B drives north at $80$ km/h. How fast is the distance between them growing (km/h) after one hour?', 'num', 100,
          [r'Let $x$, $y$ be their distances from the crossroads and $z$ the distance between them: $z^2=x^2+y^2$.', r'$2z\dot z=2x\dot x+2y\dot y$. After one hour $x=60$, $y=80$, $z=100$.'],
          r'''$z^2=x^2+y^2\ \Rightarrow\ 2z\dfrac{dz}{dt}=2x\dfrac{dx}{dt}+2y\dfrac{dy}{dt}$.

After 1 h: $x=60$, $y=80$, $z=\sqrt{3600+6400}=100$.
$$\frac{dz}{dt}=\frac{60\cdot60+80\cdot80}{100}=\frac{10000}{100}=100\ \text{km/h}.$$
(Here the answer is the same at every moment: the triangle just scales up. A 3–4–5 triangle.)''', fmt='km/h')
B.md(r'''
### Linear approximation and errors
''')
B.problem(S3, r'Use the linear approximation at $0$ to estimate $e^{0.05}$.', 'num', 1.05,
          [r'$e^x\approx1+x$.'],
          r'''$e^{0.05}\approx1+0.05=$ **1.05**. (Exact: $1.05127$; the error $0.00127\approx\frac12\cdot0.05^2$.)''')
B.problem(S3, r'Use $\ln(1+x)\approx x$ to estimate the **doubling time in years** of money growing at $4\%$ per year: solve $(1.04)^t=2$, i.e. $t=\dfrac{\ln2}{\ln1.04}$, with the approximation in the denominator and $\ln2\approx0.693$.', 'num', 0.693 / 0.04,
          [r'$\ln1.04=\ln(1+0.04)\approx0.04$.'],
          r'''$\ln(1.04)\approx0.04$, so $t\approx\dfrac{0.693}{0.04}\approx$ **17.3 years**. (Exact: $17.67$.)

This is the banker's "rule of 70": doubling time ≈ 70 ÷ (percentage rate).''', fmt='years')
B.problem(S3, r'The side of a cube is measured as $10$ cm $\pm\,0.1$ cm. Estimate the possible error in the computed **volume** (in cm³).', 'num', 30,
          [r"$\Delta V\approx V'(s)\,\Delta s$ with $V=s^3$."],
          r'''$V=s^3$, $V'(s)=3s^2$.
$$\Delta V\approx3\cdot10^2\cdot0.1=30\ \text{cm}^3 .$$
Relative: $\dfrac{30}{1000}=3\%$, three times the 1 % error in the side.''', fmt='cm³')
B.problem(S3, r'The power dissipated in a resistor is $P=\dfrac{V^2}{R}$. $V$ is known to $1\%$ and $R$ to $2\%$. What is the worst-case relative error in $P$ (in %)?', 'num', 4,
          [r'$P=V^{2}R^{-1}$. Relative errors add, weighted by the powers; worst case: add the sizes.'],
          r'''$P=V^2R^{-1}$:
$$\frac{\Delta P}{P}\approx2\,\frac{\Delta V}{V}-1\cdot\frac{\Delta R}{R}.$$
Worst case (errors of opposite sign): $2\cdot1\%+2\%=$ **4 %**.''', fmt='a number (percent)')
B.md(r'''
### Newton's method
''')
B.problem(S4, r'Do **two** Newton steps by hand for $x^3-2=0$ starting from $x_0=1$. Give $x_2$.', 'num', 1.2638888888888888,
          [r"$f(x)=x^3-2$, $f'(x)=3x^2$. First step: $x_1=1-\dfrac{-1}{3}$.", r"$x_1=\frac43$. Then $f(\frac43)=\frac{64}{27}-2=\frac{10}{27}$ and $f'(\frac43)=\frac{16}{3}$."],
          r'''$f(x)=x^3-2$, $f'(x)=3x^2$.

**Step 1.** $x_1=1-\dfrac{1-2}{3}=1+\dfrac13=\dfrac43\approx1.3333$.

**Step 2.** $f\!\left(\tfrac43\right)=\dfrac{64}{27}-2=\dfrac{10}{27}$, $\;f'\!\left(\tfrac43\right)=3\cdot\dfrac{16}{9}=\dfrac{16}{3}$.
$$x_2=\frac43-\frac{10/27}{16/3}=\frac43-\frac{10}{144}=\frac{192-10}{144}=\frac{91}{72}\approx1.2639 .$$
(True value $\sqrt[3]{2}=1.25992$.)''')
B.problem(S4, r'For $f(x)=x^2-a$, Newton’s formula becomes $x_{n+1}=\frac12\left(x_n+\dfrac{a}{x_n}\right)$. Use it once to improve the guess $x_0=3$ for $\sqrt{10}$.', 'num', 19 / 6,
          [r'Average of 3 and $\frac{10}{3}$.'],
          r'''$$x_1=\frac12\left(3+\frac{10}{3}\right)=\frac12\cdot\frac{19}{3}=\frac{19}{6}\approx3.1667 .$$
($\sqrt{10}=3.16228$: already three correct digits after one step.)''')
B.problem(S4, r'Use your `newton` function (or the loop of Experiment 5) to solve $\cos x=x$. Give the solution to at least 4 decimals.', 'num', 0.7390851332151607,
          [r"Write it as $f(x)=\cos x-x=0$, with $f'(x)=-\sin x-1$. Start from $x_0=1$."],
          r'''$f(x)=\cos x-x$, $f'(x)=-\sin x-1$.

`newton(lambda v: cos(v) - v, lambda v: -sin(v) - 1, 1.0)` gives $x\approx$ **0.739085**.

By hand, the first step from $x_0=1$: $x_1=1-\dfrac{\cos1-1}{-\sin1-1}=1-\dfrac{-0.4597}{-1.8415}=0.7504$ — already close.''')
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
1. Why does differentiating $y^2$ with respect to $x$ give $2y\,y'$ and not $2y$?
2. Derive the derivative of $\arctan x$.
3. The five steps of a related-rates problem — and which order mistake ruins everything?
4. Derive Newton's formula from the tangent-line equation.
5. One situation where Newton's method fails, and why bisection would not.

*Your answers:*

&nbsp;

### 3 · Lab strand — Newton's method at work in the circuit simulator (1 hour)
The Voltaic simulator below opens with the circuit of §4.3: a 9 V source, a $330\ \Omega$ resistor and an LED in series (an LED is a diode with a larger forward voltage, about 2 V). The simulator finds the operating point with Newton's method at every time step.

**Predict first:** if the LED drops about 2 V, what current flows? Then click the resistor and the LED and read their voltage and current. Now change the source to 18 V: **predict** how much the LED voltage will change — a lot, or hardly at all? (The diode equation says that doubling the current adds only about $V_T\ln2\approx18$ mV per unit of the diode's ideality factor.) You can rebuild the silicon-diode circuit of Experiment 5 yourself: replace the LED by a *Diode* and set $V=5$ V, $R=1\ \text{k}\Omega$.
''')
B.code(r'''
lab('voltaic', height=680, preset='led')
''')
B.md(r'''
### 4 · What comes next
**Week 4** — the last of the unit — uses $f'$ and $f''$ to find where a function is largest or smallest, and applies that to design problems: the box of largest volume, the load that draws the most power, the launch angle of greatest range.
''')

if __name__ == '__main__':
    B.write()
