
function sposta(id) {
  document.location=id;
}

window.onload = () => {
    'use strict';
    if ('serviceWorker' in navigator) {
        navigator.serviceWorker
            .register('./service-worker.js').then(function (registration) {
          // Service worker registered correctly.
          console.log('ServiceWorker registration successful with scope: ', registration.scope);
        },
        function (err) {
          // Troubles in registering the service worker. :(
          console.log('ServiceWorker registration failed: ', err);
        });
    }
}