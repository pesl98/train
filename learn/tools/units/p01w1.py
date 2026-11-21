"""Physics strand · Part 1 (weeks 1-3) - SI units, dimensional analysis, estimates, vectors."""
import math
from nbkit import Book
import figs_p01 as F

B = Book('p01w1', 'Physics 1 — Units, dimensions and vectors', 'year1/p01w1-units-dimensions-vectors.ipynb')
S1, S2, S3, S4 = '1 SI units and conversion', '2 Dimensional analysis', '3 Estimates and uncertainty', '4 Vectors'

B.md(r'''
# Physics 1 — Units, dimensions and vectors
*Physics strand, weeks 1–3 · about 9 hours (3 per week), next to Unit 1*

**Why this comes first.** Every physics answer is a number **with a unit**, and most mistakes in physics are not hard mathematics — they are a lost factor 1000, a minute treated as a second, or a force added to an energy. This notebook gives you three habits that catch those mistakes before they cost you, and one tool that all of mechanics is written in: the **vector**.

**What you will be able to do at the end**
1. Name the SI base units, build derived units (newton, joule, watt, volt, ohm) from them, and convert any quantity with the "multiply by one" method.
2. Check an equation by its dimensions — and *derive* the form of a law (the pendulum period) from dimensions alone.
3. Make a quick order-of-magnitude estimate, and say how uncertain a computed result is.
4. Work with vectors in components: magnitude, direction, addition, resolving a force, the dot product.

**Maths used:** algebra, right-angled triangles, $\sin$, $\cos$, $\tan$ and their inverses (Unit 1, weeks 1–2). Nothing else.

Run the grey *SETUP* cell first.
''')

# =====================================================================================
B.md(r'''
---
# Part 1 — SI units

## 1.1 Seven base units — everything else is built from them

**Why.** To compare a measurement in Delft with one in Tokyo, everyone needs the same yardsticks. The International System (SI) defines **seven base units**. Mechanics needs three of them; electricity adds a fourth.

| quantity | unit | symbol |
|---|---|---|
| length | metre | m |
| mass | kilogram | kg |
| time | second | s |
| electric current | ampere | A |
| temperature | kelvin | K |
| amount of substance | mole | mol |
| luminous intensity | candela | cd |

**Derived units** are products and quotients of base units. You do not have to memorise them — each one follows from the law that defines it:

| quantity | defining law | unit | in base units |
|---|---|---|---|
| velocity | $v=\dfrac{\text{distance}}{\text{time}}$ | m/s | $\text{m}\,\text{s}^{-1}$ |
| acceleration | $a=\dfrac{\text{change of velocity}}{\text{time}}$ | m/s² | $\text{m}\,\text{s}^{-2}$ |
| force | $F=ma$ | newton, N | $\text{kg}\,\text{m}\,\text{s}^{-2}$ |
| energy, work | $W=F\,d$ | joule, J $=$ N m | $\text{kg}\,\text{m}^2\text{s}^{-2}$ |
| power | $P=\dfrac{W}{t}$ | watt, W $=$ J/s | $\text{kg}\,\text{m}^2\text{s}^{-3}$ |
| charge | $Q=I\,t$ | coulomb, C $=$ A s | $\text{A}\,\text{s}$ |
| voltage | $V=\dfrac{P}{I}$ | volt, V $=$ W/A | $\text{kg}\,\text{m}^2\text{s}^{-3}\text{A}^{-1}$ |
| resistance | $R=\dfrac{V}{I}$ | ohm, Ω $=$ V/A | $\text{kg}\,\text{m}^2\text{s}^{-3}\text{A}^{-2}$ |

**Worked example — what is a joule?** Step 1: work $=$ force × distance, so $\text{J}=\text{N}\cdot\text{m}$. Step 2: force $=$ mass × acceleration, so $\text{N}=\text{kg}\cdot\text{m/s}^2$. Step 3: substitute: $\text{J}=\text{kg}\cdot\text{m/s}^2\cdot\text{m}=\text{kg}\,\text{m}^2/\text{s}^2$. Lifting 1 kg by 10 cm takes about one joule.

## 1.2 Prefixes

| prefix | symbol | factor | | prefix | symbol | factor |
|---|---|---|---|---|---|---|
| nano | n | $10^{-9}$ | | kilo | k | $10^{3}$ |
| micro | µ | $10^{-6}$ | | mega | M | $10^{6}$ |
| milli | m | $10^{-3}$ | | giga | G | $10^{9}$ |

A prefix is just a number: $4.7\ \text{k}\Omega=4.7\times10^3\ \Omega$, $220\ \mu\text{F}=220\times10^{-6}\ \text{F}$. **Watch out:** $1\ \text{cm}^2=(10^{-2}\ \text{m})^2=10^{-4}\ \text{m}^2$ — the prefix is squared too.

## 1.3 Converting: multiply by one

**Build.** A fraction like $\dfrac{1000\ \text{m}}{1\ \text{km}}$ has the same quantity on top and bottom, so it **equals 1**. Multiplying by 1 never changes a quantity — it only changes how it is written. Choose the fraction so that the unit you want to remove cancels.

**Worked example 1 — 72 km/h in m/s.**
$$72\ \frac{\text{km}}{\text{h}}\times\frac{1000\ \text{m}}{1\ \text{km}}\times\frac{1\ \text{h}}{3600\ \text{s}}=\frac{72\,000}{3600}\ \frac{\text{m}}{\text{s}}=20\ \text{m/s}.$$
km cancels km, h cancels h. A useful shortcut follows: **divide km/h by 3.6** to get m/s.

**Worked example 2 — a kilowatt-hour in joules.** $1\ \text{kWh}=1000\ \text{W}\times3600\ \text{s}=3.6\times10^6\ \text{W s}=3.6\ \text{MJ}$ (a watt-second is a joule).

**Worked example 3 — a phone battery, 3000 mAh, as charge.** mAh is current × time: $3000\times10^{-3}\ \text{A}\times3600\ \text{s}=10\,800\ \text{C}$.

**The habit:** carry the units through every line of a calculation, as if they were algebra symbols. If they do not cancel to the unit you expected, you have made a mistake — before you even look at the number.
''')
B.code(r'''
# Units as algebra: sympy can carry them for you.
from sympy.physics.units import kilometer, meter, hour, second, convert_to, kilogram, newton, joule
v = 72 * kilometer / hour
print(convert_to(v, meter / second))
print(convert_to(joule, [kilogram, meter, second]))
''')
B.ask(r'''Convert 90 km/h to m/s.''', 'num', 25,
      r'''$90\times\frac{1000}{3600}=25$ m/s (or $90/3.6$).''',
      r'''Multiply by $\frac{1000\ \text{m}}{1\ \text{km}}$ and by $\frac{1\ \text{h}}{3600\ \text{s}}$.''', fmt='m/s')
B.ask(r'''A battery delivers 0.25 A for one hour. How much charge (in coulombs) passes?''', 'num', 900,
      r'''$Q=It=0.25\ \text{A}\times3600\ \text{s}=900$ C.''',
      r'''$Q=I\,t$ with $t$ in seconds.''', fmt='coulombs')

# =====================================================================================
B.md(r'''
---
# Part 2 — Dimensional analysis

## 2.1 Dimensions

**Build.** Forget the particular unit (metre, inch, light-year) and keep only *what kind* of quantity it is. Write the **dimension** of a quantity in square brackets, using
$$\mathsf{L}\ (\text{length}),\quad\mathsf{M}\ (\text{mass}),\quad\mathsf{T}\ (\text{time}),\quad\mathsf{I}\ (\text{current}).$$
So $[v]=\mathsf{L\,T^{-1}}$, $[a]=\mathsf{L\,T^{-2}}$, $[F]=\mathsf{M\,L\,T^{-2}}$, $[E]=\mathsf{M\,L^2T^{-2}}$. Pure numbers (2, $\pi$, an angle in radians) have no dimension: $[2\pi]=1$.

## 2.2 Three rules that every correct equation obeys

1. **Both sides have the same dimension.** (A length cannot equal a time.)
2. **You can only add or subtract quantities of the same dimension.** ($3\ \text{m}+2\ \text{s}$ means nothing.)
3. **The argument of $\sin$, $\cos$, $e^{\square}$, $\ln$ must be dimensionless.** (In $e^{-t/\tau}$, $\tau$ must be a time.)

**Worked example — check $v^2=v_0^2+2ax$.** Term by term: $[v^2]=\mathsf{L^2T^{-2}}$; $[v_0^2]=\mathsf{L^2T^{-2}}$; $[2ax]=\mathsf{L\,T^{-2}}\cdot\mathsf{L}=\mathsf{L^2T^{-2}}$. All the same ✓. (This does *not* prove the 2 is right — numbers are invisible to dimensions. It does catch most algebra slips.)

**Worked counter-example.** A student writes $x=v_0t+at$. Then $[at]=\mathsf{L\,T^{-2}}\cdot\mathsf{T}=\mathsf{L\,T^{-1}}$, a velocity, added to a length: wrong. The correct term is $\frac12at^2$.
''')
B.ask(r'''Which equation is dimensionally **wrong**? (a) $x=\tfrac12at^2$ (b) $v=at^2$ (c) $F=mv^2/r$ (d) $E=mgh$''', 'choice', 'b',
      r'''$[at^2]=\mathsf{L\,T^{-2}}\cdot\mathsf{T^2}=\mathsf{L}$ — a length, not a velocity. The others: (a) $\mathsf L$ ✓, (c) $\mathsf{M\,L^2T^{-2}/L}=\mathsf{M\,L\,T^{-2}}$ ✓, (d) $\mathsf{M\cdot L\,T^{-2}\cdot L}$ ✓.''',
      r'''Work out the dimension of the right-hand side of each.''')

B.md(r'''
## 2.3 Deriving a law from dimensions: the pendulum
''')
B.fig('pendulum', F.pendulum, 'A mass m on a string of length L, in gravity g. How long does one swing take?')
B.md(r'''
**Why.** Sometimes you can find the *form* of a law without solving any physics — only by asking which combination of the ingredients has the right dimension.

**Build.** The period $T_p$ of a pendulum (small swings) could depend on the mass $m$, the length $L$ and gravity $g$. Suppose
$$T_p=C\,m^{\alpha}L^{\beta}g^{\gamma}$$
with $C$ a pure number.

**Step 1 — write the dimensions of both sides.**
$$\mathsf{T}^1=\mathsf{M}^{\alpha}\cdot\mathsf{L}^{\beta}\cdot\left(\mathsf{L\,T^{-2}}\right)^{\gamma}=\mathsf{M}^{\alpha}\,\mathsf{L}^{\beta+\gamma}\,\mathsf{T}^{-2\gamma}.$$

**Step 2 — match the powers of each dimension** (they are independent, so each must agree):
$$\mathsf{M}:\ \alpha=0,\qquad \mathsf{L}:\ \beta+\gamma=0,\qquad \mathsf{T}:\ -2\gamma=1.$$

**Step 3 — solve:** $\gamma=-\frac12$, $\beta=\frac12$, $\alpha=0$:
$$\boxed{\,T_p=C\sqrt{\frac{L}{g}}\,}$$

**What we learned without any physics:**
- the period does **not depend on the mass** (Galileo's discovery);
- four times the length gives **twice** the period;
- on the Moon ($g$ six times smaller) the period is $\sqrt6\approx2.4$ times longer.

Dimensions cannot give $C$. Experiment (below) or the theory of Unit 9 gives $C=2\pi$.

### Experiment 1 — measure the pendulum
The cell simulates a real pendulum (Newton's law, solved numerically — you will learn how in Unit 5) and measures the period.

**Predict first:** you double the mass. You quadruple the length. What happens to the period each time?
''')
B.code(r'''
def period(L=1.0, m=1.0, g=9.81, amp_deg=10):
    th, w, tt, h = radians(amp_deg), 0.0, 0.0, 1e-3       # angle, angular velocity, time, step
    crossings = []
    while len(crossings) < 3:
        # one small step of  theta'' = -(g/L) sin(theta)   (m does not appear in the equation at all)
        w_new = w - h * g / L * sin(th); th_new = th + h * w_new
        if w < 0 <= w_new: crossings.append(tt)              # velocity changes sign at the left turning point
        th, w, tt = th_new, w_new, tt + h
    Tp = crossings[2] - crossings[1]
    print(f'measured period {Tp:.3f} s     sqrt(L/g) = {sqrt(L / g):.3f} s     ratio C = {Tp / sqrt(L / g):.3f}   (2*pi = {2 * pi:.3f})')

explore(period, L=(0.25, 4, 0.25, 1), m=(0.1, 5, 0.1, 1), g=(1.6, 25, 0.1, 9.81), amp_deg=(5, 90, 5, 10))
''')
B.md(r'''
**What you should see:** the mass slider changes nothing; $C\approx6.28=2\pi$ whatever $L$ and $g$ — *as long as the swing is small*. Push `amp_deg` to 60° and $C$ creeps up: the "small swings" assumption (Unit 4: $\sin\theta\approx\theta$) is failing.
''')
B.ask(r'''A pendulum of length 1 m has period 2.0 s. What is the period (s) of a 4 m pendulum in the same place?''', 'num', 4,
      r'''$T_p\propto\sqrt L$: $\sqrt4=2$ times longer, so 4.0 s.''',
      r'''$T_p=C\sqrt{L/g}$; only $L$ changes.''', fmt='seconds')

# =====================================================================================
B.md(r'''
---
# Part 3 — Estimates and uncertainty

## 3.1 Order of magnitude

**Why.** Before a long calculation, know roughly what answer to expect. If you expect "about a thousand" and get $10^{-6}$, you look for the mistake.

**Build — a Fermi estimate.** Break the question into factors you can guess to within a factor of 3, then multiply.

*How many heartbeats in a lifetime?* $\approx70\ \tfrac{\text{beats}}{\text{min}}\times60\ \tfrac{\text{min}}{\text{h}}\times24\ \tfrac{\text{h}}{\text{day}}\times365\ \tfrac{\text{days}}{\text{yr}}\times80\ \text{yr}\approx3\times10^9$. The **order of magnitude** is $10^9$ — the power of ten nearest the answer.

## 3.2 Significant figures and uncertainty

Every measurement has an uncertainty: a length "12.0 cm" means "somewhere between 11.95 and 12.05 cm". Write $L=12.0\pm0.05$ cm. The **relative uncertainty** is $\frac{0.05}{12.0}\approx0.4\%$.

**Rule for products and quotients.** If $A=x\cdot y$ (or $x/y$), the relative uncertainties **add**:
$$\frac{\Delta A}{A}\approx\frac{\Delta x}{x}+\frac{\Delta y}{y}.$$

**Why (step by step).** Let $x$ be too large by $\Delta x$ and $y$ by $\Delta y$:
$$(x+\Delta x)(y+\Delta y)=xy+y\,\Delta x+x\,\Delta y+\Delta x\,\Delta y .$$
The last term is the product of two small numbers — much smaller still, drop it. Divide the change $y\Delta x+x\Delta y$ by $A=xy$: $\frac{\Delta x}{x}+\frac{\Delta y}{y}$ ✓. (In Unit 2 you will recognise this as the product rule.)

**Consequence.** For a power, $A=x^n$, the relative uncertainty is $n\frac{\Delta x}{x}$ — squaring doubles it.

**Worked example.** A rectangle measures $10.0\pm0.2$ cm by $4.0\pm0.1$ cm. Area $40$ cm². Relative uncertainty $2\%+2.5\%=4.5\%$, so $\Delta A\approx1.8$ cm²: write $A=40\pm2$ cm².

**How many digits to give.** About as many as the least precise input. $9.81\times1.2$ is $12$, not $11.772$.
''')
B.ask(r'''A ball's speed is measured as $v=5.0\pm0.1$ m/s. What is the relative uncertainty (in %) of its kinetic energy $\tfrac12mv^2$ (take $m$ exact)?''', 'num', 4,
      r'''$\frac{\Delta v}{v}=2\%$; squaring doubles it: 4 %.''',
      r'''For $x^n$ the relative uncertainty is $n$ times that of $x$.''', fmt='a number (percent)')

# =====================================================================================
B.md(r'''
---
# Part 4 — Vectors

## 4.1 Scalars and vectors

A **scalar** is just a number with a unit: mass, time, energy, temperature. A **vector** also has a **direction**: displacement, velocity, force. "5 m/s" is a speed; "5 m/s towards the north-east" is a velocity. We draw a vector as an arrow and write it $\vec v$.

## 4.2 Components
''')
B.fig('components', F.components, 'A vector is fully described by two numbers: its x- and y-components.')
B.md(r'''
**Build.** Put the tail of $\vec v$ at the origin. Drop perpendiculars to the axes: they form a right-angled triangle with hypotenuse $v=|\vec v|$ and angle $\theta$ from the $x$-axis.

**Step 1 — from magnitude and angle to components** (definition of $\cos$, $\sin$ in a right triangle):
$$v_x=v\cos\theta,\qquad v_y=v\sin\theta .$$

**Step 2 — back again.** Pythagoras gives the magnitude, and $\tan\theta=\frac{v_y}{v_x}$ the angle:
$$v=\sqrt{v_x^2+v_y^2},\qquad\theta=\arctan\frac{v_y}{v_x}\quad(\text{careful with the quadrant!}).$$

**The quadrant trap (Unit 1, week 2).** $\arctan$ only returns angles between $-90^\circ$ and $90^\circ$. For $\vec v=(-3,4)$, $\arctan\frac{4}{-3}=-53.1^\circ$ — but the vector points up-left, at $180^\circ-53.1^\circ=126.9^\circ$. Always sketch the vector. In code use `atan2(vy, vx)`, which looks at both signs.

We write $\vec v=(v_x,v_y)$, or with the **unit vectors** $\hat\imath=(1,0)$, $\hat\jmath=(0,1)$: $\vec v=v_x\hat\imath+v_y\hat\jmath$.

## 4.3 Adding vectors
''')
B.fig('vector_add', F.vector_add, 'Tip to tail. In components: add x to x and y to y.')
B.md(r'''
**Build.** Walk 3.2 m east and 0.9 m north (vector $\vec a$), then 1.6 m east and 1.9 m north ($\vec b$). Where are you? East: $3.2+1.6=4.8$ m. North: $0.9+1.9=2.8$ m. So
$$\vec a+\vec b=(a_x+b_x,\ a_y+b_y).$$
Graphically: put the tail of $\vec b$ at the tip of $\vec a$. **Never add magnitudes** — $|\vec a+\vec b|$ is usually *less* than $|\vec a|+|\vec b|$ (here $5.56$ m versus $3.32+2.48=5.80$ m).

**Scaling:** $k\vec v=(kv_x,kv_y)$ — same direction (reversed if $k<0$), $|k|$ times as long. **Subtracting:** $\vec a-\vec b=\vec a+(-1)\vec b$.

**Worked example — three forces on a ring.** Forces $\vec F_1=(30,0)$ N, $\vec F_2=(0,40)$ N and an unknown $\vec F_3$ hold a ring still. Still means the total force is zero (Newton, Physics 3): $\vec F_3=-(\vec F_1+\vec F_2)=(-30,-40)$ N, magnitude 50 N.
''')
B.code(r'''
def add(a=3.0, a_deg=15, b=2.5, b_deg=50):
    A = np.array([a * cos(radians(a_deg)), a * sin(radians(a_deg))])
    Bv = np.array([b * cos(radians(b_deg)), b * sin(radians(b_deg))])
    S = A + Bv
    plt.figure(figsize=(5, 4))
    kw = dict(angles='xy', scale_units='xy', scale=1, width=0.012)
    plt.quiver(0, 0, *A, color='C0', **kw); plt.quiver(*A, *Bv, color='C2', **kw); plt.quiver(0, 0, *S, color='C3', **kw)
    plt.xlim(-6, 6); plt.ylim(-6, 6); plt.gca().set_aspect('equal'); plt.show()
    print(f'a + b = ({S[0]:.2f}, {S[1]:.2f})   |a+b| = {np.hypot(*S):.2f}   |a| + |b| = {a + b:.2f}   direction {degrees(atan2(S[1], S[0])):.1f} deg')

explore(add, a=(0, 5, 0.1, 3), a_deg=(-180, 180, 5, 15), b=(0, 5, 0.1, 2.5), b_deg=(-180, 180, 5, 50))
''')
B.md(r'''
**Try:** make the two angles equal (then $|\vec a+\vec b|=a+b$), then $180^\circ$ apart (then it is $|a-b|$). Every other case is in between.
''')
B.ask(r'''What is the magnitude of $\vec v=(-6,8)$?''', 'num', 10,
      r'''$\sqrt{36+64}=10$.''', r'''Pythagoras on the components.''')
B.ask(r'''A force of 20 N points at $120^\circ$ from the $+x$ axis. What is its $x$-component (N)?''', 'num', -10,
      r'''$20\cos120^\circ=20\cdot(-\tfrac12)=-10$ N — negative, because it points to the left.''',
      r'''$F_x=F\cos\theta$; the sign matters.''', fmt='newtons (with sign)')

B.md(r'''
## 4.4 Resolving a force on a slope
''')
B.fig('incline_resolve', F.incline_resolve, 'The weight split into a part along the slope and a part into the slope.')
B.md(r'''
**Build.** On a slope it is easier to use tilted axes: one **along** the slope, one **perpendicular** to it.

**Step 1.** The angle between the weight $mg$ (straight down) and the perpendicular to the slope equals the slope angle $\theta$. (Both are "rotated by $\theta$" from the vertical and from the horizontal respectively.)

**Step 2.** So, in the tilted axes:
$$\text{along the slope (downhill)}:\ mg\sin\theta,\qquad\text{into the slope}:\ mg\cos\theta .$$

**Sanity check with the extremes** — always do this: $\theta=0$ (flat): nothing along the slope, all $mg$ into it ✓. $\theta=90^\circ$ (vertical wall): all $mg$ along it — free fall ✓.

## 4.5 The dot product

**Why.** Physics often asks "how much of $\vec a$ points along $\vec b$?" — work is force *along* the motion (Physics 3), power is force along the velocity.

**Build.** Define
$$\vec a\cdot\vec b=a_xb_x+a_yb_y\qquad(\text{a scalar}).$$
**Claim:** $\vec a\cdot\vec b=|\vec a|\,|\vec b|\cos\varphi$, with $\varphi$ the angle between them.

*Proof, step by step.* The vector $\vec a-\vec b$ closes the triangle with sides $\vec a$ and $\vec b$.
1. Law of cosines: $|\vec a-\vec b|^2=|\vec a|^2+|\vec b|^2-2|\vec a||\vec b|\cos\varphi$.
2. In components: $|\vec a-\vec b|^2=(a_x-b_x)^2+(a_y-b_y)^2=|\vec a|^2+|\vec b|^2-2(a_xb_x+a_yb_y)$.
3. Compare the two lines: $a_xb_x+a_yb_y=|\vec a||\vec b|\cos\varphi$ ∎

**Uses.** The angle between two vectors: $\cos\varphi=\frac{\vec a\cdot\vec b}{|\vec a||\vec b|}$. Perpendicular vectors: $\vec a\cdot\vec b=0$. The component of $\vec a$ along a unit vector $\hat u$: $\vec a\cdot\hat u$.

**Worked example.** $\vec a=(3,4)$, $\vec b=(4,-3)$: $\vec a\cdot\vec b=12-12=0$ — perpendicular.
''')
B.ask(r'''$\vec a=(1,2)$ and $\vec b=(3,-1)$. What is $\vec a\cdot\vec b$?''', 'num', 1,
      r'''$1\cdot3+2\cdot(-1)=1$.''', r'''$a_xb_x+a_yb_y$.''')

B.md(r'''
### Code it — the direction of a vector, in every quadrant
Complete the function. It must return the angle from the $+x$ axis in degrees, **between 0 and 360**. Use `atan2(vy, vx)` (radians, between $-\pi$ and $\pi$) and fix negative results.
''')
B.code(r'''
def direction(vx, vy):
    """Angle of the vector (vx, vy) from the +x axis, in degrees, 0 <= angle < 360."""
    ang = ...                # atan2 gives radians; convert with degrees(...)
    return ang               # if it is negative, add 360 first


# ---------- tests: do not change ----------
for v, want in (((1, 1), 45), ((-1, 1), 135), ((-1, -1), 225), ((0, -2), 270), ((3, 0), 0), ((-3, 4), 126.87)):
    try:
        got = direction(*v); ok = abs(got - want) < 0.01
    except Exception as err:
        got, ok = err, False
    print('✓' if ok else '✗', v, '->', got, '  expected', want)
''', ref=r'''
def direction(vx, vy):
    ang = degrees(atan2(vy, vx))
    return ang + 360 if ang < 0 else ang
for v, want in (((1, 1), 45), ((-1, 1), 135), ((-1, -1), 225), ((0, -2), 270), ((3, 0), 0), ((-3, 4), 126.87)):
    assert abs(direction(*v) - want) < 0.01
print('ok')
''')

B.md(r'''
## Summary — everything on one page

- **SI base units** m, kg, s, A (+ K, mol, cd). Derived: N $=$ kg m/s², J $=$ N m, W $=$ J/s, C $=$ A s, V $=$ W/A, Ω $=$ V/A.
- **Convert** by multiplying by fractions equal to 1; carry units through every line. km/h ÷ 3.6 = m/s; 1 kWh = 3.6 MJ.
- **Dimensions**: both sides equal, only add like with like, arguments of sin/exp dimensionless. Matching powers gives the form of a law: $T_p\propto\sqrt{L/g}$.
- **Uncertainty**: relative uncertainties add for products and quotients; multiply by $n$ for a power.
- **Vectors**: $v_x=v\cos\theta$, $v_y=v\sin\theta$; $v=\sqrt{v_x^2+v_y^2}$; angle via a sketch or `atan2`. Add component by component.
- **Slope**: $mg\sin\theta$ along, $mg\cos\theta$ into. **Dot product** $a_xb_x+a_yb_y=|a||b|\cos\varphi$.
''')

# =====================================================================================
B.md(r'''
---
# Problems

Paper first. First attempt counts. `hint(n)` → `solution(n)` → `mistake(n, '...')`.

### SI units and conversion
''')
B.problem(S1, r'A car drives at 108 km/h. What is its speed in m/s?', 'num', 30,
          [r'Divide by 3.6 — or multiply by $\frac{1000}{3600}$.'],
          r'''$108\times\frac{1000\ \text{m}}{3600\ \text{s}}=$ **30 m/s**.''', fmt='m/s')
B.problem(S1, r'A light-year is the distance light travels in one year (365.25 days) at $c=3.00\times10^8$ m/s. How many metres is that?', 'num', 3e8 * 365.25 * 86400,
          [r'Seconds in a year: $365.25\times24\times3600$.', r'Distance $=$ speed × time.'],
          r'''$t=365.25\times86\,400=3.156\times10^7$ s. $d=3.00\times10^8\times3.156\times10^7\approx$ **$9.47\times10^{15}$ m**.''', fmt='metres; you can type `9.47e15`')
B.problem(S1, r'Water has a density of 1.00 g/cm³. Express this in kg/m³.', 'num', 1000,
          [r'$1\ \text{cm}^3=(10^{-2}\ \text{m})^3$.', r'$1\ \text{g}=10^{-3}$ kg.'],
          r'''$1\ \frac{\text{g}}{\text{cm}^3}\times\frac{10^{-3}\ \text{kg}}{1\ \text{g}}\times\frac{1\ \text{cm}^3}{10^{-6}\ \text{m}^3}=$ **1000 kg/m³**. (The cube of the prefix is the usual trap.)''', fmt='kg/m³')
B.problem(S1, r'A 2 kW kettle runs for 3 minutes. How much energy does it use, in kilojoules?', 'num', 360,
          [r'Energy $=$ power × time, with time in seconds.'],
          r'''$E=Pt=2000\ \text{W}\times180\ \text{s}=360\,000$ J $=$ **360 kJ** (0.1 kWh).''', fmt='kJ')
B.md(r'''
### Dimensional analysis
''')
B.problem(S2, r'A spring with stiffness $k$ (unit N/m) carries a mass $m$. Suppose its period is $T_p=C\,m^{\alpha}k^{\beta}$. Find $(\alpha,\beta)$.', 'tuple', (0.5, -0.5),
          [r'$[k]=\frac{[F]}{\mathsf L}=\mathsf{M\,T^{-2}}$.', r'Match: $\mathsf M$: $\alpha+\beta=0$; $\mathsf T$: $-2\beta=1$.'],
          r'''$[k]=\mathsf{M\,L\,T^{-2}}/\mathsf L=\mathsf{M\,T^{-2}}$. So $\mathsf T=\mathsf M^{\alpha}\mathsf M^{\beta}\mathsf T^{-2\beta}$: $\beta=-\frac12$, $\alpha=\frac12$.

$T_p=C\sqrt{m/k}$ (and $C=2\pi$ again — Unit 9). Answer **(0.5, −0.5)**.''', fmt='a tuple `(alpha, beta)`')
B.problem(S2, r'The speed of a wave on a string depends on the tension $F$ (N) and the mass per metre $\mu$ (kg/m): $v=C\,F^{a}\mu^{b}$. Find $(a,b)$.', 'tuple', (0.5, -0.5),
          [r'$[F]=\mathsf{M\,L\,T^{-2}}$, $[\mu]=\mathsf{M\,L^{-1}}$.', r'Three equations: $\mathsf M$: $a+b=0$; $\mathsf L$: $a-b=1$; $\mathsf T$: $-2a=-1$.'],
          r'''$\mathsf{L\,T^{-1}}=\mathsf{M}^{a+b}\mathsf{L}^{a-b}\mathsf{T}^{-2a}$. $\mathsf T$: $a=\frac12$; $\mathsf M$: $b=-\frac12$; $\mathsf L$: $\frac12+\frac12=1$ ✓ (a free check).

$v=C\sqrt{F/\mu}$ — tighter strings and lighter strings carry faster waves (and sound higher). **(0.5, −0.5)**.''', fmt='a tuple `(a, b)`')
B.problem(S2, r'Air drag at high speed is $F=k\,v^2$. What is the unit of $k$? (a) kg/s (b) kg/m (c) kg·m/s (d) N·s', 'choice', 'b',
          [r'$k=F/v^2$; write N in base units.'],
          r'''$[k]=\frac{\mathsf{M\,L\,T^{-2}}}{\mathsf{L^2T^{-2}}}=\mathsf{M\,L^{-1}}$: **(b) kg/m**.''')
B.problem(S2, r'In $x(t)=A\,e^{-t/\tau}\cos(\omega t)$, $x$ is in metres and $t$ in seconds. What is the unit of $\omega$? (a) s (b) 1/s (c) m/s (d) none', 'choice', 'b',
          [r'The argument of $\cos$ must be dimensionless.'],
          r'''$\omega t$ must be a pure number, so $[\omega]=\mathsf T^{-1}$: **(b) 1/s** (radians per second). Likewise $\tau$ is in seconds and $A$ in metres.''')
B.md(r'''
### Estimates and uncertainty
''')
B.problem(S3, r'A rectangle measures $10.0\pm0.2$ cm by $4.0\pm0.1$ cm. What is the relative uncertainty of its area, in percent?', 'num', 4.5,
          [r'Relative uncertainties add for a product.'],
          r'''$\frac{0.2}{10}+\frac{0.1}{4}=2\%+2.5\%=$ **4.5 %**.''', fmt='a number (percent)')
B.problem(S3, r'The volume of a sphere is $\frac43\pi r^3$. The radius is measured to $\pm1\%$. What is the relative uncertainty of the volume (%)?', 'num', 3,
          [r'A power $n$ multiplies the relative uncertainty by $n$; $\frac43\pi$ is exact.'],
          r'''$3\times1\%=$ **3 %**.''', fmt='a number (percent)')
B.problem(S3, r'Estimate the number of seconds in a human lifetime of 80 years. Give the order of magnitude: the exponent $n$ in $10^n$.', 'num', 9,
          [r'One year is about $3\times10^7$ s.'],
          r'''$80\times3.2\times10^7\approx2.5\times10^9$ s: order of magnitude **9**.''', fmt='an integer')
B.md(r'''
### Vectors
''')
B.problem(S4, r'A velocity of 10 m/s points at $30^\circ$ above the $+x$ axis. Give its components $(v_x,v_y)$.', 'tuple', (10 * math.cos(math.pi / 6), 5),
          [r'$v_x=v\cos\theta$, $v_y=v\sin\theta$.'],
          r'''$v_x=10\cos30^\circ=8.66$, $v_y=10\sin30^\circ=5$: **(8.66, 5)** m/s.''', fmt='a tuple `(vx, vy)`')
B.problem(S4, r'Give the magnitude and the direction (degrees from $+x$, between 0 and 360) of $\vec v=(-3,4)$.', 'tuple', (5, 180 - math.degrees(math.atan(4 / 3))),
          [r'Magnitude: Pythagoras.', r'Sketch it: it points up and to the left (second quadrant). $\arctan(4/3)=53.13^\circ$ is the angle with the $-x$ axis.'],
          r'''$|\vec v|=5$. The vector is in the second quadrant: $180^\circ-53.13^\circ=126.87^\circ$. **(5, 126.87)**.''', fmt='a tuple `(magnitude, degrees)`')
B.problem(S4, r'Two forces act on a box: 12 N to the east and 5 N to the north. What single force (magnitude in N) has the same effect?', 'num', 13,
          [r'Add the vectors: $(12,5)$.'],
          r'''$\vec F=(12,5)$ N, $|\vec F|=\sqrt{144+25}=$ **13 N**, at $\arctan\frac5{12}=22.6^\circ$ north of east.''', fmt='newtons')
B.problem(S4, r'A 4.0 kg box sits on a $25^\circ$ slope ($g=9.81$ m/s²). What is the component of its weight along the slope (N)?', 'num', 4 * 9.81 * math.sin(math.radians(25)),
          [r'$mg\sin\theta$.'],
          r'''$4.0\times9.81\times\sin25^\circ=39.24\times0.4226\approx$ **16.6 N**.''', fmt='newtons')
B.problem(S4, r'What is the angle (degrees) between $\vec a=(2,1)$ and $\vec b=(1,3)$?', 'num', 45,
          [r'$\cos\varphi=\frac{\vec a\cdot\vec b}{|\vec a||\vec b|}$.', r'$\vec a\cdot\vec b=5$, $|\vec a|=\sqrt5$, $|\vec b|=\sqrt{10}$.'],
          r'''$\cos\varphi=\frac{5}{\sqrt5\sqrt{10}}=\frac{5}{\sqrt{50}}=\frac{1}{\sqrt2}$, so $\varphi=$ **45°**.''', fmt='degrees')
B.problem(S4, r'Three ropes pull on a ring that does not move. Two of the forces are $(4,0)$ N and $(-1,3)$ N. Give the third force $(F_x,F_y)$.', 'tuple', (-3, -3),
          [r'At rest: the three forces add to zero.'],
          r'''$\vec F_3=-\big((4,0)+(-1,3)\big)=-(3,3)=$ **(−3, −3) N**.''', fmt='a tuple `(Fx, Fy)`')
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
1. Build the joule and the ohm from base units.
2. State the three rules of dimensional analysis and use them to derive $T_p\propto\sqrt{L/g}$.
3. Why do relative uncertainties add when you multiply?
4. Why is $|\vec a+\vec b|$ not $|\vec a|+|\vec b|$? When is it?
5. Prove $\vec a\cdot\vec b=|\vec a||\vec b|\cos\varphi$.

*Your answers:*

&nbsp;

### 3 · Lab — vectors in motion (30 minutes)
The Physics Lab opens on projectile motion. Watch the velocity arrow: its horizontal component never changes; only the vertical one does — gravity is a vector pointing down. **Predict first:** at the highest point, what are $v_x$ and $v_y$? Then pause there and read the velocity graph.
''')
B.code(r'''
lab('physics', height=640, exp='proj', k=0)
''')
B.md(r'''
### 4 · What comes next
**Physics 2 — kinematics:** position, velocity and acceleration as vectors that change in time — and, as soon as Unit 2 gives you derivatives, the exact link between them.
''')

if __name__ == '__main__':
    B.write()
