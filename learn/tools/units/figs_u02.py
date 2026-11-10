"""Figures for Unit 2 (derivatives)."""
from figkit import *


# ------------------------------------------------------------------ week 1 (the definition)
def slope_line():
    fig, ax = graph(5.6, 3.6)
    xs = np.linspace(-1, 5, 10); ax.plot(xs, .75 * xs + 1, color=C['b'])
    p, q = (1, 1.75), (4, 4)
    seg(ax, p, (q[0], p[1]), 'g', 2, '--'); seg(ax, (q[0], p[1]), q, 'r', 2, '--'); dot(ax, p); dot(ax, q)
    txt(ax, (2.5, 1.4), r'run $\Delta x=3$', 'g', 11); txt(ax, (4.12, 2.9), r'rise $\Delta y=2.25$', 'r', 11, ha='left')
    txt(ax, (1.6, 4.3), r'slope $=\dfrac{\Delta y}{\Delta x}=0.75$', 'b', 12)
    ax.set_xlim(-1, 6.6); ax.set_ylim(-.5, 5.4)
    return fig


def secant_tangent():
    fig, ax = graph(6.6, 4.2)
    f = lambda v: .25 * v ** 2 + .5
    xs = np.linspace(-.5, 5, 200); ax.plot(xs, f(xs), color=C['k'], lw=2.4)
    a = 1.5
    for hh, col in ((3, 'g'), (2, 'o'), (1, 'p')):
        m = (f(a + hh) - f(a)) / hh; ax.plot(xs, f(a) + m * (xs - a), color=C[col], lw=1.2); dot(ax, (a + hh, f(a + hh)), col, 28)
        txt(ax, (a + hh + .08, f(a + hh) - .32), '$h=%d$' % hh, col, 10.5, ha='left')
    ax.plot(xs, f(a) + .5 * a * (xs - a), color=C['r'], lw=2.2); dot(ax, (a, f(a)), 'r', 45)
    txt(ax, (3.9, 1.72), 'tangent\n(limit $h\\to0$)', 'r', 10.5); txt(ax, (.55, 5.4), 'secant lines', 'gr', 10.5)
    txt(ax, (a - .1, f(a) + .42), r'$(a,\,f(a))$', 'r', 11, ha='right')
    ax.set_xlim(-.5, 5.4); ax.set_ylim(-.6, 6.3)
    return fig


def diff_quotient():
    fig, ax = graph(6.2, 4)
    f = lambda v: .3 * v ** 2 + .6
    xs = np.linspace(0, 4.6, 200); ax.plot(xs, f(xs), color=C['k'], lw=2.2)
    a, hh = 1.4, 2.2; p, q = (a, f(a)), (a + hh, f(a + hh))
    ax.plot(xs, p[1] + (q[1] - p[1]) / hh * (xs - a), color=C['b'], lw=1.3)
    seg(ax, p, (q[0], p[1]), 'g', 2, '--'); seg(ax, (q[0], p[1]), q, 'r', 2, '--'); dot(ax, p); dot(ax, q)
    txt(ax, (a + hh / 2, p[1] - .3), '$h$', 'g', 13); txt(ax, (q[0] + .1, (p[1] + q[1]) / 2), r'$f(a+h)-f(a)$', 'r', 11.5, ha='left')
    for xv, lab in ((a, '$a$'), (a + hh, '$a+h$')):
        ax.plot([xv, xv], [0, f(xv)], color=C['gr'], ls=':', lw=1); txt(ax, (xv, -.35), lab, 'k', 12)
    txt(ax, (a - .12, p[1] + .25), '$P$'); txt(ax, (q[0] - .12, q[1] + .28), '$Q$')
    ax.set_xlim(0, 6.2); ax.set_ylim(-.7, 6.6); ax.set_xticks([]); ax.set_yticks([])
    return fig


def f_and_fprime():
    fig, ax = plt.subplots(2, 1, figsize=(6.6, 5.2), sharex=True)
    xs = np.linspace(-2.2, 2.2, 300); f = xs ** 3 - 3 * xs; d = 3 * xs ** 2 - 3
    ax[0].plot(xs, f, color=C['b']); ax[1].plot(xs, d, color=C['r'])
    for A in ax: A.grid(True, alpha=.3); A.axhline(0, color=C['k'], lw=.8)
    for xv in (-1, 1):
        for A in ax: A.axvline(xv, color=C['gr'], ls=':', lw=1)
        ax[0].plot([xv - .45, xv + .45], [xv ** 3 - 3 * xv] * 2, color=C['g'], lw=2.5); ax[1].scatter([xv], [0], color=C['g'], zorder=5)
    ax[0].set_ylabel('$f(x)=x^3-3x$'); ax[1].set_ylabel("$f'(x)=3x^2-3$")
    ax[0].text(-1.9, 2.2, 'rising', color=C['r'], fontsize=10); ax[0].text(-.35, 1.6, 'falling', color=C['r'], fontsize=10); ax[0].text(1.35, -1.6, 'rising', color=C['r'], fontsize=10)
    ax[1].text(-2.1, 5.5, "$f'>0$", color=C['r'], fontsize=10.5); ax[1].text(-.25, -2.2, "$f'<0$", color=C['r'], fontsize=10.5); ax[1].text(1.5, 5.5, "$f'>0$", color=C['r'], fontsize=10.5)
    ax[0].text(-.95, 2.35, 'flat: slope 0', color=C['g'], fontsize=9.5)
    fig.tight_layout()
    return fig


def not_differentiable():
    fig, ax = plt.subplots(1, 3, figsize=(10, 2.9))
    xs = np.linspace(-2, 2, 400)
    ax[0].plot(xs, np.abs(xs), color=C['b']); ax[0].set_title('corner: $|x|$ at 0', fontsize=10.5)
    ax[1].plot(xs, np.cbrt(xs), color=C['b']); ax[1].set_title(r'vertical tangent: $\sqrt[3]{x}$ at 0', fontsize=10.5)
    ax[2].plot(xs[xs < 0], xs[xs < 0] * .5, color=C['b']); ax[2].plot(xs[xs >= 0], xs[xs >= 0] * .5 + 1, color=C['b']); ax[2].scatter([0], [0], s=40, facecolor='white', edgecolor=C['b'], zorder=5, lw=2); ax[2].scatter([0], [1], s=28, color=C['b'], zorder=5)
    ax[2].set_title('jump: not even continuous', fontsize=10.5)
    for A in ax: A.grid(True, alpha=.3); A.axhline(0, color=C['k'], lw=.8); A.axvline(0, color=C['k'], lw=.8)
    fig.tight_layout()
    return fig


def tangent_zoom():
    fig, ax = plt.subplots(1, 3, figsize=(10, 3))
    f = lambda v: np.sin(v) + .3 * v ** 2
    a = 1.0; m = math.cos(a) + .6 * a
    for A, w in zip(ax, (2.5, .5, .1)):
        xs = np.linspace(a - w, a + w, 200); A.plot(xs, f(xs), color=C['b'], lw=2.2, label='curve'); A.plot(xs, f(a) + m * (xs - a), color=C['r'], lw=1.3, ls='--', label='tangent')
        A.scatter([a], [f(a)], color=C['k'], zorder=5, s=25); A.grid(True, alpha=.3); A.set_title('window width %.1f' % (2 * w), fontsize=10.5)
    ax[0].legend(fontsize=9)
    fig.tight_layout()
    return fig


# ------------------------------------------------------------------ week 2 (rules)
def product_rect():
    fig, ax = canvas(5.6, 4.2, (-.9, 6.4), (-.9, 4.9))
    u, v, du, dv = 4, 3, 1.4, 1.0
    ax.add_patch(Rectangle((0, 0), u, v, facecolor=C['fb'], edgecolor=C['k'], lw=1.5))
    ax.add_patch(Rectangle((u, 0), du, v, facecolor=C['fg'], edgecolor=C['k'], lw=1.5))
    ax.add_patch(Rectangle((0, v), u, dv, facecolor=C['fr'], edgecolor=C['k'], lw=1.5))
    ax.add_patch(Rectangle((u, v), du, dv, facecolor=C['fy'], edgecolor=C['k'], lw=1.5))
    txt(ax, (u / 2, v / 2), r'$u\,v$', 'b', 16); txt(ax, (u + du / 2, v / 2), r'$v\,\Delta u$', 'g', 13); txt(ax, (u / 2, v + dv / 2), r'$u\,\Delta v$', 'r', 13)
    txt(ax, (u + du / 2, v + dv / 2), r'$\Delta u\,\Delta v$', 'o', 10.5)
    txt(ax, (u / 2, -.35), '$u$'); txt(ax, (u + du / 2, -.35), r'$\Delta u$'); txt(ax, (-.4, v / 2), '$v$'); txt(ax, (-.45, v + dv / 2), r'$\Delta v$')
    return fig


def sine_velocity():
    fig, ax = canvas(5, 4.6, (-1.45, 1.75), (-1.35, 1.6))
    axes_cross(ax, 1.3, ('', '')); circle(ax); th = 40; p = P(th)
    seg(ax, (0, 0), p, 'k', 1.6); dot(ax, p); angle(ax, (0, 0), .25, 0, th, 'k', label=r'$\theta$', lr=.38)
    v = (-math.sin(math.radians(th)) * .75, math.cos(math.radians(th)) * .75)
    q = (p[0] + v[0], p[1] + v[1]); arrow(ax, p, q, 'r', 2.4)
    seg(ax, p, (p[0], q[1]), 'g', 1.6, '--'); seg(ax, (p[0], q[1]), q, 'p', 1.6, '--')
    txt(ax, (p[0] + .08, (p[1] + q[1]) / 2), r'$\cos\theta$', 'g', 11, ha='left'); txt(ax, ((p[0] + q[0]) / 2, q[1] + .1), r'$-\sin\theta$', 'p', 11)
    txt(ax, (q[0] - .28, q[1] - .32), 'velocity\n(length 1)', 'r', 9.5); rightangle(ax, p, (-math.cos(math.radians(th)), -math.sin(math.radians(th))), (-math.sin(math.radians(th)), math.cos(math.radians(th))), .08)
    txt(ax, (p[0] + .1, p[1] - .12), r'$(\cos\theta,\ \sin\theta)$', 'k', 10.5, ha='left')
    return fig


def chain_gears():
    fig, ax = canvas(7.6, 2.3, (0, 11), (0, 3))
    for x0, lab, col in ((1.2, '$x$', 'fb'), (5.5, '$u=g(x)$', 'fg'), (9.8, '$y=f(u)$', 'fy')):
        ax.add_patch(Rectangle((x0 - 1.1, 1), 2.2, 1.1, facecolor=C[col], edgecolor=C['k'], lw=1.5)); txt(ax, (x0, 1.55), lab, 'k', 13)
    arrow(ax, (2.4, 1.55), (4.3, 1.55), 'k'); arrow(ax, (6.7, 1.55), (8.6, 1.55), 'k')
    txt(ax, (3.35, 2.15), r'$\times\ \dfrac{du}{dx}$', 'g', 12); txt(ax, (7.65, 2.15), r'$\times\ \dfrac{dy}{du}$', 'o', 12)
    txt(ax, (5.5, .4), r'a small change in $x$ is multiplied twice:  $\dfrac{dy}{dx}=\dfrac{dy}{du}\cdot\dfrac{du}{dx}$', 'k', 11.5)
    return fig


def exp_slopes():
    fig, ax = graph(6.2, 3.9)
    xs = np.linspace(-2, 1.6, 200)
    for b, col in ((2, 'g'), (math.e, 'r'), (4, 'b')):
        ax.plot(xs, b ** xs, color=C[col], label=('$e^x$' if abs(b - math.e) < 1e-9 else '$%d^x$' % b) + ': slope at 0 is %.3f' % math.log(b))
    ax.plot(xs, 1 + xs, color=C['k'], ls='--', lw=1.2, label='line of slope 1')
    dot(ax, (0, 1)); ax.set_ylim(-.3, 5); ax.set_xlim(-2, 1.6); ax.legend(fontsize=9.5, loc='upper left')
    return fig


# ------------------------------------------------------------------ week 3 (implicit, rates, Newton)
def implicit_circle():
    fig, ax = canvas(4.9, 4.7, (-6.6, 7.4), (-6.6, 7))
    axes_cross(ax, 6.2, ('$x$', '$y$')); circle(ax, r=5, col='b', lw=2)
    p = (3, 4); seg(ax, (0, 0), p, 'gr', 1.5); dot(ax, p)
    xs = np.array([-.5, 6.6]); ax.plot(xs, 4 - .75 * (xs - 3), color=C['r'], lw=2)
    txt(ax, (3.5, 4.75), '$(3,\\,4)$', 'k', 11, ha='left'); txt(ax, (5.3, 3.4), r'slope $-\frac{3}{4}$', 'r', 11, ha='left'); txt(ax, (1.0, 2.3), r'slope $\frac{4}{3}$', 'gr', 10.5)
    txt(ax, (-3.2, -4.9), '$x^2+y^2=25$', 'b', 12)
    return fig


def ladder():
    fig, ax = canvas(4.6, 4, (-1, 5.4), (-.9, 4.9))
    seg(ax, (0, 0), (5, 0), 'k', 3); seg(ax, (0, 0), (0, 4.6), 'k', 3)
    seg(ax, (3, 0), (0, 4), 'o', 4); dot(ax, (3, 0)); dot(ax, (0, 4))
    arrow(ax, (3.1, -.35), (4.3, -.35), 'r', 2); txt(ax, (3.7, -.68), r'$\dfrac{dx}{dt}=1$ m/s', 'r', 10.5)
    arrow(ax, (-.35, 3.9), (-.35, 2.8), 'b', 2); txt(ax, (-.6, 3.3), r'$\dfrac{dy}{dt}=?$', 'b', 10.5, ha='right')
    txt(ax, (1.5, -.28), '$x$'); txt(ax, (.22, 2), '$y$'); txt(ax, (1.85, 2.25), '5 m', 'o', 11)
    return fig


def newton():
    fig, ax = graph(6.8, 4)
    f = lambda v: v ** 2 - 2
    xs = np.linspace(.6, 3.3, 200); ax.plot(xs, f(xs), color=C['b'], lw=2.2)
    xk = 3.0
    for k, col in enumerate(('r', 'o', 'g')):
        yk = f(xk); xn = xk - yk / (2 * xk)
        ax.plot([xk, xk], [0, yk], color=C['gr'], ls=':', lw=1); ax.plot([xk, xn], [yk, 0], color=C[col], lw=1.6); dot(ax, (xk, yk), col, 28)
        txt(ax, (xk, -.55), '$x_%d$' % k, col, 12); xk = xn
    txt(ax, (xk - .02, -.55), '$x_3$', 'k', 12, ha='right'); dot(ax, (math.sqrt(2), 0), 'k', 30)
    txt(ax, (1.25, 6.2), '$f(x)=x^2-2$', 'b', 12); txt(ax, (2.25, 3.9), 'slide down\nthe tangent', 'r', 10)
    ax.set_xlim(.6, 3.4); ax.set_ylim(-1.5, 8.5)
    return fig


def linear_approx():
    fig, ax = graph(6, 3.8)
    xs = np.linspace(0, 9, 200); ax.plot(xs, np.sqrt(xs), color=C['b'], lw=2.2, label=r'$\sqrt{x}$')
    ax.plot(xs, 2 + (xs - 4) / 4, color=C['r'], lw=1.5, ls='--', label=r'tangent at 4:  $2+\frac{1}{4}(x-4)$')
    dot(ax, (4, 2)); ax.plot([6, 6], [math.sqrt(6), 2.5], color=C['o'], lw=3); txt(ax, (6.0, 2.85), 'error', 'o', 10.5)
    ax.legend(fontsize=10, loc='lower right'); ax.set_xlim(0, 9); ax.set_ylim(0, 3.6)
    return fig


def cone_tank():
    fig, ax = canvas(3.8, 4, (-2.6, 2.9), (-.4, 4.6))
    poly(ax, [(-2, 4), (2, 4), (0, 0)], 'white', 'k', 2); poly(ax, [(-1.1, 2.2), (1.1, 2.2), (0, 0)], 'fb', 'b', 1.5)
    seg(ax, (0, 0), (0, 4), 'gr', 1, ':'); arrow(ax, (2.3, 0), (2.3, 2.2), 'b', 1.3, '<|-|>', 9); txt(ax, (2.45, 1.1), '$h$', 'b', 12, ha='left')
    seg(ax, (0, 2.2), (1.1, 2.2), 'r', 2); txt(ax, (.55, 2.42), '$r$', 'r', 12)
    seg(ax, (0, 4), (2, 4), 'k', 1.2); txt(ax, (1, 4.25), '2 m'); arrow(ax, (-2.35, 0), (-2.35, 4), 'k', 1.2, '<|-|>', 9); txt(ax, (-2.5, 2), '4 m', ha='right')
    return fig


# ------------------------------------------------------------------ week 4 (applications)
def extrema():
    fig, ax = graph(7.2, 4)
    f = lambda v: v ** 3 - 3 * v + .5
    xs = np.linspace(-2.3, 2.5, 300); ax.plot(xs, f(xs), color=C['b'], lw=2.2)
    for xv, lab, dy in ((-1, 'local max\n$f\'=0$, $f\'\'<0$', .95), (1, 'local min\n$f\'=0$, $f\'\'>0$', -1.05)):
        dot(ax, (xv, f(xv)), 'r', 45); ax.plot([xv - .5, xv + .5], [f(xv)] * 2, color=C['r'], lw=1.6); txt(ax, (xv, f(xv) + dy), lab, 'r', 10)
    dot(ax, (0, .5), 'g', 40); txt(ax, (.12, .95), 'inflection\n$f\'\'=0$', 'g', 10, ha='left')
    ax.axvspan(-2.3, 0, color=C['fy'], alpha=.5); ax.axvspan(0, 2.5, color=C['fb'], alpha=.5)
    txt(ax, (-1.7, -3.6), 'concave down ∩', 'o', 10.5); txt(ax, (1.7, -3.6), 'concave up ∪', 'b', 10.5)
    ax.set_xlim(-2.3, 2.5); ax.set_ylim(-4.5, 5)
    return fig


def mvt():
    fig, ax = graph(6, 3.9)
    f = lambda v: .08 * v ** 3 - .3 * v ** 2 + 1.2 * v + .5
    xs = np.linspace(0, 5.5, 200); ax.plot(xs, f(xs), color=C['b'], lw=2.2)
    a, b = .5, 5; m = (f(b) - f(a)) / (b - a); ax.plot([a, b], [f(a), f(b)], color=C['g'], lw=1.6); dot(ax, (a, f(a)), 'g'); dot(ax, (b, f(b)), 'g')
    # points where f'(c) = m
    cs = np.roots([.24, -.6, 1.2 - m]); cs = [c.real for c in cs if abs(c.imag) < 1e-9 and a < c.real < b]
    for c in cs:
        ax.plot([c - 1, c + 1], [f(c) - m, f(c) + m], color=C['r'], lw=1.8); dot(ax, (c, f(c)), 'r'); txt(ax, (c - .25, f(c) + .6), '$c$', 'r', 12)
    txt(ax, (1.7, 5.6), 'average slope\n(secant)', 'g', 10); txt(ax, (4.3, 2.6), 'somewhere the tangent\nis parallel to the secant', 'r', 10)
    txt(ax, (a + .25, f(a) - .45), '$a$', 'g', 12); txt(ax, (b + .2, f(b) - .5), '$b$', 'g', 12); ax.set_xlim(0, 5.8); ax.set_ylim(0, 10)
    return fig


def box_fold():
    fig, ax = canvas(8.2, 3.5, n=2)
    A = ax[0]; A.set_xlim(-1, 13); A.set_ylim(-1.6, 13)
    A.add_patch(Rectangle((0, 0), 12, 12, facecolor=C['fb'], edgecolor=C['k'], lw=1.5)); s = 2.2
    for cx, cy in ((0, 0), (12 - s, 0), (0, 12 - s), (12 - s, 12 - s)): A.add_patch(Rectangle((cx, cy), s, s, facecolor='white', edgecolor=C['r'], lw=1.3, hatch='///'))
    A.add_patch(Rectangle((s, s), 12 - 2 * s, 12 - 2 * s, fill=False, edgecolor=C['k'], ls='--', lw=1))
    txt(A, (s / 2, -.6), '$x$', 'r', 12); txt(A, (6, -.6), '$12-2x$', 'k', 11); txt(A, (6, 6), 'base', 'b', 11); txt(A, (6, -1.35), 'cut a square $x\\times x$ from each corner', 'k', 10)
    A = ax[1]; A.set_xlim(-1, 9); A.set_ylim(-1.6, 6)
    b0 = [(0, 0), (5, 0), (7, 2), (2, 2)]; hgt = 1.7
    poly(A, b0, 'fb'); top = [(p[0], p[1] + hgt) for p in b0]
    poly(A, [b0[0], b0[1], top[1], top[0]], 'fg', alpha=.8); poly(A, [b0[1], b0[2], top[2], top[1]], 'fy', alpha=.8)
    for p, q in zip(b0, top): seg(A, p, q, 'k', 1.3)
    seg(A, top[0], top[1], 'k', 1.3); seg(A, top[1], top[2], 'k', 1.3); seg(A, top[2], top[3], 'k', 1.3); seg(A, top[3], top[0], 'k', 1.3)
    txt(A, (2.5, -.45), '$12-2x$'); txt(A, (7.5, 1.8), '$x$', 'r', 12, ha='left'); txt(A, (4, -1.35), 'fold up: volume $V=x\\,(12-2x)^2$', 'k', 10)
    return fig


def concavity():
    fig, ax = plt.subplots(1, 2, figsize=(8.4, 3))
    xs = np.linspace(-1.5, 1.5, 100)
    for A, f, d, title in ((ax[0], lambda v: v ** 2, lambda v: 2 * v, "concave up: slopes increase, $f''>0$"), (ax[1], lambda v: -v ** 2, lambda v: -2 * v, "concave down: slopes decrease, $f''<0$")):
        A.plot(xs, f(xs), color=C['b'], lw=2.2)
        for a in (-1, -.3, .5, 1.1):
            A.plot([a - .35, a + .35], [f(a) - .35 * d(a), f(a) + .35 * d(a)], color=C['r'], lw=1.6)
        A.set_title(title, fontsize=10.5); A.grid(True, alpha=.3)
    fig.tight_layout()
    return fig


def power_transfer():
    fig, ax = canvas(5.4, 2.9, (0, 9), (0, 4.6))
    seg(ax, (1, 1), (1, 3.6)); seg(ax, (1, 3.6), (3, 3.6)); seg(ax, (5, 3.6), (7.5, 3.6)); seg(ax, (7.5, 3.6), (7.5, 3)); seg(ax, (7.5, 1.6), (7.5, 1)); seg(ax, (7.5, 1), (1, 1))
    ax.add_patch(Rectangle((3, 3.3), 2, .6, facecolor=C['fy'], edgecolor=C['k'], lw=1.5)); txt(ax, (4, 4.25), r'source resistance $r$', 'k', 10.5)
    ax.add_patch(Rectangle((7.2, 1.6), .6, 1.4, facecolor=C['fg'], edgecolor=C['k'], lw=1.5)); txt(ax, (8.0, 2.3), '$R$', 'g', 13, ha='left')
    ax.add_patch(Circle((1, 2.3), .45, facecolor='white', edgecolor=C['k'], lw=1.5, zorder=3)); txt(ax, (1, 2.3), '$V$', 'k', 12, zorder=4)
    arrow(ax, (5.4, 3.6), (6.4, 3.6), 'r', 2); txt(ax, (5.9, 3.95), '$I$', 'r', 12)
    txt(ax, (4.2, .45), r'power in the load:  $P=I^2R=\dfrac{V^2R}{(R+r)^2}$', 'k', 11)
    return fig
