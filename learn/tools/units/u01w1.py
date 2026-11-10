"""Unit 1 · Week 1 - Functions, radians and the unit circle (built from first principles)."""
import math
from nbkit import Book
import figs_u01 as F

B = Book('u01w1', 'Unit 1 · Week 1 — Functions, radians and the unit circle', 'year1/u01w1-functions-radians-circle.ipynb')
S1, S2, S3 = '1 Functions', '2 Angles and radians', '3 Trigonometry on the unit circle'

B.md(r'''
# Unit 1 · Week 1 — Functions, radians and the unit circle
*Term 1, week 1 of 12 · about 15 hours in this notebook and on paper*

**Where you are.** Your diagnostic showed solid algebra and weak trigonometry. Calculus is built on three ideas — *function*, *angle measured in radians*, and *sine and cosine as coordinates on a circle*. This week builds all three **from the ground up**. Nothing is assumed beyond school algebra (expanding brackets, solving a linear equation, square roots), and no step is left for you to guess.

**What you will be able to do at the end of the week**
1. Read and use function notation; find domains and ranges; compose and invert functions; move a graph around by changing its formula.
2. Explain what a radian *is*, convert between degrees and radians, and compute arc lengths, sector areas and rim speeds.
3. Prove Pythagoras' theorem, and *derive* (not memorise) the sine and cosine of 30°, 45° and 60°.
4. Find $\sin$, $\cos$ and $\tan$ of any multiple of $\frac{\pi}{6}$ or $\frac{\pi}{4}$ with the unit circle, and solve equations such as $\sin\theta=\tfrac12$.
''')

B.md(r'''
## How this notebook works

Every topic follows the same six steps. Do them in order.

| Step | What it is | What you do |
|---|---|---|
| **Why** | The question that makes the idea necessary | Read |
| **Build** | The idea is constructed in small numbered steps, each with its reason | Read with a pencil: copy each step on paper and make sure you can say *why* it is allowed |
| **Worked example** | Every line of a calculation | Cover the solution, try it, then compare line by line |
| **Check yourself** | A one-step question, `ask(n, ...)` | Answer straight away. Unlimited tries, not graded; you get the reasoning back |
| **Experiment** | A small simulation in Python | **Write down a prediction first**, then run, then explain any difference |
| **Problems** | Graded set at the end, `check(n, ...)` | Paper first. Your **first** attempt is recorded |

**The tools**

| You type | What happens |
|---|---|
| `ask(3, 0.5)` | checks "Check yourself 3" and explains the answer |
| `check(7, 3*pi/4)` | marks Problem 7 (first attempt counts) |
| `hint(7)` | one more hint for Problem 7 each time you call it |
| `solution(7)` | the full worked solution (after you have attempted it) |
| `mistake(7, 'forgot the sign in quadrant II')` | adds a line to your error log; `mistakes()` shows the log |
| `report()` | your progress in this notebook |

**Typing answers.** Numbers can be exact: `3*pi/4`, `sqrt(3)/2`, `-1/2`. Lists use square brackets: `[pi/6, 5*pi/6]`. Formulas are written as text: `'x**2 + 1'` (`**` means "to the power"). Angles are in **radians** unless a question says degrees.

**To run a cell**: click it and press **Shift + Enter**. Run the grey *SETUP* cell just below first — every time you open the notebook.

**Pace.** Part 1 ≈ 4 h · Part 2 ≈ 3 h · Part 3 ≈ 6 h · problems ≈ 2 h. A week is *done* when `report()` shows at least 80 % of the problems correct at the first attempt.
''')

# =====================================================================================
# PART 1 - FUNCTIONS
# =====================================================================================
B.md(r'''
---
# Part 1 — Functions

## 1.1 What a function is

**Why.** Almost every sentence in engineering says that one quantity *depends on* another: the height of a ball depends on the time, the current in a wire depends on the voltage, the price of an order depends on the quantity. Mathematics needs one precise word for "depends on". That word is *function*.

**Build.**

**Step 1 — the machine picture.** A function is a rule that takes an **input** and returns **exactly one output**. Think of a machine: you drop a number in, one number comes out. The same input always gives the same output.
''')
B.fig('machine', F.machine, 'A function as a machine: this one squares its input and then adds 1.')
B.md(r'''
**Step 2 — the notation.** We give the machine a name, usually $f$. We write

$$f(x)=x^2+1 .$$

Read this as: "*$f$ of $x$ equals $x$ squared plus one*". Three things about this notation trip people up, so let us be exact.

- $f(x)$ does **not** mean "$f$ times $x$". The brackets here mean "the output of $f$ when the input is $x$".
- The letter $x$ is only a **placeholder** — an empty box. The rule is really $f(\square)=\square^2+1$. Whatever you put in the box on the left goes into **every** box on the right.
- So $f(3)$ means: put $3$ in every box.

**Step 3 — using the rule.** With $f(x)=x^2+1$:

$$\begin{aligned}
f(3)&=3^2+1=9+1=10\\[2pt]
f(-2)&=(-2)^2+1=4+1=5 &&\text{(the whole of $-2$ is squared, so the result is $+4$)}\\[2pt]
f(a)&=a^2+1 &&\text{(a letter can go in the box too)}\\[2pt]
f(a+1)&=(a+1)^2+1 &&\text{(all of $a+1$ goes in the box — use brackets)}\\
&=(a^2+2a+1)+1 &&\text{(expand: $(a+1)^2=a^2+2a+1$)}\\
&=a^2+2a+2 .
\end{aligned}$$

The commonest mistake of all is in the fourth line: writing $f(a+1)=a^2+1+1$. The input is $a+1$, so it is $a+1$ that is squared — not $a$.

**Step 4 — the same thing in Python.** A Python function *is* a mathematical function: `def` names the machine, the bracket holds the placeholder, `return` gives the output. Run the cell.
''')
B.code(r'''
def f(u):                 # u is the placeholder (any name works)
    return u**2 + 1       # ** means "to the power"

print('f(3)  =', f(3))
print('f(-2) =', f(-2))
print('f(0.5) =', f(0.5))
''')
B.ask(r'''Let $g(x)=x^2-3x$. Work out $g(-2)$ on paper.''', 'num', 10,
      r'''Put $-2$ in **both** boxes: $g(-2)=(-2)^2-3\cdot(-2)=4+6=10$. Two sign traps: $(-2)^2=+4$, and $-3\cdot(-2)=+6$.''',
      r'''Write $g(\square)=\square^2-3\,\square$ and put $(-2)$, *with its brackets*, into both boxes.''')
B.ask(r'''With $f(x)=x^2+1$, expand $f(2a)$ into a formula in $a$.''', 'sym', '4*a**2 + 1',
      r'''The whole input $2a$ is squared: $f(2a)=(2a)^2+1=4a^2+1$. (Not $2a^2+1$: the 2 is squared as well.)''',
      r'''The input is $2a$. Put $(2a)$ in the box: $(2a)^2+1$. What is $(2a)^2$?''', fmt=r"a formula in `a` as text, e.g. `'3*a**2 - 1'`")

B.md(r'''
## 1.2 Domain and range

**Why.** Not every input is allowed. The machine $\frac{1}{x}$ jams at $x=0$. Before you use a formula you must know which inputs make sense.

**Definitions.**
- The **domain** of $f$ is the set of all inputs for which the rule gives an answer.
- The **range** of $f$ is the set of all outputs that actually come out.

**Notation for intervals.** $[a,b]$ means all numbers from $a$ to $b$ **including** the ends; $(a,b)$ means **excluding** the ends. A mixture is allowed: $[0,5)$ is $0\le x<5$. The symbol $\infty$ always gets a round bracket, because it is not a number you can reach: $[2,\infty)$ means $x\ge 2$.

**Build — the three things that can go wrong (for real numbers).** With the functions you know so far there are exactly three ways for a formula to fail:

| Trap | Rule | Because |
|---|---|---|
| division | the denominator must **not be $0$** | $\frac{1}{0}$ is not defined: no number times $0$ gives $1$ |
| even root ($\sqrt{\ }$) | what is under the root must be **$\ge 0$** | a real number squared is never negative |
| logarithm | what is inside the log must be **$>0$** | $e^{y}$ is always positive, so it never equals $0$ or a negative number |

So the recipe for a domain is: **look for these three traps, write down the condition for each, and solve the conditions.**

**Worked example A.** Find the domain of $g(x)=\dfrac{x+1}{x-2}$.

1. Trap: a division. Condition: the denominator is not zero, $x-2\ne 0$.
2. Solve: $x\ne 2$.
3. Domain: all real numbers except $2$.

**Worked example B.** Find the domain and the range of $f(x)=\sqrt{9-x^2}$.

*Domain.*
1. Trap: a square root. Condition: $9-x^2\ge 0$.
2. Add $x^2$ to both sides: $9\ge x^2$, that is $x^2\le 9$.
3. Which numbers have a square of at most $9$? Those between $-3$ and $3$: $\;-3\le x\le 3$. (Test: $x=2$ gives $4\le9$ ✓; $x=-4$ gives $16\le 9$ ✗.)
4. Domain: $[-3,\,3]$.

*Range.* Ask: how small and how large can the output get?
1. A square root is never negative, so the output is $\ge 0$. It equals $0$ when $9-x^2=0$, i.e. at $x=\pm3$. So the smallest output is $0$.
2. The output is largest when the thing under the root is largest. $9-x^2$ is largest when $x^2$ is smallest, i.e. $x=0$, giving $\sqrt{9}=3$.
3. Every value between $0$ and $3$ is reached somewhere in between. Range: $[0,\,3]$.
''')
B.fig('domain_range', F.domain_range, r'The graph of √(9 − x²). Its shadow on the x-axis is the domain; its shadow on the y-axis is the range.')
B.md(r'''
**Worked example C.** Find the domain of $h(x)=\ln(x-1)$.

1. Trap: a logarithm. Condition: $x-1>0$.
2. Solve: $x>1$. Domain: $(1,\infty)$.

**Worked example D — two traps at once.** $k(x)=\dfrac{1}{\sqrt{x-4}}$.

1. Root: $x-4\ge 0$, so $x\ge 4$.
2. Division: $\sqrt{x-4}\ne 0$, so $x\ne 4$.
3. Both must hold: $x>4$. Domain: $(4,\infty)$.
''')
B.ask(r'''What is the **smallest** number in the domain of $f(x)=\sqrt{2x-6}$?''', 'num', 3,
      r'''Root trap: $2x-6\ge0$. Add 6: $2x\ge 6$. Divide by 2: $x\ge 3$. The domain is $[3,\infty)$, whose smallest member is $3$.''',
      r'''Which trap is present? Write its condition ($\ldots\ge 0$) and solve it for $x$.''')
B.ask(r'''Which inputs are **not** allowed in $h(x)=\dfrac{x+1}{x^2-4}$? Give both numbers.''', 'set', [-2, 2],
      r'''Division trap: $x^2-4\ne0$. Now $x^2-4=0$ means $x^2=4$, so $x=2$ or $x=-2$. Both make the denominator zero, so both are excluded. (Do not forget the negative root!)''',
      r'''Set the denominator equal to zero and solve. An equation $x^2=\text{number}$ has **two** solutions.''')

B.md(r'''
## 1.3 The graph of a function

**Why.** A formula is exact but blind; a picture lets you *see* behaviour — where the function rises, where it is zero, where it is largest.

**Build.**

**Step 1.** Take an input $x$, compute the output $f(x)$, and mark the point with coordinates $(x,\,f(x))$: go $x$ sideways, $f(x)$ up.

**Step 2.** Do that for *every* $x$ in the domain. The collection of all those points is the **graph**. In practice we compute a table of values and join the dots — which is exactly what a computer plot does, with a few hundred dots.

**Step 3 — the vertical-line test.** A function gives *one* output per input. So a vertical line (one fixed $x$) can cut the graph of a function **at most once**. A circle is therefore *not* the graph of a function: the vertical line $x=0$ cuts $x^2+y^2=9$ at $y=3$ **and** $y=-3$. That is why the function in Example B was only the *upper* half of the circle.

### Experiment 1 — a graph is a table with the dots joined
**Predict first (on paper):** for $f(x)=x^2-2x-3$, fill in the table for $x=-2,-1,0,1,2,3,4$. Where does the graph cross the $x$-axis? Where is its lowest point? *Then* run the cell and compare.
''')
B.code(r'''
def f(u):
    return u**2 - 2*u - 3

xs_table = [-2, -1, 0, 1, 2, 3, 4]
table(['x', 'f(x)'], [[v, f(v)] for v in xs_table])

xs = np.linspace(-2.5, 4.5, 300)          # 300 inputs between -2.5 and 4.5
plt.plot(xs, f(xs), label='f(x) = x² − 2x − 3')
plt.plot(xs_table, [f(v) for v in xs_table], 'o', label='the points of your table')
plt.axhline(0, color='k', lw=0.8); plt.legend(); plt.xlabel('x'); plt.show()
''')
B.md(r'''
*Explain:* the graph crosses the $x$-axis where the output is zero, at $x=-1$ and $x=3$. Its lowest point is halfway between them, at $x=1$. In §1.8 you will see how to find that lowest point from the formula alone.

## 1.4 Composition — one function after another

**Why.** Real formulas are built in layers. To compute $\sqrt{x^2+1}$ you first compute $x^2+1$, *then* take the root. Recognising the layers is the key to the chain rule in Unit 2, so it pays to be fluent now.

**Build.**

**Step 1.** Take two machines $f$ and $g$. Feed the output of $g$ into $f$. The combined machine is written $f(g(x))$, or $(f\circ g)(x)$, and read "*$f$ of $g$ of $x$*".

**Step 2 — work from the inside out.** In $f(g(x))$ the *inner* function $g$ acts first, the *outer* function $f$ acts second — just as with ordinary brackets.

**Worked example.** Let $f(x)=2x+1$ and $g(x)=x^2$.

$$\begin{aligned}
f(g(3)):&\quad g(3)=3^2=9,\quad\text{then } f(9)=2\cdot 9+1=19.\\
g(f(3)):&\quad f(3)=2\cdot3+1=7,\quad\text{then } g(7)=7^2=49.
\end{aligned}$$

Different results: **the order matters**. (Putting on socks then shoes is not the same as shoes then socks.)

**Step 3 — as formulas.** Put the whole inner formula into the box of the outer one:

$$\begin{aligned}
f(g(x))&=f(x^2)=2\,(x^2)+1=2x^2+1,\\
g(f(x))&=g(2x+1)=(2x+1)^2=4x^2+4x+1 .
\end{aligned}$$

Check with $x=3$: $2\cdot9+1=19$ ✓ and $36+12+1=49$ ✓.

**Step 4 — taking a formula apart.** You will need the reverse skill more often: *see* a formula as outer(inner).

| Formula | inner $g(x)$ (done first) | outer $f(u)$ (done last) |
|---|---|---|
| $\sqrt{x^2+1}$ | $x^2+1$ | $\sqrt{u}$ |
| $\sin(3t)$ | $3t$ | $\sin u$ |
| $(5x-2)^4$ | $5x-2$ | $u^4$ |
| $e^{-x^2}$ | $-x^2$ | $e^{u}$ |

Tip: the **outer** function is the *last* button you would press on a calculator.
''')
B.ask(r'''Let $f(x)=x+2$ and $g(x)=3x$. Compute $f(g(4))$.''', 'num', 14,
      r'''Inside first: $g(4)=3\cdot4=12$. Then $f(12)=12+2=14$. (The other order gives $g(f(4))=g(6)=18$ — different.)''',
      r'''Start with the inner function: what is $g(4)$? Then feed that number into $f$.''')
B.ask(r'''In $y=\ln(x^2+4)$, which is the **outer** function?  (a) $x^2+4$  (b) $\ln u$  (c) $x^2$''', 'choice', 'b',
      r'''To compute it you first work out $x^2+4$ and press $\ln$ **last**. The last operation is the outer function: $\ln u$ with $u=x^2+4$ inside.''',
      r'''Imagine computing it for $x=1$ on a calculator. Which button do you press last?''')

B.md(r'''
## 1.5 Inverse functions — undoing

**Why.** If a function turns temperature in °C into °F, you will want the machine that goes back. If $\sin$ turns an angle into a ratio, you will want to get the angle back from the ratio (that will be $\arcsin$, next week). Undoing is the job of the **inverse function**.

**Build.**

**Step 1 — what "undo" means.** The inverse of $f$, written $f^{-1}$, takes each output of $f$ back to the input it came from:

$$\text{if } f(a)=b \quad\text{then}\quad f^{-1}(b)=a .$$

Doing $f$ and then $f^{-1}$ returns you to where you started: $f^{-1}(f(x))=x$.

> **Warning about notation.** $f^{-1}(x)$ is **not** $\dfrac{1}{f(x)}$. The "$-1$" here means "inverse machine", not "one over".

**Step 2 — undo the steps in reverse order.** Take $f(x)=2x-1$: "*double, then subtract 1*". To undo it, reverse the steps and do the opposite of each: "*add 1, then halve*". So $f^{-1}(x)=\dfrac{x+1}{2}$. (Shoes off first, then socks.)

**Step 3 — the general method: solve for the input.** For harder formulas you cannot see the steps, but you can always do this:

1. Write $y=f(x)$.
2. **Solve that equation for $x$** (get $x$ alone on one side). The result is $x=f^{-1}(y)$.
3. If you like, rename $y$ to $x$ at the end, to write the inverse as a function of $x$.

**Worked example 1.** $f(x)=2x-1$.

$$\begin{aligned}
y&=2x-1\\
y+1&=2x &&\text{(add 1 to both sides)}\\
\frac{y+1}{2}&=x &&\text{(divide both sides by 2)}
\end{aligned}$$

So $f^{-1}(y)=\dfrac{y+1}{2}$, the same as we found by reversing the steps. **Check** with a number: $f(2)=3$, and $f^{-1}(3)=\frac{3+1}{2}=2$ ✓.

**Worked example 2 (the one from your diagnostic).** $f(x)=\dfrac{2x+3}{x-1}$. Find $f^{-1}(5)$.

$$\begin{aligned}
y&=\frac{2x+3}{x-1}\\[3pt]
y\,(x-1)&=2x+3 &&\text{(multiply both sides by $x-1$ to clear the fraction)}\\
yx-y&=2x+3 &&\text{(expand the bracket)}\\
yx-2x&=y+3 &&\text{(collect every term with $x$ on the left, the rest on the right)}\\
x\,(y-2)&=y+3 &&\text{(factor $x$ out)}\\
x&=\frac{y+3}{y-2} &&\text{(divide by $y-2$)}
\end{aligned}$$

So $f^{-1}(y)=\dfrac{y+3}{y-2}$ and $f^{-1}(5)=\dfrac{5+3}{5-2}=\dfrac{8}{3}$.

**Check** by putting it back into $f$: $f\!\left(\tfrac83\right)=\dfrac{\frac{16}{3}+3}{\frac83-1}=\dfrac{\frac{25}{3}}{\frac{5}{3}}=5$ ✓.

*Shortcut when you only need one value:* to find $f^{-1}(5)$ you may simply solve $f(x)=5$. It is the same equation with $y=5$.

**Step 4 — when does an inverse exist?** The inverse must send each output back to *one* input. That fails if two different inputs give the same output. Example: $f(x)=x^2$ gives $f(2)=4$ and $f(-2)=4$. Asked to undo $4$, should the inverse answer $2$ or $-2$? It cannot decide, so $x^2$ has **no inverse on its whole domain**.

A function that never repeats an output is called **one-to-one**. On a graph: every *horizontal* line cuts it at most once (the horizontal-line test).

**The standard repair: restrict the domain.** Keep only $x\ge0$. On that half, $x^2$ is one-to-one and its inverse is $\sqrt{x}$. That is why $\sqrt{4}$ means $2$ and not $-2$: the square root is *defined* as the inverse of the restricted squaring function. Remember this repair — next week $\arcsin$, $\arccos$ and $\arctan$ are built in exactly the same way.

**Step 5 — the graph of an inverse.** If the point $(a,b)$ is on the graph of $f$ (meaning $f(a)=b$), then $f^{-1}(b)=a$, so the point $(b,a)$ is on the graph of $f^{-1}$. Swapping the two coordinates of every point is the same as **mirroring in the line $y=x$**.
''')
B.fig('inverse_reflect', F.inverse_reflect, 'A function and its inverse are mirror images in the line y = x: the point (2, 3) becomes (3, 2).')
B.ask(r'''Let $f(x)=\dfrac{x-4}{5}$. Find $f^{-1}(2)$.''', 'num', 14,
      r'''Solve $f(x)=2$: $\dfrac{x-4}{5}=2\Rightarrow x-4=10\Rightarrow x=14$. Or reverse the steps: $f$ is "subtract 4, divide by 5", so the inverse is "multiply by 5, add 4": $2\cdot5+4=14$.''',
      r'''$f^{-1}(2)$ is the input that produces the output 2. Solve $\dfrac{x-4}{5}=2$.''')
B.ask(r'''Which of these has an inverse on **all** real numbers?  (a) $x^2$  (b) $x^3$  (c) $x^4$''', 'choice', 'b',
      r'''$x^3$ never repeats an output: different inputs always give different cubes (and negative inputs give negative outputs). $x^2$ and $x^4$ give the same output for $x$ and $-x$, so they fail the horizontal-line test.''',
      r'''Test each with the pair of inputs $2$ and $-2$. Do they give the same output?''')

B.md(r'''
## 1.6 Transformations — moving a graph by changing its formula

**Why.** Every sine wave in an AC circuit is the *same* basic curve, shifted and stretched. If you know how a change in the formula moves the graph, you need to remember only a handful of basic shapes.

**Build.** Start with any function $y=f(x)$. There are two places to make a change: **outside** $f$ (after it has done its work) or **inside** (before it gets the input).

**Step 1 — changes outside act on the output: vertical, and exactly as you expect.**

- $y=f(x)+b$: every output gets $b$ added → every point moves **up** by $b$.
- $y=c\,f(x)$: every output is multiplied by $c$ → the graph is **stretched vertically** by the factor $c$ (and flipped upside down if $c<0$).

Nothing surprising here: the output *is* the height.

**Step 2 — changes inside act on the input: horizontal, and "backwards".** This is the one that needs an argument. Compare $f(x)=x^2$ with $g(x)=f(x-2)=(x-2)^2$ in a table:

| $x$ | $-1$ | $0$ | $1$ | $2$ | $3$ | $4$ |
|---|---|---|---|---|---|---|
| $f(x)=x^2$ | $1$ | $\mathbf{0}$ | $1$ | $4$ | $9$ | $16$ |
| $g(x)=(x-2)^2$ | $9$ | $4$ | $1$ | $\mathbf{0}$ | $1$ | $4$ |

The row of $g$ is the row of $f$ slid **two places to the right**: $f$ has its zero at $x=0$, $g$ has it at $x=2$.

*Why right, when the formula says minus?* Ask: "for which $x$ does $g$ produce what $f$ produced at $0$?" We need the inside of $g$ to be $0$: $x-2=0$, so $x=2$. In general $g$ needs an input that is **2 larger** to do what $f$ already did. Every feature of the graph therefore appears 2 units later, i.e. further right.
''')
B.fig('shift_right', F.shift_right, 'Replacing x by x − 2 moves every point 2 units to the right.')
B.md(r'''
**Step 3 — the same argument for a factor inside.** Let $g(x)=f(2x)$. For which $x$ does $g$ produce what $f$ produced at $6$? We need $2x=6$, so $x=3$ — **half** as far out. Everything happens at half the distance: the graph is **compressed horizontally by the factor 2**.

**Step 4 — mirror images.** $y=-f(x)$ changes the sign of every output: mirror in the $x$-axis. $y=f(-x)$ uses the input from the other side: mirror in the $y$-axis.

**Summary.**

| New formula | What happens to the graph of $y=f(x)$ | Kind |
|---|---|---|
| $f(x)+b$ | up by $b$ | outside → vertical, as expected |
| $c\,f(x)$ | stretched vertically by $c$ | outside → vertical, as expected |
| $-f(x)$ | mirrored in the $x$-axis | outside |
| $f(x-a)$ | **right** by $a$ | inside → horizontal, backwards |
| $f(kx)$ | **compressed** horizontally by $k$ | inside → horizontal, backwards |
| $f(-x)$ | mirrored in the $y$-axis | inside |

**Worked example.** Where is the lowest point of $y=(x-3)^2+4$?

1. Basic shape: $y=x^2$, lowest point at $(0,0)$.
2. Inside change $x\to x-3$: right by 3. The lowest point is now at $(3,0)$.
3. Outside change $+4$: up by 4. The lowest point is at $(3,4)$.

### Experiment 2 — transformations with sliders
The cell plots $y=c\cdot f\big(k\,(x-a)\big)+b$ for $f(x)=x^3-x$ (grey: the original).

**Predict first:** what will the graph do when you (1) set $a=1$; (2) set $b=-2$; (3) set $c=-1$; (4) set $k=2$? Write your four predictions down, *then* move the sliders one at a time.
''')
B.code(r'''
def base(u):
    return u**3 - u                     # try also:  np.abs(u)   or   u**2

def show(a=0.0, b=0.0, c=1.0, k=1.0):
    xs = np.linspace(-3, 3, 600)
    plt.figure(figsize=(7, 4.2))
    plt.plot(xs, base(xs), color='0.7', label='y = f(x)')
    plt.plot(xs, c * base(k * (xs - a)) + b, label='y = c·f(k(x − a)) + b')
    plt.axhline(0, color='k', lw=0.8); plt.axvline(0, color='k', lw=0.8)
    plt.ylim(-4, 4); plt.legend(loc='upper left'); plt.show()

explore(show, a=(-2, 2, 0.5, 0), b=(-3, 3, 0.5, 0), c=(-2, 2, 0.5, 1), k=(0.5, 3, 0.5, 1))
''')
B.ask(r'''The graph of $y=\sqrt{x}$ is moved **3 to the left** and **2 down**. What is the value of the new function at $x=1$?''', 'num', 0,
      r'''Left by 3 is an inside change, and inside changes are backwards: $x\to x+3$. Down by 2 is an outside change: $-2$. New function: $y=\sqrt{x+3}-2$. At $x=1$: $\sqrt{4}-2=0$.''',
      r'''"Left by 3" replaces $x$ by $x+3$ (backwards!). "Down by 2" subtracts 2 from the output. Write the new formula, then put in $x=1$.''')
B.ask(r'''The point $(4,\,5)$ lies on $y=f(x)$. Which $x$-coordinate has the corresponding point on $y=f(2x)$?''', 'num', 2,
      r'''We need the inside to equal 4: $2x=4$, so $x=2$. The point is $(2,5)$: same height, half as far out. The graph is compressed by the factor 2.''',
      r'''Ask: for which $x$ is the *inside*, $2x$, equal to 4?''')

B.md(r'''
## 1.7 Even and odd functions

**Why.** Symmetry halves the work, and $\cos$ and $\sin$ will turn out to be the standard examples of the two kinds.

**Definitions.**
- $f$ is **even** if $f(-x)=f(x)$ for every $x$: opposite inputs give the *same* output. The graph is its own mirror image in the $y$-axis. Example: $x^2$.
- $f$ is **odd** if $f(-x)=-f(x)$ for every $x$: opposite inputs give *opposite* outputs. The graph is unchanged by a half-turn about the origin. Example: $x^3$.
- Most functions are **neither**.

**The test.** Replace $x$ by $(-x)$ everywhere, simplify, and compare with the original.

**Worked example 1.** $f(x)=x^3-x$.
$$f(-x)=(-x)^3-(-x)=-x^3+x=-(x^3-x)=-f(x)\quad\Rightarrow\quad\text{odd.}$$
(Here $(-x)^3=(-x)(-x)(-x)=-x^3$: an odd number of minus signs leaves one minus.)

**Worked example 2.** $f(x)=x^4-3x^2$.
$$f(-x)=(-x)^4-3(-x)^2=x^4-3x^2=f(x)\quad\Rightarrow\quad\text{even.}$$
(An even number of minus signs cancel.)

**Worked example 3.** $f(x)=x^3+1$.
$$f(-x)=-x^3+1 .$$
That is neither $f(x)=x^3+1$ nor $-f(x)=-x^3-1$. **Neither.**

This is where the names come from: even powers of $x$ give even functions, odd powers give odd functions.
''')
B.ask(r'''Is $f(x)=x^5-4x$ (a) even, (b) odd, or (c) neither?''', 'choice', 'b',
      r'''$f(-x)=(-x)^5-4(-x)=-x^5+4x=-(x^5-4x)=-f(x)$. Odd. (Only odd powers of $x$ appear.)''',
      r'''Compute $f(-x)$: replace every $x$ by $(-x)$ and simplify the signs.''')

B.md(r'''
## 1.8 Completing the square

**Why.** In Experiment 1 the parabola had a lowest point, and in §1.6 you read the lowest point of $(x-3)^2+4$ straight off the formula. *Completing the square* rewrites **any** quadratic in that readable form. You will use it again for integrals and for circles.

**Build.**

**Step 1 — the pattern we are aiming for.** Expand a squared bracket:
$$(x+p)^2=(x+p)(x+p)=x^2+px+px+p^2=x^2+2px+p^2 .$$
Notice: the number in front of $x$ is $2p$ — **twice** the number in the bracket.

**Step 2 — run it backwards.** Given $x^2+bx$, choose $p$ to be **half of $b$**. Then $(x+\tfrac b2)^2=x^2+bx+(\tfrac b2)^2$. That is what we want *plus an extra* $(\tfrac b2)^2$, so subtract the extra:

$$\boxed{\,x^2+bx=\left(x+\frac b2\right)^2-\left(\frac b2\right)^2\,}$$

In words: **halve the coefficient of $x$, put it in the bracket, subtract its square.**

**Worked example 1.** $x^2-4x+7$.
$$\begin{aligned}
x^2-4x+7&=\underbrace{(x-2)^2-4}_{x^2-4x}+7 &&\text{(half of $-4$ is $-2$; subtract $(-2)^2=4$)}\\
&=(x-2)^2+3 .
\end{aligned}$$
Now read it. A square is never negative, so $(x-2)^2\ge0$, with equality only when $x=2$. Hence the smallest value of the whole expression is $0+3=3$, reached at $x=2$. In the language of §1.6: the parabola $x^2$ moved right 2 and up 3.

**Check** by expanding back: $(x-2)^2+3=x^2-4x+4+3=x^2-4x+7$ ✓. *Always do this check — it takes ten seconds.*

**Worked example 2 — a number in front of $x^2$.** $2x^2+12x+5$. First take the 2 outside the terms with $x$:
$$\begin{aligned}
2x^2+12x+5&=2\,(x^2+6x)+5\\
&=2\,\big[(x+3)^2-9\big]+5 &&\text{(half of 6 is 3; subtract $3^2=9$)}\\
&=2(x+3)^2-18+5 &&\text{(the 2 multiplies the $-9$ as well!)}\\
&=2(x+3)^2-13 .
\end{aligned}$$
Lowest value $-13$, at $x=-3$.
''')
B.ask(r'''Complete the square for $x^2+6x+10$. What is its minimum value?''', 'num', 1,
      r'''Half of 6 is 3, and $3^2=9$: $x^2+6x+10=(x+3)^2-9+10=(x+3)^2+1$. The square is at least 0, so the minimum is $1$ (at $x=-3$).''',
      r'''Halve the 6, put it in the bracket, subtract its square: $(x+3)^2-9+10$. Then use "a square is never negative".''')

# =====================================================================================
# PART 2 - ANGLES AND RADIANS
# =====================================================================================
B.md(r'''
---
# Part 2 — Angles and radians

## 2.1 What does it mean to measure an angle?

**Why.** You learned angles in degrees. Calculus, physics and every programming language use **radians**. This part shows that the radian is not an arbitrary new unit to memorise: it is *the* natural way to measure an angle, and the famous $2\pi$ falls out by itself.

**Build.**

**Step 1 — degrees are a historical accident.** A full turn is $360^\circ$ because the Babylonians liked the number 360 (it has many divisors and is close to the number of days in a year). Nothing in geometry forces 360. We could have chosen 100 or 400 (the "gradian" on your calculator does exactly that).

**Step 2 — what we want instead.** A measure of "how far open" an angle is that comes from the geometry itself, with no arbitrary number in it. The natural object to use is a circle around the corner of the angle: a wider angle cuts off a longer piece of the circle. We will measure the angle by that piece — but first we need one fact about circles.

## 2.2 The number π

**Step 1 — all circles have the same shape.** Any circle is a scaled copy of any other. When you scale a figure, *all* its lengths are multiplied by the same factor. So if you double a circle's diameter, its circumference doubles too.

**Step 2 — therefore the ratio is a constant.** Because circumference and diameter always scale together,
$$\frac{\text{circumference}}{\text{diameter}}$$
is the **same number for every circle**. That number is called $\pi$. This is the *definition* of $\pi$; it is about $3.14159$.

**Step 3 — the formula.** With $C$ for circumference, $d$ for diameter and $r$ for radius ($d=2r$):
$$\frac{C}{d}=\pi\quad\Rightarrow\quad C=\pi d=2\pi r .$$

### Experiment 3 — computing π from Pythagoras alone (optional, 20 min)
How do we know $\pi\approx3.14159$? Archimedes' idea: a regular polygon with many sides drawn inside a circle of radius 1 is almost the circle, so half its perimeter is almost $\pi$.

Start with a hexagon: it is six equilateral triangles, so each side is $s_6=1$ and the perimeter is 6, giving $\pi\approx 3$. Now double the number of sides again and again. Two applications of Pythagoras (try to find them — draw one side, the radius to its midpoint, and the new shorter sides) give the new side length from the old one:
$$s_{2n}=\sqrt{\,2-\sqrt{4-s_n^{\,2}}\,}.$$
**Predict:** how many sides do you need for 3.14? Then run.
''')
B.code(r'''
n_sides, s = 6, 1.0
rows = []
for step in range(10):
    rows.append([n_sides, s, n_sides * s / 2])
    s = math.sqrt(2 - math.sqrt(4 - s**2))     # side length after doubling the number of sides
    n_sides = 2 * n_sides
table(['sides', 'side length', 'half perimeter ≈ π'], rows, fmt='%.8f')
print('\nmath.pi =', math.pi)
''')
B.md(r'''
*Explain:* with 96 sides (as far as Archimedes went, by hand, around 250 BC) you already have $3.14$. Each doubling roughly quarters the error.

## 2.3 The radian

**Build.**

**Step 1 — the key observation.** Draw an angle and three circles of radius 1, 2, 3 around its corner. The angle cuts an arc out of each.
''')
B.fig('same_angle_circles', F.same_angle_circles, 'One angle, three circles. The arcs are scaled copies of each other.')
B.md(r'''
The three "pie slices" are scaled copies of one another. Scaling multiplies every length by the same factor, so the arc on the circle of radius 2 is twice as long as on the circle of radius 1, and on radius 3 it is three times as long:
$$\frac{s_1}{1}=\frac{s_2}{2}=\frac{s_3}{3}.$$
**The ratio arc ÷ radius does not depend on which circle you drew. It depends only on the angle.**

**Step 2 — the definition.** A number that depends only on the angle is exactly what we were looking for. So we *define*:

$$\boxed{\;\theta=\frac{s}{r}\;}\qquad\text{angle in radians}=\frac{\text{arc length}}{\text{radius}} .$$

**Step 3 — what one radian looks like.** $\theta=1$ means $s=r$: the arc is exactly as long as the radius. Take a piece of string as long as the radius and lay it along the circle — the angle it covers is one radian (about $57.3^\circ$, as you will see in a moment).
''')
B.fig('radian_def', F.radian_def, 'Left: one radian. Right: the general definition.')
B.md(r'''
**Step 4 — a full turn.** For a full turn the arc is the whole circumference, $s=2\pi r$ (§2.2). So
$$\theta_{\text{full turn}}=\frac{2\pi r}{r}=2\pi .$$
The radius cancels, as it must. **That is where every $2\pi$ in physics and engineering comes from: it is one full turn.** Consequently:

| Turn | full | half | quarter | sixth | eighth | twelfth |
|---|---|---|---|---|---|---|
| radians | $2\pi$ | $\pi$ | $\dfrac{\pi}{2}$ | $\dfrac{\pi}{3}$ | $\dfrac{\pi}{4}$ | $\dfrac{\pi}{6}$ |
| degrees | $360^\circ$ | $180^\circ$ | $90^\circ$ | $60^\circ$ | $45^\circ$ | $30^\circ$ |

**Step 5 — a radian has no unit.** $\theta=s/r$ is a length divided by a length: metres cancel. An angle in radians is a pure number. (We write "rad" only as a reminder.) This is the deep reason calculus prefers radians, and you will meet it again in §3.11.

## 2.4 Converting between degrees and radians

**Build.** You need only **one** fact, from the table above:
$$180^\circ=\pi\ \text{rad}.$$
Divide both sides by 180: $\;1^\circ=\dfrac{\pi}{180}$ rad. Divide both sides by $\pi$ instead: $\;1\text{ rad}=\dfrac{180^\circ}{\pi}\approx57.3^\circ$. Hence

$$\text{degrees}\to\text{radians: multiply by }\frac{\pi}{180},\qquad \text{radians}\to\text{degrees: multiply by }\frac{180}{\pi}.$$

*How not to mix them up:* radians are the "small numbers" ($180$ becomes about $3.14$), so going to radians must make the number smaller.

**Worked example 1.** $135^\circ$ in radians.
$$135\cdot\frac{\pi}{180}=\frac{135}{180}\,\pi=\frac{3}{4}\,\pi=\frac{3\pi}{4}\qquad\Big(\text{divide top and bottom by }45\Big).$$
*Quicker by thinking in turns:* $135^\circ=3\times45^\circ$ and $45^\circ=\frac{\pi}{4}$, so $135^\circ=\frac{3\pi}{4}$.

**Worked example 2.** $\dfrac{5\pi}{6}$ rad in degrees.
$$\frac{5\pi}{6}\cdot\frac{180^\circ}{\pi}=\frac{5\cdot180^\circ}{6}=5\cdot30^\circ=150^\circ .$$
*Quicker:* replace $\pi$ by $180^\circ$: $\frac{5\cdot180^\circ}{6}=150^\circ$.

**Worked example 3.** $2$ rad in degrees (no $\pi$ in sight — that is allowed, radians are just numbers): $2\cdot\frac{180^\circ}{\pi}\approx114.6^\circ$.

In Python: `radians(135)` and `degrees(5*pi/6)`. **Trap:** `sin`, `cos`, `tan` in Python (and in every other language) expect **radians**. `sin(30)` is *not* $\frac12$.
''')
B.code(r'''
print('135 degrees =', radians(135), 'rad;   3*pi/4 =', 3*pi/4)
print('5*pi/6 rad  =', degrees(5*pi/6), 'degrees')
print()
print('sin(30)          =', sin(30), '   <- 30 RADIANS: wrong if you meant degrees')
print('sin(radians(30)) =', sin(radians(30)), '   <- 30 degrees, converted first')
''')
B.ask(r'''Convert $210^\circ$ to radians.''', 'num', 7 * math.pi / 6,
      r'''$210\cdot\dfrac{\pi}{180}=\dfrac{7\pi}{6}$ (divide 210 and 180 by 30). In turns: $210^\circ=7\times30^\circ=7\cdot\dfrac{\pi}{6}$. Type it as `7*pi/6`.''',
      r'''Multiply by $\dfrac{\pi}{180}$ and simplify the fraction $\dfrac{210}{180}$. You can type the result as `7*pi/6`-style.''', fmt='a number; you can type e.g. `5*pi/3`')
B.ask(r'''Convert $\dfrac{2\pi}{5}$ rad to degrees.''', 'num', 72,
      r'''Replace $\pi$ by $180^\circ$: $\dfrac{2\cdot180^\circ}{5}=72^\circ$.''',
      r'''Replace $\pi$ by $180^\circ$ and work out the fraction.''', fmt='a number of degrees')

B.md(r'''
## 2.5 Arc length and sector area

**Build.**

**Arc length.** Multiply the definition $\theta=\dfrac sr$ by $r$:
$$\boxed{\,s=r\,\theta\,}\qquad(\theta\text{ in radians}).$$
There is nothing to prove — it *is* the definition, rearranged. In degrees the same formula would read $s=r\theta\cdot\frac{\pi}{180}$: the awkward factor is exactly what radians remove.

**Sector area.** A sector is a "pie slice" with angle $\theta$.

1. The whole disc has area $\pi r^2$ (taken as known here; you will *derive* it with an integral in Unit 3).
2. The slice is a fraction of the disc. Which fraction? The same fraction as its angle is of a full turn: $\dfrac{\theta}{2\pi}$.
3. Multiply: $\;A=\dfrac{\theta}{2\pi}\cdot\pi r^2=\dfrac{\theta\, r^2}{2}$.

$$\boxed{\,A=\tfrac12 r^2\theta\,}$$
''')
B.fig('sector', F.sector, 'A sector with angle θ: arc length rθ, area ½r²θ.')
B.md(r'''
**Worked example.** A circle has radius $5$ cm. For an angle of $72^\circ$ find the arc length and the sector area.

1. Convert first — the formulas need radians: $72^\circ=72\cdot\frac{\pi}{180}=\frac{2\pi}{5}\approx1.2566$.
2. Arc: $s=r\theta=5\cdot\frac{2\pi}{5}=2\pi\approx6.28$ cm.
3. Area: $A=\frac12r^2\theta=\frac12\cdot25\cdot\frac{2\pi}{5}=5\pi\approx15.71$ cm².

*Sanity check:* $72^\circ$ is one fifth of a turn; the full circumference is $2\pi\cdot5=31.4$ cm, and a fifth of that is $6.28$ cm ✓.
''')
B.ask(r'''A circle has radius $4$ m. How long is the arc cut off by an angle of $0.75$ rad?''', 'num', 3,
      r'''$s=r\theta=4\cdot0.75=3$ m. The angle is already in radians, so there is nothing to convert.''',
      r'''Use $s=r\theta$. Is the angle already in radians?''', fmt='metres')

B.md(r'''
## 2.6 Rotation: angular velocity and rim speed

**Why.** Motors, wheels, generators and the "rotating arrow" picture of AC all describe turning. This is the first physics formula of the course, and you can derive it yourself.

**Build.**

**Step 1 — angular velocity.** If something turns through an angle $\Delta\theta$ in a time $\Delta t$ (the symbol $\Delta$, "delta", just means "a change in"), its **angular velocity** is
$$\omega=\frac{\Delta\theta}{\Delta t}\qquad\text{in rad/s}.$$
($\omega$ is the Greek letter omega.) It is the rotational twin of speed $=\dfrac{\text{distance}}{\text{time}}$.

**Step 2 — the speed of a point on the rim.** A point at distance $r$ from the axis travels along an arc. When the wheel turns by $\Delta\theta$, the point moves a distance $\Delta s=r\,\Delta\theta$ (that is $s=r\theta$ from §2.5). Its speed is distance over time:
$$v=\frac{\Delta s}{\Delta t}=\frac{r\,\Delta\theta}{\Delta t}=r\,\frac{\Delta\theta}{\Delta t}=r\,\omega .$$

$$\boxed{\,v=\omega r\,}$$

Points further from the axis move faster, although every point shares the same $\omega$.

**Step 3 — from rpm to rad/s.** Machines are rated in revolutions per minute. One revolution is $2\pi$ rad; one minute is 60 s:
$$1\ \text{rpm}=\frac{1\ \text{rev}}{1\ \text{min}}=\frac{2\pi\ \text{rad}}{60\ \text{s}}\qquad\Rightarrow\qquad\omega=\text{rpm}\cdot\frac{2\pi}{60}.$$

**Worked example.** A drill turns at 1500 rpm with a bit of radius 4 mm. How fast does the cutting edge move?

1. $\omega=1500\cdot\dfrac{2\pi}{60}=50\pi\approx157.1$ rad/s.
2. $r=4\text{ mm}=0.004$ m (SI units before you multiply!).
3. $v=\omega r=157.1\cdot0.004\approx0.63$ m/s.

### Experiment 4 — simulate a point on a turning wheel
The simulation steps time forward in small steps, moves a point round a circle, measures how far it travelled, and compares the measured speed with $\omega r$.

**Predict first:** radius 0.3 m, 120 rpm. What rim speed do you expect? If the radius is doubled, what happens to the speed? To the time for one revolution?
''')
B.code(r'''
def wheel(rpm=120, r=0.3):
    omega = rpm * 2 * pi / 60                 # rad/s
    dt = 0.0005                               # time step in seconds
    ts = np.arange(0, 1 + dt, dt)             # one second of motion
    th = omega * ts                           # angle at each instant
    px, py = r * np.cos(th), r * np.sin(th)   # position of the point (Part 3 explains cos and sin)
    travelled = np.sum(np.hypot(np.diff(px), np.diff(py)))   # add up the tiny straight steps
    fig, (a1, a2) = plt.subplots(1, 2, figsize=(9.5, 3.6), gridspec_kw={'width_ratios': [1, 1.7]})
    a1.plot(px, py); a1.set_aspect('equal'); a1.set_title('path of the point')
    show_t = ts <= 4 * pi / omega             # two revolutions
    a2.plot(ts[show_t], px[show_t], label='x(t)'); a2.plot(ts[show_t], py[show_t], label='y(t)')
    a2.set_xlabel('time (s)'); a2.legend(); a2.set_title('its coordinates against time')
    plt.show()
    print(f'omega = {omega:.3f} rad/s      time for one revolution = {2*pi/omega:.4f} s')
    print(f'measured speed (distance in 1 s) = {travelled:.4f} m/s      formula omega*r = {omega*r:.4f} m/s')

explore(wheel, rpm=(30, 300, 30, 120), r=(0.1, 0.6, 0.1, 0.3))
''')
B.md(r'''
*Explain:* the measured speed agrees with $\omega r$ to four figures. Doubling $r$ doubles the speed but leaves the time per revolution unchanged — it depends only on $\omega$. Look at the right-hand plot: the coordinates of a point going round a circle trace **waves**. Those waves are the sine and cosine of Part 3.
''')
B.ask(r'''A motor runs at $300$ rpm. What is its angular velocity in rad/s?''', 'num', 10 * math.pi,
      r'''$\omega=300\cdot\dfrac{2\pi}{60}=10\pi\approx31.4$ rad/s. (300 revolutions per minute is 5 per second, and each is $2\pi$ rad.)''',
      r'''Multiply the rpm by $\dfrac{2\pi}{60}$: each revolution is $2\pi$ rad, each minute is 60 s.''', fmt='rad/s')

# =====================================================================================
# PART 3 - TRIGONOMETRY
# =====================================================================================
B.md(r'''
---
# Part 3 — Trigonometry on the unit circle

## 3.1 Sine, cosine and tangent in a right-angled triangle

**Why.** A surveyor measures one angle and one length and wants a height. An engineer knows a force and its direction and wants its horizontal part. Both need a link between **angles** and **ratios of lengths**. That link is trigonometry.

**Build.**

**Step 1 — names of the sides.** In a right-angled triangle, pick one of the two acute angles and call it $\theta$. Then
- the **hypotenuse** is the longest side, opposite the right angle;
- the **opposite** side is the one across from $\theta$;
- the **adjacent** side is the one next to $\theta$ that is not the hypotenuse.

**Step 2 — why the ratios depend only on the angle.** Draw a second right-angled triangle with the same angle $\theta$, but bigger.
''')
B.fig('similar_triangles', F.similar_triangles, 'Two right-angled triangles with the same angle θ are scaled copies of each other.')
B.md(r'''
Both triangles have a right angle and the angle $\theta$. The angles of a triangle add up to $180^\circ$, so the third angle is $90^\circ-\theta$ in both. Triangles with the same three angles have the same shape: one is a **scaled copy** of the other. Scaling multiplies all three sides by the same factor $k$, so any *ratio* of two sides is unchanged:
$$\frac{k\cdot\text{opposite}}{k\cdot\text{hypotenuse}}=\frac{\text{opposite}}{\text{hypotenuse}} .$$
**So the ratio opposite ÷ hypotenuse is the same in every right-angled triangle with angle $\theta$. It is a function of $\theta$ alone.** (Compare §2.3: the same scaling argument gave us the radian.)

**Step 3 — the definitions.** Give those ratios names:
$$\sin\theta=\frac{\text{opposite}}{\text{hypotenuse}},\qquad\cos\theta=\frac{\text{adjacent}}{\text{hypotenuse}},\qquad\tan\theta=\frac{\text{opposite}}{\text{adjacent}} .$$
(Memory aid: **SOH – CAH – TOA**.)

**Step 4 — the tangent is not new information.** Divide sine by cosine:
$$\frac{\sin\theta}{\cos\theta}=\frac{\ \dfrac{\text{opp}}{\text{hyp}}\ }{\dfrac{\text{adj}}{\text{hyp}}}=\frac{\text{opp}}{\text{hyp}}\cdot\frac{\text{hyp}}{\text{adj}}=\frac{\text{opp}}{\text{adj}}=\tan\theta
\qquad\Rightarrow\qquad\boxed{\tan\theta=\frac{\sin\theta}{\cos\theta}}$$

**Step 5 — using them.** Rearranged, the definitions turn a hypotenuse into the two other sides:
$$\text{opposite}=\text{hypotenuse}\cdot\sin\theta,\qquad\text{adjacent}=\text{hypotenuse}\cdot\cos\theta .$$

**Worked example.** A triangle has sides 3, 4, 5 with the right angle between the sides 3 and 4. Let $\theta$ be the angle opposite the side 3. Then hypotenuse $=5$, opposite $=3$, adjacent $=4$:
$$\sin\theta=\tfrac35=0.6,\qquad\cos\theta=\tfrac45=0.8,\qquad\tan\theta=\tfrac34=0.75 .$$
''')
B.ask(r'''In a right-angled triangle the hypotenuse is 10 and the side **adjacent** to $\theta$ is 6. What is $\cos\theta$?''', 'num', 0.6,
      r'''$\cos\theta=\dfrac{\text{adjacent}}{\text{hypotenuse}}=\dfrac{6}{10}=0.6$.''',
      r'''CAH: cosine = adjacent ÷ hypotenuse.''')

B.md(r'''
## 3.2 Pythagoras' theorem — with proof

**Why.** Everything that follows (the special angles, $\sin^2+\cos^2=1$, distances, the unit circle) rests on this one theorem. You have used it for years; here is *why it is true*.

**Theorem.** In a right-angled triangle with legs $a$, $b$ and hypotenuse $c$:
$$a^2+b^2=c^2 .$$

**Proof.** Take four copies of the triangle and a square with side $a+b$. Arrange the triangles inside the square as in the left picture.
''')
B.fig('pythagoras', F.pythagoras, 'The same big square, filled in two ways with the same four triangles.')
B.md(r'''
**Step 1 — the tilted figure in the middle is a square of side $c$.** Each of its four sides is a hypotenuse, so all four sides have length $c$. Its corners are right angles: at a point where two triangles meet along an edge of the big square, three angles sit side by side along a straight line — the two *different* acute angles of the triangle, and the corner of the tilted figure. The two acute angles of a right-angled triangle add up to $90^\circ$ (because all three add to $180^\circ$ and one is $90^\circ$). A straight line is $180^\circ$. So the corner of the tilted figure is $180^\circ-90^\circ=90^\circ$. Four equal sides and right angles: a square, with area $c^2$.

**Step 2 — write the area of the big square in two ways.**

*As one square:* its side is $a+b$, so its area is $(a+b)^2=a^2+2ab+b^2$.

*As the sum of its pieces:* four triangles, each of area $\frac12ab$, plus the tilted square: $4\cdot\frac12ab+c^2=2ab+c^2$.

**Step 3 — the two expressions describe the same area, so they are equal.**
$$\begin{aligned}
a^2+2ab+b^2&=2ab+c^2\\
a^2+b^2&=c^2 &&\text{(subtract $2ab$ from both sides)}\qquad\blacksquare
\end{aligned}$$

*The right-hand picture shows the same thing without algebra:* slide the four triangles into two rectangles, and the space left over is a square $a^2$ plus a square $b^2$. Same big square, same four triangles — so the left-over areas are equal: $c^2=a^2+b^2$.

**Worked example.** Legs $5$ and $12$: $c^2=25+144=169$, so $c=13$.

**Worked example — finding a leg.** Hypotenuse $10$, one leg $6$: $6^2+b^2=10^2\Rightarrow b^2=100-36=64\Rightarrow b=8$.
''')
B.ask(r'''A right-angled triangle has hypotenuse $17$ and one leg $8$. How long is the other leg?''', 'num', 15,
      r'''$8^2+b^2=17^2\Rightarrow b^2=289-64=225\Rightarrow b=15$.''',
      r'''Write $a^2+b^2=c^2$ with $c=17$ (the hypotenuse is always alone on its side) and solve for the unknown leg.''')

B.md(r'''
## 3.3 The first identity: $\sin^2\theta+\cos^2\theta=1$

**Build.** Take a right-angled triangle with opposite side $a$, adjacent side $b$, hypotenuse $c$, so that $\sin\theta=\frac ac$ and $\cos\theta=\frac bc$.

$$\begin{aligned}
a^2+b^2&=c^2 &&\text{(Pythagoras)}\\[2pt]
\frac{a^2}{c^2}+\frac{b^2}{c^2}&=1 &&\text{(divide every term by $c^2$)}\\[2pt]
\left(\frac ac\right)^2+\left(\frac bc\right)^2&=1\\[2pt]
(\sin\theta)^2+(\cos\theta)^2&=1 .
\end{aligned}$$

**Notation.** $(\sin\theta)^2$ is written $\sin^2\theta$ to save brackets. So:
$$\boxed{\,\sin^2\theta+\cos^2\theta=1\,}$$
This is Pythagoras' theorem, written with ratios. It lets you get one of sine and cosine from the other.

**Worked example.** $\theta$ is an acute angle with $\sin\theta=\frac35$. Find $\cos\theta$ and $\tan\theta$.

$$\begin{aligned}
\cos^2\theta&=1-\sin^2\theta=1-\frac{9}{25}=\frac{16}{25}\\
\cos\theta&=\frac45 &&\text{(positive root, because for an acute angle all sides — hence all ratios — are positive)}\\
\tan\theta&=\frac{\sin\theta}{\cos\theta}=\frac{3/5}{4/5}=\frac34 .
\end{aligned}$$

*(For angles beyond $90^\circ$ the root may have to be negative — §3.6 will tell you when.)*
''')
B.ask(r'''$\theta$ is acute and $\sin\theta=\dfrac{5}{13}$. Find $\cos\theta$.''', 'num', 12 / 13,
      r'''$\cos^2\theta=1-\dfrac{25}{169}=\dfrac{144}{169}$, so $\cos\theta=\dfrac{12}{13}\approx0.923$ (positive because the angle is acute). It is the 5–12–13 triangle.''',
      r'''Use $\cos^2\theta=1-\sin^2\theta$, then take the positive square root.''', fmt='a number, e.g. `7/25`')

B.md(r'''
## 3.4 The special angles — derived, not memorised

**Why.** For most angles $\sin$ and $\cos$ are ugly decimals. For $30^\circ$, $45^\circ$ and $60^\circ$ they are exact, and those values appear everywhere. You should be able to *rebuild* them in 20 seconds from two little pictures.
''')
B.fig('special_triangles', F.special_triangles, 'The only two triangles you need.')
B.md(r'''
**Build — the 45° triangle.**

1. Take a square with side 1 and cut it along a diagonal. Each half is a right-angled triangle with two legs of length 1.
2. The diagonal cuts the $90^\circ$ corner into two equal parts, so the acute angles are $45^\circ$ each.
3. Hypotenuse by Pythagoras: $c^2=1^2+1^2=2$, so $c=\sqrt2$.
4. Read off the ratios:
$$\sin45^\circ=\frac{\text{opp}}{\text{hyp}}=\frac{1}{\sqrt2},\qquad\cos45^\circ=\frac{1}{\sqrt2},\qquad\tan45^\circ=\frac11=1 .$$
5. Tidy up $\frac{1}{\sqrt2}$ by multiplying top and bottom by $\sqrt2$: $\;\dfrac{1}{\sqrt2}\cdot\dfrac{\sqrt2}{\sqrt2}=\dfrac{\sqrt2}{2}\approx0.7071$.

**Build — the 30°/60° triangle.**

1. Take an equilateral triangle with side 2. All three sides are equal, so all three angles are equal: $180^\circ/3=60^\circ$ each.
2. Drop the height from the top corner. By symmetry it meets the base at its midpoint, cutting the base into $1+1$, and it cuts the top angle into $30^\circ+30^\circ$.
3. Each half is a right-angled triangle with hypotenuse $2$, short leg $1$, and angles $60^\circ$ (at the base) and $30^\circ$ (at the top).
4. The height by Pythagoras: $1^2+h^2=2^2\Rightarrow h^2=3\Rightarrow h=\sqrt3$.
5. Read off the ratios. Seen from the $60^\circ$ corner: opposite $=\sqrt3$, adjacent $=1$. Seen from the $30^\circ$ corner the roles swap: opposite $=1$, adjacent $=\sqrt3$.

$$\sin30^\circ=\frac12,\quad\cos30^\circ=\frac{\sqrt3}{2},\quad\tan30^\circ=\frac{1}{\sqrt3};\qquad
\sin60^\circ=\frac{\sqrt3}{2},\quad\cos60^\circ=\frac12,\quad\tan60^\circ=\sqrt3 .$$

**The table you have just derived.**

| $\theta$ | $30^\circ=\frac{\pi}{6}$ | $45^\circ=\frac{\pi}{4}$ | $60^\circ=\frac{\pi}{3}$ |
|---|---|---|---|
| $\sin\theta$ | $\frac12$ | $\frac{\sqrt2}{2}$ | $\frac{\sqrt3}{2}$ |
| $\cos\theta$ | $\frac{\sqrt3}{2}$ | $\frac{\sqrt2}{2}$ | $\frac12$ |
| $\tan\theta$ | $\frac{1}{\sqrt3}$ | $1$ | $\sqrt3$ |

**Two things to notice.**

- *The cosine row is the sine row backwards.* That is no coincidence: in any right-angled triangle, the side opposite $\theta$ is the side adjacent to the other acute angle, $90^\circ-\theta$. So
$$\sin\theta=\cos(90^\circ-\theta).$$
That is what the "co" in cosine means: *sine of the complementary angle*.
- *A memory aid, once you understand where the values come from:* the sines of $0^\circ,30^\circ,45^\circ,60^\circ,90^\circ$ are $\frac{\sqrt0}{2},\frac{\sqrt1}{2},\frac{\sqrt2}{2},\frac{\sqrt3}{2},\frac{\sqrt4}{2}$.

**Size check** (do this whenever you write one of these down): $\frac12=0.5<\frac{\sqrt2}{2}\approx0.707<\frac{\sqrt3}{2}\approx0.866$. A bigger angle has a bigger opposite side, so a bigger sine.
''')
B.ask(r'''Without a calculator: what is $\tan\dfrac{\pi}{3}$? (Type it exactly, e.g. `sqrt(3)/3`.)''', 'num', math.sqrt(3),
      r'''$\frac{\pi}{3}=60^\circ$. In the half-equilateral triangle, seen from the $60^\circ$ corner: opposite $\sqrt3$, adjacent $1$. So $\tan60^\circ=\sqrt3\approx1.732$. (Check: $\frac{\sin}{\cos}=\frac{\sqrt3/2}{1/2}=\sqrt3$.)''',
      r'''Sketch the half-equilateral triangle (sides $1,\sqrt3,2$). Which corner is $60^\circ$? Then tan = opposite ÷ adjacent.''')

B.md(r'''
## 3.5 Beyond 90°: the unit circle

**Why.** A right-angled triangle only has room for angles between $0^\circ$ and $90^\circ$. But a wheel turns through $200^\circ$, $720^\circ$, or backwards. To give $\sin200^\circ$ a meaning we need a definition that works for **every** angle — and agrees with the triangle definition where both apply.

**Build.**

**Step 1 — put the triangle in a circle of radius 1.** Draw the circle of radius 1 around the origin (the **unit circle**). Start at the point $(1,0)$ and turn counter-clockwise through the angle $\theta$. You arrive at a point $P$ on the circle.
''')
B.fig('unit_circle_def', F.unit_circle_def, 'The point P reached after turning through θ has coordinates (cos θ, sin θ).')
B.md(r'''
**Step 2 — its coordinates are the cosine and the sine.** Drop a vertical line from $P$ to the $x$-axis. For an acute angle this makes a right-angled triangle whose hypotenuse is the radius, **1**. By §3.1:
$$\text{adjacent}=\text{hyp}\cdot\cos\theta=1\cdot\cos\theta,\qquad\text{opposite}=\text{hyp}\cdot\sin\theta=1\cdot\sin\theta .$$
The adjacent side is how far $P$ is to the right, and the opposite side is how far up. So
$$P=(\cos\theta,\ \sin\theta).$$

**Step 3 — turn that into the definition for all angles.** For angles beyond $90^\circ$ there is no triangle to appeal to, but the point $P$ still exists. So we **define**, for any angle $\theta$:

> $\cos\theta$ is the **$x$-coordinate**, and $\sin\theta$ is the **$y$-coordinate**, of the point reached by turning through $\theta$ from $(1,0)$ on the unit circle.
> Positive angles turn **counter-clockwise**, negative angles **clockwise**.

For acute angles this agrees with SOH–CAH–TOA (Step 2). For all other angles it is new — and everything else in trigonometry follows from this one sentence.

**Step 4 — four things you can read off immediately.**

**(a) The values on the axes.** Turning by $0$, $\frac\pi2$, $\pi$, $\frac{3\pi}{2}$ lands on $(1,0)$, $(0,1)$, $(-1,0)$, $(0,-1)$:

| $\theta$ | $0$ | $\frac\pi2$ | $\pi$ | $\frac{3\pi}{2}$ |
|---|---|---|---|---|
| point | $(1,0)$ | $(0,1)$ | $(-1,0)$ | $(0,-1)$ |
| $\cos\theta$ | $1$ | $0$ | $-1$ | $0$ |
| $\sin\theta$ | $0$ | $1$ | $0$ | $-1$ |

**(b) The size limits.** No point of the unit circle is further than 1 from either axis, so $-1\le\cos\theta\le1$ and $-1\le\sin\theta\le1$, always.

**(c) $\sin^2\theta+\cos^2\theta=1$ for every angle.** The distance from the origin to $P=(x,y)$ is $\sqrt{x^2+y^2}$ by Pythagoras, and on the unit circle this distance is 1. So $x^2+y^2=1$, i.e. $\cos^2\theta+\sin^2\theta=1$ — now for *all* angles, not only acute ones.

**(d) Periodicity.** Turning a further full turn brings you back to the same point. So adding $2\pi$ changes nothing:
$$\sin(\theta+2\pi)=\sin\theta,\qquad\cos(\theta+2\pi)=\cos\theta .$$
Angles that differ by a multiple of $2\pi$ are called **coterminal**. To handle a large or a negative angle, add or subtract $2\pi$ until it lies between $0$ and $2\pi$.

**Worked example.** $\cos\dfrac{7\pi}{3}$. Since $2\pi=\dfrac{6\pi}{3}$: $\;\dfrac{7\pi}{3}-\dfrac{6\pi}{3}=\dfrac{\pi}{3}$. So $\cos\dfrac{7\pi}{3}=\cos\dfrac{\pi}{3}=\dfrac12$.
''')
B.ask(r'''What is $\sin\dfrac{3\pi}{2}$? (Picture where you land on the circle.)''', 'num', -1,
      r'''$\frac{3\pi}{2}$ is three quarter-turns: you land at the bottom of the circle, $(0,-1)$. The sine is the $y$-coordinate: $-1$.''',
      r'''$\frac{3\pi}{2}$ is three quarter-turns counter-clockwise from $(1,0)$. Which point is that? Sine is its $y$-coordinate.''')
B.ask(r'''What is $\cos(5\pi)$?''', 'num', -1,
      r'''Subtract full turns: $5\pi-2\pi-2\pi=\pi$. So $\cos5\pi=\cos\pi$, the $x$-coordinate of $(-1,0)$, which is $-1$.''',
      r'''Remove multiples of $2\pi$ first: $5\pi-4\pi=\ ?$''')

B.md(r'''
## 3.6 Any angle: quadrant signs and the reference angle

**Why.** You know the exact values for $\frac\pi6,\frac\pi4,\frac\pi3$. The circle is symmetric, so the same three numbers ($\frac12,\frac{\sqrt2}{2},\frac{\sqrt3}{2}$) give the values at *every* multiple of $\frac\pi6$ and $\frac\pi4$ — only the signs change.

**Build.**

**Step 1 — the signs come from the coordinates.** The axes cut the plane into four **quadrants**, numbered counter-clockwise. Since $\cos\theta=x$ and $\sin\theta=y$, their signs are simply the signs of the coordinates there:

| Quadrant | angles | $x$, so $\cos$ | $y$, so $\sin$ | $\tan=\frac{\sin}{\cos}$ |
|---|---|---|---|---|
| I | $0$ to $\frac\pi2$ | $+$ | $+$ | $+$ |
| II | $\frac\pi2$ to $\pi$ | $-$ | $+$ | $-$ |
| III | $\pi$ to $\frac{3\pi}{2}$ | $-$ | $-$ | $+$ |
| IV | $\frac{3\pi}{2}$ to $2\pi$ | $+$ | $-$ | $-$ |

There is nothing to memorise: left of the $y$-axis $x$ is negative, below the $x$-axis $y$ is negative. (The mnemonic "**A**ll **S**tudents **T**ake **C**alculus" lists which of sin/cos/tan are positive in I, II, III, IV — use it only as a check.)

**Step 2 — the reference angle.** The **reference angle** of $\theta$ is the *acute* angle between the radius to $P$ and the **$x$-axis**.
''')
B.fig('quadrants', F.quadrants, 'The reference angle (orange) in each quadrant, and the signs of sin and cos there.')
B.md(r'''
The little triangle formed by the radius, the $x$-axis and the vertical through $P$ is congruent to the first-quadrant triangle with the reference angle. So **the sizes** of $\sin\theta$ and $\cos\theta$ are those of the reference angle; only the signs depend on the quadrant.

**Step 3 — the recipe.**

1. **Reduce**: add or subtract $2\pi$ until $0\le\theta<2\pi$.
2. **Quadrant**: decide where $\theta$ lies. *Trick:* write the borders with the same denominator as your angle. For sixths: $\frac\pi2=\frac{3\pi}{6}$, $\pi=\frac{6\pi}{6}$, $\frac{3\pi}{2}=\frac{9\pi}{6}$, $2\pi=\frac{12\pi}{6}$.
3. **Reference angle** = distance to the nearest part of the $x$-axis: $\;\theta$ in I, $\;\pi-\theta$ in II, $\;\theta-\pi$ in III, $\;2\pi-\theta$ in IV.
4. **Value** of the reference angle from the special triangles; **sign** from the quadrant.

**Worked example 1.** $\sin\dfrac{2\pi}{3}$ and $\cos\dfrac{2\pi}{3}$.
1. Already between $0$ and $2\pi$.
2. In thirds, $\frac\pi2=\frac{1.5\pi}{3}$ and $\pi=\frac{3\pi}{3}$; $\frac{2\pi}{3}$ lies between: quadrant II.
3. Reference angle: $\pi-\frac{2\pi}{3}=\frac{\pi}{3}$.
4. $\sin\frac\pi3=\frac{\sqrt3}{2}$, $\cos\frac\pi3=\frac12$. In II the sine is $+$ and the cosine is $-$:
$$\sin\frac{2\pi}{3}=\frac{\sqrt3}{2},\qquad\cos\frac{2\pi}{3}=-\frac12 .$$

**Worked example 2.** $\cos\dfrac{7\pi}{6}$.
1. In range. 2. $\frac{7\pi}{6}$ is between $\frac{6\pi}{6}$ and $\frac{9\pi}{6}$: quadrant III. 3. Reference angle: $\frac{7\pi}{6}-\pi=\frac\pi6$. 4. $\cos\frac\pi6=\frac{\sqrt3}{2}$, and the cosine is negative in III:
$$\cos\frac{7\pi}{6}=-\frac{\sqrt3}{2} .$$

**Worked example 3.** $\sin\dfrac{5\pi}{3}$.
1. In range. 2. In thirds, $\frac{3\pi}{2}=\frac{4.5\pi}{3}$ and $2\pi=\frac{6\pi}{3}$: quadrant IV. 3. Reference angle: $2\pi-\frac{5\pi}{3}=\frac\pi3$. 4. $\sin\frac\pi3=\frac{\sqrt3}{2}$, negative in IV:
$$\sin\frac{5\pi}{3}=-\frac{\sqrt3}{2} .$$

**Worked example 4 — a negative angle.** $\sin\left(-\dfrac{\pi}{4}\right)$.
1. Add $2\pi$: $-\frac\pi4+\frac{8\pi}{4}=\frac{7\pi}{4}$. 2. Quadrant IV. 3. Reference angle $2\pi-\frac{7\pi}{4}=\frac\pi4$. 4. Sine negative: $-\frac{\sqrt2}{2}$.
(Or directly: turn clockwise by $45^\circ$ and you are below the $x$-axis, at height $-\frac{\sqrt2}{2}$.)

### Experiment 5 — the unit circle, live
Move the slider. The left picture shows the point, the blue length is $\cos\theta$ and the red length is $\sin\theta$.

**Predict first, for each of these, the quadrant, the signs and the sizes — then set the slider (it counts in units of $\frac{\pi}{12}=15^\circ$):** $\theta=\frac{5\pi}{4}$ (15 steps), $\frac{5\pi}{6}$ (10 steps), $\frac{5\pi}{3}$ (20 steps).
''')
B.code(r'''
def circle_view(steps=15):
    th = steps * pi / 12
    c, s = cos(th), sin(th)
    fig, (a1, a2) = plt.subplots(1, 2, figsize=(10, 4.2), gridspec_kw={'width_ratios': [1, 1.4]})
    tt = np.linspace(0, 2 * pi, 400)
    a1.plot(np.cos(tt), np.sin(tt), color='0.6'); a1.set_aspect('equal')
    a1.axhline(0, color='k', lw=0.8); a1.axvline(0, color='k', lw=0.8)
    a1.plot([0, c], [0, s], 'k'); a1.plot([c, c], [0, s], 'r', lw=3, label='sin θ'); a1.plot([0, c], [0, 0], 'b', lw=3, label='cos θ')
    a1.plot([c], [s], 'ko'); a1.legend(loc='lower left', fontsize=9); a1.set_xlim(-1.3, 1.3); a1.set_ylim(-1.3, 1.3)
    a2.plot(tt, np.sin(tt), 'r', label='sin θ'); a2.plot(tt, np.cos(tt), 'b', label='cos θ')
    a2.axvline(th % (2 * pi), color='k', ls=':'); a2.plot([th % (2 * pi)] * 2, [s, c], 'ko')
    a2.set_xticks([k * pi / 2 for k in range(5)]); a2.set_xticklabels(['0', 'π/2', 'π', '3π/2', '2π']); a2.legend(fontsize=9)
    plt.show()
    print(f'θ = {steps}·π/12 = {degrees(th):.0f}°     cos θ = {c:+.4f}     sin θ = {s:+.4f}')

explore(circle_view, steps=(-12, 36, 1, 15))
''')
B.ask(r'''Find $\sin\dfrac{5\pi}{6}$.''', 'num', 0.5,
      r'''Quadrant II ($\frac{5\pi}{6}$ is between $\frac{3\pi}{6}$ and $\frac{6\pi}{6}$). Reference angle $\pi-\frac{5\pi}{6}=\frac\pi6$. $\sin\frac\pi6=\frac12$, and sine is positive in II: $\frac12$.''',
      r'''Quadrant? Reference angle $=\pi-\frac{5\pi}{6}$. Then the sign of the $y$-coordinate in that quadrant.''')
B.ask(r'''Find $\cos\dfrac{3\pi}{4}$. (Type it exactly if you like: `-sqrt(2)/2`.)''', 'num', -math.sqrt(2) / 2,
      r'''Quadrant II, reference angle $\pi-\frac{3\pi}{4}=\frac\pi4$, $\cos\frac\pi4=\frac{\sqrt2}{2}$. In II the $x$-coordinate is negative: $-\frac{\sqrt2}{2}\approx-0.707$.''',
      r'''The size is $\cos\frac\pi4$. The sign: is $x$ positive or negative in quadrant II?''')
B.ask(r'''Find $\sin\dfrac{4\pi}{3}$.''', 'num', -math.sqrt(3) / 2,
      r'''Quadrant III ($\frac{4\pi}{3}$ is between $\pi=\frac{3\pi}{3}$ and $\frac{3\pi}{2}=\frac{4.5\pi}{3}$). Reference angle $\frac{4\pi}{3}-\pi=\frac\pi3$. $\sin\frac\pi3=\frac{\sqrt3}{2}$; below the $x$-axis, so $-\frac{\sqrt3}{2}\approx-0.866$.''',
      r'''Quadrant III: reference angle $=\theta-\pi$. Both coordinates are negative there.''')

B.md(r'''
## 3.7 Four symmetries of the circle

**Why.** The reference-angle recipe is really four mirror symmetries in disguise. Seen as formulas they are identities you will use constantly — and each can be *read off a picture* in five seconds, so there is no need to memorise any of them.

**Build.** Let $P=(\cos\theta,\sin\theta)$ be the point for the angle $\theta$. Each picture shows what happens to $P$ under one symmetry of the circle.
''')
B.fig('symmetries', F.symmetries, 'Grey: the point for θ. Red: the point for the new angle.')
B.md(r'''
**(1) $-\theta$: mirror in the $x$-axis.** Turning the other way gives the mirror image below the axis. Mirroring in the $x$-axis keeps $x$ and flips the sign of $y$:
$$\cos(-\theta)=\cos\theta,\qquad\sin(-\theta)=-\sin\theta .$$
In the language of §1.7: **cosine is an even function, sine is an odd function.**

**(2) $\pi-\theta$: mirror in the $y$-axis.** Measuring $\theta$ backwards from the negative $x$-axis gives the mirror image on the left. That keeps $y$ and flips $x$:
$$\sin(\pi-\theta)=\sin\theta,\qquad\cos(\pi-\theta)=-\cos\theta .$$

**(3) $\theta+\pi$: half a turn.** Half a turn carries $P$ to the diametrically opposite point: both coordinates change sign:
$$\sin(\theta+\pi)=-\sin\theta,\qquad\cos(\theta+\pi)=-\cos\theta .$$

**(4) $\frac\pi2-\theta$: mirror in the line $y=x$.** Measuring $\theta$ backwards from the positive $y$-axis is the mirror image in the diagonal. Mirroring in $y=x$ **swaps** the two coordinates (you saw this with inverse functions in §1.5):
$$\sin\!\left(\frac\pi2-\theta\right)=\cos\theta,\qquad\cos\!\left(\frac\pi2-\theta\right)=\sin\theta .$$
This is the "co-sine" fact of §3.4, now for every angle.

**Worked example.** Given $\sin\theta=0.3$, find $\sin(\pi-\theta)$, $\sin(\theta+\pi)$, $\sin(-\theta)$ and $\cos(\frac\pi2-\theta)$.
By (2), (3), (1), (4): $\;0.3,\;-0.3,\;-0.3,\;0.3$.
''')
B.ask(r'''If $\cos\theta=0.2$, what is $\cos(\pi-\theta)$?''', 'num', -0.2,
      r'''$\pi-\theta$ is the mirror image in the $y$-axis: the $x$-coordinate changes sign. $\cos(\pi-\theta)=-\cos\theta=-0.2$.''',
      r'''Which mirror takes $\theta$ to $\pi-\theta$? What does that mirror do to the $x$-coordinate?''')

B.md(r'''
## 3.8 The tangent on the circle

**Build.**

**Step 1 — definition for any angle.** Keep the formula from §3.1: $\tan\theta=\dfrac{\sin\theta}{\cos\theta}=\dfrac{y}{x}$ for the point $P=(x,y)$.

**Step 2 — what it means.** $\dfrac yx$ is "rise over run" from the origin to $P$: the **slope of the radius line**. An angle of $45^\circ$ has slope 1; a steeper line has a bigger tangent.

**Step 3 — where it does not exist.** Division by zero is not allowed (§1.2), so $\tan\theta$ is undefined where $\cos\theta=0$: at $\theta=\frac\pi2$ and $\frac{3\pi}{2}$ (and all angles coterminal with them). The radius is vertical there — a vertical line has no slope.

**Step 4 — its period is $\pi$, not $2\pi$.** Half a turn sends $(x,y)$ to $(-x,-y)$, by symmetry (3). The slope is unchanged: $\dfrac{-y}{-x}=\dfrac yx$. So
$$\tan(\theta+\pi)=\tan\theta .$$
A line through the origin looks the same after half a turn.

**Step 5 — why it is called "tangent".** Extend the radius until it meets the vertical line $x=1$, which touches the circle (is *tangent* to it) at $(1,0)$. A line through the origin with slope $m$ is at height $m$ when $x=1$. So the radius line meets the tangent line at height $\tan\theta$.
''')
B.fig('tan_slope', F.tan_slope, 'tan θ is the height at which the extended radius meets the tangent line x = 1.')
B.md(r'''
**Worked example.** $\tan\dfrac{3\pi}{4}$. Quadrant II, reference angle $\frac\pi4$: $\sin\frac{3\pi}{4}=+\frac{\sqrt2}{2}$, $\cos\frac{3\pi}{4}=-\frac{\sqrt2}{2}$.
$$\tan\frac{3\pi}{4}=\frac{\ \ \frac{\sqrt2}{2}\ }{-\frac{\sqrt2}{2}}=-1 .$$
(A line sloping down at $45^\circ$ has slope $-1$ ✓.)
''')
B.ask(r'''Find $\tan\dfrac{7\pi}{6}$. (Exact form welcome.)''', 'num', 1 / math.sqrt(3),
      r'''Quadrant III, reference angle $\frac\pi6$: $\sin=-\frac12$, $\cos=-\frac{\sqrt3}{2}$. $\tan=\dfrac{-1/2}{-\sqrt3/2}=\dfrac{1}{\sqrt3}\approx0.577$ — positive, because minus over minus is plus. Or: $\tan(\frac\pi6+\pi)=\tan\frac\pi6$ since the period is $\pi$.''',
      r'''Find $\sin$ and $\cos$ of $\frac{7\pi}{6}$ separately (quadrant III, reference angle $\frac\pi6$), then divide. Watch the two signs.''')

B.md(r'''
## 3.9 The graphs of sine and cosine

**Build.** Plot the height of the point $P$ against the angle turned. As $\theta$ grows from $0$, the height rises from $0$ to $1$ (at $\frac\pi2$), falls back through $0$ (at $\pi$) to $-1$ (at $\frac{3\pi}{2}$), and returns to $0$ (at $2\pi$). Then everything repeats.
''')
B.fig('unroll', F.unroll, 'The sine graph is the height of a point on the unit circle, "unrolled" against the angle.')
B.md(r'''
**What to read from the graph.**

- **Period $2\pi$**: the pattern repeats after each full turn (§3.5 d).
- **Between $-1$ and $1$**: always (§3.5 b). The size of the swing, here 1, is called the **amplitude**.
- **Zeros of sine** at $0,\pi,2\pi,\dots$ (the point is on the $x$-axis). **Zeros of cosine** at $\frac\pi2,\frac{3\pi}{2},\dots$ (the point is on the $y$-axis).
- **Cosine is the same wave, a quarter turn ahead.** Proof with the symmetries of §3.7:
$$\sin\!\left(\theta+\frac\pi2\right)=\sin\!\left(\frac\pi2-(-\theta)\right)\overset{(4)}{=}\cos(-\theta)\overset{(1)}{=}\cos\theta .$$
So the graph of $\cos$ is the graph of $\sin$ shifted **left** by $\frac\pi2$ (an inside change, §1.6).

You saw these two waves already in Experiment 4 (the coordinates of a point on a turning wheel) and in the right-hand panel of Experiment 5. Next week is about stretching and shifting them.

## 3.10 Solving $\sin\theta=c$ and $\cos\theta=c$

**Why.** "At what angle is the height 0.5?" is the reverse question — and on a circle it nearly always has **two** answers per turn. Missing the second one is the classic mistake.

**Build.**

**Step 1 — the picture.** $\sin\theta=c$ asks: *which points of the unit circle have height $c$?* Draw the horizontal line $y=c$. For $-1<c<1$ it cuts the circle in **two** points, mirror images in the $y$-axis. $\cos\theta=c$ asks which points have $x$-coordinate $c$: the vertical line $x=c$, again two points, mirror images in the $x$-axis.
''')
B.fig('solve_sin', F.solve_sin, 'Each equation picks out two points of the circle.')
B.md(r'''
**Step 2 — the recipe.**

1. Find the **reference angle** $\alpha$: the acute angle whose sine (or cosine) is $|c|$, from the special triangles.
2. Decide the **two quadrants** from the sign of $c$: sine is the height, so $c>0$ means quadrants I and II, $c<0$ means III and IV. Cosine is the $x$-coordinate: $c>0$ means I and IV, $c<0$ means II and III.
3. Put the reference angle into those quadrants: $\;\alpha$ (I), $\;\pi-\alpha$ (II), $\;\pi+\alpha$ (III), $\;2\pi-\alpha$ (IV).

**Worked example 1.** Solve $\sin\theta=\frac12$ for $0\le\theta<2\pi$.
1. $\sin\alpha=\frac12\Rightarrow\alpha=\frac\pi6$. 2. Positive sine: quadrants I and II. 3. $\theta=\frac\pi6$ and $\theta=\pi-\frac\pi6=\frac{5\pi}{6}$.

**Worked example 2.** Solve $\cos\theta=-\frac12$ for $0\le\theta<2\pi$.
1. $\cos\alpha=\frac12\Rightarrow\alpha=\frac\pi3$. 2. Negative cosine: quadrants II and III. 3. $\theta=\pi-\frac\pi3=\frac{2\pi}{3}$ and $\theta=\pi+\frac\pi3=\frac{4\pi}{3}$.

**Worked example 3.** Solve $\sin\theta=-\frac{\sqrt2}{2}$ for $0\le\theta<2\pi$.
1. $\alpha=\frac\pi4$. 2. Negative sine: III and IV. 3. $\theta=\pi+\frac\pi4=\frac{5\pi}{4}$ and $\theta=2\pi-\frac\pi4=\frac{7\pi}{4}$.

**Always check** by putting each answer back (Experiment 5 will do it for you).

**How many solutions?** Two per turn if $-1<c<1$; exactly one if $c=\pm1$ (the line just touches the circle); none if $|c|>1$ (the line misses the circle).
''')
B.ask(r'''Solve $\cos\theta=\dfrac{\sqrt3}{2}$ for $0\le\theta<2\pi$. Give both solutions.''', 'set', [math.pi / 6, 11 * math.pi / 6],
      r'''Reference angle: $\cos\alpha=\frac{\sqrt3}{2}\Rightarrow\alpha=\frac\pi6$. Positive cosine means $x>0$: quadrants I and IV. So $\theta=\frac\pi6$ and $\theta=2\pi-\frac\pi6=\frac{11\pi}{6}$.''',
      r'''Reference angle first. Then: in which two quadrants is the $x$-coordinate positive?''', fmt='a list, e.g. `[pi/3, 5*pi/3]`')

B.md(r'''
## 3.11 Small angles: why $\sin\theta\approx\theta$

**Why.** The most used approximation in physics. It turns the pendulum equation into one you can solve, and it is the seed of the derivative of sine (Unit 2). Here is where it comes from.

**Build.** On the unit circle, mark an angle $\theta$ (in radians) and three lengths:
- the height of $P$, which is $\sin\theta$ (red);
- the **arc** from $(1,0)$ to $P$. On a circle of radius 1, $s=r\theta=\theta$: **the arc length is the angle itself** (blue);
- the height on the tangent line, $\tan\theta$ (purple).
''')
B.fig('small_angle', F.small_angle, 'sin θ, the arc θ and tan θ: clearly different for a large angle, almost equal for a small one.')
B.md(r'''
For a large angle the three lengths clearly differ: $\sin\theta<\theta<\tan\theta$. As the angle shrinks, the arc straightens out and all three nearly coincide. Hence, **for small angles in radians**,
$$\sin\theta\approx\theta,\qquad\tan\theta\approx\theta .$$

*This only works in radians*, because only then is the angle equal to the arc length. ($\sin1^\circ$ is not close to $1$; it is close to $\frac{\pi}{180}\approx0.01745$, which is $1^\circ$ expressed in radians.)

**And the cosine?** For small $\theta$, $\cos\theta$ is just below 1. How far below? Use $\cos^2\theta=1-\sin^2\theta\approx1-\theta^2$. Now try the guess $\cos\theta\approx1-\frac{\theta^2}{2}$ and square it:
$$\left(1-\frac{\theta^2}{2}\right)^2=1-\theta^2+\frac{\theta^4}{4} .$$
For small $\theta$ the last term is tiny (if $\theta=0.1$ it is $0.000025$), so the square is $1-\theta^2$ almost exactly — as required. Hence
$$\cos\theta\approx1-\frac{\theta^2}{2} .$$

In week 3 the "$\approx$" is made precise with limits; in Unit 4 you will get the full formula with all correction terms.

### Experiment 6 — how good is the approximation?
**Predict first:** by what percentage does $\theta$ overestimate $\sin\theta$ at $\theta=0.5$ rad (about $29^\circ$)? At $\theta=0.1$ rad? When $\theta$ becomes 10 times smaller, how much smaller does the error become?
''')
B.code(r'''
rows = []
for th in [1.0, 0.5, 0.25, 0.1, 0.05, 0.01]:
    rows.append([th, degrees(th), sin(th), 100 * (th - sin(th)) / sin(th), cos(th), 1 - th**2 / 2])
table(['θ (rad)', 'θ (deg)', 'sin θ', 'error of sin θ ≈ θ (%)', 'cos θ', '1 − θ²/2'], rows, fmt='%.6f')
''')
B.md(r'''
*Explain:* at $0.1$ rad ($5.7^\circ$) the error is under $0.2\%$. Making the angle 10 times smaller makes the *relative* error 100 times smaller: the error behaves like $\theta^2$. A pendulum swinging through a few degrees is therefore described extremely well by replacing $\sin\theta$ with $\theta$.
''')

# =====================================================================================
# PART 4 - CHART AND DRILL
# =====================================================================================
B.md(r'''
---
# Part 4 — The whole circle, and the daily drill

**Build it yourself first.** On paper, draw a large circle and mark the 16 angles $0,\frac\pi6,\frac\pi4,\frac\pi3,\frac\pi2,\dots$ all the way round. Using only the two special triangles and the quadrant signs, write the coordinates $(\cos\theta,\sin\theta)$ next to each. *Then* compare with the chart below. Repeat on a blank page every day this week until it takes under three minutes.
''')
B.fig('unit_circle_full', F.unit_circle_full, 'The unit circle. Every point is (cos θ, sin θ). Only three sizes ever appear: 1/2, √2/2, √3/2.')
B.md(r'''
### Daily drill (15 minutes, paper first)
`drill()` prints ten questions, different each day. Work them out **without a calculator**, then type your ten answers into `drill_check([...])`. Exact forms are fine: `sqrt(3)/2`, `-1/2`, `-sqrt(2)/2`, `1/sqrt(3)`.
''')
B.code(r'''
drill()
''')
B.code(r'''
drill_check([..., ..., ..., ..., ..., ..., ..., ..., ..., ...])
''', ref='drill(); drill_check([v for _, _, v in _DR["qs"]])')

B.md(r'''
## Week 1 summary — everything on one page

**Functions**
- $f(x)$: output of the machine $f$ for input $x$; put the *whole* input in every box.
- Domain traps: denominator $\ne0$; under an even root $\ge0$; inside a log $>0$.
- $f(g(x))$: inside first. Inverse: solve $y=f(x)$ for $x$; exists only if one-to-one; graph mirrored in $y=x$.
- Outside changes are vertical and direct; inside changes are horizontal and backwards.
- $x^2+bx=(x+\frac b2)^2-(\frac b2)^2$.

**Radians**
- $\theta=\dfrac sr$; full turn $=2\pi$; $180^\circ=\pi$.
- $s=r\theta$, $A=\frac12r^2\theta$, $v=\omega r$, $\omega=\text{rpm}\cdot\frac{2\pi}{60}$.

**Trigonometry**
- $\sin=\frac{\text{opp}}{\text{hyp}}$, $\cos=\frac{\text{adj}}{\text{hyp}}$, $\tan=\frac{\text{opp}}{\text{adj}}=\frac{\sin}{\cos}$.
- $a^2+b^2=c^2\ \Rightarrow\ \sin^2\theta+\cos^2\theta=1$.
- Half-square: $1,1,\sqrt2$. Half-equilateral: $1,\sqrt3,2$.
- Unit circle: $P=(\cos\theta,\sin\theta)$. Sizes from the reference angle, signs from the quadrant.
- $\cos$ even, $\sin$ odd; $\sin(\pi-\theta)=\sin\theta$; $\sin(\frac\pi2-\theta)=\cos\theta$; $\tan$ has period $\pi$.
- Small angles (radians): $\sin\theta\approx\theta$, $\cos\theta\approx1-\frac{\theta^2}{2}$.
''')

# =====================================================================================
# PROBLEMS
# =====================================================================================
B.md(r'''
---
# Week 1 problems

**Rules.** Paper first, no calculator for the exact ones. Type your answer into `check(n, ...)`. The **first** attempt is recorded. Wrong? Re-check your working → `hint(n)` → try again → `solution(n)` → write one line with `mistake(n, '...')`. Right? Still open `solution(n)` and compare the method with yours.

### Functions
''')
B.problem(S1, r'How many **integers** lie in the domain of $f(x)=\sqrt{9-x^2}$?', 'num', 7,
          [r'Which trap is present? Write the condition it imposes on $9-x^2$.',
           r'$9-x^2\ge0$ means $x^2\le9$, i.e. $-3\le x\le3$. Now list the whole numbers in that interval — include the ends and zero.'],
          r'''**Condition.** A square root needs $9-x^2\ge0$.

**Solve.** $9\ge x^2$, so $-3\le x\le3$. The domain is $[-3,3]$.

**Count the integers.** $-3,-2,-1,0,1,2,3$: that is **7** integers.

*Typical slips:* forgetting $0$, or forgetting that the end points $\pm3$ are allowed ($\sqrt0=0$ is fine).''', fmt='an integer')
B.problem(S1, r'What is the minimum value of $f(x)=x^2-6x+13$?', 'num', 4,
          [r'Complete the square: halve the coefficient of $x$, put it in the bracket, subtract its square.',
           r'$x^2-6x=(x-3)^2-9$. Add the 13 and use that a square is never negative.'],
          r'''**Complete the square.** Half of $-6$ is $-3$, and $(-3)^2=9$:
$$x^2-6x+13=(x-3)^2-9+13=(x-3)^2+4 .$$

**Read off.** $(x-3)^2\ge0$, with equality at $x=3$. So the minimum value is $0+4=$ **4**, reached at $x=3$.

**Check.** $f(3)=9-18+13=4$ ✓, and a neighbour is larger: $f(4)=16-24+13=5$ ✓.''')
B.problem(S1, r'For $f(x)=\dfrac{3x+1}{x-2}$, find $f^{-1}(4)$.', 'num', 9,
          [r'$f^{-1}(4)$ is the input that gives the output 4. So solve $f(x)=4$.',
           r'Multiply both sides of $\dfrac{3x+1}{x-2}=4$ by $(x-2)$, expand, and collect the $x$ terms on one side.'],
          r'''$f^{-1}(4)$ is the $x$ with $f(x)=4$.

$$\begin{aligned}
\frac{3x+1}{x-2}&=4\\
3x+1&=4(x-2) &&\text{(multiply by $x-2$)}\\
3x+1&=4x-8 &&\text{(expand)}\\
1+8&=4x-3x &&\text{($x$ terms to the right, numbers to the left)}\\
x&=9 .
\end{aligned}$$

**Check.** $f(9)=\dfrac{27+1}{9-2}=\dfrac{28}{7}=4$ ✓. So $f^{-1}(4)=$ **9**.''')
B.problem(S1, r'Let $f(x)=x^2$ and $g(x)=f(x-2)+1$. Compute $g(5)$. Also decide for yourself: where is the lowest point of the graph of $g$?', 'num', 10,
          [r'Put $x=5$ into $g$: the inside becomes $5-2$.'],
          r'''$g(5)=f(5-2)+1=f(3)+1=3^2+1=$ **10**.

**The graph.** $g(x)=(x-2)^2+1$ is the parabola $x^2$ moved **right** by 2 (inside change, backwards) and **up** by 1 (outside change). Its lowest point is $(2,1)$.''')
B.problem(S1, r'Let $f(x)=\sqrt{x+1}$ and $g(x)=x^2-1$. Compute $f(g(3))+g(f(3))$.', 'num', 6,
          [r'Do the two compositions separately, each from the inside out. Start with $g(3)$ for the first and $f(3)$ for the second.',
           r'$g(3)=8$, so $f(g(3))=f(8)=\sqrt9$. And $f(3)=\sqrt4=2$, so $g(f(3))=g(2)$.'],
          r'''**First term.** Inside: $g(3)=3^2-1=8$. Outside: $f(8)=\sqrt{8+1}=\sqrt9=3$.

**Second term.** Inside: $f(3)=\sqrt{3+1}=2$. Outside: $g(2)=2^2-1=3$.

**Sum.** $3+3=$ **6**.

*Remark.* Here both orders happen to give 3. In fact $g(f(x))=(\sqrt{x+1})^2-1=x$: on these inputs $g$ undoes $f$. They are inverse functions (with $g$ restricted to $x\ge0$).''')
B.md(r'''
### Angles and radians
''')
B.problem(S2, r'Convert $252^\circ$ to radians.', 'num', 252 * math.pi / 180,
          [r'Multiply by $\dfrac{\pi}{180}$.', r'Simplify $\dfrac{252}{180}$: both are divisible by 36.'],
          r'''$$252^\circ=252\cdot\frac{\pi}{180}=\frac{252}{180}\pi=\frac{7}{5}\pi=\frac{7\pi}{5}\approx4.398 .$$
(Divide 252 and 180 by 36.) *Sanity check:* $252^\circ$ is more than half a turn ($\pi\approx3.14$) and less than a full turn ($6.28$) ✓.''', fmt='a number, e.g. `5*pi/3`')
B.problem(S2, r'A belt runs over a pulley of radius $0.15$ m without slipping. The belt moves $1.2$ m. Through what angle (in radians) does the pulley turn?', 'num', 8,
          [r'The belt length that passes equals the arc length that the rim turns through.', r'Use the definition $\theta=\dfrac{s}{r}$.'],
          r'''No slipping means: arc length turned $=$ belt length moved, $s=1.2$ m.
$$\theta=\frac sr=\frac{1.2}{0.15}=8\ \text{rad}.$$
That is $\dfrac{8}{2\pi}\approx1.27$ revolutions.''', fmt='radians')
B.problem(S2, r'A wheel of radius $0.3$ m turns at $120$ rpm. How fast (in m/s) does a point on its rim move?', 'num', 0.3 * 120 * 2 * math.pi / 60,
          [r'Two steps: convert rpm to $\omega$ in rad/s, then use $v=\omega r$.', r'$\omega=120\cdot\dfrac{2\pi}{60}=4\pi$ rad/s.'],
          r'''**Angular velocity.** $\omega=120\cdot\dfrac{2\pi}{60}=4\pi\approx12.57$ rad/s.

**Rim speed.** $v=\omega r=4\pi\cdot0.3=1.2\pi\approx$ **3.77 m/s**.

*Check another way:* 120 rpm is 2 revolutions per second; one revolution is a circumference $2\pi\cdot0.3=1.885$ m; so $2\times1.885=3.77$ m/s ✓.''', fmt='m/s')
B.problem(S2, r'A lawn sprinkler waters a sector of angle $120^\circ$ out to a distance of $6$ m. What area (in m²) does it water?', 'num', 12 * math.pi,
          [r'The formula $A=\frac12r^2\theta$ needs $\theta$ in radians. Convert $120^\circ$ first.', r'$120^\circ=\dfrac{2\pi}{3}$. Then $A=\frac12\cdot6^2\cdot\dfrac{2\pi}{3}$.'],
          r'''**Convert.** $120^\circ=120\cdot\dfrac{\pi}{180}=\dfrac{2\pi}{3}$ rad.

**Area.** $A=\tfrac12r^2\theta=\tfrac12\cdot36\cdot\dfrac{2\pi}{3}=12\pi\approx$ **37.7 m²**.

*Check:* $120^\circ$ is a third of a turn; the full disc is $\pi\cdot36=113.1$ m²; a third of that is $37.7$ ✓.''', fmt='m²')
B.md(r'''
### Trigonometry on the unit circle
''')
B.problem(S3, r'Compute $\cos\dfrac{2\pi}{3}+\sin\dfrac{7\pi}{6}$ exactly.', 'num', -1,
          [r'Do the two terms separately with the recipe: quadrant → reference angle → size → sign.',
           r'$\frac{2\pi}{3}$ is in quadrant II with reference angle $\frac\pi3$; $\frac{7\pi}{6}$ is in quadrant III with reference angle $\frac\pi6$.'],
          r'''**First term.** $\frac{2\pi}{3}$: quadrant II, reference angle $\pi-\frac{2\pi}{3}=\frac\pi3$. $\cos\frac\pi3=\frac12$, and $x<0$ in II: $\cos\frac{2\pi}{3}=-\frac12$.

**Second term.** $\frac{7\pi}{6}$: quadrant III, reference angle $\frac{7\pi}{6}-\pi=\frac\pi6$. $\sin\frac\pi6=\frac12$, and $y<0$ in III: $\sin\frac{7\pi}{6}=-\frac12$.

**Sum.** $-\frac12-\frac12=$ **−1**.''')
B.problem(S3, r'Compute $\sin\dfrac{5\pi}{4}\cdot\cos\dfrac{7\pi}{4}$ exactly.', 'num', -0.5,
          [r'Both have reference angle $\frac\pi4$. Find the quadrant of each for the signs.',
           r'$\frac{5\pi}{4}$ is in III (sine negative); $\frac{7\pi}{4}$ is in IV (cosine positive). Then multiply $\left(-\frac{\sqrt2}{2}\right)\left(\frac{\sqrt2}{2}\right)$.'],
          r'''$\frac{5\pi}{4}$: quadrant III, reference angle $\frac\pi4$, sine negative: $\sin\frac{5\pi}{4}=-\frac{\sqrt2}{2}$.

$\frac{7\pi}{4}$: quadrant IV, reference angle $\frac\pi4$, cosine positive: $\cos\frac{7\pi}{4}=+\frac{\sqrt2}{2}$.

**Product.** $\left(-\dfrac{\sqrt2}{2}\right)\cdot\dfrac{\sqrt2}{2}=-\dfrac{\sqrt2\cdot\sqrt2}{4}=-\dfrac24=$ **−1/2**.''')
B.problem(S3, r'$\sin\theta=\dfrac35$ and $\theta$ lies in the **second quadrant**. Find $\cos\theta$.', 'num', -0.8,
          [r'Use $\sin^2\theta+\cos^2\theta=1$ to get $\cos^2\theta$.', r'$\cos^2\theta=\frac{16}{25}$, so $\cos\theta=\pm\frac45$. Which sign does the $x$-coordinate have in quadrant II?'],
          r'''**Size.** $\cos^2\theta=1-\sin^2\theta=1-\dfrac{9}{25}=\dfrac{16}{25}$, so $\cos\theta=\pm\dfrac45$.

**Sign.** In quadrant II the point is to the *left* of the $y$-axis, so $x=\cos\theta$ is negative.

$$\cos\theta=-\frac45=-0.8 .$$

*The identity gives the size; the quadrant gives the sign. You always need both.*''')
B.problem(S3, r'Solve $\cos\theta=-\dfrac{\sqrt3}{2}$ for $0\le\theta<2\pi$.', 'set', [5 * math.pi / 6, 7 * math.pi / 6],
          [r'Reference angle: which acute angle has cosine $\frac{\sqrt3}{2}$?', r'The reference angle is $\frac\pi6$. Cosine is negative where $x<0$: quadrants II and III. So $\pi-\frac\pi6$ and $\pi+\frac\pi6$.'],
          r'''**Reference angle.** $\cos\alpha=\frac{\sqrt3}{2}\Rightarrow\alpha=\frac\pi6$.

**Quadrants.** The cosine is the $x$-coordinate; it is negative in II and III.

**Solutions.** II: $\theta=\pi-\frac\pi6=\dfrac{5\pi}{6}$. III: $\theta=\pi+\frac\pi6=\dfrac{7\pi}{6}$.

**Check.** Both points are at $x=-\frac{\sqrt3}{2}\approx-0.866$ ✓ (mirror images in the $x$-axis).''', fmt='a list of the two solutions, e.g. `[pi/3, 5*pi/3]`')
B.problem(S3, r'Solve $\sin\theta=-\dfrac12$ for $0\le\theta<2\pi$.', 'set', [7 * math.pi / 6, 11 * math.pi / 6],
          [r'Reference angle from $\sin\alpha=\frac12$. Then: where is the height negative?', r'$\alpha=\frac\pi6$; quadrants III and IV: $\pi+\alpha$ and $2\pi-\alpha$.'],
          r'''**Reference angle.** $\sin\alpha=\frac12\Rightarrow\alpha=\frac\pi6$.

**Quadrants.** The sine is the height; it is negative below the $x$-axis: III and IV.

**Solutions.** III: $\theta=\pi+\frac\pi6=\dfrac{7\pi}{6}$. IV: $\theta=2\pi-\frac\pi6=\dfrac{11\pi}{6}$.''', fmt='a list of the two solutions')
B.problem(S3, r'Compute $\cos\!\left(-\dfrac{17\pi}{6}\right)$ exactly.', 'num', -math.sqrt(3) / 2,
          [r'First bring the angle into $[0,2\pi)$ by adding $2\pi=\frac{12\pi}{6}$ as often as needed.',
           r'$-\frac{17\pi}{6}+\frac{24\pi}{6}=\frac{7\pi}{6}$: quadrant III, reference angle $\frac\pi6$.'],
          r'''**Reduce.** $2\pi=\frac{12\pi}{6}$. Add it twice: $-\frac{17\pi}{6}+\frac{24\pi}{6}=\frac{7\pi}{6}$.

**Quadrant.** $\frac{7\pi}{6}$ is between $\pi$ and $\frac{3\pi}{2}$: quadrant III. Reference angle $\frac{7\pi}{6}-\pi=\frac\pi6$.

**Value.** $\cos\frac\pi6=\frac{\sqrt3}{2}$; in III the cosine is negative:
$$\cos\!\left(-\frac{17\pi}{6}\right)=-\frac{\sqrt3}{2}\approx-0.866 .$$

*Alternative start:* cosine is even, so $\cos(-\frac{17\pi}{6})=\cos\frac{17\pi}{6}$, and $\frac{17\pi}{6}-2\pi=\frac{5\pi}{6}$ (quadrant II, same value).''')
B.problem(S3, r'$\tan\theta=\dfrac34$ and $\theta$ lies in the **third quadrant**. Find $\sin\theta+\cos\theta$.', 'num', -1.4,
          [r'Draw the reference triangle: opposite 3, adjacent 4. What is its hypotenuse?', r'Hypotenuse 5, so the sizes are $\frac35$ and $\frac45$. In quadrant III both coordinates are negative.'],
          r'''**Reference triangle.** $\tan=\dfrac{\text{opp}}{\text{adj}}=\dfrac34$: take opposite 3, adjacent 4. Hypotenuse: $\sqrt{9+16}=5$.

**Sizes.** $|\sin\theta|=\frac35$, $|\cos\theta|=\frac45$.

**Signs.** Quadrant III: both coordinates negative. (Consistent: minus over minus gives the positive tangent.)

$$\sin\theta+\cos\theta=-\frac35-\frac45=-\frac75=-1.4 .$$''')
B.problem(S3, r'A $5$ m ladder leans against a wall, making an angle of $60^\circ$ with the ground. How high up the wall does it reach (in m)?', 'num', 5 * math.sqrt(3) / 2,
          [r'Sketch it. The ladder is the hypotenuse; the height is the side **opposite** the $60^\circ$ angle.', r'opposite $=$ hypotenuse $\cdot\sin60^\circ$.'],
          r'''The ladder, the wall and the ground form a right-angled triangle. The ladder is the hypotenuse (5 m); the height on the wall is opposite the $60^\circ$ angle.

$$\text{height}=5\sin60^\circ=5\cdot\frac{\sqrt3}{2}\approx4.33\ \text{m}.$$

(The foot of the ladder is $5\cos60^\circ=2.5$ m from the wall. Check with Pythagoras: $4.33^2+2.5^2=18.75+6.25=25=5^2$ ✓.)''', fmt='metres')
B.problem(S3, r'A pendulum model replaces $\sin\theta$ by $\theta$. At $\theta=0.2$ rad, what is the relative error $\dfrac{\theta-\sin\theta}{\sin\theta}$ in **percent**? (Use the code cell below as a calculator.)', 'num', (0.2 - math.sin(0.2)) / math.sin(0.2) * 100,
          [r'Compute `sin(0.2)` in a code cell, then $(0.2-\sin0.2)/\sin0.2\times100$.'],
          r'''$\sin0.2=0.198669\ldots$

$$\frac{0.2-0.198669}{0.198669}\times100\approx0.67\%.$$

So for swings up to about $11^\circ$ the simple model is accurate to better than 1 %. (Experiment 6 showed the error grows like $\theta^2$: at $0.4$ rad it is about four times larger.)''', fmt='a number (percent)')
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
Double-click this cell and write your answers *in your own words, without looking back*. If you cannot, that section is not finished — re-read it and try again tomorrow.

1. Why does $f(x-2)$ move a graph to the **right**?
2. What *is* a radian, and why is a full turn $2\pi$ of them?
3. Derive $\sin60^\circ$ and $\cos60^\circ$ from a picture.
4. Why is $\sin^2\theta+\cos^2\theta=1$ for every angle?
5. Why does $\sin\theta=\frac12$ have two solutions per turn?

*Your answers:*

&nbsp;

### 3 · Physics strand — the oscillator (1 hour)
The Physics Lab below runs a mass on a spring, with no friction and no driving force. **Before touching anything, predict:** what shape will the position-against-time graph have? What happens to the time for one swing if you make the spring stiffer?

Then look at the plots under the animation. You will recognise the wave from Experiment 4: an oscillation is the "shadow" of circular motion. Measure the time between two peaks, and keep that number — in week 2 you will connect it to $\omega$ through $T=\dfrac{2\pi}{\omega}$.
''')
B.code(r'''
lab('physics', exp='osc', F0=0, c=0, x0=1, k=25, m=1)
''')
B.md(r'''
### 4 · What comes next
**Week 2** takes the two waves you met here and (1) proves the addition formulas $\sin(a+b)$, $\cos(a+b)$ from the unit circle, (2) builds the inverse functions $\arcsin$, $\arccos$, $\arctan$ with the "restrict the domain" repair of §1.5, and (3) describes any oscillation as $A\sin(\omega t+\varphi)$ using the transformations of §1.6.
''')

if __name__ == '__main__':
    B.write()
