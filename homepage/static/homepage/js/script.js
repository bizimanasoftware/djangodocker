// Add shadow on scroll for better floating effect
document.addEventListener('DOMContentLoaded', function () {
    const navbar = document.querySelector('nav.navbar');
    // Check if the navbar exists and is fixed-top
    if (navbar && navbar.classList.contains('fixed-top')) {
        window.addEventListener('scroll', () => {
            if (window.scrollY > 10) { // Adjust scroll threshold as needed
                navbar.classList.add('scrolled');
            } else {
                navbar.classList.remove('scrolled');
            }
        });
    }
});

document.addEventListener('DOMContentLoaded', function() {
    const listenButton = document.getElementById('listenButton');
    const myAudio = document.getElementById('myAudio');
    let isPlaying = false;

    if (listenButton && myAudio) {
        // This function attempts to play the audio and handles the Promise
        function toggleAudio() {
            if (!isPlaying) {
                // Try to play the audio
                const playPromise = myAudio.play();
                
                if (playPromise !== undefined) {
                    playPromise.then(() => {
                        // Playback started successfully
                        isPlaying = true;
                        listenButton.innerHTML = '⏸️ Pause';
                    }).catch(error => {
                        // Playback was prevented, log the error
                        console.error("Audio playback was blocked:", error);
                        isPlaying = false; // Reset state
                    });
                }
            } else {
                // Pause the audio
                myAudio.pause();
                isPlaying = false;
                listenButton.innerHTML = '🎧 Listen';
            }
        }

        // Use a single, reliable event listener for both mobile and desktop
        listenButton.addEventListener('click', toggleAudio);
    }
});

 let deferredPrompt;
  const installPrompt = document.getElementById('installPrompt');

  window.addEventListener('beforeinstallprompt', (e) => {
    e.preventDefault();
    deferredPrompt = e;
    setTimeout(() => {
      installPrompt.style.display = 'flex';
    }, 1000);
  });

  installPrompt.addEventListener('click', () => {
    installPrompt.style.display = 'none';
    deferredPrompt.prompt();
    deferredPrompt.userChoice.then(choiceResult => {
      if (choiceResult.outcome === 'accepted') {
        console.log('✅ User accepted the install prompt');
      } else {
        console.log('❌ User dismissed the install prompt');
      }
      deferredPrompt = null;
    });
  });

  window.addEventListener('appinstalled', () => {
    console.log('🎉 Gloex PWA installed');
    installPrompt.style.display = 'none';
  });
