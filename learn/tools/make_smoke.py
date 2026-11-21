import sys; sys.path.insert(0, 'learn/tools')
from mk import *
write('learn/content/00-setup-check.ipynb', [
 md("# Setup check\nRun every cell (Shift+Enter). All should work without errors."),
 code("import numpy as np, sympy as sp\nprint('numpy', np.__version__, '| sympy', sp.__version__)"),
 code("x = sp.symbols('x')\nsp.integrate(sp.sin(x)**2, x)"),
 code("import matplotlib.pyplot as plt\nt = np.linspace(0, 2*np.pi, 200)\nplt.plot(t, np.sin(t)); plt.title('sin(t)'); plt.grid(True); plt.show()"),
 md(r'''
## Installing packages

These notebooks run Python **inside your browser** (Pyodide) — there is no server. Some packages are always available; others you install yourself.

**Already there — just import them:** `numpy`, `sympy`, `matplotlib` (every course notebook loads them in its SETUP cell), and `ipywidgets` for the sliders.

**Anything else:** run, in a code cell,
```python
%pip install pandas
```
then `import pandas` as usual. The same, written as Python:
```python
import piplite
await piplite.install('pandas')
```

**What can be installed**
- ✓ pure-Python packages from PyPI;
- ✓ scientific packages built for the browser: `pandas`, `scipy`, `scikit-learn`, `networkx`, `pillow`, … ([full list](https://pyodide.org/en/stable/usage/packages-in-pyodide.html));
- ✗ packages that need compiled code not built for Pyodide, e.g. `torch`, `tensorflow`.

**An install does not stay.** It lasts until the kernel restarts or the page reloads. Put the `%pip install ...` line in the first cell of your notebook (after SETUP), so it runs every time.

Try it — the first install takes a few seconds (it downloads the package):
'''),
 code("%pip install pandas\nimport pandas as pd\ndf = pd.DataFrame({'R (ohm)': [100, 220, 470], 'V (V)': [5, 5, 5]})\ndf['I (mA)'] = df['V (V)'] / df['R (ohm)'] * 1000\ndf"),
 code("import piplite\nawait piplite.install('scipy')\nfrom scipy.integrate import quad\nval, err = quad(lambda u: np.exp(-u**2), -np.inf, np.inf)\nprint('integral of exp(-x^2) =', val, '   sqrt(pi) =', np.sqrt(np.pi))"),
])
