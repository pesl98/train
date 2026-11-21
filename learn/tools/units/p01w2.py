"""Physics strand · Part 2 (weeks 4-6) - kinematics: velocity, acceleration, constant acceleration, free fall, projectiles."""
import math
from nbkit import Book
import figs_p01 as F

B = Book('p01w2', 'Physics 2 — Kinematics', 'year1/p01w2-kinematics.ipynb')
S1, S2, S3, S4 = '1 Velocity and acceleration', '2 Constant acceleration', '3 Free fall', '4 Projectiles and relative motion'
g = 9.81

B.md(r'''
# Physics 2 — Kinematics: describing motion
*Physics strand, weeks 4–6 · about 9 hours, next to Unit 2 (derivatives)*

**Why.** Before asking *why* things move (forces — Physics 3), you need a precise language for *how* they move: where, how fast, speeding up or slowing down. That language is **kinematics**, and it is the first and best application of the derivative you are learning in Unit 2.

**What you will be able to do at the end**
1. Tell displacement from distance and velocity from speed; read velocity as the slope of a position graph and acceleration as the slope of a velocity graph.
2. Derive the four equations of constant acceleration from a velocity graph — and choose the right one for a problem.
3. Solve free-fall problems (dropped, thrown up, thrown from a height).
4. Split a projectile's motion into two independent motions and find its range, height and flight time; add velocities (river crossings).

**Maths used:** vectors and components (Physics 1), solving quadratics, and — from Unit 2 week 4 — the derivative as a slope. Areas of rectangles and triangles stand in for integrals until Unit 3.

Run the grey *SETUP* cell first. Use $g=9.81$ m/s² throughout.
''')

# =====================================================================================
B.md(r'''
---
# Part 1 — Position, velocity, acceleration

## 1.1 Displacement and average velocity

**Build.** Put a ruler (an $x$-axis) along the road and choose an origin. The **position** $x(t)$ is where the object is at time $t$ — a number with a sign (left of the origin is negative).

- **Displacement** between two moments: $\Delta x=x(t_2)-x(t_1)$ — "from where to where", with sign.
- **Distance travelled**: the total length of road covered — never negative.

A runner who does one 400 m lap of a track has run a distance of 400 m but has displacement 0.

**Average velocity** is displacement per time; **average speed** is distance per time:
$$\bar v=\frac{\Delta x}{\Delta t},\qquad\text{average speed}=\frac{\text{distance}}{\Delta t}.$$

## 1.2 Instantaneous velocity: the derivative

**Build.** A speedometer does not show an average over an hour; it shows the velocity *now*. Take the average over a shorter and shorter interval:
$$v(t)=\lim_{\Delta t\to0}\frac{x(t+\Delta t)-x(t)}{\Delta t}=\frac{dx}{dt}=x'(t).$$
That is exactly the definition of the derivative (Unit 2, week 4). **Graphically:** the velocity is the **slope of the tangent** to the $x$–$t$ graph.

In the same way, **acceleration** is the rate of change of velocity:
$$a(t)=\frac{dv}{dt}=\frac{d^2x}{dt^2}.$$
Units: m/s², "metres per second, per second" — how many m/s the velocity changes each second.
''')
B.fig('motion_graphs', F.motion_graphs, 'Each graph is the slope of the one before it. And going backwards: the area under v is the distance.')
B.md(r'''
**Worked example.** $x(t)=5t^2$ (metres, seconds) — a car pulling away.
- Average velocity from $t=1$ to $t=3$: $\frac{45-5}{2}=20$ m/s.
- Instantaneous: $v=\frac{d}{dt}5t^2=10t$, so $v(1)=10$, $v(3)=30$ m/s. (The average, 20, sits in between.)
- $a=\frac{d}{dt}10t=10$ m/s² — constant.

**Signs.** Positive $a$ does not always mean "speeding up". It means "velocity becoming more positive". A car moving left ($v<0$) and braking has $a>0$. **Speeding up** happens when $v$ and $a$ have the **same sign**.
''')
B.code(r'''
# Average velocity over a shrinking interval approaches the derivative: x(t) = 5 t^2 at t = 1
xf = lambda tt: 5 * tt**2
rows = []
for dt in (1, 0.1, 0.01, 0.001, 1e-5):
    rows.append([dt, (xf(1 + dt) - xf(1)) / dt])
table(['dt (s)', 'average velocity (m/s)'], rows)
print('derivative 10 t at t = 1:', 10)
''')
B.ask(r'''$x(t)=2t^3$ (m). What is the velocity (m/s) at $t=2$ s?''', 'num', 24,
      r'''$v=6t^2$, $v(2)=24$ m/s.''', r'''Differentiate $x(t)$.''', fmt='m/s')
B.ask(r'''A car moves in the negative $x$-direction ($v=-15$ m/s) and its acceleration is $+3$ m/s². Is it (a) speeding up or (b) slowing down?''', 'choice', 'b',
      r'''$v$ and $a$ have opposite signs: slowing down. After 5 s it stops; then it speeds up to the right.''',
      r'''Compare the signs of $v$ and $a$.''')

# =====================================================================================
B.md(r'''
---
# Part 2 — Constant acceleration

**Why.** A dropped stone, a car braking hard, a lift starting: over short times the acceleration is (nearly) constant. Then the motion follows from four simple equations — derived here, not memorised.

## 2.1 Derivation from the velocity graph

**Step 1 — velocity.** Constant $a$ means the $v$–$t$ graph has constant slope $a$: a straight line starting at $v_0$:
$$\boxed{\,v=v_0+a\,t\,}\tag{1}$$
''')
B.fig('vt_trapezoid', F.vt_trapezoid, 'The displacement is the area under the velocity graph: a rectangle plus a triangle.')
B.md(r'''
**Step 2 — displacement is area.** Over a tiny time $dt$ the object moves $v\,dt$ — a thin strip of height $v$ and width $dt$ under the graph. Adding all strips: displacement $=$ **area under the $v$–$t$ graph** (Unit 3 will call this an integral). Here the area is a rectangle ($v_0t$) plus a triangle ($\frac12\cdot t\cdot(v-v_0)=\frac12\cdot t\cdot at$):
$$\boxed{\,\Delta x=v_0t+\tfrac12at^2\,}\tag{2}$$
*Check with calculus:* $\frac{d}{dt}\left(v_0t+\frac12at^2\right)=v_0+at=v$ ✓.

**Step 3 — the same area as a trapezoid:** width $t$, average height $\frac{v_0+v}{2}$:
$$\boxed{\,\Delta x=\tfrac12(v_0+v)\,t\,}\tag{3}$$

**Step 4 — eliminate $t$.** From (1), $t=\frac{v-v_0}{a}$. Put it in (3):
$$\Delta x=\frac{(v+v_0)(v-v_0)}{2a}=\frac{v^2-v_0^2}{2a}\qquad\Longrightarrow\qquad\boxed{\,v^2=v_0^2+2a\,\Delta x\,}\tag{4}$$

## 2.2 Choosing the equation

Each equation leaves out one of the five quantities $\Delta x, v_0, v, a, t$:

| equation | does not contain |
|---|---|
| (1) $v=v_0+at$ | $\Delta x$ |
| (2) $\Delta x=v_0t+\frac12at^2$ | $v$ |
| (3) $\Delta x=\frac12(v_0+v)t$ | $a$ |
| (4) $v^2=v_0^2+2a\Delta x$ | $t$ |

**The method.** (i) Sketch; choose a positive direction. (ii) List the three known quantities with signs, and the one you want. (iii) Pick the equation that does not contain the fifth. (iv) Solve, then check units and the size of the answer.

**Worked example — emergency stop.** A car at $30$ m/s (108 km/h) brakes and stops in $45$ m. Deceleration?
Known: $v_0=30$, $v=0$, $\Delta x=45$. Wanted: $a$. Not involved: $t$ → equation (4): $0=900+2a\cdot45$, so $a=-10$ m/s² (about $g$ — good tyres on dry road). Time: from (1), $t=\frac{0-30}{-10}=3$ s.

**Worked example — reaction time.** The driver needs $0.7$ s to react; during that time the car still moves at 30 m/s: $21$ m. Total stopping distance $21+45=66$ m. Note: braking distance grows with $v^2$ — double the speed, **four times** the braking distance.

### Experiment 1 — stopping distance
**Predict first:** at 50 km/h the stopping distance is about 25 m. What is it at 100 km/h — 50 m, or more?
''')
B.code(r'''
def stopping(v_kmh=50, t_react=0.8, decel=7.0):
    v0 = v_kmh / 3.6
    d_react = v0 * t_react
    d_brake = v0**2 / (2 * decel)                     # equation (4) with v = 0
    ts = np.linspace(0, t_react + v0 / decel, 300)
    v = np.where(ts < t_react, v0, v0 - decel * (ts - t_react))
    fig, (a1, a2) = plt.subplots(1, 2, figsize=(10, 3.2))
    a1.plot(ts, v * 3.6); a1.axvline(t_react, color='r', ls=':'); a1.set_xlabel('t (s)'); a1.set_ylabel('speed (km/h)')
    a2.barh(['stopping'], [d_react], color='C1', label='reaction'); a2.barh(['stopping'], [d_brake], left=[d_react], color='C3', label='braking')
    a2.set_xlim(0, 160); a2.set_xlabel('metres'); a2.legend(); plt.tight_layout(); plt.show()
    print(f'reaction {d_react:.1f} m + braking {d_brake:.1f} m = {d_react + d_brake:.1f} m')

explore(stopping, v_kmh=(10, 150, 5, 50), t_react=(0.3, 2.0, 0.1, 0.8), decel=(2, 10, 0.5, 7.0))
''')
B.ask(r'''A cyclist accelerates from rest at 2 m/s². How far (m) has the cyclist gone after 5 s?''', 'num', 25,
      r'''$\Delta x=\frac12at^2=\frac12\cdot2\cdot25=25$ m.''',
      r'''$v_0=0$; which equation has $\Delta x$, $a$ and $t$ but not $v$?''', fmt='metres')
B.ask(r'''If braking distance is 20 m at 40 km/h, what is it (m) at 80 km/h, same deceleration?''', 'num', 80,
      r'''$\Delta x=\frac{v_0^2}{2|a|}\propto v_0^2$: twice the speed gives four times the distance, 80 m.''',
      r'''Equation (4) with $v=0$.''', fmt='metres')

# =====================================================================================
B.md(r'''
---
# Part 3 — Free fall

## 3.1 One acceleration for everything

**The fact (Galileo, checked to 1 part in $10^{14}$ today):** without air resistance, every object near the Earth's surface has the same downward acceleration
$$g\approx9.81\ \text{m/s}^2 .$$
A hammer and a feather fall together on the Moon (Apollo 15 did it). With $y$ pointing **up**, free fall is constant acceleration with $a=-g$, so the four equations apply.

**Worked example 1 — dropped from 20 m.** $v_0=0$, $\Delta y=-20$ m, $a=-9.81$. Equation (2): $-20=-\frac12\,9.81\,t^2$, $t=\sqrt{\frac{40}{9.81}}=2.02$ s. Impact speed from (4): $v^2=2\cdot9.81\cdot20$, $|v|=19.8$ m/s (71 km/h).

**Worked example 2 — thrown straight up at $15$ m/s.**
- Highest point: $v=0$. (4): $0=225-2\cdot9.81\cdot h$, $h=\frac{v_0^2}{2g}=11.5$ m.
- Time up: (1): $0=15-9.81\,t$, $t=\frac{v_0}{g}=1.53$ s. Time down is the same (**symmetry**), and it lands at 15 m/s.
- At the top $v=0$ but $a=-g$ still — the ball does not "stop accelerating". (The most common free-fall mistake.)

**Worked example 3 — thrown up at 10 m/s from a 15 m roof.** Equation (2) with $\Delta y=-15$: $-15=10t-4.905t^2$, i.e. $4.905t^2-10t-15=0$. Quadratic formula: $t=\frac{10\pm\sqrt{100+294.3}}{9.81}$; the positive root is $t=3.04$ s. (The negative root is "when it would have been thrown from the ground" — not our ball.)

### Experiment 2 — measure $g$ from data
A phone filmed a falling ball; the cell below holds the measured heights (with measuring noise). Fit a parabola $y=c_0+c_1t+c_2t^2$; comparing with $y=y_0+v_0t-\frac12gt^2$ gives $g=-2c_2$.
''')
B.code(r'''
rng = np.random.default_rng(3)
tt = np.linspace(0, 0.6, 13)
y_meas = 2.0 + 0.5 * tt - 0.5 * 9.81 * tt**2 + rng.normal(0, 0.004, tt.size)     # "measured" heights (m)
c2, c1, c0 = np.polyfit(tt, y_meas, 2)                                            # least-squares parabola
print(f'fit: y = {c0:.3f} + {c1:.3f} t + {c2:.3f} t^2     so  g = -2 c2 = {-2 * c2:.2f} m/s^2,  v0 = {c1:.2f} m/s')
ts = np.linspace(0, 0.6, 100)
plt.plot(tt, y_meas, 'o', label='measured'); plt.plot(ts, c0 + c1 * ts + c2 * ts**2, label='fitted parabola')
plt.xlabel('t (s)'); plt.ylabel('height (m)'); plt.legend(); plt.show()
''')

B.md(r'''
### Code it — free fall in small steps
Computers do not use the four equations — they take tiny time steps: in each step $dt$, *velocity changes by $a\,dt$, position by $v\,dt$*. This is how every simulator in the Lab works (and the subject of Unit 5). Complete the one missing line.
''')
B.code(r'''
def fall_time(h, dt=1e-4):
    """Drop from height h (m). Step until y < 0. Return the time (s)."""
    y, v, tt = h, 0.0, 0.0
    while y > 0:
        v = v - 9.81 * dt          # velocity changes by a*dt  (a = -g)
        y = ...                    # position changes by v*dt
        tt = tt + dt
    return tt


# ---------- tests: do not change ----------
for h in (20, 45, 1.25):
    try:
        got = fall_time(h); want = sqrt(2 * h / 9.81); ok = abs(got - want) < 1e-3
    except Exception as err:
        got, want, ok = err, sqrt(2 * h / 9.81), False
    print('✓' if ok else '✗', f'h = {h} m:  stepping gives {got},  formula sqrt(2h/g) = {want:.4f}')
''', ref=r'''
def fall_time(h, dt=1e-4):
    y, v, tt = h, 0.0, 0.0
    while y > 0:
        v = v - 9.81 * dt
        y = y + v * dt
        tt = tt + dt
    return tt
for h in (20, 45, 1.25): assert abs(fall_time(h) - sqrt(2 * h / 9.81)) < 1e-3
print('ok')
''')
B.ask(r'''A ball is thrown straight up at 20 m/s. How high (m) does it rise?''', 'num', 400 / (2 * g),
      r'''$h=\frac{v_0^2}{2g}=\frac{400}{19.62}=20.4$ m.''', r'''At the top $v=0$; use equation (4).''', fmt='metres')
B.ask(r'''At the very top of its flight, what is the ball's acceleration (m/s², with $y$ up)?''', 'num', -g,
      r'''$-9.81$ m/s² — gravity does not switch off when the velocity is momentarily zero.''',
      r'''What force acts on the ball at the top?''', fmt='m/s² (with sign)')

# =====================================================================================
B.md(r'''
---
# Part 4 — Projectiles and relative motion

## 4.1 Two independent motions
''')
B.fig('projectile_path', F.projectile_path, 'Horizontally: constant velocity. Vertically: free fall. Together: a parabola.')
B.md(r'''
**The key idea.** Gravity points straight down. It has **no horizontal component**, so it cannot change the horizontal velocity. The motion splits into two separate one-dimensional problems that share only the time $t$.

**Build.** Launch at speed $v_0$ and angle $\theta$ from the ground (origin at the launch point).

**Step 1 — split the initial velocity** (Physics 1): $v_{0x}=v_0\cos\theta$, $v_{0y}=v_0\sin\theta$.

**Step 2 — write each motion.**
$$\text{horizontal } (a_x=0):\quad x=v_0\cos\theta\;t\qquad\qquad\text{vertical } (a_y=-g):\quad y=v_0\sin\theta\;t-\tfrac12gt^2$$

**Step 3 — time of flight.** It lands when $y=0$: $t\left(v_0\sin\theta-\frac12gt\right)=0$, so (other than $t=0$)
$$t_f=\frac{2v_0\sin\theta}{g}.$$

**Step 4 — range.** Put $t_f$ into $x$, and use $2\sin\theta\cos\theta=\sin2\theta$ (Unit 1, week 2):
$$R=v_0\cos\theta\cdot\frac{2v_0\sin\theta}{g}=\frac{v_0^2\sin2\theta}{g}.$$

**Step 5 — maximum height.** Vertical velocity zero: $H=\frac{(v_0\sin\theta)^2}{2g}$.

**Reading the range formula.** $\sin2\theta$ is largest (1) at $2\theta=90^\circ$: **45° gives the longest range** (without air). And $\sin2\theta=\sin(180^\circ-2\theta)$, so complementary angles ($30^\circ$ and $60^\circ$) land at the same spot — the high one takes longer.

**Path shape.** Eliminate $t=\frac{x}{v_0\cos\theta}$: $y=x\tan\theta-\frac{g}{2v_0^2\cos^2\theta}x^2$ — a parabola.

**Worked example — rolled off a table.** A ball leaves a 0.80 m high table horizontally at 2.5 m/s. Vertical: dropped from 0.80 m, $t=\sqrt{2\cdot0.8/9.81}=0.404$ s. Horizontal: $x=2.5\cdot0.404=1.01$ m from the table.

### Experiment 3 — the 45° rule, and what air does to it
**Predict first:** with air drag switched on, is the best angle still 45°, more, or less? Use the lab's drag slider and try 35°, 45°, 55°.
''')
B.code(r'''
def throw(v0=25.0, ang=45):
    th = radians(ang)
    tf = 2 * v0 * sin(th) / g; ts = np.linspace(0, tf, 200)
    plt.figure(figsize=(8, 3.4))
    for a_, st in ((ang, '-'), (90 - ang, '--')):
        t2 = 2 * v0 * sin(radians(a_)) / g; tt = np.linspace(0, t2, 200)
        plt.plot(v0 * cos(radians(a_)) * tt, v0 * sin(radians(a_)) * tt - g / 2 * tt**2, st, label=f'{a_} deg')
    plt.xlim(0, 70); plt.ylim(0, 35); plt.xlabel('x (m)'); plt.ylabel('y (m)'); plt.legend(); plt.gca().set_aspect('equal'); plt.show()
    print(f'range {v0**2 * sin(2 * th) / g:.1f} m   height {(v0 * sin(th))**2 / (2 * g):.1f} m   flight time {tf:.2f} s')

g = 9.81
explore(throw, v0=(5, 25, 1, 25), ang=(5, 85, 5, 45))
''')
B.code(r'''
lab('physics', height=640, exp='proj', v0=25, ang=45, k=0.02)
''')
B.md(r'''
*(With drag the best angle drops below 45°: a long flat flight spends less time fighting the air.)*

## 4.2 Relative velocity

**Build.** Velocities add like vectors. A boat's velocity relative to the ground is its velocity relative to the water **plus** the water's velocity relative to the ground:
$$\vec v_{\text{boat, ground}}=\vec v_{\text{boat, water}}+\vec v_{\text{water, ground}} .$$

**Worked example.** A river 60 m wide flows east at 1.5 m/s. A boat heads straight north at 2 m/s relative to the water.
- Velocity relative to the ground: $(1.5,\ 2)$ m/s, speed $2.5$ m/s.
- Crossing time: only the northward part matters: $\frac{60}{2}=30$ s (the current does not delay it!).
- Drift downstream: $1.5\times30=45$ m.
- To land straight across it must aim upstream, at angle $\alpha$ with $2\sin\alpha=1.5$: $\alpha=48.6^\circ$ west of north; the crossing then takes longer ($\frac{60}{2\cos\alpha}=45.4$ s).
''')
B.ask(r'''A projectile is launched at 20 m/s at $45^\circ$. What is its range (m) on flat ground?''', 'num', 400 / g,
      r'''$R=\frac{v_0^2\sin90^\circ}{g}=\frac{400}{9.81}=40.8$ m.''', r'''$R=\frac{v_0^2\sin2\theta}{g}$.''', fmt='metres')
B.ask(r'''A plane flies north at 200 m/s relative to the air; the wind blows east at 50 m/s. What is its ground speed (m/s)?''', 'num', math.hypot(200, 50),
      r'''$\sqrt{200^2+50^2}=206$ m/s.''', r'''Add the two velocity vectors.''', fmt='m/s')

B.md(r'''
## Summary — everything on one page

- $v=\frac{dx}{dt}$ (slope of $x$–$t$), $a=\frac{dv}{dt}$ (slope of $v$–$t$); displacement $=$ area under $v$–$t$.
- Speeding up when $v$ and $a$ have the same sign.
- **Constant $a$:** $v=v_0+at$; $\Delta x=v_0t+\frac12at^2$; $\Delta x=\frac12(v_0+v)t$; $v^2=v_0^2+2a\Delta x$ — pick the one without the unwanted quantity.
- **Free fall:** $a=-g$ (y up). Max height $\frac{v_0^2}{2g}$, time up $\frac{v_0}{g}$, symmetric.
- **Projectile:** $x=v_0\cos\theta\,t$, $y=v_0\sin\theta\,t-\frac12gt^2$; $t_f=\frac{2v_0\sin\theta}{g}$, $R=\frac{v_0^2\sin2\theta}{g}$, $H=\frac{v_0^2\sin^2\theta}{2g}$.
- **Relative velocity:** add the vectors.
''')

# =====================================================================================
B.md(r'''
---
# Problems

Paper first, with a sketch and a chosen positive direction. First attempt counts. $g=9.81$ m/s².

### Velocity and acceleration
''')
B.problem(S1, r'A runner does one 400 m lap in 50 s and finishes at the starting line. Give (average speed, average velocity) in m/s.', 'tuple', (8, 0),
          [r'Speed uses distance; velocity uses displacement.'],
          r'''Average speed $\frac{400}{50}=8$ m/s; displacement 0, so average velocity 0. **(8, 0)**.''', fmt='a tuple `(speed, velocity)`')
B.problem(S1, r'$x(t)=3t^2-2t$ (m, s). What is the velocity at $t=2$ s?', 'num', 10,
          [r'$v=\frac{dx}{dt}$.'],
          r'''$v=6t-2$, $v(2)=$ **10 m/s**.''', fmt='m/s')
B.problem(S1, r'For the same $x(t)=3t^2-2t$, what is the average velocity between $t=1$ s and $t=3$ s?', 'num', 10,
          [r'$\bar v=\frac{x(3)-x(1)}{2}$.'],
          r'''$x(3)=21$, $x(1)=1$: $\bar v=\frac{20}{2}=$ **10 m/s** (equal to $v(2)$ here because $a$ is constant — the midpoint rule).''', fmt='m/s')
B.problem(S1, r'$x(t)=4\sin(2t)$ (m). What is the acceleration (m/s²) at $t=\pi/4$ s?', 'num', -16,
          [r'Differentiate twice (chain rule).', r'$a=-16\sin(2t)$.'],
          r'''$v=8\cos2t$, $a=-16\sin2t$. At $t=\frac\pi4$: $\sin\frac\pi2=1$, so $a=$ **−16 m/s²**. (Note $a=-4x$: this is simple harmonic motion — Unit 9.)''', fmt='m/s²')
B.md(r'''
### Constant acceleration
''')
B.problem(S2, r'A car accelerates from rest at 3.0 m/s² for 6.0 s. How far does it travel?', 'num', 54,
          [r'$\Delta x=v_0t+\frac12at^2$ with $v_0=0$.'],
          r'''$\frac12\cdot3\cdot36=$ **54 m**.''', fmt='metres')
B.problem(S2, r'A train at 25 m/s brakes at 0.50 m/s². How far does it travel before stopping?', 'num', 625,
          [r'No time involved: equation (4) with $v=0$.'],
          r'''$0=625-2\cdot0.5\cdot\Delta x$, $\Delta x=$ **625 m** — why trains need signals far ahead.''', fmt='metres')
B.problem(S2, r'A driver at 20 m/s has a reaction time of 0.80 s and then brakes at 8.0 m/s². Total stopping distance?', 'num', 16 + 25,
          [r'Reaction: constant speed. Braking: equation (4).'],
          r'''Reaction $20\cdot0.8=16$ m. Braking $\frac{400}{16}=25$ m. Total **41 m**.''', fmt='metres')
B.problem(S2, r'An object speeds up from 5.0 m/s to 15 m/s over 40 m. What is its (constant) acceleration?', 'num', 2.5,
          [r'$v^2=v_0^2+2a\Delta x$.'],
          r'''$225=25+80a$, $a=$ **2.5 m/s²**.''', fmt='m/s²')
B.md(r'''
### Free fall
''')
B.problem(S3, r'A stone is dropped from a 45 m high bridge. How long does it take to reach the water?', 'num', math.sqrt(90 / g),
          [r'$45=\frac12gt^2$.'],
          r'''$t=\sqrt{\frac{2\cdot45}{9.81}}=$ **3.03 s**.''', fmt='seconds')
B.problem(S3, r'With what speed does that stone hit the water?', 'num', math.sqrt(2 * g * 45),
          [r'$v^2=2gh$ — or $v=gt$.'],
          r'''$v=\sqrt{2\cdot9.81\cdot45}=$ **29.7 m/s** (check: $9.81\times3.03=29.7$ ✓).''', fmt='m/s')
B.problem(S3, r'A ball is thrown straight up at 12 m/s from the edge of a 20 m high roof and falls to the ground beside the building. How long is it in the air?', 'num', (12 + math.sqrt(144 + 2 * g * 20)) / g,
          [r'$y$ up, origin at the roof: $-20=12t-\frac12gt^2$.', r'$4.905t^2-12t-20=0$; take the positive root.'],
          r'''$t=\frac{12+\sqrt{144+392.4}}{9.81}=\frac{12+23.16}{9.81}=$ **3.58 s**.''', fmt='seconds')
B.problem(S3, r'On the Moon ($g=1.62$ m/s²) an astronaut throws a ball up at 5 m/s. How high (m) does it go?', 'num', 25 / (2 * 1.62),
          [r'$h=\frac{v_0^2}{2g}$ with the Moon value of $g$.'],
          r'''$\frac{25}{3.24}=$ **7.72 m** — six times higher than on Earth.''', fmt='metres')
B.md(r'''
### Projectiles and relative motion
''')
B.problem(S4, r'A ball is kicked at 20 m/s, $30^\circ$ above flat ground. What is its range?', 'num', 400 * math.sin(math.radians(60)) / g,
          [r'$R=\frac{v_0^2\sin2\theta}{g}$.'],
          r'''$\frac{400\sin60^\circ}{9.81}=\frac{346.4}{9.81}=$ **35.3 m**.''', fmt='metres')
B.problem(S4, r'What maximum height does that ball reach?', 'num', 100 / (2 * g),
          [r'Only the vertical component counts: $v_{0y}=10$ m/s.'],
          r'''$H=\frac{(20\sin30^\circ)^2}{2g}=\frac{100}{19.62}=$ **5.10 m**.''', fmt='metres')
B.problem(S4, r'A ball rolls off a 1.2 m high table at 3.0 m/s (horizontally). How far from the table does it land?', 'num', 3 * math.sqrt(2.4 / g),
          [r'Fall time from the vertical motion only.', r'$t=\sqrt{2h/g}$, then $x=v_xt$.'],
          r'''$t=\sqrt{2.4/9.81}=0.495$ s; $x=3\cdot0.495=$ **1.48 m**.''', fmt='metres')
B.problem(S4, r'Which other launch angle (degrees) gives the same range as $25^\circ$, at the same speed?', 'num', 65,
          [r'$\sin2\theta=\sin(180^\circ-2\theta)$.'],
          r'''$90^\circ-25^\circ=$ **65°**.''', fmt='degrees')
B.problem(S4, r'A boat heads straight across an 80 m wide river at 4 m/s relative to the water; the current is 3 m/s. How far downstream (m) does it land?', 'num', 60,
          [r'Crossing time uses only the across-component.'],
          r'''$t=\frac{80}{4}=20$ s; drift $3\cdot20=$ **60 m**. (Ground speed 5 m/s, path length 100 m.)''', fmt='metres')
B.code(r'''
# scratch cell
''')

B.md(r'''
---
# Finish

### 1 · Report
''')
B.code(r'''
report()
''')
B.md(r'''
### 2 · Teach-back (20 minutes, from memory)
1. Define velocity and acceleration as derivatives and explain "slope" and "area" on the graphs.
2. Derive all four constant-acceleration equations from the $v$–$t$ graph.
3. A ball is thrown up: describe $v$ and $a$ at the start, at the top and on landing.
4. Derive the range formula and explain why 45° is best.
5. Why does the current not change the crossing time of a boat aimed straight across?

*Your answers:*

&nbsp;

### 3 · What comes next
**Physics 3 — Newton's laws and energy:** *why* the acceleration is what it is. Force causes acceleration, $\vec F=m\vec a$ — and energy gives a second, often much quicker, way to the same answers.
''')

if __name__ == '__main__':
    B.write()
