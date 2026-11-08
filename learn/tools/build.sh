#!/bin/sh
# Rebuild the in-browser Jupyter environment and regenerate notebooks.
# Needs a venv with: jupyterlite-core jupyterlite-pyodide-kernel jupyter-server nbformat sympy numpy
# usage:  JL=path/to/venv/Scripts sh learn/tools/build.sh   (run from the project root)
$JL/python learn/tools/make_diagnostic.py
$JL/python learn/tools/make_u01.py
rm -rf learn/notebooks
$JL/jupyter-lite build --contents learn/content --output-dir learn/notebooks
