"""Figures for Unit 1 (functions, trigonometry, limits)."""
from figkit import *


# ------------------------------------------------------------------ week 1
def machine():
    fig, ax = canvas(7.6, 1.9, (0, 10), (0, 2.4))
    ax.add_patch(Rectangle((3.6, .5), 2.8, 1.4, facecolor=C['fb'], edgecolor=C['b'], lw=2))
    txt(ax, (5, 1.2), r'$f$:  "square it,' + '\nthen add 1"', 'b', 12)
    arrow(ax, (1.6, 1.2), (3.5, 1.2), 'k'); arrow(ax, (6.5, 1.2), (8.4, 1.2), 'k')
    txt(ax, (.9, 1.2), 'input\n$x = 3$', 'k', 12); txt(ax, (9.2, 1.2), 'output\n$f(3) = 10$', 'k', 12)
    txt(ax, (2.55, 1.5), 'in', 'gr', 10); txt(ax, (7.45, 1.5), 'out', 'gr', 10)
    return fig


def domain_range():
    fig, ax = graph(6.4, 3.4)
    xs = np.linspace(-3, 3, 400); ax.plot(xs, np.sqrt(9 - xs ** 2), color=C['b'])
    ax.plot([-3, 3], [0, 0], color=C['r'], lw=5, alpha=.6, solid_capstyle='butt'); ax.plot([0, 0], [0, 3], color=C['g'], lw=5, alpha=.6, solid_capstyle='butt')
    ax.set_xlim(-4.5, 4.5); ax.set_ylim(-.8, 3.8); ax.set_aspect('equal')
    txt(ax, (2.4, -.45), 'domain $[-3,\\,3]$', 'r', 11); txt(ax, (.2, 3.35), 'range $[0,\\,3]$', 'g', 11, ha='left')
    txt(ax, (3.3, 2.5), r'$y=\sqrt{9-x^2}$', 'b', 12)
    return fig


def inverse_reflect():
    fig, ax = graph(5.2, 5)
    xs = np.linspace(-1, 4.5, 200)
    ax.plot(xs, 2 * xs - 1, color=C['b'], label='$f(x)=2x-1$')
    ax.plot(xs, (xs + 1) / 2, color=C['r'], label=r'$f^{-1}(x)=\dfrac{x+1}{2}$')
    ax.plot(xs, xs, color=C['gr'], ls='--', lw=1.2, label='mirror line $y=x$')
    dot(ax, (2, 3), 'b'); dot(ax, (3, 2), 'r'); seg(ax, (2, 3), (3, 2), 'gr', 1, ':')
    txt(ax, (1.55, 3.25), '$(2,\\,3)$', 'b', 11); txt(ax, (3.5, 1.75), '$(3,\\,2)$', 'r', 11)
    ax.set_xlim(-1, 4.5); ax.set_ylim(-1, 4.5); ax.set_aspect('equal'); ax.legend(loc='upper left', fontsize=10)
    return fig


def shift_right():
    fig, ax = graph(6.6, 3.3)
    xs = np.linspace(-3, 5, 300)
    ax.plot(xs, xs ** 2, color=C['gr'], label='$y=x^2$'); ax.plot(xs, (xs - 2) ** 2, color=C['b'], label='$y=(x-2)^2$')
    for y0 in (1, 4):
        r = math.sqrt(y0); arrow(ax, (r, y0), (r + 2, y0), 'r', 1.4, ms=11); dot(ax, (r, y0), 'gr', 25); dot(ax, (r + 2, y0), 'b', 25)
    dot(ax, (0, 0), 'gr', 25); dot(ax, (2, 0), 'b', 25); arrow(ax, (0, 0), (2, 0), 'r', 1.4, ms=11)
    txt(ax, (1, .45), '+2', 'r', 11)
    ax.set_xlim(-3, 5.2); ax.set_ylim(-.6, 6); ax.legend(loc='upper center', fontsize=10)
    return fig


def radian_def():
    fig, ax = canvas(8.4, 3.9, n=2)
    for a, th, lab in ((ax[0], 57.2958, r'$\theta = 1$ rad'), (ax[1], 130, r'$\theta = \dfrac{s}{r}$')):
        a.set_xlim(-1.35, 1.5); a.set_ylim(-1.25, 1.35)
        circle(a); seg(a, (0, 0), (1, 0), 'k'); seg(a, (0, 0), P(th), 'k')
        tt = np.radians(np.linspace(0, th, 60)); a.plot(np.cos(tt), np.sin(tt), color=C['r'], lw=4)
        angle(a, (0, 0), .28, 0, th, 'b', label=lab, lr=.62 if th < 90 else .5, fill='fb', size=12)
        txt(a, (.5, -.1), '$r$', 'k'); m = P(th / 2, 1.3 if th < 90 else 1.16)
        txt(a, m, '$s = r$' if th < 90 else '$s$', 'r', 13); dot(a, (0, 0), 'k', 18)
    txt(ax[0], (0, -1.18), 'arc as long as the radius  →  1 radian', 'k', 10.5)
    txt(ax[1], (0, -1.18), 'in general: angle = arc ÷ radius', 'k', 10.5)
    return fig


def same_angle_circles():
    fig, ax = canvas(4.6, 3.5, (-.2, 3.4), (-.3, 2.5))
    th = 40
    for r, col in ((1, 'b'), (2, 'g'), (3, 'r')):
        tt = np.radians(np.linspace(0, th, 40)); ax.plot(r * np.cos(tt), r * np.sin(tt), color=C[col], lw=3.5)
        txt(ax, P(th / 2, r + .22), '$s_%d$' % r, col, 12)
    seg(ax, (0, 0), (3.2, 0), 'k', 1.5); seg(ax, (0, 0), P(th, 3.2), 'k', 1.5)
    angle(ax, (0, 0), .45, 0, th, 'k', label=r'$\theta$', lr=.62)
    for r in (1, 2, 3): txt(ax, (r, -.17), '$r=%d$' % r, 'k', 10)
    return fig


def sector():
    fig, ax = canvas(3.8, 3.4, (-1.25, 1.25), (-1.2, 1.25))
    ax.add_patch(Wedge((0, 0), 1, 20, 95, color=C['fy'])); circle(ax)
    seg(ax, (0, 0), P(20)); seg(ax, (0, 0), P(95)); angle(ax, (0, 0), .25, 20, 95, 'b', label=r'$\theta$', lr=.38)
    txt(ax, P(57, .68), r'area $\frac{1}{2}r^2\theta$', 'o', 11); txt(ax, P(57, 1.13), r'$s=r\theta$', 'r', 12); txt(ax, P(8, .55), '$r$')
    tt = np.radians(np.linspace(20, 95, 40)); ax.plot(np.cos(tt), np.sin(tt), color=C['r'], lw=3.5)
    return fig


def similar_triangles():
    fig, ax = canvas(7.4, 2.9, (-.2, 8.4), (-.6, 3.2))
    th = math.radians(35)
    for x0, L, col in ((0, 2.2, 'fb'), (3.2, 4.6, 'fg')):
        A, B, Cc = (x0, 0), (x0 + L, 0), (x0 + L, L * math.tan(th))
        poly(ax, [A, B, Cc], col); rightangle(ax, B, (-1, 0), (0, 1), .16)
        angle(ax, A, .5, 0, 35, 'b', label=r'$\theta$', lr=.72)
        txt(ax, ((A[0] + B[0]) / 2, -.25), 'adjacent', 'k', 10); txt(ax, (B[0] + .1, Cc[1] / 2), 'opposite', 'k', 10, ha='left')
        txt(ax, ((A[0] + Cc[0]) / 2 - .25, Cc[1] / 2 + .28), 'hypotenuse', 'k', 10, rotation=35)
    return fig


def pythagoras():
    fig, ax = canvas(8.6, 4.2, n=2)
    a, b = 3, 4; s = a + b
    for k, A in enumerate(ax):
        A.set_xlim(-.6, s + .6); A.set_ylim(-1.1, s + .6)
        A.add_patch(Rectangle((0, 0), s, s, fill=False, edgecolor=C['k'], lw=2))
    A = ax[0]   # tilted square c^2 in the middle
    T = [[(0, 0), (a, 0), (0, b)], [(a, 0), (s, 0), (s, a)], [(s, a), (s, s), (b, s)], [(b, s), (0, s), (0, b)]]
    for tri in T: poly(A, tri, 'fb')
    poly(A, [(a, 0), (s, a), (b, s), (0, b)], 'fy'); txt(A, (s / 2, s / 2), '$c^2$', 'o', 20)
    txt(A, (a / 2, -.35), '$a$'); txt(A, (a + b / 2, -.35), '$b$'); txt(A, (-.35, b / 2), '$b$'); txt(A, (-.35, b + a / 2), '$a$')
    txt(A, (a / 2 + .35, b / 2 + .3), '$c$', 'o', 13)
    txt(A, (s / 2, -.85), 'four triangles + one tilted square $c^2$', 'k', 10.5)
    A = ax[1]   # same triangles pushed into two rectangles
    poly(A, [(0, 0), (a, 0), (a, b)], 'fb'); poly(A, [(0, 0), (0, b), (a, b)], 'fb')
    poly(A, [(a, b), (s, b), (s, s)], 'fb'); poly(A, [(a, b), (a, s), (s, s)], 'fb')
    poly(A, [(0, b), (a, b), (a, s), (0, s)], 'fg'); poly(A, [(a, 0), (s, 0), (s, b), (a, b)], 'fr')
    txt(A, (a / 2, b + a / 2), '$a^2$', 'g', 18); txt(A, (a + b / 2, b / 2), '$b^2$', 'r', 20)
    txt(A, (a / 2, -.35), '$a$'); txt(A, (a + b / 2, -.35), '$b$'); txt(A, (-.35, b / 2), '$b$'); txt(A, (-.35, b + a / 2), '$a$')
    txt(A, (s / 2, -.85), 'the same four triangles + squares $a^2$ and $b^2$', 'k', 10.5)
    return fig


def special_triangles():
    fig, ax = canvas(8.6, 3.5, n=2)
    A = ax[0]; A.set_xlim(-.5, 2.3); A.set_ylim(-.5, 1.6)
    A.add_patch(Rectangle((0, 0), 1, 1, fill=False, edgecolor=C['gr'], lw=1.2, ls='--'))
    poly(A, [(0, 0), (1, 0), (1, 1)], 'fb'); rightangle(A, (1, 0), (-1, 0), (0, 1), .07)
    angle(A, (0, 0), .22, 0, 45, 'b', label=r'$45^\circ$', lr=.36, size=11); angle(A, (1, 1), .2, 225, 270, 'b', label=r'$45^\circ$', lr=.34, size=11)
    txt(A, (.5, -.12), '$1$'); txt(A, (1.1, .5), '$1$'); txt(A, (.38, .58), r'$\sqrt{2}$', 'r', 13)
    txt(A, (1.05, -.38), 'half of a square with side 1', 'k', 10.5)
    A = ax[1]; A.set_xlim(-.4, 2.5); A.set_ylim(-.62, 2.0)
    hgt = math.sqrt(3)
    A.add_patch(Polygon([(0, 0), (2, 0), (1, hgt)], closed=True, fill=False, edgecolor=C['gr'], lw=1.2, ls='--'))
    poly(A, [(0, 0), (1, 0), (1, hgt)], 'fg'); rightangle(A, (1, 0), (-1, 0), (0, 1), .09)
    angle(A, (0, 0), .3, 0, 60, 'g', label=r'$60^\circ$', lr=.5, size=11); angle(A, (1, hgt), .36, 240, 270, 'g', label=r'$30^\circ$', lr=.56, size=11)
    txt(A, (.5, -.14), '$1$'); txt(A, (1.5, -.14), '$1$', 'gr'); txt(A, (.36, .95), '$2$'); txt(A, (1.64, .95), '$2$', 'gr'); txt(A, (1.16, .7), r'$\sqrt{3}$', 'r', 13)
    txt(A, (1.05, -.47), 'half of an equilateral triangle with side 2', 'k', 10.5)
    return fig


def unit_circle_def(th=38):
    fig, ax = canvas(4.9, 4.6, (-1.45, 1.6), (-1.4, 1.5))
    axes_cross(ax, 1.33); circle(ax)
    p = P(th); poly(ax, [(0, 0), (p[0], 0), p], 'fb', 'k', 1)
    seg(ax, (0, 0), p, 'k', 2.2); seg(ax, (p[0], 0), p, 'r', 3); seg(ax, (0, 0), (p[0], 0), 'b', 3)
    rightangle(ax, (p[0], 0), (-1, 0), (0, 1), .07); angle(ax, (0, 0), .25, 0, th, 'k', label=r'$\theta$', lr=.38)
    dot(ax, p); txt(ax, (p[0] + .08, p[1] + .12), r'$P=(\cos\theta,\ \sin\theta)$', 'k', 12, ha='left')
    txt(ax, (p[0] / 2, -.12), r'$\cos\theta$', 'b', 12); txt(ax, (p[0] + .08, p[1] / 2), r'$\sin\theta$', 'r', 12, ha='left')
    txt(ax, (.3, .38), '$1$'); txt(ax, (1.07, -.12), '$1$', 'gr', 10); txt(ax, (-.1, 1.08), '$1$', 'gr', 10)
    return fig


def quadrants():
    fig, ax = canvas(10, 2.9, n=4)
    data = [(40, 'I', r'$\theta$ itself'), (140, 'II', r'$\pi-\theta$'), (220, 'III', r'$\theta-\pi$'), (320, 'IV', r'$2\pi-\theta$')]
    signs = ['sin +, cos +', 'sin +, cos −', 'sin −, cos −', 'sin −, cos +']
    for A, (th, q, ref), sg in zip(ax, data, signs):
        A.set_xlim(-1.3, 1.3); A.set_ylim(-1.55, 1.45); axes_cross(A, 1.2, ('', '')); circle(A)
        p = P(th); seg(A, (0, 0), p, 'k', 2); seg(A, (p[0], 0), p, 'r', 2.5); seg(A, (0, 0), (p[0], 0), 'b', 2.5); dot(A, p, 'k', 22)
        angle(A, (0, 0), .2, 0, th, 'gr', 1.2)
        base = 0 if p[0] > 0 else 180
        a0, a1 = sorted([base, th if abs(th - base) < 90 else th - 360 if base == 0 else th])
        angle(A, (0, 0), .42, a0, a1, 'o', 2, fill='fy')
        txt(A, (0, 1.33), 'quadrant ' + q, 'k', 11); txt(A, (0, -1.28), 'reference angle: ' + ref, 'o', 10); txt(A, (0, -1.5), sg, 'k', 10)
    return fig


def symmetries():
    fig, ax = canvas(10, 3.0, n=4)
    th = 35
    cases = [(-th, r'$-\theta$', 'mirror in the $x$-axis', r'$(\cos\theta,\,-\sin\theta)$'),
             (180 - th, r'$\pi-\theta$', 'mirror in the $y$-axis', r'$(-\cos\theta,\ \sin\theta)$'),
             (180 + th, r'$\theta+\pi$', 'half turn about $O$', r'$(-\cos\theta,\,-\sin\theta)$'),
             (90 - th, r'$\frac{\pi}{2}-\theta$', 'mirror in the line $y=x$', r'$(\sin\theta,\ \cos\theta)$')]
    for A, (t2, name, how, coord) in zip(ax, cases):
        A.set_xlim(-1.3, 1.3); A.set_ylim(-1.75, 1.45); axes_cross(A, 1.2, ('', '')); circle(A)
        p, q = P(th), P(t2)
        seg(A, (0, 0), p, 'gr', 2); dot(A, p, 'gr', 25); seg(A, (0, 0), q, 'r', 2); dot(A, q, 'r', 25); seg(A, p, q, 'gr', 1, ':')
        if 'y=x' in how: seg(A, (-1.1, -1.1), (1.1, 1.1), 'b', 1, '--')
        txt(A, (p[0] + .12, p[1] + .13), r'$\theta$', 'gr', 11); txt(A, (q[0] * 1.22, q[1] * 1.22 + (0.08 if q[1] > 0 else -.08)), name, 'r', 11)
        txt(A, (0, 1.36), how, 'k', 10); txt(A, (0, -1.45), 'new point', 'k', 9.5); txt(A, (0, -1.68), coord, 'r', 10.5)
    return fig


def unit_circle_full():
    fig, ax = canvas(7.4, 7.2, (-1.75, 1.75), (-1.7, 1.7))
    axes_cross(ax, 1.25, ('', '')); circle(ax, col='k')
    F = {0: '0', 30: r'\frac{\pi}{6}', 45: r'\frac{\pi}{4}', 60: r'\frac{\pi}{3}', 90: r'\frac{\pi}{2}', 120: r'\frac{2\pi}{3}', 135: r'\frac{3\pi}{4}',
         150: r'\frac{5\pi}{6}', 180: r'\pi', 210: r'\frac{7\pi}{6}', 225: r'\frac{5\pi}{4}', 240: r'\frac{4\pi}{3}', 270: r'\frac{3\pi}{2}',
         300: r'\frac{5\pi}{3}', 315: r'\frac{7\pi}{4}', 330: r'\frac{11\pi}{6}'}
    V = {0: '0', .5: r'\frac{1}{2}', 1: '1'}

    def val(v):
        s = '-' if v < -1e-9 else ''
        a = abs(v)
        for ref, tex in ((0, '0'), (.5, r'\frac{1}{2}'), (math.sqrt(2) / 2, r'\frac{\sqrt{2}}{2}'), (math.sqrt(3) / 2, r'\frac{\sqrt{3}}{2}'), (1, '1')):
            if abs(a - ref) < 1e-9: return s + tex
    for d, tex in F.items():
        p = P(d); col = 'r' if d % 90 == 0 else ('b' if d % 45 == 0 else 'g')
        seg(ax, (0, 0), p, col, 1, alpha=.55); dot(ax, p, col, 28)
        txt(ax, P(d, .74), '$%s$' % tex, col, 13)
        txt(ax, P(d, 1.42), r'$(%s,\ %s)$' % (val(p[0]), val(p[1])), 'k', 10.5)
    txt(ax, (0, 0), ' ', 'k')
    return fig


def unroll():
    fig, ax = plt.subplots(1, 2, figsize=(10, 3.3), gridspec_kw={'width_ratios': [1, 2.1]})
    A, B = ax
    A.set_aspect('equal'); A.axis('off'); A.set_xlim(-1.3, 1.3); A.set_ylim(-1.3, 1.3); axes_cross(A, 1.2, ('', '')); circle(A)
    B.grid(True, alpha=.3); B.axhline(0, color=C['k'], lw=.8)
    tt = np.linspace(0, 2 * np.pi, 300); B.plot(tt, np.sin(tt), color=C['r'])
    cols = ['b', 'g', 'o', 'p']
    for d, col in zip((50, 140, 230, 320), cols):
        p = P(d); th = math.radians(d)
        seg(A, (0, 0), p, col, 1.5); seg(A, (p[0], 0), p, col, 3); dot(A, p, col, 25)
        B.plot([th, th], [0, math.sin(th)], color=C[col], lw=3); B.scatter([th], [math.sin(th)], color=C[col], zorder=5, s=25)
    B.set_xticks([k * np.pi / 2 for k in range(5)]); B.set_xticklabels(['0', r'$\pi/2$', r'$\pi$', r'$3\pi/2$', r'$2\pi$'])
    B.set_xlabel(r'angle $\theta$ (rad)'); B.set_ylabel(r'height $=\sin\theta$'); B.set_ylim(-1.25, 1.25)
    A.set_title('height of the point on the circle…', fontsize=10.5); B.set_title('…plotted against the angle', fontsize=10.5)
    return fig


def solve_sin():
    fig, ax = canvas(8.8, 3.9, n=2)
    A = ax[0]; A.set_xlim(-1.45, 1.45); A.set_ylim(-1.35, 1.4); axes_cross(A, 1.3, ('', '')); circle(A)
    seg(A, (-1.3, .5), (1.3, .5), 'r', 1.5, '--'); txt(A, (0.35, .64), r'$y=\frac{1}{2}$', 'r', 11)
    for d, col, lab in ((30, 'b', r'$\frac{\pi}{6}$'), (150, 'g', r'$\pi-\frac{\pi}{6}$')):
        p = P(d); seg(A, (0, 0), p, col, 2); dot(A, p, col, 30); angle(A, (0, 0), .3 if d < 90 else .2, 0, d, col, 1.3)
        txt(A, P(d - 12 if d < 90 else d + 12, 1.3), lab, col, 12)
    txt(A, (0, -1.25), r'$\sin\theta=\frac{1}{2}$: two points at that height', 'k', 10.5)
    A = ax[1]; A.set_xlim(-1.45, 1.45); A.set_ylim(-1.35, 1.4); axes_cross(A, 1.3, ('', '')); circle(A)
    seg(A, (-.5, -1.3), (-.5, 1.3), 'r', 1.5, '--'); txt(A, (-.82, .2), r'$x=-\frac{1}{2}$', 'r', 11)
    for d, col, lab in ((120, 'b', r'$\frac{2\pi}{3}$'), (240, 'g', r'$\frac{4\pi}{3}$')):
        p = P(d); seg(A, (0, 0), p, col, 2); dot(A, p, col, 30); txt(A, P(d + (14 if d < 180 else -14), 1.3), lab, col, 12)
    txt(A, (0, -1.25), r'$\cos\theta=-\frac{1}{2}$: two points with that $x$', 'k', 10.5)
    return fig


def tan_slope():
    fig, ax = canvas(4.6, 4.3, (-1.4, 1.75), (-1.35, 1.5))
    axes_cross(ax, 1.3, ('', '')); circle(ax); th = 40; p = P(th); T = (1, math.tan(math.radians(th)))
    seg(ax, (1, -1.3), (1, 1.4), 'gr', 1, '--'); seg(ax, (0, 0), T, 'k', 1.6); dot(ax, p); dot(ax, T, 'p')
    seg(ax, (1, 0), T, 'p', 3.2); angle(ax, (0, 0), .25, 0, th, 'k', label=r'$\theta$', lr=.38)
    txt(ax, (1.08, T[1] / 2), r'$\tan\theta$', 'p', 12, ha='left'); txt(ax, (.5, -.12), '$1$')
    txt(ax, (1.05, 1.32), 'tangent line $x=1$', 'gr', 9.5, ha='left')
    return fig


def small_angle():
    fig, ax = canvas(8.6, 3.2, n=2)
    for A, th in zip(ax, (50, 14)):
        A.set_xlim(-.1, 1.5); A.set_ylim(-.22, 1.3 if th > 30 else .5)
        tt = np.radians(np.linspace(0, 90 if th > 30 else 30, 80)); A.plot(np.cos(tt), np.sin(tt), color=C['gr'], lw=1.3)
        seg(A, (0, 0), (1.25, 0), 'gr', 1); p = P(th); T = (1, math.tan(math.radians(th)))
        seg(A, (0, 0), T, 'k', 1.3); seg(A, (p[0], 0), p, 'r', 3); seg(A, (1, 0), T, 'p', 3)
        ta = np.radians(np.linspace(0, th, 40)); A.plot(np.cos(ta), np.sin(ta), color=C['b'], lw=3)
        angle(A, (0, 0), .2, 0, th, 'k', label=r'$\theta$', lr=.3)
        txt(A, (p[0] - .04, p[1] / 2), r'$\sin\theta$', 'r', 11, ha='right'); txt(A, (1.04, T[1] / 2), r'$\tan\theta$', 'p', 11, ha='left')
        if th > 30: txt(A, P(th * .5, .8), r'arc $=\theta$', 'b', 11)
        A.set_title('large angle: three clearly different lengths' if th > 30 else 'small angle: the three almost coincide', fontsize=10.5)
    return fig


# ------------------------------------------------------------------ week 2
def cos_diff():
    fig, ax = canvas(9, 4.2, n=2)
    a, b = 110, 35
    A = ax[0]; A.set_xlim(-1.45, 1.6); A.set_ylim(-1.4, 1.45); axes_cross(A, 1.3, ('', '')); circle(A)
    pa, pb = P(a), P(b); seg(A, (0, 0), pa, 'b'); seg(A, (0, 0), pb, 'g'); seg(A, pa, pb, 'r', 3); dot(A, pa, 'b'); dot(A, pb, 'g')
    angle(A, (0, 0), .22, 0, b, 'g', 1.3, label='$b$', lr=.33); angle(A, (0, 0), .45, 0, a, 'b', 1.3, label='$a$', lr=.56)
    angle(A, (0, 0), .7, b, a, 'r', 1.5, label='$a-b$', lr=.86, size=11)
    txt(A, (pa[0] - .1, pa[1] + .13), r'$A=(\cos a,\ \sin a)$', 'b', 10.5); txt(A, (pb[0] + .08, pb[1] + .13), r'$B=(\cos b,\ \sin b)$', 'g', 10.5, ha='left')
    txt(A, (.42, 1.0), '$d$', 'r', 14); txt(A, (0, -1.3), 'chord between the two points', 'k', 10.5)
    A = ax[1]; A.set_xlim(-1.45, 1.6); A.set_ylim(-1.4, 1.45); axes_cross(A, 1.3, ('', '')); circle(A)
    pc, pd = P(a - b), (1, 0); seg(A, (0, 0), pc, 'b'); seg(A, (0, 0), pd, 'g'); seg(A, pc, pd, 'r', 3); dot(A, pc, 'b'); dot(A, pd, 'g')
    angle(A, (0, 0), .4, 0, a - b, 'r', 1.5, label='$a-b$', lr=.6, size=11)
    txt(A, (pc[0] + .05, pc[1] + .14), r"$A'=(\cos(a-b),\ \sin(a-b))$", 'b', 10.5, ha='left'); txt(A, (1.06, -.14), r"$B'=(1,\,0)$", 'g', 10.5, ha='left')
    txt(A, (.78, .58), '$d$', 'r', 14); txt(A, (0, -1.3), 'the same picture turned back by $b$: same chord', 'k', 10.5)
    return fig


def sinusoid_anatomy():
    fig, ax = plt.subplots(figsize=(9, 3.8))
    A_, w, ph, C0 = 2, 2, math.pi / 3, 1
    ts = np.linspace(-1.2, 6, 600); ax.plot(ts, A_ * np.sin(w * ts + ph) + C0, color=C['b'])
    ax.axhline(C0, color=C['gr'], ls='--', lw=1.2); ax.axhline(0, color=C['k'], lw=.8); ax.axvline(0, color=C['k'], lw=.8); ax.grid(True, alpha=.3)
    t0 = -ph / w; tp = t0 + math.pi / (2 * w)
    arrow(ax, (tp, C0), (tp, C0 + A_), 'r', 1.5, '<|-|>', 11); txt(ax, (tp + .1, C0 + A_ / 2), 'amplitude $A$', 'r', 11, ha='left')
    T_ = 2 * math.pi / w
    arrow(ax, (tp, C0 + A_ + .25), (tp + T_, C0 + A_ + .25), 'g', 1.5, '<|-|>', 11); txt(ax, (tp + T_ / 2, C0 + A_ + .52), r'period $T=\dfrac{2\pi}{\omega}$', 'g', 11)
    arrow(ax, (0, C0 - A_ - .3), (t0, C0 - A_ - .3), 'p', 1.5, '-|>', 11); txt(ax, (t0 - .05, C0 - A_ - .62), r'shift left by $\varphi/\omega$', 'p', 11, ha='center')
    dot(ax, (t0, C0), 'p', 30); ax.plot([t0, t0], [C0 - A_ - .3, C0], color=C['p'], ls=':', lw=1)
    txt(ax, (5.9, C0 + .2), 'midline $y=C$', 'gr', 10.5, ha='right')
    ax.plot(ts, A_ * np.sin(w * ts) + C0, color=C['gr'], lw=1, ls=':'); ax.set_ylim(-2.2, 4.3); ax.set_xlim(-1.2, 6); ax.set_xlabel('$t$')
    ax.set_title(r'$y=A\sin(\omega t+\varphi)+C$   (dotted: the same wave with $\varphi=0$)', fontsize=11)
    return fig


def rphi_triangle():
    fig, ax = canvas(8.8, 3.6, n=2)
    A = ax[0]; A.set_xlim(-.6, 4.3); A.set_ylim(-.9, 4.6)
    poly(A, [(0, 0), (3, 0), (3, 4)], 'fb'); rightangle(A, (3, 0), (-1, 0), (0, 1), .2)
    angle(A, (0, 0), .7, 0, 53.13, 'r', label=r'$\varphi$', lr=1.0)
    txt(A, (1.5, -.3), '$a$'); txt(A, (3.25, 2), '$b$'); txt(A, (1.2, 2.3), r'$R=\sqrt{a^2+b^2}$', 'o', 12, rotation=53)
    txt(A, (1.9, -.75), r'$a=R\cos\varphi,\quad b=R\sin\varphi$', 'k', 11)
    A = ax[1]; A.set_xlim(-1.5, 5.6); A.set_ylim(-1.1, 5); arrow(A, (-1, 0), (5, 0), 'gr', 1); arrow(A, (0, -.8), (0, 4.8), 'gr', 1)
    arrow(A, (0, 0), (3, 0), 'b', 2.4); arrow(A, (3, 0), (3, 4), 'g', 2.4); arrow(A, (0, 0), (3, 4), 'r', 2.8)
    txt(A, (1.5, -.35), r'$a\sin x$', 'b', 11); txt(A, (3.15, 2), r'$b\cos x$', 'g', 11, ha='left'); txt(A, (1.0, 2.2), r'$R$', 'r', 13)
    angle(A, (0, 0), .8, 0, 53.13, 'r', label=r'$\varphi$', lr=1.1)
    txt(A, (2, -.9), 'as arrows (phasors): add tip to tail', 'k', 10.5)
    return fig


def inverse_branches():
    fig, ax = plt.subplots(1, 3, figsize=(10.4, 3.3))
    xs = np.linspace(-2 * np.pi, 2 * np.pi, 600)
    for A, f, lo, hi, name in ((ax[0], np.sin, -np.pi / 2, np.pi / 2, 'sin'), (ax[1], np.cos, 0, np.pi, 'cos')):
        A.plot(xs, f(xs), color=C['gr'], lw=1.3); xb = np.linspace(lo, hi, 100); A.plot(xb, f(xb), color=C['r'], lw=3.5)
        A.axhline(0, color=C['k'], lw=.8); A.axvline(0, color=C['k'], lw=.8); A.grid(True, alpha=.3)
        A.axhline(.6, color=C['b'], ls='--', lw=1); A.set_title('%s: red branch is one-to-one' % name, fontsize=10.5)
        A.set_xticks([-np.pi, -np.pi / 2, 0, np.pi / 2, np.pi]); A.set_xticklabels([r'$-\pi$', r'$-\frac{\pi}{2}$', '0', r'$\frac{\pi}{2}$', r'$\pi$'])
        A.set_xlim(-2 * np.pi, 2 * np.pi)
    A = ax[2]; xt = np.linspace(-1.45, 1.45, 200)
    for k in (-1, 0, 1): A.plot(xt + k * np.pi, np.tan(xt), color=C['r'] if k == 0 else C['gr'], lw=3.5 if k == 0 else 1.3)
    A.set_ylim(-5, 5); A.axhline(0, color=C['k'], lw=.8); A.axvline(0, color=C['k'], lw=.8); A.grid(True, alpha=.3); A.set_title('tan: red branch is one-to-one', fontsize=10.5)
    A.set_xticks([-np.pi, -np.pi / 2, 0, np.pi / 2, np.pi]); A.set_xticklabels([r'$-\pi$', r'$-\frac{\pi}{2}$', '0', r'$\frac{\pi}{2}$', r'$\pi$'])
    fig.tight_layout()
    return fig


def law_cos():
    fig, ax = canvas(8.8, 3.3, n=2)
    for A, title in zip(ax, ('law of cosines: split $a$ with the height $h$', 'law of sines: write $h$ in two ways')):
        A.set_xlim(-.5, 5.6); A.set_ylim(-.9, 3.4)
        Cc, B, Aa = (0, 0), (5, 0), (1.6, 2.6)
        poly(A, [Cc, B, Aa], 'fb'); seg(A, Aa, (1.6, 0), 'r', 1.6, '--'); rightangle(A, (1.6, 0), (1, 0), (0, 1), .16, 'r')
        txt(A, (1.78, 1.2), '$h$', 'r', 12); txt(A, (-.2, -.15), '$C$'); txt(A, (5.2, -.15), '$B$'); txt(A, (1.6, 2.85), '$A$')
        txt(A, (.55, 1.5), '$b$'); txt(A, (3.55, 1.5), '$c$'); txt(A, (2.5, -.7), title, 'k', 10.5)
    A = ax[0]; txt(A, (.8, -.25), r'$b\cos C$', 'g', 10.5); txt(A, (3.3, -.25), r'$a-b\cos C$', 'g', 10.5); angle(A, (0, 0), .5, 0, 58.4, 'k', label='$C$', lr=.75, size=11)
    A = ax[1]; txt(A, (2.9, -.25), '$a$'); angle(A, (0, 0), .5, 0, 58.4, 'k', label='$C$', lr=.75, size=11); angle(A, (5, 0), .6, 142.6, 180, 'k', label='$B$', lr=.9, size=11)
    return fig


def addition_geo():
    """Classic stacked-triangle proof of sin(a+b), cos(a+b) for acute angles."""
    fig, ax = canvas(6.2, 4.6, (-.25, 1.25), (-.2, 1.05))
    a, b = math.radians(28), math.radians(34)
    O = (0, 0); Pp = (math.cos(a + b), math.sin(a + b))        # OP = 1, at angle a+b
    Q = (math.cos(b) * math.cos(a), math.cos(b) * math.sin(a))  # foot on the ray at angle a: OQ = cos b, PQ = sin b
    Aft = (Q[0], 0); Bft = (Pp[0], 0); R = (Pp[0], Q[1])
    poly(ax, [O, Aft, Q], 'fb', 'k', 1.2); poly(ax, [O, Q, Pp], 'fg', 'k', 1.2); poly(ax, [R, Q, Pp], 'fy', 'k', 1.2)
    seg(ax, Pp, Bft, 'r', 1.4, '--'); seg(ax, O, (1.15, 0), 'gr', 1)
    rightangle(ax, Aft, (-1, 0), (0, 1), .03); rightangle(ax, Q, (-math.cos(a), -math.sin(a)), (-math.sin(a), math.cos(a)), .03); rightangle(ax, R, (1, 0), (0, 1), .03)
    angle(ax, O, .16, 0, math.degrees(a), 'b', label='$a$', lr=.21, size=12); angle(ax, O, .24, math.degrees(a), math.degrees(a + b), 'g', label='$b$', lr=.3, size=12)
    angle(ax, Pp, .12, 270, 270 + math.degrees(a), 'o', label='$a$', lr=.17, size=11)
    for p_, s_, d in ((O, '$O$', (-.04, -.04)), (Pp, '$P$', (-.03, .04)), (Q, '$Q$', (.04, .02)), (Aft, '$A$', (0, -.05)), (Bft, '$B$', (0, -.05)), (R, '$R$', (-.04, 0))):
        txt(ax, (p_[0] + d[0], p_[1] + d[1]), s_, 'k', 12)
    txt(ax, (Pp[0] / 2 - .06, Pp[1] / 2 + .03), '$1$', 'k', 12); txt(ax, ((Q[0]) / 2 + .03, Q[1] / 2 - .045), r'$\cos b$', 'g', 11, rotation=28)
    txt(ax, ((Pp[0] + Q[0]) / 2 + .055, (Pp[1] + Q[1]) / 2 + .03), r'$\sin b$', 'g', 11, rotation=-62)
    return fig


# ------------------------------------------------------------------ week 3
def hole():
    fig, ax = graph(5.6, 3.6)
    xs = np.linspace(0, 5, 100); ax.plot(xs, xs + 3, color=C['b'])
    ax.scatter([3], [6], s=70, facecolor='white', edgecolor=C['b'], zorder=5, lw=2)
    ax.plot([3, 3], [0, 6], color=C['gr'], ls=':', lw=1); ax.plot([0, 3], [6, 6], color=C['gr'], ls=':', lw=1)
    arrow(ax, (1.9, 4.55), (2.75, 5.4), 'r', 1.6, ms=12); arrow(ax, (4.1, 7.45), (3.25, 6.6), 'r', 1.6, ms=12)
    ax.set_xlim(0, 5); ax.set_ylim(0, 8.5); ax.set_xlabel('$x$'); txt(ax, (1.5, 7.4), r'$y=\dfrac{x^2-9}{x-3}$', 'b', 13)
    txt(ax, (3.9, 4.6), 'no point at $x=3$,\nbut the graph heads to 6', 'k', 10)
    return fig


def limit_fail():
    fig, ax = plt.subplots(1, 3, figsize=(10.4, 3.1))
    A = ax[0]; A.plot([-2, 0], [-1, -1], color=C['b']); A.plot([0, 2], [1, 1], color=C['b'])
    A.scatter([0, 0], [-1, 1], s=50, facecolor='white', edgecolor=C['b'], zorder=5, lw=2); A.set_title('jump: left and right disagree', fontsize=10.5); A.set_ylim(-2, 2)
    A = ax[1]; xs = np.linspace(.05, 2, 200); A.plot(xs, 1 / xs ** 2, color=C['b']); A.plot(-xs, 1 / xs ** 2, color=C['b']); A.set_ylim(0, 30); A.set_title('blow-up: grows without bound', fontsize=10.5)
    A = ax[2]; xs = np.linspace(.01, 1, 6000); A.plot(xs, np.sin(1 / xs), color=C['b'], lw=.7); A.plot(-xs, np.sin(-1 / xs), color=C['b'], lw=.7); A.set_title(r'oscillation: $\sin(1/x)$ never settles', fontsize=10.5)
    for A in ax: A.grid(True, alpha=.3); A.axvline(0, color=C['k'], lw=.8); A.axhline(0, color=C['k'], lw=.8)
    fig.tight_layout()
    return fig


def squeeze():
    fig, ax = canvas(6.4, 4.4, (-.15, 1.75), (-.25, 1.2))
    th = 48; p = P(th); T = (1, math.tan(math.radians(th)))
    poly(ax, [(0, 0), (1, 0), T], 'fp', 'p', 1.2)
    ax.add_patch(Wedge((0, 0), 1, 0, th, facecolor=C['fb'], edgecolor=C['b'], lw=1.5))
    poly(ax, [(0, 0), (1, 0), p], 'fr', 'r', 1.5)
    tt = np.radians(np.linspace(0, 90, 90)); ax.plot(np.cos(tt), np.sin(tt), color=C['gr'], lw=1)
    seg(ax, (0, 0), (1.3, 0), 'gr', 1); seg(ax, (p[0], 0), p, 'r', 1.3, '--')
    angle(ax, (0, 0), .2, 0, th, 'k', label='$x$', lr=.28)
    txt(ax, (-.06, -.07), '$O$'); txt(ax, (1.0, -.09), '$A=(1,0)$', ha='center'); txt(ax, (p[0] - .08, p[1] + .07), '$P$'); txt(ax, (T[0] + .07, T[1] + .03), '$T$')
    txt(ax, (p[0] + .02, p[1] / 2 - .05), r'$\sin x$', 'r', 11, ha='left'); txt(ax, (1.04, T[1] * .62), r'$\tan x$', 'p', 11, ha='left'); txt(ax, (.5, -.09), '$1$')
    txt(ax, (1.42, .28), 'triangle $OAP$  (red)\n≤ sector $OAP$  (blue)\n≤ triangle $OAT$  (purple)', 'k', 10, ha='center')
    return fig


def eps_delta():
    fig, ax = graph(6, 4)
    xs = np.linspace(0, 5, 50); ax.plot(xs, 2 * xs + 1, color=C['b'])
    L, a, eps = 7, 3, 1.2; d = eps / 2
    ax.axhspan(L - eps, L + eps, color=C['fr'], alpha=.9); ax.axvspan(a - d, a + d, color=C['fb'], alpha=.9)
    ax.plot(xs, 2 * xs + 1, color=C['b']); dot(ax, (a, L), 'k', 30)
    txt(ax, (.75, L + eps + .35), r'$L+\varepsilon$', 'r', 11); txt(ax, (.75, L - eps - .4), r'$L-\varepsilon$', 'r', 11)
    txt(ax, (a - d - .05, .5), r'$a-\delta$', 'b', 11, ha='right'); txt(ax, (a + d + .05, .5), r'$a+\delta$', 'b', 11, ha='left')
    ax.set_xlim(0, 5); ax.set_ylim(0, 11); txt(ax, (4.2, 8.2), '$y=2x+1$', 'b', 12, ha='left')
    txt(ax, (1.35, 9.9), 'every $x$ in the blue strip\nlands inside the red strip', 'k', 10)
    return fig


def discontinuities():
    fig, ax = plt.subplots(1, 4, figsize=(11, 2.8))
    xs = np.linspace(-2, 2, 400)
    A = ax[0]; A.plot(xs, xs + 1, color=C['b']); A.scatter([1], [2], s=50, facecolor='white', edgecolor=C['b'], zorder=5, lw=2); A.scatter([1], [.7], s=30, color=C['b'], zorder=5); A.set_title('removable (a hole)', fontsize=10.5)
    A = ax[1]; A.plot(xs[xs < 0], xs[xs < 0] * .5 - .5, color=C['b']); A.plot(xs[xs >= 0], xs[xs >= 0] * .5 + 1, color=C['b']); A.scatter([0], [-.5], s=50, facecolor='white', edgecolor=C['b'], zorder=5, lw=2); A.scatter([0], [1], s=30, color=C['b'], zorder=5); A.set_title('jump', fontsize=10.5)
    A = ax[2]; xl = np.linspace(-2, -.05, 200); A.plot(xl, 1 / xl, color=C['b']); A.plot(-xl, -1 / xl, color=C['b']); A.set_ylim(-10, 10); A.set_title('infinite (asymptote)', fontsize=10.5)
    A = ax[3]; xo = np.linspace(.01, 2, 5000); A.plot(xo, np.sin(1 / xo), color=C['b'], lw=.7); A.plot(-xo, -np.sin(1 / xo), color=C['b'], lw=.7); A.set_title('oscillating', fontsize=10.5)
    for A in ax: A.grid(True, alpha=.3)
    fig.tight_layout()
    return fig


def bisection():
    fig, ax = graph(7, 3.5)
    f = lambda v: v ** 3 - v - 1
    xs = np.linspace(.8, 2.1, 200); ax.plot(xs, f(xs), color=C['b'])
    a, b = 1.0, 2.0
    for k in range(4):
        y = -1.6 - .55 * k
        ax.plot([a, b], [y, y], color=C['r'], lw=4, solid_capstyle='butt'); txt(ax, (2.13, y), 'step %d' % k, 'r', 9.5, ha='left')
        m = (a + b) / 2
        if f(a) * f(m) <= 0: b = m
        else: a = m
    dot(ax, (1.3247, 0), 'k', 40); txt(ax, (1.36, .5), 'root', 'k', 10.5, ha='left')
    ax.set_xlim(.8, 2.4); ax.set_ylim(-3.6, 5.2); txt(ax, (1.72, 3.9), '$f(x)=x^3-x-1$', 'b', 12, ha='right')
    txt(ax, (1.0, -1.05), '$f<0$', 'k', 10); txt(ax, (2.0, -1.05), '$f>0$', 'k', 10)
    return fig


def secant_speed():
    fig, ax = graph(6.4, 3.8)
    ts = np.linspace(0, 3.2, 100); ax.plot(ts, 5 * ts ** 2, color=C['b'])
    for hh, col in ((1.5, 'g'), (.8, 'o'), (.3, 'r')):
        t0, t1 = 1, 1 + hh; m = (5 * t1 ** 2 - 5) / hh; xs = np.array([.4, 3.1]); ax.plot(xs, 5 + m * (xs - 1), color=C[col], lw=1.3, label='h = %.1f: average speed %.1f m/s' % (hh, m))
        dot(ax, (t1, 5 * t1 ** 2), col, 25)
    dot(ax, (1, 5), 'k', 35); ax.set_xlim(0, 3.2); ax.set_ylim(-5, 45); ax.set_xlabel('time $t$ (s)'); ax.set_ylabel('distance fallen $s$ (m)'); ax.legend(fontsize=9.5, loc='upper left')
    return fig


def rational_inf():
    fig, ax = graph(6.6, 3.5)
    xs = np.linspace(-10, 10, 2000); y = (2 * xs ** 2 + 1) / (xs ** 2 - 4); y[np.abs(y) > 12] = np.nan
    ax.plot(xs, y, color=C['b']); ax.axhline(2, color=C['r'], ls='--', lw=1.3); ax.axvline(2, color=C['g'], ls='--', lw=1.3); ax.axvline(-2, color=C['g'], ls='--', lw=1.3)
    ax.set_ylim(-8, 12); txt(ax, (7.3, 4.6), 'horizontal\nasymptote $y=2$', 'r', 10); txt(ax, (6.3, -5), 'vertical asymptotes\n$x=\\pm2$', 'g', 10)
    txt(ax, (-6.5, 8.5), r'$y=\dfrac{2x^2+1}{x^2-4}$', 'b', 12)
    return fig
