"""Unit 4 · Week 1 (course week 11) - Sequences and infinite series."""
import math
from nbkit import Book
import figs_u04 as F

B = Book('u04w1', 'Unit 4 · Week 1 — Sequences and infinite series', 'year1/u04w1-sequences-series.ipynb')
S1, S2, S3, S4 = '1 Sequences', '2 Geometric series', '3 Divergence and comparison', '4 Convergence tests'

B.md(r'''
# Unit 4 · Week 1 — Sequences and infinite series
*Term 1, week 11 of 12 · about 15 hours in this notebook and on paper*

**Where you are.** Three times already the course has met an infinite process and promised to make sense of it "in Unit 4": the number $e=\lim(1+\frac1n)^n$, approximations such as $e^x\approx1+x+\frac{x^2}{2}$ that seemed to want *more* terms, and the improper integral $\int_1^\infty\frac{dx}{x^p}$ whose borderline was $p=1$. This unit keeps those promises.

The question of this week sounds simple and is not: **what does it mean to add infinitely many numbers?** Sometimes the answer is a perfectly ordinary number ($\frac12+\frac14+\frac18+\dots=1$). Sometimes there is no answer, even though the terms shrink to zero ($1+\frac12+\frac13+\dots$ grows without bound). You will learn to tell the two apart — and why it matters: next week every function you know will be written as such an infinite sum.

**What you will be able to do at the end of this week**
1. Compute limits of sequences and say why a rising, bounded sequence must converge; finish the proof that $e$ exists.
2. Define the sum of a series through its partial sums; derive and use the formula for a geometric series.
3. Prove that the harmonic series diverges, and explain why "terms → 0" is not enough.
4. Decide convergence with the comparison, integral, ratio and alternating-series tests, and bound the error of a partial sum.

**What is used from earlier:** limits (Unit 1 week 3), the improper integrals $\int_1^\infty x^{-p}\,dx$ (Unit 3 week 3), L'Hôpital and "exponentials beat powers" (Unit 2 week 4).

Run the grey *SETUP* cell first.
''')

# =====================================================================================
B.md(r'''
---
# Part 1 — Sequences

## 1.1 What a sequence is

**Build.** A **sequence** is an infinite list of numbers in a definite order:
$$a_1,\ a_2,\ a_3,\ \dots$$
Usually given by a formula for the $n$-th term, $a_n$. It is just a function whose inputs are the whole numbers $1,2,3,\dots$

| formula | first terms |
|---|---|
| $a_n=\dfrac1n$ | $1,\ \frac12,\ \frac13,\ \frac14,\ \dots$ |
| $a_n=\dfrac{n}{n+1}$ | $\frac12,\ \frac23,\ \frac34,\ \frac45,\ \dots$ |
| $a_n=(-1)^n$ | $-1,\ 1,\ -1,\ 1,\ \dots$ |
| $a_n=2^n$ | $2,\ 4,\ 8,\ 16,\ \dots$ |

Sequences can also be defined **recursively**: each term from the previous one. Newton's method (Unit 2 week 3) produced a sequence $x_{n+1}=\frac12\big(x_n+\frac2{x_n}\big)$ that closed in on $\sqrt2$.

## 1.2 Limits of sequences

**Build.** $\displaystyle\lim_{n\to\infty}a_n=L$ means exactly what $\lim_{x\to\infty}f(x)=L$ meant in Unit 1: the terms get as close to $L$ as we like, and stay there, once $n$ is large enough. The sequence **converges** to $L$. Otherwise it **diverges** — by growing without bound ($2^n$) or by never settling ($(-1)^n$).

All the limit techniques of Unit 1 week 3 apply unchanged:

**Worked example 1.** $a_n=\dfrac{3n^2+1}{n^2-5n}$. Divide top and bottom by $n^2$: $\dfrac{3+\frac{1}{n^2}}{1-\frac5n}\to\dfrac31=3$.

**Worked example 2.** $a_n=\dfrac{n^2}{2^n}$. "Exponentials beat powers" (L'Hôpital twice on $\frac{x^2}{2^x}$): $a_n\to0$.

**Worked example 3.** $a_n=r^n$ — the most important sequence of all.
- $|r|<1$: $r^n\to0$ (each factor shrinks it further: $0.9^n$ is $0.35$ at $n=10$, $0.000027$ at $n=100$).
- $r=1$: constant 1. $\;r>1$: grows without bound. $\;r\le-1$: jumps between signs, no limit.

**Worked example 4 — a recursive sequence.** $a_1=1$, $a_{n+1}=\sqrt{2+a_n}$. Terms: $1,\ 1.732,\ 1.932,\ 1.983,\ 1.996,\dots$ If it converges to some $L$, then taking the limit of both sides of the rule gives $L=\sqrt{2+L}$, so $L^2-L-2=0$, $(L-2)(L+1)=0$, and $L=2$ (the terms are positive). *Careful:* this finds the only possible limit; it does not prove that there is one. That needs the next idea.
''')
B.ask(r'''Find $\displaystyle\lim_{n\to\infty}\frac{5n+2}{2n-1}$.''', 'num', 2.5,
      r'''Divide by $n$: $\dfrac{5+\frac2n}{2-\frac1n}\to\dfrac52$.''',
      r'''Divide top and bottom by $n$.''')
B.ask(r'''Does $a_n=(0.99)^n$ converge? If so, give its limit.''', 'num', 0,
      r'''$|r|=0.99<1$, so $r^n\to0$ — slowly ($0.99^{100}\approx0.37$, $0.99^{1000}\approx0.00004$), but surely.''',
      r'''$r^n$ with $|r|<1$.''')

B.md(r'''
## 1.3 Rising and bounded: the completeness of the real numbers

**Why.** Many sequences come without a formula for their limit — the recursion above, or $(1+\frac1n)^n$. How can we know a limit exists when we cannot compute it?

**The principle (monotone convergence).** *A sequence that never decreases and never exceeds some fixed number converges.* (Likewise one that never increases and stays above some number.)

**Why it is believable.** The terms creep upwards but can never pass the ceiling $M$. They pile up somewhere at or below $M$ — at the lowest ceiling of all. A picture: a ball rolling up to a wall it can never pass, ever more slowly.

*(Honesty note: that "the lowest ceiling exists as a real number" is precisely the property that distinguishes the real numbers from, for instance, the fractions. The sequence $1,\ 1.4,\ 1.41,\ 1.414,\dots$ of decimal approximations of $\sqrt2$ consists of fractions, rises, is bounded by 2, and yet has no limit among the fractions. Courses in analysis take this property as an axiom. We use it.)*

## 1.4 The promise of Unit 1: why $e$ exists

In Unit 1 week 3 you saw a table in which $(1+\frac1n)^n$ rose towards $2.718\dots$, and were told that a proof would come. Here it is.

**Step 1 — expand with the binomial theorem.** For a whole number $n$ (the "pick 1 or $\frac1n$ from each bracket" counting of Unit 2 week 1):
$$\left(1+\frac1n\right)^n=\sum_{k=0}^{n}\binom nk\frac{1}{n^k},\qquad\binom nk=\frac{n(n-1)\cdots(n-k+1)}{k!}.$$

**Step 2 — rewrite each term.** Spread the $n^k$ over the $k$ factors on top:
$$\binom nk\frac{1}{n^k}=\frac{1}{k!}\cdot\frac nn\cdot\frac{n-1}{n}\cdots\frac{n-k+1}{n}=\frac{1}{k!}\left(1-\frac1n\right)\left(1-\frac2n\right)\cdots\left(1-\frac{k-1}{n}\right).$$

**Step 3 — the sequence rises.** Going from $n$ to $n+1$, every bracket $\left(1-\frac jn\right)$ becomes $\left(1-\frac j{n+1}\right)$, which is **larger**; and one extra positive term appears. So every term grows and there are more of them: $a_{n+1}>a_n$.

**Step 4 — the sequence is bounded.** Every bracket is less than 1, so each term is at most $\frac{1}{k!}$. And $k!=1\cdot2\cdot3\cdots k\ge2^{k-1}$ (every factor after the first is at least 2). Hence
$$\left(1+\frac1n\right)^n\le1+1+\frac12+\frac14+\frac18+\dots<1+2=3 .$$
(The sum $1+\frac12+\frac14+\dots=2$ is the geometric series of §2.2, below.)

**Step 5 — conclude.** Rising and bounded by 3: by the principle of §1.3 it converges. Its limit is called $e$. $\blacksquare$

Step 4 also showed more: letting $n\to\infty$ term by term suggests
$$e=1+1+\frac{1}{2!}+\frac{1}{3!}+\frac{1}{4!}+\dots$$
— a much faster way to compute it (Experiment 1). Next week you will see that this is the case $x=1$ of a series for $e^x$.

### Experiment 1 — two roads to $e$
**Predict first:** to get 6 correct decimals of $e$, roughly how large must $n$ be in $(1+\frac1n)^n$? How many terms of $1+1+\frac1{2!}+\frac1{3!}+\dots$?
''')
B.code(r'''
rows = []
s, fact = 0.0, 1
for k in range(0, 13):
    if k > 0: fact *= k
    s += 1 / fact
    n = 10 ** (k // 2 + 1)
    rows.append([k + 1, s, abs(s - e), n, (1 + 1 / n) ** n, abs((1 + 1 / n) ** n - e)])
table(['terms', 'sum 1/k!', 'error', 'n', '(1+1/n)^n', 'error '], rows, fmt='%.3g')
''')
B.md(r'''
*Explain:* the series reaches 6 decimals with about 10 terms; $(1+\frac1n)^n$ needs $n\approx10^6$ (and loses digits to rounding before it gets much better). The error of $(1+\frac1n)^n$ shrinks like $\frac{e}{2n}$; the error of the series like the first omitted term, $\frac{1}{k!}$ — which shrinks faster than any power.
''')
B.ask(r'''The sequence $a_1=1$, $a_{n+1}=\sqrt{6+a_n}$ rises and stays below 3. What is its limit?''', 'num', 3,
      r'''If $a_n\to L$ then $L=\sqrt{6+L}$, so $L^2-L-6=(L-3)(L+2)=0$; the terms are positive, so $L=3$.''',
      r'''Put $L$ on both sides of the rule: $L=\sqrt{6+L}$. Square and solve.''')

# =====================================================================================
B.md(r'''
---
# Part 2 — Series

## 2.1 What an infinite sum means

**Why.** You cannot add infinitely many numbers one after another — you would never finish. But you can add the first $n$ and watch what happens as $n$ grows. That turns an infinite sum into a limit of a sequence, which you already know how to handle.

**Build.** Given terms $a_1,a_2,a_3,\dots$, form the **partial sums**
$$S_1=a_1,\quad S_2=a_1+a_2,\quad S_3=a_1+a_2+a_3,\quad\dots,\quad S_n=\sum_{k=1}^{n}a_k .$$
If the sequence of partial sums has a limit $S$, the **series** $\sum_{k=1}^\infty a_k$ **converges** and we write
$$\sum_{k=1}^{\infty}a_k=S=\lim_{n\to\infty}S_n .$$
If $S_n$ has no limit, the series **diverges**.

So an infinite sum is not a sum at all: it is the limit of finite sums. The notation $\sum_{k=1}^\infty a_k$ means that limit — when it exists.
''')
B.fig('partial_sums', F.partial_sums, 'Two series whose terms both shrink to zero. Only one has a sum.')
B.md(r'''
## 2.2 The geometric series

**Why.** Each term is a fixed multiple $r$ of the one before: $a+ar+ar^2+ar^3+\dots$ It is the most important series there is — compound interest, bouncing balls, signals echoing in a cable, and next week the key to all power series.

**Build.**

**Step 1 — the finite sum.** Let $S_n=a+ar+ar^2+\dots+ar^{n-1}$ ($n$ terms). Multiply by $r$:
$$rS_n=ar+ar^2+\dots+ar^{n-1}+ar^n .$$

**Step 2 — subtract.** Almost everything cancels (the same telescoping trick as for $\sum k^2$ in Unit 3):
$$S_n-rS_n=a-ar^n\qquad\Rightarrow\qquad S_n=a\,\frac{1-r^n}{1-r}\quad(r\ne1).$$

**Step 3 — let $n\to\infty$.** Everything depends on $r^n$ (§1.2, example 3):
- $|r|<1$: $r^n\to0$, so $\displaystyle S_n\to\frac{a}{1-r}$.
- $|r|\ge1$: the terms do not shrink to zero; the partial sums have no limit.

$$\boxed{\,a+ar+ar^2+ar^3+\dots=\frac{a}{1-r}\qquad\text{for }|r|<1\,}$$
''')
B.fig('halves_square', F.halves_square, 'One half, one quarter, one eighth, … of a unit square: they fill it exactly.')
B.md(r'''
**Worked example 1.** $\frac12+\frac14+\frac18+\dots$: first term $a=\frac12$, ratio $r=\frac12$. Sum $\dfrac{1/2}{1-1/2}=1$ — the picture above.

**Worked example 2 — a repeating decimal.** $0.\overline{3}=0.333\ldots=\frac3{10}+\frac3{100}+\dots$: $a=\frac{3}{10}$, $r=\frac1{10}$: sum $\dfrac{3/10}{9/10}=\dfrac13$.
And $0.\overline{9}=\dfrac{9/10}{9/10}=1$. Yes: $0.999\ldots$ **is** $1$ — the partial sums $0.9,0.99,0.999,\dots$ have limit 1, and the infinite decimal *means* that limit.

**Worked example 3 — the bouncing ball.** A ball dropped from 2 m bounces back to 60 % of its previous height each time. Total distance travelled?
''')
B.fig('bounce', F.bounce, 'Infinitely many bounces, ever smaller.')
B.md(r'''
Down 2 m. Then each bounce goes up and comes down the same height: $2\cdot(1.2+0.72+0.432+\dots)$, a geometric series with $a=1.2$, $r=0.6$:
$$2+2\cdot\frac{1.2}{1-0.6}=2+2\cdot3=8\ \text{m}.$$
Infinitely many bounces, a finite distance. (And a finite *time*, too: each flight time is proportional to the square root of the height, giving a geometric series with ratio $\sqrt{0.6}$.)

**Worked example 4 — starting later.** $\sum_{k=2}^\infty\left(\frac23\right)^k=\frac49+\frac8{27}+\dots$: first term $\frac49$, ratio $\frac23$: sum $\dfrac{4/9}{1/3}=\dfrac43$. *Always identify the first term actually present* — the most common slip is to use $a=1$ out of habit.

### Experiment 2 — partial sums with a slider
**Predict first:** for $r=0.9$, how many terms until the partial sum is within 1 % of $\frac{1}{1-r}$? What happens for $r=-0.9$? For $r=1$?
''')
B.code(r'''
def geo(r=0.5, n=30):
    k = np.arange(n)
    S = np.cumsum(r ** k)
    plt.figure(figsize=(8, 3.4))
    plt.plot(np.arange(1, n + 1), S, 'o-', ms=4, label='partial sums of 1 + r + r² + …')
    if abs(r) < 1: plt.axhline(1 / (1 - r), color='r', ls='--', label='1 / (1 − r) = %.4g' % (1 / (1 - r)))
    plt.xlabel('number of terms'); plt.legend(); plt.show()
    print('last partial sum:', S[-1])

explore(geo, r=(-1.2, 1.2, 0.05, 0.5), n=(5, 80, 5, 30))
''')
B.ask(r'''Find $\displaystyle\sum_{k=0}^{\infty}\left(\frac13\right)^k$.''', 'num', 1.5,
      r'''$a=1$ (the $k=0$ term), $r=\frac13$: $\dfrac{1}{1-1/3}=\dfrac32$.''',
      r'''First term (at $k=0$) is 1; ratio $\frac13$.''')
B.ask(r'''Write $0.\overline{45}=0.454545\ldots$ as a fraction (type it as `a/b`).''', 'num', 45 / 99,
      r'''$\frac{45}{100}+\frac{45}{100^2}+\dots$: $a=\frac{45}{100}$, $r=\frac1{100}$, sum $\dfrac{45/100}{99/100}=\dfrac{45}{99}=\dfrac5{11}$.''',
      r'''The block "45" repeats every two digits: ratio $\frac{1}{100}$.''', fmt='a fraction, e.g. `5/11`')

# =====================================================================================
B.md(r'''
---
# Part 3 — Divergence, and the harmonic series

## 3.1 The terms must go to zero

**Build.** If $\sum a_k$ converges to $S$, then $a_n=S_n-S_{n-1}\to S-S=0$. So:

> **Divergence test.** If the terms $a_n$ do **not** tend to 0, the series diverges.

Examples: $\sum\frac{n}{n+1}$ diverges (terms → 1); $\sum(-1)^n$ diverges (terms do not settle at all).

**The trap — the converse is false.** Terms tending to 0 do **not** guarantee convergence. The next section shows the most famous example.

## 3.2 The harmonic series diverges

$$1+\frac12+\frac13+\frac14+\frac15+\dots$$
The terms go to zero. The partial sums grow ever more slowly ($S_{100}\approx5.19$, $S_{1000}\approx7.49$, $S_{10^6}\approx14.39$). It looks as if they might level off. They do not.

**Proof (by grouping; Oresme, around 1350).** Group the terms in blocks that end at $\frac12,\frac14,\frac18,\frac1{16},\dots$:
''')
B.fig('harmonic_groups', F.harmonic_groups, 'Each block of terms adds more than one half.')
B.md(r'''
- $\frac13+\frac14>\frac14+\frac14=\frac12$ (replace each term by the smallest in the block).
- $\frac15+\frac16+\frac17+\frac18>4\cdot\frac18=\frac12$.
- $\frac19+\dots+\frac1{16}>8\cdot\frac1{16}=\frac12$, and so on.

After $2^m$ terms the partial sum exceeds $1+\frac m2$. Since $m$ can be as large as we like, the partial sums exceed every bound. $\blacksquare$

**How slowly?** The picture in §2.1 suggests $S_n\approx\ln n+0.577$ — the area under $\frac1x$ (Unit 3) plus a constant (Euler's constant $\gamma=0.5772\ldots$). To reach $S_n>100$ you would need about $e^{99.4}\approx10^{43}$ terms. Divergence can be incredibly slow; a computer adding terms would never "see" it.
''')
B.ask(r'''Does $\displaystyle\sum_{n=1}^\infty\frac{n^2}{n^2+1}$ converge? Enter the limit of its **terms** (the divergence test decides the rest).''', 'num', 1,
      r'''The terms tend to 1, not 0, so the series diverges.''',
      r'''What do the terms tend to as $n\to\infty$?''')

# =====================================================================================
B.md(r'''
---
# Part 4 — Convergence tests

**Why.** Most series have no formula for their sum. But often we only need to know *whether* a series converges (if it does, a computer can add enough terms to get its value). The tests below answer that question by comparing with series we already understand.

All four tests are for series of **positive** terms except the last. For positive terms the partial sums only rise, so by §1.3 a series of positive terms converges exactly when its partial sums stay bounded.

## 4.1 Comparison

> If $0\le a_n\le b_n$ for all $n$ and $\sum b_n$ converges, then $\sum a_n$ converges. If $\sum a_n$ diverges, so does $\sum b_n$.

*Why:* the partial sums of $\sum a_n$ rise and are bounded by the sum of $\sum b_n$.

**Worked example.** $\sum\dfrac{1}{2^n+n}$: each term is less than $\dfrac1{2^n}$, and $\sum\frac1{2^n}$ converges (geometric). So it converges.

**Worked example.** $\sum\dfrac{1}{\sqrt n}$: each term is at least $\dfrac1n$, and $\sum\frac1n$ diverges. So it diverges.

## 4.2 The integral test and the $p$-series

**Build.** Compare the series $\sum f(n)$ with the integral $\int_1^\infty f(x)\,dx$, for a positive, decreasing $f$.
''')
B.fig('integral_test', F.integral_test, 'Each bar has width 1 and height f(n): its area is the term f(n).')
B.md(r'''
The bar on $[n,n+1]$ has height $f(n)$, at least as high as the curve over that interval (the curve falls). So the series is at least the integral. Shifting the bars one place to the left puts them *under* the curve, so the series without its first term is at most the integral:
$$\int_1^{\infty}f(x)\,dx\ \le\ \sum_{n=1}^{\infty}f(n)\ \le\ f(1)+\int_1^{\infty}f(x)\,dx .$$

> **Integral test.** For positive decreasing $f$, the series $\sum f(n)$ and the integral $\int_1^\infty f(x)\,dx$ either both converge or both diverge.

**The $p$-series.** With $f(x)=\frac1{x^p}$ and the improper integrals of Unit 3 week 3:
$$\sum_{n=1}^{\infty}\frac1{n^p}\quad\text{converges if }p>1,\ \text{diverges if }p\le1 .$$
The harmonic series is the borderline case $p=1$ — the same borderline as for the integrals.

**Worked example.** $\sum\frac1{n^2}$ converges ($p=2$); the inequality bounds its sum between $\int_1^\infty\frac{dx}{x^2}=1$ and $1+1=2$. (Its exact value is $\frac{\pi^2}{6}\approx1.645$ — a famous result of Euler that needs Fourier series, Unit 12.)

## 4.3 The ratio test

**Build.** Compare with a geometric series. If, far out, each term is roughly $L$ times the one before, the series behaves like a geometric series with ratio $L$:

> **Ratio test.** Let $L=\displaystyle\lim_{n\to\infty}\left|\frac{a_{n+1}}{a_n}\right|$. If $L<1$ the series converges; if $L>1$ it diverges; if $L=1$ the test says nothing.

**Worked example.** $\sum\frac{1}{n!}$: $\dfrac{a_{n+1}}{a_n}=\dfrac{n!}{(n+1)!}=\dfrac1{n+1}\to0<1$: converges (we knew: its sum is $e-1$).

**Worked example.** $\sum\frac{n}{2^n}$: $\dfrac{(n+1)/2^{n+1}}{n/2^n}=\dfrac{n+1}{2n}\to\frac12$: converges.

**Worked example — where it fails.** For $\frac1n$ and for $\frac1{n^2}$ the ratio tends to 1 in both cases, yet one diverges and the other converges. Ratio 1 means: use another test.

The ratio test is the one you will use most next week, for power series.

## 4.4 Alternating series

**Build.** Signs alternate: $b_1-b_2+b_3-b_4+\dots$ with $b_n>0$.

> **Alternating series test.** If $b_n$ decreases and tends to 0, the series converges. Moreover, stopping after $n$ terms makes an error no larger than the **first omitted term**, $b_{n+1}$.
''')
B.fig('alternating', F.alternating, 'The partial sums step down, up, down, … by ever smaller amounts, closing in from both sides.')
B.md(r'''
*Why:* each step overshoots the previous one by less than it moved before, so the partial sums swing back and forth inside a shrinking interval; the limit is always trapped between two consecutive partial sums, which differ by exactly the next term.

**Worked example.** $1-\frac12+\frac13-\frac14+\dots$ converges (to $\ln2$, as you will see next week) — although the same terms without the signs diverge. The signs make the difference.

**Worked example — error bound.** How many terms of $1-\frac13+\frac15-\frac17+\dots$ (which sums to $\frac\pi4$) are needed for an error below $0.001$? The error after $n$ terms is below the next term $\frac{1}{2n+1}$; we need $2n+1>1000$, so $n=500$ terms. (Slow! Next week you will find much faster series for $\pi$.)

### Experiment 3 — which converge?
**Predict first** for each column: converges or not, and to roughly what?
''')
B.code(r'''
N = [10, 100, 1000, 10**4, 10**5, 10**6]
rows = []
for n in N:
    k = np.arange(1, n + 1, dtype=float)
    rows.append([n, np.sum(1 / k), np.sum(1 / k**2), np.sum(1 / k**1.1), np.sum((-1) ** (k + 1) / k)])
table(['n', 'Σ 1/k', 'Σ 1/k²', 'Σ 1/k^1.1', 'Σ (−1)^(k+1)/k'], rows, fmt='%.6f')
print('\npi²/6 =', pi**2 / 6, '    ln 2 =', ln(2))
''')
B.ask(r'''By comparison with a $p$-series: does $\sum\dfrac{1}{n^2+5}$ converge? (a) yes (b) no''', 'choice', 'a',
      r'''Each term is below $\frac1{n^2}$, and $\sum\frac1{n^2}$ converges ($p=2>1$). So it converges.''',
      r'''Compare each term with $\frac{1}{n^2}$.''')
B.ask(r'''Ratio test for $\sum\dfrac{2^n}{n!}$: what is $L=\lim\left|\dfrac{a_{n+1}}{a_n}\right|$?''', 'num', 0,
      r'''$\dfrac{2^{n+1}/(n+1)!}{2^n/n!}=\dfrac{2}{n+1}\to0$. $L=0<1$: converges.''',
      r'''Divide the $(n+1)$-th term by the $n$-th; most factors cancel.''')
B.ask(r'''You stop $1-\frac14+\frac19-\frac1{16}+\dots$ (terms $\pm\frac1{n^2}$) after 9 terms. The error is at most which number?''', 'num', 0.01,
      r'''At most the first omitted term: $\frac{1}{10^2}=0.01$.''',
      r'''Alternating series: error ≤ first omitted term.''')
B.md(r'''
*Explain:* $\sum\frac1k$ keeps growing like $\ln n$. $\sum\frac1{k^2}$ settles at $1.6449=\frac{\pi^2}{6}$. $\sum\frac1{k^{1.1}}$ **converges** ($p>1$) — to about $10.58$ — but so slowly that a million terms are still far off: a table cannot tell it from divergence. The alternating column closes in on $\ln2$ with error about $\frac1{2n}$, as the bound promises.

## Week summary — everything on one page

- **Sequence limit** as for functions; $r^n\to0$ for $|r|<1$. Rising + bounded ⇒ converges (completeness). Hence $e=\lim(1+\frac1n)^n$ exists, and $e=\sum\frac1{k!}$.
- **Series**: $\sum a_k=\lim S_n$ (limit of partial sums).
- **Geometric**: $a+ar+ar^2+\dots=\dfrac{a}{1-r}$ for $|r|<1$; diverges otherwise.
- **Divergence test**: terms not → 0 ⇒ diverges. Terms → 0 proves nothing (harmonic series).
- **Comparison**; **integral test**; **$p$-series** $\sum\frac1{n^p}$ converges iff $p>1$.
- **Ratio test**: $\lim|a_{n+1}/a_n|<1$ converges, $>1$ diverges, $=1$ undecided.
- **Alternating series**: decreasing terms → 0 ⇒ converges; error ≤ first omitted term.
''')

# =====================================================================================
B.md(r'''
---
# Problems

Paper first. First attempt counts. `hint(n)` → `solution(n)` → `mistake(n, '...')`.

### Sequences
''')
B.problem(S1, r'$\displaystyle\lim_{n\to\infty}\frac{2n^2-n}{5n^2+3}$', 'num', 0.4,
          [r'Divide top and bottom by $n^2$.'],
          r'''$$\frac{2-\frac1n}{5+\frac3{n^2}}\to\frac25=0.4 .$$''')
B.problem(S1, r'$\displaystyle\lim_{n\to\infty}\left(1+\frac3n\right)^{n}$', 'num', math.exp(3),
          [r'Unit 1 week 3: $\left(1+\frac rn\right)^n\to e^r$.'],
          r'''$\left(1+\frac rn\right)^n\to e^r$ with $r=3$: **$e^3\approx20.09$**.''', fmt='a number; you can type `exp(3)`')
B.problem(S1, r'$a_1=2$ and $a_{n+1}=\dfrac12\left(a_n+\dfrac{5}{a_n}\right)$. The sequence converges (it is Newton’s method). To what?', 'num', math.sqrt(5),
          [r'Assume $a_n\to L$ and put $L$ on both sides.', r'$L=\frac12(L+\frac5L)$ gives $L^2=5$.'],
          r'''If $a_n\to L$: $L=\frac12\left(L+\frac5L\right)\Rightarrow2L=L+\frac5L\Rightarrow L^2=5$. The terms are positive: $L=\sqrt5\approx$ **2.236**.''', fmt='a number; you can type `sqrt(5)`')
B.md(r'''
### Geometric series
''')
B.problem(S2, r'$\displaystyle\sum_{k=0}^{\infty}3\left(\frac14\right)^k$', 'num', 4,
          [r'$a=3$, $r=\frac14$.'],
          r'''$$\frac{3}{1-\frac14}=\frac{3}{3/4}=4 .$$''')
B.problem(S2, r'$\displaystyle\sum_{k=1}^{\infty}\left(-\frac12\right)^k$', 'num', -1 / 3,
          [r'The first term (at $k=1$) is $-\frac12$; the ratio is $-\frac12$.'],
          r'''$$\frac{-1/2}{1-(-1/2)}=\frac{-1/2}{3/2}=-\frac13 .$$''', fmt='a number, e.g. `-1/3`')
B.problem(S2, r'Write $0.\overline{12}=0.121212\ldots$ as a fraction.', 'num', 12 / 99,
          [r'$a=\frac{12}{100}$, $r=\frac1{100}$.'],
          r'''$$\frac{12/100}{1-1/100}=\frac{12}{99}=\frac{4}{33}.$$''', fmt='a fraction, e.g. `4/33`')
B.problem(S2, r'A ball is dropped from 5 m and each bounce reaches $\frac23$ of the previous height. What total distance (m) does it travel?', 'num', 25,
          [r'Down 5 m, then up-and-down pairs: $2\cdot(\frac{10}{3}+\frac{20}{9}+\dots)$.', r'The pairs form a geometric series with $a=\frac{10}{3}$, $r=\frac23$.'],
          r'''Down 5. Then each bounce height counts twice: $2\cdot\left(\tfrac{10}{3}+\tfrac{20}{9}+\dots\right)=2\cdot\dfrac{10/3}{1-2/3}=2\cdot10=20$.

Total **25 m**.''', fmt='metres')
B.problem(S2, r'The series $\displaystyle\sum_{k=0}^\infty(2x)^k$ converges exactly for $|x|<c$. Find $c$.', 'num', 0.5,
          [r'A geometric series converges iff the ratio has size below 1. Here the ratio is $2x$.'],
          r'''Ratio $r=2x$; convergence iff $|2x|<1$, i.e. $|x|<\frac12$. So $x_{\max}=$ **1/2**, and for those $x$ the sum is $\dfrac{1}{1-2x}$.''')
B.md(r'''
### Divergence and comparison
''')
B.problem(S3, r'Which series diverges? (a) $\sum\frac1{n^2}$ (b) $\sum\frac{n}{2n+1}$ (c) $\sum\frac1{3^n}$', 'choice', 'b',
          [r'Check what the terms tend to.'],
          r'''(b): the terms $\frac{n}{2n+1}\to\frac12\ne0$, so by the divergence test it diverges. (a) is a $p$-series with $p=2$; (c) is geometric with $r=\frac13$; both converge.''')
B.problem(S3, r'The harmonic series: after $2^m$ terms the partial sum is more than $1+\frac m2$. Using this bound, how many terms suffice to be sure the partial sum exceeds 10? Give it as a power of two: the exponent $m$.', 'num', 18,
          [r'Need $1+\frac m2\ge10$.'],
          r'''$1+\frac m2\ge10\Rightarrow m\ge18$. So $2^{18}=262\,144$ terms certainly suffice (in fact about $12\,367$ are enough — the bound is generous).''', fmt='an integer')
B.problem(S3, r'Does $\sum\dfrac{1}{n^2+n}$ converge? Find its sum exactly, using $\dfrac{1}{n^2+n}=\dfrac1n-\dfrac1{n+1}$.', 'num', 1,
          [r'Write out $S_N$: the terms telescope.', r'$S_N=1-\frac1{N+1}$.'],
          r'''$$S_N=\left(1-\tfrac12\right)+\left(\tfrac12-\tfrac13\right)+\dots+\left(\tfrac1N-\tfrac1{N+1}\right)=1-\tfrac1{N+1}\to1 .$$
Converges, with sum **1**. (Also by comparison: $\frac1{n^2+n}<\frac1{n^2}$.)''')
B.md(r'''
### Convergence tests
''')
B.problem(S4, r'For which value of $p$ is $\sum\frac1{n^p}$ the borderline between convergence and divergence?', 'num', 1,
          [r'Same borderline as $\int_1^\infty x^{-p}dx$.'],
          r'''Converges for $p>1$, diverges for $p\le1$: borderline **p = 1** (the harmonic series, which diverges).''')
B.problem(S4, r'Ratio test for $\sum\dfrac{3^n}{n!}$: compute $L=\lim\left|\dfrac{a_{n+1}}{a_n}\right|$.', 'num', 0,
          [r'$\dfrac{3^{n+1}/(n+1)!}{3^n/n!}=\dfrac{3}{n+1}$.'],
          r'''$$\frac{a_{n+1}}{a_n}=\frac{3^{n+1}}{(n+1)!}\cdot\frac{n!}{3^n}=\frac{3}{n+1}\to0 .$$
$L=$ **0** $<1$: converges (to $e^3-1$, as next week shows).''')
B.problem(S4, r'Ratio test for $\sum\dfrac{n^2}{2^n}$: compute $L$.', 'num', 0.5,
          [r'$\dfrac{(n+1)^2}{2^{n+1}}\cdot\dfrac{2^n}{n^2}=\dfrac12\left(\dfrac{n+1}{n}\right)^2$.'],
          r'''$$\frac{a_{n+1}}{a_n}=\frac12\left(1+\frac1n\right)^2\to\frac12 .$$
$L=$ **1/2**: converges.''')
B.problem(S4, r'Using the alternating-series error bound: how many terms of $1-\frac12+\frac13-\frac14+\dots$ guarantee an error below $0.01$?', 'num', 99,
          [r'After $n$ terms the error is below $\frac1{n+1}$.'],
          r'''Need $\frac1{n+1}\le0.01$, i.e. $n+1\ge100$: **99 terms** (then the error is at most $\frac1{100}$).''', fmt='an integer')
B.problem(S4, r'Bound the sum of $\sum_{n=1}^{\infty}\frac1{n^3}$ with the integral test: give the upper bound $f(1)+\int_1^\infty f$.', 'num', 1.5,
          [r'$\int_1^\infty x^{-3}dx=\frac12$.'],
          r'''$\int_1^\infty\frac{dx}{x^3}=\frac12$, so $\frac12\le\sum\frac1{n^3}\le1+\frac12=$ **1.5**. (The true value is $1.2020\ldots$)''')
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
1. What does $\sum_{k=1}^\infty a_k$ mean, exactly?
2. Derive the geometric-series formula with the $S-rS$ trick.
3. Prove the harmonic series diverges.
4. Why does $0.999\ldots=1$?
5. Finish the sentence: "the integral test works because …" (draw the bars).

*Your answers:*

&nbsp;

### 3 · What comes next
**Week 2** turns series into a tool: a **power series** $c_0+c_1x+c_2x^2+\dots$ is an "infinite polynomial", and almost every function you know is one. You will build those series from derivatives (Taylor), find where they converge (the ratio test of §4.3), and use them to compute $e$, $\pi$ and $\sin x$ — and to see why the pendulum's period depends, very slightly, on how far it swings.
''')

if __name__ == '__main__':
    B.write()
