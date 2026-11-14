# Personal University of Engineering & Science

A self-built, browser-based curriculum: a course map, in-browser Jupyter notebooks (JupyterLite + Pyodide), and interactive simulators.

## Run it
Static site, no build step for the hub and labs:

    python -m http.server 5178 --directory .

Open http://localhost:5178/

| Path | What |
|---|---|
| `index.html` | Hub: course map, progress tracking, diagnostic result |
| `learn/curriculum.js` | Course map data (edit to reshape the curriculum) |
| `learn/tools/units/` | **Notebook sources**: one Python file per weekly notebook (`u01w1.py` …) plus the figure code |
| `learn/tools/nbkit.py`, `unilib.py` | Notebook generator kit, and the runtime embedded in every notebook (`check`, `hint`, `solution`, `ask`, `report`, `explore`, `lab`) |
| `learn/tools/build_notebooks.py`, `test_notebooks.py`, `build.sh` | Generate the notebooks, test them, build the JupyterLite site |
| `learn/content/` | Notebook contents served by JupyterLite (unit notebooks are generated here, not committed) |
| `voltaic/` | Circuit simulator (MNA engine, ESP32/Arduino part, Theory panel, CSV export). Sketches are **Arduino C++ (a teaching subset)** translated to JavaScript by `voltaic/cpp.js` — not compiled; tests: `node voltaic/test/cpp.test.js` |
| `robotics/` | Robotics lab (2R arm, PID, IK) |
| `physics/` | Physics lab (6 experiments) |
| `shared/theory.js` | Reusable KaTeX + SVG Theory panel |

## Build the in-browser notebooks
`learn/notebooks/` (the JupyterLite site) is not committed; GitHub Actions builds and deploys it on every push to `main`. To build locally:

    python -m venv jl
    jl/bin/pip install jupyterlite-core==0.8.7 jupyterlite-pyodide-kernel==0.8.7 jupyter-server nbformat sympy numpy matplotlib ipywidgets==8.1.9 nbclient ipykernel
    JL=jl/bin sh learn/tools/build.sh          # on Windows: JL=jl/Scripts
    jl/bin/python learn/tools/test_notebooks.py

Notes: edits you make in JupyterLite live in browser storage (use File > Download); once you have saved a notebook, your saved copy shadows later updates of that file. First start downloads ~30 MB.

## How a notebook is built (the teaching standard)
Each weekly notebook is written from first principles, in the same six steps per topic:
**Why** (the question that forces the idea) → **Build** (numbered steps, each with its reason; no skipped algebra) → **Worked examples** (every line) → **Check yourself** (`ask(n, …)`: unlimited tries, explains the answer) → **Experiment** (predict → run → explain; sliders via `explore`, simulators embedded via `lab`) → **Problems** (`check(n, …)`: first attempt counts; `hint(n)` gives progressive hints, `solution(n)` the full worked solution).

To add a notebook: copy a file in `learn/tools/units/`, add its module name to `UNITS` in `build_notebooks.py` and an entry in `learn/curriculum.js`. `test_notebooks.py` runs every notebook twice with a real kernel — untouched (must not raise) and with the answer key filled in (every `check`/`ask` must pass) — so a wrong answer key or a broken experiment cannot ship.

Results are saved per notebook as `<id>-results.json` in the browser; the hub reads them and shows the scores on the course map. The labs accept deep links, e.g. `physics/index.html#exp=osc&F0=0&c=0`.

## Curriculum
Year 1: Term 0 diagnostic, Term 1 calculus rebuilt, Term 2 ODEs / linear algebra / dynamics, Term 3 circuits & signals. See `learn/curriculum.js`.

## Install as an app (PWA)
Open the hub in Chrome or Edge (from `http://localhost:5178/` or any https host) and choose **Install** in the address bar. The hub and the three labs then work offline, including the maths typesetting (KaTeX). The notebooks work offline after you have opened a notebook once while online: JupyterLite caches itself and the Python runtime as it loads (`jupyter-lite.json` sets `enableServiceWorkerCache`).

- `manifest.webmanifest`, `sw.js`, `shared/pwa.js`, `icons/` (regenerate with `learn/tools/make_icons.py`).
- After changing app files, bump `VERSION` in `sw.js` so installed copies refresh (they also refresh in the background on the next visit).

## Password gate
The deployed site shows a password screen (`shared/gate.js`) before any page. It is a **soft gate**: GitHub Pages serves static files, so it keeps visitors and search engines out of the interface but does not hide direct file URLs.
- The committed `gate.js` is switched off (empty hash). The deploy workflow runs `learn/tools/make_gate.py`, which writes a salted PBKDF2 hash of the repository secret `SITE_PASSWORD` into the deployed copy and adds the script to every notebook page. The password itself is never in the repo or the site.
- Set or change the password: GitHub → Settings → Secrets and variables → Actions → `SITE_PASSWORD`, then re-run the *Deploy to GitHub Pages* workflow. Everyone is asked again.
- Without the secret the workflow warns and deploys ungated. The hub has a **Lock** button to forget the password in the current browser.
