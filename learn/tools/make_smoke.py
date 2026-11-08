import sys; sys.path.insert(0, 'learn/tools')
from mk import *
write('learn/content/00-setup-check.ipynb', [
 md("# Setup check\nRun every cell (Shift+Enter). All should work without errors."),
 code("import numpy as np, sympy as sp\nprint('numpy', np.__version__, '| sympy', sp.__version__)"),
 code("x = sp.symbols('x')\nsp.integrate(sp.sin(x)**2, x)"),
 code("import matplotlib.pyplot as plt\nt = np.linspace(0, 2*np.pi, 200)\nplt.plot(t, np.sin(t)); plt.title('sin(t)'); plt.grid(True); plt.show()"),
])
