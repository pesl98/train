"""Small drawing helpers for the build-time figures (matplotlib, Agg)."""
import math
import numpy as np
import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt
from matplotlib.patches import Arc, Polygon, Wedge, FancyArrowPatch, Rectangle, Circle

C = {'b': '#1f6feb', 'r': '#d1242f', 'g': '#1a7f37', 'o': '#bc4c00', 'p': '#8250df', 'k': '#24292f', 'gr': '#8c959f', 'lg': '#d0d7de',
     'fb': '#ddf4ff', 'fr': '#ffebe9', 'fg': '#dafbe1', 'fy': '#fff8c5', 'fp': '#fbefff'}
plt.rcParams.update({'font.size': 11, 'mathtext.fontset': 'cm', 'axes.spines.top': False, 'axes.spines.right': False})


def canvas(w=6, h=4, xlim=None, ylim=None, n=1, axes=False, equal=True):
    """A clean drawing area without axes (geometry) - or n of them side by side."""
    fig, ax = plt.subplots(1, n, figsize=(w, h))
    for a in (np.atleast_1d(ax)):
        if equal: a.set_aspect('equal')
        if not axes: a.axis('off')
        if xlim: a.set_xlim(*xlim)
        if ylim: a.set_ylim(*ylim)
    return fig, ax


def graph(w=6, h=3.6, n=1, **kw):
    """Ordinary x-y axes through the origin style."""
    fig, ax = plt.subplots(1, n, figsize=(w, h), **kw)
    for a in np.atleast_1d(ax).flat:
        a.grid(True, alpha=.3); a.axhline(0, color=C['k'], lw=.8); a.axvline(0, color=C['k'], lw=.8)
    return fig, ax


def seg(ax, p, q, col='k', lw=2, ls='-', **kw):
    ax.plot([p[0], q[0]], [p[1], q[1]], color=C.get(col, col), lw=lw, ls=ls, solid_capstyle='round', **kw)


def arrow(ax, p, q, col='k', lw=1.6, style='-|>', ms=14):
    ax.add_patch(FancyArrowPatch(p, q, arrowstyle=style, mutation_scale=ms, color=C.get(col, col), lw=lw, shrinkA=0, shrinkB=0))


def dot(ax, p, col='k', s=40, **kw):
    ax.scatter([p[0]], [p[1]], s=s, color=C.get(col, col), zorder=5, **kw)


def txt(ax, p, s, col='k', size=12, ha='center', va='center', **kw):
    ax.text(p[0], p[1], s, color=C.get(col, col), fontsize=size, ha=ha, va=va, **kw)


def angle(ax, c, r, a0, a1, col='k', lw=1.5, label=None, lr=None, size=12, fill=None):
    """Arc of radius r about c from a0 to a1 (degrees), optional label at the middle."""
    if fill: ax.add_patch(Wedge(c, r, a0, a1, color=C.get(fill, fill), lw=0))
    ax.add_patch(Arc(c, 2 * r, 2 * r, theta1=a0, theta2=a1, color=C.get(col, col), lw=lw))
    if label:
        m = math.radians((a0 + a1) / 2); lr = lr or r * 1.45
        txt(ax, (c[0] + lr * math.cos(m), c[1] + lr * math.sin(m)), label, col, size)


def rightangle(ax, c, d1, d2, s=0.08, col='k'):
    """Small square at corner c; d1, d2 unit directions of the two legs."""
    p1 = (c[0] + s * d1[0], c[1] + s * d1[1]); p3 = (c[0] + s * d2[0], c[1] + s * d2[1])
    p2 = (p1[0] + s * d2[0], p1[1] + s * d2[1])
    ax.plot([p1[0], p2[0], p3[0]], [p1[1], p2[1], p3[1]], color=C.get(col, col), lw=1)


def poly(ax, pts, face='fb', edge='k', lw=1.5, alpha=1, **kw):
    ax.add_patch(Polygon(pts, closed=True, facecolor=C.get(face, face), edgecolor=C.get(edge, edge), lw=lw, alpha=alpha, **kw))


def circle(ax, c=(0, 0), r=1, col='gr', lw=1.5, **kw):
    ax.add_patch(Circle(c, r, fill=False, color=C.get(col, col), lw=lw, **kw))


def axes_cross(ax, L=1.3, labels=('x', 'y')):
    arrow(ax, (-L, 0), (L, 0), 'gr', 1); arrow(ax, (0, -L), (0, L), 'gr', 1)
    txt(ax, (L + .06, -.02), labels[0], 'gr', 11, ha='left'); txt(ax, (.02, L + .08), labels[1], 'gr', 11)


def P(deg, r=1): return (r * math.cos(math.radians(deg)), r * math.sin(math.radians(deg)))
