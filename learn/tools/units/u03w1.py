"""Unit 3 · Week 1 (course week 8) - Area, Riemann sums, the definite integral and the fundamental theorem."""
import math
from nbkit import Book
import figs_u03 as F

B = Book('u03w1', 'Unit 3 · Week 1 — The integral and the fundamental theorem', 'year1/u03w1-integral-fundamental-theorem.ipynb')
S1, S2, S3, S4 = '1 Sums and Riemann sums', '2 The definite integral', '3 The fundamental theorem', '4 Antiderivatives and applications'

B.md(r'''
# Unit 3 · Week 1 — The integral and the fundamental theorem
*Term 1, week 8 of 12 · about 15 hours in this notebook and on paper*

**Where you are.** Unit 2 answered: *given a quantity, how fast is it changing?* This unit asks the reverse: **given how fast something changes, how much does it change in total?** Given the velocity, how far did you go? Given the current, how much charge flowed? Given the force, how much work was done?

The answer is the **integral**. This week builds it from the only thing we can be sure of — *rate × time = amount, when the rate is constant* — and then proves the most important theorem of calculus: that integration and differentiation undo each other.

**The plan for Unit 3**

| week | content |
|---|---|
| **1 (this notebook)** | area as a limit of sums; the definite integral; the fundamental theorem; basic antiderivatives |
| 2 | techniques: substitution, integration by parts, numerical integration |
| 3 | applications: areas, volumes, averages and RMS, work and energy, improper integrals |

**What you will be able to do at the end of this week**
1. Write and evaluate sums in $\Sigma$-notation, and compute an area as the limit of a Riemann sum.
2. Say precisely what $\int_a^bf(x)\,dx$ means, and use its basic properties.
3. **Prove** both parts of the fundamental theorem of calculus and explain in words why it is true.
4. Evaluate definite integrals with antiderivatives.

**What is used from earlier:** limits (Unit 1 week 3); all derivatives (Unit 2); the squeeze theorem; the fact that two functions with the same derivative differ by a constant (Unit 2 week 4, §4.1).

**A new tool.** `nint(f, a, b)` computes a definite integral numerically, e.g. `nint(lambda v: v**2, 0, 1)`. Use it to **check** every integral you work out by hand.

Run the grey *SETUP* cell first.
''')

# =====================================================================================
B.md(r'''
---
# Part 1 — From rate to amount: sums

## 1.1 The problem

**Why.** If you drive at a constant 20 m/s for 3 s, you cover $20\times3=60$ m. No calculus needed. But what if the speed changes all the time?

**Build.**

**Step 1 — constant rate: a rectangle.** Plot velocity against time. For a constant velocity the graph is a horizontal line, and distance = velocity × time is the **area of the rectangle** under it.

**Step 2 — changing rate: chop the time into short pieces.** During a *short* interval the velocity hardly changes, so "distance ≈ velocity × time" is nearly right for that piece: a thin rectangle. Add up the thin rectangles.
''')
B.fig('const_velocity', F.const_velocity, 'Distance is the area under the velocity graph. For a changing velocity: approximate it by thin rectangles.')
B.md(r'''
**Step 3 — make the pieces shorter.** The shorter the pieces, the less the velocity changes within each, the smaller the error. The exact distance is the **limit** of the sum as the pieces shrink — and geometrically it is the exact **area under the curve**.

So the two problems
- *total change from a varying rate*, and
- *area under a curve*

are the same problem. Everything this week is the careful version of these three steps. It is the pattern of Unit 1 again: a quantity we cannot compute directly (area under a curve) is the limit of quantities we can (sums of rectangles).

*Check with the picture:* velocity $v=10t$ from $0$ to $3$ s. The region under the line is a triangle: $\frac12\cdot3\cdot30=45$ m. And indeed a ball falling for 3 s covers $5t^2=45$ m.

## 1.2 Writing sums: $\Sigma$-notation

**Why.** We are going to add hundreds of terms. We need a compact way to write that.

**Build.** The Greek capital sigma, $\Sigma$, means "sum".
$$\sum_{k=1}^{5}k^2=1^2+2^2+3^2+4^2+5^2=55 .$$
Read: "the sum, for $k$ from 1 to 5, of $k^2$". The letter $k$ is a counter (the *index*): it takes each whole-number value from the bottom limit to the top limit; for each, you compute the expression after the $\Sigma$; then you add everything. In Python: `sum(k**2 for k in range(1, 6))`.

The index is a dummy — $\sum_{j=1}^5j^2$ is the same number.

**Two rules** (they are just the ordinary rules of addition):
$$\sum_{k=1}^{n}c\,a_k=c\sum_{k=1}^{n}a_k,\qquad\sum_{k=1}^{n}(a_k+b_k)=\sum_{k=1}^{n}a_k+\sum_{k=1}^{n}b_k .$$
And a constant added $n$ times: $\sum_{k=1}^nc=nc$.

## 1.3 Two sums we need

**(a) $1+2+3+\dots+n=\dfrac{n(n+1)}{2}$.**

*Proof (the trick attributed to the schoolboy Gauss).* Write the sum $S$ forwards and backwards and add the two lines column by column:
''')
B.fig('gauss_pairs', F.gauss_pairs, 'For n = 10: ten columns, each adding to 11.')
B.md(r'''
$$\begin{aligned}
S&=1+2+\dots+(n-1)+n\\
S&=n+(n-1)+\dots+2+1\\\hline
2S&=(n+1)+(n+1)+\dots+(n+1)=n\,(n+1)
\end{aligned}$$
There are $n$ columns, each $n+1$. So $S=\dfrac{n(n+1)}{2}$. $\blacksquare$ (For $n=10$: $\frac{10\cdot11}{2}=55$ ✓.)

**(b) $1^2+2^2+\dots+n^2=\dfrac{n(n+1)(2n+1)}{6}$.**

*Proof.* Start from an identity that is easy to check by expanding: $(k+1)^3-k^3=3k^2+3k+1$. Add it up for $k=1,2,\dots,n$. On the left almost everything cancels (a "telescoping" sum):
$$\big(2^3-1^3\big)+\big(3^3-2^3\big)+\dots+\big((n+1)^3-n^3\big)=(n+1)^3-1 .$$
On the right, with $S_2=\sum k^2$ and the result (a): $\;3S_2+3\cdot\dfrac{n(n+1)}{2}+n$. So
$$\begin{aligned}
3S_2&=(n+1)^3-1-n-\tfrac32n(n+1)\\
&=(n+1)^3-(n+1)-\tfrac32n(n+1)\\
&=(n+1)\Big[(n+1)^2-1-\tfrac32n\Big]=(n+1)\Big[n^2+\tfrac12n\Big]=\tfrac12\,n\,(n+1)(2n+1).
\end{aligned}$$
Divide by 3. $\blacksquare$ (For $n=5$: $\frac{5\cdot6\cdot11}{6}=55$ ✓.)
''')
B.ask(r'''Compute $\displaystyle\sum_{k=1}^{4}(2k+1)$.''', 'num', 24,
      r'''$3+5+7+9=24$. Or with the rules: $2\sum k+\sum1=2\cdot10+4=24$.''',
      r'''Write out the four terms for $k=1,2,3,4$ and add.''')
B.ask(r'''What is $1+2+3+\dots+100$?''', 'num', 5050,
      r'''$\dfrac{n(n+1)}{2}=\dfrac{100\cdot101}{2}=5050$.''',
      r'''Use $\dfrac{n(n+1)}{2}$ with $n=100$.''')

B.md(r'''
## 1.4 Riemann sums

**Build.** To approximate the area under $y=f(x)$ between $x=a$ and $x=b$:

1. **Cut** $[a,b]$ into $n$ strips of equal width $\Delta x=\dfrac{b-a}{n}$.
2. In each strip **pick a point** $x_k$ and use the height $f(x_k)$ there. The strip is replaced by a rectangle of area $f(x_k)\,\Delta x$.
3. **Add** the rectangles:
$$\text{area}\approx\sum_{k=1}^{n}f(x_k)\,\Delta x .$$

This is a **Riemann sum**. Where you pick the point gives it its name: left end (*left sum*), right end (*right sum*), middle (*midpoint sum*).
''')
B.fig('riemann', F.riemann, 'The area under y = x² from 0 to 1 with five rectangles. The exact value turns out to be 1/3.')
B.md(r'''
For a rising function the left sum is too small and the right sum too big; the truth is trapped between them, and as $n$ grows both close in on it.

**Worked example — the area under $y=x^2$ from $0$ to $1$, exactly.**

1. Strips: $\Delta x=\dfrac1n$. Right end points: $x_k=\dfrac kn$ for $k=1,\dots,n$.
2. Heights: $f(x_k)=\dfrac{k^2}{n^2}$.
3. Right sum:
$$R_n=\sum_{k=1}^{n}\frac{k^2}{n^2}\cdot\frac1n=\frac{1}{n^3}\sum_{k=1}^{n}k^2=\frac{1}{n^3}\cdot\frac{n(n+1)(2n+1)}{6}=\frac{(n+1)(2n+1)}{6n^2}.$$
   (The factor $\frac{1}{n^3}$ does not depend on $k$, so it comes out of the sum; then formula (b).)
4. Multiply out the top: $(n+1)(2n+1)=2n^2+3n+1$, so
$$R_n=\frac{2n^2+3n+1}{6n^2}=\frac13+\frac{1}{2n}+\frac{1}{6n^2}.$$
5. Let $n\to\infty$: the last two terms vanish. **The area is exactly $\dfrac13$.**

Check with $n=5$: $\frac13+\frac1{10}+\frac{1}{150}=0.44$ ✓ (the figure).

Step 4 also shows how fast the sum converges: the error is about $\frac{1}{2n}$. A hundred rectangles give two correct decimals — slow. (The midpoint sum is much better; Experiment 1.)

### Experiment 1 — Riemann sums with a slider
**Predict first:** for $n=10$, is the left sum above or below $\frac13$, and by about how much? Which of the three sums is closest? When $n$ is doubled, by what factor does each error shrink?
''')
B.code(r'''
def f(u):
    return u**2                       # try also:  np.sin(u)  on [0, pi]  (change a, b below)

a, b = 0.0, 1.0

def sums(n=10):
    dx = (b - a) / n
    left = a + dx * np.arange(n)                    # left end of each strip
    L = np.sum(f(left)) * dx
    R = np.sum(f(left + dx)) * dx
    M = np.sum(f(left + dx / 2)) * dx
    xs = np.linspace(a, b, 300)
    plt.figure(figsize=(7, 3.6))
    plt.bar(left, f(left + dx / 2), width=dx, align='edge', color='#fff8c5', edgecolor='k', lw=0.6)
    plt.plot(xs, f(xs), lw=2); plt.title(f'midpoint rectangles, n = {n}'); plt.show()
    exact = nint(f, a, b)
    table(['sum', 'value', 'error'], [['left', L, L - exact], ['right', R, R - exact], ['midpoint', M, M - exact]], fmt='%.6f')

explore(sums, n=(2, 100, 2, 10))
''')
B.md(r'''
*Explain:* the left and right errors are about $\mp\frac{1}{2n}$: doubling $n$ halves them. The midpoint error is far smaller and shrinks by a factor **4** when $n$ doubles — it behaves like $\frac{1}{n^2}$. (Week 2 explains why.)
''')
B.ask(r'''Compute the **right** Riemann sum for $f(x)=x^2$ on $[0,2]$ with $n=4$ strips.''', 'num', 3.75,
      r'''$\Delta x=0.5$; right ends $0.5,1,1.5,2$; heights $0.25,1,2.25,4$. Sum of heights $7.5$, times $0.5$: $3.75$. (The exact area is $\frac83\approx2.67$; a right sum of a rising function overestimates.)''',
      r'''$\Delta x=\frac{2-0}{4}$. List the four right end points, square them, add, multiply by $\Delta x$.''')

# =====================================================================================
B.md(r'''
---
# Part 2 — The definite integral

## 2.1 The definition

$$\boxed{\,\int_a^bf(x)\,dx=\lim_{n\to\infty}\sum_{k=1}^{n}f(x_k)\,\Delta x\,}$$

This limit is called the **definite integral of $f$ from $a$ to $b$**. For a continuous function it exists, and it is the same whichever points $x_k$ you pick in the strips. *(That is a theorem; the proof needs the fine structure of the real numbers, like the extreme value theorem. Our worked example is one case where we saw it happen.)*

**Reading the notation.** Every symbol is a reminder of the sum it came from.

| symbol | meaning |
|---|---|
| $\int$ | an elongated **S**, for "sum" — the limit of $\sum$ |
| $a$, $b$ | the **limits of integration**: where the region starts and ends |
| $f(x)$ | the **integrand**: the height of the rectangle at $x$ |
| $dx$ | the width of an infinitely thin strip — the limit of $\Delta x$. It also names the variable. |

So $\int_a^bf(x)\,dx$ reads: "*add up, from $a$ to $b$, height times width*". In physics: $\int_0^Tv(t)\,dt$ — "add up velocity × little time" — is a distance, and its units are (m/s)·(s) = m. **The units of an integral are the units of the integrand times the units of the variable.**

The variable is a dummy, like the index of a sum: $\int_0^1x^2\,dx=\int_0^1t^2\,dt=\frac13$. The integral is a **number**, not a function of $x$.

## 2.2 Signed area

**Build.** Where $f(x)$ is negative, the "height" $f(x_k)$ is negative, and that strip contributes a **negative** amount. So the integral counts area above the axis as positive and area below as negative.
''')
B.fig('signed_area', F.signed_area, 'The integral of sin x from 0 to 2π is zero: the two regions cancel.')
B.md(r'''
That is what you want physically: with velocity, positive area is distance forwards and negative area distance backwards, so the integral is the **net displacement**. (The total distance travelled is $\int|v|\,dt$ — count all area as positive.)

## 2.3 Properties

Each follows from the definition as a sum, or from the picture.

| property | why |
|---|---|
| $\displaystyle\int_a^b[f(x)+g(x)]\,dx=\int_a^bf\,dx+\int_a^bg\,dx$ | sums can be split |
| $\displaystyle\int_a^bc\,f(x)\,dx=c\int_a^bf(x)\,dx$ | a common factor comes out of a sum |
| $\displaystyle\int_a^bf\,dx+\int_b^cf\,dx=\int_a^cf\,dx$ | areas side by side add |
| $\displaystyle\int_a^af\,dx=0$ | no width |
| $\displaystyle\int_b^af\,dx=-\int_a^bf\,dx$ | going backwards, $\Delta x$ is negative (a convention that keeps the third rule true in any order) |

The first two together are **linearity** — as for derivatives. And as for derivatives, there is **no** simple rule for the integral of a product.

## 2.4 Integrals you can do with geometry

When the region is a familiar shape, no limit is needed.

**Worked example 1.** $\displaystyle\int_0^3(2x+1)\,dx$: under the line $y=2x+1$ from $0$ to $3$ lies a trapezoid with parallel sides $1$ (at $x=0$) and $7$ (at $x=3$) and width $3$: area $\frac{1+7}{2}\cdot3=12$.

**Worked example 2.** $\displaystyle\int_{-2}^{2}\sqrt{4-x^2}\,dx$: $y=\sqrt{4-x^2}$ is the upper half of the circle $x^2+y^2=4$. Half a disc of radius 2: $\frac12\pi\cdot2^2=2\pi$.

**Worked example 3 — symmetry.** $\displaystyle\int_{-1}^{1}x^3\,dx=0$: $x^3$ is odd, so the area below the axis on the left exactly cancels the area above on the right. In general $\int_{-a}^{a}(\text{odd function})\,dx=0$.
''')
B.ask(r'''Use geometry: $\displaystyle\int_0^4\tfrac12x\,dx=\ ?$''', 'num', 4,
      r'''Under the line $y=\frac x2$ from 0 to 4 is a triangle with base 4 and height 2: area $\frac12\cdot4\cdot2=4$.''',
      r'''Sketch $y=\frac x2$. Which shape lies under it between 0 and 4?''')
B.ask(r'''If $\displaystyle\int_0^2f\,dx=5$ and $\displaystyle\int_0^6f\,dx=3$, what is $\displaystyle\int_2^6f\,dx$?''', 'num', -2,
      r'''$\int_0^2+\int_2^6=\int_0^6$, so $\int_2^6=3-5=-2$. (Negative: between 2 and 6 the function is mostly below the axis.)''',
      r'''Areas side by side add: $\int_0^2+\int_2^6=\int_0^6$.''')

# =====================================================================================
B.md(r'''
---
# Part 3 — The fundamental theorem of calculus

Computing $\int_0^1x^2\,dx$ from the definition took a page and a clever formula. For $\int_0^\pi\sin x\,dx$ there is no such formula to hand. If that were all, integration would be a curiosity. What makes it a tool is a discovery of Newton and Leibniz: **areas can be computed with antiderivatives.**

## 3.1 The area function

**Build.** Fix the left end $a$ and let the right end **move**. Define
$$A(x)=\int_a^xf(t)\,dt\qquad\text{= the area under $f$ from $a$ up to $x$.}$$
(The variable inside is called $t$ only because $x$ is now in use as the end point.) This is a perfectly good *function of $x$*: move $x$ to the right and the accumulated area changes.

**The key question: how fast does the area grow as $x$ moves?** That is: what is $A'(x)$?
''')
B.fig('strip', F.strip, 'Moving the right end from x to x + h adds one thin strip.')
B.md(r'''
**The idea.** Move the end from $x$ to $x+h$. The area grows by one thin strip, of width $h$ and height about $f(x)$:
$$A(x+h)-A(x)\approx f(x)\cdot h\qquad\Longrightarrow\qquad\frac{A(x+h)-A(x)}{h}\approx f(x).$$
**The rate at which area accumulates is the height of the curve at that point.** Where the curve is high, area piles up fast; where it is at zero, the area stops growing.

## 3.2 The theorem, part 1

**Theorem (FTC 1).** If $f$ is continuous, then $A(x)=\displaystyle\int_a^xf(t)\,dt$ is differentiable, and
$$\boxed{\,\frac{d}{dx}\int_a^xf(t)\,dt=f(x)\,}$$

**Proof.** Make the "≈" exact with a squeeze. Take $h>0$. On the interval $[x,x+h]$ the continuous function $f$ has a smallest value $m$ and a largest value $M$ (extreme value theorem). The strip lies between a rectangle of height $m$ and a rectangle of height $M$, both of width $h$:
$$m\,h\ \le\ A(x+h)-A(x)\ \le\ M\,h .$$
Divide by $h$:
$$m\ \le\ \frac{A(x+h)-A(x)}{h}\ \le\ M .$$
Now let $h\to0$. The interval $[x,x+h]$ shrinks to the single point $x$, and because $f$ is continuous its smallest and largest values there both tend to $f(x)$. By the squeeze theorem the difference quotient tends to $f(x)$. (For $h<0$ the same argument works.) $\blacksquare$

**In words: differentiation undoes integration.** Integrate $f$ up to $x$, then differentiate with respect to $x$: you are back at $f$.

**Worked example.** $\dfrac{d}{dx}\displaystyle\int_0^x\cos(t^2)\,dt=\cos(x^2)$. No computation: replace $t$ by $x$. (This integral has no formula in terms of elementary functions — and yet we know its derivative exactly.)

### Experiment 2 — watch the area function
The cell computes $A(x)=\int_0^x\cos t\,dt$ numerically, by adding thin strips, and plots it.

**Predict first:** $A$ grows fastest where $\cos$ is largest and has its peak where $\cos$ crosses zero. Sketch $A$. Which function does it look like?
''')
B.code(r'''
func = np.cos                              # try also:  np.sin,  lambda u: u**2,  lambda u: np.exp(-u**2)
xs = np.linspace(0, 2 * pi, 2001)
dx = xs[1] - xs[0]
mid = func(xs[:-1] + dx / 2)               # height in the middle of each thin strip
A = np.concatenate([[0], np.cumsum(mid * dx)])   # running total of the strip areas

fig, (a1, a2) = plt.subplots(1, 2, figsize=(10.5, 3.6))
a1.plot(xs, func(xs)); a1.fill_between(xs, 0, func(xs), alpha=0.2); a1.axhline(0, color='k', lw=0.8); a1.set_title('f')
a2.plot(xs, A, 'r', lw=5, alpha=0.35, label='A(x): accumulated area'); a2.plot(xs, np.sin(xs), 'k--', lw=1.2, label='sin x')
a2.axhline(0, color='k', lw=0.8); a2.legend(); a2.set_title('the area function'); plt.show()
print('slope of A at x = 1 (numerically):', (A[319] - A[317]) / (2 * dx), '   f(1) =', float(func(xs[318])))
''')
B.md(r'''
*Explain:* the area function of $\cos$ is $\sin$ — the function whose *derivative* is $\cos$. That is FTC 1 in a picture.

## 3.3 The theorem, part 2

**Definition.** $F$ is an **antiderivative** of $f$ if $F'=f$. (Example: $\frac{x^3}{3}$ is an antiderivative of $x^2$. So is $\frac{x^3}{3}+7$.)

**Theorem (FTC 2).** If $f$ is continuous on $[a,b]$ and $F$ is **any** antiderivative of $f$, then
$$\boxed{\,\int_a^bf(x)\,dx=F(b)-F(a)\,}$$

**Proof.** Three short steps.

1. By FTC 1, the area function $A(x)=\int_a^xf(t)\,dt$ is an antiderivative of $f$: $A'=f$.
2. $F$ is also an antiderivative: $F'=f$. Two functions with the same derivative differ by a constant (Unit 2 week 4, §4.1): $\;A(x)=F(x)+C$ for all $x$.
3. Find $C$ by putting $x=a$: $A(a)=\int_a^af=0$, so $0=F(a)+C$, i.e. $C=-F(a)$. Hence $A(x)=F(x)-F(a)$, and at $x=b$:
$$\int_a^bf(t)\,dt=A(b)=F(b)-F(a).\qquad\blacksquare$$

**What this achieves.** The left side is a limit of sums of thousands of rectangles. The right side is two function evaluations and a subtraction. To compute an area: **find any function whose derivative is the integrand, evaluate it at the two ends, subtract.**

**Notation.** $F(b)-F(a)$ is written $\big[F(x)\big]_a^b$.

**Worked example 1 — the page of work, in one line.**
$$\int_0^1x^2\,dx=\left[\frac{x^3}{3}\right]_0^1=\frac13-0=\frac13\ ✓$$

**Worked example 2 (from your diagnostic).**
$$\int_0^\pi\sin x\,dx=\big[-\cos x\big]_0^\pi=(-\cos\pi)-(-\cos0)=1-(-1)=2 .$$
($-\cos x$ is an antiderivative of $\sin x$ because $\frac{d}{dx}(-\cos x)=\sin x$.) One arch of the sine curve has area exactly 2.

**Worked example 3.**
$$\int_1^3(3x^2-2x)\,dx=\big[x^3-x^2\big]_1^3=(27-9)-(1-1)=18 .$$

**Why any antiderivative will do:** with $F+C$ instead of $F$, the constant cancels: $(F(b)+C)-(F(a)+C)=F(b)-F(a)$.

**In words: integration undoes differentiation.** $\int_a^bF'(x)\,dx=F(b)-F(a)$: *adding up all the little changes of $F$ gives the total change of $F$.* For motion: adding up velocity × time gives the change in position.
''')
B.ask(r'''What is $\dfrac{d}{dx}\displaystyle\int_1^x\frac{\sin t}{t}\,dt$ at $x=\dfrac\pi2$?''', 'num', 2 / math.pi,
      r'''By FTC 1 the derivative is the integrand at $x$: $\dfrac{\sin x}{x}$. At $\frac\pi2$: $\dfrac{1}{\pi/2}=\dfrac2\pi\approx0.637$.''',
      r'''FTC 1: differentiating $\int_a^xf(t)\,dt$ gives $f(x)$. No integration needed.''', fmt='a number; you can type `2/pi`')
B.ask(r'''Evaluate $\displaystyle\int_0^2x^3\,dx$ with an antiderivative.''', 'num', 4,
      r'''$\left[\dfrac{x^4}{4}\right]_0^2=\dfrac{16}{4}-0=4$.''',
      r'''Which function has derivative $x^3$? Try $\frac{x^4}{4}$. Then $F(2)-F(0)$.''')

# =====================================================================================
B.md(r'''
---
# Part 4 — Antiderivatives

## 4.1 The indefinite integral

**Build.** The fundamental theorem turns "integrate" into "find an antiderivative". So we need a notation for *all* antiderivatives of $f$:
$$\int f(x)\,dx=F(x)+C\qquad\text{means}\qquad F'(x)=f(x).$$
This is the **indefinite integral** (no limits). The **constant of integration** $C$ stands for "any constant": all antiderivatives differ by a constant, and adding a constant never changes the derivative.

*Do not confuse:* $\int_a^bf\,dx$ is a **number** (an area); $\int f\,dx$ is a **family of functions**.

**How to check an antiderivative: differentiate it.** You never have to wonder whether an integral is right. This is the great asymmetry of calculus: differentiating is mechanical, integrating is a search — but checking the result of the search is mechanical again.

## 4.2 The table: every derivative, read backwards

| because $\dfrac{d}{dx}[\ \ ]$ | | we have $\displaystyle\int\ \ dx$ |
|---|---|---|
| $\dfrac{d}{dx}\left[\dfrac{x^{n+1}}{n+1}\right]=x^n$ | | $\displaystyle\int x^n\,dx=\frac{x^{n+1}}{n+1}+C\quad(n\ne-1)$ |
| $\dfrac{d}{dx}[\ln\lvert x\rvert]=\dfrac1x$ | | $\displaystyle\int\frac1x\,dx=\ln\lvert x\rvert+C$ |
| $\dfrac{d}{dx}[e^x]=e^x$ | | $\displaystyle\int e^x\,dx=e^x+C$ |
| $\dfrac{d}{dx}\left[\dfrac{e^{kx}}{k}\right]=e^{kx}$ | | $\displaystyle\int e^{kx}\,dx=\frac{e^{kx}}{k}+C$ |
| $\dfrac{d}{dx}[-\cos x]=\sin x$ | | $\displaystyle\int\sin x\,dx=-\cos x+C$ |
| $\dfrac{d}{dx}[\sin x]=\cos x$ | | $\displaystyle\int\cos x\,dx=\sin x+C$ |
| $\dfrac{d}{dx}[\tan x]=\dfrac{1}{\cos^2x}$ | | $\displaystyle\int\frac{1}{\cos^2x}\,dx=\tan x+C$ |
| $\dfrac{d}{dx}[\arctan x]=\dfrac{1}{1+x^2}$ | | $\displaystyle\int\frac{1}{1+x^2}\,dx=\arctan x+C$ |
| $\dfrac{d}{dx}[\arcsin x]=\dfrac{1}{\sqrt{1-x^2}}$ | | $\displaystyle\int\frac{1}{\sqrt{1-x^2}}\,dx=\arcsin x+C$ |

**The power rule for integrals, in words:** *raise the power by one and divide by the new power* — the reverse of "bring the power down and reduce it by one".

**Why $n=-1$ is the exception.** The formula would give $\frac{x^0}{0}$: division by zero. The gap is filled by the logarithm: $\int\frac1x\,dx=\ln|x|+C$. (Why $|x|$? For $x<0$, $\frac{d}{dx}\ln(-x)=\frac{-1}{-x}=\frac1x$ by the chain rule. So $\ln|x|$ works on both sides of zero.)

**The signs of sine and cosine.** $\int\sin=-\cos$ and $\int\cos=+\sin$. If in doubt, differentiate your answer.

**Linearity** carries over from derivatives: integrate term by term, constants come out.

**Worked example 1.** $\displaystyle\int\left(6x^2-\frac{4}{x^3}+2\right)dx$. Rewrite $\frac{4}{x^3}=4x^{-3}$:
$$=6\cdot\frac{x^3}{3}-4\cdot\frac{x^{-2}}{-2}+2x+C=2x^3+\frac{2}{x^2}+2x+C .$$
*Check:* $\frac{d}{dx}\big[2x^3+2x^{-2}+2x\big]=6x^2-4x^{-3}+2$ ✓

**Worked example 2.** $\displaystyle\int\sqrt{x}\,dx=\int x^{1/2}\,dx=\frac{x^{3/2}}{3/2}+C=\frac23x^{3/2}+C$.

**Worked example 3 (from your diagnostic).**
$$\int_0^1\frac{dx}{1+x^2}=\big[\arctan x\big]_0^1=\arctan1-\arctan0=\frac\pi4 .$$
A region bounded by a simple rational curve has area $\frac\pi4$: the inverse trig derivatives of Unit 2 week 3 at work.

**Worked example 4.** $\displaystyle\int_1^e\frac1x\,dx=\big[\ln x\big]_1^e=1-0=1$. (This is one way to *define* $e$: the number for which the area under $\frac1x$ from 1 reaches exactly 1.)

**Worked example 5 — tidy first.** $\displaystyle\int\frac{x^2+1}{x}\,dx=\int\left(x+\frac1x\right)dx=\frac{x^2}{2}+\ln|x|+C$. As with derivatives: no quotient rule exists for integrals; divide out first.
''')
B.code(r'''
# Check worked example 3 numerically - and then use this cell to check your own answers.
print('numerical value :', nint(lambda v: 1 / (1 + v**2), 0, 1))
print('pi / 4          :', pi / 4)
''')
B.ask(r'''Find an antiderivative of $4x^3-6x+5$.''', 'anti', '4*x**3 - 6*x + 5',
      r'''$x^4-3x^2+5x$ (plus any constant). Check: its derivative is $4x^3-6x+5$ ✓.''',
      r'''Raise each power by one and divide by the new power; the constant 5 becomes $5x$. Differentiate your answer to check it.''',
      fmt="a formula in `x` as text (the constant $C$ is not needed)", sample='x**4 - 3*x**2 + 5*x')
B.ask(r'''Evaluate $\displaystyle\int_0^{\pi/2}\cos x\,dx$.''', 'num', 1,
      r'''$\big[\sin x\big]_0^{\pi/2}=1-0=1$.''',
      r'''An antiderivative of $\cos x$ is $\sin x$.''')

B.md(r'''
## 4.3 Net change: the theorem in physics

**Build.** Read FTC 2 with $F'$ as a rate:
$$\int_a^b(\text{rate of change of }F)\,dt=F(b)-F(a)=\text{net change of }F .$$

| the rate | integrated over time gives |
|---|---|
| velocity $v=\frac{ds}{dt}$ | displacement $s(b)-s(a)$ |
| acceleration $a=\frac{dv}{dt}$ | change in velocity |
| current $i=\frac{dq}{dt}$ | charge that has flowed |
| power $P=\frac{dE}{dt}$ | energy used |
| flow rate (litres/s) | volume delivered |

**Worked example.** A ball is thrown up with velocity $v(t)=20-10t$ m/s.

*Displacement from $t=0$ to $t=3$:*
$$\int_0^3(20-10t)\,dt=\big[20t-5t^2\big]_0^3=60-45=15\ \text{m}.$$
*Total distance travelled:* the ball rises until $v=0$ at $t=2$, then falls. Up: $\int_0^2v\,dt=[20t-5t^2]_0^2=20$ m. Down: $\int_2^3v\,dt=15-20=-5$ m. Distance $=20+5=25$ m; displacement $=20-5=15$ m ✓.

### Experiment 3 — distance from a speed that has no formula
A parachutist falls with air resistance: the acceleration is $g-c\,v^2$. The cell steps the velocity forward in time (as in Unit 2), and at the same time **accumulates distance** by adding $v\,\Delta t$ — a Riemann sum, built while the simulation runs.

**Predict first:** sketch the velocity against time. What happens to it in the long run? What does that mean for the distance graph?
''')
B.code(r'''
def fall(c=0.004, dt=0.05):
    g, v, s = 9.81, 0.0, 0.0
    ts, vs, ss = [0.0], [0.0], [0.0]
    while ts[-1] < 20:
        v = v + (g - c * v**2) * dt        # velocity changes at the rate a = g − c v²
        s = s + v * dt                     # distance accumulates: one more thin rectangle v·dt
        ts.append(ts[-1] + dt); vs.append(v); ss.append(s)
    fig, (a1, a2) = plt.subplots(1, 2, figsize=(10.5, 3.5))
    a1.plot(ts, vs); a1.fill_between(ts, 0, vs, alpha=0.2); a1.set_xlabel('t (s)'); a1.set_ylabel('velocity (m/s)')
    a2.plot(ts, ss, 'r'); a2.set_xlabel('t (s)'); a2.set_ylabel('distance fallen (m)'); plt.show()
    print(f'terminal velocity sqrt(g/c) = {sqrt(g / c):.1f} m/s     distance after 20 s = {ss[-1]:.0f} m  (the shaded area)')

explore(fall, c=(0.001, 0.02, 0.001, 0.004))
''')
B.md(r'''
*Explain:* the velocity levels off at the terminal velocity $\sqrt{g/c}$, where gravity and drag balance. From then on the area under the velocity curve grows at a constant rate, so the distance graph becomes a straight line whose slope is the terminal velocity. Distance is the integral of velocity; velocity is the derivative of distance — you are looking at both statements at once.
''')

B.md(r'''
## Week summary — everything on one page

**Sums.** $\displaystyle\sum_{k=1}^nk=\frac{n(n+1)}{2},\qquad\sum_{k=1}^nk^2=\frac{n(n+1)(2n+1)}{6}$.

**Definition.** $\displaystyle\int_a^bf(x)\,dx=\lim_{n\to\infty}\sum_{k=1}^nf(x_k)\,\Delta x$: signed area; total of rate × time.

**Properties.** Linear; $\int_a^b+\int_b^c=\int_a^c$; $\int_b^a=-\int_a^b$; odd function over $[-a,a]$ gives $0$.

**Fundamental theorem.**
1. $\dfrac{d}{dx}\displaystyle\int_a^xf(t)\,dt=f(x)$ — area accumulates at the rate "height".
2. $\displaystyle\int_a^bf(x)\,dx=F(b)-F(a)$ for any $F$ with $F'=f$ — the sum of all the little changes is the total change.

**Antiderivatives.** $\int x^n=\frac{x^{n+1}}{n+1}$ ($n\ne-1$), $\int\frac1x=\ln|x|$, $\int e^{kx}=\frac{e^{kx}}{k}$, $\int\sin=-\cos$, $\int\cos=\sin$, $\int\frac{1}{1+x^2}=\arctan x$. Always $+C$; always check by differentiating.

**Net change.** $\int v\,dt$ = displacement, $\int i\,dt$ = charge, $\int P\,dt$ = energy.
''')

# =====================================================================================
B.md(r'''
---
# Problems

Paper first; check with `nint` in the scratch cell if you like. First attempt counts. `hint(n)` → `solution(n)` → `mistake(n, '...')`.

### Sums and Riemann sums
''')
B.problem(S1, r'Compute $\displaystyle\sum_{k=1}^{20}(3k-1)$.', 'num', 610,
          [r'Split: $3\sum k-\sum1$.', r'$\sum_{k=1}^{20}k=\frac{20\cdot21}{2}=210$ and $\sum_{k=1}^{20}1=20$.'],
          r'''$$\sum_{k=1}^{20}(3k-1)=3\sum_{k=1}^{20}k-\sum_{k=1}^{20}1=3\cdot\frac{20\cdot21}{2}-20=630-20=610 .$$''')
B.problem(S1, r'Compute the **left** Riemann sum for $f(x)=x^2+1$ on $[0,2]$ with $n=4$.', 'num', 3.75,
          [r'$\Delta x=0.5$. Left end points: $0,\ 0.5,\ 1,\ 1.5$.'],
          r'''$\Delta x=0.5$; left ends $0,0.5,1,1.5$; heights $1,\ 1.25,\ 2,\ 3.25$ (sum $7.5$).

$L_4=7.5\cdot0.5=$ **3.75**. (Exact area: $\frac83+2=4.667$; the left sum of a rising function underestimates.)''')
B.problem(S1, r'The right Riemann sum for $f(x)=x$ on $[0,4]$ with $n$ strips can be written in closed form using $\sum k=\frac{n(n+1)}{2}$. What is its value for $n=8$?', 'num', 9,
          [r'$\Delta x=\frac4n$, $x_k=\frac{4k}{n}$, so $R_n=\sum\frac{4k}{n}\cdot\frac4n=\frac{16}{n^2}\sum k$.', r'$R_n=\frac{16}{n^2}\cdot\frac{n(n+1)}{2}=\frac{8(n+1)}{n}$.'],
          r'''$$R_n=\sum_{k=1}^n\frac{4k}{n}\cdot\frac4n=\frac{16}{n^2}\cdot\frac{n(n+1)}{2}=\frac{8(n+1)}{n}=8+\frac8n .$$
For $n=8$: **9**. As $n\to\infty$: $8$, the area of the triangle $\frac12\cdot4\cdot4$ ✓.''')
B.md(r'''
### The definite integral
''')
B.problem(S2, r'Use geometry: $\displaystyle\int_{-3}^{3}\sqrt{9-x^2}\,dx$.', 'num', 4.5 * math.pi,
          [r'$y=\sqrt{9-x^2}$ is the upper half of a circle. Which radius?'],
          r'''Upper half of the circle $x^2+y^2=9$, radius 3: area $\frac12\pi\cdot9=\dfrac{9\pi}{2}\approx$ **14.14**.''', fmt='a number; you can type `9*pi/2`')
B.problem(S2, r'If $\displaystyle\int_0^2f\,dx=3$ and $\displaystyle\int_2^5f\,dx=-1$, what is $\displaystyle\int_0^52f(x)\,dx$?', 'num', 4,
          [r'First $\int_0^5f=\int_0^2f+\int_2^5f$. Then the factor 2 comes out.'],
          r'''$\int_0^5f\,dx=3+(-1)=2$, so $\int_0^52f\,dx=2\cdot2=$ **4**.''')
B.problem(S2, r'What is the total **area** (all counted positive) between $y=\sin x$ and the $x$-axis for $0\le x\le2\pi$?', 'num', 4,
          [r'The integral over $[0,2\pi]$ is 0 because the arches cancel. Treat the two arches separately.', r'$\int_0^\pi\sin x\,dx=2$, and the second arch has the same size.'],
          r'''$\int_0^\pi\sin x\,dx=[-\cos x]_0^\pi=2$. The arch from $\pi$ to $2\pi$ lies below the axis: its integral is $-2$, its area $2$.

Total area $2+2=$ **4** (whereas the integral $\int_0^{2\pi}\sin x\,dx=0$).''')
B.md(r'''
### The fundamental theorem
''')
B.problem(S3, r'Let $g(x)=\displaystyle\int_0^x\cos(t^2)\,dt$. Find $g\,^\prime(\sqrt\pi)$.', 'num', -1,
          [r'FTC 1: the derivative is the integrand evaluated at $x$.'],
          r'''$g'(x)=\cos(x^2)$, so $g'(\sqrt\pi)=\cos\pi=$ **−1**.''')
B.problem(S3, r'$\displaystyle\int_1^3(3x^2-2x)\,dx$', 'num', 18,
          [r'Antiderivative: $x^3-x^2$.'],
          r'''$$\big[x^3-x^2\big]_1^3=(27-9)-(1-1)=18 .$$''')
B.problem(S3, r'$\displaystyle\int_0^{\pi}\sin x\,dx$ *(from your diagnostic)*', 'num', 2,
          [r'An antiderivative of $\sin x$ is $-\cos x$. Careful with the signs when you subtract.'],
          r'''$$\big[-\cos x\big]_0^\pi=(-\cos\pi)-(-\cos0)=(1)-(-1)=2 .$$''')
B.problem(S3, r'$\displaystyle\int_0^{1}\frac{dx}{1+x^2}$ *(from your diagnostic)*', 'num', math.pi / 4,
          [r'Which function has derivative $\frac{1}{1+x^2}$? (Unit 2 week 3.)'],
          r'''$$\big[\arctan x\big]_0^1=\arctan1-\arctan0=\frac\pi4\approx0.785 .$$''', fmt='a number; you can type `pi/4`')
B.problem(S3, r'$\displaystyle\int_0^4\sqrt{x}\,dx$', 'num', 16 / 3,
          [r'$\sqrt{x}=x^{1/2}$; raise the power to $\frac32$ and divide by $\frac32$.', r'$\left[\frac23x^{3/2}\right]_0^4$ and $4^{3/2}=8$.'],
          r'''$$\int_0^4x^{1/2}\,dx=\left[\tfrac23x^{3/2}\right]_0^4=\tfrac23\cdot8=\frac{16}{3}\approx5.33 .$$''', fmt='a number, e.g. `16/3`')
B.problem(S3, r'$\displaystyle\int_0^{\ln2}e^x\,dx$', 'num', 1,
          [r'$e^{\ln2}=2$.'],
          r'''$$\big[e^x\big]_0^{\ln2}=e^{\ln2}-e^0=2-1=1 .$$''')
B.problem(S3, r'$\displaystyle\int_1^{e^2}\frac{3}{x}\,dx$', 'num', 6,
          [r'$3\ln x$, and $\ln(e^2)=2$.'],
          r'''$$\big[3\ln x\big]_1^{e^2}=3\cdot2-3\cdot0=6 .$$''')
B.md(r'''
### Antiderivatives and applications
''')
B.problem(S4, r'Find an antiderivative of $6x^2-\dfrac{4}{x^3}+2$.', 'anti', '6*x**2 - 4/x**3 + 2',
          [r'Rewrite $\frac{4}{x^3}$ as $4x^{-3}$. Raising $-3$ by one gives $-2$.', r'$-4\cdot\frac{x^{-2}}{-2}=+2x^{-2}$.'],
          r'''$$\int\left(6x^2-4x^{-3}+2\right)dx=2x^3-4\cdot\frac{x^{-2}}{-2}+2x+C=2x^3+\frac{2}{x^2}+2x+C .$$
Check by differentiating: $6x^2-4x^{-3}+2$ ✓.''', fmt="a formula in `x` as text (no $+C$ needed)", sample='2*x**3 + 2/x**2 + 2*x')
B.problem(S4, r'Find an antiderivative of $\cos x-3\sin x+e^{2x}$.', 'anti', 'cos(x) - 3*sin(x) + exp(2*x)',
          [r'$\int\cos=\sin$, $\int\sin=-\cos$, $\int e^{2x}=\frac{e^{2x}}{2}$.'],
          r'''$$\sin x-3(-\cos x)+\frac{e^{2x}}{2}+C=\sin x+3\cos x+\tfrac12e^{2x}+C .$$
Check: $\cos x-3\sin x+e^{2x}$ ✓.''', fmt="a formula in `x` as text; write $e^{2x}$ as `exp(2*x)`", sample='sin(x) + 3*cos(x) + exp(2*x)/2')
B.problem(S4, r'A ball has velocity $v(t)=20-10t$ m/s. What **total distance** (not displacement) does it travel between $t=0$ and $t=3$ s?', 'num', 25,
          [r'The velocity changes sign at $t=2$. Integrate over $[0,2]$ and $[2,3]$ separately.', r'Up: $20$ m. Down: $-5$ m, i.e. 5 m of travel.'],
          r'''$v=0$ at $t=2$. With $F(t)=20t-5t^2$:

Up: $\int_0^2v\,dt=F(2)-F(0)=20$ m. Down: $\int_2^3v\,dt=F(3)-F(2)=15-20=-5$ m.

Distance $=20+5=$ **25 m** (the displacement is $15$ m).''', fmt='metres')
B.problem(S4, r'The current in a wire is $i(t)=3t^2$ amperes. How much **charge** (in coulombs) flows between $t=0$ and $t=2$ s?', 'num', 8,
          [r'$q=\int i\,dt$.'],
          r'''$$q=\int_0^23t^2\,dt=\big[t^3\big]_0^2=8\ \text{C}.$$''', fmt='coulombs')
B.problem(S4, r'A function has $f\,^\prime(x)=6x^2-2$ and $f(1)=5$. Find $f(2)$.', 'num', 17,
          [r'Net change: $f(2)-f(1)=\int_1^2f\,^\prime(x)\,dx$.'],
          r'''$$f(2)-f(1)=\int_1^2(6x^2-2)\,dx=\big[2x^3-2x\big]_1^2=(16-4)-(2-2)=12 .$$
So $f(2)=5+12=$ **17**. (Equivalently: $f(x)=2x^3-2x+C$ with $C=5$ from $f(1)=5$.)''')
B.code(r'''
# scratch cell: check an integral numerically, e.g.  nint(lambda v: sqrt(v), 0, 4)
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
1. Why is distance the area under the velocity graph, even when the velocity changes?
2. Compute $\int_0^1x^2\,dx$ from the definition (right sums and the formula for $\sum k^2$).
3. Draw the "thin strip" picture and explain why $\frac{d}{dx}\int_a^xf=f(x)$.
4. Prove $\int_a^bf=F(b)-F(a)$ from part 1. Where is "same derivative ⇒ differ by a constant" used?
5. Why is $\int\frac1x\,dx$ not given by the power rule?

*Your answers:*

&nbsp;

### 3 · Physics strand — position is the integral of velocity (1 hour)
The projectile simulator plots velocity and position. Drag is off, launch straight-ish up at $80^\circ$ with $v_0=20$ m/s, so the vertical velocity is $v_y(t)=19.7-9.81t$.

**Predict first:** the maximum height is the area under the $v_y$ graph up to the moment $v_y=0$ — a triangle. Compute it. Then read the maximum height from the simulator. Export the data with **CSV** if you want to add up $v_y\,\Delta t$ yourself and compare with the height column.
''')
B.code(r'''
lab('physics', exp='proj', k=0, v0=20, ang=80)
''')
B.md(r'''
### 4 · What comes next
The table of §4.2 handles sums of basic functions. **Week 2** is about everything else: integrals that need the chain rule backwards (*substitution*), the product rule backwards (*integration by parts*), and — when no antiderivative exists — accurate numerical methods.
''')

if __name__ == '__main__':
    B.write()
