"""Notebook generator kit.

A unit file (learn/tools/units/*.py) builds a Book:

    B = Book('u01w1', 'Unit 1 · Week 1 - ...', 'year1/u01w1-....ipynb')
    B.md(r'''markdown''')                      # theory
    B.fig('name', draw, 'caption')             # a figure drawn at build time, stored inside the notebook
    B.code(r'''python''')                      # experiment the student runs
    B.ask(text, kind, answer, why, nudge)      # "check yourself": ungraded, unlimited tries, explains
    B.problem(section, text, kind, answer, hints=[...], solution=...)   # graded, first attempt counts
    B.write()

Answer kinds: num, sym (expression, given as a string), anti (antiderivative), set, tuple, choice, fn.
Every answer is also kept in B.answers so tests can replay the notebook with the right answers."""
import base64, io, json, os, sys
import nbformat as nbf

HERE = os.path.dirname(os.path.abspath(__file__))
OUT = os.path.join(HERE, '..', 'content')
BOOKS = []
FMT = {'num': 'a number', 'sym': "an expression as a string, e.g. `'cos(x)'`", 'set': 'a list of numbers, e.g. `[1, 2]`',
       'tuple': 'a tuple, e.g. `(1, 2)`', 'choice': "a letter as a string, e.g. `'b'`", 'anti': "an expression in `x` as a string",
       'fn': 'a Python function'}


class Book:
    def __init__(self, id, title, path):
        self.id, self.title, self.path = id, title, path
        self.cells, self.P, self.Q, self.secs, self.answers = [None], {}, {}, [], []
        self.nfig = 0
        BOOKS.append(self)

    # ---- plain cells
    def md(self, s):
        self.cells.append(nbf.v4.new_markdown_cell(s.strip('\n')))

    def code(self, s, ref=None):
        """A code cell. ref = replacement source used by the tests (for cells the student must complete)."""
        c = nbf.v4.new_code_cell(s.strip('\n'))
        if ref is not None: self.answers.append((len(self.cells), ref.strip('\n')))
        self.cells.append(c)

    def fig(self, name, draw, caption='', width=None):
        """draw() must build a matplotlib figure and return it. Stored as a PNG attachment (visible without running anything)."""
        import matplotlib
        matplotlib.use('Agg')
        import matplotlib.pyplot as plt
        fig = draw()
        buf = io.BytesIO(); fig.savefig(buf, format='png', dpi=110, bbox_inches='tight', facecolor='white'); plt.close(fig)
        fn = '%s.png' % name
        c = nbf.v4.new_markdown_cell('![%s](attachment:%s)' % (caption or name, fn) + ('\n\n*%s*' % caption if caption else ''))
        c['attachments'] = {fn: {'image/png': base64.b64encode(buf.getvalue()).decode()}}
        self.cells.append(c); self.nfig += 1

    # ---- questions
    def ask(self, text, kind, answer, why, nudge='', fmt=None, sample=None):
        """sample: for kind 'anti' (answer = the integrand) a correct antiderivative, used by the tests."""
        n = len(self.Q) + 1
        f = fmt or FMT[kind]
        self.Q[str(n)] = {'k': kind, 'a': answer, 'why': why.strip(), 'nudge': nudge.strip(), 'f': f}
        self.md('> **Check yourself %d.** %s\n>\n> *Answer:* %s' % (n, text.strip().replace('\n', '\n> '), f))
        self.code('ask(%d, ...)' % n, ref='ask(%d, %s)' % (n, _lit(kind, answer, sample)))

    def problem(self, sec, text, kind, answer, hints=(), solution='', fmt=None, ref=None, sample=None):
        n = len(self.P) + 1
        if sec not in self.secs: self.secs.append(sec)
        f = fmt or FMT[kind]
        assert solution.strip(), 'problem %d needs a worked solution' % n
        self.P[str(n)] = {'k': kind, 'a': answer, 'sec': sec, 'h': [h_.strip() for h_ in hints], 's': solution.strip(), 'f': f}
        self.md('**Problem %d.** %s\n\n*Answer:* %s' % (n, text.strip(), f))
        self.code('check(%d, ...)' % n, ref=ref or 'check(%d, %s)' % (n, _lit(kind, answer, sample)))

    # ---- output
    def setup_source(self):
        data = {'id': self.id, 'title': self.title, 'secs': self.secs, 'p': self.P, 'q': self.Q}
        lib = open(os.path.join(HERE, 'unilib.py'), encoding='utf-8').read()
        return ('# SETUP - run this cell first (Shift+Enter). You do not need to read it.\n'
                'try:\n    import piplite\n    await piplite.install(["ipywidgets"])\nexcept Exception:\n    pass\n'
                '_DATA = "%s"\n' % base64.b64encode(json.dumps(data).encode()).decode()
                + lib + "\nprint('Ready: %s.  Progress is saved in this browser as', _FILE)\n" % self.title.replace("'", ''))

    def notebook(self, solved=False):
        nb = nbf.v4.new_notebook()
        cells = [nbf.from_dict(dict(c)) if c is not None else None for c in self.cells]
        setup = nbf.v4.new_code_cell(self.setup_source())
        setup.metadata['jupyter'] = {'source_hidden': True}
        cells[0] = setup
        if solved:
            for i, src in self.answers: cells[i]['source'] = src
        # the title cell goes above the setup cell
        nb.cells = cells[1:2] + [cells[0]] + cells[2:]
        nb.metadata['kernelspec'] = {'name': 'python', 'display_name': 'Python (Pyodide)', 'language': 'python'}
        nb.metadata['language_info'] = {'name': 'python'}
        for k, c in enumerate(nb.cells): c['id'] = '%s-%03d' % (self.id, k)
        return nb

    def write(self):
        blob = json.dumps([self.P, self.Q]) + ''.join(c['source'] for c in self.cells if c is not None and c['cell_type'] == 'markdown')
        assert "\\\\'" not in blob and "\\'" not in blob, self.id + ": found \\' in text - use a double-quoted raw string instead of escaping the quote"
        p = os.path.join(OUT, self.path)
        os.makedirs(os.path.dirname(p), exist_ok=True)
        nbf.write(self.notebook(), p)
        print('%-52s %3d cells  %2d problems  %2d checks  %2d figures  %4d KB' % (
            self.path, len(self.cells), len(self.P), len(self.Q), self.nfig, os.path.getsize(p) // 1024))


def _lit(kind, a, sample=None):
    if kind == 'fn': raise ValueError('fn problems need an explicit ref=')
    if kind == 'anti':
        assert sample, "kind 'anti' needs sample= (a correct antiderivative) for the tests"
        return repr(sample)
    return repr(a)
