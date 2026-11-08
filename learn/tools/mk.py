"""Tiny helper to write .ipynb files from Python lists of cells."""
import nbformat as nbf, sys, os
def md(s): return nbf.v4.new_markdown_cell(s.strip('\n'))
def code(s): return nbf.v4.new_code_cell(s.strip('\n'))
def write(path, cells, title=None):
    nb = nbf.v4.new_notebook(); nb.cells = cells
    nb.metadata['kernelspec'] = {'name': 'python', 'display_name': 'Python (Pyodide)', 'language': 'python'}
    nb.metadata['language_info'] = {'name': 'python'}
    os.makedirs(os.path.dirname(path), exist_ok=True); nbf.write(nb, path)
