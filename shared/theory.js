/* Shared "Theory" panel for every laboratory.
 *
 *   Theory.open({ title, intro, focus, sections })
 *     focus / each section = { h, p, tex:[latex…], eq:'plain fallback', svg:'<svg…>', live:'text' }
 *   Theory.plot({ f | series, xr, yr, xl, yl, point, vlines, hlines, w, h })  -> SVG string
 *   Theory.fmt(v)                                                           -> short number string
 *
 * Maths is typeset with KaTeX (loaded from cdnjs; plain text is shown if it cannot load).
 * Colours follow the lab theme so diagrams match the app.
 */
(function () {
  const KV = '0.16.9', CDN = 'https://cdnjs.cloudflare.com/ajax/libs/KaTeX/' + KV + '/';
  const css = `
  #thy{position:fixed;inset:0;background:rgba(4,6,14,.74);display:none;place-items:center;z-index:1000;font:14px/1.55 Inter,"Segoe UI",system-ui,sans-serif}
  #thy.show{display:grid}
  #thy .tc{width:min(860px,95vw);max-height:90vh;overflow:auto;background:#10152b;color:#e8ebff;border:1px solid rgba(255,255,255,.18);border-radius:16px;padding:24px 30px 28px;box-shadow:0 24px 80px rgba(0,0,0,.55)}
  #thy h2{margin:0 0 4px;font-size:23px}
  #thy .lead{color:#9aa3c8;margin:0 0 4px}
  #thy .sec{margin-top:22px;padding-top:4px}
  #thy h5{margin:0 0 6px;font-size:12px;letter-spacing:1.3px;text-transform:uppercase;color:#22d3ee}
  #thy p{margin:4px 0 8px;color:#b6bdde}
  #thy .eq{margin:8px 0;padding:6px 14px;background:#0a0e1d;border:1px solid rgba(255,255,255,.07);border-radius:10px;overflow-x:auto;color:#eef0ff}
  #thy .eq .katex-display{margin:.45em 0}
  #thy .eq .katex{font-size:1.12em}
  #thy pre.fb{margin:6px 0;padding:10px 14px;background:#0a0e1d;border-radius:8px;font:12.5px/1.6 ui-monospace,Consolas,monospace;color:#d5dbff;white-space:pre-wrap}
  #thy .fig{margin:10px 0;padding:8px;background:#0a0e1d;border:1px solid rgba(255,255,255,.07);border-radius:10px;text-align:center}
  #thy .fig svg{max-width:100%;height:auto}
  #thy .fig.row{display:flex;gap:10px;flex-wrap:wrap;justify-content:center;background:transparent;border:0;padding:0}
  #thy .fig.row>div{flex:1 1 300px;background:#0a0e1d;border:1px solid rgba(255,255,255,.07);border-radius:10px;padding:8px;text-align:center}
  #thy .focus{border:1px solid rgba(124,140,255,.55);background:rgba(124,140,255,.07);border-radius:12px;padding:14px 18px 12px;margin:16px 0 0}
  #thy .focus h5{color:#a78bfa}
  #thy .live{font:12.5px ui-monospace,Consolas,monospace;color:#4ade80;margin-top:8px}
  #thy .x{float:right;background:rgba(255,255,255,.06);border:1px solid rgba(255,255,255,.14);color:inherit;border-radius:8px;height:30px;padding:0 12px;cursor:pointer;font:inherit}
  #thy .x:hover{background:rgba(255,255,255,.12)}
  #thy kbd{font:11px ui-monospace,monospace;background:rgba(255,255,255,.08);border-radius:4px;padding:0 5px}
  #thy svg text{font-family:Inter,"Segoe UI",system-ui,sans-serif}
  #thy .ax{stroke:#4a5486;stroke-width:1.2}#thy .gr{stroke:rgba(255,255,255,.07)}
  #thy .tk{fill:#8a93b8;font-size:10.5px}#thy .al{fill:#aab2d8;font-size:11.5px}
  #thy .sym{stroke:#cfd6ff;stroke-width:2;fill:none;stroke-linecap:round;stroke-linejoin:round}
  #thy .lb{fill:#e8ebff;font-size:13px}#thy .lbm{fill:#8a93b8;font-size:12px}`;
  const st = document.createElement('style'); st.textContent = css; document.head.appendChild(st);

  // KaTeX (async). `ready` resolves true/false.
  const ready = new Promise(res => {
    const l = document.createElement('link'); l.rel = 'stylesheet'; l.href = CDN + 'katex.min.css'; document.head.appendChild(l);
    const s = document.createElement('script'); s.src = CDN + 'katex.min.js'; s.onload = () => res(true); s.onerror = () => res(false); document.head.appendChild(s);
    setTimeout(() => res(!!window.katex), 6000);
  });

  const root = document.createElement('div'); root.id = 'thy'; root.innerHTML = '<div class="tc"></div>'; document.body.appendChild(root);
  const card = root.firstChild;
  const close = () => root.classList.remove('show');
  root.addEventListener('mousedown', e => { if (e.target === root) close(); });
  addEventListener('keydown', e => { if (e.key === 'Escape' && root.classList.contains('show')) { close(); e.stopPropagation(); } }, true);

  const esc = s => String(s).replace(/&/g, '&amp;').replace(/</g, '&lt;');
  function block(s) {
    let h = '';
    if (s.h) h += `<h5>${s.h}</h5>`;
    if (s.p) h += `<p>${s.p}</p>`;
    if (s.tex) h += s.tex.map(t => `<div class="eq" data-tex="${esc(t).replace(/"/g, '&quot;')}"></div>`).join('');
    else if (s.eq) h += `<pre class="fb">${esc(s.eq)}</pre>`;
    if (s.svg) h += Array.isArray(s.svg) ? `<div class="fig row">${s.svg.map(x => `<div>${x}</div>`).join('')}</div>` : `<div class="fig">${s.svg}</div>`;
    if (s.live) h += `<div class="live">${esc(s.live)}</div>`;
    return h;
  }
  function typeset() {
    card.querySelectorAll('.eq[data-tex]').forEach(el => {
      const t = el.getAttribute('data-tex');
      if (window.katex) { try { katex.render(t, el, { displayMode: true, throwOnError: false }); return; } catch (e) { } }
      el.innerHTML = `<pre class="fb" style="margin:0;background:none">${esc(t)}</pre>`;
    });
  }

  /* ---------------- SVG helpers ---------------- */
  function fmt(v) {
    if (v === 0) return '0'; const a = Math.abs(v);
    if (a >= 1e4 || a < 1e-2) { const e = Math.floor(Math.log10(a)), m = v / 10 ** e; return (Math.abs(m - Math.round(m)) < 1e-9 ? Math.round(m) : m.toFixed(1)) + 'e' + e; }
    return +v.toPrecision(3) + '';
  }
  function nice(lo, hi, n) {
    const span = hi - lo || 1, raw = span / n, p = 10 ** Math.floor(Math.log10(raw)), f = raw / p, step = (f < 1.5 ? 1 : f < 3.5 ? 2 : f < 7.5 ? 5 : 10) * p;
    const out = []; for (let v = Math.ceil(lo / step - 1e-9) * step; v <= hi + step * 1e-9; v += step) out.push(+v.toPrecision(12)); return out;
  }
  /* series: [{f:(x)=>y | pts:[[x,y]], col, dash, w, label}] */
  function plot(o) {
    const W = o.w || 380, H = o.h || 220, L = 52, R = 14, T = 12, B = 38, pw = W - L - R, ph = H - T - B;
    const ser = o.series || [{ f: o.f, col: '#22d3ee' }];
    const xr = o.xr, N = 160, data = ser.map(s => s.pts || Array.from({ length: N + 1 }, (_, i) => { const x = xr[0] + (xr[1] - xr[0]) * i / N; return [x, s.f(x)]; }));
    let yr = o.yr; if (!yr) { let lo = 1e30, hi = -1e30; data.forEach(d => d.forEach(p => { if (isFinite(p[1])) { lo = Math.min(lo, p[1]); hi = Math.max(hi, p[1]); } })); const pad = (hi - lo) * .08 || 1; yr = [lo - pad, hi + pad]; }
    const X = x => L + (x - xr[0]) / (xr[1] - xr[0]) * pw, Y = y => T + ph - (y - yr[0]) / (yr[1] - yr[0]) * ph;
    const cl = y => Math.max(yr[0], Math.min(yr[1], y));
    let s = `<svg viewBox="0 0 ${W} ${H}" width="${W}" role="img">`;
    const xt = o.xticks || nice(xr[0], xr[1], 5), yt = o.yticks || nice(yr[0], yr[1], 4);
    xt.forEach(v => { s += `<line class="gr" x1="${X(v)}" y1="${T}" x2="${X(v)}" y2="${T + ph}"/><text class="tk" x="${X(v)}" y="${T + ph + 14}" text-anchor="middle">${fmt(v)}</text>`; });
    yt.forEach(v => { s += `<line class="gr" x1="${L}" y1="${Y(v)}" x2="${L + pw}" y2="${Y(v)}"/><text class="tk" x="${L - 6}" y="${Y(v) + 3.5}" text-anchor="end">${fmt(v)}</text>`; });
    if (xr[0] < 0 && xr[1] > 0) s += `<line class="ax" x1="${X(0)}" y1="${T}" x2="${X(0)}" y2="${T + ph}"/>`;
    if (yr[0] < 0 && yr[1] > 0) s += `<line class="ax" x1="${L}" y1="${Y(0)}" x2="${L + pw}" y2="${Y(0)}"/>`;
    s += `<rect x="${L}" y="${T}" width="${pw}" height="${ph}" fill="none" class="ax"/>`;
    (o.vlines || []).forEach(v => { s += `<line x1="${X(v.x)}" y1="${T}" x2="${X(v.x)}" y2="${T + ph}" stroke="${v.col || '#fbbf24'}" stroke-dasharray="4 4" opacity=".8"/>` + (v.label ? `<text class="tk" x="${X(v.x) + 3}" y="${T + 10}" fill="${v.col || '#fbbf24'}">${v.label}</text>` : ''); });
    (o.hlines || []).forEach(v => { s += `<line x1="${L}" y1="${Y(v.y)}" x2="${L + pw}" y2="${Y(v.y)}" stroke="${v.col || '#fbbf24'}" stroke-dasharray="4 4" opacity=".8"/>` + (v.label ? `<text class="tk" x="${L + pw - 3}" y="${Y(v.y) - 3}" text-anchor="end" fill="${v.col || '#fbbf24'}">${v.label}</text>` : ''); });
    s += `<clipPath id="cp${W}${H}"><rect x="${L}" y="${T}" width="${pw}" height="${ph}"/></clipPath>`;
    ser.forEach((se, i) => {
      const d = data[i].filter(p => isFinite(p[1])).map((p, k) => (k ? 'L' : 'M') + X(p[0]).toFixed(1) + ' ' + Y(p[1]).toFixed(1)).join('');
      s += `<path d="${d}" clip-path="url(#cp${W}${H})" fill="none" stroke="${se.col || '#22d3ee'}" stroke-width="${se.w || 2.4}" ${se.dash ? 'stroke-dasharray="5 4"' : ''} stroke-linejoin="round"/>`;
      if (se.label) { const p = data[i][Math.floor(data[i].length * (se.at || .85))]; s += `<text class="tk" x="${X(p[0])}" y="${Y(cl(p[1])) - 6}" fill="${se.col}" text-anchor="middle">${se.label}</text>`; }
    });
    (o.points || (o.point ? [o.point] : [])).forEach(p => {
      const px = X(Math.max(xr[0], Math.min(xr[1], p[0]))), py = Y(cl(p[1]));
      s += `<circle cx="${px}" cy="${py}" r="9" fill="rgba(251,191,36,.18)"/><circle cx="${px}" cy="${py}" r="4.5" fill="#fbbf24" stroke="#10152b" stroke-width="1.5"/>`;
      if (p[2]) s += `<text class="tk" x="${Math.min(px + 10, L + pw - 40)}" y="${Math.max(py - 10, T + 12)}" fill="#fbbf24">${p[2]}</text>`;
    });
    if (o.xl) s += `<text class="al" x="${L + pw / 2}" y="${H - 5}" text-anchor="middle">${o.xl}</text>`;
    if (o.yl) s += `<text class="al" transform="translate(13 ${T + ph / 2}) rotate(-90)" text-anchor="middle">${o.yl}</text>`;
    if (o.title) s += `<text class="lb" x="${L + 8}" y="${T + 16}" font-size="12">${o.title}</text>`;
    return s + '</svg>';
  }

  window.Theory = {
    plot, fmt, nice, ready,
    open(o) {
      card.innerHTML = `<button class="x">Close <kbd>Esc</kbd></button><h2>${o.title || 'Theory'}</h2>` + (o.intro ? `<p class="lead">${o.intro}</p>` : '') +
        (o.focus ? `<div class="focus">${block(o.focus)}</div>` : '') + (o.sections || []).map(s => `<div class="sec">${block(s)}</div>`).join('');
      card.querySelector('.x').onclick = close; card.scrollTop = 0; root.classList.add('show');
      typeset(); ready.then(typeset);
    },
    close,
  };
})();
