"""Unit 3 · Week 2 (course week 9) - Techniques of integration: substitution, parts, trig, partial fractions, numerical."""
import math
from nbkit import Book
import figs_u03 as F

B = Book('u03w2', 'Unit 3 · Week 2 — Techniques of integration', 'year1/u03w2-techniques-of-integration.ipynb')
S1, S2, S3, S4 = '1 Substitution', '2 Integration by parts', '3 Trigonometric integrals and partial fractions', '4 Numerical integration'

B.md(r'''
# Unit 3 · Week 2 — Techniques of integration
*Term 1, week 9 of 12 · about 15 hours in this notebook and on paper*

**Where you are.** Last week: to integrate, find an antiderivative. The table of basic antiderivatives handles sums of standard functions — but not $\int2x\cos(x^2)\,dx$ or $\int x\,e^x\,dx$.

Differentiation had a rule for every way of combining functions. Integration has **no** such complete set. What it has instead is each differentiation rule *read backwards*:

| differentiation rule | read backwards | part |
|---|---|---|
| chain rule | **substitution** | 1 |
| product rule | **integration by parts** | 2 |
| trig identities, algebra | rewriting the integrand until the table applies | 3 |
| — (when nothing works) | **numerical integration** | 4 |

**An honest remark before you start.** Differentiation is mechanical; integration is a search, and some perfectly ordinary functions — $e^{-x^2}$, $\frac{\sin x}{x}$ — have **no** antiderivative that can be written with the functions you know. That is not a gap in your skill. It is why Part 4 matters, and why every integral you find by hand should be **checked**: differentiate your answer (`compare(F, f)`), or compare with `nint(f, a, b)`.

**What is used from earlier:** the antiderivative table and the fundamental theorem (last week); chain and product rules (Unit 2 week 2); power reduction and product-to-sum formulas (Unit 1 week 2).

Run the grey *SETUP* cell first.
''')

# =====================================================================================
B.md(r'''
---
# Part 1 — Substitution: the chain rule backwards

## 1.1 The idea

**Build.**

**Step 1 — look at what the chain rule produces.**
$$\frac{d}{dx}\sin(x^2)=\cos(x^2)\cdot2x .$$
So, reading backwards, $\int\cos(x^2)\cdot2x\,dx=\sin(x^2)+C$. The integrand has a recognisable shape: a function of an *inside* ($x^2$), **multiplied by the derivative of that inside** ($2x$).

**Step 2 — in general.** The chain rule says $\frac{d}{dx}F(g(x))=F'(g(x))\,g'(x)$. With $F'=f$:
$$\int f\big(g(x)\big)\,g'(x)\,dx=F\big(g(x)\big)+C .$$

**Step 3 — a notation that does the bookkeeping.** Name the inside: $u=g(x)$. Then $\dfrac{du}{dx}=g'(x)$, which we write as
$$du=g'(x)\,dx .$$
With these two replacements the integral becomes one from the table:
$$\int f\big(\underbrace{g(x)}_{u}\big)\,\underbrace{g'(x)\,dx}_{du}=\int f(u)\,du=F(u)+C=F(g(x))+C .$$

*(What does "$du=g'(x)\,dx$" mean? Not a statement about numbers — $\frac{du}{dx}$ is a limit, not a fraction. It is a rule for rewriting integrals, and the three lines above are its justification: it produces exactly what the chain rule says is correct.)*

## 1.2 The procedure

1. **Choose $u$**: an *inside* function whose derivative (up to a constant factor) also appears in the integrand.
2. **Compute $du=u'\,dx$.**
3. **Rewrite the whole integral in terms of $u$** — no $x$ may remain.
4. **Integrate** with respect to $u$.
5. **Substitute back** $u=g(x)$. Check by differentiating.

**Worked example 1.** $\displaystyle\int2x\cos(x^2)\,dx$.
1. $u=x^2$ (the inside of the cosine). 2. $du=2x\,dx$. 3. $\int\cos u\,du$. 4. $\sin u+C$. 5. $\sin(x^2)+C$.
*Check:* $\frac{d}{dx}\sin(x^2)=2x\cos(x^2)$ ✓

**Worked example 2 — a constant factor is missing.** $\displaystyle\int x\,e^{x^2}\,dx$.
1. $u=x^2$. 2. $du=2x\,dx$. We have only $x\,dx$, not $2x\,dx$ — so solve for what we have: $x\,dx=\frac12du$.
3. $\int e^u\cdot\frac12\,du$. 4. $\frac12e^u+C$. 5. $\frac12e^{x^2}+C$.
A missing **constant** can always be repaired this way. A missing **$x$** cannot: $\int e^{x^2}dx$ has no elementary antiderivative.

**Worked example 3 — a linear inside.** $\displaystyle\int\cos(3x+1)\,dx$. $u=3x+1$, $du=3\,dx$, $dx=\frac13du$:
$$\int\cos u\cdot\tfrac13\,du=\tfrac13\sin u+C=\tfrac13\sin(3x+1)+C .$$
Worth knowing on sight: $\displaystyle\int f(ax+b)\,dx=\frac1aF(ax+b)+C$. In particular $\int e^{kx}dx=\frac1ke^{kx}$, $\int\sin\omega t\,dt=-\frac1\omega\cos\omega t$ — *integrating divides by the inner factor, where differentiating multiplied by it*.

**Worked example 4 — a power of a bracket.** $\displaystyle\int x\,(x^2+1)^5\,dx$. $u=x^2+1$, $du=2x\,dx$:
$$\int u^5\cdot\tfrac12\,du=\frac{u^6}{12}+C=\frac{(x^2+1)^6}{12}+C .$$

**Worked example 5 — the pattern $\dfrac{g'}{g}$.** $\displaystyle\int\frac{x}{x^2+1}\,dx$. $u=x^2+1$, $du=2x\,dx$:
$$\int\frac1u\cdot\tfrac12\,du=\tfrac12\ln|u|+C=\tfrac12\ln(x^2+1)+C .$$
In general $\displaystyle\int\frac{g'(x)}{g(x)}\,dx=\ln|g(x)|+C$: *top is the derivative of the bottom → logarithm of the bottom*.

**Worked example 6 — the tangent.** $\displaystyle\int\tan x\,dx=\int\frac{\sin x}{\cos x}\,dx$. The top is *minus* the derivative of the bottom: $u=\cos x$, $du=-\sin x\,dx$:
$$\int\frac{-du}{u}=-\ln|u|+C=-\ln|\cos x|+C .$$

**How to choose $u$.** Look for an *inside*: the content of a bracket, a root, an exponent, a denominator, the argument of sin/cos/ln. Then check that its derivative is present. If after step 3 an $x$ is left over, the choice was wrong — try another.
''')
B.code(r'''
# Check worked example 5: is (1/2) ln(x² + 1) really an antiderivative of x / (x² + 1)?
compare(lambda v: 0.5 * ln(v**2 + 1),      # your antiderivative F
        lambda v: v / (v**2 + 1))          # the integrand f      -> the slope of F must match f
''')
B.ask(r'''Find $\displaystyle\int3x^2\,(x^3+1)^4\,dx$.''', 'anti', '3*x**2*(x**3+1)**4',
      r'''$u=x^3+1$, $du=3x^2\,dx$: $\int u^4\,du=\dfrac{u^5}{5}+C=\dfrac{(x^3+1)^5}{5}+C$.''',
      r'''The inside is $x^3+1$ and its derivative $3x^2$ is sitting right there. Let $u=x^3+1$.''',
      fmt="a formula in `x` as text (no $+C$)", sample='(x**3+1)**5/5')
B.ask(r'''Find $\displaystyle\int e^{-2x}\,dx$.''', 'anti', 'exp(-2*x)',
      r'''$u=-2x$, $dx=-\frac12du$: $-\frac12e^{-2x}+C$. (Dividing by the inner factor $-2$.)''',
      r'''A linear inside: $\int e^{kx}dx=\frac1ke^{kx}$.''', fmt="a formula in `x` as text; write $e^{\\ldots}$ as `exp(...)`", sample='-exp(-2*x)/2')

B.md(r'''
## 1.3 Substitution in a definite integral: change the limits

**Build.** The limits $a$ and $b$ are values of $x$. Once the integral is written in $u$, they must be values of $u$. Two correct ways:

- **Method A — change the limits** (recommended): when $x=a$, $u=g(a)$; when $x=b$, $u=g(b)$. Then never go back to $x$.
$$\int_a^bf(g(x))\,g'(x)\,dx=\int_{g(a)}^{g(b)}f(u)\,du .$$
- **Method B**: find the antiderivative in $x$ first (indefinite integral, substitute back), then apply the original limits.

**The classic mistake** is to mix them: integrating in $u$ but using the $x$-limits.

**Worked example 1.** $\displaystyle\int_0^{\sqrt{\pi/2}}2x\cos(x^2)\,dx$. $u=x^2$, $du=2x\,dx$. Limits: $x=0\Rightarrow u=0$; $x=\sqrt{\pi/2}\Rightarrow u=\frac\pi2$.
$$\int_0^{\pi/2}\cos u\,du=\big[\sin u\big]_0^{\pi/2}=1 .$$
''')
B.fig('subst_area', F.subst_area, 'A substitution reshapes the region but keeps its area.')
B.md(r'''
**Worked example 2.** $\displaystyle\int_0^22x\,(x^2+1)^3\,dx$. $u=x^2+1$, $du=2x\,dx$; $x=0\Rightarrow u=1$, $x=2\Rightarrow u=5$:
$$\int_1^5u^3\,du=\left[\frac{u^4}{4}\right]_1^5=\frac{625-1}{4}=156 .$$

**Worked example 3.** $\displaystyle\int_1^e\frac{\ln x}{x}\,dx$. $u=\ln x$, $du=\frac1x\,dx$; $x=1\Rightarrow u=0$, $x=e\Rightarrow u=1$:
$$\int_0^1u\,du=\frac12 .$$

**Worked example 4 — limits that come out "backwards".** $\displaystyle\int_0^{\pi/2}\sin x\cos^2x\,dx$. $u=\cos x$, $du=-\sin x\,dx$; $x=0\Rightarrow u=1$, $x=\frac\pi2\Rightarrow u=0$:
$$\int_1^0u^2\,(-du)=\int_0^1u^2\,du=\frac13 .$$
(Swapping the limits changes the sign, which absorbs the minus.)
''')
B.code(r'''
# Check worked example 4 numerically
print(nint(lambda v: np.sin(v) * np.cos(v)**2, 0, pi / 2), '   expected 1/3')
''')
B.ask(r'''Evaluate $\displaystyle\int_0^1\frac{2x}{x^2+1}\,dx$.''', 'num', math.log(2),
      r'''$u=x^2+1$, $du=2x\,dx$; limits $u=1$ to $u=2$: $\int_1^2\frac{du}{u}=\ln2\approx0.693$.''',
      r'''$u=x^2+1$. Change the limits: $x=0\to u=1$, $x=1\to u=2$.''', fmt='a number; you can type `ln(2)`')

# =====================================================================================
B.md(r'''
---
# Part 2 — Integration by parts: the product rule backwards

## 2.1 The formula

**Why.** $\int x\,e^x\,dx$: a product, but neither factor is the derivative of an inside. Substitution fails. The product rule, read backwards, handles it.

**Build.** The product rule: $(uv)'=u'v+uv'$. Integrate both sides:
$$uv=\int u'v\,dx+\int uv'\,dx .$$
Solve for one of the integrals:
$$\boxed{\,\int u\,v'\,dx=u\,v-\int u'\,v\,dx\,}$$

**What it does.** It does not solve the integral; it **trades** it for another one, in which $u$ has been *differentiated* and $v'$ has been *integrated*. That is a good trade when $u$ becomes simpler by differentiating (like $x\to1$) and $v'$ does not become worse by integrating (like $e^x\to e^x$).

**The procedure.**
1. Split the integrand into two factors: $u$ (to differentiate) and $v'$ (to integrate).
2. Make the table $u,\ u',\ v',\ v$.
3. Apply the formula. Integrate what is left.

**Choosing $u$** — a rule of thumb, in order of preference: **L**ogarithms, **I**nverse trig, **A**lgebraic (powers of $x$), **T**rig, **E**xponentials ("LIATE"). The earlier type is $u$. It works because logs and inverse trig functions become simple when differentiated, while exponentials and sin/cos survive integration unchanged in kind.

**Worked example 1 (from your diagnostic).** $\displaystyle\int x\,e^x\,dx$.

| | | |
|---|---|---|
| $u=x$ | → differentiate → | $u'=1$ |
| $v'=e^x$ | → integrate → | $v=e^x$ |

$$\int x\,e^x\,dx=x\,e^x-\int1\cdot e^x\,dx=x\,e^x-e^x+C=(x-1)\,e^x+C .$$
*Check:* $\frac{d}{dx}\big[(x-1)e^x\big]=1\cdot e^x+(x-1)e^x=x\,e^x$ ✓

*(What if you choose the other way round, $u=e^x$, $v'=x$? You get $\frac{x^2}{2}e^x-\int\frac{x^2}{2}e^x\,dx$ — a harder integral than you started with. A wrong choice is not an error, just a dead end: go back and swap.)*

**Worked example 2.** $\displaystyle\int x\cos x\,dx$. $u=x$, $u'=1$; $v'=\cos x$, $v=\sin x$:
$$x\sin x-\int\sin x\,dx=x\sin x+\cos x+C .$$

**Worked example 3 — the logarithm, with an invisible factor 1.** $\displaystyle\int\ln x\,dx$. Write it as $\int\ln x\cdot1\,dx$: $u=\ln x$, $u'=\frac1x$; $v'=1$, $v=x$:
$$x\ln x-\int\frac1x\cdot x\,dx=x\ln x-x+C .$$

**Worked example 4 — twice.** $\displaystyle\int x^2e^x\,dx$. $u=x^2$, $v'=e^x$:
$$x^2e^x-\int2x\,e^x\,dx=x^2e^x-2\,(x-1)\,e^x+C=(x^2-2x+2)\,e^x+C$$
(using example 1 for the remaining integral). Each application lowers the power of $x$ by one.

**Worked example 5 — the integral comes back.** $I=\displaystyle\int e^x\sin x\,dx$. $u=\sin x$, $v'=e^x$:
$$I=e^x\sin x-\int e^x\cos x\,dx .$$
Again, with $u=\cos x$, $v'=e^x$: $\;\int e^x\cos x\,dx=e^x\cos x+\int e^x\sin x\,dx=e^x\cos x+I$. So
$$I=e^x\sin x-e^x\cos x-I\quad\Rightarrow\quad2I=e^x(\sin x-\cos x)\quad\Rightarrow\quad I=\tfrac12e^x(\sin x-\cos x)+C .$$
The unknown integral reappeared — and we solved for it like an unknown in an equation.

**For definite integrals:** $\displaystyle\int_a^bu\,v'\,dx=\big[u\,v\big]_a^b-\int_a^bu'\,v\,dx$.

**Worked example 6.** $\displaystyle\int_0^\pi x\sin x\,dx$. $u=x$, $v'=\sin x$, $v=-\cos x$:
$$\big[-x\cos x\big]_0^\pi+\int_0^\pi\cos x\,dx=\big(-\pi\cdot(-1)-0\big)+\big[\sin x\big]_0^\pi=\pi+0=\pi .$$
''')
B.ask(r'''Find $\displaystyle\int x\sin x\,dx$.''', 'anti', 'x*sin(x)',
      r'''$u=x$, $u'=1$; $v'=\sin x$, $v=-\cos x$. $\;-x\cos x-\int(-\cos x)\,dx=-x\cos x+\sin x+C$.''',
      r'''$u=x$ (it becomes 1), $v'=\sin x$ (so $v=-\cos x$). Watch the two minus signs.''', fmt="a formula in `x` as text (no $+C$)", sample='-x*cos(x) + sin(x)')
B.ask(r'''Evaluate $\displaystyle\int_1^e\ln x\,dx$.''', 'num', 1,
      r'''$\big[x\ln x-x\big]_1^e=(e-e)-(0-1)=1$.''',
      r'''Use $\int\ln x\,dx=x\ln x-x$ from worked example 3, then put in the limits.''')

# =====================================================================================
B.md(r'''
---
# Part 3 — Rewriting the integrand

## 3.1 Powers of sine and cosine

**Why.** $\int\sin^2x\,dx$ gives the average power in an AC circuit; products like $\sin3x\cos2x$ are the heart of Fourier series (Unit 12). Neither is in the table — but the identities of Unit 1 week 2 turn them into table entries.

**Even powers: power reduction.** $\sin^2x=\dfrac{1-\cos2x}{2}$, $\ \cos^2x=\dfrac{1+\cos2x}{2}$.
$$\int\sin^2x\,dx=\int\frac{1-\cos2x}{2}\,dx=\frac x2-\frac{\sin2x}{4}+C .$$
Over a full period: $\displaystyle\int_0^{2\pi}\sin^2x\,dx=\left[\frac x2-\frac{\sin2x}{4}\right]_0^{2\pi}=\pi$ — exactly half of the rectangle $2\pi\times1$. **The average of $\sin^2$ is $\frac12$.**

**Odd powers: peel off one factor and substitute.** $\displaystyle\int\sin^3x\,dx=\int\sin^2x\cdot\sin x\,dx=\int(1-\cos^2x)\sin x\,dx$. With $u=\cos x$, $du=-\sin x\,dx$:
$$-\int(1-u^2)\,du=-u+\frac{u^3}{3}+C=-\cos x+\frac{\cos^3x}{3}+C .$$

**Products of different frequencies: product-to-sum.** $\sin a\cos b=\frac12[\sin(a+b)+\sin(a-b)]$:
$$\int\sin3x\cos2x\,dx=\frac12\int(\sin5x+\sin x)\,dx=-\frac{\cos5x}{10}-\frac{\cos x}{2}+C .$$

## 3.2 Partial fractions

**Why.** $\int\dfrac{dx}{x^2-1}$: a rational function that is neither an arctan nor of the form $\frac{g'}{g}$. Such integrals appear in population models and, constantly, in circuit and control theory.

**Build.** The idea is to undo "putting over a common denominator".

**Step 1 — factor the denominator.** $x^2-1=(x-1)(x+1)$.

**Step 2 — write the fraction as a sum of simple ones** with unknown numerators:
$$\frac{1}{(x-1)(x+1)}=\frac{A}{x-1}+\frac{B}{x+1}.$$

**Step 3 — find $A$ and $B$.** Multiply both sides by $(x-1)(x+1)$:
$$1=A\,(x+1)+B\,(x-1).$$
This must hold for every $x$; choose the values that kill one term each. $x=1$: $1=2A$, so $A=\frac12$. $x=-1$: $1=-2B$, so $B=-\frac12$.

**Step 4 — integrate the simple fractions** (each is a logarithm):
$$\int\frac{dx}{x^2-1}=\frac12\int\frac{dx}{x-1}-\frac12\int\frac{dx}{x+1}=\frac12\ln|x-1|-\frac12\ln|x+1|+C=\frac12\ln\left|\frac{x-1}{x+1}\right|+C .$$

**Check step 3 before integrating:** $\dfrac{1/2}{x-1}-\dfrac{1/2}{x+1}=\dfrac{\frac12(x+1)-\frac12(x-1)}{(x-1)(x+1)}=\dfrac{1}{x^2-1}$ ✓

**Worked example.** $\displaystyle\int\frac{5x+1}{(x-1)(x+2)}\,dx$. $\;5x+1=A(x+2)+B(x-1)$. $x=1$: $6=3A$, $A=2$. $x=-2$: $-9=-3B$, $B=3$.
$$\int\left(\frac{2}{x-1}+\frac{3}{x+2}\right)dx=2\ln|x-1|+3\ln|x+2|+C .$$

*(This covers denominators that factor into different linear factors, with the top of lower degree than the bottom. Repeated factors and quadratic factors follow the same idea with slightly different templates; you will meet them with the Laplace transform.)*
''')
B.ask(r'''Evaluate $\displaystyle\int_0^{\pi}\cos^2x\,dx$.''', 'num', math.pi / 2,
      r'''$\cos^2x=\dfrac{1+\cos2x}{2}$: $\left[\dfrac x2+\dfrac{\sin2x}{4}\right]_0^\pi=\dfrac\pi2$. Half of the rectangle $\pi\times1$: the average of $\cos^2$ is $\frac12$.''',
      r'''Power reduction: $\cos^2x=\dfrac{1+\cos2x}{2}$.''', fmt='a number; you can type `pi/2`')
B.ask(r'''In $\dfrac{1}{x(x+2)}=\dfrac Ax+\dfrac{B}{x+2}$, what is $A$?''', 'num', 0.5,
      r'''$1=A(x+2)+Bx$. Put $x=0$: $1=2A$, $A=\frac12$. (And $x=-2$ gives $B=-\frac12$.)''',
      r'''Multiply through by $x(x+2)$, then put $x=0$.''')

# =====================================================================================
B.md(r'''
---
# Part 4 — Numerical integration

**Why.** Three situations in which no technique helps: the antiderivative does not exist in closed form ($e^{-x^2}$); the integrand is only known as measured data; or the integral sits inside a simulation that must run by itself. Then we return to the definition — a sum — and make it efficient.

## 4.1 From rectangles to trapezoids

**Build.** A Riemann sum replaces the curve by flat steps. Joining the points of the curve by straight lines follows it much better: each strip becomes a **trapezoid**.
''')
B.fig('trapezoid', F.trapezoid, 'Same four strips: flat tops against sloping tops.')
B.md(r'''
A trapezoid with parallel sides $f(x_{k-1})$ and $f(x_k)$ and width $h$ has area $\dfrac{f(x_{k-1})+f(x_k)}{2}\,h$. Add them up. Every interior point is shared by two trapezoids, so it counts twice:

$$\boxed{\,T_n=\frac h2\,\big[f(x_0)+2f(x_1)+2f(x_2)+\dots+2f(x_{n-1})+f(x_n)\big]\,},\qquad h=\frac{b-a}{n}.$$

**Worked example.** $\displaystyle\int_0^1x^2\,dx$ with $n=2$: $h=0.5$, points $0,\ 0.5,\ 1$, values $0,\ 0.25,\ 1$.
$$T_2=\frac{0.5}{2}\,\big[0+2\cdot0.25+1\big]=0.375\qquad(\text{exact: }0.3333).$$

**How good?** The error of the trapezoid rule is proportional to $h^2$: twice as many strips, a quarter of the error. The **midpoint** rule (last week's Experiment 1) also has error $\propto h^2$ — about half as large and **of the opposite sign**: where the curve bends upwards, trapezoids overshoot and midpoint rectangles undershoot.

## 4.2 Simpson's rule: let the two errors cancel

**Build.** If the trapezoid error is about $+2E$ and the midpoint error about $-E$, then the combination
$$S=\frac{2M+T}{3}$$
has error about $\frac{2(-E)+2E}{3}=0$: the leading errors cancel. Written out for one pair of strips of width $h$ each (points $x_0,x_1,x_2$; the midpoint rule uses $x_1$ with width $2h$, the trapezoid rule uses the ends):
$$\frac{2\cdot2h\,f(x_1)+\frac{2h}{2}\,[f(x_0)+f(x_2)]}{3}=\frac h3\,\big[f(x_0)+4f(x_1)+f(x_2)\big].$$
Over $n$ strips ($n$ even) the pattern of weights is $1,4,2,4,2,\dots,4,1$:

$$\boxed{\,S_n=\frac h3\,\big[f(x_0)+4f(x_1)+2f(x_2)+4f(x_3)+\dots+4f(x_{n-1})+f(x_n)\big]\,}$$

This is **Simpson's rule**. (It is also what you get by fitting a parabola through each three neighbouring points.) Its error is proportional to $h^4$: twice as many strips, **one sixteenth** of the error. It is exact for all polynomials up to degree 3.

**Worked example.** $\displaystyle\int_0^1x^2\,dx$ with $n=2$: $\;S_2=\frac{0.5}{3}\,[0+4\cdot0.25+1]=\frac{0.5\cdot2}{3}=\frac13$ — exact.

### Experiment 1 — write the trapezoid rule
Replace the `...` by the trapezoid formula. `ys` holds the values $f(x_0),\dots,f(x_n)$; `ys[0]` is the first, `ys[-1]` the last, `ys[1:-1]` all the interior ones, and `np.sum(...)` adds.
''')
B.code(r'''
def trapezoid(f, a, b, n):
    """Trapezoid rule with n strips."""
    h = (b - a) / n
    xs = a + h * np.arange(n + 1)        # the n + 1 points x0 ... xn
    ys = f(xs)
    return ...


# ---------- tests: do not change ----------
def test_trapezoid():
    cases = [('∫₀¹ x² dx, n = 2', lambda v: v**2, 0, 1, 2, 0.375), ('∫₀^π sin x dx, n = 4', np.sin, 0, pi, 4, 1.8961188979370398),
             ('∫₀² (3x + 1) dx, n = 5  (exact for a straight line)', lambda v: 3 * v + 1, 0, 2, 5, 8.0)]
    good = 0
    for name, f, a, b, n, true in cases:
        try:
            r = float(trapezoid(f, a, b, n))
        except Exception as err:
            print('✗', name, '-> not working yet (have you replaced the ... ?)'); continue
        ok = abs(r - true) < 1e-9; good += ok
        print('✓' if ok else '✗', name, '->', r)
    print('\nAll tests passed.' if good == len(cases) else '\nNot there yet: h / 2 * (ys[0] + 2 * np.sum(ys[1:-1]) + ys[-1])')

test_trapezoid()
''', ref=r'''
def trapezoid(f, a, b, n):
    h = (b - a) / n
    xs = a + h * np.arange(n + 1)
    ys = f(xs)
    return h / 2 * (ys[0] + 2 * np.sum(ys[1:-1]) + ys[-1])
print(trapezoid(lambda v: v**2, 0, 1, 2))
''')
B.md(r'''
### Experiment 2 — three rules, one integral
$\displaystyle\int_0^1e^{-x^2}dx$ has no elementary antiderivative (it is the core of the normal distribution in statistics). Its value is $0.746824132812\ldots$

**Predict first:** when $n$ doubles, by what factor does each error shrink — left rectangles, trapezoids, Simpson?
''')
B.code(r'''
g = lambda v: np.exp(-v**2)
exact = 0.7468241328124271
rows = []
for n in [2, 4, 8, 16, 32, 64]:
    h = 1 / n
    xs = h * np.arange(n + 1); ys = g(xs)
    left = h * np.sum(ys[:-1])
    trap = h / 2 * (ys[0] + 2 * np.sum(ys[1:-1]) + ys[-1])
    simp = h / 3 * (ys[0] + 4 * np.sum(ys[1:-1:2]) + 2 * np.sum(ys[2:-1:2]) + ys[-1])
    rows.append([n, abs(left - exact), abs(trap - exact), abs(simp - exact)])
table(['n', 'error: left rectangles', 'error: trapezoid', 'error: Simpson'], rows, fmt='%.2e')
''')
B.md(r'''
*Explain:* per doubling of $n$ the errors shrink by about 2, 4 and 16. With 64 strips, rectangles give 2 correct decimals, trapezoids 5, Simpson 9. The cost — 65 function evaluations — is the same for all three. **A better formula beats more brute force**; this is a theme of all numerical work, and you will see it again with Euler versus Runge–Kutta in Unit 5.
''')
B.ask(r'''Compute the trapezoid approximation of $\displaystyle\int_0^2x^3\,dx$ with $n=2$.''', 'num', 5,
      r'''$h=1$, values $f(0)=0$, $f(1)=1$, $f(2)=8$: $T_2=\frac12[0+2\cdot1+8]=5$. (Exact: 4. The curve bends upwards, so trapezoids overshoot.)''',
      r'''$h=1$; $T=\frac h2[f(0)+2f(1)+f(2)]$.''')

B.md(r'''
## Week summary — everything on one page

**Substitution** (chain rule backwards). $u=g(x)$, $du=g'(x)\,dx$; rewrite everything in $u$; for a definite integral change the limits to $u$-values.
Patterns: $\int f(ax+b)\,dx=\frac1aF(ax+b)$; $\int\frac{g'}{g}\,dx=\ln|g|$; $\int\tan x\,dx=-\ln|\cos x|$.

**Parts** (product rule backwards). $\int u\,v'\,dx=u\,v-\int u'\,v\,dx$. Choose $u$ by LIATE.
$\int xe^x=(x-1)e^x$; $\int\ln x=x\ln x-x$.

**Rewriting.** $\sin^2x=\frac{1-\cos2x}{2}$, $\cos^2x=\frac{1+\cos2x}{2}$; odd powers: peel off one factor; partial fractions $\frac{1}{(x-a)(x-b)}=\frac{A}{x-a}+\frac{B}{x-b}$.

**Numerical.** Trapezoid $\frac h2[f_0+2f_1+\dots+2f_{n-1}+f_n]$, error $\propto h^2$. Simpson $\frac h3[f_0+4f_1+2f_2+\dots+4f_{n-1}+f_n]$, error $\propto h^4$.

**Always check:** differentiate the antiderivative, or compare with `nint`.
''')

# =====================================================================================
B.md(r'''
---
# Problems

Paper first, then check with `compare` / `nint` in the scratch cell before you enter the answer. First attempt counts. `hint(n)` → `solution(n)` → `mistake(n, '...')`.

### Substitution
''')
B.problem(S1, r'Find $\displaystyle\int\frac{x}{x^2+1}\,dx$.', 'anti', 'x/(x**2+1)',
          [r'$u=x^2+1$; then $x\,dx=\frac12du$.'],
          r'''$u=x^2+1$, $du=2x\,dx$, so $x\,dx=\frac12du$:
$$\int\frac{1}{u}\cdot\frac12\,du=\frac12\ln|u|+C=\frac12\ln(x^2+1)+C .$$''', fmt="a formula in `x` as text; write $\\ln$ as `ln(...)`", sample='ln(x**2+1)/2')
B.problem(S1, r'Find $\displaystyle\int\cos(3x+1)\,dx$.', 'anti', 'cos(3*x+1)',
          [r'Linear inside: divide by the inner factor 3.'],
          r'''$u=3x+1$, $dx=\frac13du$: $\;\frac13\sin(3x+1)+C$.''', fmt="a formula in `x` as text", sample='sin(3*x+1)/3')
B.problem(S1, r'$\displaystyle\int_0^22x\,(x^2+1)^3\,dx$', 'num', 156,
          [r'$u=x^2+1$, $du=2x\,dx$. New limits: $u=1$ and $u=5$.'],
          r'''$$\int_1^5u^3\,du=\left[\frac{u^4}{4}\right]_1^5=\frac{625-1}{4}=156 .$$''')
B.problem(S1, r'$\displaystyle\int_0^{1}e^{-2x}\,dx$', 'num', (1 - math.exp(-2)) / 2,
          [r'Antiderivative: $-\frac12e^{-2x}$.'],
          r'''$$\left[-\tfrac12e^{-2x}\right]_0^1=-\tfrac12e^{-2}+\tfrac12=\frac{1-e^{-2}}{2}\approx0.432 .$$''', fmt='a number; you can type `(1-exp(-2))/2`')
B.problem(S1, r'$\displaystyle\int_0^{\pi/4}\tan x\,dx$', 'num', math.log(2) / 2,
          [r'$\int\tan x\,dx=-\ln|\cos x|$.', r'$-\ln\cos\frac\pi4+\ln\cos0=-\ln\frac{\sqrt2}{2}$.'],
          r'''$$\big[-\ln(\cos x)\big]_0^{\pi/4}=-\ln\frac{\sqrt2}{2}+\ln1=\ln\sqrt2=\tfrac12\ln2\approx0.347 .$$''', fmt='a number; you can type `ln(2)/2`')
B.problem(S1, r'$\displaystyle\int_1^{e}\frac{(\ln x)^2}{x}\,dx$', 'num', 1 / 3,
          [r'$u=\ln x$, $du=\frac1x\,dx$; limits $0$ and $1$.'],
          r'''$u=\ln x$: $\displaystyle\int_0^1u^2\,du=\frac13$.''', fmt='a number, e.g. `1/3`')
B.md(r'''
### Integration by parts
''')
B.problem(S2, r'Find an antiderivative of $x\,e^x$. *(From your diagnostic.)*', 'anti', 'x*exp(x)',
          [r'$u=x$, $v\,^\prime=e^x$.'],
          r'''$u=x$, $u'=1$; $v'=e^x$, $v=e^x$:
$$\int x\,e^x\,dx=x\,e^x-\int e^x\,dx=(x-1)\,e^x+C .$$''', fmt="a formula in `x` as text; write $e^x$ as `exp(x)`", sample='(x-1)*exp(x)')
B.problem(S2, r'Find $\displaystyle\int x\cos2x\,dx$.', 'anti', 'x*cos(2*x)',
          [r'$u=x$, $v\,^\prime=\cos2x$, so $v=\frac12\sin2x$.', r'$\frac x2\sin2x-\int\frac12\sin2x\,dx$.'],
          r'''$u=x$, $u'=1$; $v'=\cos2x$, $v=\frac12\sin2x$:
$$\frac x2\sin2x-\int\tfrac12\sin2x\,dx=\frac x2\sin2x+\frac14\cos2x+C .$$''', fmt="a formula in `x` as text", sample='x*sin(2*x)/2 + cos(2*x)/4')
B.problem(S2, r'$\displaystyle\int_0^{\pi}x\sin x\,dx$', 'num', math.pi,
          [r'$u=x$, $v\,^\prime=\sin x$, $v=-\cos x$.'],
          r'''$$\big[-x\cos x\big]_0^\pi+\int_0^\pi\cos x\,dx=\pi+\big[\sin x\big]_0^\pi=\pi .$$''', fmt='a number; you can type `pi`')
B.problem(S2, r'$\displaystyle\int_0^{1}x^2e^x\,dx$', 'num', math.e - 2,
          [r'Twice by parts; or use $\int x^2e^x\,dx=(x^2-2x+2)e^x$ from the text.'],
          r'''$$\big[(x^2-2x+2)\,e^x\big]_0^1=(1-2+2)\,e-2=e-2\approx0.718 .$$''', fmt='a number; you can type `e-2`')
B.problem(S2, r'$\displaystyle\int_1^{e}x\ln x\,dx$', 'num', (math.e ** 2 + 1) / 4,
          [r'LIATE: $u=\ln x$, $v\,^\prime=x$, $v=\frac{x^2}{2}$.', r'$\left[\frac{x^2}{2}\ln x\right]_1^e-\int_1^e\frac x2\,dx$.'],
          r'''$u=\ln x$, $u'=\frac1x$; $v'=x$, $v=\frac{x^2}{2}$:
$$\left[\frac{x^2}{2}\ln x\right]_1^e-\int_1^e\frac x2\,dx=\frac{e^2}{2}-\left[\frac{x^2}{4}\right]_1^e=\frac{e^2}{2}-\frac{e^2-1}{4}=\frac{e^2+1}{4}\approx2.097 .$$''', fmt='a number; you can type `(e**2+1)/4`')
B.md(r'''
### Trigonometric integrals and partial fractions
''')
B.problem(S3, r'$\displaystyle\int_0^{\pi}\sin^2x\,dx$', 'num', math.pi / 2,
          [r'$\sin^2x=\frac{1-\cos2x}{2}$.'],
          r'''$$\left[\frac x2-\frac{\sin2x}{4}\right]_0^\pi=\frac\pi2 .$$''', fmt='a number; you can type `pi/2`')
B.problem(S3, r'$\displaystyle\int_0^{\pi/2}\sin^3x\,dx$', 'num', 2 / 3,
          [r'$\sin^3x=(1-\cos^2x)\sin x$; $u=\cos x$.', r'Limits: $u=1$ to $u=0$; the minus from $du=-\sin x\,dx$ flips them.'],
          r'''$u=\cos x$, $du=-\sin x\,dx$:
$$\int_1^0(1-u^2)(-du)=\int_0^1(1-u^2)\,du=1-\frac13=\frac23 .$$''', fmt='a number, e.g. `2/3`')
B.problem(S3, r'$\displaystyle\int_2^{3}\frac{dx}{x^2-1}$', 'num', 0.5 * math.log(1.5),
          [r'Partial fractions: $\frac{1}{x^2-1}=\frac{1/2}{x-1}-\frac{1/2}{x+1}$.', r'Antiderivative $\frac12\ln\frac{x-1}{x+1}$.'],
          r'''$$\left[\frac12\ln\frac{x-1}{x+1}\right]_2^3=\frac12\left(\ln\frac24-\ln\frac13\right)=\frac12\ln\frac{1/2}{1/3}=\frac12\ln\frac32\approx0.203 .$$''', fmt='a number; you can type `ln(3/2)/2`')
B.md(r'''
### Numerical integration
''')
B.problem(S4, r'Compute the trapezoid approximation of $\displaystyle\int_0^1\frac{1}{1+x}\,dx$ with $n=2$.', 'num', 17 / 24,
          [r'$h=0.5$; values $1,\ \frac23,\ \frac12$.'],
          r'''$$T_2=\frac{0.5}{2}\left[1+2\cdot\frac23+\frac12\right]=\frac14\cdot\frac{17}{6}=\frac{17}{24}\approx0.7083 .$$
(Exact: $\ln2=0.6931$.)''', fmt='a number, e.g. `17/24`')
B.problem(S4, r'Compute Simpson’s approximation of the same integral $\displaystyle\int_0^1\frac{1}{1+x}\,dx$ with $n=2$.', 'num', 25 / 36,
          [r'$\frac h3[f_0+4f_1+f_2]$ with $h=0.5$.'],
          r'''$$S_2=\frac{0.5}{3}\left[1+4\cdot\frac23+\frac12\right]=\frac16\cdot\frac{25}{6}=\frac{25}{36}\approx0.6944 .$$
Error $0.0013$ against $0.0152$ for the trapezoid rule with the same three function values.''', fmt='a number, e.g. `25/36`')
B.problem(S4, r'The trapezoid rule with $n=10$ gives an error of $0.008$ on some integral. Roughly what error do you expect with $n=40$?', 'num', 0.0005,
          [r'Error $\propto h^2$; $h$ becomes 4 times smaller.'],
          r'''$h$ shrinks by a factor 4, the error by $4^2=16$: $\dfrac{0.008}{16}=$ **0.0005**.''')
B.code(r'''
# scratch cell: e.g.  compare(lambda v: (v - 1) * exp(v),  lambda v: v * exp(v))     or     nint(lambda v: v * np.sin(v), 0, pi)
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
1. Which differentiation rule is substitution the reverse of? Show it on $\int2x\cos(x^2)\,dx$.
2. Why must the limits change in a definite integral after substituting?
3. Derive the integration-by-parts formula from the product rule.
4. How do you choose $u$ in $\int x\ln x\,dx$, and why?
5. Why does combining the midpoint and trapezoid rules give a much better rule?

*Your answers:*

&nbsp;

### 3 · Lab strand — a capacitor adds up current (1 hour)
The charge on a capacitor is the integral of the current into it, $q=\int i\,dt$, and its voltage is $v=\frac qC$. The simulator opens with an RC circuit driven by a square wave.

**Predict first:** while the source is high, the current is largest at the start and dies away. What must the capacitor voltage (the running integral of that current) look like — steep at first, then flattening? Watch the two probes on the oscilloscope. Then make the resistor ten times larger: what happens to the current, and so to the speed of charging?
''')
B.code(r'''
lab('voltaic', height=680, preset='rc')
''')
B.md(r'''
### 4 · What comes next
**Week 3** puts the integral to work: areas between curves, volumes, averages and RMS values, work and energy, and integrals over infinitely long intervals.
''')

if __name__ == '__main__':
    B.write()
