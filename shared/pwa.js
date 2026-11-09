/* Registers the service worker (offline support) from any page in the app.
   The path to sw.js is derived from this script's own URL, so it works at any depth and on any host path. */
(function () {
  if (!('serviceWorker' in navigator) || !/^(https:|http:\/\/(localhost|127\.0\.0\.1))/.test(location.protocol + '//' + location.hostname)) return;
  const me = document.currentScript && document.currentScript.src;
  if (!me) return;
  const root = new URL('../', me);
  window.addEventListener('load', () => {
    navigator.serviceWorker.register(new URL('sw.js', root), { scope: root.pathname }).catch(() => {});
  });
})();
