#!/bin/sh
# Regenerate the notebooks and rebuild the in-browser Jupyter environment (JupyterLite).
# Needs a venv with: jupyterlite-core jupyterlite-pyodide-kernel jupyter-server nbformat sympy numpy matplotlib ipywidgets
# usage:  JL=path/to/venv/bin sh learn/tools/build.sh   (run from the project root; on Windows JL=venv/Scripts)
set -e
$JL/python learn/tools/make_diagnostic.py
$JL/python learn/tools/build_notebooks.py
# ipywidgets (the sliders) is bundled with the site, so notebooks also work offline
W=learn/tools/.wheels
mkdir -p $W
[ -n "$(ls $W/ipywidgets-*.whl 2>/dev/null)" ] || $JL/python -m pip download -q --no-deps -d $W ipywidgets==8.1.9 jupyterlab_widgets==3.0.17
rm -rf learn/notebooks
$JL/jupyter-lite build --contents learn/content --output-dir learn/notebooks \
  --piplite-wheels="$(ls $W/ipywidgets-*.whl)" --piplite-wheels="$(ls $W/jupyterlab_widgets-*.whl)"
