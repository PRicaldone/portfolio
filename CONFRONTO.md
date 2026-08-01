# Confronto delle tre versioni — 30 luglio 2026

Tre esecuzioni indipendenti dello stesso brief, sullo stesso materiale, sulla stessa ricerca:
**Claude** (`~/claude-sandbox/claude_post_ricerca_curatori_v1`, congelata), **Kimi K3**
(`~/kimi-sandbox/kimi_post_ricerca_curatori_v2`), **Codex gpt-5.6-sol**
(`~/codex-sandbox/codex_post_ricerca_curatori_v2`).

Letto: i tre `SCELTE.md` più il codice costruito — markup della Home, indice Works, pagine
opera, struttura della scrittura, CSS. Le affermazioni qui sotto vengono dai file, non dalle
dichiarazioni dei tre modelli.

**Come leggerlo.** Dove tutte e tre convergono senza essersi parlate, la decisione è presa e
non vale riaprirla. Dove divergono, c'è una scelta di Paolo, e per ognuna c'è una
raccomandazione con il suo perché.

---

## Le convergenze — otto punti, considerati chiusi

1. **La Home consegna l'opera.** Tutte e tre mettono Act I in autoplay muto e in loop, a
   schermo grande, e tutte e tre usano il file **con la coda** (`act-i-home.mp4`), quindi la
   tenuta sul finale è rispettata. Nessuna tagline in nessuna delle tre.
2. **La navigazione è visibile dal primo istante** e non si nasconde. È l'unica condizione
   che l'evidenza pone davvero, e nessuno ha provato ad aggirarla.
3. **Nessuno strato on-chain, da nessuna parte.** Zero occorrenze in tutte e tre, edizione
   dichiarata uguale per tutte le opere.
4. **Ogni opera ha un indirizzo proprio e stabile**, e nella pagina opera il player è
   **click-to-play**. Il movimento gratuito sta in Home, quello scelto nella pagina.
5. **Act III è solo titolo e posizione**: nessuna data, nessuna immagine, nessun link,
   nessuna cornice vuota. Nessuna sala predisposta e non abitata in nessuna delle tre.
6. **La scrittura è una voce di menu con tre livelli** — Pensiero, Appunti come ombrello,
   Silenzi come serie annidata. L'ombrello non è mai stato appiattito sulla serie.
7. **About: prima la voce, poi la scheda.** Statement in prima persona, blocco fattuale in
   terza in coda, ritratto piccolo e mai a piena larghezza. Contact ridotto alla riga
   fattuale sulla vendita privata, senza cifre.
8. **Registro visivo identico nella sostanza.** Due valori su un quasi-nero tiepido, mai
   `#000` come fondo, una sola famiglia di sistema, effetti praticamente assenti: fra i tre
   CSS ci sono in tutto **una transizione e zero animazioni**. Nessuna schermata di
   caricamento, nessun cursore custom, nessun reveal.

---

## Le divergenze — sette decisioni da prendere

### 1. Il video nell'indice Works

| | |
|---|---|
| **Claude** | due video nell'indice (Works piatta, l'opera si incontra subito) |
| **Kimi** | due fermi immagine, video solo nella pagina opera |
| **Codex** | due fermi immagine, video solo nella pagina opera |

**Raccomandazione: still nell'indice.** Due su tre, e l'argomento regge meglio del mio: con
dieci opere un indice che carica dieci video le mette in competizione nella stessa videata.
Lo still è la porta in 28 casi su 39 del campione. *(Già recepito nella skill il 29 luglio.)*

### 2. La forma dello slug della pagina opera

| | |
|---|---|
| **Claude** | `works/act-i.html` |
| **Kimi** | `act-i.html` in radice |
| **Codex** | `works/i-have-to/` (cartella, slug dal titolo) |

**Raccomandazione: `works/i-have-to/`.** Lo slug dal titolo è leggibile per chi incolla il
link in una email, e la cartella `works/` tiene l'archivio ordinato quando le opere saranno
dieci. Contro: se un titolo cambiasse, lo slug non si può più toccare — ma i titoli delle
opere non cambiano.

### 3. L'indirizzo dei singoli appunti

| | |
|---|---|
| **Claude** | una pagina per appunto |
| **Kimi** | **nessuna**: tutto in `texts.html`, i pezzi raggiungibili solo per ancora `#s001` |
| **Codex** | una pagina per appunto |

**Raccomandazione: pagina propria per ogni appunto.** L'evidenza sui link citabili — non
mandare a una pagina indice dicendo «scorri fino all'ennesimo elemento» — non riguarda solo
le opere. Un appunto senza indirizzo non si condivide e non si cita. È il difetto più netto
della versione di Kimi.

### 4. Come parte il video in Home

| | |
|---|---|
| **Claude** | attributo `autoplay muted loop playsinline` nell'HTML |
| **Kimi** | idem, più `preload="auto"` |
| **Codex** | **nessun `autoplay` nell'HTML**: JS imposta `src` e chiama `play()`, più un bottone Play/Pause e il rispetto di `prefers-reduced-motion` |

**Raccomandazione: l'attributo nell'HTML, e da Codex si innesta il resto.** L'approccio di
Codex è più elegante — carica il video solo quando serve, dà un comando esplicito, e non
avvia niente a chi ha chiesto meno movimento — ma **senza JavaScript la Home resta un poster
fermo**, e nel suo codice non c'è alcun `<noscript>`. La combinazione giusta è l'attributo
`autoplay` nell'HTML, che funziona sempre, più il bottone Play/Pause e il rispetto di
`prefers-reduced-motion` che Codex ha portato. È il suo innesto migliore.

### 5. Il loop nel player della pagina opera

| | |
|---|---|
| **Claude** | `loop` |
| **Kimi** | `loop` |
| **Codex** | **nessun loop** |

**Raccomandazione: loop.** È la regola scritta il 28 luglio, con la ragione della sala: un
single-channel in galleria gira in loop. Codex qui esegue una regola precedente.

### 6. Il margine attorno all'opera in Home

| | |
|---|---|
| **Claude** | l'opera occupa la videata, dentro il suo rapporto |
| **Kimi** | pieno assoluto, `object-fit: contain`, e le bande del 4:3 si fondono col fondo — «l'opera non è inserita nel sito, è il sito» |
| **Codex** | quasi pieno campo **ma con un margine**, perché il bordo si dissolva senza che il video diventi sfondo |

**DECISO (Paolo, 30 lug): Codex** — e non solo per il margine: si prende la sua Home anche per **la barra di navigazione e il titolo dell'opera**, cioè l'impianto completo dell'ingresso.

**Nessuna raccomandazione originaria: era una scelta estetica**, ed è la differenza più visibile fra
le tre. La posizione di Kimi è più radicale e più coerente con «la pagina diventa la sala»;
quella di Codex protegge l'opera dal diventare texture di fondo. Va guardata a schermo, non
decisa a parole.

### 7. Come è costruito il sito

| | |
|---|---|
| **Claude** | generatore Python (`_build/build.py`), testi estratti verbatim dalle fonti |
| **Kimi** | HTML scritto a mano, pagine gemelle IT in `it/` |
| **Codex** | generatore Node (`scripts/build-site.mjs`) **più una suite di test** (`tests/site.test.mjs`) |

**Raccomandazione: generatore, e i test di Codex.** Con sei pagine per due lingue, la
manutenzione a mano è il modo in cui il bilinguismo si rompe a metà — che è precisamente il
difetto osservato nell'unico sito bilingue del campione. Il generatore rende la parità fra
le due lingue una proprietà del codice invece che una promessa. I test sono la cosa che
nessuno dei due aveva chiesto e che Codex ha aggiunto: verificano che le pagine gemelle
esistano e siano coerenti.

---

## Due difetti da non ereditare

- **Kimi**: gli appunti non hanno un indirizzo proprio (divergenza 3).
- **Codex**: la Home dipende dal JavaScript e non ha `<noscript>` (divergenza 4). Nella sua
  cartella è rimasta anche `docs/superpowers/`, residuo del caricamento delle skill di
  processo: da non portare.

---

## Il contributo migliore di ciascuno

- **Claude** — la coda nel file invece che nel codice: la tenuta sul finale costruita in
  delivery funziona anche su un monitor in mostra, non solo nel browser.
- **Kimi** — la formulazione della Home: le bande del 4:3 che si fondono col fondo, così la
  pagina diventa la sala. E la lettura lunga come «biblioteca buia dove si accende un testo
  per volta», senza date, senza conteggi, senza calendario.
- **Codex** — il bottone Play/Pause con `prefers-reduced-motion`, i test sulla parità
  bilingue, e una formulazione che vale la pena tenere: *«Pensiero e opere devono avere
  prossimità architettonica, non sovrapposizione interpretativa»*.


---

## Decisioni prese — 30 luglio 2026

1. **Still nell'indice Works.** Il video vive nella pagina opera.
2. **Slug `works/i-have-to/`**, cartella e titolo.
3. **Pagina propria per ogni appunto**, con indirizzo stabile.
4. **Home di Codex, con una sola correzione al markup**: `autoplay` e `src` nell'HTML al
   posto di `data-src`, così l'opera parte anche quando il JavaScript non gira. Allo script
   restano il bottone e `prefers-reduced-motion`, che da cancello prima dell'avvio diventa
   pausa immediata dopo. A schermo, per un visitatore con JS attivo, non cambia nulla.
5. **Loop nel player** della pagina opera.
6. **Impianto d'ingresso di Codex per intero**: margine attorno all'opera, barra di
   navigazione e titolo dell'opera come li ha costruiti lui.
7. **Generatore più test.** Niente HTML a mano: la parità fra le due lingue deve essere una
   proprietà del codice.

**Bottone Play/Pause — specifica di Paolo.** Non dentro il frame: una **icona piccola fuori
dall'opera, sotto e centrata**. Discreta, senza etichetta testuale a vista, con il nome
accessibile per chi usa uno screen reader. Il gesto di comando non deve stare sopra l'opera.
