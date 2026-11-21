"""Figures for Unit 5 (first-order differential equations)."""
from figkit import *


def _field(ax, f, xr, yr, n=17, col='#8c959f'):
    xs, ys = np.linspace(*xr, n), np.linspace(*yr, n)
    dx = (xr[1] - xr[0]) / n * .38
    sx = (xr[1] - xr[0]); sy = (yr[1] - yr[0])
    for x in xs:
        for y in ys:
            s = f(x, y); vx, vy = 1 / sx, s / sy; L = math.hypot(vx, vy); vx, vy = vx / L * dx * 1, vy / L * dx * sy / sx
            ax.plot([x - vx * sx / sx, x + vx], [y - vy, y + vy], color=col, lw=1)


def _solve(f, x0, y0, x1, n=400):
    xs = np.linspace(x0, x1, n); ys = [y0]; h = xs[1] - xs[0]
    for i in range(n - 1):
        x, y = xs[i], ys[-1]
        k1 = f(x, y); k2 = f(x + h / 2, y + h / 2 * k1); k3 = f(x + h / 2, y + h / 2 * k2); k4 = f(x + h, y + h * k3)
        ys.append(y + h / 6 * (k1 + 2 * k2 + 2 * k3 + k4))
    return xs, np.array(ys)


# ------------------------------------------------------------------ week 13
def direction_field():
    fig, ax = plt.subplots(figsize=(6.4, 4.2))
    f = lambda x, y: x - y
    _field(ax, f, (-2, 3), (-2, 3))
    for y0, col in ((-1.5, C['b']), (0, C['g']), (1.5, C['o']), (2.8, C['p'])):
        xs, ys = _solve(f, -2, y0, 3); ax.plot(xs, ys, color=col, lw=2.2)
    ax.plot([-2, 3], [-3, 2], color=C['r'], ls='--', lw=1.4); txt(ax, (2.2, 1.55), '$y=x-1$', 'r', 11)
    ax.set_xlim(-2, 3); ax.set_ylim(-2, 3); ax.set_xlabel('$x$'); ax.set_ylabel('$y$'); ax.grid(True, alpha=.2)
    ax.set_title(r"$y'=x-y$: a short line with the right slope at every point", fontsize=10.5)
    return fig


def exp_family():
    fig, ax = graph(6.2, 3.6)
    ts = np.linspace(0, 3, 200)
    for C0, col in ((2, C['b']), (1, C['g']), (.5, C['o']), (-1, C['r'])):
        ax.plot(ts, C0 * np.exp(.6 * ts), color=col, lw=2, label='$C=%g$' % C0)
    ax.legend(fontsize=9.5, loc='upper left'); ax.set_xlabel('$t$'); ax.set_ylim(-7, 13)
    ax.set_title(r"$y'=0.6\,y$: one equation, a whole family $y=Ce^{0.6t}$", fontsize=10.5)
    return fig


def cooling():
    fig, ax = graph(6.4, 3.4)
    ts = np.linspace(0, 60, 300); Ta = 20
    for T0, col in ((90, C['r']), (60, C['o']), (5, C['b'])):
        ax.plot(ts, Ta + (T0 - Ta) * np.exp(-ts / 15), color=col, lw=2.2, label='start %d °C' % T0)
    ax.axhline(Ta, color=C['gr'], ls='--', lw=1.3); txt(ax, (40, 14), 'room temperature 20 °C', 'gr', 10)
    ax.set_xlabel('time (min)'); ax.set_ylabel('temperature (°C)'); ax.legend(fontsize=9.5); ax.set_ylim(0, 95)
    return fig


def logistic():
    fig, ax = plt.subplots(1, 2, figsize=(10, 3.4), gridspec_kw={'width_ratios': [1.6, 1]})
    A = ax[0]; ts = np.linspace(0, 12, 300); K, r = 100, .8
    for P0, col in ((2, C['b']), (20, C['g']), (140, C['o'])):
        A.plot(ts, K / (1 + (K / P0 - 1) * np.exp(-r * ts)), color=col, lw=2.2, label='$P_0=%d$' % P0)
    A.axhline(K, color=C['r'], ls='--', lw=1.3); A.text(.3, K + 4, 'carrying capacity K', color=C['r'], fontsize=10)
    A.set_xlabel('$t$'); A.set_ylabel('$P$'); A.legend(fontsize=9.5, loc='center right'); A.grid(True, alpha=.3); A.set_ylim(0, 150)
    B = ax[1]; Ps = np.linspace(-10, 130, 200); B.plot(Ps, r * Ps * (1 - Ps / K), color=C['b'], lw=2.2); B.axhline(0, color=C['k'], lw=.8)
    B.scatter([0, K], [0, 0], color=[C['r'], C['g']], zorder=5, s=40)
    for x0, d in ((50, 1), (115, -1), (-6, -1)): arrow(B, (x0, 1.2), (x0 + 10 * d, 1.2), 'o', 1.6, ms=12)
    B.text(-8, -12, 'unstable', color=C['r'], fontsize=9.5); B.text(92, -12, 'stable', color=C['g'], fontsize=9.5)
    B.set_xlabel('$P$'); B.set_ylabel("$P'=rP(1-P/K)$"); B.grid(True, alpha=.3)
    fig.tight_layout()
    return fig


# ------------------------------------------------------------------ week 14
def rc_circuit():
    fig, ax = canvas(6.4, 2.8, (0, 10), (0, 4.6))
    seg(ax, (1, 1), (1, 3.6)); seg(ax, (1, 3.6), (3.2, 3.6)); seg(ax, (4.8, 3.6), (7.5, 3.6)); seg(ax, (7.5, 3.6), (7.5, 2.6)); seg(ax, (7.5, 2.0), (7.5, 1)); seg(ax, (7.5, 1), (1, 1))
    ax.add_patch(Rectangle((3.2, 3.3), 1.6, .6, facecolor=C['fy'], edgecolor=C['k'], lw=1.5)); txt(ax, (4, 4.2), '$R$', 'k', 13)
    seg(ax, (6.9, 2.6), (8.1, 2.6), 'k', 3); seg(ax, (6.9, 2.0), (8.1, 2.0), 'k', 3); txt(ax, (8.5, 2.3), '$C$', 'k', 13, ha='left')
    ax.add_patch(Circle((1, 2.3), .45, facecolor='white', edgecolor=C['k'], lw=1.5, zorder=3)); txt(ax, (1, 2.3), r'$V_s$', 'k', 11, zorder=4)
    arrow(ax, (5.3, 3.6), (6.3, 3.6), 'r', 2); txt(ax, (5.8, 4.0), '$i$', 'r', 13)
    txt(ax, (9.2, 1.6), '$v$', 'b', 13); arrow(ax, (9.0, 1.2), (9.0, 3.3), 'b', 1.2, '<|-|>', 9)
    txt(ax, (4.6, .35), r'Kirchhoff: $V_s=Ri+v$,   capacitor: $i=C\,\dfrac{dv}{dt}$', 'k', 11)
    return fig


def rc_charge():
    fig, ax = graph(6.6, 3.5)
    ts = np.linspace(0, 6, 300); ax.plot(ts, 1 - np.exp(-ts), color=C['b'], lw=2.4, label='charging $1-e^{-t/\\tau}$'); ax.plot(ts, np.exp(-ts), color=C['r'], lw=2.4, label='discharging $e^{-t/\\tau}$')
    for k in range(1, 6): ax.axvline(k, color=C['lg'], lw=1)
    dot(ax, (1, 1 - math.exp(-1)), 'b'); txt(ax, (1.08, .58), '63 %', 'b', 10.5, ha='left'); dot(ax, (1, math.exp(-1)), 'r'); txt(ax, (1.08, .41), '37 %', 'r', 10.5, ha='left')
    txt(ax, (5, .9), '99.3 %\nafter 5τ', 'b', 9.5)
    ax.set_xticks(range(7)); ax.set_xticklabels(['0'] + ['%dτ' % k for k in range(1, 7)]); ax.set_ylabel('fraction of $V_s$'); ax.legend(fontsize=9.5, loc='center right'); ax.set_ylim(-.05, 1.1)
    return fig


def lowpass():
    fig, ax = plt.subplots(1, 2, figsize=(10, 3.2))
    ts = np.linspace(0, 4 * np.pi, 600)
    for A, wt in zip(ax, (.5, 3)):
        amp = 1 / math.sqrt(1 + wt * wt); ph = math.atan(wt)
        A.plot(ts, np.sin(ts), color=C['gr'], lw=1.5, label='input'); A.plot(ts, amp * np.sin(ts - ph), color=C['b'], lw=2.2, label='capacitor voltage')
        A.set_title(r'$\omega\tau=%g$: amplitude %.2f, lag %.0f°' % (wt, amp, math.degrees(ph)), fontsize=10.5); A.grid(True, alpha=.3); A.axhline(0, color=C['k'], lw=.8); A.set_ylim(-1.2, 1.2)
    ax[0].legend(fontsize=9, loc='lower left')
    fig.tight_layout()
    return fig


def tank():
    fig, ax = canvas(5, 3.3, (0, 10), (0, 6.6))
    poly(ax, [(2, 1), (8, 1), (8, 5), (2, 5)], 'fb', 'k', 2); ax.add_patch(Rectangle((2.03, 1.03), 5.94, 2.9, facecolor='#9ecbf0', edgecolor='none'))
    arrow(ax, (0.3, 5.6), (2.6, 4.4), 'g', 2); txt(ax, (.4, 6.1), 'in: 3 L/min, 2 g/L', 'g', 10, ha='left')
    arrow(ax, (8, 1.5), (9.8, 1.5), 'r', 2); txt(ax, (9.9, .7), 'out: 3 L/min', 'r', 10, ha='right')
    txt(ax, (5, 2.5), '100 L, salt $S(t)$ grams,\nwell stirred', 'k', 10.5)
    return fig


# ------------------------------------------------------------------ week 15
def euler_steps():
    fig, ax = graph(6.6, 3.8)
    ts = np.linspace(0, 2, 200); ax.plot(ts, np.exp(ts), color=C['k'], lw=2.4, label='exact $y=e^t$')
    h = .5; t, y = 0, 1; T, Y = [t], [y]
    for k in range(4):
        y2 = y + h * y; ax.plot([t, t + h], [y, y2], color=C['r'], lw=2); t, y = t + h, y2; T.append(t); Y.append(y)
    ax.scatter(T, Y, color=C['r'], zorder=5, s=30, label='Euler, $h=0.5$'); ax.plot([2, 2], [Y[-1], math.exp(2)], color=C['o'], lw=3)
    txt(ax, (2.04, (Y[-1] + math.exp(2)) / 2), 'error', 'o', 10.5, ha='left'); ax.legend(fontsize=9.5, loc='upper left'); ax.set_xlabel('$t$')
    ax.set_title(r"$y'=y$: each step follows the tangent, then the curve bends away", fontsize=10.5)
    return fig


def rk4_stages():
    fig, ax = graph(6.6, 3.8)
    f = lambda t, y: y
    ts = np.linspace(0, 1.1, 100); ax.plot(ts, np.exp(ts), color=C['k'], lw=2.4)
    t, y, h = 0, 1, 1.0
    k1 = f(t, y); k2 = f(t + h / 2, y + h / 2 * k1); k3 = f(t + h / 2, y + h / 2 * k2); k4 = f(t + h, y + h * k3)
    for (tt, yy, k, col, lab) in ((t, y, k1, C['r'], '$k_1$ at the start'), (t + h / 2, y + h / 2 * k1, k2, C['o'], '$k_2$ at the middle (via $k_1$)'), (t + h / 2, y + h / 2 * k2, k3, C['g'], '$k_3$ at the middle (via $k_2$)'), (t + h, y + h * k3, k4, C['p'], '$k_4$ at the end (via $k_3$)')):
        ax.plot([tt - .12, tt + .12], [yy - .12 * k, yy + .12 * k], color=col, lw=3, label=lab); ax.scatter([tt], [yy], color=col, zorder=5, s=25)
    y1 = y + h / 6 * (k1 + 2 * k2 + 2 * k3 + k4); ax.scatter([1], [y1], color=C['b'], s=60, zorder=6, marker='*', label='RK4 result (weighted average slope)')
    ax.legend(fontsize=8.5, loc='upper left'); ax.set_xlabel('$t$'); ax.set_xlim(-.15, 1.2)
    return fig


def instability():
    fig, ax = graph(6.6, 3.4)
    k = 10
    for h, col in ((.05, C['g']), (.15, C['o']), (.21, C['r'])):
        t, y, T, Y = 0, 1, [0], [1]
        for i in range(int(2 / h)): y = y + h * (-k * y); t += h; T.append(t); Y.append(y)
        ax.plot(T, Y, 'o-', ms=3, color=col, lw=1.4, label='$h=%g$ ($hk=%g$)' % (h, h * k))
    ts = np.linspace(0, 2, 200); ax.plot(ts, np.exp(-k * ts), color=C['k'], lw=2.2, label='exact')
    ax.set_ylim(-3, 3); ax.legend(fontsize=9, loc='lower left'); ax.set_xlabel('$t$')
    ax.set_title(r"Euler on $y'=-10y$: stable only if $h<2/10$", fontsize=10.5)
    return fig
