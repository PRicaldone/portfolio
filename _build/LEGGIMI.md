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
  `REWRITES`. Gli appunti della serie Silenzi sono dichiarati come `S005`, `S006`, … con
  etichetta, titolo e paragrafi nelle due lingue, copiati dal raccordo nel vault.
- **`test.py`** — parità fra le lingue, riferimenti che risolvono, nessuna pagina senza
  barra o senza titolo, la Home che parte senza JavaScript, l'indice Works senza video,
  una pagina per opera e per appunto, l'email solo in Contact, nessuna parola vietata,
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

## Aggiungere un appunto

La ricetta completa vive nella skill `studio-portfolio-website` § *Sezione Writing*. In breve:
il testo è nel raccordo `Studio/output/appunti/{serie}/{serie-sing}-NNN.md` del vault, integrale
IT **e** EN; qui si dichiara un blocco `SNNN` sul modello di `S006`, un elemento di lista per
paragrafo, verbatim, senza CTA e senza rimandi alle opere.

## Il video della Home

Vedi `assets/RICETTA-VIDEO-HOME.md`: dove stanno i master, come si produce il derivato, e la
trappola del fotogramma nero in coda all'export di Act I.
