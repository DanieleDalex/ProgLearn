
function sidebar_open() {
  document.getElementById("mySidebar").style.width = "250px";
  document.getElementById("mySidebar").style.display = "block";
  document.getElementById("myOverlay").style.display = "block";
}

function sidebar_close() {
  document.getElementById("mySidebar").style.width = "0";
  document.getElementById("mySidebar").style.display = "none";
  document.getElementById("myOverlay").style.display = "none";
}

function sposta(id) {
  document.location=id;
}

window.onload = () => {
    'use strict';
    if ('serviceWorker' in navigator) {
        navigator.serviceWorker
            .register('../../sw.js').then(function (registration) {
          // Service worker registered correctly.
          console.log('ServiceWorker registration successful with scope: ', registration.scope);
        },
        function (err) {
          // Troubles in registering the service worker. :(
          console.log('ServiceWorker registration failed: ', err);
        });
    }
}