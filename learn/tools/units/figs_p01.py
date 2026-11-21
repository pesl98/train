"""Figures for the Term 1 physics strand (units, vectors, kinematics, Newton, energy, circuits)."""
from figkit import *


def _res(ax, p, q, label=None, col='k', w=.32):
    """Resistor (box) from p to q, horizontal or vertical."""
    (x0, y0), (x1, y1) = p, q
    mx, my = (x0 + x1) / 2, (y0 + y1) / 2
    if y0 == y1:
        L = .8; seg(ax, p, (mx - L, my)); seg(ax, (mx + L, my), q)
        ax.add_patch(Rectangle((mx - L, my - w / 2), 2 * L, w, facecolor=C['fy'], edgecolor=C['k'], lw=1.5, zorder=3))
        if label: txt(ax, (mx, my + .45), label, col, 11)
    else:
        L = .8; seg(ax, p, (mx, my - L)); seg(ax, (mx, my + L), q)
        ax.add_patch(Rectangle((mx - w / 2, my - L), w, 2 * L, facecolor=C['fy'], edgecolor=C['k'], lw=1.5, zorder=3))
        if label: txt(ax, (mx + .35, my), label, col, 11, ha='left')


def _bat(ax, c, label, vertical=True):
    """Battery symbol at c, + terminal on top."""
    x, y = c
    seg(ax, (x, y + .9), (x, y + .18)); seg(ax, (x, y - .18), (x, y - .9))
    seg(ax, (x - .45, y + .18), (x + .45, y + .18), 'k', 2.2); seg(ax, (x - .25, y - .18), (x + .25, y - .18), 'k', 4)
    txt(ax, (x - .65, y + .45), '+', 'r', 11); txt(ax, (x - .7, y - .1), label, 'k', 11, ha='right')


# ------------------------------------------------------------------ P1: units, dimensions, vectors
def pendulum():
    fig, ax = canvas(4.2, 3.6, (-1.6, 1.8), (-2.3, .5))
    seg(ax, (-1.2, .2), (1.2, .2), 'k', 3)
    a = math.radians(28); L = 1.9; b = (L * math.sin(a), -L * math.cos(a))
    seg(ax, (0, .2), (b[0], b[1] + .2), 'k', 1.6); seg(ax, (0, .2), (0, -1.9), 'gr', 1, '--')
    ax.add_patch(Circle((b[0], b[1] + .2), .16, color=C['b'], zorder=4))
    angle(ax, (0, .2), .6, -90, -90 + 28, 'k', 1.2, r'$\theta$', .85, 11)
    txt(ax, (.62, -.6), '$L$', 'k', 13); txt(ax, (b[0] + .33, b[1] + .2), '$m$', 'b', 13, ha='left')
    arrow(ax, (b[0], b[1] + .03), (b[0], b[1] - .55), 'r', 1.8); txt(ax, (b[0] + .3, b[1] - .45), '$g$', 'r', 12)
    return fig


def components():
    fig, ax = canvas(4.8, 3.4, (-.5, 4.6), (-.5, 3.2))
    axes_cross(ax, 0)
    arrow(ax, (-.3, 0), (4.4, 0), 'gr', 1); arrow(ax, (0, -.3), (0, 3.0), 'gr', 1); txt(ax, (4.5, -.15), '$x$', 'gr', 11); txt(ax, (-.15, 3.05), '$y$', 'gr', 11)
    A = (3.6, 2.3)
    arrow(ax, (0, 0), A, 'b', 2.4, ms=16); txt(ax, (1.55, 1.45), r'$\vec v$', 'b', 14)
    seg(ax, (A[0], 0), A, 'gr', 1.2, '--'); seg(ax, (0, A[1]), A, 'gr', 1.2, '--')
    arrow(ax, (0, 0), (A[0], 0), 'r', 2); txt(ax, (1.8, -.28), r'$v_x=v\cos\theta$', 'r', 11)
    arrow(ax, (0, 0), (0, A[1]), 'g', 2); txt(ax, (-.1, 1.15), r'$v_y=v\sin\theta$', 'g', 11, ha='right')
    angle(ax, (0, 0), .7, 0, math.degrees(math.atan2(A[1], A[0])), 'k', 1.3, r'$\theta$', 1.0, 12)
    rightangle(ax, (A[0], 0), (-1, 0), (0, 1), .18)
    return fig


def vector_add():
    fig, ax = canvas(5.6, 3.2, (-.4, 6.2), (-.4, 3.4))
    a, b = (3.2, .9), (1.6, 1.9)
    arrow(ax, (0, 0), a, 'b', 2.4, ms=16); txt(ax, (1.6, .15), r'$\vec a$', 'b', 14)
    arrow(ax, a, (a[0] + b[0], a[1] + b[1]), 'g', 2.4, ms=16); txt(ax, (a[0] + b[0] / 2 + .35, a[1] + b[1] / 2 - .1), r'$\vec b$', 'g', 14)
    arrow(ax, (0, 0), (a[0] + b[0], a[1] + b[1]), 'r', 2.6, ms=16); txt(ax, (2.0, 1.75), r'$\vec a+\vec b$', 'r', 14)
    txt(ax, (5.1, .35), 'tip to tail:\nadd the components', 'gr', 10)
    return fig


def incline_resolve():
    fig, ax = canvas(5.4, 3.4, (-.3, 5.6), (-.3, 3.5))
    th = math.radians(30)
    poly(ax, [(0, 0), (5, 0), (5, 5 * math.tan(th))], 'lg', 'k', 1.2)
    angle(ax, (0, 0), .9, 0, 30, 'k', 1.2, r'$\theta$', 1.25, 12)
    c = (2.9, 2.9 * math.tan(th) + .28)
    ax.add_patch(Polygon([(c[0] - .38 * math.cos(th) + .28 * math.sin(th), c[1] - .38 * math.sin(th) - .28 * math.cos(th)),
                          (c[0] + .38 * math.cos(th) + .28 * math.sin(th), c[1] + .38 * math.sin(th) - .28 * math.cos(th)),
                          (c[0] + .38 * math.cos(th) - .28 * math.sin(th), c[1] + .38 * math.sin(th) + .28 * math.cos(th)),
                          (c[0] - .38 * math.cos(th) - .28 * math.sin(th), c[1] - .38 * math.sin(th) + .28 * math.cos(th))],
                         closed=True, facecolor=C['fb'], edgecolor=C['b'], lw=1.5, zorder=3))
    g = 1.5
    arrow(ax, c, (c[0], c[1] - g), 'k', 2); txt(ax, (c[0] + .12, c[1] - g - .15), '$mg$', 'k', 12, ha='left')
    par = (-g * math.sin(th) * math.cos(th), -g * math.sin(th) * math.sin(th))
    per = (g * math.cos(th) * math.sin(th), -g * math.cos(th) * math.cos(th))
    arrow(ax, c, (c[0] + par[0], c[1] + par[1]), 'r', 2); txt(ax, (c[0] + par[0] - .2, c[1] + par[1] + .25), r'$mg\sin\theta$', 'r', 11, ha='right')
    arrow(ax, c, (c[0] + per[0], c[1] + per[1]), 'g', 2); txt(ax, (c[0] + per[0] + .15, c[1] + per[1] - .1), r'$mg\cos\theta$', 'g', 11, ha='left')
    return fig


# ------------------------------------------------------------------ P2: kinematics
def motion_graphs():
    fig, ax = plt.subplots(1, 3, figsize=(10.5, 2.9))
    ts = np.linspace(0, 4, 200); v0, a = 2, 1.5
    for A, ys, lab, col in ((ax[0], v0 * ts + a * ts ** 2 / 2, 'position $x$ (m)', C['b']), (ax[1], v0 + a * ts, 'velocity $v$ (m/s)', C['g']), (ax[2], a + 0 * ts, 'acceleration $a$ (m/s²)', C['r'])):
        A.plot(ts, ys, color=col, lw=2.4); A.set_xlabel('$t$ (s)'); A.set_title(lab, fontsize=10.5); A.grid(True, alpha=.3); A.set_ylim(bottom=0)
    ax[0].plot([2, 3], [v0 * 2 + a * 2, v0 * 2 + a * 2 + (v0 + a * 2)], color=C['o'], lw=1.6, ls='--'); ax[0].text(.2, 15, 'slope of $x$ = $v$', color=C['o'], fontsize=9.5)
    ax[1].fill_between(ts, 0, v0 + a * ts, color=C['fg']); ax[1].text(.3, 1, 'area = distance', color=C['g'], fontsize=9.5)
    ax[1].text(.2, 7, 'slope of $v$ = $a$', color=C['r'], fontsize=9.5)
    fig.tight_layout()
    return fig


def vt_trapezoid():
    fig, ax = graph(5.4, 3.4)
    v0, v, T = 2, 8, 4
    ax.fill([0, T, T, 0], [0, 0, v0, v0], color=C['fb']); ax.fill([0, T, T], [v0, v0, v], color=C['fg'])
    ax.plot([0, T], [v0, v], color=C['k'], lw=2.4)
    txt(ax, (2, 1), r'rectangle $v_0t$', 'b', 11); txt(ax, (2.9, 4.6), r'triangle $\frac{1}{2}(v-v_0)t$', 'g', 11)
    ax.set_xticks([0, T]); ax.set_xticklabels(['0', '$t$']); ax.set_yticks([v0, v]); ax.set_yticklabels(['$v_0$', '$v$'])
    ax.set_xlim(-.2, 4.8); ax.set_ylim(0, 9); ax.set_xlabel('time'); ax.set_ylabel('velocity')
    return fig


def projectile_path():
    fig, ax = graph(6.4, 3.3)
    v0, a, g = 20, math.radians(50), 9.81
    T = 2 * v0 * math.sin(a) / g; ts = np.linspace(0, T, 200)
    X, Y = v0 * math.cos(a) * ts, v0 * math.sin(a) * ts - g * ts ** 2 / 2
    ax.plot(X, Y, color=C['b'], lw=2.4)
    for tk in np.linspace(0, T, 7):
        x0, y0 = v0 * math.cos(a) * tk, v0 * math.sin(a) * tk - g * tk ** 2 / 2; vy = v0 * math.sin(a) - g * tk
        ax.scatter([x0], [y0], color=C['k'], s=14, zorder=5)
        ax.add_patch(FancyArrowPatch((x0, y0), (x0 + v0 * math.cos(a) * .18, y0), arrowstyle='-|>', mutation_scale=10, color=C['r'], lw=1.4))
        ax.add_patch(FancyArrowPatch((x0, y0), (x0, y0 + vy * .18), arrowstyle='-|>', mutation_scale=10, color=C['g'], lw=1.4))
    ax.text(16, 17.5, 'red: $v_x$ never changes', color=C['r'], fontsize=10); ax.text(16, 15.6, 'green: $v_y$ falls by $g$ each second', color=C['g'], fontsize=10)
    ax.set_xlabel('$x$ (m)'); ax.set_ylabel('$y$ (m)'); ax.set_aspect('equal'); ax.set_ylim(-1, 19)
    return fig


# ------------------------------------------------------------------ P3: Newton and energy
def free_body():
    fig, ax = canvas(8.6, 3.2, n=2)
    A = ax[0]; A.set_xlim(-2, 2); A.set_ylim(-1.9, 1.9)
    A.add_patch(Rectangle((-.5, -.4), 1, .8, facecolor=C['fb'], edgecolor=C['b'], lw=1.5)); seg(A, (-1.8, -.4), (1.8, -.4), 'k', 2)
    arrow(A, (0, 0), (0, -1.5), 'k', 2); txt(A, (.15, -1.45), '$W=mg$', 'k', 11, ha='left')
    arrow(A, (0, 0), (0, 1.5), 'g', 2); txt(A, (.15, 1.45), '$N$', 'g', 12, ha='left')
    arrow(A, (0, 0), (1.6, 0), 'r', 2); txt(A, (1.55, .25), '$F$', 'r', 12)
    arrow(A, (0, -.2), (-1.3, -.2), 'o', 2); txt(A, (-1.3, .05), '$f$', 'o', 12)
    A.set_title('a crate pushed across a floor', fontsize=10)
    B = ax[1]; B.set_xlim(-2, 2); B.set_ylim(-1.9, 1.9)
    dot(B, (0, 0), 'b', 70)
    arrow(B, (0, 0), (0, -1.5), 'k', 2); txt(B, (.15, -1.45), '$mg$', 'k', 11, ha='left')
    arrow(B, (0, 0), (0, 1.5), 'g', 2); txt(B, (.15, 1.45), '$N$', 'g', 12, ha='left')
    arrow(B, (0, 0), (1.6, 0), 'r', 2); txt(B, (1.55, .25), '$F$', 'r', 12)
    arrow(B, (0, 0), (-1.3, 0), 'o', 2); txt(B, (-1.3, .25), '$f$', 'o', 12)
    B.set_title('the free-body diagram: one dot, every force on it', fontsize=10)
    return fig


def atwood():
    fig, ax = canvas(3.8, 3.8, (-1.8, 1.8), (-2.6, 1.0))
    circle(ax, (0, .4), .45, 'k', 1.6); seg(ax, (0, .4), (0, .95), 'k', 2); seg(ax, (-.8, .95), (.8, .95), 'k', 3)
    seg(ax, (-.45, .4), (-.45, -1.1), 'k', 1.4); seg(ax, (.45, .4), (.45, -.5), 'k', 1.4)
    ax.add_patch(Rectangle((-.8, -1.8), .7, .7, facecolor=C['fr'], edgecolor=C['r'], lw=1.5)); txt(ax, (-.45, -1.45), '$m_2$', 'r', 12)
    ax.add_patch(Rectangle((.15, -1.0), .6, .5, facecolor=C['fb'], edgecolor=C['b'], lw=1.5)); txt(ax, (.45, -.75), '$m_1$', 'b', 12)
    arrow(ax, (-1.15, -1.0), (-1.15, -1.9), 'r', 1.6); txt(ax, (-1.35, -1.45), '$a$', 'r', 12, ha='right')
    arrow(ax, (1.1, -1.0), (1.1, -.1), 'b', 1.6); txt(ax, (1.3, -.55), '$a$', 'b', 12, ha='left')
    txt(ax, (-.2, -.1), '$T$', 'k', 11, ha='right'); txt(ax, (.55, -.1), '$T$', 'k', 11, ha='left')
    return fig


def work_area():
    fig, ax = graph(6.2, 3.3, n=2)
    A = ax[0]; xs = np.linspace(0, 5, 100); A.fill_between([1, 4], 0, 3, color=C['fb']); A.plot([0, 5], [3, 3], color=C['b'], lw=2.4)
    A.text(1.6, 1.3, r'$W=F\,d$', color=C['b'], fontsize=12); A.set_ylim(0, 4); A.set_xlabel('$x$'); A.set_ylabel('$F$'); A.set_title('constant force', fontsize=10)
    B = ax[1]; B.fill_between(xs[xs <= 4], 0, 1.2 * xs[xs <= 4], color=C['fg']); B.plot(xs, 1.2 * xs, color=C['g'], lw=2.4)
    B.text(2.2, .9, r'$W=\int F\,dx$', color=C['g'], fontsize=12); B.set_xlabel('$x$'); B.set_title('spring: $F=kx$', fontsize=10)
    fig.tight_layout()
    return fig


def energy_bars():
    fig, ax = plt.subplots(1, 3, figsize=(8.4, 2.8), sharey=True)
    for A, (h, lab) in zip(ax, ((1, 'top: all potential'), (.5, 'half-way'), (0, 'bottom: all kinetic'))):
        A.bar(['$mgh$', r'$\frac{1}{2}mv^2$', 'total'], [h, 1 - h, 1], color=[C['p'], C['o'], C['gr']])
        A.set_title(lab, fontsize=10); A.set_ylim(0, 1.15); A.grid(True, axis='y', alpha=.3)
    fig.tight_layout()
    return fig


# ------------------------------------------------------------------ P4: circuits
def series_parallel():
    fig, ax = canvas(9.4, 3.0, n=2)
    A = ax[0]; A.set_xlim(0, 10); A.set_ylim(0, 4.6)
    _bat(A, (1, 2.3), '$V$'); seg(A, (1, 3.2), (1, 3.8)); _res(A, (1, 3.8), (5, 3.8), '$R_1$'); _res(A, (5, 3.8), (9, 3.8), '$R_2$')
    seg(A, (9, 3.8), (9, .8)); seg(A, (9, .8), (1, .8)); seg(A, (1, .8), (1, 1.4))
    arrow(A, (8.3, 2.6), (8.3, 1.8), 'r', 1.8); txt(A, (8.0, 2.2), '$I$', 'r', 12, ha='right')
    A.set_title('series: one path, the same current', fontsize=10)
    B = ax[1]; B.set_xlim(0, 10); B.set_ylim(0, 4.6)
    _bat(B, (1, 2.3), '$V$'); seg(B, (1, 3.2), (1, 3.8)); seg(B, (1, 3.8), (8, 3.8)); seg(B, (1, .8), (8, .8)); seg(B, (1, .8), (1, 1.4))
    _res(B, (5, 3.8), (5, .8), '$R_1$'); _res(B, (8, 3.8), (8, .8), '$R_2$')
    dot(B, (5, 3.8), 'k', 25); dot(B, (5, .8), 'k', 25)
    B.set_title('parallel: the same voltage across each', fontsize=10)
    return fig


def divider():
    fig, ax = canvas(4.6, 3.6, (0, 7), (0, 5.4))
    _bat(ax, (1, 2.7), r'$V_{in}$'); seg(ax, (1, 3.6), (1, 4.6)); seg(ax, (1, 4.6), (4, 4.6))
    _res(ax, (4, 4.6), (4, 2.7), '$R_1$'); _res(ax, (4, 2.7), (4, .8), '$R_2$')
    seg(ax, (4, .8), (1, .8)); seg(ax, (1, .8), (1, 1.8)); seg(ax, (4, 2.7), (5.6, 2.7)); dot(ax, (5.6, 2.7), 'r', 40); dot(ax, (4, 2.7), 'k', 25)
    txt(ax, (5.75, 2.7), r'$V_{out}$', 'r', 12, ha='left'); dot(ax, (5.6, .8), 'k', 25); seg(ax, (4, .8), (5.6, .8)); txt(ax, (5.75, .8), '0 V', 'k', 11, ha='left')
    return fig


def two_loop():
    fig, ax = canvas(7.4, 3.6, (0, 13), (0, 5.6))
    _bat(ax, (1, 2.7), '9 V'); _bat(ax, (12, 2.7), '5 V')
    seg(ax, (1, 3.6), (1, 4.6)); _res(ax, (1, 4.6), (6.5, 4.6), r'$R_1=1\,\mathrm{k}\Omega$'); _res(ax, (6.5, 4.6), (12, 4.6), r'$R_2=1\,\mathrm{k}\Omega$'); seg(ax, (12, 4.6), (12, 3.6))
    _res(ax, (6.5, 4.6), (6.5, .8), r'$R_3=2\,\mathrm{k}\Omega$')
    seg(ax, (1, .8), (12, .8)); seg(ax, (1, .8), (1, 1.8)); seg(ax, (12, .8), (12, 1.8))
    dot(ax, (6.5, 4.6), 'b', 50); txt(ax, (6.5, 5.15), 'node $A$ at $V_A$', 'b', 11); dot(ax, (6.5, .8), 'k', 30); txt(ax, (6.5, .35), '0 V (ground)', 'k', 10)
    arrow(ax, (2.6, 4.05), (4.1, 4.05), 'r', 1.6); txt(ax, (3.35, 3.7), '$I_1$', 'r', 12)
    arrow(ax, (10.4, 4.05), (8.9, 4.05), 'g', 1.6); txt(ax, (9.65, 3.7), '$I_2$', 'g', 12)
    arrow(ax, (5.75, 3.2), (5.75, 2.2), 'p', 1.6); txt(ax, (5.5, 2.7), '$I_3$', 'p', 12, ha='right')
    return fig
