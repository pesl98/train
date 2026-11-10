"""Figures for Unit 3 (integrals)."""
from figkit import *


def _area(ax, f, a, b, col='fb', n=200, **kw):
    xs = np.linspace(a, b, n); ax.fill_between(xs, 0, f(xs), color=C.get(col, col), **kw)


# ------------------------------------------------------------------ week 1
def const_velocity():
    fig, ax = plt.subplots(1, 2, figsize=(9.6, 3.2))
    A = ax[0]; A.add_patch(Rectangle((0, 0), 3, 20, facecolor=C['fb'], edgecolor=C['b'], lw=1.5)); A.plot([0, 3], [20, 20], color=C['b'], lw=2.2)
    A.text(1.5, 10, 'area = 20 × 3\n= 60 m', ha='center', va='center', color=C['b'], fontsize=11); A.set_title('constant velocity', fontsize=10.5)
    A = ax[1]; ts = np.linspace(0, 3, 100); v = 10 * ts; A.plot(ts, v, color=C['b'], lw=2.2)
    for k in range(6):
        t0 = k * .5; A.add_patch(Rectangle((t0, 0), .5, 10 * t0, facecolor=C['fy'], edgecolor=C['o'], lw=1))
    A.text(1.25, 25, 'each strip: (velocity) × (short time)\n= distance covered in that time', color=C['o'], fontsize=9.5, ha='center'); A.set_title('changing velocity: chop the time into short pieces', fontsize=10.5)
    for A in ax: A.set_xlabel('time (s)'); A.set_ylabel('velocity (m/s)'); A.set_xlim(0, 3.4); A.set_ylim(0, 32); A.grid(True, alpha=.3)
    fig.tight_layout()
    return fig


def riemann():
    fig, ax = plt.subplots(1, 3, figsize=(10.6, 3.1), sharey=True)
    f = lambda v: v ** 2
    xs = np.linspace(0, 1, 200)
    for A, kind, col in zip(ax, ('left', 'right', 'midpoint'), ('fg', 'fr', 'fy')):
        n = 5; dx = 1 / n; s = 0
        for k in range(n):
            x0 = k * dx; xe = {'left': x0, 'right': x0 + dx, 'midpoint': x0 + dx / 2}[kind]; hgt = f(xe); s += hgt * dx
            A.add_patch(Rectangle((x0, 0), dx, hgt, facecolor=C[col], edgecolor=C['k'], lw=1)); A.plot([xe], [hgt], 'o', color=C['k'], ms=3.5)
        A.plot(xs, f(xs), color=C['b'], lw=2.2); A.set_title('%s sum, n = 5:  %.3f' % (kind, s), fontsize=10.5); A.grid(True, alpha=.3); A.set_xlim(0, 1.05); A.set_ylim(0, 1.08)
    fig.tight_layout()
    return fig


def signed_area():
    fig, ax = graph(6.8, 3.3)
    f = lambda v: np.sin(v)
    xs = np.linspace(0, 2 * np.pi, 300); ax.plot(xs, f(xs), color=C['b'], lw=2.2)
    xa = np.linspace(0, np.pi, 100); ax.fill_between(xa, 0, f(xa), color=C['fg']); xb = np.linspace(np.pi, 2 * np.pi, 100); ax.fill_between(xb, 0, f(xb), color=C['fr'])
    txt(ax, (np.pi / 2, .42), 'counts +', 'g', 12); txt(ax, (3 * np.pi / 2, -.42), 'counts −', 'r', 12)
    ax.set_xticks([0, np.pi, 2 * np.pi]); ax.set_xticklabels(['0', r'$\pi$', r'$2\pi$']); ax.set_ylim(-1.25, 1.25)
    return fig


def strip():
    fig, ax = graph(6.6, 4)
    f = lambda v: .12 * (v - 1) ** 2 + 1.4 + .5 * np.sin(v)
    xs = np.linspace(0, 6.2, 300); ax.plot(xs, f(xs), color=C['b'], lw=2.2)
    a, x0, hh = .8, 3.4, .9
    xa = np.linspace(a, x0, 100); ax.fill_between(xa, 0, f(xa), color=C['fb']); xb = np.linspace(x0, x0 + hh, 40); ax.fill_between(xb, 0, f(xb), color=C['fy'], edgecolor=C['o'], lw=1.2)
    txt(ax, ((a + x0) / 2, .9), '$A(x)$', 'b', 15); txt(ax, (x0 + hh / 2, .75), 'new\nstrip', 'o', 10)
    for xv, lab in ((a, '$a$'), (x0, '$x$'), (x0 + hh, '$x+h$')): txt(ax, (xv, -.22), lab, 'k', 12); ax.plot([xv, xv], [0, f(xv)], color=C['k'], lw=1)
    arrow(ax, (x0, f(x0) + .45), (x0 + hh, f(x0) + .45), 'o', 1.3, '<|-|>', 9); txt(ax, (x0 + hh / 2, f(x0) + .68), '$h$', 'o', 12)
    txt(ax, (x0 + hh + .12, f(x0) / 2 + .4), 'height\n$\\approx f(x)$', 'k', 10, ha='left')
    txt(ax, (5.3, 3.75), '$y=f(t)$', 'b', 12); ax.set_xlim(0, 6.4); ax.set_ylim(-.45, 4.6); ax.set_xticks([]); ax.set_yticks([])
    return fig


def gauss_pairs():
    fig, ax = canvas(7, 2.2, (0, 11), (0, 3.2))
    for k in range(1, 11):
        txt(ax, (k, 2.4), str(k), 'b', 13); txt(ax, (k, 1.5), str(11 - k), 'r', 13); txt(ax, (k, .5), '11', 'k', 12); seg(ax, (k - .3, 1.05), (k + .3, 1.05), 'gr', 1)
    txt(ax, (.25, 2.4), '', 'k'); txt(ax, (5.5, 3.0), 'the sum written forwards and backwards: every column adds to 11', 'k', 10.5)
    return fig


# ------------------------------------------------------------------ week 2
def trapezoid():
    fig, ax = plt.subplots(1, 2, figsize=(9.2, 3.2), sharey=True)
    f = lambda v: 1.2 + np.sin(1.3 * v) * .8 + .1 * v
    xs = np.linspace(0, 4, 300)
    for A, kind in zip(ax, ('rect', 'trap')):
        n = 4; dx = 4 / n
        for k in range(n):
            x0, x1 = k * dx, (k + 1) * dx
            if kind == 'rect': A.add_patch(Rectangle((x0, 0), dx, f(x0), facecolor=C['fr'], edgecolor=C['k'], lw=1))
            else: A.add_patch(Polygon([(x0, 0), (x1, 0), (x1, f(x1)), (x0, f(x0))], closed=True, facecolor=C['fg'], edgecolor=C['k'], lw=1))
        A.plot(xs, f(xs), color=C['b'], lw=2.2); A.grid(True, alpha=.3); A.set_xlim(0, 4.1); A.set_ylim(0, 2.8)
        A.set_title('rectangles: flat tops' if kind == 'rect' else 'trapezoids: sloping tops follow the curve', fontsize=10.5)
    fig.tight_layout()
    return fig


def subst_area():
    fig, ax = plt.subplots(1, 2, figsize=(9.2, 3))
    xs = np.linspace(0, 2, 200); ax[0].plot(xs, 2 * xs * np.cos(xs ** 2), color=C['b'], lw=2); xa = np.linspace(0, math.sqrt(np.pi / 2), 100); ax[0].fill_between(xa, 0, 2 * xa * np.cos(xa ** 2), color=C['fb'])
    ax[0].set_title(r'$\int_0^{\sqrt{\pi/2}}2x\cos(x^2)\,dx$', fontsize=11); ax[0].set_xlabel('$x$')
    us = np.linspace(0, 4, 200); ax[1].plot(us, np.cos(us), color=C['r'], lw=2); ua = np.linspace(0, np.pi / 2, 100); ax[1].fill_between(ua, 0, np.cos(ua), color=C['fr'])
    ax[1].set_title(r'$\int_0^{\pi/2}\cos u\,du$   (same area: both are 1)', fontsize=11); ax[1].set_xlabel('$u=x^2$')
    for A in ax: A.grid(True, alpha=.3); A.axhline(0, color=C['k'], lw=.8)
    fig.tight_layout()
    return fig


# ------------------------------------------------------------------ week 3
def between_curves():
    fig, ax = graph(5.4, 4)
    xs = np.linspace(-.2, 1.25, 200); ax.plot(xs, xs, color=C['b'], lw=2, label='$y=x$'); ax.plot(xs, xs ** 2, color=C['r'], lw=2, label='$y=x^2$')
    xa = np.linspace(0, 1, 100); ax.fill_between(xa, xa ** 2, xa, color=C['fy'])
    x0 = .6; ax.add_patch(Rectangle((x0 - .025, x0 ** 2), .05, x0 - x0 ** 2, facecolor=C['o'], edgecolor=C['k'], lw=.8))
    txt(ax, (x0 + .06, (x0 + x0 ** 2) / 2), 'height = top − bottom\n$= x-x^2$', 'k', 10, ha='left'); txt(ax, (x0, -.07), '$dx$', 'o', 11)
    ax.legend(fontsize=10, loc='upper left'); ax.set_xlim(-.2, 1.5); ax.set_ylim(-.15, 1.3)
    return fig


def disc_sphere():
    fig, ax = canvas(8.8, 3.6, n=2)
    A = ax[0]; A.set_xlim(-1.4, 1.5); A.set_ylim(-1.3, 1.35); axes_cross(A, 1.3, ('$x$', '$y$'))
    tt = np.linspace(0, np.pi, 100); A.plot(np.cos(tt), np.sin(tt), color=C['b'], lw=2); A.fill_between(np.cos(tt), 0, np.sin(tt), color=C['fb'])
    x0 = .45; y0 = math.sqrt(1 - x0 ** 2); A.add_patch(Rectangle((x0 - .04, 0), .08, y0, facecolor=C['o'], edgecolor=C['k'], lw=.8))
    txt(A, (x0 + .08, y0 / 2), r'$y=\sqrt{r^2-x^2}$', 'k', 10.5, ha='left'); txt(A, (x0, -.12), '$x$', 'o', 11); txt(A, (0, -1.15), 'half-disc of radius $r$ …', 'k', 10.5)
    A = ax[1]; A.set_xlim(-1.4, 1.5); A.set_ylim(-1.3, 1.35)
    circle(A, col='b', lw=2); from matplotlib.patches import Ellipse
    A.add_patch(Ellipse((x0, 0), .28, 2 * y0, facecolor=C['fy'], edgecolor=C['o'], lw=1.5)); A.add_patch(Ellipse((0, 0), .5, 2, fill=False, edgecolor=C['gr'], lw=1, ls=':'))
    seg(A, (-1.3, 0), (1.3, 0), 'gr', 1); seg(A, (x0, 0), (x0, y0), 'k', 1.3); txt(A, (x0 + .2, y0 / 2 + .1), '$y$', 'k', 11)
    txt(A, (-.45, .62), 'disc: area $\\pi y^2$,\nthickness $dx$', 'o', 10); txt(A, (0, -1.15), '… rotated about the $x$-axis: a ball, sliced into discs', 'k', 10.5)
    return fig


def rings():
    fig, ax = canvas(8.4, 3.3, n=2)
    A = ax[0]; A.set_xlim(-1.3, 1.3); A.set_ylim(-1.35, 1.25)
    for r in np.linspace(1, .1, 10): A.add_patch(Circle((0, 0), r, facecolor=C['fb'] if int(round(r * 10)) % 2 else 'white', edgecolor=C['b'], lw=.8))
    A.add_patch(Wedge((0, 0), .7, 0, 360, width=.1, facecolor=C['fy'], edgecolor=C['o'], lw=1.5)); seg(A, (0, 0), (.65, 0), 'k', 1.3); txt(A, (.33, .09), r'$\rho$', 'k', 12)
    txt(A, (0, -1.22), 'a disc as thin rings', 'k', 10.5)
    A = ax[1]; A.set_xlim(-.4, 5); A.set_ylim(-1.1, 1.6)
    A.add_patch(Rectangle((0, .3), 4.4, .28, facecolor=C['fy'], edgecolor=C['o'], lw=1.5)); txt(A, (2.2, .82), r'length $2\pi\rho$ (the circumference)', 'k', 10.5); txt(A, (4.5, .44), r'$d\rho$', 'o', 11, ha='left')
    txt(A, (2.2, -.3), r'one ring, cut and straightened: area $\approx2\pi\rho\,d\rho$', 'k', 10.5)
    return fig


def spring_work():
    fig, ax = graph(5.6, 3.5)
    xs = np.linspace(0, 1, 50); ax.plot(xs, 3 * xs, color=C['b'], lw=2.2); ax.fill_between(xs[xs <= .8], 0, 3 * xs[xs <= .8], color=C['fb'])
    ax.add_patch(Rectangle((.5, 0), .04, 1.5, facecolor=C['o'], edgecolor=C['k'], lw=.8))
    txt(ax, (.4, 1.95), 'force $kx$\n× tiny step $dx$', 'o', 10); txt(ax, (.3, .3), r'work $=\frac{1}{2}kx^2$', 'b', 12)
    ax.set_xlabel('stretch $x$'); ax.set_ylabel('force $F=kx$'); ax.set_xlim(0, 1.05); ax.set_ylim(0, 3.2); ax.set_xticks([0, .8]); ax.set_xticklabels(['0', '$x$']); ax.set_yticks([])
    return fig


def rms():
    fig, ax = graph(7.4, 3.4)
    ts = np.linspace(0, 2 * np.pi, 400); ax.plot(ts, np.sin(ts), color=C['b'], lw=1.6, label=r'$v=V\sin\omega t$')
    ax.plot(ts, np.sin(ts) ** 2, color=C['r'], lw=2, label=r'$v^2$ (proportional to power)'); ax.fill_between(ts, 0, np.sin(ts) ** 2, color=C['fr'])
    ax.axhline(.5, color=C['g'], ls='--', lw=1.5, label=r'average of $v^2$: $\frac{1}{2}V^2$'); ax.axhline(1 / math.sqrt(2), color=C['o'], ls=':', lw=1.5, label=r'RMS: $V/\sqrt{2}$')
    ax.set_xticks([0, np.pi, 2 * np.pi]); ax.set_xticklabels(['0', '$T/2$', '$T$']); ax.set_yticks([-1, 0, .5, 1]); ax.set_yticklabels(['$-V$', '0', '', '$V$']); ax.legend(fontsize=9, loc='lower left'); ax.set_ylim(-1.15, 1.15)
    return fig


def improper():
    fig, ax = graph(6.6, 3.3)
    xs = np.linspace(0, 4, 300); ax.plot(xs, np.exp(-2 * xs), color=C['b'], lw=2.2); ax.fill_between(xs, 0, np.exp(-2 * xs), color=C['fb'])
    ax.axvline(1.6, color=C['r'], ls='--', lw=1.3); txt(ax, (1.66, .55), 'cut off at $b$,\nthen let $b\\to\\infty$', 'r', 10, ha='left')
    txt(ax, (.55, .12), r'area $\to\frac{1}{2}$', 'b', 12); txt(ax, (3.2, .12), 'infinitely long,\nfinite area', 'k', 10); ax.set_xlim(0, 4); ax.set_ylim(0, 1.05); txt(ax, (.6, .8), '$y=e^{-2x}$', 'b', 12)
    return fig


def average_value():
    fig, ax = graph(6, 3.4)
    f = lambda v: 1.5 + np.sin(v) + .25 * v
    xs = np.linspace(.5, 5.5, 200); ax.plot(xs, f(xs), color=C['b'], lw=2.2); ax.fill_between(xs, 0, f(xs), color=C['fb'], alpha=.7)
    avg = np.trapezoid(f(xs), xs) / 5 if hasattr(np, 'trapezoid') else np.trapz(f(xs), xs) / 5
    ax.add_patch(Rectangle((.5, 0), 5, avg, fill=False, edgecolor=C['r'], lw=2, ls='--')); txt(ax, (3, avg + .2), 'rectangle of the same area: its height is the average value', 'r', 9.5)
    ax.set_xticks([.5, 5.5]); ax.set_xticklabels(['$a$', '$b$']); ax.set_yticks([]); ax.set_xlim(0, 6); ax.set_ylim(0, 4)
    return fig
