"""Switch on the password gate in an assembled site directory.

usage:  SITE_PASSWORD=... python learn/tools/make_gate.py _site

- writes a random salt and the PBKDF2-SHA256 hash of the password into <site>/shared/gate.js
- copies it to <site>/learn/notebooks/gate.js and adds a <script> tag to every JupyterLite index.html
Without SITE_PASSWORD it prints a warning and leaves the site ungated."""
import hashlib, os, re, secrets, sys

ITER = 200000
site = sys.argv[1] if len(sys.argv) > 1 else '_site'
pw = os.environ.get('SITE_PASSWORD', '')
if not pw:
    print('::warning::SITE_PASSWORD is not set - the site is deployed WITHOUT a password gate')
    sys.exit(0)

salt = secrets.token_bytes(16)
digest = hashlib.pbkdf2_hmac('sha256', pw.encode('utf-8'), salt, ITER, 32).hex()
path = os.path.join(site, 'shared', 'gate.js')
src = open(path, encoding='utf-8').read()
new = src.replace("var SALT = '', HASH = ''", "var SALT = '%s', HASH = '%s'" % (salt.hex(), digest), 1)
assert new != src, 'gate.js placeholders not found'
open(path, 'w', encoding='utf-8').write(new)

nb = os.path.join(site, 'learn', 'notebooks')
open(os.path.join(nb, 'gate.js'), 'w', encoding='utf-8').write(new)
count = 0
for root, _, files in os.walk(nb):
    for f in files:
        if f != 'index.html': continue
        p = os.path.join(root, f)
        html = open(p, encoding='utf-8').read()
        if 'gate.js' in html: continue
        rel = os.path.relpath(os.path.join(nb, 'gate.js'), root).replace(os.sep, '/')
        tag = '<script src="%s"></script>' % rel
        out, n = re.subn(r'(<head[^>]*>)', lambda m: m.group(1) + tag, html, count=1)
        if n:
            open(p, 'w', encoding='utf-8').write(out); count += 1
print('gate enabled: %d notebook pages patched' % count)
