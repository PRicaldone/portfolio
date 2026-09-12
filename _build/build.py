#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Generatore del sito — versione mix (v2), 30 luglio 2026.

Base: la v1 di Claude. Innesti decisi in CONFRONTO.md § Decisioni prese:
impianto d'ingresso di Codex (margine, barra centrale, targa), still nell'indice
Works, pagina propria per opera e per appunto, alberi /it/ speculari.

I testi non sono scritti qui: si estraggono verbatim dagli snapshot in _source/
e si allineano al master con le correzioni registrate in REWRITES.
"""

import os, re

# PREVIEW=1 marca le pagine come non indicizzabili (pubblicazione parallela)
PREVIEW = os.environ.get('PREVIEW') == '1'
SITE = 'https://pricaldone.art'

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
SRC = os.path.join(ROOT, "_source")

# ---------------------------------------------------------------- estrazione

def clean(t):
    t = re.sub(r"<script.*?</script>", "", t, flags=re.S)
    return re.sub(r"<style.*?</style>", "", t, flags=re.S)

def load(name):
    with open(os.path.join(SRC, name), encoding="utf-8") as f:
        return clean(f.read())

REWRITES = [
    ("Creo le opere interamente in CGI, per non avere limiti di possibilità comunicativa e poter astrarre senza sentirmi imbrigliato dalla realtà. Ogni fotogramma è una decisione, ogni movimento è sentito.",
     "Creo le opere interamente in CGI, per non avere limiti di possibilità comunicativa e poter astrarre senza sentirmi imbrigliato dalla realtà: ogni fotogramma è una decisione, ogni movimento è sentito. Oggi non uso AI generativa, non per opposizione allo strumento, ma perché non mi dà il controllo e la responsabilità autoriale che cerco."),
    ("Oggi non uso AI generativa nel mio lavoro: non per opposizione allo strumento, ma perché non mi offre il controllo e la responsabilità autoriale che cerco, fino all'ultimo pixel.", ""),
    ("I create the works entirely in CGI, to have no limits on what can be communicated and to abstract without being bound by reality. Every frame is a decision, every movement is felt.",
     "I create the works entirely in CGI, to have no limits on what can be communicated and to abstract without being bound by reality: every frame is a decision, every movement is felt. Today I do not use generative AI, not out of opposition to the tool, but because it does not offer the control and the authorial responsibility I seek."),
    ("Today I do not use generative AI in my work: not out of opposition to the tool, but because it does not offer the control and the authorial responsibility I seek, down to the final pixel.", ""),
    ("My works are born from instinct, when something becomes visceral. What I create is not a message to deliver, nor a code to decipher.",
     "What I create is not a message to deliver, nor a code to decipher."),
    ("Le mie opere nascono dall'istinto, quando qualcosa diventa viscerale. Quello che creo non è un messaggio da consegnare, né un codice da decifrare.",
     "Quello che creo non è un messaggio da consegnare, né un codice da decifrare."),
    ("I give this energy body by staging space, matter, light, and time.",
     "I give body to emotion by staging space, matter, light, and time."),
    ("Do corpo a questa energia mettendo in scena spazio, materia, luce e tempo.",
     "Do corpo all'emozione mettendo in scena spazio, materia, luce e tempo."),
]

def revise(s):
    for a, b in REWRITES:
        s = s.replace(a, b)
    return s

def paragraphs(block):
    out = (revise(p.strip()) for p in re.findall(r"<p[^>]*>(.*?)</p>", block, flags=re.S))
    return [p for p in out if p]

def texts_content(fn):
    t = load(fn)
    intro = paragraphs(re.search(r'<div class="texts-intro">(.*?)</div>\s*<div class="texts-layout">', t, flags=re.S).group(1))
    sidebar = re.search(r'<nav class="texts-sidebar">(.*?)</nav>', t, flags=re.S).group(1)
    titles = {}
    for tid, body in re.findall(r'<a class="sidebar-item[^"]*"\s+data-target="([^"]+)">(.*?)</a>', sidebar, flags=re.S):
        lab = re.search(r'<div class="sidebar-label">(.*?)</div>', body, flags=re.S)
        tit = re.search(r'<div class="sidebar-title">(.*?)</div>', body, flags=re.S)
        titles[tid] = (lab.group(1).strip() if lab else "", tit.group(1).strip() if tit else "")
    panels = {}
    for pid, body in re.findall(r'<div class="text-panel[^"]*" id="([^"]+)">(.*?)(?=<div class="text-panel|</div>\s*</div>\s*</div>)', t, flags=re.S):
        panels[pid] = paragraphs(body)
    return intro, titles, panels

def about_paragraphs(fn):
    t = load(fn)
    block = re.search(r'<div class="text-section">(.*?)</div>\s*</div>\s*</div>', t, flags=re.S).group(1)
    out = []
    for tb in re.findall(r'<div class="text-block">(.*?)</div>', block, flags=re.S):
        tb = re.sub(r'<span class="highlight">(.*?)</span>', r"\1", tb, flags=re.S)
        tb = re.sub(r'<span class="text-line">|</span>', "", tb)
        for line in re.split(r"<br\s*/?>", tb):
            line = revise(" ".join(line.split()))
            if line:
                out.append(line)
    return out

TX = {"en": texts_content("live_texts.html"), "it": texts_content("live_it_texts.html")}
AB = {"en": about_paragraphs("live_about.html"), "it": about_paragraphs("live_it_about.html")}

# ------------------------------------------------------------ ordini e testi

ORDER = {
    "en": ["I give body to emotion", "in its essence", "propagates like a wave",
           "emotional state staged", "visual treatment", "firm principle"],
    "it": ["Do corpo all'emozione", "nella sua essenza", "si propaga come un'onda",
           "Lo stato emotivo", "Il trattamento visivo", "Da qui un principio"],
}
DROP = {"en": "message to deliver", "it": "Quello che creo"}

def reorder(items, keys, drop):
    items = [x for x in items if drop not in x]
    out, left = [], list(items)
    for k in keys:
        for i, x in enumerate(left):
            if k in x:
                out.append(left.pop(i))
                break
    return out + left

TX_INTRO = {l: reorder(TX[l][0], ORDER[l], DROP[l]) for l in ("en", "it")}
TX_ORDER = ["t1", "t2", "t3", "t4", "t5", "t6", "t7", "method"]

def pick(items, *keys):
    out = []
    for k in keys:
        for x in items:
            if k in x:
                out.append(x)
                break
    return out

REL = {
 "en": "My drive to create has a relational root. I create the works to make people feel, physically. I cannot hold emotions back: I want those close to me to feel them. I start from my own, but I know the reading belongs to whoever watches, open, theirs.",
 "it": "La mia spinta alla creazione ha una radice relazionale. Creo le opere per far sentire, fisicamente. Non riesco a trattenere le emozioni: voglio che chi mi è vicino le senta. Parto dalla mia, ma so che la lettura è di chi guarda, aperta, sua.",
}
ABOUT = {}
for _l, _keys in (("en", ("the stomach that reacts first", "do not begin from concepts",
                          "interpretive keys", "craft begins", "entirely in CGI", "single original")),
                  ("it", ("lo stomaco a reagire per primo", "non nascono da concetti",
                          "chiavi di lettura", "mestiere comincia", "interamente in CGI", "originale unico"))):
    _p = pick(AB[_l], *_keys)
    ABOUT[_l] = [_p[0] + " " + _p[1], REL[_l]] + _p[2:]

FACTS = {
 "en": ["Paolo Ricaldone (Turin, 1968) lives and works in Turin.",
        "He works with silent single-channel video, made entirely in CGI.",
        "<em>The Stage — Acts of a Lucid Silence</em>, a trilogy in three acts begun in 2026, is the current body of work."],
 "it": ["Paolo Ricaldone (Torino, 1968) vive e lavora a Torino.",
        "Lavora con video muti single-channel, realizzati interamente in CGI.",
        "<em>The Stage — Acts of a Lucid Silence</em>, trilogia in tre atti iniziata nel 2026, è il corpus in corso."],
}

# Opere — dati dai record del vault. Nessun dato dedotto.
WORKS = [
 # Un file per opera, lo stesso in Home e nella pagina opera: cambia solo chi
 # preme play. Via l'embed Vimeo (1 ago 2026) — il player di terzi non garantisce
 # la tenuta sull'ultimo fotogramma, che dipendeva da un'impostazione nel loro
 # pannello, e ricomprime il file a parametri che non decidiamo noi.
 {"slug": "i-have-to", "act": "Act I", "title": "I Have To", "year": "2026",
  "anchor": "act-i", "video": "act-i-site.mp4", "poster": "act-i-poster.jpg",
  "duration": "01:18", "res": "3840 × 2880 (4:3)", "fps": "25 fps"},
 {"slug": "i-could", "act": "Act II", "title": "I Could", "year": "2026",
  "anchor": "act-ii", "video": "act-ii-site.mp4", "poster": "act-ii-poster.jpg",
  "duration": "00:38", "res": "3840 × 2880 (4:3)", "fps": "25 fps"},
 # Act III è uscito il 6 set 2026: entra come le altre, con la sua pagina e il suo
 # anno. Sparisce con lui la riga d'attesa «In produzione» che teneva il posto in
 # fondo all'indice — la trilogia è completa e non c'è più nessun atto annunciato.
 # Durata e risoluzione misurate sul master (2800 frame a 25 fps = 112 s).
 {"slug": "i-dont", "act": "Act III", "title": "I Don't", "year": "2026",
  "anchor": "act-iii", "video": "act-iii-site.mp4", "poster": "act-iii-poster.jpg",
  "duration": "01:52", "res": "3840 × 2880 (4:3)", "fps": "25 fps"},
]
HOME_WORK = WORKS[0]        # slot d'autore: si cambia qui, e in nessun altro punto

EMAIL = "studio@pricaldone.art"
# Indirizzi presi dai record in Studio/account-profili/ (instagram.md)
# X tolto il 1 set 2026: canale dormiente, non si alimenta più — mandarci chi arriva dal
# sito significherebbe mandarlo su un profilo fermo. Record: Studio/account-profili/x.md.
SOCIAL = [("Instagram", "https://www.instagram.com/pricaldone.art/", "@pricaldone.art")]

T = {
 "en": {"other": "IT",
   "nav": [("works/", "Works"), ("writing/", "Writing"), ("about/", "About"), ("contact/", "Contact")],
   "skip": "Skip to content", "play": "Play", "pause": "Pause", "replay": "Play again",
   "collection_title": "The Stage — Acts of a Lucid Silence",
   "collection_frame": "A trilogy of 1/1 video works on a bare stage. Each act stages a single emotional state, present from the first frame, isolated from its cause.",
   "medium": "Silent video, single-channel, CGI",
   "edition": "Single original, certified by the artist",
   "behaviour": "silent · single-channel · 4:3 · plays once, holding on the final frame",
   # Dichiarare cosa si sta guardando: senza questa riga il visitatore crede che
   # la versione pubblicata sia l'opera. Dato, non argomento di vendita.
   "shown": "shown here at 2560 × 1920 · the single certified original is 3840 × 2880, ProRes 422 HQ",
   "viewing": "Best experienced on a large screen in a quiet space",
   "spec": ["Medium", "Duration", "Resolution", "Edition", "Year"],
   "works": "Works", "writing": "Writing", "about": "About", "contact": "Contact",
   "thought": "Thought", "essay": "Essay",
   "sections": "Sections", "sale": "Works are sold privately, directly by the artist.",
   "city": "Turin, Italy", "l_email": "Email", "l_studio": "Studio",
   "copyright": "© Paolo Ricaldone. All rights reserved."},
 "it": {"other": "EN",
   "nav": [("works/", "Opere"), ("writing/", "Scritti"), ("about/", "Chi sono"), ("contact/", "Contatti")],
   "skip": "Vai al contenuto", "play": "Riproduci", "pause": "Metti in pausa", "replay": "Rivedi",
   "collection_title": "The Stage — Acts of a Lucid Silence",
   "collection_frame": "Una trilogia di opere video 1/1 su un palco spoglio. Ogni atto mette in scena un singolo stato emotivo, presente dal primo istante, isolato dalla sua causa.",
   "medium": "Video muto, single-channel, CGI",
   "edition": "Originale unico, certificato dall'artista",
   "behaviour": "muto · single-channel · 4:3 · si riproduce una volta, con tenuta sull'ultimo fotogramma",
   "shown": "presentato qui a 2560 × 1920 · l'originale unico certificato è 3840 × 2880, ProRes 422 HQ",
   "viewing": "Da vivere su uno schermo grande, in uno spazio silenzioso",
   "spec": ["Medium", "Durata", "Risoluzione", "Edizione", "Anno"],
   "works": "Opere", "writing": "Scritti", "about": "Chi sono", "contact": "Contatti",
   "thought": "Pensiero", "essay": "Saggio",
   "sections": "Sezioni", "sale": "Le opere si vendono privatamente, direttamente dall'artista.",
   "city": "Torino, Italia", "l_email": "Email", "l_studio": "Studio",
   "copyright": "© Paolo Ricaldone. Tutti i diritti riservati."},
}

# ------------------------------------------------------------------- render

PAGES = []

def up(depth):
    return "../" * depth

def par(items, indent="    "):
    return "\n".join(f"{indent}<p>{x}</p>" for x in items)

def shell(lang, depth, title, desc, body, alt, body_class="", current="", script=False):
    t = T[lang]
    u = up(depth)
    other = "it" if lang == "en" else "en"
    # up() risale alla radice del sito, che è la radice dell'inglese: senza il
    # prefisso della lingua la barra di navigazione di una pagina italiana
    # riporta all'inglese, e il cambio lingua vale solo per la pagina a video.
    home = u + ("it/" if lang == "it" else "")
    nav = "\n".join(
        '      <a class="site-nav__link"{cur} href="{home}{href}index.html">{label}</a>'.format(
            cur=' aria-current="page"' if current == href else "", home=home, href=href, label=label)
        for href, label in t["nav"])
    js = f'\n<script src="{u}assets/js/site.js"></script>' if script else ""
    robots = '\n<meta name="robots" content="noindex, nofollow">' if PREVIEW else ""
    return f"""<!doctype html>
<html lang="{lang}">
<head>
<meta charset="utf-8">
<meta name="viewport" content="width=device-width, initial-scale=1">
<title>{title}</title>
<meta name="description" content="{desc}">
<link rel="icon" type="image/png" sizes="32x32" href="{u}assets/icons/favicon-32.png">
<link rel="icon" type="image/png" sizes="16x16" href="{u}assets/icons/favicon-16.png">
<link rel="apple-touch-icon" sizes="180x180" href="{u}assets/icons/apple-touch-icon.png">
<link rel="alternate" hreflang="{other}" href="{alt}">
<meta property="og:type" content="website">
<meta property="og:title" content="{title}">
<meta property="og:description" content="{desc}">
<meta property="og:image" content="{SITE}/og-image.jpg">
<meta property="og:locale" content="{'it_IT' if lang == 'it' else 'en_GB'}">
<meta name="twitter:card" content="summary_large_image">{robots}
<link rel="stylesheet" href="{u}assets/css/site.css">
</head>
<body class="{body_class}">
<a class="skip-link" href="#content">{t['skip']}</a>
<header class="site-header">
  <div class="site-header__inner">
    <a class="site-name" href="{home}index.html">Paolo Ricaldone</a>
    <nav class="site-nav" aria-label="{t['works']}">
{nav}
    </nav>
    <a class="language-link" href="{alt}" hreflang="{other}" lang="{other}">{t['other']}</a>
  </div>
</header>
<main id="content" class="site-main">
{body}
</main>
<footer class="site-footer"><small>{t['copyright']}</small></footer>{js}
</body>
</html>
"""

def emit(path, html):
    PAGES.append((path, html))

def build(lang):
    t = T[lang]
    pre = "it/" if lang == "it" else ""
    d = 1 if lang == "it" else 0

    def alt_of(rest):
        # la gemella sta nello stesso punto dell'albero dell'altra lingua
        return (up(d + rest.count("/")) + ("" if lang == "it" else "it/") + rest) if True else ""

    # ---- Home
    w = HOME_WORK
    body = f"""  <section class="home-stage" aria-labelledby="home-work-title">
    <div class="home-stage__media">
      <video class="home-stage__video" id="home-video" src="{up(d)}assets/{w['video']}"
             poster="{up(d)}assets/{w['poster']}" autoplay muted playsinline
             aria-label="{w['act']} — {w['title']}, {t['medium']}, {w['duration']}"></video>
    </div>
    <p class="media-toggle-row">
      <button class="media-toggle" type="button" id="home-video-toggle"
              aria-controls="home-video" aria-pressed="true"
              data-play="{t['play']}" data-pause="{t['pause']}" data-replay="{t['replay']}" hidden>
        <span class="media-toggle__icon" aria-hidden="true"></span>
        <span class="visually-hidden">{t['pause']}</span>
      </button>
    </p>
    <div class="home-stage__caption">
      <p class="eyebrow">{t['collection_title']}</p>
      <h1 id="home-work-title"><span>{w['act']}</span><cite>{w['title']}</cite></h1>
    </div>
  </section>"""
    emit(pre + "index.html",
         shell(lang, d, f"Paolo Ricaldone — {w['title']}",
               "Paolo Ricaldone — silent single-channel video, made entirely in CGI.",
               body, alt_of("index.html"), "home-page", script=True))

    # ---- Works: indice a fermi immagine
    rows = []
    for x in WORKS:
        rows.append(f"""        <li class="work-row" id="{x['anchor']}">
          <a class="work-row__link" href="{x['slug']}/index.html">
            <!-- Niente loading="lazy" sui fermi immagine dell'indice: sono tre file da una
                 quindicina di kilobyte l'uno, e il rinvio non risparmiava banda ma faceva
                 comparire gli still uno dopo l'altro. Il posto è già riservato dal CSS
                 (aspect-ratio 4/3), quindi non c'è salto di impaginazione. -->
            <span class="work-row__still"><img src="{up(d + 1)}assets/{x['poster']}" alt=""></span>
            <span class="work-row__text">
              <span class="eyebrow">{x['act']}</span>
              <cite class="work-row__title">{x['title']}</cite>
              <span class="work-row__meta">{t['medium']} · {x['duration']} · {x['year']}</span>
            </span>
          </a>
        </li>""")
    body = f"""  <div class="page">
    <div class="page-heading"><h1>{t['works']}</h1></div>
    <section class="collection" aria-labelledby="collection-title">
      <h2 class="collection__title" id="collection-title">{t['collection_title']}</h2>
      <p class="collection__frame">{t['collection_frame']}</p>
      <ul class="work-list">
{chr(10).join(rows)}
      </ul>
    </section>
  </div>"""
    emit(pre + "works/index.html",
         shell(lang, d + 1, f"{t['works']} — Paolo Ricaldone", t["collection_frame"],
               body, alt_of("works/index.html"), current="works/"))

    # ---- pagina opera
    for x in WORKS:
        spec = list(zip(t["spec"], [t["medium"], x["duration"], f"{x['res']}, {x['fps']}",
                                    t["edition"], x["year"]]))
        rowsx = "\n".join(f'      <div class="spec__row"><dt>{k}</dt><dd>{v}</dd></div>' for k, v in spec)
        body = f"""  <div class="page page--work">
    <nav class="crumb"><a href="{up(d + 2)}{'it/' if lang == 'it' else ''}works/index.html">{t['works']}</a></nav>
    <div class="work-detail__heading">
      <p class="eyebrow">{t['collection_title']} · {x['act']}</p>
      <h1><cite>{x['title']}</cite></h1>
    </div>
    <div class="work-detail__video">
      <video class="work-detail__player" src="{up(d + 2)}assets/{x['video']}"
             poster="{up(d + 2)}assets/{x['poster']}" controls controlsList="nodownload"
             preload="metadata" playsinline
             aria-label="{x['act']} — {x['title']}, {t['medium']}, {x['duration']}"></video>
    </div>
    <dl class="spec">
{rowsx}
    </dl>
    <p class="behaviour">{t['behaviour']}</p>
    <p class="behaviour behaviour--shown">{t['shown']}</p>
    <p class="viewing">{t['viewing']}</p>
  </div>"""
        emit(pre + f"works/{x['slug']}/index.html",
             shell(lang, d + 2, f"{x['title']} — Paolo Ricaldone",
                   f"{x['act']} — {x['title']}. {t['medium']}, {x['duration']}.",
                   body, alt_of(f"works/{x['slug']}/index.html"), current="works/"))

    # ---- Writing: il saggio, una pagina sola, sezioni citabili per ancora.
    # Dal 12 set 2026 la scrittura pubblica è il solo Pensiero: gli Appunti sono
    # chiusi (vault, architettura-social § Chiusura degli Appunti). Senza la
    # seconda colonna un indice che rimanda a una pagina sola era uno strato in
    # più, quindi /writing/ è il saggio; /writing/thought/ resta come 301.
    _, titles, panels = TX[lang]
    toc = "\n".join(f'        <li><a href="#{tid}">{titles[tid][1]}</a></li>'
                    for tid in TX_ORDER if tid in panels)
    secs = "\n".join(f"""    <section class="entry" id="{tid}">
      <h2>{titles[tid][1]}</h2>
{par(panels[tid], "      ")}
    </section>""" for tid in TX_ORDER if tid in panels)
    body = f"""  <article class="page page--reading">
    <p class="type-label">{t['essay']}</p>
    <h1>{t['thought']}</h1>
    <div class="lede">
{par(TX_INTRO[lang], "      ")}
    </div>
    <nav class="toc" aria-label="{t['sections']}">
      <ol>
{toc}
      </ol>
    </nav>
{secs}
  </article>"""
    emit(pre + "writing/index.html",
         shell(lang, d + 1, f"{t['thought']} — Paolo Ricaldone", t["thought"],
               body, alt_of("writing/index.html"), current="writing/"))

    # ---- About
    body = f"""  <div class="page page--about">
    <figure class="portrait">
      <img src="{up(d + 1)}assets/paolo-ricaldone.jpg" alt="Paolo Ricaldone" width="400" height="300" decoding="async">
    </figure>
    <article class="about">
      <h1 class="page-title">Paolo Ricaldone</h1>
{par(ABOUT[lang], "      ")}
      <div class="facts">
{par(FACTS[lang], "        ")}
      </div>
    </article>
  </div>"""
    emit(pre + "about/index.html",
         shell(lang, d + 1, f"{t['about']} — Paolo Ricaldone",
               "Paolo Ricaldone — Turin, 1968. Silent single-channel video, made entirely in CGI.",
               body, alt_of("about/index.html"), current="about/"))

    # ---- Contact: elenco con etichette, forma presa dalla versione di Kimi
    rows = [(t['l_email'], f'<a href="mailto:{EMAIL}">{EMAIL}</a>'),
            (t['l_studio'], t['city'])]
    rows += [(n, f'<a href="{u}" rel="me noopener">{h}</a>') for n, u, h in SOCIAL]
    listed = "\n".join(
        f'      <p><span class="c-label">{k}</span> {v}</p>' for k, v in rows)
    body = f"""  <div class="page page--contact">
    <div class="page-heading"><h1>{t['contact']}</h1></div>
    <div class="contact-list">
{listed}
    </div>
    <p class="contact-sale">{t['sale']}</p>
  </div>"""
    emit(pre + "contact/index.html",
         shell(lang, d + 1, f"{t['contact']} — Paolo Ricaldone", EMAIL,
               body, alt_of("contact/index.html"), current="contact/"))

for _lang in ("en", "it"):
    build(_lang)

for _path, _html in PAGES:
    _p = os.path.join(ROOT, _path)
    os.makedirs(os.path.dirname(_p), exist_ok=True)
    with open(_p, "w", encoding="utf-8") as f:
        f.write(_html)

print(f"{len(PAGES)} pagine generate")
