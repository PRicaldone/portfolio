# Il sito si genera, non si scrive a mano

Dal 31 luglio 2026 le pagine di questo repo sono **prodotte da `build.py`**. Modificare
direttamente un `index.html` non serve a niente: la modifica sparisce alla prima
ricostruzione, senza avvisare nessuno.

## Il flusso

```sh
python3 _build/build.py    # produce 28 pagine, quattordici per lingua
python3 _build/test.py     # 1000 controlli — devono passare prima di ogni push
git add -A && git commit && git push origin main
```

Netlify pubblica da `main`. Dopo il deploy si verifica con `curl` sull'URL live.
**Mai un server locale, mai Playwright** per «vedere se viene bene»: resta appeso e Paolo
deve fermarlo a mano. I controlli automatici prima, `curl` dopo, e il giudizio visivo è suo
(regola del 14 lug 2026).

## Cosa c'è qui dentro

- **`build.py`** — il generatore. I testi non sono scritti qui: si estraggono **verbatim**
  dagli snapshot in `_source/`, e le revisioni del master si applicano nella tabella
  `REWRITES`. Dal 12 set 2026 non ci sono più appunti: Writing è il saggio stesso.
- **`test.py`** — parità fra le lingue, riferimenti che risolvono, nessuna pagina senza
  barra o senza titolo, la Home che parte senza JavaScript, l'indice Works senza video,
  una pagina per opera e nessuna pagina di appunto, l'email solo in Contact, nessuna parola vietata,
  nessun anno diverso da 2026 e 1968.
- **`_redirects`** — la fonte; la copia in radice è quella che Netlify legge. **Si modifica
  qui**, poi si copia. Blocca anche `/_source/*` e `/_build/*`, che sono versionati ma non
  vanno serviti.
- **`_source/`** (fuori da questa cartella) — gli snapshot del sito precedente, da cui i
  testi vengono estratti. Non si toccano: sono la ragione per cui il pensiero pubblicato è
  identico al master nel vault.

`PREVIEW=1` marca le pagine `noindex`, e serve solo per pubblicazioni parallele.

## Perché sta nel repo

Fino al 1° agosto 2026 il generatore viveva in una cartella su un disco solo, non versionata
da nessuna parte: il sito restava online ma non era più rifacibile se quella cartella fosse
sparita. Adesso il programma e ciò che produce stanno nello stesso commit, e un cambio di
`build.py` si legge insieme all'HTML che ha generato.

## Gli Appunti non ci sono più

Chiusi il 12 set 2026, con la serie Silenzi (dieci pezzi) e la sezione Appunti di Writing.
Paolo non crea le opere dagli appunti ma da intuizioni emozionali, e una pratica di scrittura
che non è sua non deve stare sul sito come se lo fosse. I vecchi indirizzi `/writing/silences/*`
e `/writing/thought/` restano vivi come 301 verso `/writing/`, che ora è il saggio. Storia e
ragioni nel vault: `Studio/strategie/architettura-social.md` § *Chiusura degli Appunti*.

## I video delle opere

Vedi `assets/RICETTA-VIDEO-SITO.md`: è lo **standard di consegna per ogni opera di ogni
collezione**. Un file solo per opera, `…_SITE_2560x1920`, lo stesso in Home e nella pagina
opera; l'opera finisce e resta sull'ultimo fotogramma, il replay lo decide chi guarda. Dentro
anche il preset Resolve, le verifiche obbligatorie prima di pubblicare e le trappole già
incontrate — il doppio job in coda che corrompe il file, l'in/out del Deliver che sposta la
durata.
