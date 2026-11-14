"""Unit 4 · Week 2 (course week 12) - Power series and Taylor expansions."""
import math
from nbkit import Book
import figs_u04 as F

B = Book('u04w2', 'Unit 4 · Week 2 — Power series and Taylor expansions', 'year1/u04w2-power-taylor-series.ipynb')
S1, S2, S3, S4 = '1 Power series', '2 Taylor polynomials', '3 Error and approximation', '4 Applications'

B.md(r'''
# Unit 4 · Week 2 — Power series and Taylor expansions
*Term 1, week 12 of 12 · about 15 hours in this notebook and on paper*

**Where you are.** Last week: infinite sums, the geometric series, and tests that decide convergence. This week those tools produce one of the most useful ideas in all of mathematics and engineering: **a smooth function can be written as an "infinite polynomial"**,
$$f(x)=c_0+c_1x+c_2x^2+c_3x^3+\dots$$
Polynomials only need $+$ and $\times$. So this is how a calculator computes $\sin x$ and $e^x$, how physicists simplify equations ("to first order…"), and how every approximation of this course so far ($\sin x\approx x$, $e^x\approx1+x$, $\cos x\approx1-\frac{x^2}{2}$) fits into one picture.

**What you will be able to do at the end of this week**
1. Find the interval in which a power series converges (ratio test).
2. Produce new series from the geometric series by substituting, differentiating and integrating — and get series for $\ln(1+x)$ and $\arctan x$.
3. **Derive** the Taylor coefficients $\frac{f^{(n)}(a)}{n!}$ from "match the value, the slope, the curvature, …", and write down the series of $e^x$, $\sin x$, $\cos x$, $(1+x)^\alpha$.
4. Bound the error of a Taylor polynomial and decide how many terms are needed.
5. Apply it: limits, the pendulum's period at large swings, computing $e$ and $\pi$, and a first look at $e^{i\theta}=\cos\theta+i\sin\theta$.

Run the grey *SETUP* cell first.
''')

# =====================================================================================
B.md(r'''
---
# Part 1 — Power series

## 1.1 The geometric series as a function

**Build.** Last week, for $|x|<1$:
$$1+x+x^2+x^3+\dots=\frac{1}{1-x}.$$
Read it the other way round: **the function $\frac1{1-x}$ equals an infinite polynomial**, as long as $|x|<1$. Outside that interval the left side is meaningless (it diverges), while the right side is perfectly fine (except at $x=1$). The series describes the function only on part of its domain.

**Definition.** A **power series** (around 0) is
$$\sum_{n=0}^{\infty}c_nx^n=c_0+c_1x+c_2x^2+\dots$$
For each $x$ it is an ordinary series of numbers, which converges or not.

## 1.2 Where does it converge? The radius of convergence

**Build.** Apply the ratio test (last week, §4.3) to the terms $c_nx^n$:
$$\left|\frac{c_{n+1}x^{n+1}}{c_nx^n}\right|=\left|\frac{c_{n+1}}{c_n}\right|\cdot|x|\ \longrightarrow\ \frac{|x|}{R}\qquad\text{where }\ \frac1R=\lim\left|\frac{c_{n+1}}{c_n}\right| .$$
The series converges when this is below 1, i.e. $|x|<R$, and diverges when $|x|>R$. $R$ is the **radius of convergence**: the series works on the interval $(-R,R)$. (At the two end points anything can happen — check them separately if needed.)

**Worked example 1.** $\sum x^n$: $c_n=1$, ratio 1, $R=1$ ✓.

**Worked example 2.** $\sum\frac{x^n}{n}$ (from your diagnostic): $\left|\dfrac{c_{n+1}}{c_n}\right|=\dfrac{n}{n+1}\to1$, so $R=1$.

**Worked example 3.** $\sum\frac{x^n}{n!}$: $\dfrac{c_{n+1}}{c_n}=\dfrac{1}{n+1}\to0$, so $R=\infty$: it converges for **every** $x$.

**Worked example 4.** $\sum n!\,x^n$: ratio $(n+1)\to\infty$, so $R=0$: useless except at $x=0$.
''')
B.ask(r'''What is the radius of convergence of $\displaystyle\sum_{n=0}^\infty\frac{x^n}{3^n}$?''', 'num', 3,
      r'''It is geometric with ratio $\frac x3$: converges iff $|x|<3$. (Ratio test: $\frac{c_{n+1}}{c_n}=\frac13$, so $R=3$.)''',
      r'''$c_n=3^{-n}$; compute $\lim|c_{n+1}/c_n|=\frac1R$.''')

B.md(r'''
## 1.3 New series from old

**Build.** Inside its radius of convergence a power series can be treated like a polynomial: you may **substitute**, **differentiate term by term** and **integrate term by term**. *(These facts need proof — they are true because inside the radius the series converges "uniformly enough"; we use them.)*

**(a) Substitute.** Put $-x$ for $x$ in the geometric series:
$$\frac{1}{1+x}=1-x+x^2-x^3+\dots\qquad(|x|<1).$$
Put $-x^2$ for $x$:
$$\frac{1}{1+x^2}=1-x^2+x^4-x^6+\dots\qquad(|x|<1).$$

**(b) Integrate.** $\ln(1+x)=\int_0^x\frac{dt}{1+t}$, so integrate the series of $\frac1{1+t}$ term by term:
$$\boxed{\,\ln(1+x)=x-\frac{x^2}{2}+\frac{x^3}{3}-\frac{x^4}{4}+\dots\qquad(-1<x\le1)\,}$$
At $x=1$ this is the alternating harmonic series of last week: $1-\frac12+\frac13-\dots=\ln2$ — promise kept.

Likewise $\arctan x=\int_0^x\frac{dt}{1+t^2}$:
$$\boxed{\,\arctan x=x-\frac{x^3}{3}+\frac{x^5}{5}-\frac{x^7}{7}+\dots\qquad(|x|\le1)\,}$$
At $x=1$: $\;\dfrac\pi4=1-\dfrac13+\dfrac15-\dfrac17+\dots$ (Leibniz's series — beautiful, but slow; §4.3 does better.)

**(c) Differentiate.** Differentiate $\frac{1}{1-x}=\sum x^n$:
$$\frac{1}{(1-x)^2}=1+2x+3x^2+4x^3+\dots$$

**A puzzle that the radius explains.** $\frac{1}{1+x^2}$ is smooth for **every** real $x$ — no division by zero, no corner. Yet its series stops working at $|x|=1$:
''')
B.fig('radius', F.radius, 'More terms help inside |x| < 1 and make things worse outside it.')
B.md(r'''
Why? Because $1+x^2=0$ at $x=\pm i$ — at *complex* numbers a distance 1 from 0. The radius of convergence is the distance to the nearest point where the function breaks down, and that point may be off the real line. This is a first hint that complex numbers (Unit 6) are not optional extras.
''')
B.ask(r'''Use the series of $\ln(1+x)$ with three terms to estimate $\ln(1.1)$.''', 'num', 0.1 - 0.005 + 0.001 / 3,
      r'''$0.1-\frac{0.01}{2}+\frac{0.001}{3}=0.1-0.005+0.000333=0.095333$. (True: $0.095310$; the error is below the next term, $\frac{0.0001}{4}$.)''',
      r'''$x-\frac{x^2}{2}+\frac{x^3}{3}$ with $x=0.1$.''')

# =====================================================================================
B.md(r'''
---
# Part 2 — Taylor polynomials and Taylor series

## 2.1 The idea: copy the function at one point

**Why.** Substituting into the geometric series works for a few functions. For $e^x$, $\sin x$ or $\sqrt{1+x}$ we need a systematic method. The question is: *which polynomial imitates $f$ best near a point?*

**Build.** Near $x=0$, ask a polynomial to agree with $f$ in more and more respects:
''')
B.fig('match_derivs', F.match_derivs, 'Copying the value, then the slope, then the curvature of e^x at 0.')
B.md(r'''
- **degree 0**: the same value, $p(0)=f(0)$: a constant. (Unit 1: crude.)
- **degree 1**: also the same slope, $p'(0)=f'(0)$: the tangent line. (Unit 2: the linear approximation.)
- **degree 2**: also the same curvature, $p''(0)=f''(0)$. (Unit 2 week 3 found the error term $\frac12f''h^2$ — this is it.)
- … and so on: each extra degree copies one more derivative.

## 2.2 Finding the coefficients

**Build.** Let $p(x)=c_0+c_1x+c_2x^2+c_3x^3+\dots+c_nx^n$. Differentiate repeatedly and put $x=0$ each time — all terms with a leftover $x$ vanish:

| | at $x=0$ |
|---|---|
| $p(x)=c_0+c_1x+c_2x^2+c_3x^3+\dots$ | $p(0)=c_0$ |
| $p'(x)=c_1+2c_2x+3c_3x^2+\dots$ | $p'(0)=c_1$ |
| $p''(x)=2c_2+3\cdot2\,c_3x+\dots$ | $p''(0)=2c_2$ |
| $p^{\prime\prime\prime}(x)=3\cdot2\,c_3+\dots$ | $p^{\prime\prime\prime}(0)=3\cdot2\cdot1\,c_3=3!\,c_3$ |
| in general | $p^{(k)}(0)=k!\,c_k$ |

Requiring $p^{(k)}(0)=f^{(k)}(0)$ gives every coefficient:
$$\boxed{\,c_k=\frac{f^{(k)}(0)}{k!}\,}$$

The **Taylor polynomial of degree $n$** (around 0; also called *Maclaurin*) and, letting $n\to\infty$, the **Taylor series**:
$$f(x)\approx f(0)+f'(0)\,x+\frac{f''(0)}{2!}x^2+\frac{f^{\prime\prime\prime}(0)}{3!}x^3+\dots+\frac{f^{(n)}(0)}{n!}x^n .$$
Around another point $a$, replace $x$ by $(x-a)$ and the derivatives at 0 by those at $a$:
$$f(x)\approx\sum_{k=0}^{n}\frac{f^{(k)}(a)}{k!}(x-a)^k .$$

## 2.3 The great series

**$e^x$.** Every derivative is $e^x$, which is $1$ at $0$. So $c_k=\frac1{k!}$:
$$\boxed{\,e^x=1+x+\frac{x^2}{2!}+\frac{x^3}{3!}+\frac{x^4}{4!}+\dots\qquad\text{for all }x\,}$$
($R=\infty$ by §1.2 example 3.) At $x=1$: $e=\sum\frac1{k!}$, as found last week.

**$\sin x$.** Derivatives cycle (Unit 2 week 2): $\sin,\cos,-\sin,-\cos,\sin,\dots$, which at 0 are $0,1,0,-1,0,1,\dots$ Only odd powers survive, with alternating signs:
$$\boxed{\,\sin x=x-\frac{x^3}{3!}+\frac{x^5}{5!}-\frac{x^7}{7!}+\dots\,}$$

**$\cos x$.** At 0 the derivatives are $1,0,-1,0,1,\dots$: even powers only.
$$\boxed{\,\cos x=1-\frac{x^2}{2!}+\frac{x^4}{4!}-\frac{x^6}{6!}+\dots\,}$$
Both for all $x$. *Checks:* $\sin$ is odd and has only odd powers; $\cos$ is even, only even powers; differentiating the sine series term by term gives the cosine series.

**$(1+x)^\alpha$, the binomial series**, for any real $\alpha$. Derivatives: $\alpha(1+x)^{\alpha-1}$, $\alpha(\alpha-1)(1+x)^{\alpha-2}$, … At 0: $\alpha$, $\alpha(\alpha-1)$, $\alpha(\alpha-1)(\alpha-2)$, …
$$\boxed{\,(1+x)^\alpha=1+\alpha x+\frac{\alpha(\alpha-1)}{2!}x^2+\frac{\alpha(\alpha-1)(\alpha-2)}{3!}x^3+\dots\qquad(|x|<1)\,}$$
For a whole number $\alpha$ the series stops (it is the ordinary binomial theorem). For $\alpha=\frac12$: $\sqrt{1+x}=1+\frac x2-\frac{x^2}{8}+\frac{x^3}{16}-\dots$

**Now every approximation of the course has its place:** $\sin x\approx x$, $\cos x\approx1-\frac{x^2}2$, $e^x\approx1+x$, $\ln(1+x)\approx x$, $(1+x)^n\approx1+nx$ are simply the first one or two terms of these series — and the series tell you what the **next** term (the error) is.
''')
B.fig('taylor_sin', F.taylor_sin, 'Each extra term extends the range where the polynomial follows the sine.')
B.md(r'''
### Experiment 1 — Taylor polynomials with a slider
**Predict first:** for $\sin x$ around 0 with degree 5, beyond roughly which $x$ does the polynomial visibly leave the curve? Does $\ln(1+x)$ ever fit beyond $x=1$, however many terms? And what happens when you move the centre $a$?
''')
B.code(r'''
FUN = {'sin': (np.sin, lambda k, a: [np.sin(a), np.cos(a), -np.sin(a), -np.cos(a)][k % 4]),
       'exp': (np.exp, lambda k, a: np.exp(a)),
       'ln(1+x)': (lambda v: np.log1p(v), lambda k, a: np.log1p(a) if k == 0 else (-1) ** (k + 1) * math.factorial(k - 1) / (1 + a) ** k)}

def taylor_view(func='sin', degree=5, a=0.0):
    f, d = FUN[func]
    xs = np.linspace(-6, 6, 800)
    xs_f = xs[xs > -0.999] if func == 'ln(1+x)' else xs
    p = sum(d(k, a) / math.factorial(k) * (xs - a) ** k for k in range(degree + 1))
    plt.figure(figsize=(8.5, 3.8))
    plt.plot(xs_f, f(xs_f), 'k', lw=3, label=func)
    plt.plot(xs, p, 'r', lw=1.8, label=f'Taylor polynomial, degree {degree}, centre {a}')
    plt.plot([a], [f(np.array([a]))[0]], 'bo'); plt.ylim(-3, 5); plt.axhline(0, color='k', lw=0.8); plt.legend(loc='upper left'); plt.show()

explore(taylor_view, func=['sin', 'exp', 'ln(1+x)'], degree=(0, 25, 1, 5), a=(-2, 2, 0.5, 0))
''')
B.ask(r'''What is the coefficient of $x^4$ in the Taylor series of $e^x$? *(From your diagnostic.)*''', 'num', 1 / 24,
      r'''$c_4=\frac{1}{4!}=\frac1{24}\approx0.0417$.''',
      r'''$c_k=\frac{f^{(k)}(0)}{k!}$ and every derivative of $e^x$ is 1 at 0.''', fmt='a number, e.g. `1/24`')
B.ask(r'''Write the Taylor series of $e^{-x^2}$ by substituting into the series of $e^u$. What is the coefficient of $x^4$?''', 'num', 0.5,
      r'''$e^{u}=1+u+\frac{u^2}{2}+\dots$ with $u=-x^2$: $1-x^2+\frac{x^4}{2}-\dots$ Coefficient $\frac12$.''',
      r'''Put $u=-x^2$ into $1+u+\frac{u^2}{2!}+\dots$; $u^2=x^4$.''', fmt='a number, e.g. `1/2`')

# =====================================================================================
B.md(r'''
---
# Part 3 — How large is the error?

## 3.1 Taylor's theorem with remainder

**Why.** "More terms are better" is not enough for engineering. You need: *how many terms for 6 correct decimals?* or *how far from $a$ is the approximation good to 1 %?*

**The result (Lagrange form of the remainder).** If $f$ has $n+1$ derivatives, then
$$f(x)=\underbrace{\sum_{k=0}^{n}\frac{f^{(k)}(a)}{k!}(x-a)^k}_{\text{Taylor polynomial }p_n(x)}+\underbrace{\frac{f^{(n+1)}(\xi)}{(n+1)!}(x-a)^{n+1}}_{\text{remainder }R_n(x)}$$
for some point $\xi$ between $a$ and $x$. In words: **the error looks like the next term**, but with the derivative evaluated at an unknown point in between.

*(Why it is true, for $n=0$: it is exactly the mean value theorem of Unit 2 week 4, $f(x)-f(a)=f'(\xi)(x-a)$. The general case is proved by applying the same idea repeatedly; we use the result.)*

**How to use it.** You never know $\xi$, but you can bound $|f^{(n+1)}|$ on the interval by some $M$:
$$|R_n(x)|\le\frac{M}{(n+1)!}\,|x-a|^{n+1}.$$

**Worked example 1 — $e$ to 6 decimals.** $f=e^x$, $a=0$, $x=1$. All derivatives are $e^\xi\le e<3$ on $[0,1]$. So $|R_n|\le\frac{3}{(n+1)!}$. We need this below $5\times10^{-7}$: $(n+1)!>6\times10^6$. $10!=3\,628\,800$ is not enough, $11!=39\,916\,800$ is. So $n=10$: **11 terms** $\sum_{k=0}^{10}\frac1{k!}$ (matching last week's Experiment 1).

**Worked example 2 — $\sin(0.1)$.** Using $x-\frac{x^3}{6}$: this is $p_4$ as well (the $x^4$ coefficient is zero), so the error is at most $\frac{|x|^5}{5!}$ (all derivatives of sin are at most 1): $\frac{10^{-5}}{120}\approx8\times10^{-8}$. Two terms give 7 correct decimals.

**Worked example 3 — when is $\sin x\approx x$ good to 1 %?** The error is about $\frac{x^3}{6}$; relative to $x$ that is $\frac{x^2}{6}<0.01$, so $|x|<0.245$ rad $\approx14^\circ$. That is the "small angle" of the pendulum, made precise.

## 3.2 Limits, the easy way

Taylor series turn many hard limits into arithmetic:
$$\frac{\sin x-x}{x^3}=\frac{\left(x-\frac{x^3}{6}+\frac{x^5}{120}-\dots\right)-x}{x^3}=-\frac16+\frac{x^2}{120}-\dots\ \longrightarrow\ -\frac16 ,$$
the limit that needed L'Hôpital three times in Unit 2.
$$\frac{1-\cos x}{x^2}=\frac{\frac{x^2}{2}-\frac{x^4}{24}+\dots}{x^2}\to\frac12,\qquad\frac{e^x-1-x}{x^2}=\frac{\frac{x^2}{2}+\frac{x^3}{6}+\dots}{x^2}\to\frac12 .$$

### Experiment 2 — write the exponential and the sine yourself
Complete the two functions. Each new term comes from the previous one by one multiplication — never compute large powers or factorials directly. The tests compare with Python's built-in functions.
''')
B.code(r'''
def my_exp(x, n=20):
    """e^x from the first n+1 terms of its Taylor series."""
    term, total = 1.0, 1.0            # the k = 0 term
    for k in range(1, n + 1):
        term = ...                    # (1) next term from the previous one:  x^k/k! = (x^(k-1)/(k-1)!) * x / k
        total = total + term
    return total

def my_sin(x, n=10):
    """sin x from the terms x - x^3/3! + x^5/5! - ... (n terms)."""
    term, total = x, x
    for k in range(1, n):
        term = ...                    # (2) next term: multiply by  -x² / ((2k)(2k+1))
        total = total + term
    return total


# ---------- tests: do not change ----------
def test_series():
    good = 0
    for name, mine, ref, xs in [('my_exp', my_exp, exp, [0, 1, -2, 3.5]), ('my_sin', my_sin, sin, [0.1, 1, 2.5, -3])]:
        for v in xs:
            try:
                r = float(mine(v))
            except Exception as err:
                print('✗', name, '-> not working yet (have you replaced the ... ?)'); break
            ok = abs(r - ref(v)) < 1e-9 * max(1, abs(ref(v))); good += ok
            print('✓' if ok else '✗', f'{name}({v}) = {r:.12f}   built-in: {ref(v):.12f}')
    print('\nAll tests passed.' if good == 8 else '\nNot there yet - see the comments for the update rules.')

test_series()
''', ref=r'''
def my_exp(x, n=20):
    term, total = 1.0, 1.0
    for k in range(1, n + 1):
        term = term * x / k
        total = total + term
    return total

def my_sin(x, n=10):
    term, total = x, x
    for k in range(1, n):
        term = term * (-x * x) / ((2 * k) * (2 * k + 1))
        total = total + term
    return total
print(my_exp(1.0), my_sin(1.0))
''')
B.ask(r'''What is the coefficient of $x^5$ in the Taylor series of $\sin x$?''', 'num', 1 / 120,
      r'''$+\frac{x^5}{5!}=\frac{x^5}{120}$: coefficient $\frac1{120}$.''',
      r'''The signs alternate $+,-,+$ for $x$, $x^3$, $x^5$; the denominators are odd factorials.''', fmt='a number, e.g. `1/120`')
B.ask(r'''Bound the error of $\cos x\approx1-\frac{x^2}{2}$ at $x=0.5$ by the next term of the series, $\frac{x^4}{4!}$.''', 'num', 0.5 ** 4 / 24,
      r'''$\frac{0.5^4}{24}=\frac{0.0625}{24}\approx0.0026$. (True error: $0.0026$ — the next term is an excellent estimate.)''',
      r'''Compute $\frac{0.5^4}{24}$.''')
B.ask(r'''Using $(1+x)^\alpha\approx1+\alpha x+\frac{\alpha(\alpha-1)}{2}x^2$, estimate $\sqrt{1.2}$ (three terms).''', 'num', 1 + 0.1 - 0.005,
      r'''$\alpha=\frac12$, $x=0.2$: $1+0.1+\frac{\frac12(-\frac12)}{2}\cdot0.04=1+0.1-0.005=1.095$. (True: $1.09545$.)''',
      r'''$\alpha=\frac12$: the $x^2$ coefficient is $\frac{\frac12\cdot(-\frac12)}{2}=-\frac18$.''')
B.md(r'''
**How a calculator computes $\sin x$.** It never sums the series for a large $x$ (for $x=100$ the terms first grow to about $10^{42}$ before shrinking — rounding would destroy the answer). Instead: (1) **reduce** the angle using periodicity and symmetry ($\sin(x+2\pi)=\sin x$, $\sin(\pi-x)=\sin x$, $\sin x=\cos(\frac\pi2-x)$, Unit 1) to $0\le x\le\frac\pi4$; (2) there, a few terms suffice:
''')
B.fig('calc_sin', F.calc_sin, 'On [0, π/4] four terms of the sine series are already accurate to better than 1e-8 (built-in libraries use slightly tuned coefficients and a few more terms).')
B.ask(r'''Using the series, find $\displaystyle\lim_{x\to0}\frac{x-\arctan x}{x^3}$.''', 'num', 1 / 3,
      r'''$\arctan x=x-\frac{x^3}{3}+\dots$, so $x-\arctan x=\frac{x^3}{3}-\dots$ and the limit is $\frac13$.''',
      r'''Write $\arctan x=x-\frac{x^3}{3}+\frac{x^5}{5}-\dots$ and simplify the top.''', fmt='a number, e.g. `1/3`')

# =====================================================================================
B.md(r'''
---
# Part 4 — Applications

## 4.1 The pendulum beyond small swings

**Why.** In Unit 1 you used $\sin\theta\approx\theta$ for the pendulum. The resulting period $T_0=2\pi\sqrt{L/g}$ does not depend on the amplitude — the property that made pendulum clocks possible. Is it really independent? Series answer this.
''')
B.fig('pendulum', F.pendulum, 'A pendulum of length L released at angle θ₀.')
B.md(r'''
**The result.** The exact period of a pendulum released at angle $\theta_0$ is an integral (from energy conservation) that has no elementary formula. Expanding it in a series in $\theta_0$ gives
$$T=2\pi\sqrt{\frac Lg}\left(1+\frac{\theta_0^2}{16}+\frac{11\,\theta_0^4}{3072}+\dots\right).$$
*(Deriving the coefficients needs the binomial series inside an integral; the first correction $\frac{\theta_0^2}{16}$ is what matters.)*

**Reading it.** At $\theta_0=10^\circ=0.175$ rad the correction is $\frac{0.0305}{16}=0.19\,\%$ — about 2.7 minutes per day for a clock. At $60^\circ$ it is already 7 %. The small-angle formula is the first term of a series, and now you know the size of the next one.

### Experiment 3 — measure it in a simulation
The cell simulates the full pendulum $\ddot\theta=-\frac gL\sin\theta$ with the Runge–Kutta method (no small-angle approximation), measures the period, and compares with the series.

**Predict first:** at $90^\circ$, is the true period longer or shorter than the small-angle period, and by roughly how much (use the series)?
''')
B.code(r'''
def period(theta0_deg, L=1.0, g=9.81, dt=1e-4):
    th, w, t = radians(theta0_deg), 0.0, 0.0
    f = lambda th_, w_: (w_, -g / L * np.sin(th_))
    crossed = []
    prev = th
    while len(crossed) < 2 and t < 20:
        k1 = f(th, w); k2 = f(th + dt / 2 * k1[0], w + dt / 2 * k1[1]); k3 = f(th + dt / 2 * k2[0], w + dt / 2 * k2[1]); k4 = f(th + dt * k3[0], w + dt * k3[1])
        th_new = th + dt / 6 * (k1[0] + 2 * k2[0] + 2 * k3[0] + k4[0]); w = w + dt / 6 * (k1[1] + 2 * k2[1] + 2 * k3[1] + k4[1])
        if th > 0 >= th_new or th < 0 <= th_new: crossed.append(t + dt * th / (th - th_new))
        th, t = th_new, t + dt
    return 2 * (crossed[1] - crossed[0])          # two zero crossings = half a period

T0 = 2 * pi * sqrt(1 / 9.81)
rows = []
for a in [5, 10, 20, 30, 45, 60, 90, 120]:
    s = radians(a)
    rows.append([a, period(a), T0, T0 * (1 + s**2 / 16), T0 * (1 + s**2 / 16 + 11 * s**4 / 3072)])
table(['amplitude (°)', 'simulated T (s)', 'small angle', '+ θ²/16', '+ 11θ⁴/3072'], rows, fmt='%.5f')
''')
B.md(r'''
*Explain:* up to about $20^\circ$ the first correction alone matches the simulation to $10^{-4}$ s; around $45^\circ$ the second term is needed for that accuracy; at $90^\circ$ two terms are still $0.4\,\%$ short and at $120^\circ$ about $2\,\%$. The series is exact in the limit but useful in a range — the general lesson of this week.

## 4.2 Computing $\pi$

Leibniz's series $\frac\pi4=1-\frac13+\frac15-\dots$ needs 500 terms for three decimals. A trick of John Machin (1706) uses the addition formula for $\tan$ (Unit 1 week 2) to show
$$\frac\pi4=4\arctan\frac15-\arctan\frac1{239}.$$
Now the arctan series has $x=\frac15$ and $x=\frac1{239}$: each term is 25 (or 57 121) times smaller than the one before. Ten terms give 14 correct digits; Machin computed 100 digits by hand.
''')
B.code(r'''
def arctan_series(x, n):
    return sum((-1) ** k * x ** (2 * k + 1) / (2 * k + 1) for k in range(n))

for n in [1, 2, 3, 5, 10]:
    machin = 4 * (4 * arctan_series(1 / 5, n) - arctan_series(1 / 239, n))
    leibniz = 4 * arctan_series(1, n)
    print(f'{n:2d} terms:   Machin {machin:.15f}   error {abs(machin - pi):.1e}     Leibniz error {abs(leibniz - pi):.1e}')
''')
B.md(r'''
## 4.3 A first look at $e^{i\theta}$

**Build.** The series of $e^x$ makes sense for any number you can multiply — including the imaginary unit $i$ with $i^2=-1$ (Unit 6 develops complex numbers properly; here we only *calculate formally*). Put $x=i\theta$ and use $i^2=-1$, $i^3=-i$, $i^4=1$:
$$e^{i\theta}=1+i\theta-\frac{\theta^2}{2!}-i\frac{\theta^3}{3!}+\frac{\theta^4}{4!}+i\frac{\theta^5}{5!}-\dots$$
Collect the terms without $i$ and those with $i$:
$$e^{i\theta}=\underbrace{\left(1-\frac{\theta^2}{2!}+\frac{\theta^4}{4!}-\dots\right)}_{\cos\theta}+i\underbrace{\left(\theta-\frac{\theta^3}{3!}+\frac{\theta^5}{5!}-\dots\right)}_{\sin\theta}$$
$$\boxed{\,e^{i\theta}=\cos\theta+i\sin\theta\,}\qquad\text{Euler's formula.}$$
At $\theta=\pi$: $e^{i\pi}=-1$. The exponential, the trigonometric functions, and the imaginary unit are one family. In Unit 6 this formula turns the addition formulas of Unit 1 into one line ($e^{i(a+b)}=e^{ia}e^{ib}$) and turns every AC circuit calculation into algebra.

*(Honesty note: we added the terms of a series in a different order and allowed complex numbers in it; both are justified for this series — it converges "absolutely" — but that is proved in Unit 6.)*
''')
B.code(r'''
theta = pi / 3
series = sum((1j * theta) ** k / math.factorial(k) for k in range(25))
print('series for e^(i θ):', series)
print('cos θ + i sin θ   :', complex(cos(theta), sin(theta)))
''')
B.ask(r'''Using $e^{i\theta}=\cos\theta+i\sin\theta$: what is the real part of $e^{i\pi/2}$?''', 'num', 0,
      r'''$e^{i\pi/2}=\cos\frac\pi2+i\sin\frac\pi2=0+i\cdot1=i$. Real part 0.''',
      r'''$\cos\frac\pi2=0$.''')

B.md(r'''
## Week summary — everything on one page

**Power series** $\sum c_nx^n$ converge for $|x|<R$, $\frac1R=\lim\left|\frac{c_{n+1}}{c_n}\right|$. Inside: substitute, differentiate, integrate term by term.

**Taylor series** $f(x)=\sum\frac{f^{(k)}(a)}{k!}(x-a)^k$ — copy value, slope, curvature, …

| function | series | valid |
|---|---|---|
| $\frac{1}{1-x}$ | $1+x+x^2+\dots$ | $\lvert x\rvert<1$ |
| $e^x$ | $1+x+\frac{x^2}{2!}+\frac{x^3}{3!}+\dots$ | all $x$ |
| $\sin x$ | $x-\frac{x^3}{3!}+\frac{x^5}{5!}-\dots$ | all $x$ |
| $\cos x$ | $1-\frac{x^2}{2!}+\frac{x^4}{4!}-\dots$ | all $x$ |
| $\ln(1+x)$ | $x-\frac{x^2}{2}+\frac{x^3}{3}-\dots$ | $-1<x\le1$ |
| $\arctan x$ | $x-\frac{x^3}{3}+\frac{x^5}{5}-\dots$ | $\lvert x\rvert\le1$ |
| $(1+x)^\alpha$ | $1+\alpha x+\frac{\alpha(\alpha-1)}{2!}x^2+\dots$ | $\lvert x\rvert<1$ |

**Error.** $|R_n|\le\dfrac{M}{(n+1)!}|x-a|^{n+1}$ — the size of the next term. For alternating series: at most the first omitted term.

**Uses.** Approximations with known error; limits; computing $e$, $\pi$, $\sin$; pendulum $T\approx2\pi\sqrt{L/g}\,(1+\frac{\theta_0^2}{16})$; $e^{i\theta}=\cos\theta+i\sin\theta$.
''')

# =====================================================================================
B.md(r'''
---
# Problems

Paper first. First attempt counts. `hint(n)` → `solution(n)` → `mistake(n, '...')`.

### Power series
''')
B.problem(S1, r'Radius of convergence of $\displaystyle\sum_{n=1}^{\infty}\frac{x^n}{n}$. *(From your diagnostic.)*', 'num', 1,
          [r'$c_n=\frac1n$. Compute $\lim\left|\frac{c_{n+1}}{c_n}\right|$.'],
          r'''$\dfrac{c_{n+1}}{c_n}=\dfrac{n}{n+1}\to1$, so $\frac1R=1$: **R = 1**.

(At $x=-1$ it is the alternating harmonic series — converges, to $-\ln2$; at $x=1$ the harmonic series — diverges. It is $-\ln(1-x)$.)''')
B.problem(S1, r'Radius of convergence of $\displaystyle\sum_{n=0}^{\infty}\frac{n\,x^n}{4^n}$.', 'num', 4,
          [r'$\dfrac{c_{n+1}}{c_n}=\dfrac{n+1}{4n}$.'],
          r'''$\dfrac{c_{n+1}}{c_n}=\dfrac{(n+1)/4^{n+1}}{n/4^n}=\dfrac{n+1}{4n}\to\dfrac14$, so **R = 4**.''')
B.problem(S1, r'From $\frac{1}{1-x}=\sum x^n$, find the series of $\dfrac{1}{1+3x}$. What is its coefficient of $x^2$?', 'num', 9,
          [r'Substitute $-3x$ for $x$.'],
          r'''$\dfrac{1}{1-(-3x)}=1-3x+9x^2-27x^3+\dots$: coefficient of $x^2$ is **9** (valid for $|x|<\frac13$).''')
B.problem(S1, r'Using $\ln(1+x)=x-\frac{x^2}{2}+\frac{x^3}{3}-\dots$, what is the coefficient of $x^3$ in the series of $\ln(1+2x)$?', 'num', 8 / 3,
          [r'Substitute $2x$: the $x^3$ term is $\frac{(2x)^3}{3}$.'],
          r'''$\frac{(2x)^3}{3}=\frac{8x^3}{3}$: coefficient **8/3**.''', fmt='a number, e.g. `8/3`')
B.md(r'''
### Taylor polynomials
''')
B.problem(S2, r'What is the coefficient of $x^4$ in the Maclaurin series of $e^x$? *(From your diagnostic.)*', 'num', 1 / 24,
          [r'$c_4=\frac{f^{(4)}(0)}{4!}$.'],
          r'''Every derivative of $e^x$ is $1$ at $0$: $c_4=\frac{1}{4!}=$ **1/24**.''', fmt='a number, e.g. `1/24`')
B.problem(S2, r'Find the Taylor polynomial of degree 2 of $\cos x$ around $0$, and use it to estimate $\cos(0.2)$.', 'num', 1 - 0.02,
          [r'$\cos x\approx1-\frac{x^2}{2}$.'],
          r'''$p_2(x)=1-\frac{x^2}{2}$; $p_2(0.2)=1-0.02=$ **0.98**. (True: $0.980067$; the error is about the next term $\frac{x^4}{24}=0.000067$.)''')
B.problem(S2, r'Find the Taylor polynomial of degree 2 of $\sqrt{x}$ around $a=4$, and use it to estimate $\sqrt{4.2}$.', 'num', 2 + 0.05 - 0.04 / 64,
          [r'$f(4)=2$, $f\,^\prime(x)=\frac{1}{2\sqrt x}$, $f\,^{\prime\prime}(x)=-\frac{1}{4x^{3/2}}$.', r"$f'(4)=\frac14$, $f''(4)=-\frac1{32}$. Then $2+\frac14(0.2)+\frac{-1/32}{2}(0.2)^2$."],
          r'''$f(4)=2$, $f'(4)=\frac14$, $f''(4)=-\frac{1}{4\cdot8}=-\frac1{32}$.
$$p_2(x)=2+\tfrac14(x-4)-\tfrac{1}{64}(x-4)^2 .$$
$p_2(4.2)=2+0.05-\frac{0.04}{64}=2.049375$. (True: $2.0493902$.)''')
B.problem(S2, r'Write the first terms of $\sin x\cdot\cos x$ by multiplying the two series. What is the coefficient of $x^3$?', 'num', -2 / 3,
          [r'$\left(x-\frac{x^3}{6}\right)\left(1-\frac{x^2}{2}\right)$: collect the $x^3$ terms.', r'Check with $\sin x\cos x=\frac12\sin2x$.'],
          r'''$\left(x-\frac{x^3}{6}+\dots\right)\left(1-\frac{x^2}{2}+\dots\right)=x-\frac{x^3}{2}-\frac{x^3}{6}+\dots=x-\frac23x^3+\dots$

Coefficient **−2/3**. Check: $\frac12\sin2x=\frac12\left(2x-\frac{8x^3}{6}+\dots\right)=x-\frac23x^3+\dots$ ✓''', fmt='a number, e.g. `-2/3`')
B.problem(S2, r'Binomial series: the coefficient of $x^2$ in $(1+x)^{-1/2}=\dfrac{1}{\sqrt{1+x}}$.', 'num', 3 / 8,
          [r'$\frac{\alpha(\alpha-1)}{2}$ with $\alpha=-\frac12$.'],
          r'''$\dfrac{\alpha(\alpha-1)}{2}=\dfrac{(-\frac12)(-\frac32)}{2}=\dfrac{3/4}{2}=\dfrac38$.

So $\frac{1}{\sqrt{1+x}}=1-\frac x2+\frac38x^2-\dots$ (used for the relativistic energy $mc^2/\sqrt{1-v^2/c^2}\approx mc^2+\frac12mv^2$.)''', fmt='a number, e.g. `3/8`')
B.md(r'''
### Error and approximation
''')
B.problem(S3, r'$\displaystyle\lim_{x\to0}\frac{\sin x-x}{x^3}$ — by series.', 'num', -1 / 6,
          [r'$\sin x=x-\frac{x^3}{6}+\dots$'],
          r'''$\dfrac{(x-\frac{x^3}{6}+\frac{x^5}{120}-\dots)-x}{x^3}=-\frac16+\frac{x^2}{120}-\dots\to$ **−1/6**.''', fmt='a number, e.g. `-1/6`')
B.problem(S3, r'$\displaystyle\lim_{x\to0}\frac{e^x-1-x}{x^2}$ — by series.', 'num', 0.5,
          [r'$e^x=1+x+\frac{x^2}{2}+\dots$'],
          r'''$\dfrac{\frac{x^2}{2}+\frac{x^3}{6}+\dots}{x^2}=\frac12+\frac x6+\dots\to$ **1/2**.''')
B.problem(S3, r'How many terms $\sum_{k=0}^{n}\frac1{k!}$ (give $n$) guarantee $e$ with an error below $10^{-4}$? Use $|R_n|\le\frac{3}{(n+1)!}$.', 'num', 7,
          [r'Need $(n+1)!>30\,000$.', r'$7!=5040$, $8!=40\,320$.'],
          r'''Need $\frac{3}{(n+1)!}<10^{-4}$, i.e. $(n+1)!>30\,000$. $7!=5040$ is too small, $8!=40\,320$ is enough: $n+1=8$, **n = 7** (eight terms).''', fmt='an integer')
B.problem(S3, r'The approximation $\sin x\approx x$ is used with $x=0.3$ rad. Estimate the **relative** error $\frac{x-\sin x}{\sin x}$ in percent with the next term of the series.', 'num', 100 * 0.09 / 6,
          [r'$x-\sin x\approx\frac{x^3}{6}$; relative to $x$ that is $\frac{x^2}{6}$.'],
          r'''$\dfrac{x-\sin x}{\sin x}\approx\dfrac{x^3/6}{x}=\dfrac{x^2}{6}=\dfrac{0.09}{6}=0.015$, i.e. **1.5 %**. (Exact: $1.53\%$.)''', fmt='a number (percent)')
B.md(r'''
### Applications
''')
B.problem(S4, r'A pendulum swings with amplitude $\theta_0=20^\circ$. By what percentage is its period longer than the small-angle period? (First correction only.)', 'num', 100 * math.radians(20) ** 2 / 16,
          [r'$T\approx T_0\left(1+\frac{\theta_0^2}{16}\right)$, with $\theta_0$ in radians.'],
          r'''$\theta_0=20^\circ=0.349$ rad, $\frac{\theta_0^2}{16}=\frac{0.1218}{16}=0.0076$: **0.76 %** longer.''', fmt='a number (percent)')
B.problem(S4, r'Use $(1+x)^\alpha\approx1+\alpha x$ to estimate $\sqrt[3]{1.06}$.', 'num', 1.02,
          [r'$\alpha=\frac13$, $x=0.06$.'],
          r'''$1+\frac13\cdot0.06=$ **1.02**. (True: $1.019613$.)''')
B.problem(S4, r'Using $e^{i\theta}=\cos\theta+i\sin\theta$, compute the real part of $e^{i\pi}+1$.', 'num', 0,
          [r'$e^{i\pi}=\cos\pi+i\sin\pi$.'],
          r'''$e^{i\pi}=-1+0i$, so $e^{i\pi}+1=0$: real part **0** — Euler's identity, linking $e$, $i$, $\pi$, $1$ and $0$.''')
B.code(r'''
# scratch cell
''')

B.md(r'''
---
# Finish the week — and Term 1

### 1 · Report
''')
B.code(r'''
report()
''')
B.md(r'''
### 2 · Teach-back (30 minutes, from memory)
1. Why is the Taylor coefficient $\frac{f^{(k)}(0)}{k!}$? (Differentiate the polynomial $k$ times.)
2. Write the series of $e^x$, $\sin x$, $\cos x$ and check them against each other by differentiating.
3. Why does the series of $\frac1{1+x^2}$ fail at $|x|=1$, although the function is fine there?
4. How many terms of the series for $e$ give 6 decimals, and why?
5. Where does $e^{i\theta}=\cos\theta+i\sin\theta$ come from?

*Your answers:*

&nbsp;

### 3 · Physics strand — when does "small angle" stop being small? (1 hour)
The Physics Lab's **double pendulum** contains two pendulums; with a small swing it behaves almost regularly, with a large swing chaotically. Choose *Small swing*, then gradually increase the angles. **Predict first:** from Part 3, below which angle do you expect $\sin\theta\approx\theta$ to stay within 1 %? Where does the motion visibly stop looking like two simple sine waves?
''')
B.code(r'''
lab('physics', exp='dbl', scen='Small swing (almost regular)')
''')
B.md(r'''
### 4 · Term 1 review
This was the last notebook of Term 1. Run `report()` in the notebooks of Units 1–4, or look at the course map.

- Every week at ≥ 80 % first time → **Term 2** (ODEs, linear algebra, dynamics) can start: first-order differential equations, which use everything of this term at once.
- Otherwise: a short patch week on the weakest unit before Term 2. Your `mistakes()` logs tell you which.

**What you now have.** Functions and trigonometry (Unit 1); rates of change (Unit 2); accumulation (Unit 3); and approximation by series (Unit 4). That is single-variable calculus — the language in which almost all of physics and engineering is written.
''')

if __name__ == '__main__':
    B.write()
