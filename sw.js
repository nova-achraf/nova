// AZAMI AI — Service Worker (PWA)
// Network-first for HTML (always fresh), cache-first for assets, offline support
const CACHE = 'azami-ai-v7';
const ASSETS = [
  'azami-global.html',
  'azami-manifest.json',
  'azami-logo.webp',
  'azami-icon-192.png',
  'azami-icon-512.png',
  'azami-apple-icon.png'
];

// Install: pre-cache core assets
self.addEventListener('install', function(e) {
  e.waitUntil(
    caches.open(CACHE).then(function(c) { return c.addAll(ASSETS); }).then(function() { return self.skipWaiting(); })
  );
});

// Activate: purge old caches
self.addEventListener('activate', function(e) {
  e.waitUntil(
    caches.keys().then(function(keys) {
      return Promise.all(keys.filter(function(k) { return k !== CACHE; }).map(function(k) { return caches.delete(k); }));
    }).then(function() { return self.clients.claim(); })
  );
});

// Fetch strategy
self.addEventListener('fetch', function(e) {
  var req = e.request;
  if (req.method !== 'GET') return;

  // Network-first for navigation (HTML pages) — always get fresh version
  if (req.mode === 'navigate') {
    e.respondWith(
      fetch(req).then(function(res) {
        var copy = res.clone();
        caches.open(CACHE).then(function(c) { c.put(req, copy); });
        return res;
      }).catch(function() {
        return caches.match(req).then(function(r) { return r || caches.match('azami-global.html'); });
      })
    );
    return;
  }

  // Cache-first for other assets (manifest, icons, images)
  e.respondWith(
    caches.match(req).then(function(cached) {
      return cached || fetch(req).then(function(res) {
        if (res && res.status === 200) {
          var copy = res.clone();
          caches.open(CACHE).then(function(c) { c.put(req, copy); });
        }
        return res;
      }).catch(function() { return cached; });
    })
  );
});
