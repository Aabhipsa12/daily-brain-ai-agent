// Daily Brain Service Worker
const CACHE_NAME = 'daily-brain-v1';
const ASSETS_TO_CACHE = [
  '/',
  '/app/static/icon-192.png',
  '/app/static/icon-512.png',
  '/app/static/apple-touch-icon.png',
  '/app/static/manifest.json'
];

self.addEventListener('install', (event) => {
  event.waitUntil(
    caches.open(CACHE_NAME).then((cache) => {
      return cache.addAll(ASSETS_TO_CACHE).catch(() => {});
    })
  );
  self.skipWaiting();
});

self.addEventListener('activate', (event) => {
  event.waitUntil(
    caches.keys().then((keys) => {
      return Promise.all(
        keys.map((key) => {
          if (key !== CACHE_NAME) {
            return caches.delete(key);
          }
        })
      );
    })
  );
  self.clients.claim();
});

self.addEventListener('fetch', (event) => {
  // Pass dynamic websocket and API streams straight through
  if (event.request.url.includes('/_stcore') || event.request.url.includes('stream')) {
    return;
  }
  event.respondWith(
    fetch(event.request).catch(() => {
      return caches.match(event.request);
    })
  );
});