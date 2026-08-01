# La versione LOOP di un'opera — standard di consegna

**Vale per ogni opera, di ogni collezione, presente e futura** (deciso l'1 agosto 2026
guardando Act I in loop sul sito, dopo quattro prove). Non è una regola di *The Stage*: è il
modo in cui un'opera si mostra ovunque venga riprodotta più di una volta — home del sito,
pagina opera, monitor in mostra.

## Il problema che risolve

Le opere non sono looped: ognuna ha una durata precisa e finisce, e il residuo che lascia sta
nella memoria di chi guarda. Ma ovunque si mostrino davvero — un sito, una sala — il
dispositivo le ripete. E un ciclo che riparte di colpo **cancella il deposito**, cioè l'ultimo
movimento dell'arco emotivo, che è la parte che l'opera consegna per ultima.

La chiusura si costruisce **nel file** e non nel player: così funziona su qualsiasi dispositivo,
senza dipendere da JavaScript, da un lettore o da chi allestisce.

## Lo standard

**In ingresso, niente.** L'opera parte a piena luminosità dal primo fotogramma. Nessun nero,
nessuna dissolvenza. Lo stato emotivo è presente fin dal primo frame — è il principio guida
della costruzione — e un fade in trasformerebbe l'irruzione in un avvicinamento. Il nero che
precede, alla fine del ciclo prima, lavora già come stacco.

**Nessuna tenuta.** L'opera corre fino al suo ultimo fotogramma. Un fermo immagine aggiunto
allunga l'opera con un tempo che l'autore non ha scritto, e su un'opera che chiude in
movimento — Act I accelera nell'ultimo secondo e mezzo — la ferma al posto suo.

**Dissolvenza: 0,75 s**, e cade su un fotogramma **clonato dopo la fine**, non sugli ultimi
fotogrammi dell'opera. Nessun fotogramma dell'opera viene mai oscurato mentre il movimento è
ancora in corso: è ciò che permette di dire che questo file non è una seconda opera.

**Nero: 2 s** prima che il ciclo riparta.

> **Perché la simmetria non si applica.** In uscita si sfuma qualcosa che è stato aggiunto
> dopo la fine; in entrata si sfumerebbe l'opera stessa. E la fine ha bisogno di protezione
> perché il loop la cancella, mentre l'inizio non ha niente da proteggere. Le due estremità
> non sono lo stesso problema, e trattarle allo stesso modo sarebbe una coerenza solo formale.

## Dove stanno le cose

- **Master** — disco interno del Mac, `___PRicaldone/Works/_ARCHIVIO_FINALE/{collezione}/{opera}/1_OPERA/…_MASTER_….mov`.
  ProRes, risoluzione piena. L'HDD esterno ne tiene la copia. Mai su Google Drive.
- **Export web largo** — stessa cartella, `…_WEB_….mp4`. Quello che esce da Resolve, pesante
  perché a bitrate fisso alto (Act I: 160 MB). **Non va in git**: GitHub rifiuta i file oltre
  i 100 MB.
- **Versione LOOP** — stessa cartella, `…_LOOP_….mp4`. Il file prodotto con questa ricetta.
  Se ne tiene una **per ogni opera**, non solo per quella in vetrina: lo slot della Home è una
  scelta d'autore che cambia, e senza la variante pronta cambiarla costa un giro di export.
- **Il file online** — `assets/{opera}-home.mp4` in questo repo: copia della versione LOOP
  dell'opera attualmente in Home. Solo quella, perché git conserva ogni versione per sempre.

## L'export da Resolve

Metà esatta della risoluzione del master (per un master 3840×2880: **1920×1440**, 4:3), stesso
frame rate, H.264 a bitrate alto oppure ProRes. Non serve che sia leggero: la compressione web
la fa il comando qui sotto.

Rec.709, video levels. **Export Audio disattivato** — le opere sono mute e non devono portarsi
dietro una traccia silente.

## Il comando

```sh
ffmpeg -i <export-web>.mp4 \
  -vf "trim=end_frame=<N>,setpts=PTS-STARTPTS,tpad=stop_mode=clone:stop_duration=0.75,fade=t=out:st=<durata_opera>:d=0.75,tpad=stop_mode=add:stop_duration=2:color=black" \
  -c:v libx264 -preset slow -crf 18 -pix_fmt yuv420p \
  -colorspace bt709 -color_primaries bt709 -color_trc bt709 \
  -movflags +faststart -an \
  <opera>_LOOP.mp4
```

`<N>` è il numero di fotogrammi dell'opera, `<durata_opera>` l'istante in cui finisce (per Act I:
1940 e 77.6). Il `trim` serve anche a scartare eventuali fotogrammi spuri in coda — vedi sotto.

**CRF 18** scelto misurando (1 ago 2026): a quel livello il file è indistinguibile dalla
sorgente da 160 MB, verificato ingrandendo la zona di sfumatura sul cemento con contrasto
forzato, e pesa circa 5 MB. Scendere non conviene, il guadagno è invisibile e la perdita no.
Se un'opera futura avrà grana vera, si rimisura.

## Verificare, sempre

```sh
ffprobe -v error -show_entries stream=width,height,nb_frames -show_entries format=duration,size -of default=nw=1 <file>.mp4
ffmpeg -i <file>.mp4 -vf blackdetect=d=0.05:pix_th=0.03 -f null -
```

E il profilo della chiusura, che è la cosa che gli occhi non controllano da soli:

```sh
for t in <fine-0.1> <fine+0.2> <fine+0.5> <fine+1.0>; do
  ffmpeg -loglevel error -ss $t -i <file>.mp4 -frames:v 1 \
    -vf "signalstats,metadata=print:key=lavfi.signalstats.YAVG:file=-" -f null - 2>/dev/null | grep -o "YAVG=[0-9.]*"
done
```

Su video levels, **16 è il nero** e il valore a piena immagine dipende dall'opera. Per Act I:
24,9 fino a 77,5 s, poi la discesa, nero pieno da 78,5.

## Fotogrammi spuri in coda — controllare prima

L'export web di Act I ha **un fotogramma nero in più** rispetto al master, residuo di un
re-render superato. Se non si scarta, `tpad=stop_mode=clone` clona **quello**: il video va a
buio di colpo alla fine e ci resta, cioè sparisce esattamente la chiusura che stiamo
costruendo. Il file sembra corretto per durata e per peso, e l'errore si vede solo misurando.

Controllare **sempre** gli ultimi fotogrammi di un export prima di usarlo:

```sh
ffmpeg -i <file>.mp4 -vf "select='gte(n,<ultimi>)',signalstats,metadata=print:key=lavfi.signalstats.YAVG:file=-" -vsync 0 -f null -
```

Storia e dettaglio: `Studio/vendite/opere/act-i-i-have-to/identificazione.md`.

## Quando la Home cambia opera

Si tocca un punto solo: il file in `assets/` e la riga di targa nel generatore. L'ordine dentro
Works non cambia — la scelta della Home è ortogonale alla sequenza della collezione.

Il giudizio visivo è di Paolo: niente server locale, niente Playwright. Controlli automatici
prima, `curl` sull'URL live dopo, e l'occhio è il suo.
