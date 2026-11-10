# ---------------------------------------------------------------------------
# Personal University - notebook runtime. This file is embedded (by nbkit.py)
# in the first code cell of every notebook, so a notebook is self-contained.
# It gives the student:  check / hint / solution   graded problems
#                        ask                       quick "check yourself" questions
#                        mistake / mistakes        the error log
#                        report                    progress per section
#                        explore                   sliders on any Python function
#                        lab                       embed one of the simulators
# _DATA (base64 JSON with answers, hints, solutions) is defined just above.
# ---------------------------------------------------------------------------
import base64, json, math, time, datetime, random
from fractions import Fraction
import numpy as np, sympy as sp
import matplotlib.pyplot as plt
from IPython.display import display, Markdown, HTML

pi, e = math.pi, math.e
x, t, theta = sp.symbols('x t theta')
plt.rcParams.update({'figure.figsize': (8, 3.6), 'axes.grid': True, 'grid.alpha': 0.35,
                     'figure.dpi': 96, 'axes.axisbelow': True, 'lines.linewidth': 2})


def _smart(name, npname=None, spname=None):
    mf, nf, sf = getattr(math, name), getattr(np, npname or name), getattr(sp, spname or name)

    def f(v):
        if isinstance(v, sp.Basic): return sf(v)
        if isinstance(v, (np.ndarray, list, tuple)): return nf(np.asarray(v, dtype=float))
        return mf(v)
    f.__name__ = name
    f.__doc__ = name + '(v): works on numbers (radians), numpy arrays and sympy expressions.'
    return f


sin, cos, tan, exp, sqrt = (_smart(k) for k in ['sin', 'cos', 'tan', 'exp', 'sqrt'])
asin, acos, atan = _smart('asin', 'arcsin'), _smart('acos', 'arccos'), _smart('atan', 'arctan')
arcsin, arccos, arctan = asin, acos, atan
ln = _smart('log')
log10 = _smart('log10', 'log10', 'log')
atan2, degrees, radians, hypot = math.atan2, math.degrees, math.radians, math.hypot

_D = json.loads(base64.b64decode(_DATA).decode())
_ID = _D['id']
_FILE = _ID + '-results.json'


def _load():
    try:
        with open(_FILE) as fh: s = json.load(fh)
    except Exception:
        s = {}
    for k, d in (('p', {}), ('q', {}), ('drills', []), ('mistakes', [])): s.setdefault(k, d)
    return s


_S = _load()


def _summary():
    P = _D['p']
    got = sum(1 for k in P if _S['p'].get(k, {}).get('ok'))
    later = sum(1 for k in P if not _S['p'].get(k, {}).get('ok') and _S['p'].get(k, {}).get('later'))
    tried = sum(1 for k in P if k in _S['p'])
    qd = sum(1 for k in _D['q'] if _S['q'].get(k, {}).get('ok'))
    return {'got': got, 'later': later, 'tried': tried, 'n': len(P), 'q': qd, 'nq': len(_D['q']),
            'drills': len(_S['drills']), 'mistakes': len(_S['mistakes'])}


def _save():
    _S['id'], _S['title'], _S['sum'], _S['updated'] = _ID, _D['title'], _summary(), time.time()
    try:
        with open(_FILE, 'w') as fh: json.dump(_S, fh)
    except Exception as err:
        print('(could not save progress:', err, ')')


# ----------------------------------------------------------------- comparing answers
_LOC = {s: sp.Symbol(s) for s in ['x', 't', 'h', 'n', 'a', 'b', 'c', 'k', 'y', 'u', 'r', 'theta', 'omega', 'phi', 'A', 'R', 'T', 'L', 'C']}
_LOC.update(pi=sp.pi, e=sp.E, ln=sp.log, arcsin=sp.asin, arccos=sp.acos, arctan=sp.atan)


def _sym(v):
    if isinstance(v, str): return sp.sympify(v.replace('^', '**'), locals=_LOC)
    return sp.sympify(v)


def _num(v):
    if isinstance(v, str): v = _sym(v)
    if isinstance(v, sp.Basic): v = v.evalf()
    return float(v)


def _close(a, b): return abs(a - b) <= 5e-3 * max(1.0, abs(b))


def _same(a, b):
    d = a - b
    try:
        if sp.simplify(d) == 0: return True
    except Exception:
        pass
    fs = sorted(d.free_symbols, key=str)
    if not fs: return abs(complex(d.evalf())) < 1e-7
    rng, good = random.Random(7), 0
    for _ in range(40):
        sub = {s: rng.uniform(0.2, 1.4) for s in fs}
        try:
            v, ref = complex(d.subs(sub).evalf()), complex(b.subs(sub).evalf())
        except Exception:
            continue
        if v != v or ref != ref: continue
        if abs(v) > 1e-7 * (1 + abs(ref)): return False
        good += 1
        if good >= 6: return True
    return good >= 3


def _correct(kind, ans, exp_):
    if kind == 'num': return _close(_num(ans), exp_)
    if kind == 'sym': return _same(_sym(ans), _sym(exp_))
    if kind == 'anti':  # an antiderivative: its derivative must equal the integrand
        return _same(sp.diff(_sym(ans), _LOC['x']), _sym(exp_))
    if kind == 'set':
        a, b = sorted(_num(v) for v in ans), sorted(exp_)
        return len(a) == len(b) and all(_close(p, q) for p, q in zip(a, b))
    if kind == 'tuple':
        a = [_num(v) for v in ans]
        return len(a) == len(exp_) and all(_close(p, q) for p, q in zip(a, exp_))
    if kind == 'choice': return str(ans).strip().lower().strip('().') == str(exp_).lower()
    if kind == 'fn':  # ans is a function; exp_ = list of [args, expected]
        for args, want in exp_:
            got = ans(*args)
            if got is None or not _close(float(got), want): return False
        return True
    raise ValueError('unknown kind ' + kind)


def _blank(ans): return ans is None or ans is Ellipsis or (isinstance(ans, (list, tuple)) and any(v is Ellipsis for v in ans))


def _md(s): display(Markdown(s))


# ----------------------------------------------------------------- graded problems
def check(n, ans=None):
    """Mark your answer to Problem n. The FIRST attempt is the one that counts."""
    k = str(n)
    if k not in _D['p']: print('There is no problem', n, 'in this notebook.'); return
    if _blank(ans): print('Replace the ... with your answer, then run the cell again.'); return
    q = _D['p'][k]
    try:
        ok = bool(_correct(q['k'], ans, q['a']))
    except Exception as err:
        print('I could not read that answer (%s). Expected format: %s' % (err, q['f'])); return
    rec = _S['p'].get(k)
    if rec is None:
        _S['p'][k] = {'ok': ok, 't': time.time(), 'tries': 1, 'sol': False}
        if ok: print('✓ Correct, first time.  solution(%d) shows a model answer - compare it with your own working.' % n)
        else: print('✗ Not correct. This first attempt is recorded.\n  Next: re-check your working, then hint(%d). If still stuck: solution(%d).\n  Afterwards write one line: mistake(%d, "what went wrong")' % (n, n, n))
    else:
        rec['tries'] = rec.get('tries', 1) + 1
        if ok and not rec['ok']: rec['later'] = True
        print(('✓ Correct now' if ok else '✗ Still not correct - try hint(%d)' % n) + '   (first attempt was ' + ('correct' if rec['ok'] else 'wrong') + ')')
    _save()


def hint(n, all=False):
    """Show the next hint for Problem n (each call reveals one more)."""
    k = str(n); q = _D['p'].get(k)
    if q is None: print('There is no problem', n); return
    hs = q.get('h') or []
    if not hs: print('No hint for this one - after an honest attempt go to solution(%d).' % n); return
    used = _S.setdefault('hints', {}).get(k, 0)
    upto = len(hs) if all else min(used + 1, len(hs))
    for i in range(upto): _md('**Hint %d of %d.** %s' % (i + 1, len(hs), hs[i]))
    if upto == len(hs): print('That was the last hint. After an honest attempt: solution(%d)' % n)
    _S['hints'][k] = upto
    _save()


def solution(n, force=False):
    """Show the full worked solution of Problem n. Attempt the problem first."""
    k = str(n); q = _D['p'].get(k)
    if q is None: print('There is no problem', n); return
    rec = _S['p'].get(k)
    if rec is None and not force:
        print('Attempt it first: enter an answer with check(%d, ...).\nTruly stuck even after hint(%d)?  ->  solution(%d, force=True)' % (n, n, n)); return
    if rec is not None and not rec['ok']: rec['sol'] = True
    _md('#### Worked solution - Problem %d\n\n%s' % (n, q['s']))
    _save()


# ----------------------------------------------------------------- quick checks
def ask(n, ans=None):
    """Check yourself: unlimited tries, not graded. Explains the answer once you have it."""
    k = str(n); q = _D['q'].get(k)
    if q is None: print('There is no check-yourself question', n); return
    if _blank(ans): print('Replace the ... with your answer, then run the cell again.'); return
    try:
        ok = bool(_correct(q['k'], ans, q['a']))
    except Exception as err:
        print('I could not read that answer (%s). Expected format: %s' % (err, q['f'])); return
    rec = _S['q'].setdefault(k, {'ok': False, 'tries': 0}); rec['tries'] += 1
    if ok:
        rec['ok'] = True
        _md('✓ **Right.** ' + q.get('why', ''))
    else:
        nud = q.get('nudge', '')
        if rec['tries'] >= 3:
            _md('✗ Not yet - here is the reasoning, read it and then redo it yourself without looking:\n\n' + q.get('why', nud))
        else:
            _md('✗ Not yet. ' + (nud or 'Re-read the paragraph just above and try once more.'))
    _save()


# ----------------------------------------------------------------- error log and report
def mistake(n, note):
    """Record in one line what went wrong in Problem n."""
    _S['mistakes'].append({'n': n, 'note': note, 'd': str(datetime.date.today())}); _save(); print('logged.')


def mistakes():
    if not _S['mistakes']: print('No mistakes logged yet.'); return
    for m in _S['mistakes']: print('%s  problem %s: %s' % (m['d'], m['n'], m['note']))


def report():
    """Progress for this notebook, per section."""
    P, done = _D['p'], _S['p']
    print(_D['title']); print('=' * len(_D['title']))
    rows = []
    for sec in _D['secs']:
        ids = [k for k in P if P[k]['sec'] == sec]
        if not ids: continue
        got = sum(1 for k in ids if done.get(k, {}).get('ok'))
        tried = sum(1 for k in ids if k in done)
        bar = ''.join('#' if done.get(k, {}).get('ok') else ('+' if done.get(k, {}).get('later') else ('x' if k in done else '.')) for k in ids)
        rows.append((sec, got, tried, len(ids)))
        print('%-44s %2d/%-2d  [%s]' % (sec[:44], got, len(ids), bar))
    s = _summary()
    print('\n# correct first time   + correct on a retry   x not yet correct   . not attempted')
    print('Problems: %d/%d first time (%d more on retry).   Check-yourself: %d/%d.' % (s['got'], s['n'], s['later'], s['q'], s['nq']))
    peeked = [k for k in P if done.get(k, {}).get('sol')]
    if peeked: print('Solution opened before solving:', ', '.join(peeked), ' -> redo these on another day without the solution.')
    if s['drills']: print('Drills done: %d, average %.0f%%' % (s['drills'], 100 * sum(a / b for _, a, b in _S['drills']) / s['drills']))
    if s['tried'] < s['n']: print('Still to attempt: %d problems.' % (s['n'] - s['tried']))
    elif s['got'] >= 0.8 * s['n']: print('>= 80% first time: this notebook is DONE. Move on.')
    else: print('Below 80% first time: redo the x problems on a different day, then move on once they are right.')
    print('\nThe course map (hub page) picks this up automatically. Line for your tutor:')
    print(json.dumps({'nb': _ID, 'sections': {r[0]: list(r[1:]) for r in rows}, 'sum': s}))
    _save()


# ----------------------------------------------------------------- interactive helpers
def explore(fn, **controls):
    """Sliders for a function.  explore(f, a=(min, max, step, start), mode=['x', 'y'], show=True)
    Drag a slider and fn is re-run with the new values. Without widgets it runs once with the start values."""
    start = {}
    for k, v in controls.items():
        if isinstance(v, tuple): start[k] = v[3] if len(v) > 3 else v[0]
        elif isinstance(v, list): start[k] = v[0]
        else: start[k] = v
    try:
        import ipywidgets as W
        ws = {}
        for k, v in controls.items():
            if isinstance(v, tuple):
                isint = all(isinstance(q, int) and not isinstance(q, bool) for q in v)
                cls = W.IntSlider if isint else W.FloatSlider
                kw = dict(min=v[0], max=v[1], step=v[2] if len(v) > 2 else (1 if isint else (v[1] - v[0]) / 100), value=start[k],
                          description=k, continuous_update=False, layout=W.Layout(width='460px'))
                if not isint: kw['readout_format'] = '.3g'
                ws[k] = cls(**kw)
            elif isinstance(v, list): ws[k] = W.Dropdown(options=v, value=v[0], description=k)
            elif isinstance(v, bool): ws[k] = W.Checkbox(value=v, description=k)
            else: ws[k] = W.fixed(v)
        W.interact(fn, **ws)
    except Exception:
        fn(**start)
        print('(Sliders are not available here: change the numbers in the explore(...) line and re-run the cell.)')


def _site():
    try:
        import js
        href = str(js.location.href)
        if '/learn/notebooks/' in href: return href.split('/learn/notebooks/')[0] + '/'
    except Exception:
        pass
    return 'https://pesl98.github.io/train/'


def lab(name, height=620, **params):
    """Embed a simulator in the notebook:  lab('physics', exp='osc')  /  lab('voltaic')  /  lab('robotics')"""
    from urllib.parse import urlencode
    url = _site() + name + '/index.html' + ('#' + urlencode(params) if params else '')
    display(HTML('<p><a href="%s" target="_blank" rel="noopener">Open the %s lab in its own tab ↗</a> (more room)</p>'
                 '<iframe src="%s" style="width:100%%;height:%dpx;border:1px solid #bbb;border-radius:8px" loading="lazy"></iframe>' % (url, name, url, height)))


def table(headers, rows, fmt='%.6g'):
    """Print a small aligned table. rows: list of lists."""
    cells = [[(fmt % v) if isinstance(v, float) else str(v) for v in r] for r in rows]
    w = [max(len(str(hd)), *(len(r[i]) for r in cells)) for i, hd in enumerate(headers)]
    print('   '.join(str(hd).rjust(w[i]) for i, hd in enumerate(headers)))
    print('   '.join('-' * w[i] for i in range(len(headers))))
    for r in cells: print('   '.join(r[i].rjust(w[i]) for i in range(len(headers))))


# ----------------------------------------------------------------- unit-circle drill (Unit 1)
def _plabel(fr):
    a, b = fr.numerator, fr.denominator
    if a == 0: return '0'
    return ('pi' if a == 1 else '%dpi' % a) + ('' if b == 1 else '/%d' % b)


_DR = {}


def drill(count=10, seed=None):
    """Ten unit-circle questions, new every day. Work them out on paper, then drill_check([...])."""
    seed = datetime.date.today().toordinal() if seed is None else seed
    rng = random.Random(seed)
    pool = sorted({Fraction(k, 6) for k in range(12)} | {Fraction(k, 4) for k in range(8)})
    qs = []
    while len(qs) < count:
        a = rng.choice(pool); f = rng.choice(['sin', 'cos', 'tan']); th = float(a) * math.pi
        if f == 'tan' and abs(math.cos(th)) < 1e-9: continue
        qs.append((f, a, getattr(math, f)(th)))
    _DR['qs'] = qs
    for i, (f, a, _) in enumerate(qs, 1): print('%2d.  %s(%s)' % (i, f, _plabel(a)))
    print('\nNow: drill_check([...]) with %d numbers. You may type exact values, e.g. sqrt(3)/2 or -1/2.' % count)


def drill_check(ans):
    qs = _DR.get('qs')
    if not qs: print('Run drill() first.'); return
    if _blank(ans) or len(ans) != len(qs): print('Give exactly %d numbers.' % len(qs)); return
    s = 0
    for i, ((f, a, v), g) in enumerate(zip(qs, ans), 1):
        ok = abs(_num(g) - v) < 0.01; s += ok
        print('%2d. %s(%s) = %+.4f   ' % (i, f, _plabel(a), v) + ('✓' if ok else '✗ (you said %+.4f)' % _num(g)))
    print('\nScore %d/%d' % (s, len(qs)))
    _S['drills'].append([str(datetime.date.today()), s, len(qs)]); _save()


# ----------------------------------------------------------------- calculus helpers (Unit 2 onwards)
def nderiv(f, x0, h=1e-5):
    """Numerical derivative of f at x0 (central difference). Works on numbers and on numpy arrays."""
    return (f(x0 + h) - f(x0 - h)) / (2 * h)


def compare(f, fprime, lo=-3.0, hi=3.0):
    """Test a derivative you worked out by hand:  compare(f, your_derivative).
    Plots the numerical slope of f and your formula; if they coincide, your derivative is (almost certainly) right.
    Write both with v as the variable, e.g.  compare(lambda v: v**2 * sin(v), lambda v: 2*v*sin(v) + v**2*cos(v))"""
    xs = np.linspace(lo, hi, 600)
    num = nderiv(f, xs)
    mine = np.asarray(fprime(xs), dtype=float) * np.ones_like(xs)
    ok = np.isfinite(num) & np.isfinite(mine)
    err = float(np.max(np.abs(num[ok] - mine[ok]) / (1 + np.abs(num[ok])))) if ok.any() else float('nan')
    plt.figure(figsize=(8, 3.4))
    plt.plot(xs, f(xs), color='0.7', label='f')
    plt.plot(xs, num, lw=6, alpha=0.3, color='C0', label='numerical slope of f')
    plt.plot(xs, mine, 'r--', lw=1.6, label='your formula')
    lim = np.nanpercentile(np.abs(np.concatenate([num[ok], mine[ok]])), 98) * 1.3 + 0.5 if ok.any() else 5
    plt.ylim(-lim, lim); plt.axhline(0, color='k', lw=0.8); plt.legend(fontsize=9, loc='upper right'); plt.show()
    print('✓ They agree: your derivative matches the numerical slope.' if err < 1e-4 else '✗ They differ (largest relative difference %.3g). Re-check your working.' % err)
