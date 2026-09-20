// Daily Brain Service Worker
const CACHE_NAME = 'daily-brain-v2';
const OFFLINE_URL = '/app/static/offline.html';

const ASSETS_TO_CACHE = [
  '/',
  OFFLINE_URL,
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
  // Pass dynamic websocket and Streamlit internal streams straight through
  if (
    event.request.url.includes('/_stcore') || 
    event.request.url.includes('stream') ||
    event.request.method !== 'GET'
  ) {
    return;
  }

  event.respondWith(
    fetch(event.request)
      .then((networkResponse) => {
        // Cache static resources on success
        if (
          networkResponse && 
          networkResponse.status === 200 && 
          (event.request.url.includes('/app/static/') || event.request.url.includes('/static/'))
        ) {
          const responseClone = networkResponse.clone();
          caches.open(CACHE_NAME).then((cache) => {
            cache.put(event.request, responseClone);
          });
        }
        return networkResponse;
      })
      .catch(async () => {
        const cachedResponse = await caches.match(event.request);
        if (cachedResponse) {
          return cachedResponse;
        }
        if (event.request.mode === 'navigate') {
          return caches.match(OFFLINE_URL);
        }
      })
  );
});
