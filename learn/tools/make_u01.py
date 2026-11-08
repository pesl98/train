"""Generate Unit 1 — Functions, trigonometry & limits (weeks 1-3).
Run with the build venv:  python learn/tools/make_u01.py
Answers are computed here and embedded (base64) so the notebook can mark without spoiling."""
import sys, json, base64, math
sys.path.insert(0, 'learn/tools')
from mk import md, code, write

W1 = 'Week 1 - Functions, radians, circle'
W2 = 'Week 2 - Identities & sinusoids'
W3 = 'Week 3 - Limits & continuity'
cells, P = [], []

def prob(week, text, fmt, kind, exp):
    n = len(P) + 1
    P.append((week, kind, exp))
    cells.append(md('**Problem %d.** %s\n\n*Answer:* %s' % (n, text, fmt)))
    cells.append(code('check(%d, ...)' % n))

def M(s): cells.append(md(s))
def C(s): cells.append(code(s))

# ------------------------------------------------------------------ intro
M(r'''
# Unit 1 — Functions, trigonometry & limits
*Weeks 1–3 of Term 1 · about 15 h/week in this notebook and on paper (the other 5 h are the physics strand and error review)*

The diagnostic said: algebra is solid, **trigonometry and limits are the weak link**, and everything in calculus stands on them. This unit rebuilds exactly that, in three weeks, with a *predict → run → explain* rhythm.

## How a week works
| Time | What |
|---|---|
| 6 h | **Read** the sections below with pencil in hand; re-derive every boxed result yourself on paper. |
| 6 h | **Problems on paper first**, then type the answer into the `check(n, ...)` cell. |
| 3 h | **Experiments** (the code cells): *predict on paper before you run.* |
| 15 min/day | **Unit-circle drill** (`drill()`), a different set each day. |
| end of week | **Teach-back**: write the section summary in your own words in the marked cell. Run `report()`. |

## Rules
- Paper first; Python is a calculator and a lab, not a solver. No `sympy.solve`/`limit` on a first attempt.
- Your **first attempt** at each problem is recorded; retries are allowed but flagged. Missed problem → write one line in the error log: `log(12, 'forgot the quadrant sign')`.
- **Done with a week** when you score ≥ 80 % first time, or ≥ 80 % when you redo the missed ones on a *different day*.
- Answers: numbers, lists `[a, b]`, or expressions as strings in `x`, e.g. `'cos(x)'`. Angles are **radians** unless stated. `pi` is available.

Run the setup cell below first (Shift+Enter).
''')
SETUP_INDEX = len(cells)
cells.append(None)  # setup cell filled in at the end

# ------------------------------------------------------------------ WEEK 1
M(r'''
---
# Week 1 — Functions, radians and the unit circle

## 1.1 Functions
A **function** assigns to every input in its **domain** exactly one output; the outputs form the **range**. You can hold it as a formula, a graph, a table — or as a Python `def`. They are the same object.

**Domain traps:** division by zero, even roots of negatives, logarithms of non-positives.

**Composition:** $(f\circ g)(x)=f(g(x))$ — apply $g$ first. Order matters: $f(g(3))\ne g(f(3))$ in general.

**Inverse:** $f^{-1}$ undoes $f$. It exists when $f$ is one-to-one. Method: write $y=f(x)$, solve for $x$, swap names. Graphically it is the reflection in $y=x$.

**Transformations** (start from $y=f(x)$):

| New graph | Effect |
|---|---|
| $f(x-a)$ | shift **right** by $a$ (inside the bracket acts "backwards") |
| $f(x)+b$ | shift up by $b$ |
| $c\,f(x)$ | stretch vertically by $c$ |
| $f(cx)$ | compress horizontally by $c$ |
| $f(-x)$ | mirror in the $y$-axis |

**Even / odd:** even means $f(-x)=f(x)$ (like $x^2$, $\cos x$); odd means $f(-x)=-f(x)$ (like $x^3$, $\sin x$).

### Experiment 1 — transformations
*Predict:* sketch $f(x)=x^3-x$, then sketch $f(x-1)$, $f(x)+1$, $2f(x)$, $f(2x)$. Then run.
''')
C(r'''
import matplotlib.pyplot as plt
f = lambda x: x**3 - x
xs = np.linspace(-2.5, 2.5, 400)
cases = [('f(x-1)', lambda x: f(x-1)), ('f(x)+1', lambda x: f(x)+1),
         ('2 f(x)', lambda x: 2*f(x)), ('f(2x)', lambda x: f(2*x))]
fig, axs = plt.subplots(2, 2, figsize=(9, 7), sharex=True, sharey=True)
for ax, (name, g) in zip(axs.flat, cases):
    ax.plot(xs, f(xs), color='0.7', label='f(x)')
    ax.plot(xs, g(xs), label=name)
    ax.set_ylim(-5, 5); ax.grid(True); ax.legend()
plt.show()
''')
M(r'''
## 1.2 Radians — the only angle unit calculus likes
The angle in radians is **arc length ÷ radius**: $\theta = s/r$. A full turn is $2\pi$ rad $=360^\circ$, so

$$\text{rad}=\text{deg}\cdot\frac{\pi}{180},\qquad \text{deg}=\text{rad}\cdot\frac{180}{\pi}.$$

Why radians: arc length is $s=r\theta$, sector area is $\tfrac12 r^2\theta$, and — the key fact for the whole course — for small $\theta$,
$$\sin\theta\approx\theta,\qquad \tan\theta\approx\theta,\qquad \cos\theta\approx 1-\tfrac{\theta^2}{2}\quad(\theta\text{ in radians}).$$
In degrees none of this is true, and every derivative formula would carry an ugly factor $\pi/180$.

**Rotation:** angular velocity $\omega=d\theta/dt$ in rad/s; a point at radius $r$ moves at speed $v=\omega r$. From revolutions per minute: $\omega=2\pi\cdot\text{rpm}/60$.

### Experiment 2 — how good is $\sin\theta\approx\theta$?
*Predict:* at $\theta=0.5$, what percent error do you expect? at $0.1$? Then run. Notice the error shrinks like $\theta^2$.
''')
C(r'''
print('  theta     sin(theta)   rel. error of "sin t ~ t"')
for th in [1, 0.5, 0.1, 0.05, 0.01]:
    print(f'{th:7.2f}   {math.sin(th):.6f}   {(th - math.sin(th)) / math.sin(th) * 100:8.4f} %')
print()
print('Classic mistake: math.sin() takes radians.')
print('sin(30 degrees) done wrong :', math.sin(30))
print('sin(30 degrees) done right :', math.sin(math.radians(30)))
''')
M(r'''
## 1.3 The unit circle
Put a point on the circle of radius 1 at angle $\theta$ measured counter-clockwise from the positive $x$-axis. Its coordinates **are** $(\cos\theta,\ \sin\theta)$. Hence $\cos^2\theta+\sin^2\theta=1$ and $\tan\theta=\sin\theta/\cos\theta$.

Do not memorise a table. Memorise one pattern, for $0^\circ,30^\circ,45^\circ,60^\circ,90^\circ$ (i.e. $0,\frac\pi6,\frac\pi4,\frac\pi3,\frac\pi2$):

$$\sin:\ \frac{\sqrt0}{2},\ \frac{\sqrt1}{2},\ \frac{\sqrt2}{2},\ \frac{\sqrt3}{2},\ \frac{\sqrt4}{2}\qquad\cos:\ \text{the same list reversed}.$$

Every other angle: reduce to a **reference angle** in the first quadrant, then fix the sign by quadrant — **A**ll positive in I, **S**in in II, **T**an in III, **C**os in IV. Useful reflections:

$$\sin(\pi-\theta)=\sin\theta,\quad \cos(\pi-\theta)=-\cos\theta,\quad \sin(\theta+\pi)=-\sin\theta,\quad \sin(\tfrac\pi2-\theta)=\cos\theta.$$

### Experiment 3 — see it
*Predict:* at $\theta = 5\pi/4$, are $\sin$ and $\cos$ positive or negative, and how big? Change `theta` and re-run until the picture is automatic.
''')
C(r'''
theta = 5 * pi / 4          # <- change me
fig, (a1, a2) = plt.subplots(1, 2, figsize=(10, 4.2), gridspec_kw={'width_ratios': [1, 1.4]})
t = np.linspace(0, 2 * np.pi, 400)
a1.plot(np.cos(t), np.sin(t), color='0.6'); a1.set_aspect('equal'); a1.grid(True)
a1.plot([0, math.cos(theta)], [0, math.sin(theta)], 'k')
a1.plot([math.cos(theta)] * 2, [0, math.sin(theta)], 'r', label='sin')
a1.plot([0, math.cos(theta)], [0, 0], 'b', label='cos'); a1.legend()
a2.plot(t, np.sin(t), 'r', label='sin'); a2.plot(t, np.cos(t), 'b', label='cos')
a2.axvline(theta % (2 * np.pi), color='k', ls=':'); a2.grid(True); a2.legend()
a2.set_xticks([k * np.pi / 2 for k in range(5)]); a2.set_xticklabels(['0', 'π/2', 'π', '3π/2', '2π'])
plt.show()
print(f'cos = {math.cos(theta):.4f}   sin = {math.sin(theta):.4f}   tan = {math.tan(theta):.4f}')
''')
M(r'''
### Daily drill (15 minutes, paper first)
`drill()` gives ten new questions each day. Work them out **without** a calculator, then enter the ten decimals into `drill_check`.
''')
C(r'''
drill()
''')
C(r'''
drill_check([...])
''')
M(r'''
### Week 1 problems
''')
prob(W1, 'How many **integers** lie in the domain of $f(x)=\\sqrt{9-x^2}$?', 'an integer', 'num', 7)
prob(W1, 'What is the minimum value of $f(x)=x^2-4x+7$? (Complete the square.)', 'a number', 'num', 3)
prob(W1, 'For $f(x)=3x-2$, compute $f^{-1}(10)$.', 'a number', 'num', 4)
prob(W1, 'Convert $135^\\circ$ to radians.', 'a number (radians)', 'num', 3 * math.pi / 4)
prob(W1, 'A circle has radius 4 m. What arc length subtends an angle of $0.75$ rad?', 'metres', 'num', 3)
prob(W1, 'Reduce $\\dfrac{7\\pi}{3}$ to the equivalent angle in $[0,2\\pi)$.', 'radians', 'num', math.pi / 3)
prob(W1, 'Compute $\\cos\\frac{2\\pi}{3}+\\sin\\frac{7\\pi}{6}$ exactly, then give the number.', 'a number', 'num', -1)
prob(W1, 'Compute $\\tan\\frac{3\\pi}{4}$.', 'a number', 'num', -1)
prob(W1, 'If $\\sin\\theta=\\frac35$ and $\\theta$ is in the **second quadrant**, find $\\cos\\theta$.', 'a number', 'num', -0.8)
prob(W1, 'Let $f(x)=x^2$ and $g(x)=f(x-2)+1$. Compute $g(5)$.', 'a number', 'num', 10)
prob(W1, 'Solve $\\cos\\theta=-\\frac{\\sqrt3}{2}$ for $\\theta\\in[0,2\\pi)$.', 'a list of the two solutions in radians', 'set', [5 * math.pi / 6, 7 * math.pi / 6])
prob(W1, 'A wheel of radius $0.3$ m turns at 120 rpm. How fast does a point on its rim move?', 'm/s', 'num', 0.3 * 120 * 2 * math.pi / 60)
M(r'''
### Week 1 teach-back
*Double-click this cell and write, in your own words (no looking back): (1) why calculus needs radians, (2) how you get $\sin$ and $\cos$ of any multiple of $\pi/6$ or $\pi/4$ from the first quadrant, (3) which transformation rule you keep getting wrong.*

&nbsp;

**Physics link (strand, 1 h):** open the [Physics Lab](/physics/index.html), choose *Oscillators*, and read off the period for a few amplitudes. Does a small-angle approximation hold? You will prove why in Unit 4.
''')

# ------------------------------------------------------------------ WEEK 2
M(r'''
---
# Week 2 — Trig identities, inverse functions, sinusoids

## 2.1 Identities
$$\sin^2 x+\cos^2 x=1\quad\Rightarrow\quad 1+\tan^2 x=\sec^2 x\ \ (\text{divide by }\cos^2x).$$

**Addition formulas** — the only ones worth memorising:
$$\sin(a\pm b)=\sin a\cos b\pm\cos a\sin b,\qquad \cos(a\pm b)=\cos a\cos b\mp\sin a\sin b.$$

Everything else drops out by setting $b=a$:
$$\sin 2a=2\sin a\cos a,\qquad \cos 2a=\cos^2a-\sin^2a=2\cos^2a-1=1-2\sin^2a.$$
Rearranged, the **power-reduction** forms you will integrate with in Unit 3:
$$\sin^2a=\frac{1-\cos 2a}{2},\qquad \cos^2a=\frac{1+\cos 2a}{2}.$$

(In Unit 6, Euler's formula will make all of these one-line consequences of $e^{i(a+b)}=e^{ia}e^{ib}$.)

### Experiment 4 — testing is not proving
A numerical test can *refute* an identity but never *prove* it. Run it, then notice which line fails.
''')
C(r'''
rng = np.random.default_rng(0)
t = rng.uniform(-10, 10, 1000); u = rng.uniform(-10, 10, 1000)
def test(name, lhs, rhs):
    err = np.max(np.abs(lhs - rhs))
    print(f'{name:<38} max error {err:9.2e}   ', 'looks true' if err < 1e-9 else 'FALSE')
test('sin(2t) = 2 sin t cos t',            np.sin(2*t), 2*np.sin(t)*np.cos(t))
test('cos(2t) = 1 - 2 sin^2 t',            np.cos(2*t), 1 - 2*np.sin(t)**2)
test('sin(t+u) = sin t cos u + cos t sin u', np.sin(t+u), np.sin(t)*np.cos(u) + np.cos(t)*np.sin(u))
test('sin(2t) = 2 sin t',                  np.sin(2*t), 2*np.sin(t))
test('sin(t+u) = sin t + sin u',           np.sin(t+u), np.sin(t) + np.sin(u))
''')
M(r'''
## 2.2 Inverse trigonometric functions
A sine takes each value infinitely often, so to invert it we restrict to one branch (the **principal value**):

| function | domain | range |
|---|---|---|
| $\arcsin$ | $[-1,1]$ | $[-\tfrac\pi2,\tfrac\pi2]$ |
| $\arccos$ | $[-1,1]$ | $[0,\pi]$ |
| $\arctan$ | $\mathbb R$ | $(-\tfrac\pi2,\tfrac\pi2)$ |

Trap: $\arcsin(\sin x)=x$ **only if** $x$ is in that range. $\arccos(\cos\tfrac{5\pi}{3})=\tfrac\pi3$, not $\tfrac{5\pi}{3}$.

**Solving $\sin x=c$** in $[0,2\pi)$: two solutions, $\alpha=\arcsin c$ and $\pi-\alpha$. For $\cos x=c$: $\pm\alpha$ (mod $2\pi$). For $\tan x=c$: $\alpha$ and $\alpha+\pi$. In code, `math.atan2(y, x)` returns the angle of the point $(x,y)$ in the correct quadrant — use it instead of $\arctan(y/x)$.

## 2.3 Sinusoids — the shape of AC and of every oscillator
$$y=A\sin(\omega t+\varphi)+C$$
$A$ amplitude · $\omega$ angular frequency (rad/s) · $f=\omega/2\pi$ in Hz · period $T=1/f=2\pi/\omega$ · $\varphi$ phase (the wave is shifted *left* by $\varphi/\omega$).

**Key result — combining two sinusoids of the same frequency:**
$$a\sin x+b\cos x=R\sin(x+\varphi),\qquad R=\sqrt{a^2+b^2},\quad \varphi=\operatorname{atan2}(b,a).$$
*Proof:* expand $R\sin(x+\varphi)=R\cos\varphi\,\sin x+R\sin\varphi\,\cos x$ and match $a=R\cos\varphi$, $b=R\sin\varphi$. This is the first appearance of the **phasor** idea: a sinusoid is a rotating arrow, and adding sinusoids is adding arrows.

**Triangles:** SOH-CAH-TOA; law of cosines $c^2=a^2+b^2-2ab\cos C$ (Pythagoras plus a correction); law of sines $a/\sin A=b/\sin B$.

### Experiment 5 — adding sinusoids
*Predict:* for $a=3,\ b=4$, what are the amplitude and the phase of the sum? Run, then change `a`, `b`.
''')
C(r'''
a, b = 3, 4                                  # <- change me
x_ = np.linspace(0, 4 * np.pi, 600)
R, ph = math.hypot(a, b), math.atan2(b, a)
plt.figure(figsize=(9, 3.6))
plt.plot(x_, a * np.sin(x_), '0.6', label='a sin x')
plt.plot(x_, b * np.cos(x_), '0.8', label='b cos x')
plt.plot(x_, a * np.sin(x_) + b * np.cos(x_), 'k', lw=3, alpha=0.4, label='a sin x + b cos x')
plt.plot(x_, R * np.sin(x_ + ph), 'r--', label=f'R sin(x+φ), R={R:.3f}, φ={ph:.3f}')
plt.grid(True); plt.legend(); plt.show()
''')
M(r'''
### Experiment 6 — three-phase power
The grid uses three sinusoids $120^\circ$ apart. *Predict:* what does their sum look like?
''')
C(r'''
x_ = np.linspace(0, 2 * np.pi, 600)
ph3 = [np.sin(x_ + k * 2 * np.pi / 3) for k in range(3)]
plt.figure(figsize=(9, 3.4))
for k, y in enumerate(ph3): plt.plot(x_, y, label=f'phase {k+1}')
plt.plot(x_, sum(ph3), 'k', lw=3, label='sum'); plt.grid(True); plt.legend(); plt.show()
print('largest |sum| =', float(np.max(np.abs(sum(ph3)))))
''')
M(r'''
### Week 2 problems
''')
prob(W2, 'If $\\sin x=0.6$ and $\\cos x>0$, find $\\sin 2x$.', 'a number', 'num', 0.96)
prob(W2, 'Compute $\\cos 75^\\circ$ using $\\cos(45^\\circ+30^\\circ)$.', 'a number', 'num', math.cos(math.radians(75)))
prob(W2, 'Simplify $\\dfrac{1-\\cos 2x}{2\\sin x}$.', 'an expression in `x`, e.g. `\'sin(x)\'`', 'sym', 'sin(x)')
prob(W2, 'Simplify $\\cos x\\cos 3x-\\sin x\\sin 3x$ to a single trigonometric function.', 'an expression in `x`', 'sym', 'cos(4*x)')
prob(W2, 'What is the period of $y=3\\sin(4\\pi t)$ (t in seconds)?', 'seconds', 'num', 0.5)
prob(W2, 'The mains voltage is $v(t)=325\\sin(\\omega t)$ at 50 Hz. Find $\\omega$.', 'rad/s', 'num', 100 * math.pi)
prob(W2, 'Compute $\\arcsin\\frac12+\\arccos\\frac12+\\arctan 1$.', 'a number', 'num', 3 * math.pi / 4)
prob(W2, 'Compute $\\arccos\\!\\left(\\cos\\frac{5\\pi}{3}\\right)$.', 'radians', 'num', math.pi / 3)
prob(W2, 'Write $3\\sin x+4\\cos x=R\\sin(x+\\varphi)$. Find $R$.', 'a number', 'num', 5)
prob(W2, 'For the same combination, find $\\varphi$ (in $(-\\pi,\\pi]$).', 'radians', 'num', math.atan2(4, 3))
prob(W2, 'Solve $\\cos 2x=\\frac12$ for $x\\in[0,\\pi)$.', 'a list of the two solutions in radians', 'set', [math.pi / 6, 5 * math.pi / 6])
prob(W2, 'A triangle has sides 7, 8 and 9. Find the angle opposite the side of length 9.', 'radians', 'num', math.acos(2 / 7))
prob(W2, 'Add $5\\sin\\omega t$ and $5\\sin(\\omega t+\\tfrac{2\\pi}{3})$. What is the amplitude of the sum?', 'a number', 'num', 5)
prob(W2, 'From 100 m away, the angle of elevation of a tower top is $30^\\circ$. How tall is the tower?', 'metres', 'num', 100 * math.tan(math.radians(30)))
M(r'''
### Week 2 teach-back
*Write, from memory: (1) how to derive the double-angle formulas from the addition formulas, (2) why $\arcsin(\sin x)\ne x$ in general, (3) in two sentences, why "a sin + b cos = R sin(x+φ)" is the idea behind AC circuit analysis.*

&nbsp;
''')

# ------------------------------------------------------------------ WEEK 3
M(r'''
---
# Week 3 — Limits and continuity

## 3.1 The idea
$\displaystyle\lim_{x\to a}f(x)=L$ means: *$f(x)$ can be made as close to $L$ as we like by taking $x$ close enough to $a$* ($x\ne a$). The value $f(a)$ itself is irrelevant — only the neighbourhood matters, and the left and right limits must agree. $\lim_{x\to\pm\infty}$ describes end behaviour; a limit that is $\pm\infty$ signals a vertical asymptote.

A limit may fail to exist: the sides disagree (a jump), the function blows up, or it oscillates forever ($\sin\frac1x$ at $0$).

## 3.2 Techniques
1. **Substitute.** If $f$ is continuous at $a$, you are done.
2. **$0/0$:** factor and cancel; or rationalise with the conjugate; or use a special limit.
3. **$x\to\infty$ with rational functions:** divide through by the highest power of $x$.

Limit laws: the limit of a sum, product or quotient is the sum, product or quotient of the limits (denominator limit $\ne0$).

**Special limits (radians!)**
$$\lim_{x\to0}\frac{\sin x}{x}=1,\qquad \lim_{x\to0}\frac{1-\cos x}{x^2}=\frac12,\qquad \lim_{n\to\infty}\Bigl(1+\frac1n\Bigr)^{n}=e,\qquad \lim_{h\to0}\frac{e^h-1}{h}=1.$$

*Why $\sin x/x\to1$* (sketch): on the unit circle, $\sin x< x<\tan x$ for small $x>0$; divide by $\sin x$ and squeeze.

### Experiment 7 — numerical limits, and where numerics lie
*Predict first.* The last rows of the second column are the lesson: floating-point **cancellation** destroys $1-\cos h$ for tiny $h$. A table suggests a limit; a derivation proves it.
''')
C(r'''
print('      h        sin(h)/h     (1-cos h)/h^2     (e^h-1)/h')
for h in [1, 0.1, 0.01, 0.001, 1e-4, 1e-6, 1e-8, 1e-10]:
    print(f'{h:8.0e}   {math.sin(h)/h:.10f}   {(1-math.cos(h))/h**2:.10f}   {math.expm1(h)/h:.10f}')
''')
C(r'''
# A limit that does not exist: sin(1/x) as x -> 0
xs = np.linspace(0.004, 0.3, 20000)
plt.figure(figsize=(9, 3.4)); plt.plot(xs, np.sin(1 / xs), lw=0.6); plt.grid(True)
plt.title('sin(1/x): oscillates ever faster, no limit at 0'); plt.show()
''')
M(r'''
### Experiment 8 — the number $e$ as a limit
*Predict:* does $(1+1/n)^n$ keep improving as $n$ grows? Look at the last rows.
''')
C(r'''
for n in [1, 10, 100, 1e4, 1e6, 1e8, 1e12, 1e15]:
    print(f'n = {n:8.0e}   (1+1/n)^n = {(1 + 1/n) ** n:.12f}')
print('e              =', math.e)
''')
M(r'''
## 3.3 Continuity
$f$ is **continuous at $a$** if $\lim_{x\to a}f(x)=f(a)$ — three things must hold: $f(a)$ exists, the limit exists, they are equal. Discontinuities come in kinds: *removable* (a hole), *jump*, *infinite* (asymptote), *oscillating*.

**Intermediate value theorem:** if $f$ is continuous on $[a,b]$ and $f(a),f(b)$ have opposite signs, there is a root in $(a,b)$. Halving the interval each time gives the **bisection method**; after $n$ steps the root is trapped in an interval of width $(b-a)/2^n$. Every root-finder in a simulator (including Voltaic's Newton solver) is a cousin of this idea.

**Epsilon–delta, in one paragraph.** "$\lim f=L$" is a game: an opponent names a tolerance $\varepsilon>0$ on the output; you must answer with a $\delta>0$ so that every $x$ within $\delta$ of $a$ lands within $\varepsilon$ of $L$. If you can always win, the limit is $L$. You will not need to grind these for engineering, but you should know what the words mean.

**Preview:** the derivative is *defined* as a limit,
$f'(x)=\displaystyle\lim_{h\to0}\frac{f(x+h)-f(x)}{h}$, which is where Unit 2 begins.

### Experiment 9 — write a root finder
Complete `bisect`, then test it. This is the first piece of code in the course that you write yourself.
''')
C(r'''
def bisect(f, a, b, tol=1e-9):
    """Return x in [a, b] with f(x) ~ 0, assuming f is continuous and f(a), f(b) have opposite signs.
    Halve the interval until it is narrower than tol."""
    ...

test_bisect(bisect)
''')
M(r'''
### Week 3 problems
''')
prob(W3, '$\\displaystyle\\lim_{x\\to3}\\frac{x^2-9}{x-3}$', 'a number', 'num', 6)
prob(W3, '$\\displaystyle\\lim_{x\\to0}\\frac{\\sqrt{x+4}-2}{x}$ *(hint: conjugate)*', 'a number', 'num', 0.25)
prob(W3, '$\\displaystyle\\lim_{x\\to\\infty}\\frac{2x^3-x}{x^3+5x^2}$', 'a number', 'num', 2)
prob(W3, '$\\displaystyle\\lim_{x\\to0}\\frac{\\sin 5x}{\\sin 2x}$', 'a number', 'num', 2.5)
prob(W3, '$\\displaystyle\\lim_{x\\to0}\\frac{1-\\cos x}{x^2}$', 'a number', 'num', 0.5)
prob(W3, '$\\displaystyle\\lim_{x\\to0}\\frac{1-\\cos 2x}{x^2}$', 'a number', 'num', 2)
prob(W3, '$\\displaystyle\\lim_{n\\to\\infty}\\Bigl(1+\\frac2n\\Bigr)^{n}$', 'a number', 'num', math.exp(2))
prob(W3, '$\\displaystyle\\lim_{x\\to\\infty}\\left(\\sqrt{x^2+x}-x\\right)$ *(hint: conjugate)*', 'a number', 'num', 0.5)
prob(W3, 'Find $k$ so that $f(x)=\\begin{cases}kx+1 & x\\le2\\\\ x^2-k & x>2\\end{cases}$ is continuous.', 'a number', 'num', 1)
prob(W3, 'Starting from $[0,1]$, how many bisection steps guarantee an interval narrower than $10^{-6}$?', 'an integer', 'num', 20)
prob(W3, 'How many **vertical asymptotes** does $f(x)=\\dfrac{x+1}{(x-2)(x+1)(x+3)}$ have?', 'an integer', 'num', 2)
_th = 0.25
prob(W3, 'A pendulum model replaces $\\sin\\theta$ by $\\theta$. At $\\theta=0.25$ rad, what is the relative error $(\\theta-\\sin\\theta)/\\sin\\theta$ in **percent**?', 'a number (percent)', 'num', (_th - math.sin(_th)) / math.sin(_th) * 100)
M(r'''
### Week 3 teach-back
*Write: (1) the three techniques for a $0/0$ limit, with one example each; (2) why a table of values cannot prove a limit (use Experiment 7); (3) how the intermediate value theorem guarantees bisection works.*

&nbsp;

---
# Unit review
Run `report()` below. Then:
1. Redo missed problems **on a different day** (the cell tells you if you got it right first time).
2. Read your `errors()` log: which *type* of mistake repeats — sign, quadrant, algebra slip, concept?
3. Paste the report line back to your tutor. If every week is ≥ 80 %, Unit 2 (derivatives) starts; otherwise we plan a short patch week.
''')
C(r'''
report()
''')
C(r'''
errors()
''')

# ------------------------------------------------------------------ setup cell
key = {str(i): {'k': k, 'a': a, 't': w} for i, (w, k, a) in enumerate(P, 1)}
KEY = base64.b64encode(json.dumps(key).encode()).decode()
weeks = [W1, W2, W3]

SETUP = r'''
import base64, json, math, time, datetime, random
from fractions import Fraction
import numpy as np, sympy as sp
from math import pi
x = sp.Symbol('x')
_K = json.loads(base64.b64decode("@@KEY@@").decode())
_FILE, _EFILE = 'u01-results.json', 'u01-errors.json'
def _load(f, d):
    try: return json.load(open(f))
    except Exception: return d
_R = _load(_FILE, {}); _E = _load(_EFILE, [])
def _save(f, o):
    try: json.dump(o, open(f, 'w'))
    except Exception as e: print('(could not save:', e, ')')

def _isclose(a, b): return abs(a - b) <= 5e-3 * max(1.0, abs(b))

def _correct(kind, ans, exp):
    if kind == 'num': return _isclose(float(ans), exp)
    if kind == 'sym':
        a, e = sp.sympify(ans), sp.sympify(exp)
        if sp.simplify(a - e) == 0: return True
        pts = [0.3, 0.7, 1.1, 1.9, 2.6]
        return all(abs(complex((a - e).subs(x, p).evalf())) < 1e-9 for p in pts)
    if kind == 'set':
        a = sorted(float(v) for v in ans); e = sorted(exp)
        return len(a) == len(e) and all(_isclose(p, q) for p, q in zip(a, e))
    return False

def check(n, ans):
    """Mark an answer. Your FIRST attempt is what counts; retries are flagged."""
    if ans is None or isinstance(ans, type(Ellipsis)):
        print('Write your answer first (replace the ... with it).'); return
    q = _K[str(n)]
    try: ok = bool(_correct(q['k'], ans, q['a']))
    except Exception as e: print('Could not read your answer:', e, '-- check the answer format.'); return
    rec = _R.get(str(n))
    if rec is None:
        _R[str(n)] = {'ok': ok, 't': time.time()}; _save(_FILE, _R)
        print('✓ Correct' if ok else '✗ Not correct (first attempt recorded). Log it: log(%d, "what went wrong")' % n)
    else:
        print(('✓ Correct now' if ok else '✗ Still not correct') + ' -- first attempt was ' + ('correct' if rec['ok'] else 'wrong'))

def log(n, note):
    _E.append({'n': n, 'note': note, 'd': str(datetime.date.today())}); _save(_EFILE, _E); print('logged.')

def errors():
    if not _E: print('No errors logged yet.'); return
    for e in _E: print(f"{e['d']}  problem {e['n']}: {e['note']}")

def report():
    weeks = @@WEEKS@@
    done = {int(k): v for k, v in _R.items() if k.isdigit()}
    print('Answered: %d / %d\n' % (len(done), len(_K)))
    rows = []
    for w in weeks:
        ids = [int(i) for i, q in _K.items() if q['t'] == w]
        got = sum(1 for i in ids if done.get(i, {}).get('ok')); tried = sum(1 for i in ids if i in done)
        rows.append((w, got, tried, len(ids)))
        print(f"{w:<40} {got:>2}/{len(ids)}  [" + '#' * got + '+' * (tried - got) + '.' * (len(ids) - tried) + ']')
    print('\n# = correct first time, + = tried but wrong, . = not attempted')
    for w, g, t, n in rows:
        if t < n: print(f'{w}: {n - t} not attempted yet')
        elif g / n < 0.8: print(f'{w}: below 80% -- redo the missed ones on a different day')
    dr = _R.get('drills', [])
    if dr: print('Drills done:', len(dr), ' average score: %.0f%%' % (100 * sum(s / n for _, s, n in dr) / len(dr)))
    print('\nPaste this line back to your tutor:')
    print(json.dumps({'u01': {w: [g, t, n] for w, g, t, n in rows}, 'drills': len(dr), 'errors': len(_E)}))

# ---- unit-circle drill
def _plabel(fr):
    n, d = fr.numerator, fr.denominator
    if n == 0: return '0'
    return ('pi' if n == 1 else f'{n}pi') + ('' if d == 1 else f'/{d}')
_DR = {}
def drill(n=10, seed=None):
    """Ten new unit-circle questions per day. Answer with drill_check([...])."""
    seed = datetime.date.today().toordinal() if seed is None else seed
    rng = random.Random(seed)
    pool = sorted({Fraction(k, 6) for k in range(12)} | {Fraction(k, 4) for k in range(8)})
    qs = []
    while len(qs) < n:
        a = rng.choice(pool); f = rng.choice(['sin', 'cos', 'tan'])
        th = float(a) * math.pi
        if f == 'tan' and abs(math.cos(th)) < 1e-9: continue
        qs.append((f, a, getattr(math, f)(th)))
    _DR['qs'] = qs
    for i, (f, a, _) in enumerate(qs, 1): print(f'{i:>2}.  {f}({_plabel(a)})')
    print(f'\nNow: drill_check([...])  with {n} numbers (decimals fine, e.g. math.sqrt(3)/2).')

def drill_check(ans):
    qs = _DR.get('qs')
    if not qs: print('Run drill() first.'); return
    if len(ans) != len(qs) or any(isinstance(v, type(Ellipsis)) for v in ans):
        print(f'Give exactly {len(qs)} numbers.'); return
    s = 0
    for i, ((f, a, v), g) in enumerate(zip(qs, ans), 1):
        ok = abs(float(g) - v) < 0.01; s += ok
        print(f'{i:>2}. {f}({_plabel(a)}) = {v:+.4f}   ' + ('✓' if ok else f'✗ (you said {float(g):+.4f})'))
    print(f'\nScore {s}/{len(qs)}')
    _R.setdefault('drills', []).append([str(datetime.date.today()), s, len(qs)]); _save(_FILE, _R)

# ---- test harness for the bisection experiment
def test_bisect(bisect):
    cases = [('x^2 - 2 on [0,2]', lambda t: t * t - 2, 0, 2, math.sqrt(2)),
             ('cos x on [0,2]', math.cos, 0, 2, math.pi / 2),
             ('x^3 - x - 1 on [1,2]', lambda t: t ** 3 - t - 1, 1, 2, 1.324717957244746),
             ('decreasing: 1 - x^2 on [0,3]', lambda t: 1 - t * t, 0, 3, 1.0)]
    allok = True
    for name, f, a, b, true in cases:
        try: r = bisect(f, a, b, 1e-9)
        except Exception as e: print('✗', name, 'raised', repr(e)); allok = False; continue
        if r is None: print('✗', name, '-> your function returned None (fill in the body and return the root)'); allok = False; continue
        ok = abs(r - true) < 1e-6; allok &= ok
        print('✓' if ok else '✗', name, '->', r)
    print('\nAll tests passed.' if allok else '\nSome tests failed -- note that f can be decreasing too.')

print('Unit 1 ready. Results are saved in this notebook\'s storage as', _FILE)
'''.replace('@@KEY@@', KEY).replace('@@WEEKS@@', json.dumps(weeks))
cells[SETUP_INDEX] = code(SETUP)

write('learn/content/year1/u01-functions-trig-limits.ipynb', cells)
print('cells:', len(cells), 'problems:', len(P))
