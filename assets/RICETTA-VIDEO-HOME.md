# Il video della home — come si produce

La Home mostra **una sola opera**, autoplay muto in loop, scelta da Paolo. Il file in `assets/`
è un **derivato di distribuzione**: la sorgente non vive qui, e non deve mai vivere qui.

## Dove stanno le cose

- **Master dell'opera** — disco interno del Mac,
  `___PRicaldone/Works/_ARCHIVIO_FINALE/The_Stage/{opera}/1_OPERA/…_MASTER_3840x2880_25p_ProRes422HQ.mov`.
  L'HDD esterno ne tiene la copia. Mai su Google Drive (segnaposto da zero byte, 27-28 lug 2026).
- **Export web larghi** — stessa cartella d'archivio, `…_WEB_1920x1440_25p_H264.mp4`. Sono i file
  che escono da Resolve, pesanti (Act I: 160 MB) perché a bitrate fisso alto. **Non vanno in git**:
  GitHub rifiuta i file singoli oltre i 100 MB.
- **Home version** — stessa cartella d'archivio, `…_HOME_1920x1440_25p_H264.mp4`. È il file
  prodotto con la ricetta qui sotto. Se ne tiene una **per ogni opera**, così quando la Home cambia
  opera basta copiare, senza riaprire Resolve.
- **Il file online** — `assets/act-i-home.mp4` in questo repo, cioè una copia della home version
  dell'opera attualmente in Home. **Solo quella**: git conserva ogni versione per sempre, e usare
  il repo come archivio lo farebbe crescere a ogni cambio.

## L'export da Resolve

1920×1440 (metà esatta del master 3840×2880, 4:3), 25p, H.264 a bitrate alto o ProRes. Non serve
che sia già leggero: la compressione web la fa il comando qui sotto.

Rec.709, video levels. **Export Audio disattivato** — le opere sono mute e non devono portarsi
dietro una traccia silente (regola del 27 lug 2026).

## La coda

Il video di Home non finisce di colpo: tiene l'ultimo fotogramma, dissolve, resta nero, poi
riparte. È il modo delle sale, e serve a proteggere il deposito emotivo dell'opera da un loop
che ripartirebbe sopra il finale.

Misure di Act I, da replicare: **1,9 s di tenuta**, **1,06 s di dissolvenza**, **1,2 s di nero**.

## Il comando

```sh
ffmpeg -i <export-web>.mp4 \
  -vf "trim=end_frame=<N>,setpts=PTS-STARTPTS,tpad=stop_mode=clone:stop_duration=2.96,fade=t=out:st=79.5:d=1.06,tpad=stop_mode=add:stop_duration=1.2:color=black" \
  -c:v libx264 -preset slow -crf 18 -pix_fmt yuv420p \
  -colorspace bt709 -color_primaries bt709 -color_trc bt709 \
  -movflags +faststart -an \
  <opera>-home.mp4
```

**CRF 18** è il valore scelto misurando (1 ago 2026). A quel livello il file è indistinguibile
dalla sorgente da 160 MB — verificato ingrandendo la zona di sfumatura sul cemento con contrasto
forzato — e pesa 5,4 MB. Scendere non conviene: il guadagno di peso è invisibile, la perdita no.
Il valore vale finché il materiale resta questo; se un'opera avrà grana vera, si rimisura.

`st=79.5` è l'istante in cui parte la dissolvenza, e va ricalcolato per ogni opera:
`durata_opera + 1.9`. `stop_duration=2.96` è tenuta più dissolvenza.

## Il fotogramma nero — trappola di Act I

L'export web di Act I ha **1941 fotogrammi**, uno più del master mintato, e **l'ultimo è nero**
(luminanza 16 contro 24,94 dei precedenti). Viene dal re-render del 16 lug 2026, che
`Studio/vendite/opere/act-i-i-have-to/identificazione.md` dichiara materiale superato.

Se non lo si scarta, `tpad=stop_mode=clone` clona **quel** fotogramma: il video va a nero di colpo
alla fine dell'opera e ci resta quattro secondi, cioè sparisce esattamente la tenuta che la coda
esiste per proteggere. Il file sembra corretto per durata e per peso, e l'errore si vede solo
misurando la luminanza.

Da qui il `trim=end_frame=1940` nel comando. Per le altre opere si verifica prima:

```sh
ffmpeg -i <file>.mp4 -vf "select='gte(n,<ultimi>)',signalstats,metadata=print:key=lavfi.signalstats.YAVG:file=-" -vsync 0 -f null -
```

## Verifica prima di pubblicare

```sh
ffprobe -v error -show_entries stream=width,height,nb_frames -show_entries format=duration,size -of default=nw=1 <file>.mp4
ffmpeg -i <file>.mp4 -vf blackdetect=d=0.05:pix_th=0.03 -f null -
```

Attesi per Act I: 1920×1440, 81,76 s, 5,4 MB, nero da 80,48 a 81,72.

Il giudizio visivo è di Paolo: niente server locale, niente Playwright — si guarda il file, si
pubblica, si controlla l'URL live con `curl` (regola del 14 lug 2026).

## Quando la Home cambia opera

Si tocca un punto solo: il file in `assets/` e la riga di targa nel generatore. L'ordine dentro
Works non cambia — la scelta della Home è ortogonale alla sequenza della collezione.
