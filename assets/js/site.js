/* Il video della Home parte da solo per attributo, quindi funziona anche senza
   questo script. Qui si aggiungono soltanto due cose: il comando manuale e il
   rispetto di prefers-reduced-motion, che non è un cancello prima dell'avvio
   ma una pausa subito dopo. */
(() => {
  const video = document.getElementById("home-video");
  const button = document.getElementById("home-video-toggle");
  if (!video || !button) return;

  const label = button.querySelector(".visually-hidden");
  /* Tre stati, non due: a fine opera il comando non dice "riparti" ma "rivedi".
     Il fermo immagine è il deposito, e l'etichetta deve confermare che si è
     visto tutto invece di far pensare a una pausa. */
  const sync = () => {
    const playing = !video.paused;
    const ended = video.ended;
    button.setAttribute("aria-pressed", String(playing));
    button.dataset.ended = String(ended);
    if (label) {
      label.textContent = ended ? button.dataset.replay
                        : playing ? button.dataset.pause
                        : button.dataset.play;
    }
  };

  button.hidden = false;
  button.addEventListener("click", () => {
    if (video.ended) {
      video.currentTime = 0;
      video.play().catch(() => {});
    } else if (video.paused) {
      video.play().catch(() => {});
    } else {
      video.pause();
    }
    sync();
  });
  video.addEventListener("play", sync);
  video.addEventListener("pause", sync);
  video.addEventListener("ended", sync);

  if (window.matchMedia("(prefers-reduced-motion: reduce)").matches) {
    video.pause();
  }
  sync();
})();
