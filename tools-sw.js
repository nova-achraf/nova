// PixShrink — Service Worker (PWA, offline-capable tools hub)
const CACHE = 'pixshrink-v1';
const ASSETS = [
  'tools.html',
  'tools-manifest.json',
  'pixshrink-icon-192.png',
  'pixshrink-icon-512.png',
  'pixshrink-maskable-512.png',
  'pixshrink-apple-icon.png',
  'compress.html',
  'resize-image.html',
  'webp-converter.html',
  'crop-image.html',
  'rotate-image.html',
  'image-to-pdf.html',
  'merge-pdf.html',
  'pdf-to-jpg.html',
  'passport-photo.html',
  'favicon-maker.html'
];

self.addEventListener('install', function (e) {
  e.waitUntil(
    caches.open(CACHE).then(function (c) {
      // individual adds: one 404 must not break the whole install
      return Promise.all(ASSETS.map(function (u) {
        return c.add(u).catch(function () {});
      }));
    }).then(function () { return self.skipWaiting(); })
  );
});

self.addEventListener('activate', function (e) {
  e.waitUntil(
    caches.keys().then(function (keys) {
      return Promise.all(keys.filter(function (k) { return k !== CACHE; })
        .map(function (k) { return caches.delete(k); }));
    }).then(function () { return self.clients.claim(); })
  );
});

self.addEventListener('fetch', function (e) {
  var req = e.request;
  if (req.method !== 'GET') return;

  // HTML: network-first so updates land immediately, cache as offline fallback
  if (req.mode === 'navigate') {
    e.respondWith(
      fetch(req).then(function (res) {
        var copy = res.clone();
        caches.open(CACHE).then(function (c) { c.put(req, copy); });
        return res;
      }).catch(function () {
        return caches.match(req).then(function (hit) {
          return hit || caches.match('tools.html');
        });
      })
    );
    return;
  }

  // Everything else (icons, css, libs): cache-first
  e.respondWith(
    caches.match(req).then(function (hit) {
      if (hit) return hit;
      return fetch(req).then(function (res) {
        if (res && res.status === 200 && res.type === 'basic') {
          var copy = res.clone();
          caches.open(CACHE).then(function (c) { c.put(req, copy); });
        }
        return res;
      });
    })
  );
});
