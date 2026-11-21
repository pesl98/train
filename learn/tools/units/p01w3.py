"""Physics strand · Part 3 (weeks 7-10) - Newton's laws, friction, inclines, work, energy, power."""
import math
from nbkit import Book
import figs_p01 as F

B = Book('p01w3', "Physics 3 — Newton's laws and energy", 'year1/p01w3-newton-energy.ipynb')
S1, S2, S3, S4 = "1 Newton's laws", '2 Friction, slopes and pulleys', '3 Work and kinetic energy', '4 Potential energy, conservation, power'
g = 9.81
rad = math.radians

B.md(r'''
# Physics 3 — Newton's laws and energy
*Physics strand, weeks 7–10 · about 12 hours, next to the end of Unit 2 and Unit 3 (integrals)*

**Why.** Physics 2 described motion. Now the cause: **force**. Three laws, written down by Newton in 1687, predict the motion of crates, cars, lifts and planets. Then a second point of view — **energy** — which often reaches the same answer in one line, and which you will meet again in every circuit (Physics 4) and every oscillator (Unit 9).

**What you will be able to do at the end**
1. State Newton's three laws and draw a correct free-body diagram.
2. Solve problems with weight, normal force, tension and friction — on the flat, on slopes and over pulleys.
3. Compute work (constant and variable force, as a dot product and as an integral) and derive the work–energy theorem.
4. Use potential energy and conservation of energy, including losses to friction, and compute power.

**Maths used:** vectors and the dot product (Physics 1), the constant-acceleration equations (Physics 2), derivatives (Unit 2) and — in Part 3 — the integral as an area (Unit 3, week 8).

Run the grey *SETUP* cell first. $g=9.81$ m/s².
''')

# =====================================================================================
B.md(r'''
---
# Part 1 — Newton's three laws

## 1.1 Force

A **force** is a push or a pull — a vector, measured in newtons (N). One newton gives 1 kg an acceleration of 1 m/s². (Holding an apple up takes about 1 N.)

## 1.2 The three laws

**First law (inertia).** If the total force on an object is zero, its velocity does not change: at rest stays at rest, moving keeps moving in a straight line at constant speed. *Moving does not need a force — changing the motion does.* (A hockey puck on ice glides on; it stops on carpet because friction is a force.)

**Second law.** The total (net) force equals mass times acceleration:
$$\boxed{\,\vec F_{\text{net}}=\sum\vec F=m\,\vec a\,}$$
It is a vector equation — one equation per component: $\sum F_x=ma_x$, $\sum F_y=ma_y$. Mass measures how hard it is to change an object's motion.

**Third law.** If A pushes on B, then B pushes on A with a force of the same size in the opposite direction. **The two forces act on different objects**, so they never cancel each other in one free-body diagram. (You push the wall; the wall pushes you — that is how you can push off.)

## 1.3 The forces you will meet

| force | direction | size |
|---|---|---|
| weight $W$ | straight down | $mg$ |
| normal force $N$ | perpendicular to the surface, pushing out | whatever is needed to stop you sinking in — *find it from Newton's law* |
| tension $T$ | along the rope, pulling | same all along a light rope over a smooth pulley |
| friction $f$ | along the surface, against sliding | kinetic: $f=\mu_kN$; static: up to $\mu_sN$ |

## 1.4 The method: free-body diagram
''')
B.fig('free_body', F.free_body, 'Replace the object by a dot. Draw every force acting ON it — nothing else.')
B.md(r'''
1. **Isolate** one object; draw it as a dot.
2. **Draw every force acting on it** — weight, and one force for each thing touching it (surface, rope, hand). Not the forces *it* exerts on others; no "force of motion".
3. **Choose axes** — one along the acceleration if you know its direction.
4. **Write $\sum F=ma$ for each axis.** Solve.
5. **Check** signs, units and extreme cases.

**Worked example — the lift.** A 70 kg person stands on bathroom scales in a lift accelerating **upwards** at $2.0$ m/s². What do the scales read?
1–2. Forces on the person: weight $mg$ down, normal force $N$ (from the scales) up.
3. Axis: up positive.
4. $N-mg=ma\ \Rightarrow\ N=m(g+a)=70(9.81+2.0)=827$ N.
5. The scales show $N$ (third law: you push on the scales as hard as they push on you): 827 N, as if you had a mass of 84 kg. Accelerating **down** at 2.0 m/s²: $N=m(g-a)=547$ N. In free fall ($a=g$ down): $N=0$ — "weightless".
''')
B.ask(r'''What net force (N) gives a 1200 kg car an acceleration of 2.5 m/s²?''', 'num', 3000,
      r'''$F=ma=1200\cdot2.5=3000$ N.''', r'''$F_{\text{net}}=ma$.''', fmt='newtons')
B.ask(r'''A book lies on a table. Earth pulls the book down (its weight). What is the third-law partner of that force? (a) the table pushing the book up (b) the book pulling the Earth up (c) the book pushing the table down''', 'choice', 'b',
      r'''Third-law pairs are the *same kind* of force between the *same two objects*: Earth pulls book (gravity) ⟷ book pulls Earth (gravity). The table's push on the book also equals $mg$ here, but for a different reason (the book is not accelerating — the second law).''',
      r'''A third-law pair involves the same two objects, swapped.''')

# =====================================================================================
B.md(r'''
---
# Part 2 — Friction, slopes and pulleys

## 2.1 Friction

**The empirical law.** Press two surfaces together with normal force $N$.
- **Static friction** (no sliding): adjusts itself to whatever is needed to prevent sliding, **up to** a maximum $f_s\le\mu_sN$.
- **Kinetic friction** (sliding): $f_k=\mu_kN$, opposite to the sliding velocity; usually $\mu_k<\mu_s$ (it is easier to keep a crate moving than to start it).

Typical values: rubber on dry asphalt $\mu\approx0.7$–$1$; steel on ice $\approx0.03$; wood on wood $\approx0.3$.

**Worked example.** A 20 kg crate is pushed with 100 N across a floor with $\mu_k=0.30$.
Vertical: $N-mg=0\Rightarrow N=196.2$ N. Friction: $f=0.30\cdot196.2=58.9$ N. Horizontal: $100-58.9=20a\Rightarrow a=2.06$ m/s².

## 2.2 Slopes
''')
B.fig('incline_resolve', F.incline_resolve, 'On a slope: tilt the axes. Weight splits into mg sinθ along and mg cosθ into the slope.')
B.md(r'''
**Build.** Axes along the slope (down positive) and perpendicular to it.
- Perpendicular: no acceleration, so $N=mg\cos\theta$.
- Along, no friction: $mg\sin\theta=ma\Rightarrow a=g\sin\theta$ — independent of the mass.
- Along, sliding down with kinetic friction: $ma=mg\sin\theta-\mu_kmg\cos\theta\Rightarrow a=g(\sin\theta-\mu_k\cos\theta)$.

**When does a block start to slide?** Static friction can hold it as long as $mg\sin\theta\le\mu_smg\cos\theta$, i.e. $\tan\theta\le\mu_s$. Tilt a board slowly until the block slips: **$\mu_s=\tan\theta_{\text{slip}}$** — a one-line experiment to measure friction.

## 2.3 Two connected masses: the Atwood machine
''')
B.fig('atwood', F.atwood, 'A light rope over a smooth pulley: the same tension T on both sides, the same size of acceleration a.')
B.md(r'''
**Build.** Masses $m_2>m_1$. $m_2$ goes down, $m_1$ up, both with acceleration $a$. One free-body diagram **per mass**, each with its own positive direction (the direction it moves):
$$m_1:\quad T-m_1g=m_1a\qquad\qquad m_2:\quad m_2g-T=m_2a$$
**Add** the two equations — $T$ cancels:
$$(m_2-m_1)g=(m_1+m_2)a\quad\Rightarrow\quad\boxed{\,a=\frac{m_2-m_1}{m_1+m_2}\,g\,}$$
Then $T=m_1(g+a)=\dfrac{2m_1m_2}{m_1+m_2}\,g$.

**Checks.** Equal masses: $a=0$ ✓. $m_1=0$: $a=g$, free fall, $T=0$ ✓. $T$ lies between $m_1g$ and $m_2g$ ✓ (it must lift $m_1$ but cannot fully hold $m_2$).

**Why it matters.** Atwood (1784) used this to *slow gravity down* and measure $g$ with a clock. Lifts use a counterweight for the same reason: the motor only supplies the difference.

### Experiment 1 — the sliding block
**Predict first:** $\mu_s=0.5$. At what angle does the block start to slide? Once it slides with $\mu_k=0.4$, what happens to $a$ if you double the mass?
''')
B.code(r'''
def slope(angle=20, mu_s=0.5, mu_k=0.4, m=2.0):
    th = radians(angle)
    along, Nf = m * 9.81 * sin(th), m * 9.81 * cos(th)
    if along <= mu_s * Nf:
        print(f'stays put: static friction supplies {along:.2f} N (max {mu_s * Nf:.2f} N)'); a = 0.0
    else:
        a = 9.81 * (sin(th) - mu_k * cos(th)); print(f'slides: a = g(sin - mu_k cos) = {a:.2f} m/s^2')
    print(f'slip angle = atan(mu_s) = {degrees(atan(mu_s)):.1f} deg')
    angs = np.linspace(0, 80, 400); r = np.radians(angs)
    acc = np.where(np.tan(r) > mu_s, 9.81 * (np.sin(r) - mu_k * np.cos(r)), 0)
    plt.figure(figsize=(7, 3)); plt.plot(angs, acc); plt.plot([angle], [a], 'ro'); plt.xlabel('slope angle (deg)'); plt.ylabel('a (m/s^2)'); plt.show()

explore(slope, angle=(0, 80, 1, 20), mu_s=(0, 1.2, 0.05, 0.5), mu_k=(0, 1.0, 0.05, 0.4), m=(0.5, 10, 0.5, 2.0))
''')
B.md(r'''
*Notice the jump at the slip angle: static friction lets go, the smaller kinetic friction takes over, and the block lurches — that is why things "suddenly" start to slide (and why ABS brakes keep tyres just below slipping).*

### Code it — falling with air drag
Air drag grows with speed: $F_d=kv^2$. For a falling object (down positive): $ma=mg-kv^2$. At first $a\approx g$; as $v$ grows, drag catches up with weight and the acceleration fades — **terminal velocity**, where $mg=kv_t^2$, $v_t=\sqrt{mg/k}$. Complete the line for the acceleration and watch the simulation find $v_t$.
''')
B.code(r'''
def terminal(m, k, dt=1e-3, T=60):
    v, vs = 0.0, []
    for step in range(int(T / dt)):
        a = ...                    # Newton: (weight - drag) / mass
        v = v + a * dt
        vs.append(v)
    return np.array(vs)


# ---------- tests: do not change ----------
for m, k in ((80, 0.25), (0.005, 0.0004)):        # a skydiver, a hailstone
    try:
        vs = terminal(m, k); want = sqrt(m * 9.81 / k); ok = abs(vs[-1] - want) < 0.01 * want
        print('✓' if ok else '✗', f'm = {m} kg, k = {k}:  final speed {vs[-1]:.2f} m/s,  sqrt(mg/k) = {want:.2f} m/s')
    except Exception as err:
        print('✗', err)
try:
    vs = terminal(80, 0.25); plt.plot(np.arange(len(vs)) * 1e-3, vs); plt.xlabel('t (s)'); plt.ylabel('v (m/s)'); plt.title('skydiver'); plt.show()
except Exception:
    pass
''', ref=r'''
def terminal(m, k, dt=1e-3, T=60):
    v, vs = 0.0, []
    for step in range(int(T / dt)):
        a = (m * 9.81 - k * v**2) / m
        v = v + a * dt
        vs.append(v)
    return np.array(vs)
for m, k in ((80, 0.25), (0.005, 0.0004)):
    assert abs(terminal(m, k)[-1] - sqrt(m * 9.81 / k)) < 0.01 * sqrt(m * 9.81 / k)
print('ok')
''')
B.ask(r'''A block slides down a frictionless $30^\circ$ slope. What is its acceleration (m/s²)?''', 'num', g / 2,
      r'''$a=g\sin30^\circ=4.905$ m/s².''', r'''$a=g\sin\theta$.''', fmt='m/s²')
B.ask(r'''A coin on a book starts to slide when the book is tilted to $17^\circ$. What is $\mu_s$?''', 'num', math.tan(rad(17)),
      r'''$\mu_s=\tan17^\circ=0.306$.''', r'''At the slip angle $\tan\theta=\mu_s$.''')

# =====================================================================================
B.md(r'''
---
# Part 3 — Work and kinetic energy

## 3.1 Work by a constant force

**Build.** A force $\vec F$ acts while the object moves through a displacement $\vec d$. Only the part of the force **along** the motion helps or hinders it. Define the **work**
$$W=\vec F\cdot\vec d=F\,d\cos\varphi\qquad(\text{joules, }1\ \text{J}=1\ \text{N m})$$
with $\varphi$ the angle between force and displacement — the dot product of Physics 1.
- $\varphi=0$: $W=Fd$ (full help). $\varphi=90^\circ$: $W=0$ — the normal force on a flat floor, or a satellite's gravity on a circular orbit, does **no work**. $\varphi=180^\circ$: $W=-Fd$ — friction always does negative work.

## 3.2 The work–energy theorem

**Build (constant force, along a line).** Start from Newton and from equation (4) of Physics 2:
$$F_{\text{net}}=ma,\qquad v^2=v_0^2+2a\,d .$$
**Step 1.** Multiply the second by $\frac m2$: $\frac12mv^2=\frac12mv_0^2+ma\,d$.
**Step 2.** Replace $ma$ by $F_{\text{net}}$:
$$\boxed{\,W_{\text{net}}=F_{\text{net}}\,d=\tfrac12mv^2-\tfrac12mv_0^2\,}$$
The quantity $K=\frac12mv^2$ is the **kinetic energy**. *The net work done on an object equals the change of its kinetic energy.*

**Build (any force — needs Unit 3).** If $F$ varies with position, cut the path into small pieces $dx$; on each piece the force is nearly constant and does work $F\,dx$. Adding the pieces gives an integral:
$$W=\int_{x_0}^{x_1}F(x)\,dx\qquad(\text{the area under the }F\text{–}x\text{ graph}).$$
And the theorem still holds. *Proof:* $F=ma=m\frac{dv}{dt}$. Along the motion $dx=v\,dt$, so $F\,dx=m\frac{dv}{dt}v\,dt=mv\,dv$. Hence $\int F\,dx=\int_{v_0}^{v}mv\,dv=\frac12mv^2-\frac12mv_0^2$ ∎
''')
B.fig('work_area', F.work_area, 'Work is the area under the force–position graph. For a spring the area is a triangle: ½kx².')
B.md(r'''
**Worked example — the spring.** Hooke's law: stretching a spring by $x$ takes a force $F=kx$. Work to stretch it from 0 to $x$:
$$W=\int_0^x kx'\,dx'=\tfrac12kx^2$$
— the area of the triangle in the figure.

**Worked example — braking.** A 1000 kg car at 20 m/s locks its wheels ($\mu_k=0.8$). Friction does work $-\mu_kmg\,d$, which must remove all of $K=\frac12mv^2=200$ kJ:
$$\mu_kmg\,d=\tfrac12mv^2\ \Rightarrow\ d=\frac{v^2}{2\mu_kg}=\frac{400}{15.7}=25.5\text{ m}.$$
The mass cancels; no time or acceleration needed. Energy is often the shortcut.
''')
B.code(r'''
# Work as an area: numerically integrate a varying force, compare with the change in kinetic energy.
m = 2.0
Fx = lambda xx: 6 * xx - xx**2                          # a force (N) that varies with position (m)
W = nint(Fx, 0, 4)                                      # area under F from x = 0 to 4 m
print(f'work = {W:.4f} J   (exact: 3*16 - 64/3 = {48 - 64 / 3:.4f} J)')
print(f'starting from rest, final speed = sqrt(2W/m) = {sqrt(2 * W / m):.3f} m/s')
''')
B.ask(r'''A 50 N force pulls a sled 20 m along flat snow; the rope makes $30^\circ$ with the ground. How much work (J) does the force do?''', 'num', 50 * 20 * math.cos(rad(30)),
      r'''$W=Fd\cos\varphi=50\cdot20\cdot\cos30^\circ=866$ J.''', r'''Only the component along the motion counts.''', fmt='joules')
B.ask(r'''How much work (J) does it take to stretch a spring with $k=500$ N/m by 4.0 cm?''', 'num', 0.5 * 500 * 0.04 ** 2,
      r'''$\frac12kx^2=\frac12\cdot500\cdot0.04^2=0.40$ J. (Convert cm to m first!)''', r'''$\frac12kx^2$ with $x$ in metres.''', fmt='joules')

# =====================================================================================
B.md(r'''
---
# Part 4 — Potential energy, conservation, power

## 4.1 Potential energy

**Build.** Lift a mass $m$ by a height $h$, slowly. Gravity does work $-mgh$ on it (force down, motion up). Crucially, **that work depends only on the change in height, not on the path** — go up a ramp or a staircase, only the vertical components count ($\vec F\cdot\vec d$ with $\vec F$ vertical). A force with that property is called **conservative**, and we can store its work as a **potential energy**:
$$U_{\text{grav}}=mgh,\qquad U_{\text{spring}}=\tfrac12kx^2 .$$
(The spring's work also depends only on the start and end stretch.) Friction is *not* conservative: a longer path means more work lost.

## 4.2 Conservation of mechanical energy

**Build.** Split the net work into the conservative part ($=-\Delta U$, by definition of $U$) and the rest ($W_{\text{other}}$: friction, your hand, a motor). The work–energy theorem $W_{\text{net}}=\Delta K$ becomes
$$-\Delta U+W_{\text{other}}=\Delta K\qquad\Longleftrightarrow\qquad\boxed{\,K_1+U_1+W_{\text{other}}=K_2+U_2\,}$$
If only gravity and springs do work ($W_{\text{other}}=0$): **$K+U$ stays constant.** With friction, $W_{\text{other}}=-f\,d$: the "lost" mechanical energy has become heat.
''')
B.fig('energy_bars', F.energy_bars, 'A falling ball: potential energy turns into kinetic energy; the total stays the same.')
B.md(r'''
**Worked example 1 — roller coaster.** From rest at 30 m height, frictionless, to the bottom: $mgh=\frac12mv^2\Rightarrow v=\sqrt{2gh}=24.3$ m/s — the same as free fall from 30 m, *whatever the shape of the track*. (Forces along a curved track would be a nightmare; energy does not care.)

**Worked example 2 — spring launcher.** A spring ($k=400$ N/m) compressed 0.10 m launches a 0.050 kg ball straight up. $\frac12kx^2=2.0$ J $=mgh\Rightarrow h=\frac{2.0}{0.050\cdot9.81}=4.1$ m.

**Worked example 3 — with friction.** A 2 kg block slides from rest down a 5 m long ramp that drops 3 m, with friction force 4 N. $mgh=58.9$ J; friction removes $4\cdot5=20$ J; at the bottom $K=38.9$ J, $v=\sqrt{2\cdot38.9/2}=6.2$ m/s.

## 4.3 Power

**Power** is the rate of doing work: $P=\dfrac{dW}{dt}$, in watts (J/s). For a force moving at velocity $v$: $dW=F\,dx$, so
$$P=\frac{F\,dx}{dt}=F\,v\qquad(\vec F\cdot\vec v\text{ in general}).$$
**Worked example.** A 1200 kg car climbs a road rising 1 m per 10 m (slope $\sin\theta=0.1$) at a steady 25 m/s. The engine must supply the force $mg\sin\theta=1177$ N along the road (ignoring air and rolling resistance): $P=1177\cdot25=29.4$ kW.

### Experiment 2 — energy sloshing in a spring
The Physics Lab opens on a mass on a spring with no damping and no drive. **Predict first:** when is the kinetic energy largest? What does the "total" line do? Then switch on damping: where does the energy go?
''')
B.code(r'''
lab('physics', height=640, exp='osc', F0=0, c=0, x0=1)
''')
B.ask(r'''A ball is released from rest 5.0 m above the ground (no air resistance). With what speed (m/s) does it land?''', 'num', math.sqrt(2 * g * 5),
      r'''$v=\sqrt{2gh}=\sqrt{98.1}=9.90$ m/s.''', r'''$mgh=\frac12mv^2$.''', fmt='m/s')
B.ask(r'''A 60 kg person climbs 3.0 m of stairs in 4.0 s. What is their average power output (W)?''', 'num', 60 * g * 3 / 4,
      r'''$P=\frac{mgh}{t}=\frac{60\cdot9.81\cdot3}{4}=441$ W.''', r'''Work $=mgh$; power $=$ work / time.''', fmt='watts')

B.md(r'''
## Summary — everything on one page

- **Newton:** (1) no net force → constant velocity; (2) $\sum\vec F=m\vec a$, per component; (3) equal and opposite forces on *different* objects.
- **Free-body diagram:** one object, every force on it; choose axes; $\sum F=ma$ per axis.
- **Forces:** $W=mg$; $N$ from Newton; friction $f_k=\mu_kN$, $f_s\le\mu_sN$; slope: $mg\sin\theta$ along, $N=mg\cos\theta$; slips when $\tan\theta>\mu_s$.
- **Atwood:** $a=\frac{m_2-m_1}{m_1+m_2}g$, $T=\frac{2m_1m_2}{m_1+m_2}g$. **Terminal velocity:** $v_t=\sqrt{mg/k}$.
- **Work:** $W=\vec F\cdot\vec d$; $W=\int F\,dx$; spring $\frac12kx^2$. **Work–energy:** $W_{\text{net}}=\Delta(\frac12mv^2)$.
- **Energy:** $K_1+U_1+W_{\text{other}}=K_2+U_2$ with $U=mgh$, $\frac12kx^2$. **Power:** $P=\frac{dW}{dt}=Fv$.
''')

# =====================================================================================
B.md(r'''
---
# Problems

Paper first, always with a free-body diagram. First attempt counts. $g=9.81$ m/s².

### Newton's laws
''')
B.problem(S1, r'A 70 kg person stands on scales in a lift that is moving **downwards and slowing down** at 2.0 m/s². What do the scales read (N)?', 'num', 70 * (g + 2),
          [r'Moving down and slowing down: which way does the acceleration point?', r'The acceleration points up: $N-mg=+ma$.'],
          r'''Slowing a downward motion needs an **upward** acceleration. Up positive: $N-mg=ma$, $N=70(9.81+2.0)=$ **827 N**. (You feel heavy at the bottom floor.)''', fmt='newtons')
B.problem(S1, r'A 5.0 kg box is pulled across a frictionless floor by a horizontal 20 N force. How far does it move from rest in 3.0 s?', 'num', 0.5 * 4 * 9,
          [r'Newton gives $a$; Physics 2 gives the distance.'],
          r'''$a=\frac{20}{5}=4$ m/s²; $\Delta x=\frac12\cdot4\cdot9=$ **18 m**.''', fmt='metres')
B.problem(S1, r'A lamp of mass 2.0 kg hangs from two cords, each making $30^\circ$ with the horizontal ceiling. What is the tension (N) in each cord?', 'num', 2 * g / (2 * math.sin(rad(30))),
          [r'At rest: the vertical components of the two tensions hold the weight.', r'$2T\sin30^\circ=mg$.'],
          r'''Horizontal components cancel by symmetry. Vertical: $2T\sin30^\circ=mg$, so $T=\frac{mg}{2\cdot0.5}=mg=$ **19.6 N** — each cord carries the full weight! Shallow cords need large tensions (a washing line never goes straight).''', fmt='newtons')
B.md(r'''
### Friction, slopes and pulleys
''')
B.problem(S2, r'A 20 kg crate is pushed with a horizontal force of 100 N; $\mu_k=0.30$. What is its acceleration (m/s²)?', 'num', (100 - 0.3 * 20 * g) / 20,
          [r'$N=mg$ on a flat floor; $f=\mu_kN$.'],
          r'''$f=0.30\cdot196.2=58.9$ N. $a=\frac{100-58.9}{20}=$ **2.06 m/s²**.''', fmt='m/s²')
B.problem(S2, r'A block slides down a $30^\circ$ slope with $\mu_k=0.20$. What is its acceleration (m/s²)?', 'num', g * (0.5 - 0.2 * math.cos(rad(30))),
          [r'$a=g(\sin\theta-\mu_k\cos\theta)$.'],
          r'''$9.81(0.500-0.20\cdot0.866)=9.81\cdot0.327=$ **3.21 m/s²**.''', fmt='m/s²')
B.problem(S2, r'A box starts to slide when a ramp is raised to $22^\circ$. What is the coefficient of static friction?', 'num', math.tan(rad(22)),
          [r'$\mu_s=\tan\theta_{\text{slip}}$.'],
          r'''$\tan22^\circ=$ **0.404**.''')
B.problem(S2, r'An Atwood machine has $m_1=2.0$ kg and $m_2=3.0$ kg. Give (acceleration in m/s², tension in N).', 'tuple', (g / 5, 2 * 2 * 3 * g / 5),
          [r'$a=\frac{m_2-m_1}{m_1+m_2}g$.', r'$T=m_1(g+a)$.'],
          r'''$a=\frac{1}{5}g=1.96$ m/s²; $T=2(9.81+1.96)=23.5$ N. **(1.96, 23.5)**.''', fmt='a tuple `(a, T)`')
B.problem(S2, r'A skydiver (80 kg with gear) has a drag constant $k=0.25$ kg/m. What is the terminal velocity (m/s)?', 'num', math.sqrt(80 * g / 0.25),
          [r'At terminal velocity drag equals weight: $kv^2=mg$.'],
          r'''$v_t=\sqrt{\frac{80\cdot9.81}{0.25}}=\sqrt{3139}=$ **56.0 m/s** (about 200 km/h).''', fmt='m/s')
B.md(r'''
### Work and kinetic energy
''')
B.problem(S3, r'How much net work (J) brings a 1500 kg car from rest to 20 m/s?', 'num', 0.5 * 1500 * 400,
          [r'Work–energy theorem.'],
          r'''$\Delta K=\frac12\cdot1500\cdot400=$ **300 000 J** (300 kJ).''', fmt='joules')
B.problem(S3, r'A force $F(x)=3x^2$ N acts along the $x$-axis. How much work (J) does it do from $x=0$ to $x=2$ m?', 'num', 8,
          [r'$W=\int_0^2 3x^2\,dx$.'],
          r'''$\left[x^3\right]_0^2=$ **8 J**.''', fmt='joules')
B.problem(S3, r'A 1000 kg car at 25 m/s brakes with locked wheels on a road with $\mu_k=0.70$. How far does it slide?', 'num', 625 / (2 * 0.7 * g),
          [r'Friction work $=\mu_kmg\,d$ removes all the kinetic energy.'],
          r'''$d=\frac{v^2}{2\mu_kg}=\frac{625}{13.73}=$ **45.5 m** — the mass cancels.''', fmt='metres')
B.problem(S3, r'A 2.0 kg box moves 3.0 m across a floor while you push it. Your force does $+50$ J of work and friction does $-20$ J. It started at 1.0 m/s. What is its final speed (m/s)?', 'num', math.sqrt(2 * (30 + 1) / 2),
          [r'Net work $=30$ J $=\Delta K$.', r'$K_0=\frac12\cdot2\cdot1=1$ J.'],
          r'''$K=1+30=31$ J; $v=\sqrt{2\cdot31/2}=$ **5.57 m/s**.''', fmt='m/s')
B.md(r'''
### Potential energy, conservation and power
''')
B.problem(S4, r'A roller coaster starts from rest 30 m above the bottom of its track (no friction). What is its speed (m/s) at the bottom?', 'num', math.sqrt(2 * g * 30),
          [r'$mgh=\frac12mv^2$.'],
          r'''$v=\sqrt{2\cdot9.81\cdot30}=$ **24.3 m/s**.''', fmt='m/s')
B.problem(S4, r'A spring with $k=400$ N/m is compressed 0.15 m and launches a 0.20 kg ball straight up. How high (m) does the ball rise above its launch point?', 'num', 0.5 * 400 * 0.15 ** 2 / (0.2 * g),
          [r'$\frac12kx^2=mgh$.'],
          r'''$\frac12kx^2=4.5$ J; $h=\frac{4.5}{0.2\cdot9.81}=$ **2.29 m**.''', fmt='metres')
B.problem(S4, r'A 10 kg sled is given a speed of 8.0 m/s on flat snow with $\mu_k=0.10$. How far does it slide?', 'num', 64 / (2 * 0.1 * g),
          [r'All kinetic energy goes into friction work.'],
          r'''$\mu_kmg\,d=\frac12mv^2$, $d=\frac{64}{2\cdot0.1\cdot9.81}=$ **32.6 m**.''', fmt='metres')
B.problem(S4, r'A 1000 kg car drives at a steady 15 m/s up a $5^\circ$ slope. Ignoring friction and air, what power (W) must the engine deliver?', 'num', 1000 * g * math.sin(rad(5)) * 15,
          [r'Force along the road $=mg\sin\theta$.', r'$P=Fv$.'],
          r'''$F=1000\cdot9.81\cdot\sin5^\circ=855$ N; $P=855\cdot15=$ **12.8 kW** (12 800 W).''', fmt='watts')
B.problem(S4, r'A pendulum bob is released from rest with its string horizontal; the string is 0.80 m long. What is its speed (m/s) at the lowest point?', 'num', math.sqrt(2 * g * 0.8),
          [r'The bob drops by the string length.', r'The tension is always perpendicular to the motion: it does no work.'],
          r'''Tension does no work; only gravity does. Drop $h=0.80$ m: $v=\sqrt{2\cdot9.81\cdot0.8}=$ **3.96 m/s**.''', fmt='m/s')
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
### 2 · Teach-back (30 minutes, from memory)
1. State Newton's three laws. Why do third-law forces never cancel each other?
2. Derive the acceleration and tension of an Atwood machine, and check both with extreme cases.
3. Why is $\mu_s=\tan\theta_{\text{slip}}$?
4. Derive the work–energy theorem, first for a constant force, then with an integral.
5. Why can a roller coaster's speed be found without knowing the shape of the track?

*Your answers:*

&nbsp;

### 3 · What comes next
**Physics 4 — Ohm and Kirchhoff:** energy again, but carried by charge. Voltage is energy per coulomb, current is coulombs per second, and two conservation laws (charge and energy) are all you need to solve any resistor circuit.
''')

if __name__ == '__main__':
    B.write()
