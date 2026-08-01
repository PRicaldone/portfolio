# Il file di un'opera per il sito — standard di consegna

**Vale per ogni opera, di ogni collezione, presente e futura** (deciso fra l'1 e il 2 agosto
2026, guardando Act I sul sito). Un file solo per opera, lo stesso in Home e nella pagina
opera: cambia soltanto chi preme play.

## Il principio

Le opere **non sono looped**: ognuna ha una durata precisa e finisce, e il residuo che lascia
sta nella memoria di chi guarda. Il sito rispetta questo. L'opera parte, arriva alla fine e
**resta ferma sull'ultimo fotogramma**: il deposito — l'ultimo movimento dell'arco emotivo —
dura quanto lo spettatore vuole, invece di essere cancellato da una ripartenza.

**Il replay lo decide chi guarda.** In Home il comando passa a *Rivedi* quando l'opera è
finita; nella pagina opera ci sono i controlli del player. Non siamo in sala: su un dispositivo
personale il tempo è di chi guarda.

> **Storia, per non ripercorrerla.** Fra il 31 luglio e l'1 agosto il sito ha avuto il loop, e
> si era costruita una chiusura per renderlo sopportabile: tenuta sull'ultimo fotogramma,
> dissolvenza di 0,75 s, due secondi di nero. Quella soluzione — la «versione LOOP» — è stata
> superata: senza ripartenza, dissolvenza e nero non servono a niente, e il file torna a essere
> **l'opera senza aggiunte**. La versione LOOP resta valida **solo** per un allestimento che
> imponga la ripetizione e non sia governabile: lì la chiusura va costruita nel file, perché
> non si può contare sul player. Comando e misure in `atelier-opera-post-production`.

## L'export da Resolve — preset `my_WEB`

Un solo file, `…_SITE_2560x1920_25p_H264.mp4`, in `1_OPERA/` accanto al master.

| | |
|---|---|
| Format / Codec | MP4 · H.264 |
| Network Optimization | **attivo** (è il `faststart`: il video parte prima che il download finisca) |
| Resolution | **2560 × 1920** (Custom) |
| Frame rate | Timeline Frame Rate |
| Output Color Space / Gamma | Same as Timeline (Rec.709 Gamma 2.4) |
| Quality | **Restrict to 1000 Kb/s** |
| Encoding Profile | High · Entropy Auto · Frame reordering attivo |
| Multi-pass encode | **no** |
| Export Audio | **disattivato** — le opere sono mute e non devono portarsi dietro una traccia silente |

**Perché 2560.** I contenitori del sito arrivano a 1216 px CSS, che su schermo retina sono 2432
px fisici; 1920 non li copre. 2560 li copre con margine e copre anche il fullscreen di qualsiasi
telefono. Resta metà esatta del master: **la piena risoluzione è dell'originale**, e la targa lo
dichiara.

**Perché 1000 Kb/s.** Misurato: a questo bitrate la fedeltà rispetto a un export a 4,37 Mbps è
0,9976, e il file sta sotto gli 11 MB per un'opera di 78 secondi. Salire non si vede, scendere
sì.

**Perché niente multi-pass.** Serve quando il bitrate è stretto e ogni bit conta: il primo
passaggio analizza, il secondo scrive. A 1000 Kb/s su questo materiale il guadagno è minimo e
il tempo raddoppia.

**Perché da Resolve e non con ffmpeg.** La riduzione da 10 a 8 bit va fatta con **dither**, che
Resolve applica e un comando ffmpeg no: sui gradienti lunghi a bassa luminanza è esattamente
lì che nasce il banding. E ricomprimere un H.264 già compresso costa il doppio in peso a parità
di resa — misurato: 15 MB contro 8, per lo stesso CRF.

## Verificare, sempre, prima di pubblicare

**Il controllo che conta più di tutti** — decodifica completa del file:

```sh
ffmpeg -v error -i <file>.mp4 -f null -
```

**Silenzio significa integro.** Se stampa righe `error while decoding MB`, il file è corrotto e
va rifatto. Non fidarsi mai della dimensione o del fatto che si apra: il 2 agosto 2026 due job
in coda su Resolve hanno scritto sullo stesso file, e il risultato aveva metadati perfetti,
peso plausibile e contenuto illeggibile. **Un solo job per file nella Render Queue.**

Poi i parametri e i bordi:

```sh
ffprobe -v error -show_entries stream=width,height,nb_frames -show_entries format=duration,size -of default=nw=1 <file>.mp4
```

Il **numero di fotogrammi deve corrispondere al master** (Act I: 1940 · Act II: 945). Uno scarto
di uno è tollerato sui derivati web; trentuno no, e vuol dire che l'in/out del Deliver è
spostato. E l'ultimo fotogramma non deve essere nero:

```sh
ffmpeg -i <file>.mp4 -vf "select='gte(n,<ultimi>)',signalstats,metadata=print:key=lavfi.signalstats.YAVG:file=-" -vsync 0 -f null -
```

Su video levels **16 è il nero**; il valore a piena immagine dipende dall'opera (Act I ~24,9 ·
Act II ~19,5).

## Il file nel sito

`assets/{opera}-site.mp4` in questo repo. Il tag è nativo — **niente embed di terzi**: un player
esterno non garantisce la tenuta sull'ultimo fotogramma, che dipenderebbe da un'impostazione nel
pannello di qualcun altro, e ricomprime il file a parametri che non decidiamo noi.

In Home: `autoplay muted playsinline`, **senza `loop`**, col comando che diventa *Rivedi* a fine
opera. Nella pagina opera: `controls controlsList="nodownload"`, `preload="metadata"`, **senza
autoplay** — lì è lo spettatore che comincia.

> `nodownload` toglie il pulsante di scaricamento, non impedisce il download: il file resta
> raggiungibile per indirizzo. Non è una protezione, è una dichiarazione — il sito è dove
> l'opera si guarda, non dove si preleva. La scarsità sta sull'esemplare certificato, mai sul
> file pubblicato.

## La targa

```
silent · single-channel · 4:3 · plays once, holding on the final frame
shown here at 2560 × 1920 · the single certified original is 3840 × 2880, ProRes 422 HQ
```

E in italiano: *si riproduce una volta, con tenuta sull'ultimo fotogramma* · *presentato qui a
2560 × 1920 · l'originale unico certificato è 3840 × 2880, ProRes 422 HQ*.

La seconda riga è un **dato**, non un argomento di vendita: senza, chi guarda crede che la
versione pubblicata sia l'opera. È lo stesso gesto della riga che dichiara uno still come still.

**Perché nomina anche l'unicità e il certificato** *(2 ago 2026)*. La scheda tecnica porta già
la riga *Edition · Single original, certified by the artist*, ma sta in un'altra cella e il
legame fra le due informazioni non arrivava: chi legge «2560, l'originale è 3840» pensa a un
file più grande da qualche parte, non a un esemplare unico. Le due cose vanno dette insieme,
nel punto in cui chi guarda si chiede cosa ha davanti.

## Quando la Home cambia opera

Si tocca un punto solo, `HOME_WORK` nel generatore. Il file c'è già, perché la versione SITE si
produce **per ogni opera** e non solo per quella in vetrina.

## Con decine di opere

Circa 5-11 MB per opera: il repo regge finché sono poche. Git conserva ogni versione per
sempre, quindi quando il corpus cresce conviene spostare i video su object storage (Cloudflare
R2, Backblaze B2) e lasciare che il tag `<video>` punti lì. Per questo il percorso dei file va
tenuto **in un punto solo** del generatore: il giorno del trasloco si cambia una riga.
