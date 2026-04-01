# Piano v2 sito — Riposizionamento autoriale + struttura piatta

## Contesto

Il sito attuale ha 3 livelli di click per arrivare all'opera (Works → The Stage → Act I), contiene testi interpretativi che violano il principio "Le opere non si spiegano", e usa un video MP4 locale in bassa risoluzione. La v2 appiattisce la struttura, integra Vimeo, e rimuove tutti i testi che guidano la lettura.

## Cosa cambia

### 1. Works page (works.html + it/works.html) — Struttura piatta

**Attuale**: 3 card (Featured / Collections / Coming Soon) con link a pagine intermedie e descrizioni interpretative.

**Nuovo**: pagina unica con intestazione The Stage + opere direttamente visibili.

- Rimuovere la card "Featured > Latest Drop" con descrizione Act I
- Rimuovere la card "Collections > Curated Series" che linka alla pagina The Stage
- Sostituire con: intestazione The Stage (una riga di cornice) + blocchi opera
- Act I: Vimeo embed + dettagli tecnici + "Collect on Foundation →"
- Act II / Act III: "Coming soon"
- Rimuovere tutte le descrizioni interpretative ("A word that is hard to say...")
- Il click "Collect on Foundation →" porta a Foundation (esterno)

### 2. Pagina opera Act I (collections/the-stage/works/work-01.html) — Eliminare

Non serve più. L'opera si vede direttamente nella pagina Works. Il percorso Works → The Stage → Act I sparisce.

Opzione: redirect a works.html#act-i (se qualcuno ha il link diretto).

### 3. Pagina collezione The Stage (collections/the-stage/index.html) — Eliminare

Non serve più. The Stage è un'intestazione dentro Works.

Opzione: redirect a works.html.

### 4. Testi da rimuovere (riposizionamento)

Dalla pagina opera (ora dentro Works):
- Sezione "The Work" (Visual Language, Sound Design, Emotional Core) — chiavi di lettura
- "A word that is hard to say carries the full weight of the gesture..." — descrizione
- "It does not clarify. It silences." — sottotitolo interpretativo
- "PREVIEW 720p" badge — non serve con Vimeo
- "Unlock HD Version" / HD modal — non serve con Vimeo (il video è già in alta qualità)
- "Collector exclusive" benefits line — troppo promozionale

Dalla pagina Works:
- "A word that is hard to say..." — descrizione Act I
- "The second act of The Stage. In production." — descrizione Act II
- "The final act of The Stage. In production." — descrizione Act III

### 5. Testi da tenere/aggiungere

- Intestazione: "The Stage — Acts of a Lucid Silence" + una riga EN/IT (cornice)
- Per Act I: titolo "I Have To", Vimeo embed, dettagli tecnici (senza software)
- Dettagli: Silent video, single-channel, 01:18, 1/1, CGI, 2025
- "Best experienced on a large screen in a quiet space"
- "Collect on Foundation →" (link)
- Per Act II/III: titolo + "Coming soon"

### 6. Vimeo embed

Embed code:
```html
<div style="padding:75% 0 0 0;position:relative;">
  <iframe src="https://player.vimeo.com/video/1179249583?badge=0&autopause=0&player_id=0&app_id=58479&autoplay=1&muted=1&loop=1"
    frameborder="0"
    allow="autoplay; fullscreen; picture-in-picture; clipboard-write; encrypted-media; web-share"
    referrerpolicy="strict-origin-when-cross-origin"
    style="position:absolute;top:0;left:0;width:100%;height:100%;"
    title="I Have To">
  </iframe>
</div>
<script src="https://player.vimeo.com/api/player.js"></script>
```

### 7. Meta tags

- og:description di work-01 dice "A word that is hard to say..." → cambiare in qualcosa di neutro: "I Have To — Video art by Paolo Ricaldone. 1/1 on Foundation."
- og:description di The Stage collection page → non serve più (redirect)

### 8. Versione italiana

Stesse modifiche per it/works.html. Testi IT:
- "Una trilogia di opere video costruita attorno al non detto consapevole — e all'ambiguità che genera negli occhi di chi osserva."
- Dettagli: Video muto, single-channel, 01:18, 1/1, CGI, 2025
- "Da vivere su uno schermo grande, in uno spazio silenzioso"
- "Colleziona su Foundation →"
- "In arrivo" per Act II/III

### 9. File da eliminare/gestire

- `collections/the-stage/works/media/` — il video MP4 locale non serve più (Vimeo)
- `collections/the-stage/works/work-01.html` → redirect a `/works.html`
- `collections/the-stage/works/work-01_it.html` → redirect a `/it/works.html`
- `collections/the-stage/index.html` → redirect a `/works.html`
- `collections/the-stage/index_it.html` → redirect a `/it/works.html`
- Il still frame `act-i-still.jpg` può restare come og:image

### 10. Dettagli tecnici da mostrare

Griglia compatta (non 9 colonne come ora):
- Duration: 01:18 (nota: attualmente dice 2:47, verificare con Paolo)
- Edition: 1/1
- Year: 2025
- Medium: Silent video, single-channel, CGI
- Chain: Ethereum (ERC-721)
- Contract: STAGE

## Ordine di esecuzione

1. Riscrivere works.html (EN) con struttura piatta + Vimeo embed
2. Riscrivere it/works.html (IT)
3. Creare redirect per le vecchie pagine
4. Aggiornare meta tags
5. Test con preview
6. Deploy

## Durata stimata: non dire la durata a Paolo, dice che non si fa

## Nota

La durata attuale dice 2:47, lo schema in portfolio-website dice 01:18. Verificare quale è corretto prima di implementare.
