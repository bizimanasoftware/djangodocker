const CACHE_NAME = 'gloex.org-pwa-v1';
const OFFLINE_URL = '/offline/';

// Assets to cache
const urlsToCache = [
  '/',
  OFFLINE_URL,
  '/static/manifest.json',
  '/static/images/icon192real.png',
  '/static/css/styles.css', // main site CSS
  '/static/js/script.js'      // main site JS
];

// Install event
self.addEventListener('install', event => {
  event.waitUntil(
    caches.open(CACHE_NAME)
      .then(cache => cache.addAll(urlsToCache))
      .then(() => self.skipWaiting())
  );
});

// Activate event - clean old caches
self.addEventListener('activate', event => {
  event.waitUntil(
    caches.keys().then(cacheNames =>
      Promise.all(
        cacheNames.filter(name => name !== CACHE_NAME)
          .map(name => caches.delete(name))
      )
    )
  );
  self.clients.claim();
});

// Fetch event - cache first for static, fallback for offline
self.addEventListener('fetch', event => {
  if (event.request.mode === 'navigate') {
    event.respondWith(
      fetch(event.request).catch(() => caches.match(OFFLINE_URL))
    );
  } else {
    event.respondWith(
      caches.match(event.request).then(response => response || fetch(event.request))
    );
  }
});
