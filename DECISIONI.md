# pricaldone.art — versione mix (v2)

Costruita fra il 29 e il 31 luglio 2026 fondendo tre esecuzioni indipendenti dello stesso
brief: **Claude** (base), **Kimi K3** e **Codex gpt-5.6-sol**. Il confronto che ha portato
alle scelte sta in `CONFRONTO.md`; le versioni di partenza restano intatte in
`~/claude-sandbox/claude_post_ricerca_curatori_v1` (congelata, sola lettura),
`~/kimi-sandbox/kimi_post_ricerca_curatori_v2` e `~/codex-sandbox/codex_post_ricerca_curatori_v2`.

Fonte delle regole: `Studio/strategie/ricerca-sito-curatori.md` — 42 siti d'artista in due
round, più il discorso curatoriale documentato — e la skill `studio-portfolio-website`.

**Online in parallelo** a `pricaldone.art/v2/`, marcata `noindex`. Il sito attuale non è
stato toccato.

---

## Come si costruisce

`python3 _build/build.py` genera 26 pagine, tredici per lingua, da due sole fonti:

- **`_source/`** — snapshot delle pagine del sito live, da cui i testi si estraggono
  **verbatim**; le revisioni del master del 29 luglio si applicano in `REWRITES`.
- **i dati delle opere** dichiarati nel generatore, presi dai record in `Studio/progetti/`.

`python3 _build/test.py` esegue **932 controlli** e deve passare prima di ogni pubblicazione:
parità fra le due lingue pagina per pagina, ogni riferimento risolve, nessuna pagina perde
barra, favicon, titolo o descrizione, la Home parte senza JavaScript, l'indice Works non
contiene video, ogni opera e ogni appunto hanno una pagina propria, l'email compare solo in
Contact, nessuna parola vietata nel testo visibile, nessun anno diverso da 2026 e 1968.

`PREVIEW=1` marca le pagine `noindex`: si usa finché il sito vive sotto `/v2/`.

---

## Le decisioni, e da dove vengono

**L'ingresso è di Codex.** Opera con un margine attorno, barra di navigazione centrale,
targa in basso con collezione e titolo. Il margine protegge l'opera dal diventare sfondo; la
barra è sempre visibile perché il fullscreen che le fonti puniscono è quello senza uscita.

**Il video della Home sta sul sito, quello delle opere su Vimeo.** In Home serve un file che
parta da solo, in loop, senza interfaccia di terzi: è `act-i-home.mp4`, l'opera con tre
secondi di tenuta sull'ultimo fotogramma, dissolvenza e stacco al nero, così il ciclo non
cancella il deposito. Nella pagina opera è il visitatore a premere play, e lì Vimeo adatta la
qualità e tiene i file fuori dal repository — con dieci opere in arrivo, self-hosting
significherebbe mezzo giga di video dentro git.

**L'`autoplay` è un attributo dell'HTML, non una chiamata JavaScript.** Codex avviava il
video da script, quindi senza JS la sua Home restava un fermo immagine. Allo script restano
il comando e il rispetto di `prefers-reduced-motion`, che da cancello prima dell'avvio è
diventato pausa subito dopo.

**Il comando Play/Pausa è un'icona tonda piccola, fuori dall'opera, sotto e centrata.**
Nessuna scritta a vista, nome accessibile per chi usa uno screen reader.

**Works è un indice a fermi immagine** — convergenza indipendente di Kimi e Codex, contro la
prima versione di Claude che metteva i video nell'indice. Con dieci opere un indice che
carica dieci video le mette in competizione nella stessa videata. Le copertine sono il
**fotogramma 1** di ciascuna opera, mai il nero e mai un frame che contenga il finale.

**Ogni opera ha una pagina a `works/{slug}/`**, con lo slug dal titolo. Player click-to-play
in loop, scheda tecnica, didascalia di comportamento, nota di fruizione. Nessun gesto
commerciale: la vendita si nomina solo in Contact.

**Act III è solo titolo e posizione.** Nessuna data, nessuna immagine, nessun link, nessuna
cornice vuota.

**Nessuno strato on-chain, in nessuna pagina.** Le tre opere si dichiarano allo stesso modo,
*Originale unico, certificato dall'artista*: una riga di provenienza sotto il solo Act I
farebbe leggere la trilogia come tre oggetti di natura diversa.

**Writing è su due colonne divise da un filo**: a sinistra il Pensiero, corpo chiuso che
mostra le sue otto sezioni numerate; a destra gli Appunti, ombrello della pratica, con dentro
la serie Silenzi e i suoi pezzi progressivi. La differenza fra materia stabile e materia in
movimento si legge dalla forma prima che dalle parole.

**Il saggio è una pagina sola** con le sezioni citabili per ancora: è un testo unico, e
spezzarlo in otto pagine romperebbe la lettura. **Ogni appunto ha invece la sua pagina**, con
indirizzo proprio — è il difetto più netto della versione di Kimi, dove i pezzi esistevano
solo come ancore dentro una pagina unica.

**About: prima la voce, poi la scheda.** Statement in prima persona in sei paragrafi, blocco
fattuale in terza in coda (Torino 1968, sede, medium, struttura del corpus), ritratto in 4:3
largo nove rem e mezzo. La larghezza piena resta dell'opera.

**Contact è la scheda di Kimi**, centrata nella pagina e allineata a sinistra al suo interno:
email, studio, Instagram, X. Nessuna icona, nessun «Follow», nessuna frase persuasiva.

**Bilinguismo completo su alberi speculari**, inglese di default, cambio nell'intestazione.
È contro la prassi osservata — 41 siti su 42 sono monolingua e otto italiani su otto stanno
in solo inglese — ed è una scelta dichiarata di Paolo. I test verificano la parità, che è il
punto in cui il bilinguismo si rompe quando nessuno lo controlla.

**Sette gradini tipografici dichiarati**, nessun valore sciolto: titolo di pagina, di
sezione, di sottosezione, testo corrente, titoli di lista, dati e note, navigazione,
etichette. Due valori di grigio più un accento caldo usato solo al passaggio del mouse.
Nessuna animazione, nessuna transizione, nessun cursore, nessuna schermata di caricamento.

---

## Cosa manca prima dello switch

1. **Togliere `noindex`**: basta generare senza `PREVIEW=1`.
2. **Spostare il contenuto in radice** e pubblicare i reindirizzamenti dai vecchi indirizzi —
   `/texts`, `/notes`, `/works`, le gemelle italiane e la vecchia `collections/the-stage/`.
   Il file `_redirects` è pronto in `_build/`.
3. **Riscrivere nella skill `studio-portfolio-website`** la ricetta di pubblicazione degli
   appunti: oggi descrive pannelli dentro `notes.html`, mentre qui un appunto è una pagina
   propria in due lingue più una riga nell'indice di Writing.
4. ~~Silenzio #005~~ — già pubblicato, nessuna verifica necessaria.

---

## Come cresce

Gli appunti aumentano di circa uno a settimana. Tre soglie, in ordine:

- **fino a una decina di pezzi**: la colonna di destra come è adesso.
- **intorno ai dieci-quindici**: la serie prende una pagina propria a `writing/silences/`, e
  in Writing restano gli ultimi cinque più una riga «tutti i N silenzi →». Sulla pagina della
  serie il più recente sta in alto.
- **da due serie in poi**: la colonna Appunti elenca **le serie**, non i pezzi — nome, cornice
  di una riga, quanti pezzi, l'ultimo uscito. A quel punto ha la stessa forma di Works.

Due cose che non cambiano mai: **nessuna data** sui pezzi, e **nessuna cadenza dichiarata**.
Una cadenza è una promessa che il sito mostra ogni volta che la manchi, ed è il modo in cui
muoiono tutte le sezioni simili del campione.
