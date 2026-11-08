"""Generate the Week 0 diagnostic notebook (44 problems, self-checking, per-topic report).
Run with the build venv:  python learn/tools/make_diagnostic.py
Expected answers are computed here with sympy/math and embedded (base64) so the notebook can check without spoiling."""
import sys, json, base64, math
sys.path.insert(0, 'learn/tools')
from mk import md, code, write
import sympy as sp

x = sp.Symbol('x')
R = sp.Rational
# (topic, statement, answer-format, kind, expected)
P = []
def add(topic, text, fmt, kind, exp): P.append((topic, text, fmt, kind, exp))

# ---------------- Algebra ----------------
add('Algebra', 'Solve $3x^2 - 5x - 2 = 0$.', 'a set (list) of the two roots, e.g. `[1, 2]`', 'set', [2, -1/3])
add('Algebra', 'Solve the system $2x + 3y = 12$, $\\;x - y = 1$.', 'a tuple `(x, y)`', 'tuple', [3, 2])
add('Algebra', 'Simplify $\\dfrac{x^2 - 9}{x^2 - x - 6}$ (for $x \\ne 3, -2$).', 'a sympy expression or string in `x`', 'sym', '(x+3)/(x+2)')
add('Algebra', 'How many **integers** satisfy $|2x - 3| < 5$?', 'an integer', 'num', 4)
add('Algebra', 'Compute the binomial coefficient $\\binom{10}{3}$.', 'an integer', 'num', 120)
# ---------------- Functions & trigonometry ----------------
add('Functions & trig', 'Let $f(x) = 2x + 1$ and $g(x) = x^2$. Compute $f(g(3)) + g(f(3))$.', 'a number', 'num', 19 + 49)
add('Functions & trig', 'For $f(x) = \\dfrac{2x + 3}{x - 1}$, find $f^{-1}(5)$.', 'a number', 'num', 8 / 3)
add('Functions & trig', 'Evaluate $\\sin\\frac{\\pi}{6} + \\cos\\frac{\\pi}{3} + \\tan\\frac{\\pi}{4}$.', 'a number', 'num', 2)
add('Functions & trig', 'Solve $\\sin x = \\tfrac12$ for $x \\in [0, 2\\pi)$.', 'a list of the two solutions in radians', 'set', [math.pi / 6, 5 * math.pi / 6])
add('Functions & trig', 'Simplify $\\dfrac{\\sin 2x}{2\\sin x}$.', 'a sympy expression or string in `x`', 'sym', 'cos(x)')
add('Functions & trig', 'A triangle has sides 5 and 7 with a $60^\\circ$ angle between them. Find the third side.', 'a number', 'num', math.sqrt(25 + 49 - 35))
# ---------------- Exponentials & logarithms ----------------
add('Exponentials & logs', 'Solve $2^{3x-1} = 32$.', 'a number', 'num', 2)
add('Exponentials & logs', 'Compute $\\log_{10} 2 + \\log_{10} 50$.', 'a number', 'num', 2)
add('Exponentials & logs', 'Compute $\\ln\\!\\left(e^{3}\\sqrt{e}\\right)$.', 'a number', 'num', 3.5)
add('Exponentials & logs', 'A sample of 80 g has a half-life of 5 days. How many grams remain after 12 days?', 'a number (grams)', 'num', 80 * 0.5 ** (12 / 5))
# ---------------- Limits ----------------
add('Limits', '$\\displaystyle\\lim_{x\\to 0}\\frac{\\sin 3x}{x}$', 'a number', 'num', 3)
add('Limits', '$\\displaystyle\\lim_{x\\to \\infty}\\frac{3x^2 + 2x}{5x^2 - 1}$', 'a number', 'num', 0.6)
add('Limits', '$\\displaystyle\\lim_{x\\to 2}\\frac{x^2 - 4}{x - 2}$', 'a number', 'num', 4)
# ---------------- Derivatives ----------------
add('Derivatives', 'Differentiate $x^3\\sin x$.', 'a sympy expression in `x`', 'sym', '3*x**2*sin(x) + x**3*cos(x)')
add('Derivatives', 'Differentiate $\\ln(1 + x^2)$.', 'a sympy expression in `x`', 'sym', '2*x/(1+x**2)')
add('Derivatives', 'Differentiate $e^{-x^2}$.', 'a sympy expression in `x`', 'sym', '-2*x*exp(-x**2)')
add('Derivatives', 'For $f(x) = \\dfrac{x^2 + 1}{x - 1}$, compute $f\'(2)$.', 'a number', 'num', -1)
add('Derivatives', 'At which $x > 0$ does $f(x) = x e^{-x}$ attain its maximum?', 'a number', 'num', 1)
add('Derivatives', 'What is the slope of the tangent to $y = x^3 - 2x$ at $x = 2$?', 'a number', 'num', 10)
# ---------------- Integrals ----------------
add('Integrals', '$\\displaystyle\\int_0^{\\pi} \\sin x\\,dx$', 'a number', 'num', 2)
add('Integrals', 'Find an antiderivative of $x e^{x}$.', 'a sympy expression in `x` (constant of integration not needed)', 'anti', '(x-1)*exp(x)')
add('Integrals', '$\\displaystyle\\int_0^{1} \\frac{dx}{1 + x^2}$', 'a number', 'num', math.pi / 4)
add('Integrals', '$\\displaystyle\\int_0^{\\infty} e^{-2x}\\,dx$', 'a number', 'num', 0.5)
add('Integrals', 'Find the area enclosed between $y = x$ and $y = x^2$.', 'a number', 'num', 1 / 6)
# ---------------- Series ----------------
add('Series', 'What is the coefficient of $x^4$ in the Taylor (Maclaurin) series of $e^x$?', 'a number', 'num', 1 / 24)
add('Series', 'What is the radius of convergence of $\\displaystyle\\sum_{n=1}^{\\infty}\\frac{x^n}{n}$?', 'a number', 'num', 1)
# ---------------- Vectors & matrices ----------------
add('Vectors & matrices', 'Compute the dot product $(1, 2, 3)\\cdot(4, -5, 6)$.', 'a number', 'num', 12)
add('Vectors & matrices', 'Compute the cross product $(1, 0, 0)\\times(0, 1, 0)$.', 'a tuple of three numbers', 'tuple', [0, 0, 1])
add('Vectors & matrices', 'Compute the determinant of $\\begin{pmatrix}2 & 1\\\\5 & 3\\end{pmatrix}$.', 'a number', 'num', 1)
add('Vectors & matrices', 'Find the eigenvalues of $\\begin{pmatrix}4 & 1\\\\2 & 3\\end{pmatrix}$.', 'a list of two numbers', 'set', [2, 5])
# ---------------- Complex numbers ----------------
add('Complex numbers', 'Compute $(3 + 4i)(1 - 2i)$.', 'a Python complex number, e.g. `3+4j`', 'complex', [11, -2])
add('Complex numbers', 'Compute $|(1 + i)^8|$.', 'a number', 'num', 16)
# ---------------- Physics & circuits ----------------
add('Physics & circuits', 'A stone is dropped from rest from a height of 20 m (take $g = 9.81\\,\\text{m/s}^2$, no air resistance). How long does it take to land?', 'seconds', 'num', math.sqrt(2 * 20 / 9.81))
add('Physics & circuits', 'A 2 kg block slides on a frictionless incline of $30^\\circ$. What is its acceleration? ($g = 9.81$)', 'm/s²', 'num', 9.81 * 0.5)
add('Physics & circuits', 'A 1.5 kg mass falls from rest through 3 m. What is its speed at the bottom? ($g = 9.81$)', 'm/s', 'num', math.sqrt(2 * 9.81 * 3))
add('Physics & circuits', '12 V is applied across a 100 Ω and a 300 Ω resistor **in parallel**. What total current is drawn?', 'amperes', 'num', 12 / 75)
add('Physics & circuits', 'A capacitor charges from 0 V through a resistor from a 5 V source. What is its voltage after exactly one time constant $\\tau = RC$?', 'volts', 'num', 5 * (1 - math.exp(-1)))
# ---------------- Probability ----------------
add('Probability', 'Two fair dice are rolled. What is the probability that the sum is 7?', 'a number between 0 and 1', 'num', 1 / 6)
add('Probability', 'A fair six-sided die is rolled. What is the expected value of the **square** of the result?', 'a number', 'num', 91 / 6)

# build key
key = {}
for i, (topic, text, fmt, kind, exp) in enumerate(P, 1):
    key[str(i)] = {'k': kind, 'a': exp, 't': topic}
KEY = base64.b64encode(json.dumps(key).encode()).decode()
topics = []
for t, *_ in P:
    if t not in topics: topics.append(t)

setup = '''
import base64, json, math, time
import numpy as np, sympy as sp
x = sp.Symbol('x')
_KEY = "%s"
_K = json.loads(base64.b64decode(_KEY).decode())
_FILE = 'diagnostic-results.json'
try:
    _R = json.load(open(_FILE))
except Exception:
    _R = {}

def _save():
    try: json.dump(_R, open(_FILE, 'w'))
    except Exception as e: print('(could not save results:', e, ')')

def _isclose(a, b):
    return abs(a - b) <= 5e-3 * max(1.0, abs(b))

def _correct(kind, ans, exp):
    if kind == 'num':
        return _isclose(float(ans), exp)
    if kind == 'sym':
        return sp.simplify(sp.sympify(ans) - sp.sympify(exp)) == 0
    if kind == 'anti':
        return sp.simplify(sp.diff(sp.sympify(ans), x) - sp.diff(sp.sympify(exp), x)) == 0
    if kind == 'set':
        a = sorted(float(v) for v in ans); e = sorted(exp)
        return len(a) == len(e) and all(_isclose(p, q) for p, q in zip(a, e))
    if kind == 'tuple':
        a = [float(v) for v in ans]
        return len(a) == len(exp) and all(_isclose(p, q) for p, q in zip(a, exp))
    if kind == 'complex':
        return abs(complex(ans) - complex(*exp)) < 1e-6
    return False

def check(n, ans):
    """Record and mark your answer. Your FIRST attempt counts for the diagnostic; retries are allowed but flagged."""
    if ans is None or (isinstance(ans, type(Ellipsis))):
        print('Write your answer first (replace the ... with it).'); return
    q = _K[str(n)]
    try: ok = bool(_correct(q['k'], ans, q['a']))
    except Exception as e: print('Could not read your answer:', e, '-- check the answer format.'); return
    rec = _R.get(str(n))
    if rec is None:
        _R[str(n)] = {'ok': ok, 't': time.time()}; _save()
        print('\\u2713 Correct' if ok else '\\u2717 Not correct (first attempt recorded)')
    else:
        print(('\\u2713 Correct now' if ok else '\\u2717 Still not correct') + ' -- first attempt was ' + ('correct' if rec['ok'] else 'wrong'))

def report():
    topics = %s
    done = {int(k): v for k, v in _R.items()}
    print('Answered: %%d / %d' %% len(done))
    print()
    rows = []
    for t in topics:
        ids = [int(i) for i, q in _K.items() if q['t'] == t]
        got = sum(1 for i in ids if done.get(i, {}).get('ok'))
        tried = sum(1 for i in ids if i in done)
        rows.append((t, got, tried, len(ids)))
        bar = '#' * got + '+' * (tried - got) + '.' * (len(ids) - tried)
        print(f'{t:<22} {got}/{len(ids)}  [{bar}]')
    print()
    print('# = correct first time, + = tried but wrong, . = not attempted')
    weak = [r[0] for r in sorted(rows, key=lambda r: (r[1] / r[3], r[0])) if r[2] == r[3] and r[1] / r[3] < 0.7]
    left = sum(r[3] - r[2] for r in rows)
    if left: print(left, 'problems not attempted yet -- finish them for a complete picture.')
    print('Areas to focus on first:', ', '.join(weak) if weak else 'none -- solid foundation')
    print()
    print('Copy this line and paste it back to your tutor:')
    print(json.dumps({'diag': {t: [g, tr, n] for t, g, tr, n in rows}}))
''' % (KEY, json.dumps(topics), len(P))

intro = '''
# Week 0 — Diagnostic

**Purpose:** find out exactly where your mathematics and physics are rusty, so the first term can be built around what you actually need. This is **not** an exam and nothing is graded for anyone else.

## Rules
- **44 problems** in 10 topics. Plan about **2–3 hours**; spread it over several sessions if you like (your first-attempt results are saved automatically).
- Work on **paper first**. Use Python only as a calculator (`math`, `numpy`) — **do not use sympy to solve the calculus problems** on the first attempt. That would measure sympy, not you.
- No books or search on the first attempt. If you are stuck, write `...` and move on — an honest "don't know" is the most useful answer.
- Your **first attempt** is what counts. You may retry afterwards (the cell tells you if it was right first time).
- Answer format is shown under each problem. Expressions can be given as sympy objects or strings, for example `'cos(x)'` or `3*x**2`.

## How to run
1. Press **Shift+Enter** on the cell below to load the checker (takes a few seconds the first time).
2. For each problem, replace `...` with your answer and run the cell.
3. At the end, run `report()`.
'''

cells = [md(intro), code(setup)]
cur = None; num = 0
for i, (topic, text, fmt, kind, exp) in enumerate(P, 1):
    if topic != cur:
        cur = topic
        cells.append(md(f'## {topic}'))
    cells.append(md(f'**Problem {i}.** {text}\n\n*Answer: {fmt}*'))
    cells.append(code(f'ans = ...\ncheck({i}, ans)'))
cells.append(md('## Your report\nRun the cell below when you are done (it can be run at any time).'))
cells.append(code('report()'))
write('learn/content/year1/w00-diagnostic.ipynb', cells)
print('wrote', len(P), 'problems,', len(cells), 'cells')
