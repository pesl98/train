/* Soft password gate. Include FIRST in <head> of every page.
   - Shows a password prompt and keeps the page hidden until the right password is entered.
   - The password itself is never stored: only a salted PBKDF2-SHA256 hash. SALT/HASH below are empty in git;
     the deploy workflow fills them in from the repository secret SITE_PASSWORD (learn/tools/make_gate.py).
   - With an empty HASH the gate is off (local development).
   - SOFT gate: a static site cannot truly protect its files. This keeps casual visitors and search engines out of the UI. */
(function () {
  var SALT = '', HASH = '', ITER = 200000, KEY = 'pu.gate.v1';
  var api = window.PUGate = { active: !!HASH, lock: function () { try { localStorage.removeItem(KEY); } catch (e) { } location.reload(); } };
  if (!HASH) return;
  var tag = HASH.slice(0, 16);
  try { var s = JSON.parse(localStorage.getItem(KEY)); if (s && s.ok && s.h === tag) return; } catch (e) { }

  var hide = document.createElement('style'); hide.id = 'pu-gate-hide'; hide.textContent = 'html{visibility:hidden!important}';
  document.documentElement.appendChild(hide);

  function hex(buf) { return Array.prototype.map.call(new Uint8Array(buf), function (b) { return ('0' + b.toString(16)).slice(-2); }).join(''); }
  function unhex(h) { var a = new Uint8Array(h.length / 2); for (var i = 0; i < a.length; i++) a[i] = parseInt(h.substr(2 * i, 2), 16); return a; }
  async function derive(pw) {
    var k = await crypto.subtle.importKey('raw', new TextEncoder().encode(pw), 'PBKDF2', false, ['deriveBits']);
    return hex(await crypto.subtle.deriveBits({ name: 'PBKDF2', hash: 'SHA-256', salt: unhex(SALT), iterations: ITER }, k, 256));
  }

  function build() {
    var box = document.createElement('div'); box.id = 'pu-gate';
    box.setAttribute('style', 'visibility:visible;position:fixed;inset:0;z-index:2147483647;display:grid;place-items:center;background:#080b17;color:#e8ebff;font:15px/1.5 Inter,"Segoe UI",system-ui,sans-serif');
    box.innerHTML = '<form style="width:min(340px,88vw);padding:26px 26px 22px;border:1px solid rgba(255,255,255,.18);border-radius:16px;background:#10152b">' +
      '<div style="font-size:22px;font-weight:700;margin-bottom:4px;background:linear-gradient(90deg,#22d3ee,#a78bfa);-webkit-background-clip:text;background-clip:text;color:transparent">Personal University</div>' +
      '<div style="color:#8a93b8;margin-bottom:16px;font-size:13.5px">This site is private. Enter the password to continue.</div>' +
      '<input type="password" autocomplete="current-password" placeholder="Password" style="width:100%;box-sizing:border-box;padding:10px 12px;border-radius:10px;border:1px solid rgba(255,255,255,.25);background:#0a0e1d;color:#e8ebff;font:inherit">' +
      '<button type="submit" style="margin-top:12px;width:100%;padding:10px;border:0;border-radius:10px;background:linear-gradient(135deg,#4f46e5,#0ea5e9);color:#fff;font:inherit;font-weight:600;cursor:pointer">Unlock</button>' +
      '<div class="msg" style="min-height:20px;margin-top:10px;color:#f87171;font-size:13px"></div></form>';
    document.body.appendChild(box);
    var form = box.querySelector('form'), inp = box.querySelector('input'), msg = box.querySelector('.msg'), btn = box.querySelector('button'), fails = 0;
    inp.focus();
    form.onsubmit = async function (e) {
      e.preventDefault(); if (btn.disabled) return;
      btn.disabled = true; msg.textContent = '';
      var ok = false;
      try { ok = (await derive(inp.value)) === HASH; } catch (err) { msg.textContent = 'This browser cannot check the password (needs https).'; btn.disabled = false; return; }
      if (ok) {
        try { localStorage.setItem(KEY, JSON.stringify({ ok: true, h: tag })); } catch (err) { }
        box.remove(); var h = document.getElementById('pu-gate-hide'); if (h) h.remove();
      } else {
        fails++; msg.textContent = 'Wrong password.'; inp.value = ''; inp.focus();
        setTimeout(function () { btn.disabled = false; }, Math.min(8000, 400 * Math.pow(2, fails - 1)));
      }
    };
  }
  if (document.body) build(); else document.addEventListener('DOMContentLoaded', build);
})();
