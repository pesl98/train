/* Service worker for the Personal University PWA.
   - Precaches the app shell (hub, labs, shared code, icons) so they work offline.
   - Same-origin files: stale-while-revalidate (served from cache, refreshed in the background).
   - KaTeX (cdnjs): fetched at install and cached, so maths typesetting works offline.
   - /learn/notebooks/ is NOT handled here: JupyterLite registers its own service worker
     (with enableServiceWorkerCache) that caches the notebook app and the Pyodide runtime.
   Bump VERSION whenever you want clients to drop old caches. */
const VERSION = 'v1';
const SHELL = 'pu-shell-' + VERSION;
const EXT = 'pu-ext-' + VERSION;
const KATEX = 'https://cdnjs.cloudflare.com/ajax/libs/KaTeX/0.16.9/';
const PRECACHE = [
  './', 'index.html', 'manifest.webmanifest',
  'learn/curriculum.js', 'shared/theory.js',
  'voltaic/index.html', 'voltaic/style.css', 'voltaic/sim.js', 'voltaic/theory.js', 'voltaic/app.js',
  'robotics/index.html', 'robotics/app.js',
  'physics/index.html', 'physics/app.js',
  'icons/icon-192.png', 'icons/icon-512.png', 'icons/icon-maskable-512.png', 'icons/apple-touch-icon.png',
];

self.addEventListener('install', e => {
  e.waitUntil((async () => {
    const shell = await caches.open(SHELL);
    await shell.addAll(PRECACHE);
    // KaTeX is best effort: never fail the install because the CDN is unreachable.
    try {
      const ext = await caches.open(EXT);
      const cssRes = await fetch(KATEX + 'katex.min.css', { mode: 'cors' });
      const css = await cssRes.clone().text();
      await ext.put(KATEX + 'katex.min.css', cssRes);
      const js = await fetch(KATEX + 'katex.min.js', { mode: 'cors' });
      await ext.put(KATEX + 'katex.min.js', js);
      const fonts = [...new Set([...css.matchAll(/url\((fonts\/[^)]+?\.woff2)\)/g)].map(m => m[1]))];
      await Promise.all(fonts.map(async f => { try { await ext.put(KATEX + f, await fetch(KATEX + f, { mode: 'cors' })); } catch (_) {} }));
    } catch (_) {}
    self.skipWaiting();
  })());
});

self.addEventListener('activate', e => {
  e.waitUntil((async () => {
    for (const k of await caches.keys()) if (k !== SHELL && k !== EXT) await caches.delete(k);
    await self.clients.claim();
  })());
});

async function swr(req, cacheName, fallbackUrl) {
  const cache = await caches.open(cacheName);
  const hit = await cache.match(req, { ignoreSearch: true });
  const net = fetch(req).then(res => { if (res && (res.ok || res.type === 'opaque')) cache.put(req, res.clone()); return res; });
  if (hit) { net.catch(() => {}); return hit; }
  try { return await net; }
  catch (err) {
    if (fallbackUrl) { const f = await cache.match(fallbackUrl); if (f) return f; }
    throw err;
  }
}

self.addEventListener('fetch', e => {
  const req = e.request;
  if (req.method !== 'GET') return;
  const url = new URL(req.url);
  if (url.pathname.includes('/learn/notebooks/')) return;           // JupyterLite manages itself
  if (url.origin === location.origin) {
    e.respondWith(swr(req, SHELL, req.mode === 'navigate' ? 'index.html' : null));
  } else if (url.hostname === 'cdnjs.cloudflare.com') {
    e.respondWith(swr(req, EXT));
  }
});
