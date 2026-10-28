#!/usr/bin/env python3
"""Bouwt de HTML-pagina's van de GTF Franzen site uit gedeelde onderdelen. Draai: python3 build.py"""
import hashlib
import json
from pathlib import Path

ROOT = Path(__file__).parent

# ---------------------------------------------------------------- Gegevens
# Nog aan te vullen door de familie. Lege waarden worden niet getoond op de site.
MAIL = 'info@matrixeventsupport.nl'
TEL = ''           # bijv. '+31612345678'
TEL_TXT = ''       # bijv. '+31 6 12 34 56 78'
ADRES = ''         # bijv. 'Straat 1, 6351 AA Bocholtz'
KVK = ''
INSTA = ''
FACEBOOK = ''
WHATSAPP = f'https://wa.me/{TEL.lstrip("+")}' if TEL else ''
# Zet op het eigen domein zodra het aan GitHub Pages hangt
BASE = 'https://fenno03-web.github.io/gtf-franzen-site/'
MATRIX = 'https://fenno03-web.github.io/matrix-eil-site/'

FONTS = ('https://fonts.googleapis.com/css2?family=Archivo:wdth,wght@100..125,400..900'
         '&family=Inter:wght@400;500;600&display=swap')

NAV = [('diensten.html', 'Diensten'), ('projecten.html', 'Projecten'), ('over.html', 'Ons verhaal'), ('werkwijze.html', 'Werkwijze')]
CURRENT = 'index.html'


def ver(path):
    return hashlib.md5((ROOT / path).read_bytes()).hexdigest()[:8]


ORG = {
    '@context': 'https://schema.org', '@type': 'LocalBusiness', '@id': BASE + '#gtf',
    'name': 'GTF Franzen', 'alternateName': 'GTF Franzen Sound Light Vision', 'url': BASE,
    'image': BASE + 'assets/img/og.jpg', 'slogan': 'Sound | Light | Vision',
    'description': 'Familiebedrijf uit Bocholtz voor geluid, licht, omroepinstallaties, stroom en complete producties voor events in Nederland, België en Duitsland.',
    'areaServed': [{'@type': 'Country', 'name': n} for n in ('Nederland', 'België', 'Duitsland')],
    'address': {'@type': 'PostalAddress', 'addressLocality': 'Bocholtz', 'addressCountry': 'NL'},
    'knowsAbout': ['Geluidstechniek', 'Lichttechniek', 'Omroepinstallaties', '100V-systemen', 'Aggregaten', 'Eventproductie'],
}
if MAIL:
    ORG['email'] = MAIL
if TEL:
    ORG['telephone'] = TEL

# ---------------------------------------------------------------- Inhoud
DIENSTEN = [
    {'slug': 'geluid', 'nr': '01', 'titel': 'Geluid', 'img': 'geluid.jpg',
     'kort': 'Van heldere speech tot een volle festivalwei.',
     'tekst': 'Hier is het ooit begonnen: met verhuur en zelfgebouwde speakers. Goed geluid draait om verstaanbaarheid, balans en beleving. We stemmen het systeem af op de ruimte, het publiek en wat er op het podium gebeurt, zodat elk woord aankomt en elke beat raakt.',
     'punten': ['Systemen voor zaal, tent en open lucht', 'Podium- en monitorgeluid voor bands en artiesten', 'Speech, ceremonies en presentaties', 'Bediening door eigen technici']},
    {'slug': 'licht', 'nr': '02', 'titel': 'Licht', 'img': 'licht.jpg',
     'kort': 'Sfeer waar het moet, spektakel waar het kan.',
     'tekst': 'Licht bepaalt hoe je event voelt, en hoe het eruitziet op elke foto en video. Samen met MATRIX E.I.L. verzorgen we lichtontwerp, voorprogrammering en live bediening, van subtiel en stijlvol tot een volledig geprogrammeerde show.',
     'punten': ['Lichtontwerp en previsualisatie', 'Programmering en live operation', 'LED, effecten, CO2 en confetti', 'Sfeerverlichting voor zalen en tenten']},
    {'slug': 'omroep', 'nr': '03', 'titel': 'Omroep & 100V', 'img': 'omroep.jpg',
     'kort': 'Waar we al generaties bekend om staan.',
     'tekst': 'Omroepinstallaties en 100V-systemen zitten in ons DNA. Voor optochten, sportterreinen, markten en evenementen over een groot gebied zorgen we dat iedereen hoort wat er gezegd wordt, betrouwbaar en goed verstaanbaar.',
     'punten': ['Tijdelijke en vaste omroepinstallaties', '100V-systemen over grote afstanden', 'Optochten, sportvelden en evenemententerreinen', 'Advies, aanleg en onderhoud']},
    {'slug': 'stroom', 'nr': '04', 'titel': 'Stroom & infra', 'img': 'stroom.jpg',
     'kort': 'Geen stroom, geen show. Wij regelen het.',
     'tekst': 'Op locatie begint alles bij stroom. We leveren aggregaten en zorgen voor een praktische, veilige stroomverdeling, zodat geluid, licht, bars en foodtrucks gewoon blijven draaien.',
     'punten': ['Aggregaten', 'Stroomverdeling en bekabeling', 'Planning van de stroombehoefte vooraf', 'Op afgelegen locaties en in tenten']},
    {'slug': 'productie', 'nr': '05', 'titel': 'Complete productie', 'img': 'proj/sportclub-jubileum/01.jpg',
     'kort': 'Eén partner, van eerste idee tot laatste kabel.',
     'tekst': 'De kracht van GTF Franzen zit in het geheel. Geluid, licht, stroom en podiumtechniek komen bij ons uit één hand, met één aanspreekpunt. Je hoeft niet te schakelen tussen vijf leveranciers. Wij denken mee, plannen alles op elkaar af en staan er op de dag zelf.',
     'punten': ['Eén aanspreekpunt voor alle techniek', 'Technische planning en draaiboek', 'Opbouw, show en afbouw', 'Voor festivals, jubilea, bedrijfsevents en meer']},
]

EVENTS = [
    {'id': 'festival', 'label': 'Festival', 'img': 'proj/sportclub-jubileum/28.jpg',
     'kop': 'Een festival dat staat als een huis.',
     'tekst': 'Meerdere podia, wisselende artiesten en duizenden bezoekers. We plannen de techniek van alle stages op elkaar af en houden het overzicht, van het eerste overleg tot de laatste act.',
     'regelen': ['Geluid en monitoring per podium', 'Lichtshow en effecten met MATRIX E.I.L.', 'Aggregaten en stroomverdeling', 'Omroep over het hele terrein', 'Technische crew op locatie']},
    {'id': 'dorpsfeest', 'label': 'Dorpsfeest & carnaval', 'img': 'ols.jpg',
     'kop': 'Het hele dorp op de been.',
     'tekst': 'Kermis, carnaval, schuttersfeest of een avond in de feesttent. We kennen de regio, de verenigingen en de locaties, en weten wat er nodig is om er een avond van te maken waar nog lang over gepraat wordt.',
     'regelen': ['Tentgeluid en sfeerlicht', 'Omroep voor optochten', 'Stroom voor tent, bar en kraampjes', 'Podium voor bands en zaalartiesten', 'Snel schakelen als het programma verandert']},
    {'id': 'feest', 'label': 'Bruiloft & feest', 'img': 'zaal.jpg',
     'kop': 'Jullie dag, zonder zorgen over techniek.',
     'tekst': 'Van de ceremonie en speeches tot de band en de dansvloer. Wij zorgen dat alles klinkt en er mooi uitziet, zodat jullie alleen maar hoeven te genieten.',
     'regelen': ['Microfoons voor ceremonie en speeches', 'Geluid voor band of dj', 'Sfeerverlichting en dansvloer', 'Opbouw voordat de gasten komen', 'Eén vast aanspreekpunt']},
    {'id': 'bedrijf', 'label': 'Bedrijfsevent & congres', 'img': 'gala.jpg',
     'kop': 'Professioneel, strak en op tijd.',
     'tekst': 'Een presentatie, congres, personeelsfeest of productlancering. De techniek moet gewoon werken en de boodschap moet aankomen. Wij zorgen voor heldere spraak, passend licht en een soepel verloop.',
     'regelen': ['Spraak en presentatiegeluid', 'Podium- en sfeerverlichting', 'Draadloze microfoons', 'Technische regie tijdens het programma', 'Discreet opbouwen en afbouwen']},
    {'id': 'vereniging', 'label': 'Vereniging & jubileum', 'img': 'proj/sportclub-jubileum/14.jpg',
     'kop': 'Een jubileum om nooit te vergeten.',
     'tekst': 'Honderd jaar sportclub, een lustrum of een bijzonder concert. Voor zo’n moment wil je techniek die het verhaal van je vereniging groot maakt. Daar denken we graag in mee, ook met een beperkt budget.',
     'regelen': ['Volledige productie van tent of zaal', 'Show met licht, effecten en visuals', 'Geluid voor live acts', 'Stroom en infrastructuur', 'Meedenken over planning en budget']},
    {'id': 'gemeente', 'label': 'Gemeente & omroep', 'img': 'amstel-2.jpg',
     'kop': 'Betrouwbaar, voor publieke momenten.',
     'tekst': 'Herdenkingen, intochten, markten en evenementen in de openbare ruimte. Met onze ervaring in omroep- en 100V-systemen zorgen we dat iedereen op het terrein het goed hoort.',
     'regelen': ['Omroepinstallaties en 100V', 'Spraak bij ceremonies en herdenkingen', 'Stroom op locatie', 'Advies over de opzet vooraf', 'Ervaring in NL, BE en DE']},
]

PROJECTEN = [
    {'slug': 'amstel-gold-race', 'titel': 'Amstel Gold Race', 'sub': 'Omroep langs het parcours', 'plek': 'Zuid-Limburg', 'jaar': '2025 & 2026',
     'fotos': ['amstel-1.jpg', 'amstel-2.jpg', 'amstel-3.jpg', 'amstel-6.jpg', 'amstel-4.jpg', 'amstel-5.jpg'], 'cover': 'amstel-3.jpg',
     'tekst': 'Bij een van de grootste wielerklassiekers van Nederland hangen onze hoorns langs het parcours. Het publiek op de route hoort precies wat er gebeurt in de koers, en dat elk jaar weer. Hier zie je waar we groot mee zijn geworden: omroep die het gewoon doet.',
     'rol': 'Omroepinstallatie langs het parcours door GTF Franzen',
     'pers': None},
    {'slug': 'sportclub-jubileum', 'titel': 'Sportclub’25', 'sub': '100 jaar jubileum', 'plek': 'Bocholtz', 'jaar': '2025',
     'map': 'sportclub-jubileum', 'n': 30,
     'tekst': 'Voor het honderdjarig bestaan van Sportclub’25 in Bocholtz stond er een productie die het dorp niet snel vergeet. Een groot podium, een volle tent en een avond lang artiesten, met een show die van begin tot eind op elkaar was afgestemd.',
     'rol': 'Productie en techniek door GTF Franzen · Lichtontwerp, visuals en show door MATRIX E.I.L.',
     'pers': ('Artikel op Highlite', 'https://www.highlite.com/nl/news/base/sportsclub-bocholtz.html')},
    {'slug': 'woeesj-stock', 'titel': 'Woeësj-Stock', 'sub': 'Festival in de feesttent', 'plek': 'Simpelveld', 'jaar': '2026',
     'map': 'woeesj-stock', 'n': 11,
     'tekst': 'Woeësj-Stock bracht hiphop, blaasmuziek en het hele dorp samen in één tent. Wij zorgden voor de techniek, zodat elke act klonk en eruitzag zoals hij verdiende.',
     'rol': 'Productie en techniek door GTF Franzen · Stage- en lichtontwerp door MATRIX E.I.L.',
     'pers': None},
]

TIJDLIJN = [
    ('Het begin', 'Een winkel en een passie voor techniek',
     'GTF Franzen begon als witgoedzaak in Bocholtz. Daarnaast werd er volop geknutseld aan geluid, met speakers die we zelf bouwden.'),
    ('Rond 1960', 'De verhuur gaat van start',
     'Rond 1960 kreeg de verhuur van geluid vorm. Dat werd de basis van het bedrijf zoals je het nu kent.'),
    ('Decennia lang', 'Bekend om omroep en 100V',
     'Optochten, sportvelden en evenementen in de hele regio. Met onze omroepinstallaties en 100V-systemen bouwden we een naam op voor betrouwbaarheid.'),
    ('Groeien', 'Licht, stroom en complete producties',
     'Het aanbod groeide mee met de events. Licht, aggregaten en complete producties kwamen erbij, voor festivals, bruiloften, verenigingen en bedrijven.'),
    ('Vandaag', 'Leon en de volgende generatie',
     'Leon Franzen staat aan het roer. Zoon Fenno groeide op tussen de kabels en brengt met zijn eigen bedrijven MATRIX E.I.L. en ARGUS Systems nieuwe energie mee. Dezelfde betrokkenheid, met de techniek van nu.'),
]

FAQ = [
    ('Kunnen jullie ook alleen geluid of alleen licht leveren?', 'Zeker. Je kunt ons inschakelen voor één onderdeel. Maar de meeste klanten merken dat het veel rust geeft als alle techniek uit één hand komt, met één aanspreekpunt.'),
    ('In welke regio werken jullie?', 'We komen uit Bocholtz in Zuid-Limburg en werken in heel Nederland, België en Duitsland.'),
    ('Hoe ver van tevoren moet ik boeken?', 'Hoe eerder, hoe beter, zeker voor de zomer en het carnavalsseizoen. Maar bel ook gerust als het kort dag is, dan kijken we wat er kan.'),
    ('Wat kost het?', 'Elk event is anders, dus we werken altijd met een offerte op maat. Die is vrijblijvend. Vertel ons wat je van plan bent, dan denken we mee over wat past bij je budget.'),
    ('Komen jullie eerst kijken op de locatie?', 'Bij grotere events komen we graag langs om de locatie te bekijken. Zo weten we precies waar stroom, podium en speakers moeten komen en voorkomen we verrassingen op de dag zelf.'),
    ('Zorgen jullie ook voor stroom?', 'Ja. We leveren aggregaten en verzorgen de stroomverdeling, ook voor bars, foodtrucks en andere partijen op je terrein.'),
]

STAPPEN = [
    ('Kennismaken', 'Je vertelt wat je van plan bent. We stellen de juiste vragen en kijken waar nodig samen op de locatie.'),
    ('Voorstel op maat', 'Je krijgt een helder voorstel met wat er nodig is en wat het kost. Geen standaardpakket, maar wat bij jouw event past.'),
    ('Voorbereiden', 'We plannen geluid, licht, stroom en crew op elkaar af en stemmen de tijden af met jou en andere partijen.'),
    ('De dag zelf', 'We bouwen op, testen alles en staan klaar tijdens het event. Je hebt één vast aanspreekpunt.'),
    ('Afbouw en evaluatie', 'Na afloop ruimen we alles netjes op. En we horen graag hoe het was, zodat de volgende editie nog beter wordt.'),
]


# ---------------------------------------------------------------- Onderdelen
RINGS = [(702, 12), (625, 21), (548, 30), (471, 38), (393, 50)]
GTF = ('<path d="M490 530h527v50H778v480h-56V580H490z"/>'
       '<path d="M488 628h188v97h-60v-39h-70v219h70V828h-38v-59h100v193H488z"/>'
       '<path d="M826 627h192v62H890v77h94v62h-94v134h-64z"/>')


def mark(cls='mark', small=False):
    rings = [(r, w * 1.7) for r, w in RINGS[1:]] if small else RINGS
    r = ''.join(f'<circle cx="750" cy="750" r="{rad}" stroke-width="{w:g}"/>' for rad, w in rings)
    return f'<svg class="{cls}" viewBox="0 0 1500 1500" aria-hidden="true"><g class="rings">{r}</g><g class="gtf">{GTF}</g></svg>'


def cover_of(p):
    return f'assets/img/{p["cover"]}' if 'cover' in p else f'assets/img/proj/{p["map"]}/cover.jpg'


LOGO = mark('logo-mark', small=True) + '<span class="logo-txt"><b>GTF Franzen</b><small>Sound · Light · Vision</small></span>'


def head(title, desc, image='assets/img/og.jpg', ld=None):
    url = BASE + ('' if CURRENT == 'index.html' else CURRENT)
    ld = ld if ld is not None else [ORG]
    ld_html = ''.join(f'\n<script type="application/ld+json">{json.dumps(x, ensure_ascii=False)}</script>' for x in ld)
    return f'''<!doctype html>
<html lang="nl">
<head>
<meta charset="utf-8">
<meta name="viewport" content="width=device-width, initial-scale=1, viewport-fit=cover">
<title>{title}</title>
<meta name="description" content="{desc}">
<link rel="canonical" href="{url}">
<meta name="robots" content="index, follow">
<meta property="og:type" content="website">
<meta property="og:locale" content="nl_NL">
<meta property="og:site_name" content="GTF Franzen">
<meta property="og:url" content="{url}">
<meta property="og:title" content="{title}">
<meta property="og:description" content="{desc}">
<meta property="og:image" content="{BASE}{image}">
<meta name="twitter:card" content="summary_large_image">
<meta name="theme-color" content="#0a0a0a">
<link rel="icon" href="assets/img/favicon.svg" type="image/svg+xml">
<link rel="preconnect" href="https://fonts.googleapis.com">
<link rel="preconnect" href="https://fonts.gstatic.com" crossorigin>
<link rel="stylesheet" href="{FONTS}">
<link rel="stylesheet" href="assets/css/style.css?v={ver('assets/css/style.css')}">{ld_html}
</head>'''


def header(current, dark=True):
    cur = ' aria-current="page"'
    links = ''.join(f'<a href="{href}"{cur if href == current else ""}>{label}</a>' for href, label in NAV)
    return f'''<a class="skip" href="#main">Naar de inhoud</a>
<header class="site-header{' on-dark' if dark else ''}">
  <div class="wrap">
    <a class="logo" href="index.html" aria-label="GTF Franzen home">{LOGO}</a>
    <button class="menu-btn" aria-label="Menu" aria-expanded="false" aria-controls="nav"><span></span><span></span></button>
    <nav class="nav" id="nav" aria-label="Hoofdmenu">{links}<a class="nav-cta" href="contact.html"{cur if current == 'contact.html' else ''}>Offerte aanvragen</a></nav>
  </div>
</header>'''


def contact_list(cls='contact-list'):
    items = []
    if TEL:
        items.append(f'<li><span>Bellen</span><a href="tel:{TEL}">{TEL_TXT or TEL}</a></li>')
    if WHATSAPP:
        items.append(f'<li><span>WhatsApp</span><a href="{WHATSAPP}" target="_blank" rel="noopener">Stuur een appje</a></li>')
    if MAIL:
        items.append(f'<li><span>Mail</span><a href="mailto:{MAIL}">{MAIL}</a></li>')
    items.append(f'<li><span>Waar</span><b>{ADRES or "Bocholtz, Zuid-Limburg"}</b></li>')
    items.append('<li><span>Werkgebied</span><b>Nederland · België · Duitsland</b></li>')
    return f'<ul class="{cls}">{"".join(items)}</ul>'


def footer(extra_js=''):
    socials = ''.join(f'<li><a href="{u}" target="_blank" rel="noopener">{n}</a></li>' for n, u in (('Instagram', INSTA), ('Facebook', FACEBOOK)) if u)
    return f'''<footer class="site-footer">
  <div class="wrap">
    <div class="foot-top">
      <p class="foot-claim">Van onze familie,<br><em>voor jouw event.</em></p>
      <a class="btn fill" href="contact.html">Vraag een offerte aan</a>
    </div>
    <div class="foot-grid">
      <div class="foot-brand">
        <a class="logo" href="index.html" aria-label="GTF Franzen home">{LOGO}</a>
        <p>Geluid, licht, omroep, stroom en complete producties. Al meer dan 50 jaar uit Bocholtz.</p>
      </div>
      <div>
        <h4>Diensten</h4>
        <ul>{''.join(f'<li><a href="diensten.html#{d["slug"]}">{d["titel"]}</a></li>' for d in DIENSTEN)}</ul>
      </div>
      <div>
        <h4>GTF Franzen</h4>
        <ul><li><a href="over.html">Ons verhaal</a></li><li><a href="projecten.html">Projecten</a></li><li><a href="werkwijze.html">Werkwijze</a></li><li><a href="contact.html">Contact</a></li><li><a href="{MATRIX}" target="_blank" rel="noopener">MATRIX E.I.L.</a></li>{socials}</ul>
      </div>
      <div>
        <h4>Contact</h4>
        {contact_list('foot-contact')}
      </div>
    </div>
    <div class="credits"><span>Foto’s onder andere door</span><img src="assets/img/partner-eleven-media.png" alt="Eleven Media" loading="lazy"><img src="assets/img/partner-highlite.png" alt="Highlite" loading="lazy"></div>
    <div class="foot-bottom">
      <span>&copy; <span data-year>2026</span> GTF Franzen · Sound | Light | Vision{f" · KvK {KVK}" if KVK else ""}</span>
      <a href="privacy.html">Privacy</a>
    </div>
  </div>
</footer>
<script src="assets/js/main.js?v={ver('assets/js/main.js')}"></script>{extra_js}
</body>
</html>
'''


def eyebrow(nr, txt):
    return f'<p class="eyebrow reveal"><span>{nr}</span>{txt}</p>'


def cta_band():
    return '''<section class="cta-band">
  <div class="wrap reveal">
    <h2 class="display">Vertel ons wat je<br><em>van plan bent.</em></h2>
    <p class="lead">Een kort berichtje is genoeg. We denken vrijblijvend mee en sturen je een voorstel op maat.</p>
    <div class="btns"><a class="btn fill" href="contact.html">Vraag een offerte aan</a><a class="btn ghost" href="projecten.html">Bekijk ons werk</a></div>
  </div>
</section>'''


def page(name, title, desc, body, dark_header=True, ld=None, body_cls='', image='assets/img/og.jpg', extra_js=''):
    global CURRENT
    CURRENT = name
    html = (head(title, desc, image=image, ld=ld) + f'\n<body class="{body_cls}">\n' + header(name, dark_header)
            + '\n<main id="main">\n' + body + '\n</main>\n' + footer(extra_js))
    (ROOT / name).write_text(html, encoding='utf-8')
    return name


# ---------------------------------------------------------------- Home
def home():
    diensten = ''.join(f'''
      <a class="svc reveal" href="diensten.html#{d["slug"]}">
        <span class="svc-nr">{d["nr"]}</span>
        <span class="svc-img"><img src="assets/img/{d["img"]}" alt="" loading="lazy"></span>
        <h3>{d["titel"]}</h3>
        <p>{d["kort"]}</p>
        <span class="arrow" aria-hidden="true">→</span>
      </a>''' for d in DIENSTEN)

    tabs = ''.join(f'<button role="tab" id="tab-{e["id"]}" aria-controls="pane-{e["id"]}" aria-selected="{"true" if i == 0 else "false"}" tabindex="{0 if i == 0 else -1}">{e["label"]}</button>' for i, e in enumerate(EVENTS))
    panes = ''.join(f'''
      <div class="pane" role="tabpanel" id="pane-{e["id"]}" aria-labelledby="tab-{e["id"]}"{"" if i == 0 else " hidden"}>
        <div class="pane-img"><img src="assets/img/{e["img"]}" alt="" loading="lazy"></div>
        <div class="pane-copy">
          <h3>{e["kop"]}</h3>
          <p>{e["tekst"]}</p>
          <p class="pane-label">Dit regelen wij voor je</p>
          <ul class="checks">{"".join(f"<li>{r}</li>" for r in e["regelen"])}</ul>
          <a class="btn fill" href="contact.html?type={e["id"]}">Plan je {e["label"].split(" ")[0].lower()}</a>
        </div>
      </div>''' for i, e in enumerate(EVENTS))

    tijd = ''.join(f'<li class="reveal"><span class="t-when">{w}</span><h3>{h}</h3><p>{p}</p></li>' for w, h, p in TIJDLIJN[:4]) \
        + f'<li class="reveal now"><span class="t-when">{TIJDLIJN[4][0]}</span><h3>{TIJDLIJN[4][1]}</h3><p>{TIJDLIJN[4][2]}</p></li>'

    proj = ''.join(f'''
      <a class="proj reveal" href="project-{p["slug"]}.html">
        <span class="proj-img"><img src="{cover_of(p)}" alt="{p["titel"]}" loading="lazy"></span>
        <span class="proj-meta">{p["plek"]} · {p["jaar"]}</span>
        <h3>{p["titel"]}</h3>
        <p>{p["sub"]}</p>
      </a>''' for p in PROJECTEN)

    faq = ''.join(f'<details class="reveal"><summary>{q}</summary><p>{a}</p></details>' for q, a in FAQ)
    ld = [ORG, {'@context': 'https://schema.org', '@type': 'FAQPage', 'mainEntity': [
        {'@type': 'Question', 'name': q, 'acceptedAnswer': {'@type': 'Answer', 'text': a}} for q, a in FAQ]}]

    body = f'''<section class="hero">
  <div class="hero-media"><img src="assets/img/hero.jpg" alt="Podium met CO2-jets en confetti boven een vol publiek" fetchpriority="high"></div>
  <div class="hero-waves" aria-hidden="true">{mark('wave-mark')}<i></i><i></i><i></i></div>
  <div class="wrap hero-inner">
    <p class="hero-kicker"><span class="dot"></span>Familiebedrijf uit Bocholtz · NL · BE · DE</p>
    <h1 class="hero-title">Jouw event.<br>Onze <em>familie</em><br>erachter.</h1>
    <p class="hero-lead">Geluid, licht, stroom en complete producties voor festivals, dorpsfeesten, bruiloften, verenigingen en bedrijven. Al meer dan 50 jaar, met één aanspreekpunt van begin tot eind.</p>
    <div class="btns"><a class="btn fill" href="contact.html">Vraag een offerte aan</a><a class="btn ghost" href="#evenement">Wat organiseer je?</a></div>
  </div>
</section>

<section class="facts" aria-label="GTF Franzen in cijfers">
  <div class="wrap">
    <div class="fact reveal"><b data-count="50">50</b><sup>+</sup><span>jaar ervaring in geluid en techniek</span></div>
    <div class="fact reveal"><b data-count="100">100</b><sup>+</sup><span>projecten per jaar</span></div>
    <div class="fact reveal"><b>1</b><span>aanspreekpunt voor alle techniek</span></div>
    <div class="fact reveal"><b>3</b><span>landen: NL, BE en DE</span></div>
  </div>
</section>

<section class="section intro">
  <div class="wrap two">
    <div>
      {eyebrow('01', 'Waarom één partner')}
      <h2 class="display reveal">Vijf leveranciers?<br><em>Of één familie</em><br>die alles regelt.</h2>
    </div>
    <div class="compare">
      <div class="cmp cmp-no reveal">
        <h3>Zo gaat het vaak</h3>
        <ul><li>Een partij voor geluid, een voor licht, een voor stroom</li><li>Iedereen een eigen planning en eigen wensen</li><li>Op de dag zelf weet niemand wie verantwoordelijk is</li><li>Valt er iets uit, dan begint het bellen</li></ul>
      </div>
      <div class="cmp cmp-yes reveal">
        <h3>Zo gaat het met Franzen</h3>
        <ul><li>Alle techniek uit één hand, bijna volledig eigen materiaal</li><li>Eén vast aanspreekpunt, van eerste gesprek tot afbouw</li><li>Korte lijnen, eerlijk advies en geen gedoe</li><li>Mensen die er staan als het telt, want het is ook onze naam</li></ul>
      </div>
    </div>
  </div>
</section>

<section class="section diensten-home">
  <div class="wrap">
    <div class="sec-head">
      {eyebrow('02', 'Wat we doen')}
      <h2 class="display reveal">Alles voor een event<br><em>dat klopt.</em></h2>
    </div>
    <div class="svc-grid">{diensten}
    </div>
  </div>
</section>

<section class="section picker" id="evenement">
  <div class="wrap">
    <div class="sec-head">
      {eyebrow('03', 'Voor elk event')}
      <h2 class="display reveal">Wat ga jij<br><em>organiseren?</em></h2>
    </div>
    <div class="tabs reveal" role="tablist" aria-label="Soort event">{tabs}</div>
    <div class="panes">{panes}
    </div>
  </div>
</section>

<section class="section story dark">
  <div class="wrap two">
    <div class="story-copy">
      {eyebrow('04', 'Ons verhaal')}
      <h2 class="display reveal">Een familie<br>met een <em>vak.</em></h2>
      <p class="lead reveal">Het begon met een winkel in Bocholtz en speakers die we zelf bouwden. Meer dan 50 jaar later staan we nog steeds met dezelfde mentaliteit op elk event: vakmanschap, betrokkenheid en aandacht voor elk detail.</p>
      <a class="btn ghost reveal" href="over.html">Lees ons verhaal</a>
      <div class="then-now reveal">
        <figure><img src="assets/img/bus-toen.jpg" alt="De oude GTF-bus met het logo en hoorns op het dak" loading="lazy"><figcaption>Toen</figcaption></figure>
        <figure><img src="assets/img/bussen-nu.jpg" alt="De bussen van Franzen Bocholtz voor een locatie" loading="lazy"><figcaption>Nu</figcaption></figure>
      </div>
    </div>
    <ol class="timeline">{tijd}</ol>
  </div>
</section>

<section class="proof">
  <img src="assets/img/amstel-2.jpg" alt="Hoorn met de naam Franzen Bocholtz naast een vlag van de Amstel Gold Race" loading="lazy">
  <div class="wrap">
    <p class="proof-q reveal">Onze naam hangt<br>langs het parcours van<br><em>de Amstel Gold Race.</em></p>
    <a class="link-arrow reveal" href="project-amstel-gold-race.html">Bekijk het project</a>
  </div>
</section>

<section class="section">
  <div class="wrap">
    <div class="sec-head row">
      <div>{eyebrow('05', 'Projecten')}
      <h2 class="display reveal">Waar we<br><em>trots op zijn.</em></h2></div>
      <a class="link-arrow reveal" href="projecten.html">Alle projecten</a>
    </div>
    <div class="proj-grid">{proj}
    </div>
  </div>
</section>

<section class="section values">
  <div class="wrap">
    <div class="sec-head">
      {eyebrow('06', 'Waar je op kunt rekenen')}
      <h2 class="display reveal">Wat een familiebedrijf<br><em>anders maakt.</em></h2>
    </div>
    <div class="val-grid">
      <div class="val reveal"><span class="val-ic" aria-hidden="true">01</span><h3>Je belt met de familie</h3><p>Geen callcenter of ticketnummer. Je spreekt de mensen die je event ook echt neerzetten.</p></div>
      <div class="val reveal"><span class="val-ic" aria-hidden="true">02</span><h3>Maatwerk, geen pakket</h3><p>We kijken naar wat jouw event in de praktijk nodig heeft, niet naar wat er op papier staat.</p></div>
      <div class="val reveal"><span class="val-ic" aria-hidden="true">03</span><h3>Onze naam staat erop</h3><p>Elk event draagt de naam Franzen. Daarom laten we pas los als alles goed staat.</p></div>
      <div class="val reveal"><span class="val-ic" aria-hidden="true">04</span><h3>Eigen materiaal</h3><p>We werken bijna volledig met eigen materiaal. Dat kennen we door en door, dus we weten precies wat we meenemen en hoe het erbij staat.</p></div>
    </div>
  </div>
</section>

<section class="section faq">
  <div class="wrap two">
    <div>
      {eyebrow('07', 'Veelgestelde vragen')}
      <h2 class="display reveal">Goed om<br><em>te weten.</em></h2>
    </div>
    <div class="faq-list">{faq}</div>
  </div>
</section>

{cta_band()}'''
    return page('index.html', 'GTF Franzen | Geluid, licht en complete eventproductie uit Bocholtz',
                'Familiebedrijf GTF Franzen uit Bocholtz: geluid, licht, omroep, stroom en complete producties voor festivals, dorpsfeesten, bruiloften, verenigingen en bedrijven. Al meer dan 50 jaar.',
                body, ld=ld, body_cls='home')


# ---------------------------------------------------------------- Diensten
def diensten():
    blokken = ''.join(f'''
<section class="section svc-detail{' alt' if i % 2 else ''}" id="{d["slug"]}">
  <div class="wrap two">
    <div class="svc-detail-img reveal"><img src="assets/img/{d["img"]}" alt="{d["titel"]} door GTF Franzen" loading="lazy"></div>
    <div>
      {eyebrow(d["nr"], d["titel"])}
      <h2 class="display reveal">{d["kort"]}</h2>
      <p class="lead reveal">{d["tekst"]}</p>
      <ul class="checks reveal">{"".join(f"<li>{p}</li>" for p in d["punten"])}</ul>
    </div>
  </div>
</section>''' for i, d in enumerate(DIENSTEN))
    body = f'''<section class="page-hero">
  <div class="wrap">
    {eyebrow('—', 'Diensten')}
    <h1 class="display xl reveal">Alle techniek,<br><em>uit één hand.</em></h1>
    <p class="lead reveal">Je kunt ons inschakelen voor één onderdeel of voor je complete productie. Hoe groter het geheel, hoe meer je merkt wat één partner scheelt.</p>
    <nav class="jump reveal" aria-label="Diensten">{"".join(f'<a href="#{d["slug"]}">{d["titel"]}</a>' for d in DIENSTEN)}</nav>
  </div>
</section>
{blokken}
{cta_band()}'''
    return page('diensten.html', 'Diensten | GTF Franzen', 'Geluid, licht, omroep en 100V, stroom en aggregaten en complete producties. GTF Franzen regelt alle techniek voor je event uit één hand.',
                body, dark_header=False)


# ---------------------------------------------------------------- Over
def over():
    tijd = ''.join(f'<li class="reveal{" now" if i == len(TIJDLIJN) - 1 else ""}"><span class="t-when">{w}</span><h3>{h}</h3><p>{p}</p></li>' for i, (w, h, p) in enumerate(TIJDLIJN))
    body = f'''<section class="page-hero">
  <div class="wrap">
    {eyebrow('—', 'Ons verhaal')}
    <h1 class="display xl reveal">Generaties lang<br><em>hetzelfde vak.</em></h1>
    <p class="lead reveal">GTF Franzen is een familiebedrijf met een passie voor techniek. Al meer dan 50 jaar staan vakmanschap, betrokkenheid en kwaliteit bij ons centraal. Niet omdat dat goed klinkt, maar omdat we het zo geleerd hebben.</p>
  </div>
</section>

<section class="section">
  <div class="wrap two">
    <div class="album reveal" aria-hidden="true">
      <figure class="polaroid p1"><img src="assets/img/bus-toen.jpg" alt="" loading="lazy"><figcaption>De eerste GTF-bus</figcaption></figure>
      <figure class="polaroid p2"><img src="assets/img/bus-t3.jpg" alt="" loading="lazy"><figcaption>Onze oude T3</figcaption></figure>
      <figure class="polaroid p3"><img src="assets/img/bussen-nu.jpg" alt="" loading="lazy"><figcaption>Vandaag</figcaption></figure>
    </div>
    <div>
      {eyebrow('01', 'Waar het begon')}
      <h2 class="display reveal">Van witgoedzaak<br><em>tot productiepartner.</em></h2>
      <p class="lead reveal">Onze wortels liggen in techniek en ondernemerschap. Wat begon als witgoedzaak groeide via geluidsverhuur en zelfgebouwde speakers uit tot een veelzijdig bedrijf. Rond 1960 kreeg de verhuurtak vorm, en daarmee de basis van GTF Franzen zoals je het nu kent.</p>
      <p class="reveal">We werden bekend met omroepinstallaties en 100V-systemen. Daarna kwamen licht, stroom, aggregaten en complete producties erbij. Vandaag werken we voor particulieren, bedrijven, verenigingen, gemeenten en organisatoren in Nederland, België en Duitsland.</p>
    </div>
  </div>
</section>

<section class="section dark">
  <div class="wrap">
    <div class="sec-head">{eyebrow('02', 'Door de jaren heen')}<h2 class="display reveal">Een tijdlijn<br><em>van de familie.</em></h2></div>
    <ol class="timeline wide">{tijd}</ol>
  </div>
</section>

<section class="section family">
  <div class="wrap">
    <div class="sec-head">{eyebrow('03', 'De mensen')}<h2 class="display reveal">Het gezicht<br><em>achter je event.</em></h2>
    <p class="lead reveal">Bij ons spreek je niet met een afdeling, maar met de familie. Dezelfde mensen die je voorstel maken, staan op de dag zelf naast het podium.</p></div>
    <div class="people">
      <figure class="person reveal"><div class="person-img mono" aria-hidden="true"><span>LF</span></div><figcaption><b>Leon Franzen</b><span>Eigenaar en eindverantwoordelijke</span><p>Leon kent het vak van binnen en buiten en houdt het overzicht over elke productie. Bij hem weet je waar je aan toe bent.</p></figcaption></figure>
      <figure class="person reveal"><div class="person-img mono" aria-hidden="true"><span>FF</span></div><figcaption><b>Fenno Franzen</b><span>Volgende generatie · MATRIX E.I.L. en ARGUS Systems</span><p>Fenno ging van jongs af aan mee naar events en bouwde zijn eigen bedrijven in licht, visuals en showtechniek. Hij zet het familiebedrijf voort.</p></figcaption></figure>
    </div>
    <div class="crew reveal">
      <div><b>8+</b><span>mensen bij de opbouw van een groot event, zoals het jubileum van Sportclub’25</span></div>
      <div><b>3</b><span>vaste krachten tijdens de show: FOH audio, FOH licht en backstage</span></div>
      <div><b>Eigen</b><span>materiaal: we draaien bijna alles met spullen die we door en door kennen</span></div>
    </div>
    </div>
  </div>
</section>

<section class="section values">
  <div class="wrap two">
    <div>{eyebrow('04', 'Hoe we werken')}<h2 class="display reveal">Persoonlijk,<br><em>no-nonsense.</em></h2></div>
    <div>
      <p class="lead reveal">Persoonlijk contact, open communicatie en eerlijke samenwerking. Korte lijnen en een nuchtere aanpak. Een project moet bij ons niet alleen goed klinken of werken, het moet ook goed voelen.</p>
      <p class="reveal">Daarom kiezen we nooit voor een standaardoplossing, maar voor wat bij jouw event past. En voor licht en visuals werken we samen met <a href="{MATRIX}" target="_blank" rel="noopener">MATRIX E.I.L.</a>, het bedrijf van Fenno Franzen. Zo blijft ook de nieuwste techniek in de familie.</p>
    </div>
  </div>
</section>

{cta_band()}'''
    return page('over.html', 'Ons verhaal | GTF Franzen', 'Al meer dan 50 jaar een familiebedrijf in geluid, licht en techniek. Lees hoe GTF Franzen uit Bocholtz uitgroeide van witgoedzaak tot productiepartner voor events.',
                body, dark_header=False)


# ---------------------------------------------------------------- Werkwijze
def werkwijze():
    stappen = ''.join(f'<li class="step reveal"><span class="step-nr">{i + 1:02d}</span><h3>{t}</h3><p>{p}</p></li>' for i, (t, p) in enumerate(STAPPEN))
    faq = ''.join(f'<details class="reveal"><summary>{q}</summary><p>{a}</p></details>' for q, a in FAQ)
    body = f'''<section class="page-hero">
  <div class="wrap">
    {eyebrow('—', 'Werkwijze')}
    <h1 class="display xl reveal">Zo pakken<br><em>we het aan.</em></h1>
    <p class="lead reveal">Duidelijk, persoonlijk en zonder verrassingen. Van het eerste telefoontje tot de laatste kabel die de bus in gaat.</p>
  </div>
</section>
<section class="section">
  <div class="wrap"><ol class="steps">{stappen}</ol></div>
</section>
<section class="section faq">
  <div class="wrap two">
    <div>{eyebrow('?', 'Veelgestelde vragen')}<h2 class="display reveal">Goed om<br><em>te weten.</em></h2></div>
    <div class="faq-list">{faq}</div>
  </div>
</section>
{cta_band()}'''
    return page('werkwijze.html', 'Werkwijze | GTF Franzen', 'Van kennismaking tot afbouw: zo werkt GTF Franzen aan jouw event. Eén aanspreekpunt, een voorstel op maat en techniek die gewoon klopt.',
                body, dark_header=False)


# ---------------------------------------------------------------- Projecten
def projecten():
    kaarten = ''.join(f'''
      <a class="proj big reveal" href="project-{p["slug"]}.html">
        <span class="proj-img"><img src="{cover_of(p)}" alt="{p["titel"]}" loading="lazy"></span>
        <span class="proj-meta">{p["plek"]} · {p["jaar"]}</span>
        <h3>{p["titel"]}</h3>
        <p>{p["tekst"]}</p>
      </a>''' for p in PROJECTEN)
    body = f'''<section class="page-hero">
  <div class="wrap">
    {eyebrow('—', 'Projecten')}
    <h1 class="display xl reveal">Events waar<br><em>we trots op zijn.</em></h1>
    <p class="lead reveal">Elk jaar meer dan honderd projecten: festivals, bruiloften, congressen, dorpsfeesten, bedrijfsproducties en omroepwerk. Een greep uit ons werk.</p>
  </div>
</section>
<section class="section" style="padding-top:0">
  <div class="wrap"><div class="proj-grid two-up">{kaarten}
  </div></div>
</section>
{cta_band()}'''
    return page('projecten.html', 'Projecten | GTF Franzen', 'Een greep uit de events van GTF Franzen: jubilea, festivals, dorpsfeesten en meer. Geluid, licht en complete productie uit één hand.',
                body, dark_header=False)


def project(p):
    fotos = [f'assets/img/{f}' for f in p['fotos']] if 'fotos' in p else [f'assets/img/proj/{p["map"]}/{i:02d}.jpg' for i in range(1, p['n'] + 1)]
    cover = f'assets/img/{p["cover"]}' if 'cover' in p else f'assets/img/proj/{p["map"]}/cover.jpg'
    grid = ''.join(f'<button class="ph reveal" type="button" data-i="{i}" aria-label="Foto {i + 1} groot bekijken"><img src="{f}" alt="{p["titel"]}, foto {i + 1}" loading="lazy"></button>' for i, f in enumerate(fotos))
    pers = f'<div><span>In de pers</span><a class="link-arrow" href="{p["pers"][1]}" target="_blank" rel="noopener">{p["pers"][0]}</a></div>' if p['pers'] else ''
    body = f'''<section class="pp-hero">
  <img src="{cover}" alt="" fetchpriority="high">
  <div class="wrap">
    <p class="crumb"><a href="projecten.html">Projecten</a> / {p["titel"]}</p>
    <h1 class="display xl">{p["titel"]}</h1>
    <p class="pp-sub">{p["sub"]} · {p["plek"]} · {p["jaar"]}</p>
  </div>
</section>
<section class="section">
  <div class="wrap two">
    <p class="lead reveal">{p["tekst"]}</p>
    <div class="pp-facts reveal"><div><span>Wie deed wat</span><b>{p["rol"]}</b></div>{pers}<div><span>Foto’s</span><b>{len(fotos)} beelden</b></div></div>
  </div>
</section>
<section class="section" style="padding-top:0">
  <div class="wrap"><div class="gallery" data-gallery='{json.dumps(fotos)}' data-title="{p["titel"]}">{grid}</div></div>
</section>
{cta_band()}'''
    return page(f'project-{p["slug"]}.html', f'{p["titel"]} | Projecten | GTF Franzen', f'{p["titel"]}, {p["sub"].lower()} in {p["plek"]} ({p["jaar"]}). Een project van GTF Franzen.',
                body, image=cover)


# ---------------------------------------------------------------- Contact
def contact():
    actie = f'mailto:{MAIL}' if MAIL else ''
    body = f'''<section class="page-hero contact-hero">
  <div class="wrap two">
    <div>
      {eyebrow('—', 'Offerte & contact')}
      <h1 class="display xl reveal">Jouw event<br><em>start hier.</em></h1>
      <p class="lead reveal">Vertel ons wat je van plan bent. Je hoeft nog niet alles te weten, daar helpen we je juist bij. Je krijgt snel een persoonlijke reactie van de familie.</p>
      {contact_list()}
    </div>
    <form class="quote-form reveal" data-mail="{MAIL}" action="{actie}" method="post" enctype="text/plain">
      <fieldset class="chips"><legend>Wat organiseer je?</legend>{"".join(f'<label><input type="radio" name="type" value="{e["id"]}"{" checked" if i == 0 else ""}><span>{e["label"]}</span></label>' for i, e in enumerate(EVENTS))}</fieldset>
      <fieldset class="chips"><legend>Waar heb je ons voor nodig?</legend>{"".join(f'<label><input type="checkbox" name="nodig" value="{d["titel"]}"><span>{d["titel"]}</span></label>' for d in DIENSTEN)}</fieldset>
      <div class="row2"><label>Datum<input type="date" name="datum"></label><label>Aantal gasten<input type="number" name="gasten" min="0" inputmode="numeric" placeholder="bijv. 500"></label></div>
      <label>Locatie<input type="text" name="locatie" placeholder="Plaats of naam van de locatie"></label>
      <div class="row2"><label>Naam<input type="text" name="naam" required autocomplete="name"></label><label>Telefoon<input type="tel" name="telefoon" autocomplete="tel"></label></div>
      <label>E-mail<input type="email" name="email" required autocomplete="email"></label>
      <label>Vertel iets over je event<textarea name="bericht" rows="5" placeholder="Wat voor sfeer, welke artiesten, wat is er al geregeld?"></textarea></label>
      <button class="btn fill" type="submit">Verstuur aanvraag</button>
      <p class="form-note" role="status"></p>
      <noscript><p class="form-note">{"Je kunt ons ook direct mailen." if MAIL else ""}</p></noscript>
    </form>
  </div>
</section>'''
    return page('contact.html', 'Offerte & contact | GTF Franzen', 'Vraag vrijblijvend een offerte aan bij GTF Franzen voor geluid, licht, stroom of een complete productie. Persoonlijk contact met de familie.',
                body, dark_header=False, body_cls='contact')


def privacy():
    body = f'''<section class="page-hero">
  <div class="wrap narrow">
    {eyebrow('—', 'Privacy')}
    <h1 class="display reveal">Privacyverklaring</h1>
    <div class="prose reveal">
      <p>GTF Franzen gaat zorgvuldig om met je gegevens. Als je contact opneemt of een offerte aanvraagt, gebruiken we je naam, contactgegevens en de informatie over je event alleen om je aanvraag te beantwoorden en je event voor te bereiden.</p>
      <p>We delen je gegevens niet met derden, behalve als dat nodig is voor de uitvoering van je event en altijd in overleg. We bewaren gegevens niet langer dan nodig.</p>
      <p>Deze website gebruikt geen tracking-cookies. Lettertypen worden geladen via Google Fonts.</p>
      <p>Wil je weten welke gegevens we van je hebben, of wil je ze laten verwijderen? Neem dan <a href="contact.html">contact</a> met ons op.</p>
    </div>
  </div>
</section>'''
    return page('privacy.html', 'Privacy | GTF Franzen', 'Privacyverklaring van GTF Franzen.', body, dark_header=False)


def notfound():
    body = '''<section class="page-hero lost">
  <div class="wrap">
    <p class="eyebrow"><span>404</span>Pagina niet gevonden</p>
    <h1 class="display xl">Hier ligt<br><em>geen kabel.</em></h1>
    <p class="lead">Deze pagina bestaat niet (meer). Geen zorgen, de rest van de site staat er nog gewoon.</p>
    <div class="btns"><a class="btn fill" href="index.html">Naar home</a><a class="btn ghost" href="contact.html">Contact</a></div>
  </div>
</section>'''
    return page('404.html', 'Pagina niet gevonden | GTF Franzen', 'Deze pagina bestaat niet.', body, dark_header=False)


def sitemap(pages):
    urls = ''.join(f'<url><loc>{BASE}{"" if p == "index.html" else p}</loc></url>' for p in pages if p != '404.html')
    (ROOT / 'sitemap.xml').write_text(f'<?xml version="1.0" encoding="UTF-8"?>\n<urlset xmlns="http://www.sitemaps.org/schemas/sitemap/0.9">{urls}</urlset>\n')
    (ROOT / 'robots.txt').write_text(f'User-agent: *\nAllow: /\n\nSitemap: {BASE}sitemap.xml\n')


if __name__ == '__main__':
    built = [home(), diensten(), over(), werkwijze(), projecten(), *[project(p) for p in PROJECTEN], contact(), privacy(), notfound()]
    sitemap(built)
    print('Gebouwd:', ', '.join(built))
