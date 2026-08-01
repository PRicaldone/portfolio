#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Controlli sul sito generato — innesto dalla versione di Codex.

Servono a rendere verificabili le cose che altrimenti sono promesse: la parità
fra le due lingue, i link che risolvono, e le regole della ricerca che non si
vedono guardando la pagina (lessico on-chain, prezzi, date che invecchiano).

Uso:  python3 _build/test.py
Esce con codice 1 se un controllo fallisce, così si può incatenare al build.
"""

import os, re, sys

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
SKIP = ("_source", "_build")

fails, checks = [], 0

def check(cond, msg):
    global checks
    checks += 1
    if not cond:
        fails.append(msg)

def pages():
    for d, _, fs in os.walk(ROOT):
        if any(s in d for s in SKIP):
            continue
        for f in sorted(fs):
            if f.endswith(".html"):
                p = os.path.join(d, f)
                yield os.path.relpath(p, ROOT).replace(os.sep, "/"), p

ALL = dict(pages())
EN = {k: v for k, v in ALL.items() if not k.startswith("it/")}
IT = {k: v for k, v in ALL.items() if k.startswith("it/")}

# ------------------------------------------------------------------ parità

check(len(EN) > 0, "nessuna pagina inglese trovata")
check(len(EN) == len(IT), f"le due lingue non hanno lo stesso numero di pagine: EN {len(EN)}, IT {len(IT)}")
for k in EN:
    check("it/" + k in IT, f"manca la gemella italiana di {k}")
for k in IT:
    check(k[3:] in EN, f"la pagina italiana {k} non ha gemella inglese")

# ------------------------------------------------- link, lingua, intestazione

# Parole inequivocabili: vietate ovunque nel testo visibile.
VIETATE = ["nft", "mint", "minted", "blockchain", "ethereum", "etherscan",
           "token", "not looped", "non-looped"]
# Parole del lessico di mercato che in inglese sono anche parole comuni
# («let it drop»): si controllano solo dove sarebbero identità, cioè nel
# titolo della pagina, nella navigazione e nelle intestazioni.
VIETATE_IN_TESTATE = ["drop", "floor", "listing", "holder"]

for rel, path in ALL.items():
    t = open(path, encoding="utf-8").read()
    d = os.path.dirname(path)
    lang = "it" if rel.startswith("it/") else "en"

    # ogni riferimento locale punta a un file che esiste
    for m in re.findall(r'(?:href|src)="([^"]+)"', t):
        if m.startswith(("http", "mailto:", "#")):
            continue
        target = os.path.normpath(os.path.join(d, m.split("#")[0]))
        check(os.path.isfile(target), f"{rel}: riferimento rotto → {m}")

    check(f'<html lang="{lang}"' in t, f"{rel}: attributo lang mancante o sbagliato")
    check('rel="alternate"' in t, f"{rel}: manca il link alla gemella nell'altra lingua")
    check('class="site-nav"' in t, f"{rel}: manca la barra di navigazione")
    check('favicon-32.png' in t, f"{rel}: manca il favicon")
    check('<title>' in t and '</title>' in t, f"{rel}: manca il titolo")
    check(re.search(r'<meta name="description" content="[^"]+"', t) is not None,
          f"{rel}: descrizione mancante o vuota")

    # regole della ricerca che non si vedono a occhio
    visible = re.sub(r"<[^>]+>", " ", t).lower()
    for w in VIETATE:
        check(re.search(rf"\b{re.escape(w)}\b", visible) is None,
              f"{rel}: parola vietata nel testo visibile → «{w}»")
    testate = " ".join(x for tup in re.findall(r"<title>(.*?)</title>|<h[1-3][^>]*>(.*?)</h[1-3]>",
                                               t, flags=re.S | re.I) for x in tup)
    testate = re.sub(r"<[^>]+>", " ", testate).lower()
    for w in VIETATE_IN_TESTATE:
        check(re.search(rf"\b{w}\b", testate) is None,
              f"{rel}: lessico di mercato in una posizione identitaria → «{w}»")
    check(re.search(r"[€$]\s?\d", visible) is None, f"{rel}: sembra esserci un prezzo")
    # nessuna data morta: gli anni ammessi sono quelli delle opere, dentro le schede.
    # Le misure in pixel non sono date: "2560 × 1920" contiene un 1920 che non è
    # un anno, e va tolto prima di cercare, altrimenti la targa fa fallire il test.
    senza_misure = re.sub(r"\d{3,4}\s*×\s*\d{3,4}", "", visible)
    for y in re.findall(r"\b(19\d\d|20\d\d)\b", senza_misure):
        check(y in ("2026", "1968"), f"{rel}: anno inatteso in pagina → {y}")

# ------------------------------------------------------------ struttura viva

home = ALL["index.html"]
t = open(home, encoding="utf-8").read()
check("autoplay" in t, "la Home non parte da sola senza JavaScript")
check("muted" in t, "il video della Home non è muto per attributo")
# Dall'1 ago 2026 la Home non ripete: l'opera finisce e resta sull'ultimo
# fotogramma, come nella pagina opera. Il replay lo decide chi guarda.
check(" loop" not in t, "la Home è tornata in loop: l'opera deve finire e restare sull'ultimo fotogramma")
check("act-i-site.mp4" in t, "la Home non usa il file dell'opera")
check("home-video-toggle" in t, "manca il comando Play/Pausa")

works = open(ALL["works/index.html"], encoding="utf-8").read()
check("<video" not in works, "l'indice Works contiene un video: deve avere solo fermi immagine")
check(works.count("<img") >= 2, "l'indice Works non mostra i fermi immagine")
check("I Don't" in works, "Act III non è dichiarato nell'indice")
check(re.search(r"I Don't.*?20\d\d", works, flags=re.S) is None,
      "Act III porta una data: deve essere solo titolo e posizione")

for slug in ("i-have-to", "i-could"):
    p = ALL.get(f"works/{slug}/index.html")
    check(p is not None, f"manca la pagina opera {slug}")
    if p:
        w = open(p, encoding="utf-8").read()
        # Dall'1 ago 2026 il player è nativo: niente terzi fra l'opera e chi guarda,
        # e la tenuta sull'ultimo fotogramma non dipende dal pannello di nessuno.
        check("player.vimeo.com" not in w, f"{slug}: è tornato un embed di terzi")
        check("<video" in w, f"{slug}: manca il player nativo")
        check("autoplay" not in w, f"{slug}: il player parte da solo, non deve")
        check(" loop" not in w, f"{slug}: il video è in loop, deve finire e restare")
        check("controls" in w, f"{slug}: mancano i controlli, lo spettatore non può avviare")
        check("2560" in w and "3840" in w,
              f"{slug}: la targa non dichiara risoluzione mostrata e originale")

for n in ("001", "002", "003", "004", "005"):
    check(f"writing/silences/{n}/index.html" in ALL, f"l'appunto {n} non ha una pagina propria")

about = open(ALL["about/index.html"], encoding="utf-8").read()
check("1968" in about, "About non porta il blocco fattuale")
check("paolo-ricaldone.jpg" in about, "About non porta il ritratto")

contact = open(ALL["contact/index.html"], encoding="utf-8").read()
check("mailto:" in contact, "Contact non ha l'email cliccabile")
check(sum("mailto:" in open(p, encoding='utf-8').read() for p in ALL.values()) == 2,
      "l'email compare fuori da Contact: deve stare solo lì (una volta per lingua)")

# ----------------------------------------------------------------- esito

print(f"{checks} controlli su {len(ALL)} pagine")
if fails:
    print(f"\n{len(fails)} falliti:")
    for f in fails:
        print("  ✗", f)
    sys.exit(1)
print("tutto a posto")
