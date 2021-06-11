let cacheName = 'pwa01';

let filesToCache = [
    'app.py',
    'templates/index.html',
    'templates/games.html',
    'templates/languages.html',
    'static/css/Style.css',
    'static/js/main.js'
];

/* Start the service worker and cache all of the app's content */

self.addEventListener('install', (evt) => {
    console.log('[ServiceWorker] Install');
    evt.waitUntil(
        caches.open(CACHE_NAME).then((cache) => {
            console.log('[ServiceWorker] Pre-caching offline page');
            return cache.addAll(FILES_TO_CACHE);
        })
    );

    self.skipWaiting();
});

self.addEventListener('activate', (evt) => {
    console.log('[ServiceWorker] Activate');
    evt.waitUntil(
        caches.keys().then((keyList) => {
            return Promise.all(keyList.map((key) => {
                if (key !== CACHE_NAME) {
                    console.log('[ServiceWorker] Removing old cache', key);
                    return caches.delete(key);
                }
            }));
        })
    );
    self.clients.claim();
});

/* Serve cached content when offline */

self.addEventListener('fetch', function(event) {
    event.respondWith(fetch(event.request));
});