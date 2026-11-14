"""Figures for Unit 4 (sequences, series, Taylor expansions)."""
from figkit import *


# ------------------------------------------------------------------ week 1
def halves_square():
    fig, ax = canvas(4.4, 4.4, (-.05, 1.05), (-.05, 1.05))
    ax.add_patch(Rectangle((0, 0), 1, 1, fill=False, edgecolor=C['k'], lw=1.6))
    x, y, w, h, horiz = 0, 0, 1, 1, True
    cols = ['fb', 'fg', 'fy', 'fr', 'fp', 'fb', 'fg', 'fy']
    labels = [r'$\frac{1}{2}$', r'$\frac{1}{4}$', r'$\frac{1}{8}$', r'$\frac{1}{16}$', '', '', '', '']
    for k in range(8):
        if horiz:
            ax.add_patch(Rectangle((x, y), w / 2, h, facecolor=C[cols[k]], edgecolor=C['k'], lw=1)); cx, cy = x + w / 4, y + h / 2; x += w / 2; w /= 2
        else:
            ax.add_patch(Rectangle((x, y), w, h / 2, facecolor=C[cols[k]], edgecolor=C['k'], lw=1)); cx, cy = x + w / 2, y + h / 4; y += h / 2; h /= 2
        if labels[k]: txt(ax, (cx, cy), labels[k], 'k', 18 - 3 * k)
        horiz = not horiz
    return fig


def partial_sums():
    fig, ax = plt.subplots(1, 2, figsize=(10, 3.2))
    n = np.arange(1, 16)
    A = ax[0]; S = np.cumsum(0.5 ** n); A.plot(n, S, 'o-', color=C['b']); A.axhline(1, color=C['r'], ls='--', lw=1.2); A.set_title(r'$\frac{1}{2}+\frac{1}{4}+\frac{1}{8}+\dots$  settles at 1', fontsize=10.5); A.set_ylim(0, 1.15)
    A = ax[1]; n2 = np.arange(1, 60); H = np.cumsum(1 / n2); A.plot(n2, H, 'o-', ms=3, color=C['o']); A.plot(n2, np.log(n2) + .5772, color=C['gr'], ls='--', lw=1.2, label=r'$\ln n+0.577$')
    A.set_title(r'$1+\frac{1}{2}+\frac{1}{3}+\dots$  keeps growing', fontsize=10.5); A.legend(fontsize=9)
    for A in ax: A.grid(True, alpha=.3); A.set_xlabel('number of terms $n$'); A.set_ylabel('partial sum $S_n$')
    fig.tight_layout()
    return fig


def harmonic_groups():
    fig, ax = canvas(9.4, 2.2, (0, 17.5), (0, 2.6))
    terms = ['1', r'$\frac{1}{2}$', r'$\frac{1}{3}+\frac{1}{4}$', r'$\frac{1}{5}+\dots+\frac{1}{8}$', r'$\frac{1}{9}+\dots+\frac{1}{16}$', r'$\cdots$']
    lows = ['', '', r'$>\frac{1}{4}+\frac{1}{4}=\frac{1}{2}$', r'$>4\cdot\frac{1}{8}=\frac{1}{2}$', r'$>8\cdot\frac{1}{16}=\frac{1}{2}$', '']
    xs = [0.6, 2.2, 5.0, 8.9, 13.0, 16.6]
    for x0, tterm, lo, col in zip(xs, terms, lows, ['fb', 'fg', 'fy', 'fr', 'fp', 'fb']):
        txt(ax, (x0, 1.8), tterm, 'k', 14)
        if lo: txt(ax, (x0, .8), lo, 'r', 11.5)
    for a, b in ((1.4, 1.4), (3.1, 3.1), (7.0, 7.0), (11.0, 11.0), (15.2, 15.2)): txt(ax, (a, 1.8), '+', 'gr', 14)
    txt(ax, (8.7, .15), 'each group adds at least one half - and there are infinitely many groups', 'k', 10.5)
    return fig


def integral_test():
    fig, ax = graph(7, 3.4)
    xs = np.linspace(.7, 8.5, 300); ax.plot(xs, 1 / xs ** 1.0, color=C['b'], lw=2.2, label=r'$y=1/x$')
    for k in range(1, 9): ax.add_patch(Rectangle((k, 0), 1, 1 / k, facecolor=C['fy'], edgecolor=C['o'], lw=1, alpha=.85))
    ax.plot(xs, 1 / xs, color=C['b'], lw=2.2)
    txt(ax, (1.5, .55), '1', 'o', 11); txt(ax, (2.5, .3), r'$\frac{1}{2}$', 'o', 11); txt(ax, (3.5, .2), r'$\frac{1}{3}$', 'o', 11)
    ax.set_xlim(.5, 9.2); ax.set_ylim(0, 1.2); ax.legend(fontsize=10); ax.set_xlabel('$x$')
    txt(ax, (6.3, .8), 'bars (the series) lie above\nthe curve (the integral)', 'k', 10)
    return fig


def alternating():
    fig, ax = graph(7, 3.3)
    n = np.arange(1, 21); S = np.cumsum([(-1) ** (k + 1) / k for k in n])
    ax.plot(n, S, 'o-', color=C['b'], ms=4); ax.axhline(math.log(2), color=C['r'], ls='--', lw=1.2)
    txt(ax, (16, math.log(2) + .07), r'$\ln 2 = 0.693\ldots$', 'r', 11)
    for k in (3, 4):
        ax.annotate('', xy=(k + 1, S[k]), xytext=(k, S[k - 1]), arrowprops=dict(arrowstyle='->', color=C['o'], lw=1.3))
    ax.set_xlabel('number of terms $n$'); ax.set_ylabel('$S_n$'); ax.set_ylim(.45, 1.05)
    ax.set_title(r'$1-\frac{1}{2}+\frac{1}{3}-\frac{1}{4}+\dots$: each step overshoots, by less each time', fontsize=10.5)
    return fig


def bounce():
    fig, ax = graph(7, 3.0)
    h, x, r = 2.0, 0.0, .6; xs, ys = [], []
    for k in range(9):
        t = np.linspace(0, 1, 40); w = 1.2 * math.sqrt(h / 2)
        xs += list(x + w * t); ys += list(4 * h * t * (1 - t)) if k else list(h * (1 - t ** 2)); x += w; h *= r
    ax.plot(xs, ys, color=C['b'], lw=2); ax.set_ylim(0, 2.3); ax.set_xticks([]); ax.set_ylabel('height (m)')
    txt(ax, (1.0, 2.1), 'drop from 2 m; each bounce reaches 60 % of the previous height', 'k', 10.5, ha='left')
    return fig


# ------------------------------------------------------------------ week 2
def taylor_sin():
    fig, ax = graph(7.6, 3.8)
    xs = np.linspace(-7, 7, 600); ax.plot(xs, np.sin(xs), color=C['k'], lw=3, label=r'$\sin x$')
    cols = [C['r'], C['o'], C['g'], C['b'], C['p']]
    for (n, col) in zip((1, 3, 5, 7, 13), cols):
        y = sum((-1) ** k * xs ** (2 * k + 1) / math.factorial(2 * k + 1) for k in range((n - 1) // 2 + 1))
        ax.plot(xs, y, color=col, lw=1.6, label='degree %d' % n)
    ax.set_ylim(-2.2, 2.2); ax.set_xlim(-7, 7); ax.legend(fontsize=9, loc='lower left', ncol=2)
    ax.set_title('Taylor polynomials of sin x around 0: more terms, good further out', fontsize=10.5)
    return fig


def match_derivs():
    fig, ax = plt.subplots(1, 3, figsize=(10.4, 2.9), sharey=True)
    xs = np.linspace(-1.5, 2.5, 300); f = np.exp
    titles = ['degree 0: same value', 'degree 1: + same slope', 'degree 2: + same curvature']
    polys = [lambda x: 1 + 0 * x, lambda x: 1 + x, lambda x: 1 + x + x * x / 2]
    for A, t, p in zip(ax, titles, polys):
        A.plot(xs, f(xs), color=C['k'], lw=2.6); A.plot(xs, p(xs), color=C['r'], lw=1.8); A.scatter([0], [1], color=C['b'], zorder=5)
        A.set_title(t, fontsize=10.5); A.set_ylim(-1, 6); A.grid(True, alpha=.3); A.axhline(0, color=C['k'], lw=.8); A.axvline(0, color=C['k'], lw=.8)
    ax[0].text(-1.4, 5.2, '$e^x$ (black)', fontsize=10)
    fig.tight_layout()
    return fig


def radius():
    fig, ax = graph(7, 3.4)
    xs = np.linspace(-1.6, 1.6, 600); ax.plot(xs, 1 / (1 + xs ** 2), color=C['k'], lw=3, label=r'$\frac{1}{1+x^2}$')
    for n, col in ((4, C['o']), (10, C['g']), (20, C['b'])):
        ax.plot(xs, sum((-1) ** k * xs ** (2 * k) for k in range(n // 2 + 1)), color=col, lw=1.5, label='%d terms' % (n // 2 + 1))
    ax.axvspan(-1.6, -1, color=C['fr'], alpha=.6); ax.axvspan(1, 1.6, color=C['fr'], alpha=.6)
    ax.set_ylim(-.5, 1.6); ax.legend(fontsize=9, loc='upper center', ncol=4)
    txt(ax, (1.3, -.3), 'beyond |x| = 1\nthe series fails', 'r', 9.5)
    return fig


def pendulum():
    fig, ax = canvas(3.6, 3.8, (-1.3, 1.3), (-1.35, .25))
    seg(ax, (-.6, 0), (.6, 0), 'k', 4); seg(ax, (0, 0), (0, -1.15), 'gr', 1, ':')
    th = math.radians(32); bob = (math.sin(th), -math.cos(th)); seg(ax, (0, 0), bob, 'k', 1.8); ax.add_patch(Circle(bob, .09, color=C['b']))
    angle(ax, (0, 0), .35, 270, 270 + 32, 'r', label=r'$\theta$', lr=.5)
    txt(ax, (.36, -.45), '$L$', 'k', 13)
    return fig


def calc_sin():
    fig, ax = plt.subplots(figsize=(7, 3.2)); ax.grid(True, alpha=.3)
    xs = np.linspace(0, math.pi / 4, 300); p = xs - xs ** 3 / 6 + xs ** 5 / 120 - xs ** 7 / 5040
    xs = xs[1:]; p = p[1:]; ax.semilogy(xs, np.maximum(np.abs(np.sin(xs) - p), 1e-17), color=C['b'], lw=2); ax.set_ylim(1e-17, 1e-5)
    ax.set_xlabel(r'$x$ (radians), after reducing to $[0,\pi/4]$'); ax.set_ylabel('error of 4 terms'); ax.axhline(1e-8, color=C['r'], ls='--', lw=1)
    txt(ax, (.1, 3e-8), '1e-8', 'r', 10, ha='left')
    return fig
