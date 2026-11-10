"""Unit 1 · Week 3 - Limits and continuity (built from first principles)."""
import math
from nbkit import Book
import figs_u01 as F

B = Book('u01w3', 'Unit 1 · Week 3 — Limits and continuity', 'year1/u01w3-limits-continuity.ipynb')
S1, S2, S3, S4 = '1 The idea of a limit', '2 Computing limits', '3 Special limits', '4 Continuity'

B.md(r'''
# Unit 1 · Week 3 — Limits and continuity
*Term 1, week 3 of 12 · about 15 hours in this notebook and on paper*

**Where you are.** You can now handle functions, radians and trigonometry. This week adds the one idea that separates calculus from algebra: the **limit**. It answers the question "what does this formula do *near* a point where I cannot simply evaluate it?" Derivatives (Unit 2), integrals (Unit 3) and series (Unit 4) are all *defined* as limits, so time spent here is repaid three times.

**What you will be able to do at the end of the week**
1. Explain what $\lim_{x\to a}f(x)=L$ means, and decide from a table, a graph or a formula whether a limit exists.
2. Compute limits of the form $\frac00$ by factoring, by the conjugate, and by combining fractions; compute limits as $x\to\infty$.
3. **Prove** $\lim_{x\to0}\frac{\sin x}{x}=1$ geometrically and derive $\lim_{x\to0}\frac{1-\cos x}{x^2}=\frac12$ from it.
4. Say what the number $e$ *is*.
5. Decide where a function is continuous, and use the intermediate value theorem to find a root by bisection — in code you write yourself.

**What is used from earlier weeks:** factoring and expanding; the sector area $\frac12r^2\theta$ and $\tan\theta$ on the unit circle (week 1); $\sin^2x+\cos^2x=1$ (week 1); nothing else.

Run the grey *SETUP* cell first. Tools as before: `ask`, `check`, `hint`, `solution`, `mistake`, `report`.
''')

# =====================================================================================
B.md(r'''
---
# Part 1 — The idea of a limit

## 1.1 The problem that forces the idea: speed at one instant

**Why.** A speedometer shows a speed *at this instant*. But speed is distance divided by time, and in an instant no time passes and no distance is covered: $\frac{0}{0}$. The whole of calculus grew out of making sense of that.

**Build.** A ball is dropped. After $t$ seconds it has fallen
$$s(t)=5t^2\ \text{metres}$$
(this is $\frac12gt^2$ with $g\approx10\ \text{m/s}^2$ to keep the numbers round). **How fast is it moving at exactly $t=1$?**

**Step 1 — what we can compute: an average speed.** Between $t=1$ and a slightly later time $t=1+h$, the ball covers $s(1+h)-s(1)$ metres in $h$ seconds:
$$\text{average speed}=\frac{s(1+h)-s(1)}{h}=\frac{5(1+h)^2-5}{h}.$$

**Step 2 — shrink the interval.** The shorter the interval, the less the speed can change during it, so the better the average describes the instant $t=1$. Compute it for smaller and smaller $h$:

| $h$ (s) | $1$ | $0.5$ | $0.1$ | $0.01$ | $0.001$ |
|---|---|---|---|---|---|
| average speed (m/s) | $15$ | $12.5$ | $10.5$ | $10.05$ | $10.005$ |

The numbers settle towards **10**.
''')
B.fig('secant_speed', F.secant_speed, 'Each average speed is the slope of a straight line through two points of the graph. As h shrinks, the slopes settle down.')
B.md(r'''
**Step 3 — we cannot simply put $h=0$.** That gives $\dfrac{5\cdot1-5}{0}=\dfrac00$, which has no meaning.

**Step 4 — but algebra shows what is going on.** Simplify the average speed for $h\ne0$:
$$\begin{aligned}
\frac{5(1+h)^2-5}{h}&=\frac{5(1+2h+h^2)-5}{h} &&\text{(expand the square)}\\
&=\frac{10h+5h^2}{h} &&\text{(the 5's cancel)}\\
&=10+5h &&\text{(divide by $h$ — allowed because $h\ne0$)}
\end{aligned}$$
So the average speed is exactly $10+5h$ (check with the table: $h=0.1$ gives $10.5$ ✓). As $h$ shrinks, $5h$ shrinks to nothing, and the average speed gets as close to $10$ as we please.

**Step 5 — name it.** We say: *the limit of the average speed, as $h$ tends to $0$, is $10$*, and write
$$\lim_{h\to0}\frac{s(1+h)-s(1)}{h}=10 .$$
The **instantaneous speed is defined to be this limit**: 10 m/s. We never divided by zero; we asked what the expression *approaches*.

That is the pattern of all of calculus: *a quantity we want (speed at an instant) is unreachable directly, but is approached by quantities we can compute (average speeds)*.

## 1.2 What "limit" means

**Definition (in words).**
$$\lim_{x\to a}f(x)=L$$
means: **the values $f(x)$ can be made as close to $L$ as we like, by taking $x$ close enough to $a$ — but not equal to $a$.**

Read it as "the limit of $f(x)$, as $x$ tends to $a$, is $L$". Three points in the definition matter:

1. **"not equal to $a$"** — the limit ignores what happens *at* $a$. The function need not even be defined there (as with $h=0$ above). The limit is about the neighbourhood.
2. **"as close as we like"** — not merely "close". If you ask for $f(x)$ within $0.001$ of $L$, there must be a range of $x$ around $a$ that achieves it; and the same for $0.000001$, and for any tolerance whatever.
3. **from both sides** — $x$ may approach $a$ from below or from above, and $f(x)$ must head to the same $L$ either way.

**Worked example.** $f(x)=\dfrac{x^2-9}{x-3}$ near $x=3$.

At $x=3$ itself: $\frac{0}{0}$, undefined. Near $3$:

| $x$ | $2.9$ | $2.99$ | $2.999$ | $3$ | $3.001$ | $3.01$ | $3.1$ |
|---|---|---|---|---|---|---|---|
| $f(x)$ | $5.9$ | $5.99$ | $5.999$ | — | $6.001$ | $6.01$ | $6.1$ |

From both sides the values head for $6$. So $\lim_{x\to3}f(x)=6$, even though $f(3)$ does not exist.
''')
B.fig('hole', F.hole, 'The graph is a straight line with one point missing. The limit is the height the graph heads for.')
B.md(r'''
### Experiment 1 — approach a point from both sides
`approach(f, a)` prints $f(x)$ for $x$ closing in on $a$ from the left and from the right.

**Predict first** what each of these does near the given point (a number? no limit?), then run:
(1) $\dfrac{x^2-9}{x-3}$ at $3$ (2) $\dfrac{\sin x}{x}$ at $0$ (3) $\dfrac{|x|}{x}$ at $0$ (4) $\dfrac{1}{x^2}$ at $0$.
''')
B.code(r'''
def approach(f, a, steps=6):
    rows = []
    for k in range(1, steps + 1):
        d = 10.0 ** (-k)                       # 0.1, 0.01, 0.001, ...
        rows.append([a - d, f(a - d), a + d, f(a + d)])
    table(['x (from the left)', 'f(x)', 'x (from the right)', 'f(x) '], rows, fmt='%.9g')

print('(1)'); approach(lambda v: (v**2 - 9) / (v - 3), 3)
print('\n(2)'); approach(lambda v: sin(v) / v, 0)
print('\n(3)'); approach(lambda v: abs(v) / v, 0)
print('\n(4)'); approach(lambda v: 1 / v**2, 0)
''')
B.md(r'''
*Explain:* (1) heads for 6. (2) heads for 1 — you will prove that in Part 3. (3) is $-1$ on the left and $+1$ on the right: the two sides disagree, so there is **no limit**. (4) grows without bound: no (finite) limit.
''')
B.ask(r'''From this table, what is $\lim_{x\to2}g(x)$?

| $x$ | 1.9 | 1.99 | 1.999 | 2.001 | 2.01 | 2.1 |
|---|---|---|---|---|---|---|
| $g(x)$ | 3.61 | 3.9601 | 3.996 | 4.004 | 4.0401 | 4.41 |''', 'num', 4,
      r'''From both sides the values close in on $4$. (The function is in fact $x^2$.) Note that the table does not tell you $g(2)$ — and the limit does not need it.''',
      r'''Which number do the values approach as $x$ gets close to 2 from the left *and* from the right?''')

B.md(r'''
## 1.3 One-sided limits

**Build.** Sometimes you want to look from one side only.

- $\displaystyle\lim_{x\to a^-}f(x)$: the **left-hand limit**; $x$ approaches $a$ through values *smaller* than $a$.
- $\displaystyle\lim_{x\to a^+}f(x)$: the **right-hand limit**; $x$ approaches through values *larger* than $a$.

**The connection:** the (two-sided) limit exists **exactly when** both one-sided limits exist **and are equal**.

**Worked example.** $f(x)=\dfrac{|x|}{x}$ at $0$. Recall $|x|=x$ if $x>0$ and $|x|=-x$ if $x<0$.
- For $x>0$: $f(x)=\dfrac{x}{x}=1$. So $\lim_{x\to0^+}f(x)=1$.
- For $x<0$: $f(x)=\dfrac{-x}{x}=-1$. So $\lim_{x\to0^-}f(x)=-1$.
- $1\ne-1$: $\;\lim_{x\to0}f(x)$ **does not exist**.

**Worked example — a function defined in pieces.**
$$f(x)=\begin{cases}x+1 & x<2\\ x^2 & x\ge2\end{cases}$$
- From the left use the first rule: $\lim_{x\to2^-}(x+1)=3$.
- From the right use the second rule: $\lim_{x\to2^+}x^2=4$.
- They differ: no limit at $2$. The graph jumps from height 3 to height 4.

## 1.4 The three ways a limit can fail to exist
''')
B.fig('limit_fail', F.limit_fail, 'Jump, blow-up, oscillation.')
B.md(r'''
1. **Jump:** the left and right limits both exist but differ.
2. **Blow-up:** the values grow without bound. We then write $\lim_{x\to0}\frac{1}{x^2}=\infty$. *Careful:* this notation does **not** say the limit exists — $\infty$ is not a number. It is shorthand for "the limit fails to exist in this particular way: $f(x)$ becomes larger than any number you name".
3. **Oscillation:** $\sin\frac1x$ near $0$. As $x\to0$, $\frac1x$ runs through infinitely many full turns, so the sine keeps sweeping between $-1$ and $1$ however close you get. It settles on nothing.
''')
B.ask(r'''Let $f(x)=\begin{cases}2x+1 & x<1\\ 5-x & x\ge1\end{cases}$. What is the **left-hand** limit $\lim_{x\to1^-}f(x)$?''', 'num', 3,
      r'''From the left, $x<1$, so the first rule applies: $2x+1\to2\cdot1+1=3$. (From the right: $5-1=4$. They differ, so the two-sided limit does not exist.)''',
      r'''Approaching from the left means $x<1$. Which of the two rules applies there?''')

# =====================================================================================
B.md(r'''
---
# Part 2 — Computing limits

## 2.1 The limit laws, and when you may simply substitute

**Why.** Tables only *suggest* a limit. To be sure — and to be quick — we need rules.

**The laws.** Suppose $\lim_{x\to a}f(x)=L$ and $\lim_{x\to a}g(x)=M$ (both exist). Then:

| | law | in words |
|---|---|---|
| sum | $\lim\,(f+g)=L+M$ | the limit of a sum is the sum of the limits |
| constant | $\lim\,(c\,f)=c\,L$ | constants come out |
| product | $\lim\,(f\cdot g)=L\cdot M$ | the limit of a product is the product of the limits |
| quotient | $\lim\,\dfrac fg=\dfrac LM$ **if $M\ne0$** | …of a quotient, the quotient — unless the bottom tends to 0 |
| root | $\lim\sqrt{f}=\sqrt{L}$ (if $L>0$) | |

**Why they are true (the idea).** Take the sum law. Near $a$, $f(x)$ is within some tiny error of $L$, and $g(x)$ within some tiny error of $M$. Then $f(x)+g(x)$ is within the *sum* of the two errors of $L+M$. Since each error can be made as small as we like, so can their sum. The other laws are the same kind of argument. (Part 5 shows how such arguments are made fully rigorous.)

**Two obvious starting points:** $\lim_{x\to a}x=a$ and $\lim_{x\to a}c=c$.

**Consequence: for a polynomial you may substitute.** Build the limit up with the laws:
$$\lim_{x\to2}(3x^2-x+1)=3\cdot\Big(\lim_{x\to2}x\Big)^2-\lim_{x\to2}x+1=3\cdot2^2-2+1=11 .$$
That is the same as putting $x=2$ into the formula. The same holds for a quotient of polynomials, **provided the denominator is not zero at that point** (quotient law).

**The same is true for all the standard functions** — $\sqrt{\ }$, $\sin$, $\cos$, $\tan$, $e^x$, $\ln$ — at every point where they are defined: their graphs have no breaks, so the value they approach is the value they have. (Part 4 gives this property its name: *continuity*.)

> **Rule 1. Try substituting first.** If you get a number, that number is the limit. Only if substitution fails (division by zero) is there work to do.

**Worked examples.**
$\displaystyle\lim_{x\to3}\frac{x^2+1}{x-1}=\frac{10}{2}=5$. $\qquad\displaystyle\lim_{x\to0}\cos x=\cos0=1$. $\qquad\displaystyle\lim_{x\to4}\sqrt{2x+1}=\sqrt9=3$.
''')
B.ask(r'''Compute $\displaystyle\lim_{x\to-1}\frac{x^2+3}{x+2}$.''', 'num', 4,
      r'''Substitute: $\dfrac{(-1)^2+3}{-1+2}=\dfrac{4}{1}=4$. The denominator is not zero, so substitution is allowed.''',
      r'''Rule 1: put $x=-1$ in. Is the denominator non-zero?''')

B.md(r'''
## 2.2 The form $\frac00$

**Build.**

**What $\frac00$ means.** If substitution gives $\frac00$, top and bottom both tend to zero, and the limit is decided by *which one gets there faster*. Anything can happen:
$$\lim_{x\to0}\frac{2x}{x}=2,\qquad\lim_{x\to0}\frac{x^2}{x}=0,\qquad\lim_{x\to0}\frac{x}{x^3}=\infty .$$
All three are "$\frac00$". So $\frac00$ is **not** an answer. It does not mean "0", or "1", or "no limit". It means: **rewrite the expression until the troublesome factor cancels.** It is called an *indeterminate form*.

There are four standard ways to rewrite.

### Technique A — factor and cancel
**Worked example.** $\displaystyle\lim_{x\to3}\frac{x^2-9}{x-3}$. Substitution: $\frac00$.
$$\begin{aligned}
\frac{x^2-9}{x-3}&=\frac{(x-3)(x+3)}{x-3} &&\text{(difference of squares)}\\
&=x+3 &&\text{(cancel $x-3$: allowed because $x\ne3$)}
\end{aligned}$$
**Why may we cancel?** Cancelling divides top and bottom by $x-3$, which is only forbidden when $x-3=0$. But a limit as $x\to3$ never uses $x=3$ itself (point 1 of the definition). For all the $x$ that matter, the two expressions are equal, so they have the same limit:
$$\lim_{x\to3}\frac{x^2-9}{x-3}=\lim_{x\to3}(x+3)=6 .$$

**Why does this always work for polynomials?** If a polynomial is zero at $x=a$, then $(x-a)$ is one of its factors. So if top and bottom are both zero at $a$, both contain the factor $(x-a)$, and it cancels.

**Worked example.** $\displaystyle\lim_{x\to-2}\frac{x^2-x-6}{x^2-4}$. Substitution: $\frac{4+2-6}{4-4}=\frac00$. Both must contain the factor $(x+2)$:
$$\frac{x^2-x-6}{x^2-4}=\frac{(x+2)(x-3)}{(x+2)(x-2)}=\frac{x-3}{x-2}\ \xrightarrow[x\to-2]{}\ \frac{-5}{-4}=\frac54 .$$
(To factor $x^2-x-6$: you need two numbers with product $-6$ and sum $-1$: $2$ and $-3$.)

### Technique B — multiply by the conjugate (for square roots)
**Worked example.** $\displaystyle\lim_{x\to0}\frac{\sqrt{x+4}-2}{x}$. Substitution: $\frac{2-2}{0}=\frac00$. There is nothing to factor — the root is in the way.

**The idea.** $(p-q)(p+q)=p^2-q^2$: multiplying a difference by the matching sum **squares both terms**, and squaring removes a root. The matching sum $\sqrt{x+4}+2$ is called the **conjugate**. Multiply top *and* bottom by it (that is multiplying by 1, so nothing changes):
$$\begin{aligned}
\frac{\sqrt{x+4}-2}{x}\cdot\frac{\sqrt{x+4}+2}{\sqrt{x+4}+2}&=\frac{(\sqrt{x+4})^2-2^2}{x\,(\sqrt{x+4}+2)} &&\text{(top: $(p-q)(p+q)=p^2-q^2$)}\\
&=\frac{x+4-4}{x\,(\sqrt{x+4}+2)}=\frac{x}{x\,(\sqrt{x+4}+2)}\\
&=\frac{1}{\sqrt{x+4}+2} &&\text{(cancel $x$, since $x\ne0$)}
\end{aligned}$$
Now substitution works: $\dfrac{1}{\sqrt4+2}=\dfrac14$.

*Do not multiply out the bottom.* Leave it factored; the whole point is to cancel the $x$.

### Technique C — combine the fractions
**Worked example.** $\displaystyle\lim_{x\to2}\frac{\frac1x-\frac12}{x-2}$. Substitution: $\frac00$. Put the top over a common denominator:
$$\frac1x-\frac12=\frac{2-x}{2x}\qquad\Rightarrow\qquad\frac{\frac{2-x}{2x}}{x-2}=\frac{2-x}{2x\,(x-2)}=\frac{-(x-2)}{2x\,(x-2)}=\frac{-1}{2x}\ \xrightarrow[x\to2]{}\ -\frac14 .$$
(The step $2-x=-(x-2)$ is what makes the cancellation visible.)

### Technique D — expand
**Worked example.** $\displaystyle\lim_{h\to0}\frac{(2+h)^2-4}{h}$. Expand the square:
$$\frac{4+4h+h^2-4}{h}=\frac{4h+h^2}{h}=4+h\ \xrightarrow[h\to0]{}\ 4 .$$
This is the "speed" calculation of §1.1 again, for $f(x)=x^2$ at $x=2$. In Unit 2 you will do exactly this, once, for a general $x$ — and call the result the derivative.

> **Rule 2.** $\frac00$ → factor, or conjugate, or common denominator, or expand; cancel; then substitute.
''')
B.ask(r'''Compute $\displaystyle\lim_{x\to4}\frac{x^2-16}{x-4}$.''', 'num', 8,
      r'''$\dfrac{(x-4)(x+4)}{x-4}=x+4\to8$.''',
      r'''Substitution gives $\frac00$. Factor the top as a difference of squares and cancel.''')
B.ask(r'''Compute $\displaystyle\lim_{x\to0}\frac{\sqrt{x+1}-1}{x}$.''', 'num', 0.5,
      r'''Multiply top and bottom by $\sqrt{x+1}+1$: the top becomes $(x+1)-1=x$, so the fraction is $\dfrac{x}{x(\sqrt{x+1}+1)}=\dfrac{1}{\sqrt{x+1}+1}\to\dfrac12$.''',
      r'''Multiply top and bottom by the conjugate $\sqrt{x+1}+1$. What does the top become?''')

B.md(r'''
## 2.3 Limits as $x\to\infty$

**Why.** "What happens in the long run?" — the final temperature, the terminal velocity, the steady-state current. Mathematically: what does $f(x)$ approach as $x$ grows without bound?

**Build.**

**Step 1 — meaning.** $\lim_{x\to\infty}f(x)=L$ means: $f(x)$ can be made as close to $L$ as we like by taking $x$ *large enough*. On a graph, the curve flattens out towards the horizontal line $y=L$, called a **horizontal asymptote**.

**Step 2 — the one basic fact.**
$$\lim_{x\to\infty}\frac1x=0 .$$
*Why:* want $\frac1x$ smaller than $0.001$? Take $x>1000$. Smaller than $0.000001$? Take $x>1\,000\,000$. Whatever tolerance you name, a large enough $x$ meets it. By the product law, also $\frac{1}{x^2}=\frac1x\cdot\frac1x\to0$, and likewise $\frac{c}{x^n}\to0$ for any constant $c$ and any power $n>0$.

**Step 3 — the technique for fractions: divide top and bottom by the highest power of $x$ in the denominator.** This turns every term into either a constant or something that tends to $0$.

**Worked example 1.** $\displaystyle\lim_{x\to\infty}\frac{3x^2+2x}{5x^2-1}$. Substituting "$\infty$" gives $\frac\infty\infty$, another indeterminate form. Divide top and bottom by $x^2$:
$$\frac{3x^2+2x}{5x^2-1}=\frac{3+\frac2x}{5-\frac{1}{x^2}}\ \xrightarrow[x\to\infty]{}\ \frac{3+0}{5-0}=\frac35 .$$

**Worked example 2.** $\displaystyle\lim_{x\to\infty}\frac{4x+1}{x^2+3}$. Divide by $x^2$: $\;\dfrac{\frac4x+\frac{1}{x^2}}{1+\frac{3}{x^2}}\to\dfrac{0}{1}=0$.

**Worked example 3.** $\displaystyle\lim_{x\to\infty}\frac{x^2+1}{2x+5}$. Divide by $x$: $\;\dfrac{x+\frac1x}{2+\frac5x}$. The bottom tends to $2$ but the top grows without bound: the limit is $\infty$ (no finite limit).

**The pattern** (now you know *why*): for a quotient of polynomials as $x\to\infty$, only the highest powers matter.

| degrees | limit |
|---|---|
| top $<$ bottom | $0$ |
| top $=$ bottom | ratio of the leading coefficients |
| top $>$ bottom | $\pm\infty$ |

**Worked example 4 — a root: the conjugate again.** $\displaystyle\lim_{x\to\infty}\left(\sqrt{x^2+x}-x\right)$. This is "$\infty-\infty$" — also indeterminate. Multiply and divide by the conjugate:
$$\begin{aligned}
\sqrt{x^2+x}-x&=\frac{(\sqrt{x^2+x}-x)(\sqrt{x^2+x}+x)}{\sqrt{x^2+x}+x}=\frac{x^2+x-x^2}{\sqrt{x^2+x}+x}=\frac{x}{\sqrt{x^2+x}+x}\\[4pt]
&=\frac{1}{\sqrt{1+\frac1x}+1} &&\text{(divide top and bottom by $x$; for $x>0$, $\tfrac{\sqrt{x^2+x}}{x}=\sqrt{\tfrac{x^2+x}{x^2}}=\sqrt{1+\tfrac1x}$)}\\
&\xrightarrow[x\to\infty]{}\frac{1}{\sqrt{1}+1}=\frac12 .
\end{aligned}$$
Surprising but true: $\sqrt{x^2+x}$ exceeds $x$ by almost exactly $\frac12$ for large $x$. (Try $x=100$: $\sqrt{10100}=100.4988$.)
''')
B.fig('rational_inf', F.rational_inf, 'A horizontal asymptote (behaviour as x → ±∞) and two vertical asymptotes (blow-up at a point).')
B.md(r'''
## 2.4 Infinite limits and vertical asymptotes

**Build.** What if substitution gives $\dfrac{\text{non-zero number}}{0}$? Then the top stays away from zero while the bottom shrinks to zero: the fraction grows without bound. The graph has a **vertical asymptote**. The only question is the **sign**, and it may differ on the two sides.

**Worked example.** $\dfrac{1}{x-2}$ as $x\to2$.
- From the right, $x$ slightly bigger than 2: $x-2$ is a tiny **positive** number, so $\frac{1}{x-2}$ is huge and positive: $\lim_{x\to2^+}=+\infty$.
- From the left: $x-2$ is tiny and **negative**: $\lim_{x\to2^-}=-\infty$.

**Hole or asymptote?** Both come from a zero of the denominator. The difference is whether the factor cancels.

**Worked example.** $f(x)=\dfrac{x+1}{(x-2)(x+1)(x+3)}$. The denominator is zero at $x=2$, $x=-1$ and $x=-3$.
- The factor $(x+1)$ cancels with the top: for $x\ne-1$, $f(x)=\dfrac{1}{(x-2)(x+3)}$. At $x=-1$ this is $\frac{1}{(-3)(2)}=-\frac16$: a finite limit. So $x=-1$ is a **hole**, not an asymptote.
- At $x=2$ and $x=-3$ nothing cancels: $\frac{\text{non-zero}}{0}$. **Two vertical asymptotes.**

> **Rule 3.** Cancel common factors first. The zeros of the denominator that **remain** are the vertical asymptotes; the ones that cancelled are holes.

**Summary of Part 2.**

| substitution gives | meaning | do this |
|---|---|---|
| a number | that is the limit | done |
| $\frac00$ | indeterminate | factor / conjugate / common denominator / expand, cancel, substitute again |
| $\frac{\text{non-zero}}{0}$ | blow-up | $\pm\infty$; find the sign on each side |
| $\frac\infty\infty$ | indeterminate | divide by the highest power |
| $\infty-\infty$ | indeterminate | conjugate, or combine into one fraction |
''')
B.ask(r'''Compute $\displaystyle\lim_{x\to\infty}\frac{6x^3-x}{2x^3+5x^2}$.''', 'num', 3,
      r'''Divide top and bottom by $x^3$: $\dfrac{6-\frac{1}{x^2}}{2+\frac5x}\to\dfrac62=3$. Equal degrees: ratio of the leading coefficients.''',
      r'''Divide top and bottom by $x^3$, then let every term with $x$ in a denominator go to 0.''')
B.ask(r'''How many **vertical asymptotes** does $f(x)=\dfrac{x-1}{x^2-1}$ have?''', 'num', 1,
      r'''$x^2-1=(x-1)(x+1)$. The factor $(x-1)$ cancels (a hole at $x=1$, where the limit is $\frac12$). Only $x=-1$ remains: one vertical asymptote.''',
      r'''Factor the denominator. Does anything cancel with the numerator?''', fmt='an integer')

# =====================================================================================
B.md(r'''
---
# Part 3 — The special limits

Techniques A–D are algebra. They do nothing for $\dfrac{\sin x}{x}$: there is nothing to factor. This limit needs geometry — and one new tool.

## 3.1 The squeeze theorem

**Theorem.** Suppose that near $a$ (but not necessarily at $a$)
$$g(x)\le f(x)\le h(x),$$
and that $g$ and $h$ have the **same** limit $L$ as $x\to a$. Then $f$ has that limit too: $\lim_{x\to a}f(x)=L$.

**Why.** $f$ is trapped between two functions that both close in on $L$. It has nowhere else to go.

**Worked example.** $\displaystyle\lim_{x\to0}x^2\sin\frac1x$. The factor $\sin\frac1x$ oscillates wildly (§1.4), but it always stays between $-1$ and $1$:
$$-1\le\sin\frac1x\le1\qquad\Rightarrow\qquad-x^2\le x^2\sin\frac1x\le x^2\quad\text{(multiply by $x^2\ge0$)}.$$
Both $-x^2$ and $x^2$ tend to $0$. So the squeezed function tends to $0$: the oscillation is crushed.

## 3.2 The most important limit in the course: $\dfrac{\sin x}{x}\to1$

**Theorem.** $\displaystyle\lim_{x\to0}\frac{\sin x}{x}=1$ ($x$ in radians).

Experiment 1 made this believable. In week 1 (§3.11) the picture made it plausible: for a small angle, the height $\sin x$ and the arc $x$ nearly coincide. Now the proof.

**Proof.** Take an angle $x$ with $0<x<\frac\pi2$ on the unit circle. Let $A=(1,0)$, let $P$ be the point at angle $x$, and let $T$ be the point where the extended radius meets the tangent line at $A$.
''')
B.fig('squeeze', F.squeeze, 'Three regions, each containing the one before: triangle OAP, sector OAP, triangle OAT.')
B.md(r'''
**Step 1 — three areas.**

- **Triangle $OAP$** (red): base $OA=1$; its height is the height of $P$, which is $\sin x$. Area $=\frac12\cdot1\cdot\sin x=\frac12\sin x$.
- **Sector $OAP$** (blue, the pie slice): radius 1, angle $x$. By week 1, §2.5: area $=\frac12r^2\theta=\frac12x$. *(This is the step that needs radians.)*
- **Triangle $OAT$** (purple): base $OA=1$; its height is $AT=\tan x$ (week 1, §3.8). Area $=\frac12\tan x$.

**Step 2 — compare.** The red triangle lies inside the sector, and the sector lies inside the purple triangle. A region inside another has the smaller area:
$$\tfrac12\sin x\ \le\ \tfrac12x\ \le\ \tfrac12\tan x .$$

**Step 3 — tidy up.** Multiply by 2:
$$\sin x\le x\le\tan x .$$
Divide all three by $\sin x$, which is positive for $0<x<\frac\pi2$ (so the inequalities keep their direction), and use $\tan x=\frac{\sin x}{\cos x}$:
$$1\le\frac{x}{\sin x}\le\frac{1}{\cos x}.$$
Take reciprocals. For positive numbers, taking reciprocals **reverses** inequalities (from $2\le3$ we get $\frac12\ge\frac13$):
$$1\ \ge\ \frac{\sin x}{x}\ \ge\ \cos x .$$

**Step 4 — squeeze.** As $x\to0^+$: the left side is the constant $1$, and the right side $\cos x\to\cos0=1$. The function $\frac{\sin x}{x}$ is trapped between two things that tend to $1$:
$$\lim_{x\to0^+}\frac{\sin x}{x}=1 .$$

**Step 5 — the other side.** For negative $x$, write $x=-u$ with $u>0$: $\;\dfrac{\sin(-u)}{-u}=\dfrac{-\sin u}{-u}=\dfrac{\sin u}{u}$ (sine is odd). So the function has the same values on the left as on the right — it is even — and the left-hand limit is also $1$. Both sides agree: the limit is $1$. $\blacksquare$

**What you have also proved along the way:** $\;\sin x<x<\tan x$ for $0<x<\frac\pi2$ — the precise form of "sin, arc and tan nearly coincide".

**Why radians.** In Step 1 the sector area was $\frac12x$ only because $x$ was in radians. With degrees the area is $\frac12\cdot\frac{\pi}{180}x$ and the limit comes out as $\frac{\pi}{180}\approx0.01745$, not 1. Every calculus formula for sine and cosine depends on this limit being 1 — which is why calculus uses radians.

## 3.3 What follows from it

**Build.** Each of these is $\frac{\sin x}{x}\to1$ in disguise. The skill is to *make the disguise fit*.

**(a) $\displaystyle\lim_{x\to0}\frac{\sin kx}{x}=k$.** The limit $\frac{\sin u}{u}\to1$ needs the **same thing** inside the sine and underneath. Inside is $kx$; so we want $kx$ underneath. Multiply and divide by $k$:
$$\frac{\sin kx}{x}=k\cdot\frac{\sin kx}{kx}.$$
Let $u=kx$. As $x\to0$, also $u\to0$, so $\dfrac{\sin u}{u}\to1$, and the whole thing tends to $k\cdot1=k$.
Example: $\displaystyle\lim_{x\to0}\frac{\sin3x}{x}=3$ (from your diagnostic).

**(b) A quotient of sines.** $\displaystyle\lim_{x\to0}\frac{\sin5x}{\sin2x}$. Give each sine its own partner:
$$\frac{\sin5x}{\sin2x}=\frac{\sin5x}{5x}\cdot\frac{2x}{\sin2x}\cdot\frac{5x}{2x}\ \to\ 1\cdot1\cdot\frac52=\frac52 .$$
(If $\frac{\sin u}{u}\to1$ then its reciprocal $\frac{u}{\sin u}\to\frac11=1$ too, by the quotient law.)

**(c) $\displaystyle\lim_{x\to0}\frac{\tan x}{x}=1$.** $\;\dfrac{\tan x}{x}=\dfrac{\sin x}{x}\cdot\dfrac{1}{\cos x}\to1\cdot\dfrac11=1$.

**(d) $\displaystyle\lim_{x\to0}\frac{1-\cos x}{x^2}=\frac12$.** Substitution gives $\frac00$. Use the conjugate idea — multiply by $1+\cos x$ to produce $1-\cos^2x=\sin^2x$:
$$\begin{aligned}
\frac{1-\cos x}{x^2}\cdot\frac{1+\cos x}{1+\cos x}&=\frac{1-\cos^2x}{x^2\,(1+\cos x)}\\
&=\frac{\sin^2x}{x^2\,(1+\cos x)} &&\text{($\sin^2x+\cos^2x=1$)}\\
&=\left(\frac{\sin x}{x}\right)^2\cdot\frac{1}{1+\cos x}\\
&\xrightarrow[x\to0]{}\ 1^2\cdot\frac{1}{1+1}=\frac12 .
\end{aligned}$$
This is the precise form of $\cos x\approx1-\frac{x^2}{2}$ (week 1, §3.11): rearranged, $1-\cos x\approx\frac12x^2$.

**(e) $\displaystyle\lim_{x\to0}\frac{1-\cos x}{x}=0$.** Write it as $x\cdot\dfrac{1-\cos x}{x^2}\to0\cdot\dfrac12=0$.

**Keep (a)–(e) in mind:** $\frac{\sin h}{h}\to1$ and $\frac{1-\cos h}{h}\to0$ are *exactly* the two facts needed to differentiate $\sin x$ in Unit 2.
''')
B.ask(r'''Compute $\displaystyle\lim_{x\to0}\frac{\sin7x}{x}$.''', 'num', 7,
      r'''$\dfrac{\sin7x}{x}=7\cdot\dfrac{\sin7x}{7x}\to7\cdot1=7$.''',
      r'''Make the denominator match the inside of the sine: multiply and divide by 7.''')
B.ask(r'''Compute $\displaystyle\lim_{x\to0}\frac{\sin4x}{\sin6x}$.''', 'num', 2 / 3,
      r'''$\dfrac{\sin4x}{4x}\cdot\dfrac{6x}{\sin6x}\cdot\dfrac{4x}{6x}\to1\cdot1\cdot\dfrac46=\dfrac23$.''',
      r'''Pair $\sin4x$ with $4x$ and $\sin6x$ with $6x$; what factor is left over?''', fmt='a number, e.g. `3/4`')

B.md(r'''
## 3.4 The number $e$

**Why.** You have used $e\approx2.718$ and $\ln$ for years. Where does this strange number come from? From a limit — and a banking question.

**Build.**

**Step 1 — compound interest.** A bank pays 100 % interest per year on €1.
- Paid **once**, at the end: you have $1+1=2$.
- Paid in **two halves** (50 % after six months, 50 % of the new balance after twelve): $\left(1+\frac12\right)\left(1+\frac12\right)=\left(1+\frac12\right)^2=2.25$. Better, because the first interest earns interest.
- Paid in **$n$ instalments** of $\frac1n$ each: every instalment multiplies the balance by $\left(1+\frac1n\right)$, so after a year you have
$$\left(1+\frac1n\right)^n .$$

**Step 2 — compound ever more often.** Does the balance grow without bound as $n\to\infty$? Two effects compete: more multiplications ($n$ grows) by a factor ever closer to 1 ($\frac1n$ shrinks). Run the next cell to see which wins.
''')
B.code(r'''
rows = [[k, (1 + 1 / k) ** k] for k in [1, 2, 4, 12, 52, 365, 8760, 10**6, 10**8]]
table(['n (times per year)', '(1 + 1/n)^n'], rows, fmt='%.10f')
print('\ne =', e)
''')
B.md(r'''
**Step 3 — the definition.** The values increase, but more and more slowly, and they never pass a certain number. That number is called $e$:
$$\boxed{e=\lim_{n\to\infty}\left(1+\frac1n\right)^n\approx2.718281828\ldots}$$
*(Honesty note: the table is evidence, not proof. That the sequence really does increase and stay below 3 — and therefore has a limit — is proved with the binomial theorem in Unit 4.)*

**Step 4 — other interest rates give $e^r$.** With rate $r$ instead of 100 %, the balance after $n$ instalments is $\left(1+\frac rn\right)^n$. Substitute $n=rm$ (so $\frac rn=\frac1m$, and $m\to\infty$ when $n\to\infty$):
$$\left(1+\frac rn\right)^n=\left(1+\frac1m\right)^{rm}=\left[\left(1+\frac1m\right)^m\right]^r\ \longrightarrow\ e^r .$$
So **continuous compounding at rate $r$ multiplies your money by $e^r$ per year**. That is why $e^{rt}$ describes everything that grows (or, with $r<0$, decays) in proportion to its own size: populations, radioactive decay, a capacitor discharging.

**Step 5 — the property that makes $e$ special (a preview).** For large $n$, $e\approx\left(1+\frac1n\right)^n$. Write $h=\frac1n$, a small number: $e\approx(1+h)^{1/h}$. Raise both sides to the power $h$:
$$e^h\approx1+h\qquad\Rightarrow\qquad\frac{e^h-1}{h}\approx1 .$$
This suggests
$$\lim_{h\to0}\frac{e^h-1}{h}=1 ,$$
which is true (the argument above is a sketch; the proof comes with the derivative of $e^x$ in Unit 2). It says the graph of $e^x$ crosses the $y$-axis with slope exactly 1 — the reason $e$ is the *natural* base. For any other base the limit is a different number: for base 2 it is $0.693\ldots=\ln2$.

### Experiment 2 — a table can lie
The cell evaluates three expressions for smaller and smaller $h$. You know the true limits: $1$, $\frac12$ and $1$.

**Predict first:** will the numbers keep getting better as $h$ gets smaller?
''')
B.code(r'''
rows = []
for k in [1, 2, 3, 4, 6, 8, 10, 12]:
    hh = 10.0 ** (-k)
    rows.append([hh, sin(hh) / hh, (1 - cos(hh)) / hh**2, (exp(hh) - 1) / hh])
table(['h', 'sin(h)/h', '(1 − cos h)/h²', '(e^h − 1)/h'], rows, fmt='%.10g')
''')
B.md(r'''
*Explain:* the middle column behaves until about $h=10^{-4}$, then goes wrong, and finally collapses to $0$. The computer stores about 16 significant digits. For $h=10^{-8}$, $\cos h$ differs from $1$ only in the 17th digit, so the computer's $\cos h$ is *exactly* $1.0$ and $1-\cos h$ is exactly $0$. This is **cancellation**: subtracting two nearly equal numbers destroys the digits that mattered.

Two lessons, both permanent:
1. **A table suggests a limit; a derivation proves it.** Here the derivation said $\frac12$ and the table eventually says $0$.
2. In numerical work (every simulator in this course!), *smaller step is not automatically better*. You will meet this again when you differentiate numerically in Unit 2.
''')

# =====================================================================================
B.md(r'''
---
# Part 4 — Continuity

## 4.1 What "continuous" means

**Why.** "You can draw it without lifting the pen" is the picture. The precise version matters because the two most useful theorems of this part work *only* for continuous functions, and because Rule 1 ("just substitute") is nothing else than continuity.

**Definition.** $f$ is **continuous at $a$** if
$$\lim_{x\to a}f(x)=f(a).$$
In words: *the value the function approaches is the value it has.* That one line contains three requirements:

1. $f(a)$ **exists** ($a$ is in the domain);
2. $\lim_{x\to a}f(x)$ **exists** (left and right agree, no blow-up, no oscillation);
3. the two are **equal**.

If any of the three fails, $f$ is **discontinuous** at $a$. The way it fails gives the type:
''')
B.fig('discontinuities', F.discontinuities, 'Four kinds of discontinuity.')
B.md(r'''
| type | what fails | example |
|---|---|---|
| **removable** (a hole) | the limit exists, but $f(a)$ is missing or is some other value | $\frac{x^2-9}{x-3}$ at $3$ |
| **jump** | left and right limits differ | $\frac{\lvert x\rvert}{x}$ at $0$ |
| **infinite** | blow-up | $\frac1x$ at $0$ |
| **oscillating** | no settling | $\sin\frac1x$ at $0$ |

A removable discontinuity can be *repaired* by defining (or redefining) $f(a)$ to be the limit. The others cannot.

**Which functions are continuous?** Polynomials; quotients of polynomials wherever the denominator is not zero; roots; $\sin$, $\cos$, $e^x$, $\ln x$ — each at every point of its domain. Sums, products and compositions of continuous functions are continuous (that is what the limit laws say). So in practice a formula is continuous everywhere **except** where a denominator is zero, or at the joins of a function defined in pieces. Those are the only places you need to check.

**Worked example 1 — a function in pieces.** Find $k$ so that
$$f(x)=\begin{cases}kx+1 & x\le2\\ x^2-k & x>2\end{cases}$$
is continuous everywhere.

1. Each piece is a polynomial: continuous on its own stretch. The only doubtful point is the join, $x=2$.
2. Left-hand limit (first rule): $k\cdot2+1=2k+1$. This is also $f(2)$.
3. Right-hand limit (second rule): $2^2-k=4-k$.
4. Continuity needs them equal: $2k+1=4-k\Rightarrow3k=3\Rightarrow k=1$.
5. Check: with $k=1$ the left piece ends at height $3$ and the right piece starts at height $4-1=3$ ✓.

**Worked example 2 — repairing a hole.** $f(x)=\dfrac{x^2-1}{x-1}$ is undefined at $1$. Since $\dfrac{(x-1)(x+1)}{x-1}=x+1\to2$, defining $f(1)=2$ makes $f$ continuous.
''')
B.ask(r'''Find $c$ so that $f(x)=\begin{cases}x^2+c & x<1\\ 3x & x\ge1\end{cases}$ is continuous.''', 'num', 2,
      r'''At the join $x=1$: from the left $1+c$, from the right (and the value) $3$. Equal when $1+c=3$, so $c=2$.''',
      r'''Compute the left-hand and right-hand limits at $x=1$ and set them equal.''')

B.md(r'''
## 4.2 The intermediate value theorem

**Theorem (IVT).** If $f$ is **continuous** on the interval $[a,b]$, then $f$ takes **every value between $f(a)$ and $f(b)$** somewhere in that interval.

In particular: **if $f(a)$ and $f(b)$ have opposite signs, then $f(x)=0$ for some $x$ between $a$ and $b$.**

**Why it is believable.** To get from a point below the $x$-axis to a point above it without lifting the pen, you must cross the axis. A discontinuous function can cheat by jumping over — which is exactly why the theorem demands continuity.

*(Honesty note: a full proof needs a careful statement of what the real numbers are — that the number line has no "gaps". That belongs to a course in analysis. For engineering the statement is what you use.)*

**Worked example.** Show that $x^3-x-1=0$ has a solution between $1$ and $2$.
1. $f(x)=x^3-x-1$ is a polynomial, hence continuous.
2. $f(1)=1-1-1=-1<0$. $\;f(2)=8-2-1=5>0$.
3. Opposite signs, so by the IVT there is a root in $(1,2)$.

Notice what the theorem does and does not give: it *guarantees a root exists* — for an equation you cannot solve by formula — but not where. The next section turns it into a way to find the root.

## 4.3 Bisection: turning the theorem into an algorithm

**Build.**

**The idea.** We know a root is trapped in $[a,b]$ because the signs at the ends differ. Cut the interval in half at the midpoint $m=\frac{a+b}{2}$ and look at the sign of $f(m)$:
- if $f(a)$ and $f(m)$ have opposite signs, the root is trapped in the **left** half $[a,m]$;
- otherwise $f(m)$ and $f(b)$ have opposite signs, and it is trapped in the **right** half $[m,b]$.

Either way, a root is now trapped in an interval **half as wide**. Repeat.
''')
B.fig('bisection', F.bisection, 'Each step keeps the half in which the sign changes.')
B.md(r'''
**By hand, for $f(x)=x^3-x-1$ on $[1,2]$** ($f(1)<0$, $f(2)>0$):

| step | interval | midpoint $m$ | $f(m)$ | sign | keep |
|---|---|---|---|---|---|
| 1 | $[1,\ 2]$ | $1.5$ | $0.875$ | $+$ | $[1,\ 1.5]$ |
| 2 | $[1,\ 1.5]$ | $1.25$ | $-0.297$ | $-$ | $[1.25,\ 1.5]$ |
| 3 | $[1.25,\ 1.5]$ | $1.375$ | $0.225$ | $+$ | $[1.25,\ 1.375]$ |

After three steps the root is known to lie in $[1.25,1.375]$. (It is $1.3247\ldots$)

**How fast is it?** Each step halves the width. Starting from width $b-a$:
$$\text{width after $n$ steps}=\frac{b-a}{2^n}.$$
To get the width below a tolerance $\varepsilon$:
$$\frac{b-a}{2^n}<\varepsilon\quad\Longleftrightarrow\quad2^n>\frac{b-a}{\varepsilon}\quad\Longleftrightarrow\quad n>\log_2\frac{b-a}{\varepsilon}.$$
*Example:* from width 1 to width $10^{-3}$: $2^n>1000$. Since $2^{10}=1024$, **10 steps** suffice. Every 10 steps buy three more decimal places.

**How to test for "opposite signs" in code:** two numbers have opposite signs exactly when their product is negative: `f(a) * f(m) < 0`.

### Experiment 3 — write a root finder
This is the first piece of real code you write in this course. Replace each `...` by one expression. Then run the cell; the tests underneath tell you whether it works.

**Before you run it, predict:** about how many times will the loop run for the default tolerance $10^{-9}$ on an interval of width 1?
''')
B.code(r'''
def bisect(f, a, b, tol=1e-9):
    """Return an approximate root of f in [a, b]. Needs: f continuous, f(a) and f(b) of opposite sign."""
    while b - a > tol:              # repeat as long as the interval is still too wide
        m = ...                     # (1) the midpoint of a and b
        if f(a) * f(m) <= 0:        # sign change between a and m?  then a root is in [a, m]
            b = ...                 # (2) move the right end
        else:                       # otherwise the root is in [m, b]
            a = ...                 # (3) move the left end
    return (a + b) / 2


# ---------- tests: do not change ----------
def test_bisect():
    cases = [('x² − 2 on [0, 2]', lambda v: v * v - 2, 0, 2, sqrt(2)),
             ('cos x on [0, 2]', cos, 0, 2, pi / 2),
             ('x³ − x − 1 on [1, 2]', lambda v: v**3 - v - 1, 1, 2, 1.324717957244746),
             ('1 − x² on [0, 3]  (a decreasing function)', lambda v: 1 - v * v, 0, 3, 1.0)]
    good = 0
    for name, f, a, b, true in cases:
        try:
            r = bisect(f, a, b)
        except Exception as err:
            print('✗', name, '-> not working yet:', type(err).__name__, '(have you replaced all three ... ?)'); continue
        ok = abs(r - true) < 1e-6; good += ok
        print('✓' if ok else '✗', name, '->', r)
    print('\nAll tests passed - you have written a root finder.' if good == len(cases) else '\nNot there yet. Re-read the idea above the cell.')

test_bisect()
''', ref=r'''
def bisect(f, a, b, tol=1e-9):
    while b - a > tol:
        m = (a + b) / 2
        if f(a) * f(m) <= 0:
            b = m
        else:
            a = m
    return (a + b) / 2
print('root of x^2 - 2:', bisect(lambda v: v * v - 2, 0, 2))
''')
B.md(r'''
*Explain:* for width 1 and tolerance $10^{-9}$ you need $2^n>10^9$, i.e. $n=30$ passes through the loop ($2^{30}\approx1.07\times10^9$).

**Where you will see this again.** Every simulator in this course repeatedly solves equations that have no formula solution. The Voltaic circuit simulator uses *Newton's method* for circuits with diodes: a faster cousin of bisection that you can build once you have derivatives (Unit 2). Bisection is slower but **cannot fail** once a sign change is trapped — which is why it is the fallback inside most professional solvers.
''')

# =====================================================================================
B.md(r'''
---
# Part 5 — The exact definition of a limit ($\varepsilon$–$\delta$)

*About one hour. You will not need to produce such proofs in this course, but you should be able to read the definition and know that the word "approaches" has an exact meaning behind it.*

**Why.** "As close as we like … by taking $x$ close enough" is still words. In the 19th century, limits were made exact by turning those words into a **challenge and a response**.

**Build.**

**Step 1 — the game.** I claim that $\lim_{x\to a}f(x)=L$. A sceptic challenges me:

> *Sceptic:* "I want $f(x)$ within a tolerance $\varepsilon$ of $L$." (He names any positive $\varepsilon$ — as small as he pleases.)
> *Me:* "Then stay within the distance $\delta$ of $a$." (I must answer with a positive $\delta$ that makes his demand come true.)

My claim is correct if I can answer **every** challenge.

**Step 2 — in symbols.** "Within $\varepsilon$ of $L$" is $|f(x)-L|<\varepsilon$. "Within $\delta$ of $a$, but not at $a$" is $0<|x-a|<\delta$. So:

> $\lim_{x\to a}f(x)=L$ means: **for every $\varepsilon>0$ there is a $\delta>0$ such that $0<|x-a|<\delta$ implies $|f(x)-L|<\varepsilon$.**

Compare with the three points of §1.2: "for every $\varepsilon$" is *as close as we like*; "$0<|x-a|$" is *not equal to $a$*; and $|x-a|<\delta$ covers *both sides*.
''')
B.fig('eps_delta', F.eps_delta, 'The sceptic chooses the red band (height ±ε). I answer with a blue band (width ±δ) narrow enough that the graph stays inside the red band.')
B.md(r'''
**Worked example.** Prove that $\displaystyle\lim_{x\to3}(2x+1)=7$.

*Scratch work — find out what $\delta$ must be.* The sceptic wants $|f(x)-L|<\varepsilon$:
$$|(2x+1)-7|=|2x-6|=2\,|x-3| .$$
So the demand is $2|x-3|<\varepsilon$, i.e. $|x-3|<\dfrac\varepsilon2$. That tells me what to answer: $\delta=\dfrac\varepsilon2$.

*The proof.* Let $\varepsilon>0$ be given. Choose $\delta=\frac\varepsilon2$. If $0<|x-3|<\delta$, then
$$|(2x+1)-7|=2|x-3|<2\delta=2\cdot\frac\varepsilon2=\varepsilon .\qquad\blacksquare$$

*In numbers:* if he demands $\varepsilon=0.01$, I answer $\delta=0.005$: any $x$ within $0.005$ of $3$ gives $2x+1$ within $0.01$ of $7$. The slope 2 is why I need half his tolerance: the function doubles every error in $x$.

### Experiment 4 — play the game
The sceptic's tolerance is `eps`; you answer with `delta`. The picture shows whether the graph stays inside the red band over your blue band.

**Find, for each of `eps` = 2, 1 and 0.4, the largest `delta` that wins.** What is the pattern?
''')
B.code(r'''
def game(eps=1.0, delta=1.0):
    a, L = 3, 7
    f = lambda v: 2 * v + 1
    xs = np.linspace(0, 6, 400)
    inside = np.linspace(a - delta, a + delta, 400)
    win = np.all(np.abs(f(inside) - L) <= eps + 1e-12)
    plt.figure(figsize=(7, 4.2))
    plt.axhspan(L - eps, L + eps, color='red', alpha=0.15); plt.axvspan(a - delta, a + delta, color='blue', alpha=0.12)
    plt.plot(xs, f(xs), 'k'); plt.plot(inside, f(inside), color='g' if win else 'r', lw=4)
    plt.plot([a], [L], 'ko'); plt.xlim(0, 6); plt.ylim(0, 14); plt.xlabel('x'); plt.show()
    print('You WIN: every x in your band lands inside his band.' if win else 'You LOSE: part of the graph leaves the red band. Choose a smaller delta.')

explore(game, eps=(0.2, 3, 0.2, 1), delta=(0.05, 2, 0.05, 1))
''')
B.ask(r'''For $f(x)=3x-1$ and the claim $\lim_{x\to2}f(x)=5$: the sceptic names $\varepsilon=0.03$. What is the **largest** $\delta$ you can answer with?''', 'num', 0.01,
      r'''$|(3x-1)-5|=|3x-6|=3|x-2|$. The demand $3|x-2|<0.03$ means $|x-2|<0.01$. So $\delta=\dfrac\varepsilon3=0.01$. The slope 3 triples every error, so you need a third of his tolerance.''',
      r'''Simplify $|(3x-1)-5|$ to a multiple of $|x-2|$, then solve the demand for $|x-2|$.''')

B.md(r'''
---
# Part 6 — Where this is going

In §1.1 you computed
$$\lim_{h\to0}\frac{s(1+h)-s(1)}{h}=10$$
and called it the speed at $t=1$. Do the same at a general time $t$, for a general function $f$, and you have the central definition of the next unit:
$$f'(x)=\lim_{h\to0}\frac{f(x+h)-f(x)}{h} .$$
This is the **derivative** of $f$ at $x$. Geometrically it is the slope of the graph at one point; physically it is a rate of change at one instant. Every technique from this week returns there: *expand and cancel* gives the derivative of $x^n$; $\frac{\sin h}{h}\to1$ and $\frac{1-\cos h}{h}\to0$ give the derivative of $\sin x$; $\frac{e^h-1}{h}\to1$ gives the derivative of $e^x$.

## Week 3 summary — everything on one page

**Meaning.** $\lim_{x\to a}f(x)=L$: $f(x)$ gets as close to $L$ as we like when $x$ is close enough to $a$, $x\ne a$. Both sides must agree. The value $f(a)$ is irrelevant.

**Computing.**
1. Substitute. A number → done.
2. $\frac00$ → factor / conjugate / common denominator / expand; cancel; substitute.
3. $\frac{\text{non-zero}}{0}$ → $\pm\infty$, vertical asymptote; check the sign on each side.
4. $x\to\infty$ → divide by the highest power; $\frac{c}{x^n}\to0$.

**Special limits (radians).**
$$\frac{\sin x}{x}\to1,\qquad\frac{\sin kx}{x}\to k,\qquad\frac{\tan x}{x}\to1,\qquad\frac{1-\cos x}{x^2}\to\frac12,\qquad\frac{1-\cos x}{x}\to0,$$
$$\left(1+\frac1n\right)^n\to e,\qquad\left(1+\frac rn\right)^n\to e^r,\qquad\frac{e^h-1}{h}\to1 .$$

**Continuity.** $\lim_{x\to a}f(x)=f(a)$. Check only at zeros of denominators and at the joins of piecewise functions.

**IVT and bisection.** Continuous + sign change ⇒ a root in between. Halving: width $\frac{b-a}{2^n}$ after $n$ steps.
''')

# =====================================================================================
B.md(r'''
---
# Week 3 problems

Paper first. First attempt counts. `hint(n)` → `solution(n)` → `mistake(n, '...')`.

### The idea of a limit
''')
B.problem(S1, r'A stone falls $s(t)=5t^2$ metres in $t$ seconds. Its average speed between $t=2$ and $t=2+h$ simplifies to an expression of the form $A+Bh$. Find the instantaneous speed at $t=2$, i.e. $\displaystyle\lim_{h\to0}\frac{s(2+h)-s(2)}{h}$.', 'num', 20,
          [r'Write out $s(2+h)-s(2)=5(2+h)^2-20$ and expand the square.', r'$5(4+4h+h^2)-20=20h+5h^2$. Divide by $h$.'],
          r'''$$\frac{s(2+h)-s(2)}{h}=\frac{5(2+h)^2-20}{h}=\frac{5(4+4h+h^2)-20}{h}=\frac{20h+5h^2}{h}=20+5h .$$
As $h\to0$ this tends to **20 m/s**.

(At $t=1$ it was 10 m/s: the speed grows by 10 m/s every second — that is $g$.)''', fmt='m/s')
B.problem(S1, r'Compute the **left-hand** limit $\displaystyle\lim_{x\to2^-}\frac{|x-2|}{x-2}$.', 'num', -1,
          [r'From the left, $x<2$, so $x-2$ is negative. What is $|x-2|$ then?', r'For $x<2$: $|x-2|=-(x-2)$.'],
          r'''For $x<2$ the quantity $x-2$ is negative, so $|x-2|=-(x-2)$:
$$\frac{|x-2|}{x-2}=\frac{-(x-2)}{x-2}=-1 .$$
The function is constantly $-1$ to the left of 2, so the left-hand limit is **−1**. (From the right it is $+1$; the two-sided limit does not exist.)''')
B.md(r'''
### Computing limits
''')
B.problem(S2, r'$\displaystyle\lim_{x\to2}\frac{x^2-5x+6}{x-2}$', 'num', -1,
          [r'Substitution gives $\frac00$, so $(x-2)$ is a factor of the top. Factor it.', r'$x^2-5x+6=(x-2)(x-3)$.'],
          r'''Substitution: $\frac{4-10+6}{0}=\frac00$. Factor (two numbers with product $6$ and sum $-5$: $-2$ and $-3$):
$$\frac{x^2-5x+6}{x-2}=\frac{(x-2)(x-3)}{x-2}=x-3\ \xrightarrow[x\to2]{}\ -1 .$$''')
B.problem(S2, r'$\displaystyle\lim_{x\to0}\frac{\sqrt{x+9}-3}{x}$', 'num', 1 / 6,
          [r'A root and $\frac00$: multiply top and bottom by the conjugate $\sqrt{x+9}+3$.', r'The top becomes $(x+9)-9=x$, which cancels with the $x$ below.'],
          r'''$$\frac{\sqrt{x+9}-3}{x}\cdot\frac{\sqrt{x+9}+3}{\sqrt{x+9}+3}=\frac{(x+9)-9}{x\,(\sqrt{x+9}+3)}=\frac{x}{x\,(\sqrt{x+9}+3)}=\frac{1}{\sqrt{x+9}+3}.$$
Now substitute $x=0$: $\dfrac{1}{3+3}=\dfrac16\approx0.1667$.''', fmt='a number, e.g. `1/8`')
B.problem(S2, r'$\displaystyle\lim_{h\to0}\frac{(3+h)^2-9}{h}$', 'num', 6,
          [r'Expand $(3+h)^2$.'],
          r'''$$\frac{9+6h+h^2-9}{h}=\frac{6h+h^2}{h}=6+h\ \xrightarrow[h\to0]{}\ 6 .$$
(This is the slope of the parabola $y=x^2$ at $x=3$. Compare: at $x=2$ it was 4. Can you guess the slope at a general $x$? Unit 2 starts there.)''')
B.problem(S2, r'$\displaystyle\lim_{x\to0}\frac{\frac{1}{x+1}-1}{x}$', 'num', -1,
          [r'Combine the top into one fraction: $\frac{1}{x+1}-1=\frac{1-(x+1)}{x+1}$.', r'The top is $\frac{-x}{x+1}$. Dividing by $x$ cancels the $x$.'],
          r'''**Combine the top.** $\dfrac{1}{x+1}-1=\dfrac{1-(x+1)}{x+1}=\dfrac{-x}{x+1}$.

**Divide by $x$.** $\dfrac{-x}{(x+1)\,x}=\dfrac{-1}{x+1}$.

**Substitute.** $\dfrac{-1}{0+1}=$ **−1**.''')
B.problem(S2, r'$\displaystyle\lim_{x\to\infty}\frac{6x^2-x}{2x^2+5}$', 'num', 3,
          [r'Divide top and bottom by $x^2$.'],
          r'''$$\frac{6x^2-x}{2x^2+5}=\frac{6-\frac1x}{2+\frac{5}{x^2}}\ \xrightarrow[x\to\infty]{}\ \frac{6-0}{2+0}=3 .$$''')
B.problem(S2, r'$\displaystyle\lim_{x\to\infty}\left(\sqrt{x^2+6x}-x\right)$', 'num', 3,
          [r'"$\infty-\infty$" with a root: multiply and divide by the conjugate $\sqrt{x^2+6x}+x$.',
           r'You get $\dfrac{6x}{\sqrt{x^2+6x}+x}$. Now divide top and bottom by $x$; inside the root that means dividing by $x^2$.'],
          r'''$$\sqrt{x^2+6x}-x=\frac{(x^2+6x)-x^2}{\sqrt{x^2+6x}+x}=\frac{6x}{\sqrt{x^2+6x}+x}.$$
Divide top and bottom by $x$ (for $x>0$, $\frac{\sqrt{x^2+6x}}{x}=\sqrt{1+\frac6x}$):
$$\frac{6}{\sqrt{1+\frac6x}+1}\ \xrightarrow[x\to\infty]{}\ \frac{6}{1+1}=3 .$$''')
B.problem(S2, r'How many **vertical asymptotes** does $f(x)=\dfrac{x+1}{(x-2)(x+1)(x+3)}$ have?', 'num', 2,
          [r'A zero of the denominator gives an asymptote only if its factor does **not** cancel.'],
          r'''The denominator is zero at $x=2,\ -1,\ -3$.

The factor $(x+1)$ cancels with the numerator: at $x=-1$ the function has a finite limit $\frac{1}{(-3)(2)}=-\frac16$ — a **hole**.

At $x=2$ and $x=-3$ nothing cancels: **2** vertical asymptotes.''', fmt='an integer')
B.md(r'''
### Special limits
''')
B.problem(S3, r'$\displaystyle\lim_{x\to0}\frac{\sin5x}{\sin2x}$', 'num', 2.5,
          [r'Give each sine a matching partner: $\dfrac{\sin5x}{5x}$ and $\dfrac{2x}{\sin2x}$.', r'What factor remains after pairing? $\dfrac{5x}{2x}$.'],
          r'''$$\frac{\sin5x}{\sin2x}=\frac{\sin5x}{5x}\cdot\frac{2x}{\sin2x}\cdot\frac{5x}{2x}\ \to\ 1\cdot1\cdot\frac52=2.5 .$$''')
B.problem(S3, r'$\displaystyle\lim_{x\to0}\frac{\tan3x}{x}$', 'num', 3,
          [r'Write $\tan3x=\dfrac{\sin3x}{\cos3x}$.'],
          r'''$$\frac{\tan3x}{x}=\frac{\sin3x}{x}\cdot\frac{1}{\cos3x}=3\cdot\frac{\sin3x}{3x}\cdot\frac{1}{\cos3x}\ \to\ 3\cdot1\cdot\frac{1}{1}=3 .$$''')
B.problem(S3, r'$\displaystyle\lim_{x\to0}\frac{1-\cos2x}{x^2}$', 'num', 2,
          [r'You know $\dfrac{1-\cos u}{u^2}\to\dfrac12$. Here $u=2x$: make the denominator $(2x)^2$.', r'$x^2=\dfrac{(2x)^2}{4}$, so the expression is $4\cdot\dfrac{1-\cos2x}{(2x)^2}$.'],
          r'''**Method 1 — match the pattern.** With $u=2x$: $x^2=\frac{u^2}{4}$, so
$$\frac{1-\cos2x}{x^2}=4\cdot\frac{1-\cos u}{u^2}\ \to\ 4\cdot\frac12=2 .$$

**Method 2 — the double-angle formula** (week 2): $1-\cos2x=2\sin^2x$, so
$$\frac{2\sin^2x}{x^2}=2\left(\frac{\sin x}{x}\right)^2\to2 .$$''')
B.problem(S3, r'$\displaystyle\lim_{n\to\infty}\left(1+\frac2n\right)^n$', 'num', math.exp(2),
          [r'This is $\left(1+\frac rn\right)^n$ with $r=2$.', r'The limit is $e^r$. Type `exp(2)` or `e**2`.'],
          r'''With $n=2m$: $\left(1+\frac2n\right)^n=\left(1+\frac1m\right)^{2m}=\left[\left(1+\frac1m\right)^m\right]^2\to e^2\approx$ **7.389**.

(Continuous compounding at 200 % per year multiplies your money by $e^2$.)''', fmt='a number; you can type `exp(2)`')
B.md(r'''
### Continuity
''')
B.problem(S4, r'$f(x)=\dfrac{x^2+x-6}{x-2}$ is not defined at $x=2$. Which value must $f(2)$ be given to make $f$ continuous there?', 'num', 5,
          [r'Continuity needs $f(2)=\lim_{x\to2}f(x)$. So compute that limit.', r'$x^2+x-6=(x-2)(x+3)$.'],
          r"""Continuity at 2 requires $f(2)=\lim_{x\to2}f(x)$.

$$\frac{x^2+x-6}{x-2}=\frac{(x-2)(x+3)}{x-2}=x+3\ \xrightarrow[x\to2]{}\ 5 .$$

So define $f(2)=$ **5**. The discontinuity was *removable*: a single missing point, filled in by the limit.""")
B.problem(S4, r'Find $k$ so that $f(x)=\begin{cases}kx+1 & x\le2\\ x^2-k & x>2\end{cases}$ is continuous.', 'num', 1,
          [r'Only the join $x=2$ needs checking. Left-hand limit $=2k+1$, right-hand limit $=4-k$.'],
          r'''Left of the join: $kx+1\to2k+1$ (this is also $f(2)$). Right of the join: $x^2-k\to4-k$.

Equal: $2k+1=4-k\ \Rightarrow\ 3k=3\ \Rightarrow\ k=$ **1**.

Check: both pieces meet at height 3.''')
B.problem(S4, r'Bisection starts from the interval $[0,1]$. How many steps guarantee an interval narrower than $10^{-6}$?', 'num', 20,
          [r'Width after $n$ steps: $\dfrac{1}{2^n}$. You need $2^n>10^6$.', r'$2^{10}=1024\approx10^3$, so $2^{20}\approx10^6$ — just above or just below? Compute $2^{19}$ and $2^{20}$.'],
          r'''Need $\dfrac{1}{2^n}<10^{-6}$, i.e. $2^n>1\,000\,000$.

$2^{19}=524\,288$ (not enough). $2^{20}=1\,048\,576$ ✓.

**20 steps.** (Formula: $n>\log_210^6=6\log_210\approx19.93$.)''', fmt='an integer')
B.problem(S4, r'Apply bisection **by hand** to $f(x)=x^2-2$ on $[1,2]$. After **three** steps, in which interval is $\sqrt2$ trapped?', 'tuple', [1.375, 1.5],
          [r'Step 1: $m=1.5$, $f(1.5)=0.25>0$. $f(1)=-1<0$. Which half has the sign change?', r'After step 1: $[1,1.5]$. Step 2: $m=1.25$, $f=-0.4375<0$ → $[1.25,1.5]$. One more.'],
          r'''$f(1)=-1<0$, $f(2)=2>0$.

| step | interval | $m$ | $f(m)=m^2-2$ | keep |
|---|---|---|---|---|
| 1 | $[1,\ 2]$ | $1.5$ | $+0.25$ | $[1,\ 1.5]$ |
| 2 | $[1,\ 1.5]$ | $1.25$ | $-0.4375$ | $[1.25,\ 1.5]$ |
| 3 | $[1.25,\ 1.5]$ | $1.375$ | $-0.109$ | $[1.375,\ 1.5]$ |

$\sqrt2=1.41421\ldots$ lies in **$[1.375,\ 1.5]$** ✓, an interval of width $\frac18=\frac{1}{2^3}$.''', fmt='a tuple `(left end, right end)`')
B.code(r'''
# scratch cell: use Python as a calculator here
''')

B.md(r'''
---
# Finish the week — and the unit

### 1 · Daily drill and report
''')
B.code(r'''
drill()
''')
B.code(r'''
drill_check([..., ..., ..., ..., ..., ..., ..., ..., ..., ...])
''', ref='drill(); drill_check([v for _, _, v in _DR["qs"]])')
B.code(r'''
report()
''')
B.md(r'''
### 2 · Teach-back (30 minutes, from memory)
1. What exactly does $\lim_{x\to a}f(x)=L$ say, and why is $f(a)$ irrelevant?
2. Why may you cancel $(x-3)$ in $\frac{x^2-9}{x-3}$ when taking the limit as $x\to3$?
3. Sketch the picture for $\frac{\sin x}{x}\to1$ and write the chain of three inequalities.
4. What is $e$?
5. Why does bisection always work for a continuous function with a sign change, and how fast?

*Your answers:*

&nbsp;

### 3 · Physics strand — instantaneous velocity in a simulation (1 hour)
The projectile experiment plots position and velocity against time. With drag switched off ($k=0$), the height is $y(t)=v_0\sin(\text{angle})\,t-\frac12gt^2$.

**Predict first:** from the height plot alone, at what moment is the vertical velocity zero? What does the height graph look like there? Then check on the velocity plot (`vy`). Export the data with the **CSV** button if you like, and compute an average vertical speed over a short interval near the top — it should be close to zero, and closer the shorter the interval. That is §1.1 of this notebook, on real (simulated) data.
''')
B.code(r'''
lab('physics', exp='proj', k=0, v0=25, ang=60)
''')
B.md(r'''
### 4 · Unit 1 review
Open the three notebooks of this unit and run `report()` in each (or look at the course map on the hub page, which collects them).

- Every week at ≥ 80 % first time → **Unit 2 (derivatives)** starts.
- Otherwise: redo the missed problems on a *different day* without opening the solutions, and read your `mistakes()` log. Which *type* of mistake repeats — a sign, a quadrant, an algebra slip, a concept? Tell your tutor; that decides what the patch week looks like.
''')

if __name__ == '__main__':
    B.write()
