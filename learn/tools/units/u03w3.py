"""Unit 3 · Week 3 (course week 10) - Applications of the integral."""
import math
from nbkit import Book
import figs_u03 as F

B = Book('u03w3', 'Unit 3 · Week 3 — Applications of the integral', 'year1/u03w3-applications-of-integration.ipynb')
S1, S2, S3, S4 = '1 Areas and volumes', '2 Average and RMS', '3 Work and energy', '4 Improper integrals'

B.md(r'''
# Unit 3 · Week 3 — Applications of the integral
*Term 1, week 10 of 12 · about 15 hours in this notebook and on paper*

**Where you are.** You know what an integral is (a limit of sums) and how to compute one (antiderivatives, substitution, parts, or numerically). This week uses it. Every application follows the **same four-step pattern** — learn the pattern, not the formulas:

> 1. **Slice** the thing into thin pieces.
> 2. **Approximate** the contribution of one piece (it is thin, so something is nearly constant across it).
> 3. **Add** the pieces: a Riemann sum.
> 4. **Take the limit**: the sum becomes an integral.

In practice steps 3 and 4 are one move: write the contribution of one thin piece with a $dx$ in it, and put $\int$ in front.

**What you will be able to do at the end of this week**
1. Compute areas between curves and volumes of solids of revolution — and derive $\pi r^2$, $\frac43\pi r^3$ and $\frac13\pi r^2h$ yourself.
2. Compute average and RMS values, and explain why 230 V mains has a peak of 325 V.
3. Compute work as $\int F\,dx$; derive the energy of a spring, the kinetic energy $\frac12mv^2$ and the energy of a capacitor.
4. Evaluate integrals over infinite intervals and decide whether they converge.

**What is used from earlier:** the fundamental theorem and all techniques (weeks 1–2); limits at infinity and L'Hôpital (Units 1–2).

Run the grey *SETUP* cell first. `nint(f, a, b)` checks any definite integral.
''')

# =====================================================================================
B.md(r'''
---
# Part 1 — Areas and volumes

## 1.1 The area between two curves

**Build.** Two curves, $y=f(x)$ on top and $y=g(x)$ below, between $x=a$ and $x=b$.

1. **Slice** the region into thin vertical strips of width $dx$.
2. **One strip** is nearly a rectangle: height = top − bottom $=f(x)-g(x)$, area $\big[f(x)-g(x)\big]\,dx$.
3.–4. **Add and take the limit:**
$$\boxed{\,A=\int_a^b\big[f(x)-g(x)\big]\,dx\,}\qquad(\text{top minus bottom}).$$
''')
B.fig('between_curves', F.between_curves, 'One thin strip of the region between y = x and y = x².')
B.md(r'''
**The procedure.**
1. **Sketch** both curves.
2. Find where they **cross** (solve $f(x)=g(x)$): these are usually the limits.
3. Decide which is **on top** (test one point between the crossings).
4. Integrate top − bottom.

**Worked example 1 (from your diagnostic).** The region enclosed by $y=x$ and $y=x^2$.
1. A line and a parabola. 2. $x=x^2\Rightarrow x(x-1)=0\Rightarrow x=0,\ 1$. 3. At $x=\frac12$: line $\frac12$, parabola $\frac14$ — the line is on top.
4. $A=\displaystyle\int_0^1(x-x^2)\,dx=\left[\frac{x^2}{2}-\frac{x^3}{3}\right]_0^1=\frac12-\frac13=\frac16$.

**Worked example 2.** The region between $y=x^2$ and $y=x+2$.
2. $x^2=x+2\Rightarrow x^2-x-2=(x-2)(x+1)=0\Rightarrow x=-1,\ 2$. 3. At $x=0$: line 2, parabola 0 — line on top.
4. $A=\displaystyle\int_{-1}^{2}(x+2-x^2)\,dx=\left[\frac{x^2}{2}+2x-\frac{x^3}{3}\right]_{-1}^{2}=\left(2+4-\frac83\right)-\left(\frac12-2+\frac13\right)=\frac{10}{3}+\frac76=\frac92 .$

**If the curves cross inside the interval**, "top" and "bottom" swap there: split the integral at the crossing and treat each part separately (otherwise the pieces partly cancel, as with signed area).
''')
B.ask(r'''Find the area enclosed between $y=x^2$ and $y=4$.''', 'num', 32 / 3,
      r'''Crossings: $x^2=4$, $x=\pm2$. Top is the line $y=4$. $\int_{-2}^{2}(4-x^2)\,dx=\left[4x-\frac{x^3}{3}\right]_{-2}^{2}=2\left(8-\frac83\right)=\frac{32}{3}\approx10.67$.''',
      r'''Where does the parabola reach height 4? Integrate $4-x^2$ between those two points.''', fmt='a number, e.g. `32/3`')

B.md(r'''
## 1.2 The area of a circle — the promise from Unit 1

**Why.** In Unit 1 week 1 we *used* the area $\pi r^2$ of a disc and promised to derive it. The only fact about circles we had was the definition of $\pi$: circumference $=2\pi\times$ radius.

**Build.** Slice the disc into thin **rings**, like the growth rings of a tree.
''')
B.fig('rings', F.rings, 'A thin ring of radius ρ, cut open and straightened, is nearly a rectangle.')
B.md(r'''
1. **Slice:** rings of radius $\rho$ (from $0$ to $r$) and width $d\rho$.
2. **One ring**, cut open and straightened, is nearly a rectangle of length $2\pi\rho$ (its circumference) and width $d\rho$: area $2\pi\rho\,d\rho$.
3.–4. **Add:**
$$A=\int_0^r2\pi\rho\,d\rho=\big[\pi\rho^2\big]_0^r=\pi r^2 .\qquad\blacksquare$$

Notice the pattern: **the derivative of the area $\pi r^2$ is the circumference $2\pi r$** — growing the disc by $dr$ adds one ring. The same holds one dimension up: the derivative of the volume $\frac43\pi r^3$ of a ball is its surface area $4\pi r^2$ (you met that with the balloon in Unit 2 week 3).

## 1.3 Volumes: slicing into discs

**Build.** Take the region under $y=f(x)$ between $a$ and $b$ and **rotate it about the $x$-axis**. It sweeps out a solid — a *solid of revolution* (a vase, a shaft, a ball).

1. **Slice** the solid perpendicular to the $x$-axis into thin discs of thickness $dx$.
2. **One disc** at position $x$ has radius $y=f(x)$: its face has area $\pi y^2$, its volume is $\pi y^2\,dx$.
3.–4. **Add:**
$$\boxed{\,V=\int_a^b\pi\,\big[f(x)\big]^2\,dx\,}$$
''')
B.fig('disc_sphere', F.disc_sphere, 'A ball is a half-disc rotated about the x-axis. Sliced like a loaf, each slice is a disc of radius y.')
B.md(r'''
**Worked example 1 — the volume of a ball.** The upper half of the circle $x^2+y^2=r^2$ is $y=\sqrt{r^2-x^2}$, for $-r\le x\le r$. Rotated, it gives a ball. Then $y^2=r^2-x^2$ — the root disappears:
$$V=\int_{-r}^{r}\pi\,(r^2-x^2)\,dx=\pi\left[r^2x-\frac{x^3}{3}\right]_{-r}^{r}=\pi\left[\left(r^3-\frac{r^3}{3}\right)-\left(-r^3+\frac{r^3}{3}\right)\right]=\pi\cdot\frac{4r^3}{3}.$$
$$V=\frac43\pi r^3 .\qquad\blacksquare$$

**Worked example 2 — the volume of a cone.** A cone of height $h$ and base radius $r$ is the line $y=\dfrac rhx$ ($0\le x\le h$) rotated about the $x$-axis:
$$V=\int_0^h\pi\,\frac{r^2}{h^2}\,x^2\,dx=\pi\,\frac{r^2}{h^2}\cdot\frac{h^3}{3}=\frac13\pi r^2h .\qquad\blacksquare$$
A third of the cylinder that contains it — the "$\frac13$" is the $\frac13$ of $\int x^2\,dx=\frac{x^3}{3}$.

**Worked example 3.** $y=\sqrt{x}$, $0\le x\le4$, rotated: $V=\displaystyle\int_0^4\pi x\,dx=\pi\cdot8=8\pi$.
''')
B.ask(r'''The region under $y=x$ from $x=0$ to $x=3$ is rotated about the $x$-axis. What is the volume?''', 'num', 9 * math.pi,
      r'''$V=\int_0^3\pi x^2\,dx=\pi\cdot\frac{27}{3}=9\pi\approx28.27$. (A cone with $r=3$, $h=3$: $\frac13\pi\cdot9\cdot3$ ✓.)''',
      r'''$V=\int\pi y^2\,dx$ with $y=x$.''', fmt='a number; you can type `9*pi`')

# =====================================================================================
B.md(r'''
---
# Part 2 — Averages and RMS

## 2.1 The average value of a function

**Why.** What is the average temperature over a day, the average power over a cycle? For finitely many values you add and divide by how many. For a continuously varying quantity, "add" becomes "integrate" and "how many" becomes the length of the interval.

**Build.** Sample $f$ at $n$ equally spaced points of $[a,b]$ and average:
$$\frac{f(x_1)+\dots+f(x_n)}{n}=\frac{1}{b-a}\sum_{k=1}^nf(x_k)\,\frac{b-a}{n}=\frac{1}{b-a}\sum_{k=1}^nf(x_k)\,\Delta x .$$
(Multiply and divide by $b-a$; then $\frac{b-a}{n}=\Delta x$.) That is a Riemann sum. As $n\to\infty$:
$$\boxed{\,f_{\text{avg}}=\frac{1}{b-a}\int_a^bf(x)\,dx\,}$$
''')
B.fig('average_value', F.average_value, 'The average value is the height of the rectangle with the same area.')
B.md(r'''
**Geometric meaning:** $f_{\text{avg}}\cdot(b-a)=\int_a^bf$: the average is the height of the rectangle on the same base with the same area — "level the hills into the valleys".

**Worked example 1.** Average of $x^2$ on $[0,3]$: $\dfrac13\displaystyle\int_0^3x^2\,dx=\dfrac13\cdot9=3$. (Not $\frac{0+9}{2}=4.5$: the function spends most of the interval low.)

**Worked example 2.** Average of $\sin x$ over the half-period $[0,\pi]$: $\dfrac1\pi\displaystyle\int_0^\pi\sin x\,dx=\dfrac2\pi\approx0.637$. Over a *full* period the average is $0$.

## 2.2 RMS: the average that matters for power

**Why.** The mains voltage $v(t)=V\sin\omega t$ has average zero — yet it certainly heats a kettle. The heating power in a resistor is $p=\dfrac{v^2}{R}$, and $v^2$ is never negative. What counts for power is the **average of the square**.

**Build.**

**Step 1 — average power.** $P_{\text{avg}}=\dfrac{1}{R}\cdot\big(\text{average of }v^2\big)$.

**Step 2 — define the equivalent steady voltage.** Which *constant* voltage $V_{\text{rms}}$ would give the same average power, $\dfrac{V_{\text{rms}}^2}{R}$? Comparing: $V_{\text{rms}}^2=$ average of $v^2$. So
$$\boxed{\,V_{\text{rms}}=\sqrt{\frac1T\int_0^Tv(t)^2\,dt}\,}$$
Read the name backwards: the **R**oot of the **M**ean of the **S**quare.

**Step 3 — for a sinusoid.** With $v=V\sin\omega t$ over one period $T=\frac{2\pi}{\omega}$, use power reduction (last week, §3.1): $\sin^2\omega t=\frac{1-\cos2\omega t}{2}$. Over a full period the cosine term averages to zero, leaving $\frac12$:
$$\text{average of }v^2=\frac{V^2}{2}\qquad\Longrightarrow\qquad\boxed{\,V_{\text{rms}}=\frac{V}{\sqrt2}\approx0.707\,V\,}$$
''')
B.fig('rms', F.rms, 'The square of a sinusoid is a sinusoid of twice the frequency, swinging around half the peak value.')
B.md(r'''
**The mains.** "230 V" is the RMS value. The peak is $230\cdot\sqrt2\approx325$ V — the amplitude you met in Unit 1 week 2. A 230 V AC supply heats a resistor exactly as much as a 230 V battery would.

**RMS depends on the shape.** For a square wave switching between $+V$ and $-V$, $v^2=V^2$ all the time: $V_{\text{rms}}=V$. For a triangle wave it is $\frac{V}{\sqrt3}$ (problem set).

### Experiment 1 — RMS of different waveforms
**Predict first:** all three waves have peak value 1. Rank them by RMS value. Which heats a resistor most?
''')
B.code(r'''
def wave_rms(shape='sine'):
    ts = np.linspace(0, 1, 4001)
    waves = {'sine': np.sin(2 * pi * ts),
             'square': np.sign(np.sin(2 * pi * ts)),
             'triangle': 2 / pi * np.arcsin(np.sin(2 * pi * ts))}
    v = waves[shape]
    mean_square = np.mean(v**2)                       # the average of v²: a Riemann sum divided by the length
    fig, (a1, a2) = plt.subplots(1, 2, figsize=(10.5, 3.3))
    a1.plot(ts, v); a1.axhline(0, color='k', lw=0.8); a1.set_title('v(t)'); a1.set_ylim(-1.2, 1.2)
    a2.plot(ts, v**2, 'r'); a2.fill_between(ts, 0, v**2, color='r', alpha=0.15); a2.axhline(mean_square, color='g', ls='--'); a2.set_title('v² and its average'); a2.set_ylim(0, 1.2)
    plt.show()
    print(f'{shape}:  average of v = {np.mean(v):+.3f}    average of v² = {mean_square:.4f}    RMS = {sqrt(mean_square):.4f}')

explore(wave_rms, shape=['sine', 'square', 'triangle'])
''')
B.ask(r'''What is the average value of $f(x)=3x^2$ on $[0,2]$?''', 'num', 4,
      r'''$\dfrac{1}{2-0}\displaystyle\int_0^23x^2\,dx=\dfrac12\big[x^3\big]_0^2=\dfrac82=4$.''',
      r'''$\dfrac{1}{b-a}\displaystyle\int_a^bf(x)\,dx$.''')
B.ask(r'''A sinusoidal voltage has a peak of $170$ V (the US mains). What is its RMS value?''', 'num', 170 / math.sqrt(2),
      r'''$\dfrac{170}{\sqrt2}\approx120$ V.''',
      r'''$V_{\text{rms}}=\dfrac{V}{\sqrt2}$.''', fmt='volts')

# =====================================================================================
B.md(r'''
---
# Part 3 — Work and energy

## 3.1 Work done by a varying force

**Build.** For a **constant** force $F$ along the direction of motion, work = force × distance: $W=F\,d$ (in joules, N·m). If the force **varies** with position:

1. **Slice** the path into short steps $dx$.
2. Over one short step the force is nearly constant: work $\approx F(x)\,dx$.
3.–4. **Add:**
$$\boxed{\,W=\int_a^bF(x)\,dx\,}$$
Work is the area under the force–position graph — exactly as distance is the area under the velocity–time graph.

## 3.2 The energy stored in a spring

**Build.** Hooke's law: to hold a spring stretched by $x$ you must pull with a force $F=kx$ ($k$ is the stiffness, in N/m). The force grows as you stretch — so "force × distance" does not apply directly.
''')
B.fig('spring_work', F.spring_work, 'The work to stretch a spring is the area of a triangle.')
B.md(r'''
$$W=\int_0^xk\,s\,ds=\left[\frac{k\,s^2}{2}\right]_0^x=\frac12kx^2 .$$
(The variable inside is called $s$ because $x$ is the end point.) That work is stored in the spring as **elastic potential energy** $\frac12kx^2$. Geometrically: a triangle with base $x$ and height $kx$. The factor $\frac12$ is there because the *average* force during the stretch is half the final force.

## 3.3 Where $\frac12mv^2$ comes from

**Theorem (work–energy).** The work done by the net force on a body equals the change in $\frac12mv^2$.

**Proof.** Newton's second law: $F=ma=m\dfrac{dv}{dt}$. The work along the path:
$$W=\int F\,dx=\int m\,\frac{dv}{dt}\,dx .$$
The body moves, so $x$ is a function of time: $dx=\dfrac{dx}{dt}\,dt=v\,dt$ (a substitution, from $x$ to $t$):
$$W=\int m\,\frac{dv}{dt}\,v\,dt .$$
Now substitute again, from $t$ to $v$: $\dfrac{dv}{dt}\,dt=dv$:
$$W=\int_{v_1}^{v_2}m\,v\,dv=\left[\frac12mv^2\right]_{v_1}^{v_2}=\frac12mv_2^2-\frac12mv_1^2 .\qquad\blacksquare$$

So **kinetic energy** $\frac12mv^2$ is not a definition pulled from the air: it is *what the integral of force over distance turns out to be*. The $\frac12$ and the square are the $\int v\,dv=\frac{v^2}{2}$ of the power rule.

**Worked example — a spring launcher.** A spring with $k=200$ N/m is compressed by $0.1$ m and launches a $0.05$ kg ball. Stored energy: $\frac12\cdot200\cdot0.01=1$ J. All of it becomes kinetic: $\frac12\cdot0.05\cdot v^2=1\Rightarrow v=\sqrt{40}\approx6.3$ m/s.

**Gravity.** Lifting a mass $m$ by a height $h$ against the constant force $mg$: $W=\int_0^hmg\,dy=mgh$ — gravitational potential energy.

## 3.4 The energy stored in a capacitor

**Build.** The same pattern with electrical quantities. To move a small charge $dq$ onto a capacitor that is already at voltage $v$ takes the work $v\,dq$ (voltage is energy per unit charge). And the voltage depends on the charge already there: $v=\dfrac qC$. So, charging from $0$ to $Q$:
$$W=\int_0^Q\frac qC\,dq=\frac{Q^2}{2C}=\frac12CV^2\qquad(\text{using }Q=CV).$$

| | "displacement" | "force" | stored energy |
|---|---|---|---|
| spring | stretch $x$ | $F=kx$ | $\frac12kx^2$ |
| capacitor | charge $q$ | $v=\frac qC$ | $\frac12\frac{q^2}{C}=\frac12CV^2$ |
| moving mass | (velocity $v$) | | $\frac12mv^2$ |

Three "halves of a square" — all the same integral $\int u\,du=\frac{u^2}{2}$, because in each case the effort grows in proportion to how much has already been done.

### Experiment 2 — energy in a simulation
A mass $m$ on a spring $k$, released from rest at $x_0$, simulated in small time steps. The cell tracks the spring energy $\frac12kx^2$, the kinetic energy $\frac12mv^2$, and their sum.

**Predict first:** what is the total energy for $k=25$, $x_0=1$? What is the maximum speed for $m=1$? Sketch the two energies against time.
''')
B.code(r'''
def energy(k=25.0, m=1.0, x0=1.0):
    dt, pos, vel = 0.0005, x0, 0.0
    ts, ke, pe = [], [], []
    for step in range(6000):
        vel = vel + (-k * pos / m) * dt        # acceleration from Hooke's law
        pos = pos + vel * dt
        ts.append(step * dt); ke.append(0.5 * m * vel**2); pe.append(0.5 * k * pos**2)
    ke, pe = np.array(ke), np.array(pe)
    plt.figure(figsize=(9, 3.5))
    plt.plot(ts, pe, label='spring energy ½kx²'); plt.plot(ts, ke, label='kinetic energy ½mv²'); plt.plot(ts, ke + pe, 'k--', label='total')
    plt.xlabel('t (s)'); plt.ylabel('energy (J)'); plt.legend(fontsize=9, loc='upper right'); plt.show()
    print(f'total energy = {np.mean(ke + pe):.3f} J     maximum speed = {sqrt(2 * ke.max() / m):.3f} m/s')

explore(energy, k=(5, 100, 5, 25), m=(0.5, 4, 0.5, 1), x0=(0.2, 2, 0.2, 1))
''')
B.md(r'''
*Explain:* the total stays at $\frac12kx_0^2=12.5$ J while the energy sloshes between spring and motion, twice per oscillation. Maximum speed from $\frac12mv^2=\frac12kx_0^2$: $v=x_0\sqrt{k/m}=5$ m/s — which is $A\omega$ with $\omega=\sqrt{k/m}$, the result of Unit 2 week 2 reached by a completely different route.
''')
B.ask(r'''A force $F(x)=6x$ newtons acts on a body as it moves from $x=0$ to $x=2$ m. How much work is done?''', 'num', 12,
      r'''$W=\displaystyle\int_0^26x\,dx=\big[3x^2\big]_0^2=12$ J.''',
      r'''$W=\int F\,dx$.''', fmt='joules')

# =====================================================================================
B.md(r'''
---
# Part 4 — Improper integrals

## 4.1 Integrating to infinity

**Why.** A discharging capacitor delivers current "for ever", ever more weakly. How much charge flows in total? A region can be infinitely long and still have a finite area — or not. We need a way to tell.

**Definition.**
$$\int_a^\infty f(x)\,dx=\lim_{b\to\infty}\int_a^bf(x)\,dx .$$
Integrate to a finite end $b$, **then** let $b\to\infty$. If the limit is a finite number the integral **converges**; otherwise it **diverges**. ($\infty$ is never "plugged in"; it is always a limit.)
''')
B.fig('improper', F.improper, 'The region is infinitely long, but its area is finite.')
B.md(r'''
**Worked example 1 (from your diagnostic).** $\displaystyle\int_0^\infty e^{-2x}\,dx$.
$$\int_0^be^{-2x}\,dx=\left[-\tfrac12e^{-2x}\right]_0^b=\tfrac12-\tfrac12e^{-2b}\ \xrightarrow[b\to\infty]{}\ \tfrac12-0=\tfrac12 .$$
Converges, to $\frac12$. In general $\displaystyle\int_0^\infty e^{-kx}\,dx=\frac1k$ for $k>0$.

**Worked example 2.** $\displaystyle\int_1^\infty\frac{1}{x^2}\,dx=\lim_{b\to\infty}\left[-\frac1x\right]_1^b=\lim_{b\to\infty}\left(1-\frac1b\right)=1$. Converges.

**Worked example 3.** $\displaystyle\int_1^\infty\frac1x\,dx=\lim_{b\to\infty}\big[\ln x\big]_1^b=\lim_{b\to\infty}\ln b=\infty$. **Diverges** — although $\frac1x\to0$.

**The lesson of examples 2 and 3: the integrand going to zero is not enough. It must go to zero fast enough.** $\frac1x$ is the borderline:
$$\int_1^\infty\frac{1}{x^p}\,dx\quad\begin{cases}\text{converges, to }\dfrac{1}{p-1}, & \text{if }p>1\\[4pt]\text{diverges} & \text{if }p\le1 .\end{cases}$$
(For $p\ne1$: $\left[\frac{x^{1-p}}{1-p}\right]_1^b$, and $b^{1-p}\to0$ exactly when $p>1$.) You will meet this same borderline next unit, for infinite *series*.

**Worked example 4 — with integration by parts.** $\displaystyle\int_0^\infty x\,e^{-x}\,dx$. Antiderivative ($u=x$, $v'=e^{-x}$): $-x\,e^{-x}-e^{-x}=-(x+1)e^{-x}$.
$$\big[-(x+1)e^{-x}\big]_0^b=1-\frac{b+1}{e^b}\ \xrightarrow[b\to\infty]{}\ 1,$$
because $\frac{b+1}{e^b}\to0$ (exponentials beat powers — L'Hôpital, Unit 2 week 4).

### Experiment 3 — converge or diverge?
The cell tabulates $\displaystyle\int_1^b\frac{dx}{x^p}$ for growing $b$ and three values of $p$.

**Predict first:** which columns settle down, and to what?
''')
B.code(r'''
rows = []
for bb in [10, 100, 1000, 1e4, 1e6, 1e9]:
    rows.append([bb, 2 * (sqrt(bb) - 1), ln(bb), 1 - 1 / bb])
table(['b', 'p = 1/2:  2(√b − 1)', 'p = 1:  ln b', 'p = 2:  1 − 1/b'], rows, fmt='%.6g')
''')
B.md(r'''
*Explain:* $p=2$ settles at 1. $p=1$ keeps growing — slowly ($\ln10^9\approx20.7$), but without bound: a table can make a divergent integral *look* convergent. $p=\frac12$ diverges quickly.

## 4.2 When the integrand blows up

The other kind of improper integral: a finite interval, but the function is unbounded at an end. Same idea — stop short and take a limit.
$$\int_0^1\frac{dx}{\sqrt{x}}=\lim_{a\to0^+}\big[2\sqrt{x}\big]_a^1=\lim_{a\to0^+}\big(2-2\sqrt{a}\big)=2 .$$
Converges: an infinitely tall spike with finite area. But $\displaystyle\int_0^1\frac{dx}{x}=\lim_{a\to0^+}(-\ln a)=\infty$ diverges. Near $0$ the roles are reversed: $\frac{1}{x^p}$ is integrable at $0$ when $p<1$.

## 4.3 Application: a discharging capacitor

A capacitor $C$ charged to $V_0$ discharges through a resistor $R$. The current is $i(t)=\dfrac{V_0}{R}e^{-t/RC}$ (you will derive this in Unit 5). The total charge that flows:
$$Q=\int_0^\infty\frac{V_0}{R}\,e^{-t/RC}\,dt=\frac{V_0}{R}\cdot RC=CV_0 .$$
(Using $\int_0^\infty e^{-kt}dt=\frac1k$ with $k=\frac{1}{RC}$.) Exactly the charge that was stored, $Q=CV_0$ — as it must be. The discharge takes "for ever", yet the total is finite.
''')
B.ask(r'''Evaluate $\displaystyle\int_0^\infty e^{-5x}\,dx$.''', 'num', 0.2,
      r'''$\left[-\frac15e^{-5x}\right]_0^b=\frac15-\frac15e^{-5b}\to\frac15$.''',
      r'''$\int_0^\infty e^{-kx}\,dx=\dfrac1k$.''')
B.ask(r'''Does $\displaystyle\int_1^\infty\frac{dx}{x^{1.5}}$ converge? If so, to what value?''', 'num', 2,
      r'''$p=1.5>1$: converges to $\dfrac{1}{p-1}=2$. Directly: $\left[-2x^{-1/2}\right]_1^b=2-\dfrac{2}{\sqrt b}\to2$.''',
      r'''$p>1$, so it converges to $\dfrac{1}{p-1}$.''')

B.md(r'''
## Week summary — everything on one page

**The pattern.** Slice → approximate one piece → add → limit. Write the thin piece with a $dx$, put $\int$ in front.

| quantity | thin piece | integral |
|---|---|---|
| area between curves | $(\text{top}-\text{bottom})\,dx$ | $\int_a^b[f-g]\,dx$ |
| disc area | ring $2\pi\rho\,d\rho$ | $\pi r^2$ |
| volume of revolution | disc $\pi y^2\,dx$ | $\int_a^b\pi[f(x)]^2dx$; ball $\frac43\pi r^3$; cone $\frac13\pi r^2h$ |
| average value | | $\frac{1}{b-a}\int_a^bf\,dx$ |
| RMS | | $\sqrt{\frac1T\int_0^Tv^2\,dt}$; sinusoid $\frac{V}{\sqrt2}$ |
| work | $F\,dx$ | $\int F\,dx$; spring $\frac12kx^2$; $\Delta\left(\frac12mv^2\right)$; capacitor $\frac12CV^2$ |
| charge | $i\,dt$ | $\int i\,dt$ |

**Improper integrals.** $\int_a^\infty f=\lim_{b\to\infty}\int_a^bf$. $\int_0^\infty e^{-kx}dx=\frac1k$. $\int_1^\infty\frac{dx}{x^p}$ converges iff $p>1$ (to $\frac{1}{p-1}$).
''')

# =====================================================================================
B.md(r'''
---
# Problems

Paper first; check with `nint`. First attempt counts. `hint(n)` → `solution(n)` → `mistake(n, '...')`.

### Areas and volumes
''')
B.problem(S1, r'Find the area enclosed between $y=x$ and $y=x^2$. *(From your diagnostic.)*', 'num', 1 / 6,
          [r'They cross at $x=0$ and $x=1$; the line is on top.'],
          r'''$$A=\int_0^1(x-x^2)\,dx=\left[\frac{x^2}{2}-\frac{x^3}{3}\right]_0^1=\frac12-\frac13=\frac16 .$$''', fmt='a number, e.g. `1/6`')
B.problem(S1, r'Find the area enclosed between $y=x^2$ and $y=2x+3$.', 'num', 32 / 3,
          [r'Crossings: $x^2-2x-3=(x-3)(x+1)=0$.', r'$\int_{-1}^3(2x+3-x^2)\,dx$.'],
          r'''Crossings $x=-1,\ 3$; at $x=0$ the line (3) is above the parabola (0).
$$\int_{-1}^{3}(2x+3-x^2)\,dx=\left[x^2+3x-\frac{x^3}{3}\right]_{-1}^{3}=(9+9-9)-\left(1-3+\frac13\right)=9+\frac53=\frac{32}{3}.$$''', fmt='a number, e.g. `32/3`')
B.problem(S1, r'Find the area between $y=\cos x$ and $y=\sin x$ for $0\le x\le\dfrac\pi4$.', 'num', math.sqrt(2) - 1,
          [r'On this interval the cosine is on top.', r'$\big[\sin x+\cos x\big]_0^{\pi/4}$.'],
          r'''$$\int_0^{\pi/4}(\cos x-\sin x)\,dx=\big[\sin x+\cos x\big]_0^{\pi/4}=\sqrt2-1\approx0.414 .$$''', fmt='a number; you can type `sqrt(2)-1`')
B.problem(S1, r'The region under $y=x^2$ from $x=0$ to $x=1$ is rotated about the $x$-axis. Find the volume.', 'num', math.pi / 5,
          [r'$V=\int_0^1\pi(x^2)^2\,dx$.'],
          r'''$$V=\int_0^1\pi x^4\,dx=\frac\pi5\approx0.628 .$$''', fmt='a number; you can type `pi/5`')
B.problem(S1, r'A cone has base radius $3$ and height $4$. Compute its volume **by integrating discs** (rotate $y=\frac34x$, $0\le x\le4$).', 'num', 12 * math.pi,
          [r'$V=\int_0^4\pi\left(\frac34x\right)^2dx$.'],
          r'''$$V=\int_0^4\pi\,\frac{9}{16}x^2\,dx=\frac{9\pi}{16}\cdot\frac{64}{3}=12\pi\approx37.7 .$$
Check: $\frac13\pi r^2h=\frac13\pi\cdot9\cdot4$ ✓.''', fmt='a number; you can type `12*pi`')
B.md(r'''
### Average and RMS
''')
B.problem(S2, r'What is the average value of $f(x)=\sqrt{x}$ on $[0,9]$?', 'num', 2,
          [r'$\frac19\int_0^9x^{1/2}\,dx$.'],
          r'''$$\frac19\left[\tfrac23x^{3/2}\right]_0^9=\frac19\cdot18=2 .$$''')
B.problem(S2, r'What is the average value of $\sin x$ over the half period $[0,\pi]$?', 'num', 2 / math.pi,
          [r'$\frac1\pi\int_0^\pi\sin x\,dx$.'],
          r'''$\dfrac1\pi\cdot2=\dfrac2\pi\approx$ **0.637**.''', fmt='a number; you can type `2/pi`')
B.problem(S2, r'A voltage is $v(t)=10\sin(\omega t)$ volts. What is its RMS value?', 'num', 10 / math.sqrt(2),
          [r'For a sinusoid: peak divided by $\sqrt2$.'],
          r'''$V_{\text{rms}}=\dfrac{10}{\sqrt2}\approx$ **7.07 V**.''', fmt='volts')
B.problem(S2, r'A ramp voltage rises as $v(t)=t$ for $0\le t\le1$ (one period of a sawtooth with peak 1). What is its RMS value?', 'num', 1 / math.sqrt(3),
          [r'Mean square: $\frac11\int_0^1t^2\,dt$. Then the root.'],
          r'''Mean of the square: $\displaystyle\int_0^1t^2\,dt=\frac13$. RMS $=\dfrac{1}{\sqrt3}\approx$ **0.577**.

(So a sawtooth or triangle of peak $V$ has RMS $\frac{V}{\sqrt3}$, less than a sine's $\frac{V}{\sqrt2}$: it spends more of its time near zero.)''')
B.md(r'''
### Work and energy
''')
B.problem(S3, r'A spring has stiffness $k=200$ N/m. How much work (J) is needed to stretch it from its natural length by $0.1$ m?', 'num', 1,
          [r'$W=\int_0^{0.1}kx\,dx=\frac12kx^2$.'],
          r'''$W=\frac12\cdot200\cdot0.1^2=$ **1 J**.''', fmt='joules')
B.problem(S3, r'The same spring ($k=200$ N/m): how much **additional** work to stretch it from $0.1$ m to $0.2$ m?', 'num', 3,
          [r'$\int_{0.1}^{0.2}200x\,dx$ — not the same as the first 0.1 m.'],
          r'''$$\int_{0.1}^{0.2}200x\,dx=\big[100x^2\big]_{0.1}^{0.2}=4-1=3\ \text{J}.$$
Three times the work of the first 10 cm: the force is larger the whole way.''', fmt='joules')
B.problem(S3, r'A $2$ kg body starts from rest and is pushed by the force $F(x)=6x$ N from $x=0$ to $x=2$ m. What is its final speed (m/s)?', 'num', math.sqrt(12),
          [r'Work–energy theorem: $\int F\,dx=\frac12mv^2$.', r'$W=12$ J, so $\frac12\cdot2\cdot v^2=12$.'],
          r'''$W=\displaystyle\int_0^26x\,dx=12$ J $=\frac12mv^2=v^2$, so $v=\sqrt{12}\approx$ **3.46 m/s**.''', fmt='m/s')
B.problem(S3, r'How much energy (in joules) is stored in a $100\ \mu$F capacitor charged to $12$ V?', 'num', 0.0072,
          [r'$\frac12CV^2$ with $C=10^{-4}$ F.'],
          r'''$\frac12\cdot10^{-4}\cdot144=7.2\times10^{-3}$ J $=$ **7.2 mJ**.''', fmt='joules')
B.md(r'''
### Improper integrals
''')
B.problem(S4, r'$\displaystyle\int_0^{\infty}e^{-2x}\,dx$ *(from your diagnostic)*', 'num', 0.5,
          [r'Integrate to $b$, then let $b\to\infty$.'],
          r'''$$\left[-\tfrac12e^{-2x}\right]_0^b=\tfrac12-\tfrac12e^{-2b}\to\tfrac12 .$$''')
B.problem(S4, r'$\displaystyle\int_1^{\infty}\frac{dx}{x^3}$', 'num', 0.5,
          [r'$\left[-\frac{1}{2x^2}\right]_1^b$.'],
          r'''$$\left[-\frac{1}{2x^2}\right]_1^b=\frac12-\frac{1}{2b^2}\to\frac12\qquad\left(=\frac{1}{p-1}\text{ with }p=3\right).$$''')
B.problem(S4, r'$\displaystyle\int_0^{\infty}x\,e^{-x}\,dx$', 'num', 1,
          [r'By parts: antiderivative $-(x+1)e^{-x}$.'],
          r'''$$\big[-(x+1)e^{-x}\big]_0^b=1-\frac{b+1}{e^b}\to1 .$$''')
B.problem(S4, r'$\displaystyle\int_0^{4}\frac{dx}{\sqrt{x}}$ (the integrand is unbounded at 0)', 'num', 4,
          [r'$\big[2\sqrt{x}\big]_a^4$, then $a\to0^+$.'],
          r'''$$\big[2\sqrt{x}\big]_a^4=4-2\sqrt{a}\to4 .$$''')
B.problem(S4, r'A discharging capacitor gives the current $i(t)=2e^{-4t}$ mA ($t$ in seconds). How much charge (in **mC**) flows in total, from $t=0$ for ever?', 'num', 0.5,
          [r'$Q=\int_0^\infty i\,dt$ and $\int_0^\infty e^{-kt}dt=\frac1k$.'],
          r'''$$Q=\int_0^\infty2e^{-4t}\,dt=\frac24=0.5\ \text{mC}.$$''', fmt='millicoulombs')
B.code(r'''
# scratch cell: e.g.  nint(lambda v: v - v**2, 0, 1)
''')

B.md(r'''
---
# Finish the week — and the unit

### 1 · Report
''')
B.code(r'''
report()
''')
B.md(r'''
### 2 · Teach-back (30 minutes, from memory)
1. The four-step pattern, shown on the volume of a ball.
2. Derive the area of a disc from its circumference.
3. What is an RMS value, and why is it $\frac{V}{\sqrt2}$ for a sinusoid?
4. Derive $\frac12mv^2$ from $F=ma$ and $W=\int F\,dx$.
5. Why does $\int_1^\infty\frac{dx}{x}$ diverge although $\frac1x\to0$?

*Your answers:*

&nbsp;

### 3 · Physics strand — energy in the oscillator (1 hour)
The simulator shows the mass on a spring of Experiment 2 ($k=25$ N/m, $m=1$ kg, released at $1$ m). Look at the third plot: kinetic, spring and total energy.

**Predict first:** the total (you computed it). How many times per oscillation does the kinetic energy peak? Now add damping ($c=0.4$): **predict** the shape of the total-energy curve — and where the energy goes — before you look.
''')
B.code(r'''
lab('physics', exp='osc', F0=0, c=0, x0=1, k=25, m=1)
''')
B.md(r'''
### 4 · Unit 3 review
Run `report()` in the three notebooks of this unit, or look at the course map. Every week at ≥ 80 % first time → **Unit 4 (series)**. Typical weak spots to tell your tutor: forgetting to change the limits after a substitution; sign errors in integration by parts; integrating "bottom − top"; plugging in $\infty$ instead of taking a limit.

**What comes next.** You have been using approximations such as $\sin x\approx x$ and $e^x\approx1+x$, and twice a second term appeared ($e^x\approx1+x+\frac{x^2}{2}$, $\sin x\approx x-\frac{x^3}{6}$). Unit 4 finds the complete pattern: every reasonable function is an **infinite polynomial**. That needs a careful look at what it means to add infinitely many numbers.
''')

if __name__ == '__main__':
    B.write()
