/* Il video della Home parte da solo per attributo, quindi funziona anche senza
   questo script. Qui si aggiungono soltanto due cose: il comando manuale e il
   rispetto di prefers-reduced-motion, che non è un cancello prima dell'avvio
   ma una pausa subito dopo. */
(() => {
  const video = document.getElementById("home-video");
  const button = document.getElementById("home-video-toggle");
  if (!video || !button) return;

  const label = button.querySelector(".visually-hidden");
  const sync = () => {
    const playing = !video.paused;
    button.setAttribute("aria-pressed", String(playing));
    if (label) label.textContent = playing ? button.dataset.pause : button.dataset.play;
  };

  button.hidden = false;
  button.addEventListener("click", () => {
    if (video.paused) {
      video.play().catch(() => {});
    } else {
      video.pause();
    }
    sync();
  });
  video.addEventListener("play", sync);
  video.addEventListener("pause", sync);

  if (window.matchMedia("(prefers-reduced-motion: reduce)").matches) {
    video.pause();
  }
  sync();
})();
