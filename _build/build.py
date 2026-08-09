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

def notes_content(fn):
    t = load(fn)
    sidebar = re.search(r'<nav class="texts-sidebar">(.*?)</nav>', t, flags=re.S).group(1)
    entries = []
    for tid, body in re.findall(r'<a class="sidebar-item[^"]*"\s+data-target="([^"]+)">(.*?)</a>', sidebar, flags=re.S):
        lab = re.search(r'<div class="sidebar-label">(.*?)</div>', body, flags=re.S)
        tit = re.search(r'<div class="sidebar-title">(.*?)</div>', body, flags=re.S)
        entries.append((tid, lab.group(1).strip() if lab else "", tit.group(1).strip() if tit else ""))
    panels = {}
    for pid, body in re.findall(r'<div class="text-panel[^"]*" id="([^"]+)">(.*?)(?=<div class="text-panel|\Z)', t, flags=re.S):
        panels[pid] = paragraphs(body)
    return entries, panels

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
NT = {"en": notes_content("live_notes.html"), "it": notes_content("live_it_notes.html")}
AB = {"en": about_paragraphs("live_about.html"), "it": about_paragraphs("live_it_about.html")}

S005 = {
    "label": {"en": "Silence #005", "it": "Silenzio #005"},
    "title": {"en": "The Silence I Build", "it": "Il silenzio che erigo"},
    "en": [
        "I've stopped speaking to you, and I did it on purpose. It isn't that I can't find the words: I find them perfectly well, I chose them one by one and decided to give you none of them. I wanted you to feel the absence, to have the emptiness where my voice used to be pressing on you all day long.",
        "For a while it worked the way I wanted. I'd watch you look for me, try a sentence, let it drop. I kept the wall straight and told myself you had it coming.",
        "But behind the wall, now, I sit comfortably. As long as I don't speak I don't have to hear what you'd answer, I don't have to risk that you might be even a little right. What I put up to keep you out now keeps out your side of the story too: and I'm more sheltered in here than you are out there.",
        "I keep calling it punishment. But punishment, sooner or later, ends. And I don't touch the wall.",
    ],
    "it": [
        "Ho smesso di parlarti e l'ho fatto apposta. Non è che non trovo le parole: le trovo benissimo, le ho scelte una per una e ho deciso di non dartene nessuna. Volevo che sentissi l'assenza, che il vuoto dove prima c'era la mia voce ti stesse addosso tutto il giorno.",
        "Per un po' ha funzionato come volevo. Ti vedevo cercarmi, provare una frase, lasciarla cadere. Tenevo il muro dritto e mi dicevo che te lo eri meritato.",
        "Ma dietro il muro, adesso, ci sto comodamente. Finché non parlo non devo sentire cosa risponderesti, non devo rischiare che tu abbia anche solo un po' ragione. Quello che ho tirato su per lasciarti fuori adesso tiene fuori pure la tua versione dei fatti: e sto più al riparo io qui dentro di quanto tu lo sia là fuori.",
        "Continuo a chiamarla punizione. Ma la punizione, prima o poi, finisce. E io il muro non lo tocco.",
    ],
}

S006 = {
    "label": {"en": "Silence #006", "it": "Silenzio #006"},
    "title": {"en": "The Silence That Defends You", "it": "Il silenzio che ti difende"},
    "en": [
        "They're talking about you and I'm right here. It isn't an accusation: it's the light tone of someone who looked at you from a distance and has already closed the file, a sentence said with half a smile, and the others laughing just enough not to take sides. I don't say anything.",
        "I could explain where the thing they take for a simple flaw comes from, or I could lay out the facts they don't have. But to do that I'd have to open you up in front of people who never asked you anything, and let them be the ones to decide whether my version holds. Everything I said would become theirs too. My silence is the only part of you that tonight doesn't belong to them.",
        "That evening I see you and I don't tell you. There's no way to tell it without carrying the rest in with it, the whole sentence, the face of the one who said it. So that defense stays where it happened.",
        "I defended you in the only way that leaves no trace. You'll never know, and to them I'm still on their side.",
    ],
    "it": [
        "Stanno parlando di te e io sono qui. Non è un'accusa: è il tono leggero di chi ti ha guardato da lontano e ha già chiuso la pratica, una frase detta con mezzo sorriso, e gli altri che ridono quel tanto che basta per non prendere posizione. Io non dico niente.",
        "Potrei spiegare da dove viene la cosa che a loro sembra soltanto un difetto oppure potrei mettere in fila i fatti che non conoscono. Ma per farlo dovrei aprirti davanti a gente che non ti ha mai chiesto niente, e lasciare che siano loro a decidere se la mia versione regge o meno. Tutto quello che dicessi diventerebbe anche loro. Il mio silenzio è l'unica parte di te che stasera non gli appartiene.",
        "La sera ti vedo e non te lo dico. Non c'è modo di raccontarlo senza portarti dentro anche il resto, la frase intera, la faccia di chi l'ha detta. Così quella difesa resta dove è successa.",
        "Ti ho difeso nell'unico modo che non lascia traccia. Tu non lo saprai mai, e per loro resto dalla loro parte.",
    ],
}

S007 = {
    "label": {"en": "Silence #007", "it": "Silenzio #007"},
    "title": {"en": "The Silence That Never Gets It Wrong", "it": "Il silenzio che non sbaglia"},
    "en": [
        "I've had the answer ready for three seconds and I don't give it. I turn it over, I shorten it, I take out the part that might not hold, and what comes out is something anyone could have said.",
        "With you I measure. It isn't that I have nothing to say: it's that you hear a wrong sentence right away, and what I had to say, said badly, is worth less than silence. Better too few words than one too many.",
        "So for months I've given you the short version, and you've learned to call it the way I am. Once you even paid me a compliment for it: that I never talk just to talk.",
        "I never talk just to talk, it's true. I've never yet told you anything that cost me.",
    ],
    "it": [
        "Ho la risposta pronta da tre secondi e non la do. La giro, la accorcio, le tolgo la parte che potrebbe non stare in piedi, e quando esce è una cosa che poteva dire chiunque.",
        "Con te misuro. Non è che non abbia niente da dire: è che una frase storta tu la senti subito, e quello che avevo da dire, detto male, vale meno del silenzio. Meglio poche parole che una di troppo.",
        "Così da mesi ti do la versione corta, e tu hai imparato a chiamarla il mio modo di essere. Una volta me ne hai anche fatto un complimento: che non parlo mai a vuoto.",
        "Non parlo mai a vuoto, è vero. Non ti ho ancora detto niente che mi costasse.",
    ],
}

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
]
ANNOUNCED = {"act": "Act III", "title": "I Don't", "anchor": "act-iii"}
HOME_WORK = WORKS[0]        # slot d'autore: si cambia qui, e in nessun altro punto

EMAIL = "studio@pricaldone.art"
# Indirizzi presi dai record in Studio/account-profili/ (instagram.md, x.md)
SOCIAL = [("Instagram", "https://www.instagram.com/pricaldone.art/", "@pricaldone.art"),
          ("X", "https://x.com/pricaldone_art", "@pricaldone_art")]

T = {
 "en": {"other": "IT",
   "nav": [("works/", "Works"), ("writing/", "Writing"), ("about/", "About"), ("contact/", "Contact")],
   "skip": "Skip to content", "play": "Play", "pause": "Pause", "replay": "Play again",
   "collection_title": "The Stage — Acts of a Lucid Silence",
   "collection_frame": "A trilogy of 1/1 video works on a bare stage. Each act stages a single emotional state, present from the first frame, isolated from its cause.",
   "medium": "Silent video, single-channel, CGI",
   # Lo stato dell'atto non ancora uscito: senza questa riga il posto dello still resta
   # vuoto e si legge come un'immagine che non carica, non come un'assenza voluta.
   # Una parola sola, nessuna data e nessuna cadenza: quelle sono promesse.
   "announced": "In production",
   "edition": "Single original, certified by the artist",
   "behaviour": "silent · single-channel · 4:3 · plays once, holding on the final frame",
   # Dichiarare cosa si sta guardando: senza questa riga il visitatore crede che
   # la versione pubblicata sia l'opera. Dato, non argomento di vendita.
   "shown": "shown here at 2560 × 1920 · the single certified original is 3840 × 2880, ProRes 422 HQ",
   "viewing": "Best experienced on a large screen in a quiet space",
   "spec": ["Medium", "Duration", "Resolution", "Edition", "Year"],
   "works": "Works", "writing": "Writing", "about": "About", "contact": "Contact",
   "thought": "Thought", "essay": "Essay", "notes": "Notes", "series": "Series",
   "silences": "Silences", "umbrella": "Series of reflections on the themes of the works",
   "sections": "Sections", "sale": "Works are sold privately, directly by the artist.",
   "city": "Turin, Italy", "l_email": "Email", "l_studio": "Studio",
   "copyright": "© Paolo Ricaldone. All rights reserved."},
 "it": {"other": "EN",
   "nav": [("works/", "Opere"), ("writing/", "Scritti"), ("about/", "Chi sono"), ("contact/", "Contatti")],
   "skip": "Vai al contenuto", "play": "Riproduci", "pause": "Metti in pausa", "replay": "Rivedi",
   "collection_title": "The Stage — Acts of a Lucid Silence",
   "collection_frame": "Una trilogia di opere video 1/1 su un palco spoglio. Ogni atto mette in scena un singolo stato emotivo, presente dal primo istante, isolato dalla sua causa.",
   "medium": "Video muto, single-channel, CGI",
   "announced": "In produzione",
   "edition": "Originale unico, certificato dall'artista",
   "behaviour": "muto · single-channel · 4:3 · si riproduce una volta, con tenuta sull'ultimo fotogramma",
   "shown": "presentato qui a 2560 × 1920 · l'originale unico certificato è 3840 × 2880, ProRes 422 HQ",
   "viewing": "Da vivere su uno schermo grande, in uno spazio silenzioso",
   "spec": ["Medium", "Durata", "Risoluzione", "Edizione", "Anno"],
   "works": "Opere", "writing": "Scritti", "about": "Chi sono", "contact": "Contatti",
   "thought": "Pensiero", "essay": "Saggio", "notes": "Appunti", "series": "Serie",
   "silences": "Silenzi", "umbrella": "Serie di riflessioni sui temi delle opere",
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
            <!-- Niente loading="lazy" sui fermi immagine dell'indice: sono due file da una
                 decina di kilobyte, e il rinvio non risparmiava banda ma faceva comparire il
                 secondo still un istante dopo il primo. Il posto è già riservato dal CSS
                 (aspect-ratio 4/3), quindi non c'è salto di impaginazione. -->
            <span class="work-row__still"><img src="{up(d + 1)}assets/{x['poster']}" alt=""></span>
            <span class="work-row__text">
              <span class="eyebrow">{x['act']}</span>
              <cite class="work-row__title">{x['title']}</cite>
              <span class="work-row__meta">{t['medium']} · {x['duration']} · {x['year']}</span>
            </span>
          </a>
        </li>""")
    rows.append(f"""        <li class="work-row work-row--announced" id="{ANNOUNCED['anchor']}">
          <span class="work-row__text">
            <span class="eyebrow">{ANNOUNCED['act']}</span>
            <cite class="work-row__title">{ANNOUNCED['title']}</cite>
            <span class="work-row__meta">{t['announced']}</span>
          </span>
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

    # ---- Writing: indice
    ent, pan = NT[lang]
    notes = []
    for i, (tid, lab, tit) in enumerate([e for e in ent if e[0] != "cornice"], start=1):
        notes.append({"slug": f"{i:03d}", "label": lab, "title": tit, "body": pan[tid]})
    notes.append({"slug": "005", "label": S005["label"][lang], "title": S005["title"][lang],
                  "body": S005[lang]})
    notes.append({"slug": "006", "label": S006["label"][lang], "title": S006["title"][lang],
                  "body": S006[lang]})
    notes.append({"slug": "007", "label": S007["label"][lang], "title": S007["title"][lang],
                  "body": S007[lang]})
    frame = pan.get("cornice", [])
    items = "\n".join(f"""          <li>
            <a href="{up(d + 1)}{pre}writing/silences/{n['slug']}/index.html">
              <span class="idx">{n['label']}</span><span class="ttl">{n['title']}</span>
            </a>
          </li>""" for n in notes)
    tx_titles = TX[lang][1]
    sections = "\n".join(
        f"""          <li><a href="{up(d + 1)}{pre}writing/thought/index.html#{tid}">
            <span class="sec-n">{i:02d}</span><span class="sec-t">{tx_titles[tid][1]}</span></a></li>"""
        for i, tid in enumerate([x for x in TX_ORDER if x in TX[lang][2]], start=1))
    body = f"""  <div class="page page--writing">
    <div class="page-heading"><h1>{t['writing']}</h1></div>
    <div class="wsplit">

      <section class="wcol wcol--essay">
        <p class="wkind">{t['essay']}</p>
        <h2 class="wcol-title"><a href="{up(d + 1)}{pre}writing/thought/index.html">{t['thought']}</a></h2>
        <ul class="wsections">
{sections}
        </ul>
      </section>

      <section class="wcol wcol--notes">
        <p class="wkind">{t['umbrella']}</p>
        <h2 class="wcol-title">{t['notes']}</h2>

        <section class="wseries">
          <h3 class="wseries-title">{t['silences']} <span class="wkind">{t['series']}</span></h3>
          <div class="wframe">
{par(frame, "            ")}
          </div>
          <ul class="wlist">
{items}
          </ul>
        </section>
      </section>

    </div>
  </div>"""
    emit(pre + "writing/index.html",
         shell(lang, d + 1, f"{t['writing']} — Paolo Ricaldone", t["umbrella"],
               body, alt_of("writing/index.html"), current="writing/"))

    # ---- il saggio: una pagina, sezioni citabili per ancora
    _, titles, panels = TX[lang]
    toc = "\n".join(f'        <li><a href="#{tid}">{titles[tid][1]}</a></li>'
                    for tid in TX_ORDER if tid in panels)
    secs = "\n".join(f"""    <section class="entry" id="{tid}">
      <h2>{titles[tid][1]}</h2>
{par(panels[tid], "      ")}
    </section>""" for tid in TX_ORDER if tid in panels)
    body = f"""  <article class="page page--reading">
    <nav class="crumb"><a href="{up(d + 2)}{'it/' if lang == 'it' else ''}writing/index.html">{t['writing']}</a></nav>
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
    emit(pre + "writing/thought/index.html",
         shell(lang, d + 2, f"{t['thought']} — Paolo Ricaldone", t["thought"],
               body, alt_of("writing/thought/index.html"), current="writing/"))

    # ---- un appunto, una pagina
    for n in notes:
        body = f"""  <article class="page page--reading">
    <nav class="crumb"><a href="{up(d + 3)}{'it/' if lang == 'it' else ''}writing/index.html">{t['notes']}</a> · {t['silences']}</nav>
    <p class="type-label">{n['label']}</p>
    <h1>{n['title']}</h1>
{par(n['body'], "    ")}
  </article>"""
        emit(pre + f"writing/silences/{n['slug']}/index.html",
             shell(lang, d + 3, f"{n['title']} — Paolo Ricaldone",
                   f"{n['label']} — {n['title']}", body,
                   alt_of(f"writing/silences/{n['slug']}/index.html"), current="writing/"))

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
