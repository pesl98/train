"""Execute every generated notebook twice with a real kernel:
  1. as the student first sees it (all answers still '...')   -> must run without any error
  2. with every answer filled in from the answer key           -> every check()/ask()/start() must say it is right,
     and every known-mistake (trap) answer must trigger its targeted explanation
usage:  python learn/tools/test_notebooks.py [book-id ...]"""
import os, sys, tempfile
import nbformat
from nbclient import NotebookClient
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from build_notebooks import load


def text_of(cell):
    out = []
    for o in cell.get('outputs', []):
        if o.output_type == 'stream': out.append(o.text)
        elif o.output_type in ('display_data', 'execute_result'):
            out.append(o.data.get('text/markdown', '') or o.data.get('text/plain', ''))
        elif o.output_type == 'error': out.append('ERROR ' + o.ename + ': ' + o.evalue)
    return '\n'.join(out)


def run(nb, tag):
    with tempfile.TemporaryDirectory() as d:
        NotebookClient(nb, timeout=180, kernel_name='python3', resources={'metadata': {'path': d}}, allow_errors=True).execute()
    bad = []
    for i, c in enumerate(nb.cells):
        if c.cell_type != 'code': continue
        txt = text_of(c)
        if 'ERROR ' in txt or 'Traceback' in txt: bad.append('%s: cell %d raised: %s\n      source: %s' % (tag, i, txt[-300:], c.source[:120]))
    return bad


def main():
    want, fails = sys.argv[1:], []
    for b in load():
        if want and b.id not in want: continue
        fails += run(b.notebook(), b.id + ' (blank)')
        nb = b.notebook(solved=True)
        ntrap = 0
        for kind, store, fn in (('q', b.Q, 'ask'), ('p', b.P, 'check')):
            for k, q in store.items():
                for val, _ in q.get('t') or []:
                    nb.cells.append(nbformat.v4.new_code_cell('# trap\n%s(%s, %r)' % (fn, k, val))); ntrap += 1
        fails += run(nb, b.id + ' (solved)')
        nq = np_ = ns = nt = 0
        for c in nb.cells:
            if c.cell_type != 'code': continue
            src, txt = c.source, text_of(c)
            if src.startswith('# trap'):
                nt += 1
                if 'Known mistake' not in txt: fails.append('%s: trap not recognised: %s -> %s' % (b.id, src[7:70], txt[:160]))
                continue
            if src.startswith('start('):
                ns += 1
                if '✓' not in txt: fails.append('%s: %s -> %s' % (b.id, src[:70], txt[:160]))
            elif src.startswith('ask('):
                nq += 1
                if '✓' not in txt: fails.append('%s: %s -> %s' % (b.id, src[:70], txt[:160]))
            elif src.startswith('check('):
                np_ += 1
                if '✓ Correct, first time' not in txt: fails.append('%s: %s -> %s' % (b.id, src[:70], txt[:160]))
            elif 'x' in src.split('=')[0].split() and src.strip().startswith(('x =', 't =')):
                fails.append('%s: a cell overwrites the symbol x or t: %s' % (b.id, src[:60]))
        # every problem and question must have been exercised
        if nq != len(b.Q) or np_ != len(b.P) or ns != len(b.S) or nt != ntrap:
            fails.append('%s: ran %d/%d asks, %d/%d checks, %d/%d starts, %d/%d traps' % (b.id, nq, len(b.Q), np_, len(b.P), ns, len(b.S), nt, ntrap))
        print('%-8s blank run ok, solved run: %d checks, %d asks, %d starts, %d traps' % (b.id, np_, nq, ns, nt))
    if fails:
        print('\nFAILURES\n' + '\n'.join(fails)); sys.exit(1)
    print('all notebooks pass')


if __name__ == '__main__':
    main()
