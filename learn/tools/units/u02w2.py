"""Unit 2 · Week 2 (course week 5) - Derivatives of sin, cos, exp, ln; product, quotient and chain rules."""
import math
from nbkit import Book
import figs_u02 as F

B = Book('u02w2', 'Unit 2 · Week 2 — The rules of differentiation', 'year1/u02w2-rules-of-differentiation.ipynb')
S1, S2, S3, S4 = '1 sin, cos and exp', '2 Product and quotient', '3 Chain rule', '4 ln, powers and applications'

B.md(r'''
# Unit 2 · Week 2 — The rules of differentiation
*Term 1, week 5 of 12 · about 15 hours in this notebook and on paper*

**Where you are.** Last week you defined the derivative, proved the power rule, and learned that sums can be differentiated term by term — but that products, quotients and "functions inside functions" cannot be handled so naively. This week removes every one of those restrictions.

**What you will be able to do at the end of this week**
1. **Prove** that $\frac{d}{dx}\sin x=\cos x$, $\frac{d}{dx}\cos x=-\sin x$ and $\frac{d}{dx}e^x=e^x$ from the definition.
2. **Prove** and use the product rule, the quotient rule and the chain rule.
3. Derive $\frac{d}{dx}\ln x=\frac1x$, and with it the power rule for *every* real power, and $\frac{d}{dx}a^x$.
4. Differentiate any formula built from powers, trig functions, exponentials and logarithms — and check your answer numerically.

**What is used from earlier:** the definition of the derivative and the four steps (last week); the addition formulas for $\sin$ and $\cos$ (Unit 1 week 2); the limits $\frac{\sin h}{h}\to1$, $\frac{1-\cos h}{h}\to0$, $\frac{e^h-1}{h}\to1$ (Unit 1 week 3); composition — outer and inner function (Unit 1 week 1, §1.4).

**A new tool.** `compare(f, your_derivative)` plots the numerical slope of `f` against the formula you worked out. If the curves coincide, your derivative is right. Use it on *anything* you differentiate this week. Write both functions with `v` as the variable, for example

`compare(lambda v: v**2 * sin(v),  lambda v: 2*v*sin(v) + v**2*cos(v))`

Run the grey *SETUP* cell first.
''')

# =====================================================================================
B.md(r'''
---
# Part 1 — Sine, cosine and the exponential

## 1.1 Guess first: what is the slope of the sine curve?

**Build.** Before proving anything, look. Walk along the graph of $\sin x$ and estimate its slope:

| at $x=$ | $0$ | $\frac\pi2$ | $\pi$ | $\frac{3\pi}{2}$ | $2\pi$ |
|---|---|---|---|---|---|
| the graph is… | rising, steepest | flat (top) | falling, steepest | flat (bottom) | rising, steepest |
| slope | positive, maximal | $0$ | negative, minimal | $0$ | positive, maximal |

A function that is maximal at $0$, zero at $\frac\pi2$, minimal at $\pi$, zero at $\frac{3\pi}{2}$: that is the description of $\cos x$. And how steep is the sine at $0$? By $\frac{\sin h}{h}\to1$: slope exactly $1=\cos0$. So the guess is $\frac{d}{dx}\sin x=\cos x$.

### Experiment 1 — test the guess numerically
**Predict first:** if the guess is right, what will the plot show? Then also try `cos` in place of `sin` in the first line and guess *its* derivative from the picture.
''')
B.code(r'''
func = sin                                   # try also:  cos
xs = np.linspace(0, 2 * pi, 400)
plt.plot(xs, func(xs), color='0.6', label='the function')
plt.plot(xs, nderiv(func, xs), lw=6, alpha=0.3, label='its numerical slope')
plt.plot(xs, np.cos(xs), 'r--', label='cos x')
plt.xticks([k * pi / 2 for k in range(5)], ['0', 'π/2', 'π', '3π/2', '2π']); plt.legend(fontsize=9); plt.show()
''')
B.md(r'''
## 1.2 Proof: the derivative of $\sin x$ is $\cos x$

**Theorem.** $\dfrac{d}{dx}\sin x=\cos x$ ($x$ in radians).

**Proof.** The four steps.

**Step 1 — $f(x+h)$.** We need $\sin(x+h)$ split into a part depending on $x$ and a part depending on $h$. That is exactly what the addition formula does (Unit 1 week 2, §1.5):
$$\sin(x+h)=\sin x\cos h+\cos x\sin h .$$

**Step 2 — subtract $f(x)$, and group** the two terms that contain $\sin x$:
$$\sin(x+h)-\sin x=\sin x\cos h-\sin x+\cos x\sin h=\sin x\,(\cos h-1)+\cos x\sin h .$$

**Step 3 — divide by $h$.**
$$\frac{\sin(x+h)-\sin x}{h}=\sin x\cdot\frac{\cos h-1}{h}+\cos x\cdot\frac{\sin h}{h}.$$
Here $h$ cannot be cancelled algebraically. But the two fractions are precisely the special limits of Unit 1 week 3, §3.2–3.3:
$$\frac{\sin h}{h}\to1,\qquad\frac{\cos h-1}{h}=-\frac{1-\cos h}{h}\to0 .$$

**Step 4 — let $h\to0$.** During the limit $x$ is fixed, so $\sin x$ and $\cos x$ are constants:
$$\frac{d}{dx}\sin x=\sin x\cdot0+\cos x\cdot1=\cos x .\qquad\blacksquare$$

Trace back what this rests on: the addition formula (proved from the unit circle) and $\frac{\sin h}{h}\to1$ (proved by the area squeeze). Nothing was assumed.

## 1.3 The derivative of $\cos x$ is $-\sin x$

**Proof.** Same four steps with $\cos(x+h)=\cos x\cos h-\sin x\sin h$:
$$\frac{\cos(x+h)-\cos x}{h}=\cos x\cdot\frac{\cos h-1}{h}-\sin x\cdot\frac{\sin h}{h}\ \xrightarrow[h\to0]{}\ \cos x\cdot0-\sin x\cdot1=-\sin x .\qquad\blacksquare$$

$$\boxed{\frac{d}{dx}\sin x=\cos x\qquad\frac{d}{dx}\cos x=-\sin x}$$

**Why the minus sign makes sense.** Just after $x=0$ the cosine graph starts to *fall* from its maximum, so its slope must be negative there — and $-\sin x$ is negative for small positive $x$ ✓.

**A picture that explains both at once.** A point moves round the unit circle at speed 1 (one radian per second). Its position at angle $\theta$ is $(\cos\theta,\sin\theta)$. Its velocity is tangent to the circle, hence **perpendicular to the radius**, and has length 1.
''')
B.fig('sine_velocity', F.sine_velocity, 'The velocity of a point on the unit circle is the radius turned by a quarter turn.')
B.md(r'''
Turning the radius $(\cos\theta,\sin\theta)$ by a quarter turn counter-clockwise gives $(-\sin\theta,\cos\theta)$. So the horizontal coordinate $\cos\theta$ changes at the rate $-\sin\theta$, and the vertical coordinate $\sin\theta$ changes at the rate $\cos\theta$. Those are the two derivatives.

**Why radians matter here.** "Speed 1" meant one *radian* per second; that is the same as saying the limit $\frac{\sin h}{h}$ is 1. With $x$ in degrees the derivative of $\sin$ would be $\frac{\pi}{180}\cos x$. Calculus always uses radians.

## 1.4 Differentiating again: the cycle of four

$$\sin x\ \xrightarrow{\ d/dx\ }\ \cos x\ \xrightarrow{\ d/dx\ }\ -\sin x\ \xrightarrow{\ d/dx\ }\ -\cos x\ \xrightarrow{\ d/dx\ }\ \sin x$$

After four derivatives you are back. In particular the second derivative of $\sin x$ is $-\sin x$:
$$y=\sin x\quad\Rightarrow\quad y''=-y .$$
"A quantity whose acceleration is minus itself." That equation describes every oscillator — a mass on a spring, a pendulum, an LC circuit — which is why sines and cosines turn up everywhere in physics. You will return to it in Unit 9.
''')
B.ask(r'''Differentiate $f(x)=3\sin x-2\cos x$ and give the value $f'(0)$.''', 'num', 3,
      r'''Linearity: $f'(x)=3\cos x-2\cdot(-\sin x)=3\cos x+2\sin x$. At $0$: $3\cdot1+0=3$.''',
      r'''Term by term: the derivative of $\sin$ is $\cos$, the derivative of $\cos$ is $-\sin$ (watch the double minus).''')
B.ask(r'''What is the **second** derivative of $\cos x$?''', 'sym', '-cos(x)',
      r'''$\cos x\to-\sin x\to-\cos x$. Like the sine, the cosine satisfies $y''=-y$.''',
      r'''Differentiate twice: first $-\sin x$, then differentiate that.''', fmt="a formula in `x` as text")

B.md(r'''
## 1.5 The exponential function

**Why.** Powers $x^n$ have the variable in the base. Exponentials $a^x$ have it in the exponent: population growth, compound interest, radioactive decay, a discharging capacitor. The power rule does **not** apply to them ($\frac{d}{dx}2^x$ is *not* $x\,2^{x-1}$).

**Build.** Take any base $a>0$ and run the four steps on $f(x)=a^x$.

1. $f(x+h)=a^{x+h}=a^x\cdot a^h$ (the rule for adding exponents).
2. $f(x+h)-f(x)=a^x\cdot a^h-a^x=a^x\,(a^h-1)$.
3. $\dfrac{f(x+h)-f(x)}{h}=a^x\cdot\dfrac{a^h-1}{h}$.
4. As $h\to0$, $a^x$ is a constant, so
$$\frac{d}{dx}a^x=a^x\cdot\underbrace{\lim_{h\to0}\frac{a^h-1}{h}}_{\text{a number that depends only on }a}.$$

**Read this carefully — it is the whole story of exponentials.**

- The limit $\lim_{h\to0}\frac{a^h-1}{h}=\lim_{h\to0}\frac{a^{0+h}-a^0}{h}$ is, by definition, the **slope of $a^x$ at $x=0$**. Call it $k_a$.
- So $\frac{d}{dx}a^x=k_a\cdot a^x$: **the rate of change of an exponential is proportional to its current value.** The bigger it is, the faster it grows. That is the defining property of exponential growth.

**The special base.** Is there a base for which the constant $k_a$ is exactly 1? Yes: in Unit 1 week 3, §3.4 you saw that $\frac{e^h-1}{h}\to1$. That is what makes $e$ the *natural* base:

$$\boxed{\,\frac{d}{dx}e^x=e^x\,}$$

The function $e^x$ is its own derivative: at every point, its slope equals its height.
''')
B.fig('exp_slopes', F.exp_slopes, 'All exponentials pass through (0, 1). Only for base e is the slope there exactly 1.')
B.md(r'''
### Experiment 2 — the mystery constant
The cell computes $\dfrac{a^h-1}{h}$ for a small $h$ and several bases.

**Predict first:** for which base is it 1? Is it bigger or smaller than 1 for base 2? Do you recognise the numbers? (Compare with the last column.)
''')
B.code(r'''
hh = 1e-6
rows = [[a, (a**hh - 1) / hh, ln(a)] for a in [1.5, 2, e, 3, 4, 10]]
table(['base a', '(a^h − 1)/h   (slope of a^x at 0)', 'ln a'], rows, fmt='%.6f')
''')
B.md(r'''
*Explain:* the slope of $a^x$ at 0 is $\ln a$. So $\frac{d}{dx}a^x=\ln a\cdot a^x$. You will *prove* this in §4.3 once the chain rule is available; for now it is an observation.
''')
B.ask(r'''Differentiate $f(x)=5e^x-x^3$ and give $f'(0)$.''', 'num', 5,
      r'''$f'(x)=5e^x-3x^2$. At $0$: $5\cdot1-0=5$.''',
      r'''$e^x$ is its own derivative; the constant 5 stays. Then put $x=0$ ($e^0=1$).''')

# =====================================================================================
B.md(r'''
---
# Part 2 — Products and quotients

## 2.1 The product rule

**Why.** How fast does $x^2\sin x$ change? Last week's warning: the derivative of a product is **not** the product of the derivatives. ($x\cdot x=x^2$ has derivative $2x$, not $1\cdot1$.) So what is it?

**Build — see it first.** Think of two changing quantities $u$ and $v$ as the sides of a rectangle; the product $uv$ is its area. Let $x$ change a little, so that $u$ grows by $\Delta u$ and $v$ by $\Delta v$.
''')
B.fig('product_rect', F.product_rect, 'The area grows by two strips and a tiny corner.')
B.md(r'''
The area grows by
$$\Delta(uv)=\underbrace{v\,\Delta u}_{\text{right strip}}+\underbrace{u\,\Delta v}_{\text{top strip}}+\underbrace{\Delta u\,\Delta v}_{\text{corner}}.$$
Divide by $\Delta x$:
$$\frac{\Delta(uv)}{\Delta x}=v\,\frac{\Delta u}{\Delta x}+u\,\frac{\Delta v}{\Delta x}+\frac{\Delta u}{\Delta x}\cdot\Delta v .$$
Let $\Delta x\to0$. The first two terms tend to $v\,u'$ and $u\,v'$. In the third, $\frac{\Delta u}{\Delta x}\to u'$ (a finite number) while $\Delta v\to0$ (because $v$ is continuous: last week, §5.1) — so the corner contributes $u'\cdot0=0$. It is small *of second order*: a product of two small things.

$$\boxed{\,(uv)'=u'\,v+u\,v'\,}\qquad\textbf{the product rule}$$

In words: **differentiate one factor at a time, leaving the other alone, and add.**

**Proof from the definition** (the same idea in algebra). With $p(x)=u(x)\,v(x)$:
$$\begin{aligned}
p(x+h)-p(x)&=u(x+h)\,v(x+h)-u(x)\,v(x)\\
&=u(x+h)\,v(x+h)\underbrace{-u(x)\,v(x+h)+u(x)\,v(x+h)}_{\text{add and subtract the same term}}-u(x)\,v(x)\\
&=\big[u(x+h)-u(x)\big]\,v(x+h)+u(x)\,\big[v(x+h)-v(x)\big].
\end{aligned}$$
Divide by $h$ and let $h\to0$: the first bracket over $h$ tends to $u'(x)$; $v(x+h)\to v(x)$ by continuity; the second bracket over $h$ tends to $v'(x)$. Result: $u'(x)v(x)+u(x)v'(x)$. $\blacksquare$

**Worked example 1 — check on something we know.** $x^2\cdot x^3=x^5$, whose derivative is $5x^4$. Product rule with $u=x^2$, $v=x^3$:
$$u'v+uv'=2x\cdot x^3+x^2\cdot3x^2=2x^4+3x^4=5x^4\ ✓$$

**Worked example 2.** $f(x)=x^2\sin x$. Lay it out the same way every time:

| | function | derivative |
|---|---|---|
| $u$ | $x^2$ | $2x$ |
| $v$ | $\sin x$ | $\cos x$ |

$$f'(x)=u'v+uv'=2x\sin x+x^2\cos x .$$

**Worked example 3.** $f(x)=x\,e^x$. $u=x$, $u'=1$; $v=e^x$, $v'=e^x$:
$$f'(x)=1\cdot e^x+x\cdot e^x=(1+x)\,e^x .$$

**Worked example 4.** $f(x)=e^x\cos x$: $\;f'(x)=e^x\cos x+e^x\cdot(-\sin x)=e^x(\cos x-\sin x)$.

**Three factors.** Apply the rule twice: $(uvw)'=u'vw+uv'w+uvw'$ — one factor differentiated at a time.
''')
B.code(r'''
# Check worked example 2 numerically. Change both lines to test your own answers.
compare(lambda v: v**2 * sin(v),
        lambda v: 2*v*sin(v) + v**2*cos(v))
''')
B.ask(r'''Differentiate $f(x)=x^3e^x$.''', 'sym', '3*x**2*exp(x) + x**3*exp(x)',
      r'''$u=x^3$, $u'=3x^2$; $v=e^x$, $v'=e^x$. $\;f'=3x^2e^x+x^3e^x=x^2(3+x)e^x$.''',
      r'''Table: $u=x^3$, $v=e^x$. Then $u'v+uv'$. Type $e^x$ as `exp(x)`.''', fmt="a formula in `x` as text; write $e^x$ as `exp(x)`")
B.ask(r'''Differentiate $f(x)=x\sin x$ and give $f'(\pi)$.''', 'num', -math.pi,
      r'''$f'(x)=1\cdot\sin x+x\cos x$. At $\pi$: $\sin\pi+\pi\cos\pi=0+\pi\cdot(-1)=-\pi$.''',
      r'''$u=x$, $v=\sin x$: $f'=\sin x+x\cos x$. Then $\sin\pi=0$, $\cos\pi=-1$.''', fmt='a number; you can type `-pi`')

B.md(r'''
## 2.2 The quotient rule

**Build — derive it from the product rule.** Let $q=\dfrac uv$. We do not know $q'$, but we can remove the fraction: $u=q\cdot v$. Differentiate both sides, using the product rule on the right:
$$u'=q'\,v+q\,v' .$$
Solve for $q'$:
$$\begin{aligned}
q'\,v&=u'-q\,v'\\
q'&=\frac{u'-q\,v'}{v}=\frac{u'-\frac uv\,v'}{v} &&\text{(put back $q=\tfrac uv$)}\\
&=\frac{u'v-u\,v'}{v^2} &&\text{(multiply top and bottom by $v$)}
\end{aligned}$$

$$\boxed{\,\left(\frac uv\right)'=\frac{u'v-u\,v'}{v^2}\,}\qquad\textbf{the quotient rule}$$

*How to remember the order:* it starts like the product rule ($u'v$) but with a **minus**, and the **bottom is squared**. The term with the derivative of the *top* comes first and is positive. (Check with $\frac{x}{1}$: $\frac{1\cdot1-x\cdot0}{1}=1$ ✓ — with the wrong order you would get $-1$.)

*(Honesty note: the derivation assumed that $q$ has a derivative. It does, wherever $v\ne0$; a direct proof from the definition is similar to that of the product rule.)*

**Worked example 1 (from your diagnostic).** $f(x)=\dfrac{x^2+1}{x-1}$; find $f'(2)$.

| | function | derivative |
|---|---|---|
| $u$ (top) | $x^2+1$ | $2x$ |
| $v$ (bottom) | $x-1$ | $1$ |

$$f'(x)=\frac{2x\,(x-1)-(x^2+1)\cdot1}{(x-1)^2}=\frac{2x^2-2x-x^2-1}{(x-1)^2}=\frac{x^2-2x-1}{(x-1)^2}.$$
$$f'(2)=\frac{4-4-1}{1}=-1 .$$
*Put the bracket around $(x^2+1)$ before you subtract — the minus sign applies to all of it. This is the most common slip.*

**Worked example 2 — the tangent.** $\tan x=\dfrac{\sin x}{\cos x}$: $u=\sin x$, $u'=\cos x$; $v=\cos x$, $v'=-\sin x$.
$$\frac{d}{dx}\tan x=\frac{\cos x\cdot\cos x-\sin x\cdot(-\sin x)}{\cos^2x}=\frac{\cos^2x+\sin^2x}{\cos^2x}=\frac{1}{\cos^2x}.$$
$$\boxed{\,\frac{d}{dx}\tan x=\frac{1}{\cos^2x}=\sec^2x=1+\tan^2x\,}$$
(The last form is the identity $1+\tan^2x=\sec^2x$ from Unit 1 week 2, §1.2.)

**Worked example 3 — a reciprocal.** For $\dfrac1v$ the top is $u=1$, $u'=0$: $\;\left(\dfrac1v\right)'=\dfrac{0\cdot v-1\cdot v'}{v^2}=-\dfrac{v'}{v^2}$.
E.g. $\dfrac{d}{dx}\dfrac{1}{x^2+1}=-\dfrac{2x}{(x^2+1)^2}$.

**When not to use it.** If the bottom is a single power of $x$, divide first: $\dfrac{x^3+2}{x}=x^2+2x^{-1}$, derivative $2x-\dfrac{2}{x^2}$. Faster and safer.
''')
B.ask(r'''Differentiate $f(x)=\dfrac{x}{x+1}$ and give $f'(1)$.''', 'num', 0.25,
      r'''$u=x$, $u'=1$; $v=x+1$, $v'=1$. $\;f'=\dfrac{1\cdot(x+1)-x\cdot1}{(x+1)^2}=\dfrac{1}{(x+1)^2}$. At $1$: $\dfrac14$.''',
      r'''$\dfrac{u'v-uv'}{v^2}$ with $u=x$, $v=x+1$. Simplify the top before putting $x=1$.''')
B.ask(r'''What is the slope of $y=\tan x$ at $x=\dfrac\pi4$?''', 'num', 2,
      r'''$\dfrac{d}{dx}\tan x=\dfrac{1}{\cos^2x}$. At $\frac\pi4$: $\cos^2\frac\pi4=\frac12$, so the slope is $2$. (Or $1+\tan^2\frac\pi4=1+1$.)''',
      r'''Use $\dfrac{d}{dx}\tan x=\dfrac{1}{\cos^2x}$ and $\cos\frac\pi4=\frac{\sqrt2}{2}$.''')

# =====================================================================================
B.md(r'''
---
# Part 3 — The chain rule

## 3.1 The idea: rates multiply

**Why.** Most real formulas are a function *inside* a function: $\sin(3t)$, $e^{-x^2}$, $\sqrt{x^2+1}$, $(2x+1)^{10}$. None of the rules so far touches them. The chain rule does — it is the most used rule in calculus.

**Build.** Think about rates in everyday terms. Suppose

- $y$ changes **3** times as fast as $u$, and
- $u$ changes **2** times as fast as $x$.

Then $y$ changes $3\times2=\mathbf{6}$ times as fast as $x$. (A euro is worth 1.1 dollars; a dollar is worth 150 yen; so a euro is worth $1.1\times150$ yen. Gear A turns gear B three times per turn; B turns C twice per turn; A turns C six times.) **Rates of change in a chain multiply.**
''')
B.fig('chain_gears', F.chain_gears, 'A chain of two functions: a small change is magnified twice.')
B.md(r'''
**The rule.** If $y=f(u)$ and $u=g(x)$ — that is, $y=f(g(x))$ — then

$$\boxed{\,\frac{dy}{dx}=\frac{dy}{du}\cdot\frac{du}{dx}\,}\qquad\text{or, in function notation,}\qquad\boxed{\,\frac{d}{dx}f(g(x))=f'(g(x))\cdot g'(x)\,}$$

In words: **the derivative of the outer function (evaluated at the inner function, left untouched) times the derivative of the inner function.**

## 3.2 Why it is true

**The argument.** Change $x$ by a small $\Delta x$. Then $u$ changes by some $\Delta u$, and that makes $y$ change by some $\Delta y$. As long as $\Delta u\ne0$ we may write, by plain arithmetic of fractions,
$$\frac{\Delta y}{\Delta x}=\frac{\Delta y}{\Delta u}\cdot\frac{\Delta u}{\Delta x}.$$
Now let $\Delta x\to0$. Then $\Delta u\to0$ as well ($g$ is continuous), so $\frac{\Delta y}{\Delta u}\to\frac{dy}{du}$ and $\frac{\Delta u}{\Delta x}\to\frac{du}{dx}$:
$$\frac{dy}{dx}=\frac{dy}{du}\cdot\frac{du}{dx}.$$

This is why the notation $\frac{dy}{dx}$ was designed to look like a fraction: the chain rule looks like "cancelling $du$". (It is not literally cancelling — the symbols are limits — but the rule is true, and the notation helps you remember it.)

*(Honesty note: the argument has one gap. $\Delta u$ could be zero for some small $\Delta x$ even when $\Delta x\ne0$ — for example if $g$ is constant — and then you cannot divide by it. A complete proof avoids the division by using the linear approximation of last week instead: $\Delta u\approx g'(x)\,\Delta x$ and $\Delta y\approx f'(u)\,\Delta u$, hence $\Delta y\approx f'(u)\,g'(x)\,\Delta x$, with errors that vanish faster than $\Delta x$. The conclusion is the same.)*

## 3.3 The procedure

1. **Identify the layers.** What is the outer function $f(u)$ — the *last* thing you would compute? What is the inner function $u=g(x)$? (Unit 1 week 1, §1.4.)
2. **Differentiate the outer function** with respect to $u$, and **put the inner function back** in place of $u$.
3. **Multiply by the derivative of the inner function.**

**Worked example 1 — check on something we know.** $y=(x^2+3)^2$. Last week you expanded it and got $4x^3+12x$. Now:
- outer: $u^2$, derivative $2u$; inner: $u=x^2+3$, derivative $2x$.
- $\dfrac{dy}{dx}=2u\cdot2x=2(x^2+3)\cdot2x=4x^3+12x$ ✓

**Worked example 2.** $y=\sin(3x)$.
- outer: $\sin u\to\cos u$; inner: $u=3x\to3$.
- $\dfrac{dy}{dx}=\cos(3x)\cdot3=3\cos3x$.

*Makes sense:* $\sin(3x)$ wiggles three times as fast as $\sin x$, so its slopes are three times as steep.

**Worked example 3 (from your diagnostic).** $y=e^{-x^2}$.
- outer: $e^u\to e^u$; inner: $u=-x^2\to-2x$.
- $\dfrac{dy}{dx}=e^{-x^2}\cdot(-2x)=-2x\,e^{-x^2}$.

**Worked example 4.** $y=\sqrt{x^2+1}=(x^2+1)^{1/2}$.
- outer: $u^{1/2}\to\frac12u^{-1/2}$; inner: $u=x^2+1\to2x$.
- $\dfrac{dy}{dx}=\dfrac{1}{2\sqrt{x^2+1}}\cdot2x=\dfrac{x}{\sqrt{x^2+1}}$.

**Worked example 5 — two that look alike.** Brackets decide which function is outside.
- $\sin(x^2)$: outer $\sin$, inner $x^2$. Derivative: $\cos(x^2)\cdot2x$.
- $\sin^2x=(\sin x)^2$: outer "square", inner $\sin x$. Derivative: $2\sin x\cdot\cos x$ (which is $\sin2x$).

**Worked example 6.** $y=(2x+1)^{10}$: $\;10\,(2x+1)^9\cdot2=20\,(2x+1)^9$. (Imagine expanding that first!)

**The classic mistake** is to forget step 3: writing $\frac{d}{dx}\sin(3x)=\cos(3x)$. Whenever the inside is anything other than plain $x$, **there is an extra factor**.

**Special cases worth knowing on sight** (each is the chain rule with a simple inner function):

| function | derivative | comment |
|---|---|---|
| $f(ax+b)$ | $a\,f'(ax+b)$ | linear inside → constant factor $a$ |
| $e^{kx}$ | $k\,e^{kx}$ | |
| $\sin(\omega t)$, $\cos(\omega t)$ | $\omega\cos(\omega t)$, $-\omega\sin(\omega t)$ | every derivative brings out a factor $\omega$ |
| $[g(x)]^n$ | $n\,[g(x)]^{n-1}\,g'(x)$ | power rule "with a tail" |
| $e^{g(x)}$ | $g'(x)\,e^{g(x)}$ | |
''')
B.code(r'''
# Check worked example 3 numerically, then test your own answers to the questions below.
compare(lambda v: exp(-v**2),
        lambda v: -2*v*exp(-v**2))
''')
B.ask(r'''Differentiate $y=\cos(5x)$.''', 'sym', '-5*sin(5*x)',
      r'''Outer $\cos u\to-\sin u$; inner $5x\to5$. $\;\dfrac{dy}{dx}=-\sin(5x)\cdot5=-5\sin5x$.''',
      r'''Outer function $\cos u$ (derivative $-\sin u$), inner function $u=5x$ (derivative 5). Multiply.''', fmt="a formula in `x` as text")
B.ask(r'''Differentiate $y=(x^2+1)^3$.''', 'sym', '6*x*(x**2+1)**2',
      r'''Outer $u^3\to3u^2$; inner $x^2+1\to2x$. $\;3(x^2+1)^2\cdot2x=6x(x^2+1)^2$.''',
      r'''Power rule on the bracket — leaving its contents alone — then multiply by the derivative of the contents.''', fmt="a formula in `x` as text")
B.ask(r'''Differentiate $y=e^{3x}$ and give the slope at $x=0$.''', 'num', 3,
      r'''$\dfrac{dy}{dx}=3e^{3x}$; at $0$: $3$.''',
      r'''$e^{kx}\to k\,e^{kx}$.''')

B.md(r'''
## 3.4 More than two layers, and combining the rules

**Several layers: work from the outside in, one layer at a time.** Each layer contributes one factor.

**Worked example 1.** $y=\sin^3(2x)=\big(\sin(2x)\big)^3$. Three layers: cube ← sine ← $2x$.
$$\frac{dy}{dx}=\underbrace{3\,\sin^2(2x)}_{\text{cube}}\cdot\underbrace{\cos(2x)}_{\text{sine}}\cdot\underbrace{2}_{2x}=6\sin^2(2x)\cos(2x).$$

**Worked example 2.** $y=e^{\sqrt{x^2+1}}$. Layers: $e^{\square}$ ← $\sqrt{\square}$ ← $x^2+1$.
$$\frac{dy}{dx}=e^{\sqrt{x^2+1}}\cdot\frac{1}{2\sqrt{x^2+1}}\cdot2x=\frac{x\,e^{\sqrt{x^2+1}}}{\sqrt{x^2+1}}.$$

**Chain rule inside a product.** Decide the *outermost* structure first.

**Worked example 3 (from your diagnostic).** $f(x)=x\,e^{-x}$. Outermost: a product. $u=x$, $u'=1$; $v=e^{-x}$, and by the chain rule $v'=-e^{-x}$.
$$f'(x)=1\cdot e^{-x}+x\cdot(-e^{-x})=(1-x)\,e^{-x}.$$
Since $e^{-x}$ is never zero, $f'(x)=0$ only at $x=1$: that is where $xe^{-x}$ has its maximum (the diagnostic question).

**Worked example 4.** $f(x)=x^2\sin(3x)$: $\;f'(x)=2x\sin(3x)+x^2\cdot3\cos(3x)$.

**Worked example 5 — a quotient with a chain.** $f(x)=\dfrac{e^{2x}}{x}$: $u=e^{2x}$, $u'=2e^{2x}$; $v=x$, $v'=1$.
$$f'(x)=\frac{2e^{2x}\cdot x-e^{2x}\cdot1}{x^2}=\frac{(2x-1)\,e^{2x}}{x^2}.$$

**A tip.** A quotient can always be written as a product with a negative power: $\dfrac{u}{v}=u\cdot v^{-1}$. Product rule plus chain rule then gives the same result as the quotient rule. Use whichever you find less error-prone.
''')
B.ask(r'''Differentiate $f(x)=x\cos(2x)$ and give $f'(0)$.''', 'num', 1,
      r'''Product: $u=x$, $u'=1$; $v=\cos2x$, $v'=-2\sin2x$ (chain). $f'=\cos2x-2x\sin2x$. At $0$: $1-0=1$.''',
      r'''Product rule, where the second factor needs the chain rule: $(\cos2x)'=-2\sin2x$.''')

# =====================================================================================
B.md(r'''
---
# Part 4 — The logarithm, general powers, and applications

## 4.1 The derivative of $\ln x$

**Why.** $\ln$ is the last basic function without a derivative. We do not need the definition again: $\ln$ is the **inverse** of $e^x$, and the chain rule turns that into a derivative.

**Build.**

**Step 1 — the defining property.** $\ln x$ is "the power to which $e$ must be raised to give $x$". So for $x>0$:
$$e^{\ln x}=x .$$

**Step 2 — differentiate both sides.** The right side gives $1$. The left side is a chain: outer $e^u$, inner $u=\ln x$, whose derivative is the unknown we are after:
$$e^{\ln x}\cdot\frac{d}{dx}\ln x=1 .$$

**Step 3 — solve.** Since $e^{\ln x}=x$:
$$x\cdot\frac{d}{dx}\ln x=1\qquad\Longrightarrow\qquad\boxed{\,\frac{d}{dx}\ln x=\frac1x\,}\quad(x>0)$$

*(This assumed that $\ln$ has a derivative. It does: its graph is the mirror image of the smooth graph of $e^x$ in the line $y=x$, and mirroring turns a tangent of slope $m$ into a tangent of slope $\frac1m$.)*

**Makes sense:** $\ln x$ rises steeply near $0$ (slope $\frac1x$ large) and ever more slowly for large $x$, but never stops rising ($\frac1x>0$).

**With the chain rule:**
$$\frac{d}{dx}\ln\big(g(x)\big)=\frac{1}{g(x)}\cdot g'(x)=\frac{g'(x)}{g(x)}.$$

**Worked example 1 (from your diagnostic).** $\dfrac{d}{dx}\ln(1+x^2)=\dfrac{2x}{1+x^2}$.

**Worked example 2.** $\dfrac{d}{dx}\ln(\cos x)=\dfrac{-\sin x}{\cos x}=-\tan x$.

**Worked example 3 — use log laws first.** $\dfrac{d}{dx}\ln\!\big(x^3\big)$: since $\ln x^3=3\ln x$, the derivative is $\dfrac3x$. (The chain rule gives the same: $\frac{3x^2}{x^3}$.)

## 4.2 The power rule for every real power

**Build.** Last week the power rule was proved only for whole-number powers. Now, for any real number $r$ and $x>0$, write the power with base $e$:
$$x^r=e^{\ln(x^r)}=e^{\,r\ln x}.$$
Chain rule — outer $e^u$, inner $u=r\ln x$ with derivative $\dfrac rx$:
$$\frac{d}{dx}x^r=e^{\,r\ln x}\cdot\frac rx=x^r\cdot\frac rx=r\,x^{r-1}.\qquad\blacksquare$$
The promise of last week is kept: $\frac{d}{dx}x^r=r\,x^{r-1}$ for **every** real $r$ — including $r=\frac12$, $r=-3$, $r=\pi$.

## 4.3 Exponentials with any base

**Build.** The same trick, with the variable upstairs. For $a>0$: $\;a^x=e^{\ln(a^x)}=e^{\,x\ln a}$. Here $\ln a$ is just a number, so this is $e^{kx}$ with $k=\ln a$:
$$\boxed{\,\frac{d}{dx}a^x=\ln a\cdot a^x\,}$$
That is the mystery constant of Experiment 2: the slope of $a^x$ at $0$ is $\ln a$. For $a=e$ it is $\ln e=1$.

**Logarithms with any base.** $\log_ax=\dfrac{\ln x}{\ln a}$, so $\dfrac{d}{dx}\log_ax=\dfrac{1}{x\ln a}$.

**Do not confuse** the two kinds of function:

| | variable in the… | example | derivative |
|---|---|---|---|
| power function | base | $x^3$ | $3x^2$ (power rule) |
| exponential function | exponent | $3^x$ | $\ln3\cdot3^x$ |
''')
B.ask(r'''Differentiate $f(x)=\ln(3x+1)$ and give $f'(1)$.''', 'num', 0.75,
      r'''$\dfrac{g'}{g}=\dfrac{3}{3x+1}$. At $1$: $\dfrac34$.''',
      r'''$\dfrac{d}{dx}\ln(g(x))=\dfrac{g'(x)}{g(x)}$ with $g=3x+1$.''')
B.ask(r'''What is the slope of $y=2^x$ at $x=0$? (Type it with `ln`.)''', 'num', math.log(2),
      r'''$\dfrac{d}{dx}2^x=\ln2\cdot2^x$; at $0$: $\ln2\approx0.693$.''',
      r'''$\dfrac{d}{dx}a^x=\ln a\cdot a^x$.''', fmt='a number; you can type `ln(2)`')

B.md(r'''
## 4.4 Application: the calculus of oscillations

**Build.** Take the general sinusoid of Unit 1 week 2: a mass on a spring at position
$$x(t)=A\sin(\omega t+\varphi).$$
Differentiate with the chain rule (inner function $\omega t+\varphi$, derivative $\omega$):
$$\begin{aligned}
\text{velocity:}\quad v(t)&=\frac{dx}{dt}=A\omega\cos(\omega t+\varphi),\\[2pt]
\text{acceleration:}\quad a(t)&=\frac{dv}{dt}=-A\omega^2\sin(\omega t+\varphi)=-\omega^2\,x(t).
\end{aligned}$$

**Three things to read from this.**

1. **Each derivative multiplies the amplitude by $\omega$.** Maximum speed $A\omega$; maximum acceleration $A\omega^2$. Fast oscillations have large velocities and *very* large accelerations — which is why vibration destroys machines.
2. **Each derivative shifts the wave a quarter period ahead.** $\cos u=\sin(u+\frac\pi2)$: the velocity *leads* the position by $90^\circ$. It is greatest when the mass passes through the middle and zero at the turning points.
3. **$a=-\omega^2x$:** the acceleration is proportional to the displacement and opposite to it. That is exactly Hooke's law for a spring ($F=-kx$) combined with Newton's law ($F=ma$): $a=-\frac kmx$. Comparing: $\omega^2=\frac km$, i.e. $\omega=\sqrt{k/m}$ — the formula you tested in the simulator in Unit 1 week 2. Now you know where it comes from.

**The same mathematics in a circuit.** The current into a capacitor is $i=C\,\dfrac{dv}{dt}$. If the voltage is $v=V\sin\omega t$, then $i=CV\omega\cos\omega t$: the current has amplitude $\omega CV$ and **leads the voltage by $90^\circ$**. Unit 11 (AC circuits) is built on this one line.

### Experiment 3 — position, velocity, acceleration
**Predict first:** when the position is at its maximum, what are the velocity and the acceleration? If $\omega$ is doubled (same amplitude), what happens to the height of the velocity curve? Of the acceleration curve?
''')
B.code(r'''
def oscillation(A=1.0, omega=2.0):
    ts = np.linspace(0, 2 * pi, 600)
    pos = A * np.sin(omega * ts)
    vel = A * omega * np.cos(omega * ts)
    acc = -A * omega**2 * np.sin(omega * ts)
    plt.figure(figsize=(9.5, 3.8))
    plt.plot(ts, pos, label='position  A sin ωt'); plt.plot(ts, vel, label='velocity  Aω cos ωt'); plt.plot(ts, acc, label='acceleration  −Aω² sin ωt')
    plt.axhline(0, color='k', lw=0.8); plt.xlabel('t'); plt.ylim(-10, 10); plt.legend(fontsize=9, loc='upper right'); plt.show()
    print(f'max speed Aω = {A * omega:.2f}      max acceleration Aω² = {A * omega**2:.2f}')

explore(oscillation, A=(0.5, 2, 0.5, 1), omega=(0.5, 3, 0.5, 2))
''')

B.md(r'''
## Summary — the complete table

**Basic derivatives** (all proved in weeks 1–2)

| $f(x)$ | $f'(x)$ | | $f(x)$ | $f'(x)$ |
|---|---|---|---|---|
| $c$ | $0$ | | $e^x$ | $e^x$ |
| $x^r$ (any real $r$) | $r\,x^{r-1}$ | | $a^x$ | $\ln a\cdot a^x$ |
| $\sin x$ | $\cos x$ | | $\ln x$ | $\dfrac1x$ |
| $\cos x$ | $-\sin x$ | | $\log_ax$ | $\dfrac{1}{x\ln a}$ |
| $\tan x$ | $\dfrac{1}{\cos^2x}=1+\tan^2x$ | | | |

**Rules**

| | rule |
|---|---|
| linearity | $(c\,u)'=c\,u'$, $\quad(u\pm v)'=u'\pm v'$ |
| product | $(uv)'=u'v+uv'$ |
| quotient | $\left(\dfrac uv\right)'=\dfrac{u'v-uv'}{v^2}$ |
| chain | $\dfrac{d}{dx}f(g(x))=f'(g(x))\cdot g'(x)$ |

**Method for any formula:** look at the *outermost* structure (sum? product? quotient? a function of something?), apply that rule, and repeat on the pieces. Check with `compare`.
''')

# =====================================================================================
B.md(r'''
---
# Problems

Paper first; then, if you like, test your result with `compare` in the scratch cell *before* you enter it — that is not cheating, it is what an engineer does. First attempt counts. `hint(n)` → `solution(n)` → `mistake(n, '...')`.

Type $e^x$ as `exp(x)`, $\ln x$ as `ln(x)`, $\sqrt{x}$ as `sqrt(x)`.

### sin, cos and exp
''')
B.problem(S1, r'Evaluate by recognising it as a derivative: $\displaystyle\lim_{h\to0}\frac{\sin\left(\frac\pi3+h\right)-\sin\frac\pi3}{h}$.', 'num', 0.5,
          [r"It has the form $\dfrac{f(a+h)-f(a)}{h}$ with $f=\sin$ and $a=\frac\pi3$.", r"So it equals $f'(\frac\pi3)=\cos\frac\pi3$."],
          r'''The limit is the definition of $f'(a)$ for $f(x)=\sin x$ at $a=\frac\pi3$.

$f'(x)=\cos x$, so the limit is $\cos\frac\pi3=$ **1/2**.''')
B.problem(S1, r"For $f(x)=4\cos x+e^x$, find $f''(0)$ (the second derivative at 0).", 'num', -3,
          [r"Differentiate twice. $f'(x)=-4\sin x+e^x$."],
          r'''$f'(x)=-4\sin x+e^x$.

$f''(x)=-4\cos x+e^x$.

$f''(0)=-4+1=$ **−3**.''')
B.md(r'''
### Product and quotient
''')
B.problem(S2, r'Differentiate $x^3\sin x$. *(From your diagnostic.)*', 'sym', '3*x**2*sin(x) + x**3*cos(x)',
          [r"Product rule with $u=x^3$, $v=\sin x$."],
          r'''$u=x^3$, $u'=3x^2$; $v=\sin x$, $v'=\cos x$.
$$\frac{d}{dx}\big[x^3\sin x\big]=3x^2\sin x+x^3\cos x .$$''', fmt="a formula in `x` as text")
B.problem(S2, r"For $f(x)=\dfrac{x^2+1}{x-1}$, compute $f'(2)$. *(From your diagnostic.)*", 'num', -1,
          [r"Quotient rule: $u=x^2+1$, $v=x-1$.", r"$f'(x)=\dfrac{2x(x-1)-(x^2+1)}{(x-1)^2}$. Simplify or substitute $x=2$ directly."],
          r'''$u=x^2+1$, $u'=2x$; $v=x-1$, $v'=1$.
$$f'(x)=\frac{2x(x-1)-(x^2+1)\cdot1}{(x-1)^2}=\frac{x^2-2x-1}{(x-1)^2}.$$
$$f'(2)=\frac{4-4-1}{1}=-1 .$$''')
B.problem(S2, r'Differentiate $\dfrac{x}{x^2+1}$.', 'sym', '(1 - x**2)/(x**2 + 1)**2',
          [r"$u=x$, $u'=1$; $v=x^2+1$, $v'=2x$.", r'Top: $1\cdot(x^2+1)-x\cdot2x$.'],
          r'''$$\frac{d}{dx}\frac{x}{x^2+1}=\frac{1\cdot(x^2+1)-x\cdot2x}{(x^2+1)^2}=\frac{1-x^2}{(x^2+1)^2}.$$
(So this function has horizontal tangents at $x=\pm1$.)''', fmt="a formula in `x` as text")
B.problem(S2, r"For $f(x)=x\,e^x$, find the **second** derivative at $0$, $f''(0)$.", 'num', 2,
          [r"$f'(x)=(1+x)e^x$. Differentiate that with the product rule again."],
          r'''$f'(x)=1\cdot e^x+x\,e^x=(1+x)\,e^x$.

Again by the product rule ($u=1+x$, $v=e^x$): $f''(x)=1\cdot e^x+(1+x)\,e^x=(2+x)\,e^x$.

$f''(0)=$ **2**. (Pattern: the $n$-th derivative of $xe^x$ is $(n+x)e^x$.)''')
B.problem(S2, r'At which $x>0$ is the tangent to $y=\dfrac{\ln x}{x}$ horizontal?', 'num', math.e,
          [r"Quotient rule with $u=\ln x$, $v=x$.", r"$y'=\dfrac{\frac1x\cdot x-\ln x}{x^2}=\dfrac{1-\ln x}{x^2}$. When is the top zero?"],
          r'''$u=\ln x$, $u'=\frac1x$; $v=x$, $v'=1$.
$$y'=\frac{\frac1x\cdot x-\ln x\cdot1}{x^2}=\frac{1-\ln x}{x^2}.$$
$y'=0$ when $\ln x=1$, i.e. $x=e\approx$ **2.718**.''', fmt='a number; you can type `e`')
B.md(r'''
### Chain rule
''')
B.problem(S3, r'Differentiate $e^{-x^2}$. *(From your diagnostic.)*', 'sym', '-2*x*exp(-x**2)',
          [r'Outer $e^u$, inner $u=-x^2$.'],
          r'''Outer: $e^u\to e^u$. Inner: $u=-x^2\to-2x$.
$$\frac{d}{dx}e^{-x^2}=e^{-x^2}\cdot(-2x)=-2x\,e^{-x^2}.$$''', fmt="a formula in `x` as text; write $e^{\\ldots}$ as `exp(...)`")
B.problem(S3, r'Differentiate $(2x+1)^5$.', 'sym', '10*(2*x+1)**4',
          [r'Power rule on the bracket, then multiply by the derivative of the inside.'],
          r'''$$\frac{d}{dx}(2x+1)^5=5\,(2x+1)^4\cdot2=10\,(2x+1)^4 .$$''', fmt="a formula in `x` as text")
B.problem(S3, r'Differentiate $\sin^2x$ and simplify to a single trigonometric function.', 'sym', 'sin(2*x)',
          [r'$\sin^2x=(\sin x)^2$: outer "square", inner $\sin x$.', r'You get $2\sin x\cos x$. Which double-angle formula is that?'],
          r'''Outer: $u^2\to2u$. Inner: $u=\sin x\to\cos x$.
$$\frac{d}{dx}\sin^2x=2\sin x\cos x=\sin2x .$$
(Consistent with power reduction: $\sin^2x=\frac{1-\cos2x}{2}$, whose derivative is $\frac{2\sin2x}{2}=\sin2x$ ✓.)''', fmt="a formula in `x` as text")
B.problem(S3, r"For $f(x)=\sqrt{x^2+9}$, find $f'(4)$.", 'num', 0.8,
          [r'Write it as $(x^2+9)^{1/2}$.', r"$f'(x)=\dfrac{1}{2\sqrt{x^2+9}}\cdot2x=\dfrac{x}{\sqrt{x^2+9}}$."],
          r'''$$f'(x)=\tfrac12(x^2+9)^{-1/2}\cdot2x=\frac{x}{\sqrt{x^2+9}},\qquad f'(4)=\frac{4}{\sqrt{25}}=\frac45 .$$''')
B.problem(S3, r'Differentiate $\cos(x^3)$.', 'sym', '-3*x**2*sin(x**3)',
          [r'Outer $\cos u$, inner $u=x^3$.'],
          r'''$$\frac{d}{dx}\cos(x^3)=-\sin(x^3)\cdot3x^2=-3x^2\sin(x^3).$$''', fmt="a formula in `x` as text")
B.problem(S3, r"For $f(x)=e^{2x}\sin3x$, find $f'(0)$.", 'num', 3,
          [r'Outermost structure: a product. Each factor needs the chain rule.', r"$f'(x)=2e^{2x}\sin3x+e^{2x}\cdot3\cos3x$."],
          r'''$u=e^{2x}$, $u'=2e^{2x}$; $v=\sin3x$, $v'=3\cos3x$.
$$f'(x)=2e^{2x}\sin3x+3e^{2x}\cos3x,\qquad f'(0)=0+3\cdot1\cdot1=3 .$$''')
B.problem(S3, r"For $f(x)=e^{\sin2x}$, find $f'(0)$.", 'num', 2,
          [r'Three layers: $e^{\square}$ ← $\sin\square$ ← $2x$. One factor per layer.'],
          r'''$$f'(x)=e^{\sin2x}\cdot\cos2x\cdot2,\qquad f'(0)=e^0\cdot1\cdot2=2 .$$''')
B.problem(S3, r'At which $x$ does $f(x)=x\,e^{-x}$ have a horizontal tangent? *(From your diagnostic: this is where its maximum is.)*', 'num', 1,
          [r"Product rule; the derivative of $e^{-x}$ is $-e^{-x}$.", r"$f'(x)=(1-x)e^{-x}$, and $e^{-x}$ is never zero."],
          r'''$f'(x)=1\cdot e^{-x}+x\cdot(-e^{-x})=(1-x)\,e^{-x}$.

$e^{-x}>0$ always, so $f'(x)=0$ exactly when $1-x=0$: $x=$ **1**.

($f'>0$ for $x<1$ and $f'<0$ for $x>1$: rising then falling — a maximum, of height $e^{-1}\approx0.368$.)''')
B.md(r'''
### ln, powers and applications
''')
B.problem(S4, r'Differentiate $\ln(1+x^2)$. *(From your diagnostic.)*', 'sym', '2*x/(1+x**2)',
          [r"$\dfrac{d}{dx}\ln(g(x))=\dfrac{g'(x)}{g(x)}$."],
          r'''$g(x)=1+x^2$, $g'(x)=2x$:
$$\frac{d}{dx}\ln(1+x^2)=\frac{2x}{1+x^2}.$$''', fmt="a formula in `x` as text")
B.problem(S4, r'Differentiate $\ln(\cos x)$ and simplify to a single trigonometric function.', 'sym', '-tan(x)',
          [r"$\dfrac{g'}{g}$ with $g=\cos x$."],
          r'''$$\frac{d}{dx}\ln(\cos x)=\frac{-\sin x}{\cos x}=-\tan x .$$''', fmt="a formula in `x` as text")
B.problem(S4, r'What is the slope of $y=2^x$ at $x=3$?', 'num', 8 * math.log(2),
          [r"$\dfrac{d}{dx}a^x=\ln a\cdot a^x$."],
          r'''$\dfrac{dy}{dx}=\ln2\cdot2^x$. At $x=3$: $8\ln2\approx$ **5.545**.

(*Not* $x\,2^{x-1}=12$: the power rule is for the variable in the base.)''', fmt='a number; you can type `8*ln(2)`')
B.problem(S4, r'A mass oscillates with position $x(t)=0.2\sin(5t)$ (metres, seconds). What is its **maximum acceleration** (in m/s²)?', 'num', 5,
          [r'Differentiate twice with the chain rule. Each derivative brings out a factor 5.', r'$a(t)=-0.2\cdot25\sin(5t)$. A sine is at most 1 in size.'],
          r'''$v(t)=0.2\cdot5\cos(5t)=\cos(5t)$ m/s.

$a(t)=-5\sin(5t)$ m/s².

The largest size of $a$ is **5 m/s²** ($=A\omega^2=0.2\cdot25$), reached at the turning points. The maximum speed is $A\omega=1$ m/s, reached in the middle.''', fmt='m/s²')
B.problem(S4, r'The voltage across a $100\ \mu\text{F}$ capacitor is $v(t)=10\sin(100t)$ volts. The current is $i=C\,\dfrac{dv}{dt}$. What is the **peak current** in amperes?', 'num', 0.1,
          [r'$C=100\times10^{-6}$ F. Differentiate $v$ with the chain rule.', r'$\dfrac{dv}{dt}=1000\cos(100t)$ V/s.'],
          r'''$\dfrac{dv}{dt}=10\cdot100\cos(100t)=1000\cos(100t)$ V/s.

$i=C\dfrac{dv}{dt}=10^{-4}\cdot1000\cos(100t)=0.1\cos(100t)$ A.

Peak current: **0.1 A** ($=\omega CV$). It is a cosine: the current leads the voltage by a quarter period.''', fmt='amperes')
B.code(r'''
# scratch cell: test your derivatives here before you enter them, e.g.
# compare(lambda v: v**3 * sin(v),  lambda v: ...your answer... )
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
1. Derive $\frac{d}{dx}\sin x=\cos x$ from the definition. Which two limits do you need, and where does the addition formula come in?
2. Why is the derivative of every exponential $a^x$ proportional to $a^x$ itself, and what is special about $e$?
3. Draw the rectangle for the product rule and say why the corner does not count.
4. State the chain rule in words and explain it with a rates-multiply example of your own.
5. Derive $\frac{d}{dx}\ln x=\frac1x$ from $e^{\ln x}=x$.

*Your answers:*

&nbsp;

### 3 · Physics strand — velocity leads position by a quarter period (1 hour)
The simulator shows a mass on a spring ($k=25$ N/m, $m=1$ kg, so $\omega_0=5$ rad/s), released from rest at $x=1$ m with no friction: $x(t)=\cos5t$.

**Predict first, from §4.4:** the amplitude of the velocity plot; the times of the first zero of the position and of the first extreme of the velocity; and the total energy plot — constant or not? Then look. The energy plot shows kinetic and spring energy swapping back and forth: $\frac12mv^2$ is largest exactly when $\frac12kx^2$ is zero.
''')
B.code(r'''
lab('physics', exp='osc', F0=0, c=0, x0=1, k=25, m=1)
''')
B.md(r'''
### 4 · What comes next
**Week 3** uses the chain rule in three new ways: on equations that are not solved for $y$ (*implicit differentiation*), on quantities that change together in time (*related rates*), and to solve equations by sliding down tangents (*Newton's method* — the algorithm inside the Voltaic circuit simulator).
''')

if __name__ == '__main__':
    B.write()
