"""Generate every notebook from learn/tools/units/*.py into learn/content/.
usage:  python learn/tools/build_notebooks.py            (from the project root, with the build venv)"""
import importlib, os, sys
HERE = os.path.dirname(os.path.abspath(__file__))
sys.path[:0] = [HERE, os.path.join(HERE, 'units')]
UNITS = ['u01w1', 'u01w2', 'u01w3']


def load():
    import nbkit
    for u in UNITS:
        if os.path.exists(os.path.join(HERE, 'units', u + '.py')): importlib.import_module(u)
    return nbkit.BOOKS


if __name__ == '__main__':
    for b in load(): b.write()
