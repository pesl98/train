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
| `learn/content/` | Source notebooks (`year1/w00-diagnostic`, `year1/u01-functions-trig-limits`, setup check) |
| `learn/tools/` | Notebook generators (`make_*.py`) and `build.sh` |
| `voltaic/` | Circuit simulator (MNA engine, ESP32/Arduino part, Theory panel, CSV export) |
| `robotics/` | Robotics lab (2R arm, PID, IK) |
| `physics/` | Physics lab (6 experiments) |
| `shared/theory.js` | Reusable KaTeX + SVG Theory panel |

## Build the in-browser notebooks
`learn/notebooks/` (the JupyterLite site) is not committed; build it once:

    python -m venv jl && jl/Scripts/pip install jupyterlite-core jupyterlite-pyodide-kernel jupyter-server nbformat sympy numpy
    JL=jl/Scripts sh learn/tools/build.sh

Notes: edits you make in JupyterLite live in browser storage (use File > Download); a changed notebook needs a new filename or it is shadowed by an edited copy. First start downloads ~30 MB.

## Curriculum
Year 1: Term 0 diagnostic, Term 1 calculus rebuilt, Term 2 ODEs / linear algebra / dynamics, Term 3 circuits & signals. See `learn/curriculum.js`.
