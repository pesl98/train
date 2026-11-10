"""Unit 1 · Week 2 - Trig identities, inverse trig functions, sinusoids (built from first principles)."""
import math
from nbkit import Book
import figs_u01 as F

B = Book('u01w2', 'Unit 1 · Week 2 — Identities, inverse trig and sinusoids', 'year1/u01w2-identities-sinusoids.ipynb')
S1, S2, S3, S4 = '1 Identities', '2 Inverse trig and equations', '3 Sinusoids', '4 General triangles'

B.md(r'''
# Unit 1 · Week 2 — Identities, inverse trig and sinusoids
*Term 1, week 2 of 12 · about 15 hours in this notebook and on paper*

**Where you are.** Last week you built $\sin$ and $\cos$ as the coordinates of a point on the unit circle. This week you learn to *calculate* with them.

**What you will be able to do at the end of the week**
1. **Prove** the addition formulas for $\sin(a\pm b)$ and $\cos(a\pm b)$ from the unit circle, and derive every other identity you need from them in a few lines — so that you never have to trust a formula sheet.
2. Use $\arcsin$, $\arccos$, $\arctan$ correctly and solve trigonometric equations, including finding *all* the solutions.
3. Read and write any oscillation as $A\sin(\omega t+\varphi)+C$, and add two oscillations of the same frequency — the idea behind all of AC circuit analysis.
4. Solve triangles that have no right angle (law of cosines, law of sines), with proofs.

**What is used from week 1:** the unit circle definition $P=(\cos\theta,\sin\theta)$, Pythagoras, the symmetries $\cos(-\theta)=\cos\theta$, $\sin(-\theta)=-\sin\theta$, $\sin(\frac\pi2-\theta)=\cos\theta$, the special values, inverse functions (§1.5) and transformations of graphs (§1.6). If one of these feels shaky, re-read that section first — this week leans on all of them.

Run the grey *SETUP* cell first. The tools are the same as last week: `ask`, `check`, `hint`, `solution`, `mistake`, `report`.
''')

# =====================================================================================
B.md(r'''
---
# Part 1 — Identities

## 1.1 Equation or identity?

**Why.** You will be told hundreds of times that "$\sin2x=2\sin x\cos x$". What kind of statement is that, and how would you know whether to believe it?

**Build.**

- An **equation** is true only for *some* values: $\sin x=\frac12$ holds for $x=\frac\pi6$ but not for $x=0$. You *solve* an equation.
- An **identity** is true for *every* value for which both sides make sense: $\sin^2x+\cos^2x=1$ holds whatever $x$ is. You *prove* an identity, and then you may use it to replace one side by the other anywhere.

**How to disprove a proposed identity:** find **one** value where the two sides differ. One counter-example is enough.

**How to prove one:** numbers are not enough — you cannot try every value. You need an argument that works for all values at once (geometry, or algebra starting from identities already proved).

**Worked example — a famous non-identity.** Is $\sin(a+b)=\sin a+\sin b$? Try $a=b=\frac\pi2$:
$$\text{left: }\sin\!\left(\tfrac\pi2+\tfrac\pi2\right)=\sin\pi=0,\qquad\text{right: }\sin\tfrac\pi2+\sin\tfrac\pi2=1+1=2 .$$
$0\ne2$, so it is **false**. $\sin$ is a *function*, not a number multiplying the bracket; you cannot "multiply it out". The correct formula is what §1.4–1.5 are about.

### Experiment 1 — testing is not proving
The cell tests five proposed identities at 1000 random values. A test can *refute*; it can never *prove*.

**Predict first:** which of the five do you expect to fail?
''')
B.code(r'''
rng = np.random.default_rng(0)
u = rng.uniform(-10, 10, 1000)          # 1000 random values
w = rng.uniform(-10, 10, 1000)

def test(name, lhs, rhs):
    err = np.max(np.abs(lhs - rhs))
    print(f'{name:<40} largest difference {err:8.1e}   ', 'no counter-example found' if err < 1e-9 else 'FALSE')

test('sin(2u) = 2 sin u cos u',               np.sin(2*u), 2*np.sin(u)*np.cos(u))
test('sin(2u) = 2 sin u',                     np.sin(2*u), 2*np.sin(u))
test('cos(2u) = 1 - 2 sin^2 u',               np.cos(2*u), 1 - 2*np.sin(u)**2)
test('sin(u+w) = sin u + sin w',              np.sin(u+w), np.sin(u) + np.sin(w))
test('sin(u+w) = sin u cos w + cos u sin w',  np.sin(u+w), np.sin(u)*np.cos(w) + np.cos(u)*np.sin(w))
''')
B.ask(r'''Someone claims $\cos(2x)=2\cos x$ is an identity. Test it at $x=0$: what is the left side minus the right side?''', 'num', -1,
      r'''Left: $\cos0=1$. Right: $2\cos0=2$. Difference $1-2=-1\ne0$, so the claim is false — one counter-example settles it.''',
      r'''Put $x=0$ into both sides. $\cos0=1$.''')

B.md(r'''
## 1.2 The Pythagorean family

**Build.** You proved $\sin^2x+\cos^2x=1$ last week (Pythagoras on the unit circle). Two relatives follow by dividing.

**Divide every term by $\cos^2x$** (allowed wherever $\cos x\ne0$):
$$\frac{\sin^2x}{\cos^2x}+\frac{\cos^2x}{\cos^2x}=\frac{1}{\cos^2x}\qquad\Rightarrow\qquad\tan^2x+1=\frac{1}{\cos^2x} .$$

**Three more names.** The reciprocals of $\cos$, $\sin$, $\tan$ have names of their own — you need to *recognise* them, nothing more:
$$\sec x=\frac{1}{\cos x},\qquad\csc x=\frac{1}{\sin x},\qquad\cot x=\frac{1}{\tan x}=\frac{\cos x}{\sin x} .$$
With that name the result above reads $\boxed{\tan^2x+1=\sec^2x}$. You will meet it in Unit 2 (the derivative of $\tan$) and Unit 3 (integrals).

**Worked example.** Simplify $(1-\cos x)(1+\cos x)$.
$$\begin{aligned}(1-\cos x)(1+\cos x)&=1-\cos^2x &&\text{(difference of squares: $(p-q)(p+q)=p^2-q^2$)}\\&=\sin^2x &&\text{(because $\sin^2x+\cos^2x=1$)}\end{aligned}$$
''')
B.ask(r'''Simplify $\dfrac{1-\sin^2x}{\cos x}$ to a single trigonometric function.''', 'sym', 'cos(x)',
      r'''$1-\sin^2x=\cos^2x$ (rearranged Pythagoras), so the fraction is $\dfrac{\cos^2x}{\cos x}=\cos x$.''',
      r'''What does $1-\sin^2x$ equal, by $\sin^2x+\cos^2x=1$?''', fmt="a formula in `x` as text, e.g. `'sin(x)'`")

B.md(r'''
## 1.3 A tool we need: the distance between two points

**Build.** Take two points $A=(x_1,y_1)$ and $B=(x_2,y_2)$. Draw the horizontal through one and the vertical through the other: you get a right-angled triangle whose legs are the horizontal difference $x_2-x_1$ and the vertical difference $y_2-y_1$, and whose hypotenuse is the segment $AB$. Pythagoras:
$$d^2=(x_2-x_1)^2+(y_2-y_1)^2 .$$
(It does not matter in which order you subtract, because the differences are squared.)

**Worked example.** From $(1,2)$ to $(4,6)$: $d^2=3^2+4^2=25$, so $d=5$.

## 1.4 The key theorem: $\cos(a-b)$

**Why.** We want $\sin$ and $\cos$ of a sum or difference of two angles in terms of the separate angles. Everything else this week — double angles, adding waves, phasors — is a consequence of this one result. So we prove it properly, and the proof works for **all** angles $a$ and $b$, not only acute ones.

**Theorem.** $\;\cos(a-b)=\cos a\cos b+\sin a\sin b .$

**Proof.** *Idea: compute one length in two different ways.*

Mark two points on the unit circle: $A$ at angle $a$ and $B$ at angle $b$. Call the length of the chord between them $d$.
''')
B.fig('cos_diff', F.cos_diff, 'The same chord before (left) and after (right) turning the whole picture back by the angle b.')
B.md(r'''
**Step 1 — the chord in the left picture.** The coordinates are $A=(\cos a,\sin a)$ and $B=(\cos b,\sin b)$. By the distance formula:
$$\begin{aligned}
d^2&=(\cos a-\cos b)^2+(\sin a-\sin b)^2\\
&=\cos^2a-2\cos a\cos b+\cos^2b\;+\;\sin^2a-2\sin a\sin b+\sin^2b &&\text{(expand both squares)}\\
&=(\cos^2a+\sin^2a)+(\cos^2b+\sin^2b)-2\cos a\cos b-2\sin a\sin b &&\text{(regroup)}\\
&=1+1-2\,(\cos a\cos b+\sin a\sin b) &&\text{($\sin^2+\cos^2=1$, twice)}\\
&=2-2\,(\cos a\cos b+\sin a\sin b).
\end{aligned}$$

**Step 2 — turn the whole picture.** Rotate everything clockwise by the angle $b$. Point $B$ lands on $(1,0)$, and point $A$ lands at the angle $a-b$, i.e. at $(\cos(a-b),\sin(a-b))$. **A rotation does not change lengths**, so the chord still has length $d$.

**Step 3 — the same chord in the right picture.**
$$\begin{aligned}
d^2&=(\cos(a-b)-1)^2+(\sin(a-b)-0)^2\\
&=\cos^2(a-b)-2\cos(a-b)+1+\sin^2(a-b) &&\text{(expand)}\\
&=\big(\cos^2(a-b)+\sin^2(a-b)\big)+1-2\cos(a-b)\\
&=2-2\cos(a-b) &&\text{($\sin^2+\cos^2=1$)}
\end{aligned}$$

**Step 4 — the two results describe the same length, so they are equal.**
$$\begin{aligned}
2-2\cos(a-b)&=2-2\,(\cos a\cos b+\sin a\sin b)\\
-2\cos(a-b)&=-2\,(\cos a\cos b+\sin a\sin b) &&\text{(subtract 2)}\\
\cos(a-b)&=\cos a\cos b+\sin a\sin b &&\text{(divide by $-2$)}\qquad\blacksquare
\end{aligned}$$

Nothing in the proof used that the angles are acute — only coordinates on the circle. So the formula holds for all $a$ and $b$.

**Check with numbers you know.** $a=\frac\pi2$, $b=\frac\pi6$: left side $\cos\frac\pi3=\frac12$. Right side $\cos\frac\pi2\cos\frac\pi6+\sin\frac\pi2\sin\frac\pi6=0\cdot\frac{\sqrt3}{2}+1\cdot\frac12=\frac12$ ✓.
''')
B.ask(r'''Use the theorem to compute $\cos\!\left(\dfrac\pi3-\dfrac\pi4\right)=\cos15^\circ$ exactly, then type its value.''', 'num', math.cos(math.pi / 12),
      r'''$\cos\frac\pi3\cos\frac\pi4+\sin\frac\pi3\sin\frac\pi4=\frac12\cdot\frac{\sqrt2}{2}+\frac{\sqrt3}{2}\cdot\frac{\sqrt2}{2}=\frac{\sqrt2+\sqrt6}{4}\approx0.9659$. (Sensible: $15^\circ$ is a small angle, so its cosine is close to 1.)''',
      r'''$\cos(a-b)=\cos a\cos b+\sin a\sin b$ with $a=\frac\pi3$, $b=\frac\pi4$. You can type `(sqrt(2)+sqrt(6))/4`.''')

B.md(r'''
## 1.5 The other three addition formulas

**Build.** From the one theorem, the other three follow in two lines each. The only extra ingredients are the symmetries from week 1 (§3.7):
$$\cos(-b)=\cos b,\qquad\sin(-b)=-\sin b,\qquad\sin u=\cos\!\left(\tfrac\pi2-u\right),\qquad\cos u=\sin\!\left(\tfrac\pi2-u\right).$$

**$\cos(a+b)$.** Write the sum as a difference, $a+b=a-(-b)$, and use the theorem with $-b$ in place of $b$:
$$\begin{aligned}
\cos(a+b)&=\cos\big(a-(-b)\big)\\
&=\cos a\cos(-b)+\sin a\sin(-b) &&\text{(the theorem)}\\
&=\cos a\cos b-\sin a\sin b &&\text{($\cos$ is even, $\sin$ is odd)}
\end{aligned}$$

**$\sin(a+b)$.** Turn the sine into a cosine with $\sin u=\cos(\frac\pi2-u)$:
$$\begin{aligned}
\sin(a+b)&=\cos\!\left(\tfrac\pi2-(a+b)\right)\\
&=\cos\!\left(\left(\tfrac\pi2-a\right)-b\right) &&\text{(regroup)}\\
&=\cos\!\left(\tfrac\pi2-a\right)\cos b+\sin\!\left(\tfrac\pi2-a\right)\sin b &&\text{(the theorem)}\\
&=\sin a\cos b+\cos a\sin b &&\text{(co-function symmetries)}
\end{aligned}$$

**$\sin(a-b)$.** Replace $b$ by $-b$ in the last result:
$$\sin(a-b)=\sin a\cos(-b)+\cos a\sin(-b)=\sin a\cos b-\cos a\sin b .$$

**The four addition formulas.**
$$\boxed{\begin{aligned}
\sin(a\pm b)&=\sin a\cos b\pm\cos a\sin b\\
\cos(a\pm b)&=\cos a\cos b\mp\sin a\sin b
\end{aligned}}$$

How to keep them apart: **sine mixes** (sin·cos + cos·sin) and **keeps the sign**; **cosine keeps its own kind together** (cos·cos, sin·sin) and **flips the sign**. These are the only trig formulas worth knowing by heart — and now you can rebuild them if you forget.

**See it — a second proof for acute angles.** In the picture, $OP=1$ makes the angle $a+b$ with the horizontal. The green triangle has hypotenuse 1 and angle $b$, so its legs are $OQ=\cos b$ and $PQ=\sin b$.
''')
B.fig('addition_geo', F.addition_geo, 'sin(a + b) is the height of P; cos(a + b) is the distance OB.')
B.md(r'''
- The blue triangle has hypotenuse $\cos b$ and angle $a$: its height is $QA=\cos b\sin a$ and its base is $OA=\cos b\cos a$.
- The yellow triangle has hypotenuse $\sin b$, and its angle at $P$ is again $a$ (its sides are perpendicular to the sides of the angle $a$ at $O$): so $PR=\sin b\cos a$ and $RQ=\sin b\sin a$.
- Height of $P$: $\;\sin(a+b)=PB=RB+PR=QA+PR=\sin a\cos b+\cos a\sin b$ ✓
- Distance $OB$: $\;\cos(a+b)=OA-BA=OA-RQ=\cos a\cos b-\sin a\sin b$ ✓

**Worked example 1.** $\cos75^\circ$ exactly. Split into angles you know: $75^\circ=45^\circ+30^\circ$.
$$\cos75^\circ=\cos45^\circ\cos30^\circ-\sin45^\circ\sin30^\circ=\frac{\sqrt2}{2}\cdot\frac{\sqrt3}{2}-\frac{\sqrt2}{2}\cdot\frac12=\frac{\sqrt6-\sqrt2}{4}\approx0.2588 .$$

**Worked example 2.** Simplify $\sin\!\left(x+\frac\pi2\right)$.
$$\sin\!\left(x+\tfrac\pi2\right)=\sin x\cos\tfrac\pi2+\cos x\sin\tfrac\pi2=\sin x\cdot0+\cos x\cdot1=\cos x .$$
(The cosine is the sine shifted a quarter turn — as you saw on the graphs last week.)

**Worked example 3.** Simplify $\cos x\cos3x-\sin x\sin3x$. Read the $\cos(a+b)$ formula from right to left with $a=x$, $b=3x$: it is $\cos(x+3x)=\cos4x$. *Recognising the right-hand side of a formula is as important as expanding the left.*

**The tangent of a sum** (for reference — derive it once). Divide the sine formula by the cosine formula, then divide top and bottom by $\cos a\cos b$:
$$\tan(a+b)=\frac{\sin a\cos b+\cos a\sin b}{\cos a\cos b-\sin a\sin b}=\frac{\tan a+\tan b}{1-\tan a\tan b}.$$
''')
B.ask(r'''Compute $\sin75^\circ=\sin(45^\circ+30^\circ)$ exactly and type its value.''', 'num', math.sin(math.radians(75)),
      r'''$\sin45^\circ\cos30^\circ+\cos45^\circ\sin30^\circ=\frac{\sqrt2}{2}\cdot\frac{\sqrt3}{2}+\frac{\sqrt2}{2}\cdot\frac12=\frac{\sqrt6+\sqrt2}{4}\approx0.9659$. Notice it equals $\cos15^\circ$ from the previous check: $\sin75^\circ=\cos(90^\circ-75^\circ)$.''',
      r'''Sine mixes and keeps the sign: $\sin a\cos b+\cos a\sin b$ with $a=45^\circ$, $b=30^\circ$.''')
B.ask(r'''Simplify $\sin5x\cos2x-\cos5x\sin2x$ to a single sine.''', 'sym', 'sin(3*x)',
      r'''It is the right-hand side of $\sin(a-b)=\sin a\cos b-\cos a\sin b$ with $a=5x$, $b=2x$: $\sin(5x-2x)=\sin3x$.''',
      r'''Which of the four formulas has the shape sin·cos − cos·sin? What are $a$ and $b$?''', fmt="a formula in `x` as text, e.g. `'sin(2*x)'`")

B.md(r'''
## 1.6 Double-angle and power-reduction formulas

**Build.** Put $b=a$ in the addition formulas.

**Sine.**
$$\sin2a=\sin(a+a)=\sin a\cos a+\cos a\sin a=2\sin a\cos a .$$

**Cosine.**
$$\cos2a=\cos(a+a)=\cos a\cos a-\sin a\sin a=\cos^2a-\sin^2a .$$
Using $\sin^2a=1-\cos^2a$, or $\cos^2a=1-\sin^2a$, this takes two more forms:
$$\begin{aligned}
\cos2a&=\cos^2a-(1-\cos^2a)=2\cos^2a-1,\\
\cos2a&=(1-\sin^2a)-\sin^2a=1-2\sin^2a .
\end{aligned}$$

$$\boxed{\sin2a=2\sin a\cos a\qquad\cos2a=\cos^2a-\sin^2a=2\cos^2a-1=1-2\sin^2a}$$

**Power reduction: solve the last two for the squares.**
$$\begin{aligned}
\cos2a=2\cos^2a-1\ &\Rightarrow\ 2\cos^2a=1+\cos2a\ \Rightarrow\ \cos^2a=\frac{1+\cos2a}{2},\\[3pt]
\cos2a=1-2\sin^2a\ &\Rightarrow\ 2\sin^2a=1-\cos2a\ \Rightarrow\ \sin^2a=\frac{1-\cos2a}{2}.
\end{aligned}$$

$$\boxed{\cos^2a=\frac{1+\cos2a}{2}\qquad\sin^2a=\frac{1-\cos2a}{2}}$$

These trade a *square* of a sine for a plain cosine of the double angle. That is how $\sin^2$ is integrated in Unit 3, and why the average power of an AC signal is half its peak power (Unit 11).

**Worked example 1.** $\sin x=0.6$ and $\cos x>0$. Find $\sin2x$ and $\cos2x$.

1. $\cos^2x=1-0.36=0.64$, so $\cos x=0.8$ (positive, as given).
2. $\sin2x=2\sin x\cos x=2\cdot0.6\cdot0.8=0.96$.
3. $\cos2x=1-2\sin^2x=1-2\cdot0.36=0.28$.
4. Check: $0.96^2+0.28^2=0.9216+0.0784=1$ ✓.

**Worked example 2.** Simplify $\dfrac{1-\cos2x}{2\sin x}$.
$$\frac{1-\cos2x}{2\sin x}=\frac{1-(1-2\sin^2x)}{2\sin x}=\frac{2\sin^2x}{2\sin x}=\sin x .$$
(Choose the form of $\cos2x$ that cancels the "1".)

**Worked example 3.** What is the average value of $\sin^2x$? By power reduction $\sin^2x=\frac12-\frac12\cos2x$. The cosine part swings equally above and below zero, so on average it contributes nothing. The average is $\frac12$.
''')
B.ask(r'''If $\cos x=\dfrac13$, what is $\cos2x$?''', 'num', -7 / 9,
      r'''Use the form that needs only the cosine: $\cos2x=2\cos^2x-1=2\cdot\frac19-1=-\frac79$.''',
      r'''Three forms of $\cos2x$ exist. Which one contains only $\cos x$?''', fmt='a number, e.g. `-3/8`')
B.md(r'''
### Experiment 2 — see power reduction
**Predict first:** how does the graph of $\sin^2x$ differ from that of $\sin x$? What is its period? Its lowest and highest values? Around which level does it swing?
''')
B.code(r'''
xs = np.linspace(0, 2 * pi, 500)
plt.plot(xs, np.sin(xs), color='0.7', label='sin x')
plt.plot(xs, np.sin(xs)**2, lw=5, alpha=0.35, label='sin² x')
plt.plot(xs, (1 - np.cos(2 * xs)) / 2, 'r--', lw=1.5, label='(1 − cos 2x)/2')
plt.axhline(0.5, color='g', ls=':', label='average 1/2')
plt.xticks([k * pi / 2 for k in range(5)], ['0', 'π/2', 'π', '3π/2', '2π']); plt.legend(); plt.show()
''')
B.md(r'''
*Explain:* squaring makes everything non-negative and doubles the frequency (period $\pi$). The thick curve and the dashed red curve coincide: $\sin^2x$ *is* a cosine wave of twice the frequency, centred on $\frac12$.

## 1.7 Products and sums of waves

**Build.** Add and subtract the addition formulas.

$$\begin{aligned}
\sin(a+b)&=\sin a\cos b+\cos a\sin b\\
\sin(a-b)&=\sin a\cos b-\cos a\sin b\\\hline
\text{add:}\quad\sin(a+b)+\sin(a-b)&=2\sin a\cos b
\end{aligned}$$
so $\;\sin a\cos b=\tfrac12\big[\sin(a+b)+\sin(a-b)\big]$. In the same way, from the two cosine formulas:
$$\cos a\cos b=\tfrac12\big[\cos(a-b)+\cos(a+b)\big],\qquad\sin a\sin b=\tfrac12\big[\cos(a-b)-\cos(a+b)\big].$$

**What this means physically.** Multiplying two waves of frequencies $f_1$ and $f_2$ produces waves at the **sum** and the **difference** of the frequencies. A radio receiver uses exactly this to move a station down to a frequency it can handle; you will use it for Fourier series in Unit 12.

**Read the first formula backwards** to turn a *sum* into a *product*. Let $p=a+b$ and $q=a-b$; then $a=\frac{p+q}{2}$, $b=\frac{p-q}{2}$, and
$$\sin p+\sin q=2\sin\frac{p+q}{2}\cos\frac{p-q}{2}.$$
Two notes of nearly equal pitch therefore sound like one note (the average pitch) whose loudness rises and falls slowly: **beats**.

### Experiment 3 — beats
The cell adds two sine waves of frequencies $f_1$ and $f_2$ (in Hz) and draws the slow "envelope" $\pm2\cos(\pi(f_1-f_2)t)$ predicted by the formula.

**Predict first:** with $f_1=10$ and $f_2=11$, how many times per second does the sound swell? What happens as $f_2$ gets closer to $f_1$?
''')
B.code(r'''
def beats(f1=10.0, f2=11.0):
    ts = np.linspace(0, 3, 3000)
    y = np.sin(2 * pi * f1 * ts) + np.sin(2 * pi * f2 * ts)
    env = 2 * np.cos(pi * (f1 - f2) * ts)
    plt.figure(figsize=(9.5, 3.4))
    plt.plot(ts, y, lw=0.8, label='sin(2π f₁ t) + sin(2π f₂ t)')
    plt.plot(ts, env, 'r', lw=1.5, label='envelope ±2 cos(π (f₁ − f₂) t)'); plt.plot(ts, -env, 'r', lw=1.5)
    plt.xlabel('time (s)'); plt.legend(loc='upper right', fontsize=9); plt.show()
    print(f'beat frequency |f1 - f2| = {abs(f1 - f2):.2f} per second')

explore(beats, f1=(5, 20, 0.5, 10), f2=(5, 20, 0.5, 11))
''')
B.md(r'''
*Explain:* the loudness swells $|f_1-f_2|$ times per second (the envelope $\cos$ has frequency $\frac{|f_1-f_2|}{2}$, but it produces a loud moment at both its positive and its negative peaks). Piano tuners listen for the beats to disappear.
''')

# =====================================================================================
B.md(r'''
---
# Part 2 — Inverse trigonometric functions and equations

## 2.1 Building arcsin, arccos and arctan

**Why.** Last week you solved $\sin\theta=\frac12$ because $\frac12$ is a "special" value. What if the equation is $\sin\theta=0.3$? You need a function that takes a sine *value* and returns an *angle*: the inverse of sine.

**The obstacle.** An inverse exists only for a one-to-one function (week 1, §1.5), and the sine is as far from one-to-one as a function can be: every value between $-1$ and $1$ is taken infinitely many times.

**The repair — exactly as with $x^2$ and $\sqrt{x}$: restrict the domain.** Keep only a piece of the graph on which the function takes each of its values exactly once.
''')
B.fig('inverse_branches', F.inverse_branches, 'The red pieces are one-to-one and cover every possible output exactly once.')
B.md(r'''
**Build.**

**Step 1 — choose the piece for sine.** On $\left[-\frac\pi2,\frac\pi2\right]$ the sine climbs steadily from $-1$ to $1$: each value appears once. This piece contains $0$ and all the acute angles, which is why it is the one everybody agrees on.

**Step 2 — define.** For $-1\le x\le1$,

> $\arcsin x$ is **the** angle in $\left[-\frac\pi2,\frac\pi2\right]$ whose sine is $x$.

**Step 3 — the same for cosine and tangent.** The cosine is not one-to-one on $\left[-\frac\pi2,\frac\pi2\right]$ (it goes up and comes down again), so a different piece is needed: on $[0,\pi]$ it falls steadily from $1$ to $-1$. The tangent climbs through all real values on $\left(-\frac\pi2,\frac\pi2\right)$.

| function | meaning | allowed inputs | **output always lies in** |
|---|---|---|---|
| $\arcsin x$ | the angle whose sine is $x$ | $-1\le x\le1$ | $\left[-\frac\pi2,\frac\pi2\right]$ (quadrants I and IV) |
| $\arccos x$ | the angle whose cosine is $x$ | $-1\le x\le1$ | $[0,\pi]$ (quadrants I and II) |
| $\arctan x$ | the angle whose tangent is $x$ | any real $x$ | $\left(-\frac\pi2,\frac\pi2\right)$ (quadrants I and IV) |

These outputs are called **principal values**. Other notations: $\sin^{-1}x$ (this is *not* $\frac{1}{\sin x}$), and in code `asin`, `acos`, `atan`.

**Step 4 — evaluate by asking the question in words.**

- $\arcsin\frac12$: "which angle in $[-\frac\pi2,\frac\pi2]$ has sine $\frac12$?" → $\frac\pi6$.
- $\arcsin\!\left(-\frac12\right)$: the sine is negative, so the angle is in the lower half of the allowed range: $-\frac\pi6$. (**Not** $\frac{7\pi}{6}$ or $\frac{11\pi}{6}$: those have the right sine but lie outside the allowed range.)
- $\arccos\!\left(-\frac12\right)$: "which angle in $[0,\pi]$ has cosine $-\frac12$?" Reference angle $\frac\pi3$, cosine negative → quadrant II: $\pi-\frac\pi3=\frac{2\pi}{3}$.
- $\arctan(-1)$: reference angle $\frac\pi4$, negative → $-\frac\pi4$.
- $\arctan\sqrt3=\frac\pi3$, since $\tan\frac\pi3=\sqrt3$.
''')
B.ask(r'''What is $\arccos\!\left(-\dfrac{\sqrt2}{2}\right)$?''', 'num', 3 * math.pi / 4,
      r'''We need the angle in $[0,\pi]$ with cosine $-\frac{\sqrt2}{2}$. Reference angle $\frac\pi4$; cosine negative means quadrant II: $\pi-\frac\pi4=\frac{3\pi}{4}$.''',
      r'''The answer must lie in $[0,\pi]$. Reference angle? Which quadrant has a negative cosine *and* lies in that range?''', fmt='a number, e.g. `2*pi/3`')
B.ask(r'''What is $\arcsin\!\left(-\dfrac{\sqrt3}{2}\right)$?''', 'num', -math.pi / 3,
      r'''The answer must lie in $[-\frac\pi2,\frac\pi2]$. Reference angle $\frac\pi3$, sine negative → $-\frac\pi3$.''',
      r'''arcsin can only return angles between $-\frac\pi2$ and $\frac\pi2$. A negative sine there means a negative angle.''', fmt='a number, e.g. `-pi/6`')

B.md(r'''
## 2.2 The trap: $\arcsin(\sin x)$ is not always $x$

**Build.** There are two orders in which to combine a function with its inverse, and they behave differently.

**(a) Inverse first, then the function: always safe.** $\sin(\arcsin x)=x$ for every $x$ in $[-1,1]$. "Take the angle whose sine is $x$; its sine is $x$."

**(b) Function first, then the inverse: only safe inside the principal range.** $\arcsin(\sin\theta)$ means "the angle **in $[-\frac\pi2,\frac\pi2]$** with the same sine as $\theta$". If $\theta$ is already in that range you get $\theta$ back. If not, you get a *different* angle with the same sine.

**Worked example 1.** $\arcsin\!\left(\sin\dfrac{5\pi}{6}\right)$.
1. Inside first: $\sin\frac{5\pi}{6}=\frac12$.
2. $\arcsin\frac12=\frac\pi6$. So the answer is $\frac\pi6$, **not** $\frac{5\pi}{6}$.

**Worked example 2.** $\arccos\!\left(\cos\dfrac{5\pi}{3}\right)$.
1. $\cos\frac{5\pi}{3}=\frac12$ (quadrant IV, reference angle $\frac\pi3$, cosine positive).
2. $\arccos\frac12=\frac\pi3$.

This is not a curiosity: your calculator and every program have this behaviour, and it is the source of "the code gives the wrong angle" bugs. §2.5 shows the cure.

## 2.3 A sine of an arccos, and friends

**Why.** Expressions like $\cos(\arcsin x)$ turn up when you integrate (Unit 3) and when you compute a power factor from a phase angle (Unit 11).

**Method: draw the triangle.**

**Worked example 1.** $\cos\!\left(\arcsin\frac35\right)$.
1. Let $\theta=\arcsin\frac35$. That says: $\sin\theta=\frac35$, and $\theta$ is in quadrant I (positive input).
2. Draw a right-angled triangle with opposite $3$ and hypotenuse $5$. Adjacent: $\sqrt{25-9}=4$.
3. $\cos\theta=\frac{\text{adj}}{\text{hyp}}=\frac45$.

**Worked example 2 — with a letter.** $\cos(\arcsin x)$ for $0\le x\le1$.
1. $\theta=\arcsin x$ means $\sin\theta=x=\frac x1$: opposite $x$, hypotenuse $1$.
2. Adjacent: $\sqrt{1-x^2}$.
3. $\cos(\arcsin x)=\sqrt{1-x^2}$.
(For negative $x$ the angle is in quadrant IV, where the cosine is still positive, so the formula holds for all $-1\le x\le1$.)
''')
B.ask(r'''Compute $\sin\!\left(\arccos\dfrac{5}{13}\right)$.''', 'num', 12 / 13,
      r'''$\theta=\arccos\frac{5}{13}$: adjacent 5, hypotenuse 13, so opposite $=\sqrt{169-25}=12$. $\sin\theta=\frac{12}{13}$.''',
      r'''Draw a right-angled triangle with adjacent 5 and hypotenuse 13. Find the third side.''', fmt='a number, e.g. `7/25`')

B.md(r'''
## 2.4 Solving trigonometric equations — all the solutions

**Build.** The calculator gives you **one** angle (the principal value). The circle tells you where the others are. Combine the two.

**The three basic equations** (with $\alpha$ the principal value):

| equation | principal value | all solutions in one turn | then |
|---|---|---|---|
| $\sin\theta=c$ | $\alpha=\arcsin c$ | $\alpha$ and $\pi-\alpha$ | add multiples of $2\pi$ |
| $\cos\theta=c$ | $\alpha=\arccos c$ | $\alpha$ and $-\alpha$ | add multiples of $2\pi$ |
| $\tan\theta=c$ | $\alpha=\arctan c$ | $\alpha$ | add multiples of $\pi$ |

**Where these come from** (week 1, §3.7): the points with the same height are mirror images in the $y$-axis, $\theta\leftrightarrow\pi-\theta$. The points with the same $x$ are mirror images in the $x$-axis, $\theta\leftrightarrow-\theta$. The tangent repeats every half turn.

**Then bring each answer into the interval the question asks for** by adding or subtracting $2\pi$.

**Worked example 1.** Solve $\sin\theta=0.3$ for $0\le\theta<2\pi$.
1. $\alpha=\arcsin0.3\approx0.3047$.
2. Second solution: $\pi-\alpha\approx2.8369$.
3. Both lie in $[0,2\pi)$. **Check:** $\sin2.8369\approx0.3$ ✓.

**Worked example 2.** Solve $\cos\theta=-0.4$ for $0\le\theta<2\pi$.
1. $\alpha=\arccos(-0.4)\approx1.9823$ (quadrant II — arccos takes care of that).
2. Second solution: $-\alpha\approx-1.9823$. Not in the interval; add $2\pi$: $4.3009$.
3. Solutions: $1.9823$ and $4.3009$.

**Worked example 3.** Solve $\tan\theta=2$ for $0\le\theta<2\pi$.
1. $\alpha=\arctan2\approx1.1071$.
2. Add $\pi$: $4.2487$. Add $\pi$ again: $7.39>2\pi$, too big. Solutions: $1.1071$ and $4.2487$.

**Worked example 4 — a multiple angle.** Solve $\cos2x=\frac12$ for $0\le x<\pi$.

*The safe method: rename the inside.*
1. Let $u=2x$. The equation is $\cos u=\frac12$.
2. **Translate the interval too:** $0\le x<\pi$ means $0\le2x<2\pi$, i.e. $0\le u<2\pi$.
3. Solve for $u$ in that interval: $u=\frac\pi3$ or $u=2\pi-\frac\pi3=\frac{5\pi}{3}$.
4. Go back: $x=\frac u2$, so $x=\frac\pi6$ or $x=\frac{5\pi}{6}$.

*The classic mistake* is to find only $u=\frac\pi3$, halve it, and stop — losing the second solution. Always translate the interval (step 2), and find **all** $u$ in the new interval before dividing.

**Worked example 5 — a quadratic in disguise.** Solve $2\sin^2x-\sin x-1=0$ for $0\le x<2\pi$.
1. Let $s=\sin x$: $\;2s^2-s-1=0$. Factor: $(2s+1)(s-1)=0$, so $s=-\frac12$ or $s=1$.
2. $\sin x=1$: $x=\frac\pi2$.
3. $\sin x=-\frac12$: reference angle $\frac\pi6$, quadrants III and IV: $x=\frac{7\pi}{6},\frac{11\pi}{6}$.
4. Three solutions: $\frac\pi2,\frac{7\pi}{6},\frac{11\pi}{6}$.
''')
B.code(r'''
# The calculator gives one angle; the circle gives the other.
alpha = asin(0.3)
print('arcsin(0.3)       =', alpha)
print('second solution   =', pi - alpha)
print('check: sin of both:', sin(alpha), sin(pi - alpha))
''')
B.ask(r'''Solve $\cos\theta=0.2$ for $0\le\theta<2\pi$. Give both solutions (use a code cell as calculator: `acos(0.2)`).''', 'set', [math.acos(0.2), 2 * math.pi - math.acos(0.2)],
      r'''$\alpha=\arccos0.2\approx1.3694$. The other point with the same $x$-coordinate is the mirror image $-\alpha$; adding $2\pi$ gives $2\pi-\alpha\approx4.9137$.''',
      r'''First solution: `acos(0.2)`. The second is its mirror image in the $x$-axis: $-\alpha$, brought into range by adding $2\pi$.''', fmt='a list of two numbers')
B.ask(r'''Solve $\sin2x=1$ for $0\le x<2\pi$. Give all solutions.''', 'set', [math.pi / 4, 5 * math.pi / 4],
      r'''Let $u=2x$, with $0\le u<4\pi$ (two full turns!). $\sin u=1$ at $u=\frac\pi2$ and, one turn later, $u=\frac{5\pi}{2}$. Halve: $x=\frac\pi4$ and $x=\frac{5\pi}{4}$.''',
      r'''Rename $u=2x$ and translate the interval: $0\le u<4\pi$. That is two turns, so collect the solutions of $\sin u=1$ from both.''', fmt='a list, e.g. `[pi/3, 4*pi/3]`')

B.md(r'''
## 2.5 The angle of a point: `atan2`

**Why.** Given a point $(x,y)$ — the tip of a force vector, a robot's target, a complex number — you often want its angle. The slope is $\tan\theta=\frac yx$, so the obvious formula is $\theta=\arctan\frac yx$. **It is wrong for half the plane.**

**Build.** The points $(1,1)$ and $(-1,-1)$ lie in opposite directions ($45^\circ$ and $225^\circ$), but they have the same ratio: $\frac11=\frac{-1}{-1}=1$. Once you have divided, the information about the quadrant is gone, and $\arctan$ (which only answers between $-90^\circ$ and $90^\circ$) returns $45^\circ$ for both.

**The cure:** a function that is given $y$ and $x$ **separately**, looks at their signs, and returns the angle in the correct quadrant, in $(-\pi,\pi]$. Every programming language has it: **`atan2(y, x)`** — note the order, $y$ first.
''')
B.code(r'''
rows = []
for (px, py) in [(1, 1), (-1, 1), (-1, -1), (1, -1), (0, 2), (-3, 0)]:
    naive = degrees(atan(py / px)) if px != 0 else float('nan')
    rows.append([f'({px}, {py})', naive, degrees(atan2(py, px))])
table(['point', 'arctan(y/x) in degrees', 'atan2(y, x) in degrees'], rows, fmt='%.1f')
''')
B.md(r'''
*Explain:* the two columns agree only for points with $x>0$ (quadrants I and IV). In engineering code, **always use `atan2`** to get an angle from two components.
''')

# =====================================================================================
B.md(r'''
---
# Part 3 — Sinusoids

## 3.1 The general sinusoid, one transformation at a time

**Why.** The voltage in a wall socket, the position of a mass on a spring, a pure musical note, the height of the tide: all have the same shape. One formula with four knobs describes them all:
$$y=A\sin(\omega t+\varphi)+C .$$
The variable is now called $t$ because it is nearly always *time*. You already own every tool needed to understand the four knobs: the transformation rules of week 1, §1.6.

**Build.** Start from the plain wave $y=\sin t$: it swings between $-1$ and $1$ around $0$, and one cycle takes $2\pi$.

**Knob 1 — $A$, the amplitude** (an *outside* factor). $y=A\sin t$ stretches the wave vertically: it now swings between $-A$ and $A$. The amplitude is the height of a peak above the middle.

**Knob 2 — $C$, the offset** (an *outside* addition). $y=A\sin t+C$ lifts everything by $C$. The wave swings around the **midline** $y=C$, between $C-A$ and $C+A$. From a graph: $\;C=\dfrac{\max+\min}{2}$ and $A=\dfrac{\max-\min}{2}$.

**Knob 3 — $\omega$, the angular frequency** (an *inside* factor). $y=\sin(\omega t)$ compresses the wave horizontally by the factor $\omega$. How long is one cycle now? One cycle is complete when the *inside* of the sine has grown by $2\pi$:
$$\omega T=2\pi\qquad\Rightarrow\qquad\boxed{T=\frac{2\pi}{\omega}}$$
$T$ is the **period**: the time for one cycle, in seconds. The **frequency** $f$ is the number of cycles per second, in hertz (Hz). If one cycle takes $T$ seconds, there are $\frac1T$ cycles in a second:
$$f=\frac1T=\frac{\omega}{2\pi}\qquad\Longleftrightarrow\qquad\boxed{\omega=2\pi f}$$
*Reading $\omega=2\pi f$:* each cycle is one turn of the unit circle, $2\pi$ radians; $f$ cycles per second is $2\pi f$ radians per second. $\omega$ is the angular velocity (week 1, §2.6) of the point on the circle whose shadow is the wave.

**Knob 4 — $\varphi$, the phase** (an *inside* addition). Write the inside so that $t$ stands alone, by factoring out $\omega$:
$$\omega t+\varphi=\omega\left(t+\frac{\varphi}{\omega}\right).$$
Replacing $t$ by $t+\frac{\varphi}{\omega}$ is an inside change, so it acts backwards: the wave is shifted **left** by $\dfrac{\varphi}{\omega}$ (for positive $\varphi$). It reaches every stage of its cycle *earlier*: we say it **leads**. A negative $\varphi$ shifts right: it **lags**.

> **The classic mistake:** saying "$\sin(2t+\frac\pi3)$ is shifted left by $\frac\pi3$". It is shifted left by $\frac{\pi/3}{2}=\frac\pi6$. Always factor out $\omega$ first.
''')
B.fig('sinusoid_anatomy', F.sinusoid_anatomy, 'The four knobs of a sinusoid. Here A = 2, ω = 2, φ = π/3, C = 1.')
B.md(r'''
**Summary.**

| symbol | name | unit | what it does |
|---|---|---|---|
| $A$ | amplitude | same as $y$ | half the peak-to-peak height |
| $C$ | offset | same as $y$ | the midline |
| $\omega$ | angular frequency | rad/s | $T=\dfrac{2\pi}{\omega}$, $\;f=\dfrac{\omega}{2\pi}$ |
| $\varphi$ | phase | rad | shifts the wave left by $\dfrac{\varphi}{\omega}$ |

**Worked example 1 — from formula to description.** The mains voltage in Europe is $v(t)=325\sin(100\pi t)$ volts.
- Amplitude $A=325$ V (the peak voltage; "230 V" is a kind of average called RMS — Unit 11).
- $\omega=100\pi\approx314$ rad/s.
- $f=\dfrac{\omega}{2\pi}=\dfrac{100\pi}{2\pi}=50$ Hz. $\;T=\dfrac1f=0.02$ s $=20$ ms.

**Worked example 2 — from description to formula.** A float bobs between $2$ m and $8$ m above the sea bed. One full bob takes $4$ s. At $t=0$ it is at its highest point. Find a formula.
1. Midline: $C=\frac{8+2}{2}=5$. Amplitude: $A=\frac{8-2}{2}=3$.
2. Period $T=4$ s: $\;\omega=\frac{2\pi}{T}=\frac{2\pi}{4}=\frac\pi2$ rad/s.
3. Phase: at $t=0$ we need the sine to equal $1$: $\sin\varphi=1$, so $\varphi=\frac\pi2$.
4. $y=3\sin\!\left(\frac\pi2t+\frac\pi2\right)+5$. Since $\sin(u+\frac\pi2)=\cos u$, this is simply $y=3\cos\!\left(\frac\pi2t\right)+5$: a wave that starts at its maximum is a cosine.
5. **Check:** $t=0$: $3+5=8$ ✓. Half a period later, $t=2$: $3\cos\pi+5=2$ ✓.

### Experiment 4 — the four knobs
**Predict first:** starting from $A=1,\ \omega=1,\ \varphi=0,\ C=0$, what changes when you (1) set $\omega=2$; (2) then set $\varphi=1$ — and by how much does the wave move, $1$ or $0.5$? (3) then set $A=2$, $C=1$?
''')
B.code(r'''
def wave(A=1.0, omega=1.0, phi=0.0, C=0.0):
    ts = np.linspace(-2, 10, 1200)
    plt.figure(figsize=(9.5, 3.8))
    plt.plot(ts, np.sin(ts), color='0.75', label='sin t')
    plt.plot(ts, A * np.sin(omega * ts + phi) + C, label='A sin(ωt + φ) + C')
    plt.axhline(C, color='g', ls=':', lw=1); plt.axvline(-phi / omega, color='r', ls=':', lw=1)
    plt.axhline(0, color='k', lw=0.8); plt.axvline(0, color='k', lw=0.8)
    plt.ylim(-4.2, 4.2); plt.xlabel('t'); plt.legend(loc='upper right', fontsize=9); plt.show()
    print(f'period T = 2π/ω = {2*pi/omega:.3f}    frequency f = {omega/(2*pi):.3f}    shift = −φ/ω = {-phi/omega:.3f}  (red dotted line: where the cycle starts)')

explore(wave, A=(0.5, 3, 0.5, 1), omega=(0.5, 4, 0.5, 1), phi=(-3, 3, 0.25, 0), C=(-2, 2, 0.5, 0))
''')
B.ask(r'''What is the period of $y=3\sin(4\pi t)$ ($t$ in seconds)?''', 'num', 0.5,
      r'''$\omega=4\pi$, so $T=\dfrac{2\pi}{\omega}=\dfrac{2\pi}{4\pi}=\dfrac12$ s. (The 3 is the amplitude; it does not affect the period.)''',
      r'''Identify $\omega$ (the number multiplying $t$) and use $T=\dfrac{2\pi}{\omega}$.''', fmt='seconds')
B.ask(r'''A signal is $y=\sin(120\pi t)$. What is its frequency in Hz?''', 'num', 60,
      r'''$f=\dfrac{\omega}{2\pi}=\dfrac{120\pi}{2\pi}=60$ Hz — the mains frequency in North America.''',
      r'''$\omega=120\pi$ and $f=\dfrac{\omega}{2\pi}$.''', fmt='Hz')
B.ask(r'''By how much is $y=\sin\!\left(3t+\dfrac{\pi}{2}\right)$ shifted to the **left** compared with $y=\sin3t$?''', 'num', math.pi / 6,
      r'''Factor out $\omega=3$: $3t+\frac\pi2=3\left(t+\frac\pi6\right)$. The shift is $\frac{\varphi}{\omega}=\frac{\pi/2}{3}=\frac\pi6\approx0.524$ — not $\frac\pi2$.''',
      r'''Factor the 3 out of $3t+\frac\pi2$ so that $t$ stands alone in a bracket.''', fmt='a number, e.g. `pi/4`')

B.md(r'''
## 3.2 Adding two sinusoids of the same frequency

**Why.** In an AC circuit the voltage across a resistor is a sine, across a capacitor a cosine, and Kirchhoff's law says you must add them. What is a sine plus a cosine? The answer is the most important fact about sinusoids: **a sine plus a cosine of the same frequency is again one sinusoid of that frequency.**

**Theorem.** For any numbers $a$ and $b$ (not both zero),
$$a\sin x+b\cos x=R\sin(x+\varphi),\qquad\text{with}\quad R=\sqrt{a^2+b^2}\quad\text{and}\quad\varphi=\operatorname{atan2}(b,a).$$

**Derivation.** *Idea: work backwards. Expand the right-hand side and find out which $R$ and $\varphi$ make it equal to the left.*

**Step 1 — expand** with the addition formula for sine:
$$R\sin(x+\varphi)=R\sin x\cos\varphi+R\cos x\sin\varphi=(R\cos\varphi)\sin x+(R\sin\varphi)\cos x .$$

**Step 2 — compare** with $a\sin x+b\cos x$. The two expressions are the same for all $x$ if the numbers in front of $\sin x$ agree and the numbers in front of $\cos x$ agree:
$$a=R\cos\varphi,\qquad b=R\sin\varphi .$$

**Step 3 — read these two conditions as a picture.** They say: the point $(a,b)$ is at distance $R$ from the origin, in the direction $\varphi$. (Compare the unit circle: a point at distance 1 in direction $\varphi$ is $(\cos\varphi,\sin\varphi)$; at distance $R$ it is $(R\cos\varphi,R\sin\varphi)$.)
''')
B.fig('rphi_triangle', F.rphi_triangle, 'R and φ are the length and the direction of the arrow from the origin to the point (a, b).')
B.md(r'''
**Step 4 — solve for $R$.** Square both conditions and add:
$$a^2+b^2=R^2\cos^2\varphi+R^2\sin^2\varphi=R^2(\cos^2\varphi+\sin^2\varphi)=R^2\qquad\Rightarrow\qquad R=\sqrt{a^2+b^2}.$$

**Step 5 — solve for $\varphi$.** It is the direction of the point $(a,b)$: $\;\varphi=\operatorname{atan2}(b,a)$. (Dividing the conditions gives $\tan\varphi=\frac ba$, but as §2.5 showed, the ratio alone loses the quadrant; `atan2` keeps it.) $\blacksquare$

**Worked example 1.** $3\sin x+4\cos x$.
1. $R=\sqrt{3^2+4^2}=5$.
2. $\varphi=\operatorname{atan2}(4,3)=\arctan\frac43\approx0.9273$ rad ($53.13^\circ$). (Both positive: quadrant I, so plain arctan is fine here.)
3. $3\sin x+4\cos x=5\sin(x+0.9273)$.
4. **Check at $x=0$:** left $=3\cdot0+4\cdot1=4$; right $=5\sin0.9273=5\cdot0.8=4$ ✓.

*Consequence:* the largest value $3\sin x+4\cos x$ can take is $5$ — not $3+4=7$, because the sine and the cosine never peak at the same moment.

**Worked example 2.** $\sin x-\cos x$. Here $a=1$, $b=-1$.
1. $R=\sqrt{1+1}=\sqrt2$.
2. The point $(1,-1)$ is in quadrant IV at $45^\circ$ below the axis: $\varphi=-\frac\pi4$.
3. $\sin x-\cos x=\sqrt2\sin\!\left(x-\frac\pi4\right)$.

**Worked example 3 — solving an equation with it.** Solve $\sin x+\sqrt3\cos x=1$ for $0\le x<2\pi$.
1. $a=1$, $b=\sqrt3$: $R=\sqrt{1+3}=2$; the point $(1,\sqrt3)$ is at $60^\circ$: $\varphi=\frac\pi3$.
2. The equation becomes $2\sin\!\left(x+\frac\pi3\right)=1$, i.e. $\sin u=\frac12$ with $u=x+\frac\pi3$.
3. Translate the interval: $\frac\pi3\le u<2\pi+\frac\pi3$.
4. $\sin u=\frac12$ at $u=\frac\pi6,\frac{5\pi}{6}$, and one turn later at $\frac{13\pi}{6},\dots$ Which lie in the interval? $\frac\pi6$ is too small; $\frac{5\pi}{6}$ ✓; $\frac{13\pi}{6}$ ✓ (it is less than $\frac{14\pi}{6}=2\pi+\frac\pi3$).
5. $x=u-\frac\pi3$: $\;x=\frac{5\pi}{6}-\frac{2\pi}{6}=\frac\pi2$ and $x=\frac{13\pi}{6}-\frac{2\pi}{6}=\frac{11\pi}{6}$.
6. **Check** $x=\frac\pi2$: $1+\sqrt3\cdot0=1$ ✓.

## 3.3 Phasors: a sinusoid is a rotating arrow

**Build.** Look again at what the theorem says. A sinusoid of a *given* frequency is completely described by **two numbers**: an amplitude and a phase. Two numbers are an arrow (length and direction). So:

> Every sinusoid of frequency $\omega$ can be represented by an arrow — a **phasor** — of length $A$ at angle $\varphi$.
> **Adding sinusoids of the same frequency is adding their arrows, tip to tail.**

In the theorem, $a\sin x$ is an arrow of length $a$ at angle $0$ (along the horizontal axis); $b\cos x=b\sin(x+\frac\pi2)$ is an arrow of length $b$ at angle $\frac\pi2$ (straight up). Tip to tail they reach the point $(a,b)$: length $R$, angle $\varphi$ — exactly the right-hand picture above.

Why "rotating"? Because $A\sin(\omega t+\varphi)$ is the height of a point going round a circle of radius $A$ at angular velocity $\omega$, starting from angle $\varphi$ (week 1, Experiment 4). All phasors of the same frequency rotate together, so their *relative* positions never change, and you may add them in a frozen snapshot.

This picture is the whole of AC circuit analysis in one sentence. In Unit 6, complex numbers will turn "adding arrows" into ordinary algebra.

### Experiment 5 — adding waves, adding arrows
**Predict first:** for $a=3$, $b=4$: amplitude and phase of the sum? Then try $a=3$, $b=-3$. Then $b=0$.
''')
B.code(r'''
def add_waves(a=3.0, b=4.0):
    xs = np.linspace(0, 4 * pi, 800)
    R, ph = hypot(a, b), atan2(b, a)
    fig, (a1, a2) = plt.subplots(1, 2, figsize=(11, 3.8), gridspec_kw={'width_ratios': [1, 2.2]})
    a1.set_aspect('equal'); a1.axhline(0, color='k', lw=0.8); a1.axvline(0, color='k', lw=0.8)
    a1.annotate('', xy=(a, 0), xytext=(0, 0), arrowprops=dict(arrowstyle='->', color='C0', lw=2))
    a1.annotate('', xy=(a, b), xytext=(a, 0), arrowprops=dict(arrowstyle='->', color='C2', lw=2))
    a1.annotate('', xy=(a, b), xytext=(0, 0), arrowprops=dict(arrowstyle='->', color='r', lw=2.5))
    a1.set_xlim(-5.5, 5.5); a1.set_ylim(-5.5, 5.5); a1.set_title('phasors: tip to tail')
    a2.plot(xs, a * np.sin(xs), 'C0', lw=1.2, label='a sin x'); a2.plot(xs, b * np.cos(xs), 'C2', lw=1.2, label='b cos x')
    a2.plot(xs, a * np.sin(xs) + b * np.cos(xs), 'k', lw=5, alpha=0.3, label='their sum')
    a2.plot(xs, R * np.sin(xs + ph), 'r--', lw=1.5, label='R sin(x + φ)'); a2.legend(fontsize=9, loc='upper right'); a2.set_ylim(-7.5, 7.5)
    plt.show()
    print(f'R = {R:.4f}     φ = {ph:.4f} rad = {degrees(ph):.1f}°')

explore(add_waves, a=(-5, 5, 0.5, 3), b=(-5, 5, 0.5, 4))
''')
B.ask(r'''Write $\sin x+\cos x$ as $R\sin(x+\varphi)$. What is $R$?''', 'num', math.sqrt(2),
      r'''$a=1$, $b=1$: $R=\sqrt{1^2+1^2}=\sqrt2\approx1.414$. (And $\varphi=\frac\pi4$: the point $(1,1)$ is at $45^\circ$.)''',
      r'''$R=\sqrt{a^2+b^2}$ with $a=b=1$.''')

B.md(r'''
## 3.4 Three-phase power

**Why.** Electricity is generated and distributed as **three** sinusoids of the same amplitude, each shifted by a third of a cycle ($\frac{2\pi}{3}=120^\circ$) from the next. One reason: their sum is exactly zero at every instant, so the return wire carries (ideally) no current.

**Claim.** $\;\sin x+\sin\!\left(x+\frac{2\pi}{3}\right)+\sin\!\left(x+\frac{4\pi}{3}\right)=0$ for all $x$.

**Proof by the addition formula.** Expand the second and third terms:
$$\begin{aligned}
\sin\!\left(x+\tfrac{2\pi}{3}\right)&=\sin x\cos\tfrac{2\pi}{3}+\cos x\sin\tfrac{2\pi}{3}=-\tfrac12\sin x+\tfrac{\sqrt3}{2}\cos x,\\
\sin\!\left(x+\tfrac{4\pi}{3}\right)&=\sin x\cos\tfrac{4\pi}{3}+\cos x\sin\tfrac{4\pi}{3}=-\tfrac12\sin x-\tfrac{\sqrt3}{2}\cos x .
\end{aligned}$$
(Values from the unit circle: $\frac{2\pi}{3}$ is in quadrant II, $\frac{4\pi}{3}$ in quadrant III, both with reference angle $\frac\pi3$.) Add all three:
$$\sin x\left(1-\tfrac12-\tfrac12\right)+\cos x\left(\tfrac{\sqrt3}{2}-\tfrac{\sqrt3}{2}\right)=0+0=0\qquad\blacksquare$$

**Proof by phasors, in one line.** Three arrows of equal length at $0^\circ$, $120^\circ$, $240^\circ$, placed tip to tail, form a closed equilateral triangle: their sum is the zero arrow.
''')
B.code(r'''
xs = np.linspace(0, 2 * pi, 600)
phases = [np.sin(xs + k * 2 * pi / 3) for k in range(3)]
for k, y in enumerate(phases):
    plt.plot(xs, y, label=f'phase {k + 1}')
plt.plot(xs, sum(phases), 'k', lw=3, label='sum')
plt.legend(fontsize=9, loc='upper right'); plt.show()
print('largest |sum| =', float(np.max(np.abs(sum(phases)))))
''')

# =====================================================================================
B.md(r'''
---
# Part 4 — Triangles without a right angle

**Why.** SOH–CAH–TOA needs a right angle. A surveyor's triangle, the triangle of two forces and their resultant, or the two links of a robot arm and the line to its target (the Robotics Lab solves exactly this) usually have none. Two laws handle every such triangle — and both are proved by **dropping a height**, which creates right-angled triangles you already master.

**Naming convention.** The corners are $A$, $B$, $C$; the side opposite each corner has the same small letter: $a$ is opposite $A$, and so on.
''')
B.fig('law_cos', F.law_cos, 'Drop the height h from A. It splits the triangle into two right-angled ones.')
B.md(r'''
## 4.1 The law of cosines

**Theorem.** $\;c^2=a^2+b^2-2ab\cos C$ — where $C$ is the angle **between** the sides $a$ and $b$, and $c$ is the side opposite it.

**Proof.** (Left picture.)

**Step 1.** Drop the height $h$ from $A$ onto side $a$. In the left right-angled triangle (hypotenuse $b$, angle $C$):
$$h=b\sin C,\qquad\text{the piece of $a$ next to $C$ is }b\cos C .$$

**Step 2.** The other piece of side $a$ is therefore $a-b\cos C$.

**Step 3.** Pythagoras in the right-hand right-angled triangle (legs $h$ and $a-b\cos C$, hypotenuse $c$):
$$\begin{aligned}
c^2&=h^2+(a-b\cos C)^2\\
&=b^2\sin^2C+a^2-2ab\cos C+b^2\cos^2C &&\text{(insert $h$; expand the square)}\\
&=a^2+b^2\,(\sin^2C+\cos^2C)-2ab\cos C &&\text{(collect the $b^2$ terms)}\\
&=a^2+b^2-2ab\cos C &&\text{($\sin^2+\cos^2=1$)}\qquad\blacksquare
\end{aligned}$$

(If the angle $C$ is obtuse, the height falls outside the triangle and the "piece" $b\cos C$ is negative — the same algebra still works.)

**Read the result.** It is Pythagoras with a correction term. If $C=90^\circ$ then $\cos C=0$ and it *is* Pythagoras. If $C<90^\circ$ the opposite side is shorter than Pythagoras would say; if $C>90^\circ$ ($\cos C<0$) it is longer.

**Use 1 — two sides and the angle between them → the third side.** Sides $5$ and $7$ with $60^\circ$ between them (from your diagnostic):
$$c^2=25+49-2\cdot5\cdot7\cdot\cos60^\circ=74-70\cdot\tfrac12=39,\qquad c=\sqrt{39}\approx6.245 .$$

**Use 2 — three sides → an angle.** Solve the law for the cosine:
$$\cos C=\frac{a^2+b^2-c^2}{2ab}.$$
Sides $7$, $8$, $9$; the angle opposite the side $9$:
$$\cos C=\frac{49+64-81}{2\cdot7\cdot8}=\frac{32}{112}=\frac27,\qquad C=\arccos\frac27\approx1.281\text{ rad}\approx73.4^\circ .$$
($\arccos$ returns angles in $[0,\pi]$ — exactly the range of angles a triangle can have. That is why the law of cosines is the safe way to find an angle.)

## 4.2 The law of sines, and the area

**Theorem.** $\;\dfrac{a}{\sin A}=\dfrac{b}{\sin B}=\dfrac{c}{\sin C}$.

**Proof.** (Right picture.) Compute the same height $h$ from both sides:
- in the left right-angled triangle: $h=b\sin C$;
- in the right right-angled triangle (hypotenuse $c$, angle $B$): $h=c\sin B$.

Equal heights: $b\sin C=c\sin B$. Divide both sides by $\sin B\sin C$: $\;\dfrac{b}{\sin B}=\dfrac{c}{\sin C}$. Dropping the height from another corner gives the equality with $\dfrac{a}{\sin A}$ in the same way. $\blacksquare$

**In words:** the bigger the angle, the bigger the side opposite it — in proportion to the *sine* of the angle.

**Use — one side and two angles → the other sides.** $A=40^\circ$, $B=75^\circ$, $a=10$.
1. $C=180^\circ-40^\circ-75^\circ=65^\circ$.
2. $b=\dfrac{a\sin B}{\sin A}=\dfrac{10\sin75^\circ}{\sin40^\circ}\approx15.03$.
3. $c=\dfrac{a\sin C}{\sin A}=\dfrac{10\sin65^\circ}{\sin40^\circ}\approx14.10$.

**Caution** when you use the law of sines to find an *angle*: $\sin B=0.8$ has two solutions between $0$ and $180^\circ$ ($53.1^\circ$ and $126.9^\circ$), and both may be genuine triangles. When you can, find angles with the law of cosines instead.

**The area of any triangle.** Base $a$, height $h=b\sin C$:
$$\text{Area}=\tfrac12\cdot\text{base}\cdot\text{height}=\tfrac12\,ab\sin C .$$
''')
B.ask(r'''Two sides of a triangle are $3$ and $8$, and the angle between them is $60^\circ$. How long is the third side?''', 'num', 7,
      r'''$c^2=9+64-2\cdot3\cdot8\cdot\cos60^\circ=73-48\cdot\frac12=49$, so $c=7$.''',
      r'''Law of cosines with $a=3$, $b=8$, $C=60^\circ$, $\cos60^\circ=\frac12$.''')
B.ask(r'''What is the area of that triangle (sides 3 and 8, angle $60^\circ$ between them)?''', 'num', 6 * math.sqrt(3),
      r'''$\frac12ab\sin C=\frac12\cdot3\cdot8\cdot\frac{\sqrt3}{2}=6\sqrt3\approx10.39$.''',
      r'''Area $=\frac12ab\sin C$.''')

B.md(r'''
## Week 2 summary — everything on one page

**Identities** (each derived from the one before)
- $\cos(a-b)=\cos a\cos b+\sin a\sin b$ — proved by computing a chord in two ways.
- $\sin(a\pm b)=\sin a\cos b\pm\cos a\sin b$, $\quad\cos(a\pm b)=\cos a\cos b\mp\sin a\sin b$.
- $\sin2a=2\sin a\cos a$, $\quad\cos2a=\cos^2a-\sin^2a=2\cos^2a-1=1-2\sin^2a$.
- $\sin^2a=\frac{1-\cos2a}{2}$, $\quad\cos^2a=\frac{1+\cos2a}{2}$, $\quad1+\tan^2a=\sec^2a$.

**Inverse functions**
- $\arcsin\in[-\frac\pi2,\frac\pi2]$, $\arccos\in[0,\pi]$, $\arctan\in(-\frac\pi2,\frac\pi2)$.
- $\sin\theta=c$: $\alpha,\ \pi-\alpha$. $\;\cos\theta=c$: $\pm\alpha$. $\;\tan\theta=c$: $\alpha+k\pi$. Multiple angle: rename $u$, translate the interval.
- Angle of a point: `atan2(y, x)`.

**Sinusoids** $y=A\sin(\omega t+\varphi)+C$
- $T=\frac{2\pi}{\omega}$, $f=\frac1T$, $\omega=2\pi f$; shifted left by $\frac{\varphi}{\omega}$.
- $a\sin x+b\cos x=R\sin(x+\varphi)$ with $R=\sqrt{a^2+b^2}$, $\varphi=\operatorname{atan2}(b,a)$: adding sinusoids = adding arrows.

**Triangles**
- $c^2=a^2+b^2-2ab\cos C$; $\quad\frac{a}{\sin A}=\frac{b}{\sin B}=\frac{c}{\sin C}$; $\quad$Area $=\frac12ab\sin C$.
''')

# =====================================================================================
B.md(r'''
---
# Week 2 problems

Paper first. First attempt counts. `hint(n)` → `solution(n)` → `mistake(n, '...')`. Keep your daily unit-circle drill going (cell at the very end).

### Identities
''')
B.problem(S1, r'$\sin x=0.6$ and $\cos x>0$. Find $\sin2x$.', 'num', 0.96,
          [r'$\sin2x=2\sin x\cos x$: you need $\cos x$ first.', r'$\cos^2x=1-0.36=0.64$, and the cosine is positive.'],
          r'''**Find the cosine.** $\cos^2x=1-\sin^2x=1-0.36=0.64$, so $\cos x=\pm0.8$; given $\cos x>0$: $\cos x=0.8$.

**Double angle.** $\sin2x=2\sin x\cos x=2\cdot0.6\cdot0.8=$ **0.96**.''')
B.problem(S1, r'Compute $\cos105^\circ$ exactly, using $105^\circ=60^\circ+45^\circ$. Type its value.', 'num', math.cos(math.radians(105)),
          [r'$\cos(a+b)=\cos a\cos b-\sin a\sin b$.', r'$\frac12\cdot\frac{\sqrt2}{2}-\frac{\sqrt3}{2}\cdot\frac{\sqrt2}{2}$. You can type `(sqrt(2)-sqrt(6))/4`.'],
          r'''$$\cos105^\circ=\cos60^\circ\cos45^\circ-\sin60^\circ\sin45^\circ=\frac12\cdot\frac{\sqrt2}{2}-\frac{\sqrt3}{2}\cdot\frac{\sqrt2}{2}=\frac{\sqrt2-\sqrt6}{4}\approx-0.2588 .$$

**Sanity check.** $105^\circ$ is in quadrant II, so the cosine must be negative ✓, and it is just past $90^\circ$, so small in size ✓.''')
B.problem(S1, r'Simplify $\dfrac{\sin2x}{1+\cos2x}$ to a single trigonometric function.', 'sym', 'tan(x)',
          [r'Replace $\sin2x$ by $2\sin x\cos x$. For $\cos2x$ choose the form that cancels the 1 in the denominator.',
           r'$1+\cos2x=1+(2\cos^2x-1)=2\cos^2x$.'],
          r'''$$\frac{\sin2x}{1+\cos2x}=\frac{2\sin x\cos x}{1+(2\cos^2x-1)}=\frac{2\sin x\cos x}{2\cos^2x}=\frac{\sin x}{\cos x}=\tan x .$$

The choice $\cos2x=2\cos^2x-1$ is made so that the "$+1$" and "$-1$" cancel.''', fmt="a formula in `x` as text, e.g. `'cos(x)'`")
B.problem(S1, r'Simplify $\cos x\cos3x-\sin x\sin3x$ to a single trigonometric function.', 'sym', 'cos(4*x)',
          [r'Which addition formula has the shape cos·cos − sin·sin?'],
          r'''It is the right-hand side of $\cos(a+b)=\cos a\cos b-\sin a\sin b$ with $a=x$, $b=3x$:
$$\cos x\cos3x-\sin x\sin3x=\cos(x+3x)=\cos4x .$$''', fmt="a formula in `x` as text, e.g. `'sin(2*x)'`")
B.problem(S1, r'$a$ and $b$ are acute angles with $\sin a=\dfrac35$ and $\cos b=\dfrac{5}{13}$. Find $\sin(a+b)$.', 'num', 63 / 65,
          [r'You need all four of $\sin a,\cos a,\sin b,\cos b$. Get the missing two from Pythagoras (3–4–5 and 5–12–13 triangles).',
           r'$\cos a=\frac45$, $\sin b=\frac{12}{13}$. Then $\sin a\cos b+\cos a\sin b$.'],
          r'''**Missing values** (acute angles, so everything is positive): $\cos a=\sqrt{1-\frac{9}{25}}=\frac45$; $\sin b=\sqrt{1-\frac{25}{169}}=\frac{12}{13}$.

**Addition formula.**
$$\sin(a+b)=\sin a\cos b+\cos a\sin b=\frac35\cdot\frac{5}{13}+\frac45\cdot\frac{12}{13}=\frac{15}{65}+\frac{48}{65}=\frac{63}{65}\approx0.969 .$$''', fmt='a number, e.g. `33/65`')
B.md(r'''
### Inverse functions and equations
''')
B.problem(S2, r'Compute $\arcsin\frac12+\arccos\frac12+\arctan1$.', 'num', 3 * math.pi / 4,
          [r'Ask each one in words: "which angle in the allowed range has sine $\frac12$?" and so on.'],
          r'''$\arcsin\frac12=\frac\pi6$, $\arccos\frac12=\frac\pi3$, $\arctan1=\frac\pi4$.

$$\frac\pi6+\frac\pi3+\frac\pi4=\frac{2\pi}{12}+\frac{4\pi}{12}+\frac{3\pi}{12}=\frac{9\pi}{12}=\frac{3\pi}{4}\approx2.356 .$$

*Remark:* $\arcsin x+\arccos x=\frac\pi2$ for every $x$ — the two angles are complementary (co-sine!).''')
B.problem(S2, r'Compute $\arcsin\!\left(\sin\dfrac{7\pi}{6}\right)$.', 'num', -math.pi / 6,
          [r'Inside first: what is $\sin\frac{7\pi}{6}$?', r'$\sin\frac{7\pi}{6}=-\frac12$. Now: which angle **in $[-\frac\pi2,\frac\pi2]$** has sine $-\frac12$?'],
          r'''**Inside.** $\frac{7\pi}{6}$ is in quadrant III with reference angle $\frac\pi6$: $\sin\frac{7\pi}{6}=-\frac12$.

**Outside.** $\arcsin\!\left(-\frac12\right)$ is the angle in $[-\frac\pi2,\frac\pi2]$ with sine $-\frac12$: that is $-\frac\pi6$.

So the answer is $-\dfrac\pi6\approx-0.524$, **not** $\frac{7\pi}{6}$: that angle is outside the range of arcsin.''')
B.problem(S2, r'Compute $\tan\!\left(\arcsin\dfrac{8}{17}\right)$.', 'num', 8 / 15,
          [r'Draw the triangle: opposite 8, hypotenuse 17.', r'Adjacent $=\sqrt{17^2-8^2}=15$.'],
          r'''Let $\theta=\arcsin\frac{8}{17}$: opposite $8$, hypotenuse $17$. Adjacent: $\sqrt{289-64}=\sqrt{225}=15$.

$$\tan\theta=\frac{\text{opp}}{\text{adj}}=\frac{8}{15}\approx0.533 .$$''', fmt='a number, e.g. `3/4`')
B.problem(S2, r'Solve $\cos2x=\dfrac12$ for $0\le x<\pi$.', 'set', [math.pi / 6, 5 * math.pi / 6],
          [r'Rename $u=2x$. What interval does $u$ run through when $0\le x<\pi$?', r'$0\le u<2\pi$, and $\cos u=\frac12$ there at $u=\frac\pi3$ and $u=\frac{5\pi}{3}$. Now halve.'],
          r'''**Rename.** $u=2x$, and $0\le x<\pi$ becomes $0\le u<2\pi$.

**Solve for $u$.** $\cos u=\frac12$: reference angle $\frac\pi3$, cosine positive in quadrants I and IV: $u=\frac\pi3$ or $u=\frac{5\pi}{3}$.

**Back to $x$.** $x=\frac u2$: $\;x=\dfrac\pi6$ or $x=\dfrac{5\pi}{6}$.

**Check.** $\cos\!\left(2\cdot\frac{5\pi}{6}\right)=\cos\frac{5\pi}{3}=\frac12$ ✓.''', fmt='a list of the two solutions')
B.problem(S2, r'Solve $\sin\theta=-0.3$ for $0\le\theta<2\pi$ (calculator: `asin`). Give both solutions.', 'set', [math.pi + math.asin(0.3), 2 * math.pi - math.asin(0.3)],
          [r'The principal value $\alpha=\arcsin(-0.3)$ is negative. The two solutions per turn are $\alpha$ and $\pi-\alpha$.',
           r'$\alpha\approx-0.3047$: add $2\pi$ to bring it into range. $\pi-\alpha\approx3.4463$ is already in range.'],
          r'''**Principal value.** $\alpha=\arcsin(-0.3)\approx-0.3047$.

**Two solutions per turn.** $\alpha$ and $\pi-\alpha$:
- $\alpha=-0.3047$ is not in $[0,2\pi)$; add $2\pi$: $\;5.9785$.
- $\pi-\alpha=3.1416+0.3047=3.4463$.

**Solutions:** $\theta\approx3.4463$ and $\theta\approx5.9785$ (quadrants III and IV, where the height is negative ✓).''', fmt='a list of two numbers')
B.problem(S2, r'Solve $2\cos^2x-\cos x-1=0$ for $0\le x<2\pi$. Give all solutions.', 'set', [0, 2 * math.pi / 3, 4 * math.pi / 3],
          [r'Let $c=\cos x$ and solve the quadratic $2c^2-c-1=0$ by factoring.', r'$(2c+1)(c-1)=0$, so $\cos x=1$ or $\cos x=-\frac12$. Solve each on the circle.'],
          r'''**Quadratic.** With $c=\cos x$: $2c^2-c-1=(2c+1)(c-1)=0$, so $c=1$ or $c=-\frac12$.

**$\cos x=1$:** the point $(1,0)$: $x=0$.

**$\cos x=-\frac12$:** reference angle $\frac\pi3$, quadrants II and III: $x=\frac{2\pi}{3}$ and $x=\frac{4\pi}{3}$.

**Three solutions:** $0,\ \dfrac{2\pi}{3},\ \dfrac{4\pi}{3}$.''', fmt='a list, e.g. `[0, pi/2, pi]`')
B.md(r'''
### Sinusoids
''')
B.problem(S3, r'The mains voltage is $v(t)=325\sin(\omega t)$ at $50$ Hz. Find $\omega$ in rad/s.', 'num', 100 * math.pi,
          [r'$\omega=2\pi f$.'],
          r'''$\omega=2\pi f=2\pi\cdot50=100\pi\approx$ **314.2 rad/s**. (Each cycle is $2\pi$ radians; there are 50 cycles per second.)''', fmt='rad/s')
B.problem(S3, r'A signal $y=A\sin(\omega t)+C$ swings between $-1$ and $7$ and completes $5$ cycles per second. Give $(A,\ C,\ \omega)$.', 'tuple', [4, 3, 10 * math.pi],
          [r'$C$ is the middle of the range, $A$ is half the peak-to-peak height.', r'$C=\frac{7+(-1)}{2}$, $A=\frac{7-(-1)}{2}$, and $\omega=2\pi f$ with $f=5$.'],
          r'''**Midline.** $C=\dfrac{\max+\min}{2}=\dfrac{7+(-1)}{2}=3$.

**Amplitude.** $A=\dfrac{\max-\min}{2}=\dfrac{7-(-1)}{2}=4$.

**Angular frequency.** $f=5$ Hz, so $\omega=2\pi\cdot5=10\pi\approx31.42$ rad/s.

Answer: $(4,\ 3,\ 10\pi)$. Check: $4\sin(\ldots)+3$ ranges from $-4+3=-1$ to $4+3=7$ ✓.''', fmt='a tuple `(A, C, omega)`')
B.problem(S3, r'Write $3\sin x+4\cos x=R\sin(x+\varphi)$ with $-\pi<\varphi\le\pi$. Give $(R,\ \varphi)$.', 'tuple', [5, math.atan2(4, 3)],
          [r'$R=\sqrt{a^2+b^2}$ and $\varphi$ is the direction of the point $(a,b)=(3,4)$.', r'`atan2(4, 3)` in a code cell gives $\varphi$.'],
          r'''$a=3$, $b=4$.

$R=\sqrt{9+16}=5$.

$\varphi=\operatorname{atan2}(4,3)=\arctan\frac43\approx0.9273$ rad (quadrant I).

So $3\sin x+4\cos x=5\sin(x+0.9273)$. Check at $x=0$: $4=5\sin0.9273=5\cdot0.8$ ✓.''', fmt='a tuple `(R, phi)`')
B.problem(S3, r'Add $5\sin\omega t$ and $5\sin\!\left(\omega t+\dfrac{2\pi}{3}\right)$. What is the amplitude of the sum?', 'num', 5,
          [r'Expand the second term with the addition formula so that the sum has the form $a\sin\omega t+b\cos\omega t$.',
           r'$\cos\frac{2\pi}{3}=-\frac12$, $\sin\frac{2\pi}{3}=\frac{\sqrt3}{2}$. Collect: $a=5-2.5$, $b=5\cdot\frac{\sqrt3}{2}$. Then $R=\sqrt{a^2+b^2}$.'],
          r'''**Expand the second term.**
$$5\sin\!\left(\omega t+\tfrac{2\pi}{3}\right)=5\sin\omega t\cos\tfrac{2\pi}{3}+5\cos\omega t\sin\tfrac{2\pi}{3}=-2.5\sin\omega t+\tfrac{5\sqrt3}{2}\cos\omega t .$$

**Add the first term.** $\;(5-2.5)\sin\omega t+\tfrac{5\sqrt3}{2}\cos\omega t=2.5\sin\omega t+4.330\cos\omega t$.

**Amplitude.** $R=\sqrt{2.5^2+\left(\tfrac{5\sqrt3}{2}\right)^2}=\sqrt{6.25+18.75}=\sqrt{25}=$ **5**.

**With phasors:** two arrows of length 5 with $120^\circ$ between them. Tip to tail they form two sides of an equilateral triangle; the sum is the third side, also of length 5 (pointing at $60^\circ$). This is why, in three-phase power, the sum of two phases equals minus the third.''')
B.problem(S3, r'What is the **largest value** that $2\sin x-3\cos x+1$ can take?', 'num', 1 + math.sqrt(13),
          [r'Combine $2\sin x-3\cos x$ into a single sinusoid $R\sin(x+\varphi)$. You only need $R$.', r'$R=\sqrt{2^2+(-3)^2}=\sqrt{13}$. A sinusoid of amplitude $R$ reaches at most $R$.'],
          r'''$2\sin x-3\cos x=R\sin(x+\varphi)$ with $R=\sqrt{2^2+(-3)^2}=\sqrt{13}$.

A sine never exceeds 1, so $R\sin(x+\varphi)\le\sqrt{13}$. Adding the offset:
$$\max=\sqrt{13}+1\approx4.606 .$$

(Not $2+3+1=6$: the sine and the cosine are never both at their extreme at the same $x$.)''')
B.md(r'''
### Triangles
''')
B.problem(S4, r'A triangle has sides $7$, $8$ and $9$. Find the angle (in radians) opposite the side of length $9$.', 'num', math.acos(2 / 7),
          [r'Three sides known → law of cosines, solved for the cosine.', r'$\cos C=\dfrac{7^2+8^2-9^2}{2\cdot7\cdot8}$, then `acos`.'],
          r'''$$\cos C=\frac{a^2+b^2-c^2}{2ab}=\frac{49+64-81}{2\cdot7\cdot8}=\frac{32}{112}=\frac27 .$$
$$C=\arccos\frac27\approx1.281\text{ rad}\ (\approx73.4^\circ).$$''', fmt='radians')
B.problem(S4, r'From a point $100$ m from the foot of a tower, the top is seen at an angle of elevation of $30^\circ$. How tall is the tower (in m)?', 'num', 100 * math.tan(math.radians(30)),
          [r'Sketch it: the 100 m is adjacent to the $30^\circ$ angle, the tower is opposite.', r'$\tan30^\circ=\dfrac{\text{height}}{100}$.'],
          r'''The ground distance is adjacent to the angle, the tower is opposite:
$$\tan30^\circ=\frac{h}{100}\quad\Rightarrow\quad h=100\tan30^\circ=\frac{100}{\sqrt3}\approx57.7\text{ m}.$$''', fmt='metres')
B.problem(S4, r'Two ships leave the same port. One sails $8$ km, the other $5$ km, on courses that differ by $60^\circ$. How far apart are they (in km)?', 'num', 7,
          [r'Two sides and the angle between them → law of cosines.'],
          r'''$$d^2=8^2+5^2-2\cdot8\cdot5\cdot\cos60^\circ=64+25-80\cdot\tfrac12=49,\qquad d=7\text{ km}.$$''', fmt='km')
B.code(r'''
# scratch cell: use Python as a calculator here
''')

B.md(r'''
---
# Finish the week

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
Double-click and write, without looking back:

1. The idea of the proof of $\cos(a-b)$ (what is computed twice?).
2. How to get $\sin2a$ and the three forms of $\cos2a$ from the addition formulas.
3. Why $\arcsin(\sin x)$ is not always $x$.
4. Why $\sin(2t+\frac\pi3)$ is shifted by $\frac\pi6$ and not $\frac\pi3$.
5. In two sentences: why "$a\sin x+b\cos x=R\sin(x+\varphi)$" means that adding sinusoids is adding arrows.

*Your answers:*

&nbsp;

### 3 · Physics strand — measure a period (1 hour)
The simulator below is a mass $m$ on a spring of stiffness $k$, with no friction. Its motion is a sinusoid with angular frequency $\omega_0=\sqrt{k/m}$ (you will *derive* this in Unit 9; today, test it).

**Predict before you look at the plots:** with $k=25$ N/m and $m=1$ kg, what are $\omega_0$ and the period $T=\frac{2\pi}{\omega_0}$? Then measure $T$ on the displacement plot (time between two peaks). Now set $k=100$: predict the new period first, then measure. What must you do to $m$ to double the period?
''')
B.code(r'''
lab('physics', exp='osc', F0=0, c=0, x0=1, k=25, m=1)
''')
B.md(r'''
### 4 · What comes next
**Week 3** asks the question that calculus starts from: what does a formula do *near* a point where it cannot be evaluated — such as $\dfrac{\sin x}{x}$ at $x=0$? The answer, a **limit**, uses the small-angle picture of week 1 and the identities of this week, and leads straight to the derivative.
''')

if __name__ == '__main__':
    B.write()
