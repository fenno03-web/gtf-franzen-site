#!/usr/bin/env python3
"""Bouwt de GTF Franzen site (NL, DE, EN) uit gedeelde onderdelen. Draai: python3 build.py"""
import hashlib
import json
import shutil
from html import escape
from pathlib import Path
from urllib.parse import quote

ROOT = Path(__file__).parent

# ---------------------------------------------------------------- Gegevens
# Lege waarden worden niet getoond op de site.
MAIL = 'info@franzenbocholtz.nl'   # algemeen adres, wordt doorgestuurd
TEL = ''                            # bijv. '+31612345678'
TEL_TXT = ''                        # bijv. '+31 6 12 34 56 78'
STRAAT, POSTCODE, PLAATS = 'Pastoor Neujeanstraat 5', '6351 GK', 'Bocholtz'
INSTA = ''
FACEBOOK = ''
# Zet op het eigen domein zodra het aan GitHub Pages hangt
BASE = 'https://fenno03-web.github.io/gtf-franzen-site/'

FONTS = ('https://fonts.googleapis.com/css2?family=Archivo:wdth,wght@62..125,300..800'
         '&family=JetBrains+Mono:wght@400;500&display=swap')
LANGS = ('nl', 'de', 'en')
PREFIX = {'nl': '', 'de': 'de/', 'en': 'en/'}
LOCALE = {'nl': 'nl_NL', 'de': 'de_DE', 'en': 'en_GB'}
TAAL = {'nl': 'Nederlands', 'de': 'Deutsch', 'en': 'English'}


def ver(path):
    return hashlib.md5((ROOT / path).read_bytes()).hexdigest()[:8]


# Bestandsnaam per pagina en taal
SLUG = {
    'home':      {'nl': 'index.html', 'de': 'index.html', 'en': 'index.html'},
    'geluid':    {'nl': 'geluid.html', 'de': 'ton.html', 'en': 'sound.html'},
    'omroep':    {'nl': 'omroep-100v.html', 'de': '100v-ela-anlage-mieten.html', 'en': '100v-pa-system-hire.html'},
    'licht':     {'nl': 'licht-en-video.html', 'de': 'licht-und-video.html', 'en': 'lighting-and-video.html'},
    'stroom':    {'nl': 'stroom-en-infra.html', 'de': 'strom-und-infrastruktur.html', 'en': 'power-and-infrastructure.html'},
    'verhuur':   {'nl': 'verhuur.html', 'de': 'verleih.html', 'en': 'rental.html'},
    'projecten': {'nl': 'projecten.html', 'de': 'projekte.html', 'en': 'projects.html'},
    'nieuws':    {'nl': 'nieuws.html', 'de': 'aktuelles.html', 'en': 'news.html'},
    'over':      {'nl': 'over-ons.html', 'de': 'ueber-uns.html', 'en': 'about.html'},
    'contact':   {'nl': 'contact.html', 'de': 'kontakt.html', 'en': 'contact.html'},
}
DIENSTEN = ('geluid', 'omroep', 'licht', 'stroom')

# ---------------------------------------------------------------- Teksten van de interface
UI = {
    'nl': {
        'skip': 'Naar de inhoud', 'menu': 'Menu', 'contact': 'Contact', 'cta': 'Project bespreken', 'werk': 'Bekijk ons werk',
        'nav': {'geluid': 'Geluid', 'omroep': 'Omroep', 'licht': 'Licht en video', 'stroom': 'Stroom en infra',
                'verhuur': 'Verhuur', 'projecten': 'Projecten', 'nieuws': 'Nieuws', 'over': 'Over ons'},
        'diensten': 'Diensten', 'meer': 'Meer', 'adres': 'Adres', 'taal': 'Taal', 'mail': 'E-mail', 'tel': 'Telefoon',
        'privacy': 'Privacy', 'krijgt': 'Wat u krijgt', 'materiaal': 'Materiaal', 'aanpak': 'Zo werken wij', 'faq': 'Veel&shy;gestelde vragen',
        'naar_verhuur': 'Naar de verhuurcatalogus', 'lees': 'Lees meer', 'terug': 'Alle nieuws', 'werkgebied': 'Nederland · België · Duitsland',
        'cta_kop': 'Uw<br>evenement?', 'cta_txt': 'Vertel ons wat u van plan bent. U krijgt antwoord van de mensen die het ook gaan bouwen.',
        'onderwerp': 'Aanvraag via de website', 'foot': 'Geluid, omroep, licht, video en stroom voor evenementen. Uit Bocholtz, sinds de jaren zestig.',
        'live': 'Live', 'credit': 'Foto: Highlite', 'home': 'Home', 'prijs': 'Prijzen op aanvraag',
    },
    'de': {
        'skip': 'Zum Inhalt', 'menu': 'Menü', 'contact': 'Kontakt', 'cta': 'Projekt besprechen', 'werk': 'Unsere Arbeit',
        'nav': {'geluid': 'Ton', 'omroep': 'Beschallung', 'licht': 'Licht und Video', 'stroom': 'Strom und Infra',
                'verhuur': 'Verleih', 'projecten': 'Projekte', 'nieuws': 'Aktuelles', 'over': 'Über uns'},
        'diensten': 'Leistungen', 'meer': 'Mehr', 'adres': 'Adresse', 'taal': 'Sprache', 'mail': 'E-Mail', 'tel': 'Telefon',
        'privacy': 'Datenschutz (NL)', 'krijgt': 'Das bekommen Sie', 'materiaal': 'Material', 'aanpak': 'So arbeiten wir', 'faq': 'Häufige Fragen',
        'naar_verhuur': 'Zum Mietkatalog', 'lees': 'Weiterlesen', 'terug': 'Alle Neuigkeiten', 'werkgebied': 'Niederlande · Belgien · Deutschland',
        'cta_kop': 'Ihre<br>Veranstaltung?', 'cta_txt': 'Erzählen Sie uns, was Sie vorhaben. Sie bekommen Antwort von den Leuten, die es auch aufbauen.',
        'onderwerp': 'Anfrage über die Website', 'foot': 'Ton, Beschallung, Licht, Video und Strom für Veranstaltungen. Aus Bocholtz (NL), seit den sechziger Jahren.',
        'live': 'Live', 'credit': 'Foto: Highlite', 'home': 'Start', 'prijs': 'Preise auf Anfrage',
    },
    'en': {
        'skip': 'Skip to content', 'menu': 'Menu', 'contact': 'Contact', 'cta': 'Discuss a project', 'werk': 'See our work',
        'nav': {'geluid': 'Sound', 'omroep': 'Public address', 'licht': 'Lighting and video', 'stroom': 'Power and infra',
                'verhuur': 'Rental', 'projecten': 'Projects', 'nieuws': 'News', 'over': 'About'},
        'diensten': 'Services', 'meer': 'More', 'adres': 'Address', 'taal': 'Language', 'mail': 'Email', 'tel': 'Phone',
        'privacy': 'Privacy (NL)', 'krijgt': 'What you get', 'materiaal': 'Equipment', 'aanpak': 'How we work', 'faq': 'Frequently asked questions',
        'naar_verhuur': 'See the rental catalogue', 'lees': 'Read more', 'terug': 'All news', 'werkgebied': 'Netherlands · Belgium · Germany',
        'cta_kop': 'Your<br>event?', 'cta_txt': 'Tell us what you have in mind. You will hear back from the people who will actually build it.',
        'onderwerp': 'Enquiry via the website', 'foot': 'Sound, public address, lighting, video and power for events. From Bocholtz (NL), since the sixties.',
        'live': 'Live', 'credit': 'Photo: Highlite', 'home': 'Home', 'prijs': 'Prices on request',
    },
}

# ---------------------------------------------------------------- Diensten
# Schrijf altijd vanuit "wij". Geen masten, geen merken van hoorns, niets over het inhuren van aggregaten.
DIENST = {
    'geluid': {
        'nr': '01', 'home': 'console.jpg', 'hero': 'console2.jpg', 'inset': ('vi1.jpg', 'Soundcraft Vi1'), 'strip': ['linearray2.jpg', 'odin.jpg', 'dynacord.jpg'],
        'gear': ['d&b audiotechnik E8', 'Dynacord Cobra 4', 'Dynacord Madras M18', 'Soundcraft Vi1', 'Bose 802'],
        'nl': {
            'titel': 'Geluid', 'seo': ('Geluid voor evenementen | GTF Franzen',
                                       'Wij verzorgen geluid voor festivals, tenten en podia in Nederland, België en Duitsland. Line arrays, monitoring en onze eigen technici.'),
            'kort': 'Van een feesttent tot een festivalpodium. Line arrays, monitoring en een technicus van ons achter de tafel.',
            'sub': 'Line arrays, monitoring en bediening voor podia, tenten en terreinen.',
            'lead': 'Met geluid zijn we begonnen. Het is nog steeds waar we het meest van houden.',
            'tekst': ['We werken met systemen van d&amp;b audiotechnik en Dynacord en mixen op een Soundcraft Vi1. We stemmen alles af op de ruimte en het programma, en een van onze technici staat achter de tafel tot de laatste act.'],
            'krijg': ['Line arrays, subs en fills', 'Monitoring voor podium en DJ', 'Draadloze microfoons en headsets', 'Bediening door onze eigen technici'],
        },
        'de': {
            'titel': 'Ton', 'seo': ('Ton für Veranstaltungen | GTF Franzen',
                                    'Wir liefern Ton für Festivals, Zelte und Bühnen in Deutschland, den Niederlanden und Belgien. Line Arrays, Monitoring und eigene Techniker.'),
            'kort': 'Vom Festzelt bis zur Festivalbühne. Line Arrays, Monitoring und ein Techniker von uns am Pult.',
            'sub': 'Line Arrays, Monitoring und Betreuung für Bühnen, Zelte und Gelände.',
            'lead': 'Mit Ton haben wir angefangen. Und es ist immer noch das, was wir am liebsten machen.',
            'tekst': ['Wir arbeiten mit Systemen von d&amp;b audiotechnik und Dynacord und mischen auf einem Soundcraft Vi1. Alles wird auf Raum und Programm abgestimmt, und einer unserer Techniker steht bis zum letzten Act am Pult.'],
            'krijg': ['Line Arrays, Subwoofer und Fills', 'Monitoring für Bühne und DJ', 'Funkmikrofone und Headsets', 'Betreuung durch eigene Techniker'],
        },
        'en': {
            'titel': 'Sound', 'seo': ('Sound for events | GTF Franzen',
                                      'We provide sound for festivals, tents and stages in the Netherlands, Belgium and Germany. Line arrays, monitoring and our own engineers.'),
            'kort': 'From a marquee to a festival stage. Line arrays, monitoring and one of our engineers at the desk.',
            'sub': 'Line arrays, monitoring and operation for stages, tents and sites.',
            'lead': 'Sound is where we started. It is still what we love most.',
            'tekst': ['We work with systems from d&amp;b audiotechnik and Dynacord and mix on a Soundcraft Vi1. Everything is tuned to the venue and the programme, and one of our engineers stays at the desk until the last act.'],
            'krijg': ['Line arrays, subs and fills', 'Monitoring for stage and DJ', 'Wireless microphones and headsets', 'Operation by our own engineers'],
        },
    },
    'omroep': {
        'nr': '02', 'home': 'hoorns.jpg', 'hero': 'amstel-hoorn.jpg', 'inset': ('stack.jpg', 'Magazijn Bocholtz'), 'strip': ['ols.jpg', 'stack.jpg'],
        'gear': ['300+ hoorns', '100V', 'Terreinen', 'Parcoursen', 'Jurywagens'],
        'gear_t': {'de': ['300+ Hörner', '100 Volt', 'Gelände', 'Strecken', 'Jurywagen'], 'en': ['300+ horns', '100V', 'Sites', 'Race routes', 'Jury vehicles']},
        'nl': {
            'titel': 'Omroep', 'seo': ('100V omroepinstallatie huren | Omroep voor evenementen | GTF Franzen',
                                       'Wij verhuren en verzorgen 100V-omroep met meer dan 300 eigen hoorns. Voor schuttersfeesten, wielerkoersen, optochten en grote terreinen in Nederland, België en Duitsland.'),
            'kort': '100V-omroep over hele terreinen en parcoursen, met meer dan 300 eigen hoorns.',
            'sub': '100V-omroep huren, met meer dan 300 eigen hoorns. Voor terreinen, parcoursen en optochten.',
            'lead': 'Omroep is waar we in Limburg al generaties om bekendstaan. U herkent ons aan de hoorns met FRANZEN BOCHOLTZ erop.',
            'tekst': ['We hebben meer dan 300 eigen hoorns, met de versterkers, microfoons en bekabeling die erbij horen. We bepalen samen met u waar ze moeten hangen, bouwen op en verzorgen de omroep als u dat wilt. Op het Oud Limburgs Schuttersfeest hingen er meer dan 140, langs de Amstel Gold Race hangen ze langs het parcours.'],
            'krijg': ['100V-omroep over grote terreinen en lange routes', 'Omroep op jurywagens en mobiele omroep', 'Omroep voor optochten en wielerkoersen', 'Microfoons voor speaker en presentator'],
            'faq': [('Kan ik bij jullie een 100V-omroepinstallatie huren?', 'Ja. We verhuren complete 100V-omroep uit eigen voorraad: hoorns, versterkers, microfoons en bekabeling. Meestal bouwen we zelf op, zodat u zeker weet dat alles werkt.'),
                    ('Wat is 100V-omroep?', 'Een systeem waarmee u veel hoorns via lange kabels op één versterker aansluit. Betrouwbaar en geschikt voor grote terreinen, routes en gebouwen.'),
                    ('Hoeveel hoorns kunnen jullie plaatsen?', 'We hebben er meer dan 300. Hoeveel er nodig zijn, hangt af van het terrein. Op het Oud Limburgs Schuttersfeest hingen er meer dan 140.'),
                    ('Doen jullie ook omroep op jurywagens?', 'Ja. Op schuttersfeesten zoals het OLS reden meerdere jurywagens met onze omroep.'),
                    ('Waar werken jullie?', 'Vanuit Bocholtz in heel Nederland, België en Duitsland. Aken, Luik en Maastricht liggen om de hoek.'),
                    ('Wat kost het?', 'Dat hangt af van het aantal hoorns, de afstanden en de duur. U krijgt altijd een offerte op maat.')],
        },
        'de': {
            'titel': 'Beschallung', 'seo': ('100-Volt-ELA-Anlage mieten | Beschallung für Veranstaltungen | GTF Franzen',
                                            'Wir vermieten und betreuen 100-Volt-ELA-Anlagen mit über 300 eigenen Hornlautsprechern. Für Schützenfeste, Radrennen, Umzüge und große Gelände, direkt an der Grenze bei Aachen.'),
            'kort': '100-Volt-Beschallung über ganze Gelände und Strecken, mit über 300 eigenen Hörnern.',
            'sub': '100-Volt-ELA-Anlagen mieten, mit über 300 eigenen Hörnern. Für Gelände, Strecken und Umzüge.',
            'lead': 'Beschallung ist das, wofür man uns in Limburg seit Generationen kennt. Sie erkennen uns an den Hörnern mit der Aufschrift FRANZEN BOCHOLTZ.',
            'tekst': ['Wir haben über 300 eigene Hornlautsprecher, dazu Verstärker, Mikrofone und Verkabelung. Wir planen mit Ihnen, wo sie hängen, bauen auf und übernehmen auf Wunsch die Betreuung. Entlang der Strecke des Amstel Gold Race sorgen sie dafür, dass das Publikum hört, was im Rennen passiert.'],
            'krijg': ['100-Volt-Beschallung über große Gelände und lange Strecken', 'Beschallung auf Jurywagen und mobil', 'Beschallung für Umzüge und Radrennen', 'Mikrofone für Sprecher und Moderation'],
            'faq': [('Kann ich bei Ihnen eine 100-Volt-ELA-Anlage mieten?', 'Ja. Wir vermieten komplette 100-Volt-Anlagen aus eigenem Bestand: Hornlautsprecher, Verstärker, Mikrofone und Kabel. In der Regel bauen wir selbst auf, damit sicher alles funktioniert.'),
                    ('Was ist eine 100-Volt-ELA-Anlage?', 'Eine Anlage, bei der viele Lautsprecher über lange Kabel an einem Verstärker hängen. Zuverlässig und ideal für große Gelände, Strecken und Gebäude.'),
                    ('Kommen Sie auch nach Deutschland?', 'Ja. Bocholtz liegt direkt an der Grenze, wenige Minuten von Aachen. Wir arbeiten regelmäßig in Deutschland.'),
                    ('Was kostet die Miete?', 'Das hängt von der Anzahl der Hörner, den Entfernungen und der Dauer ab. Sie bekommen immer ein Angebot.')],
        },
        'en': {
            'titel': 'Public address', 'seo': ('100V PA system hire | Public address for events | GTF Franzen',
                                               'We hire out and run 100V public address systems with more than 300 horn speakers of our own. For festivals, cycling races, parades and large sites, near Aachen, Liège and Maastricht.'),
            'kort': '100V public address across whole sites and race routes, with more than 300 horns of our own.',
            'sub': '100V public address hire, with more than 300 horns of our own. For sites, race routes and parades.',
            'lead': 'Public address is what we have been known for in Limburg for generations. You will recognise us by the horns that read FRANZEN BOCHOLTZ.',
            'tekst': ['We own more than 300 horn speakers, plus the amplifiers, microphones and cabling that go with them. We work out with you where they need to hang, set everything up and run it if you like. Along the Amstel Gold Race course they make sure the crowd hears what is happening in the race.'],
            'krijg': ['100V PA across large sites and long routes', 'PA on jury vehicles and mobile PA', 'PA for parades and cycling races', 'Microphones for announcers and presenters'],
            'faq': [('Can I hire a 100V public address system from you?', 'Yes. We hire out complete 100V systems from our own stock: horns, amplifiers, microphones and cabling. We usually set up ourselves so you know everything works.'),
                    ('What is a 100V public address system?', 'A system where many speakers run to one amplifier over long cables. Reliable and ideal for large sites, routes and buildings.'),
                    ('Where do you work?', 'From Bocholtz across the Netherlands, Belgium and Germany. Aachen, Liège and Maastricht are all close by.'),
                    ('How much does it cost?', 'That depends on the number of horns, the distances and the duration. You always get a tailored quote.')],
        },
    },
    'licht': {
        'nr': '03', 'home': 'sc-wit.jpg', 'hero': 'sc-04.jpg', 'inset': ('led.jpg', 'Showtec Polar 340 WashFX'), 'strip': ['sc-26.jpg', 'moving-rood.jpg', 'sc-24.jpg'],
        'gear': ['Infinity Furion S601', 'Showtec Polar 340', 'Shark The Meg Beam One', 'Helix S5000', 'DMT Pixelmesh LED'],
        'credit': True, 'matrix': True,
        'nl': {
            'titel': 'Licht en video', 'seo': ('Licht, video en LED-wanden voor evenementen | GTF Franzen',
                                               'Wij verzorgen podiumlicht, siteverlichting en LED-wanden voor festivals en evenementen in Nederland, België en Duitsland. Samen met MATRIX E.I.L.'),
            'kort': 'Podiumlicht, siteverlichting en LED-wanden. Ontworpen voor uw programma en live bediend.',
            'sub': 'Podiumlicht, siteverlichting en LED-wanden. Ontworpen voor uw programma en live bediend.',
            'lead': 'Licht bepaalt hoe een avond voelt, en hoe een terrein er in het donker uitziet.',
            'tekst': ['Van een podium vol moving heads, beams en strobes tot de verlichting van een heel terrein. Met onze LED-wanden laten we visuals, sponsors of livebeelden zien.'],
            'krijg': ['Lichtontwerp en programmering', 'Moving heads, washes, beams en strobes', 'Siteverlichting', 'LED-wanden en visuals'],
        },
        'de': {
            'titel': 'Licht und Video', 'seo': ('Licht, Video und LED-Wände für Veranstaltungen | GTF Franzen',
                                                'Wir liefern Bühnenlicht, Geländebeleuchtung und LED-Wände für Festivals und Veranstaltungen in Deutschland, den Niederlanden und Belgien. Zusammen mit MATRIX E.I.L.'),
            'kort': 'Bühnenlicht, Geländebeleuchtung und LED-Wände. Geplant für Ihr Programm und live gefahren.',
            'sub': 'Bühnenlicht, Geländebeleuchtung und LED-Wände. Geplant für Ihr Programm und live gefahren.',
            'lead': 'Licht bestimmt, wie sich ein Abend anfühlt, und wie ein Gelände im Dunkeln aussieht.',
            'tekst': ['Von der Bühne voller Moving Heads, Beams und Strobes bis zur Beleuchtung eines ganzen Geländes. Auf unseren LED-Wänden zeigen wir Visuals, Sponsoren oder Live-Bilder.'],
            'krijg': ['Lichtplanung und Programmierung', 'Moving Heads, Washes, Beams und Strobes', 'Geländebeleuchtung', 'LED-Wände und Visuals'],
        },
        'en': {
            'titel': 'Lighting and video', 'seo': ('Lighting, video and LED walls for events | GTF Franzen',
                                                   'We provide stage lighting, site lighting and LED walls for festivals and events in the Netherlands, Belgium and Germany. Together with MATRIX E.I.L.'),
            'kort': 'Stage lighting, site lighting and LED walls. Designed for your programme and run live.',
            'sub': 'Stage lighting, site lighting and LED walls. Designed for your programme and run live.',
            'lead': 'Lighting decides how a night feels, and what a site looks like after dark.',
            'tekst': ['From a stage full of moving heads, beams and strobes to lighting across an entire site. On our LED walls we show visuals, sponsors or live footage.'],
            'krijg': ['Lighting design and programming', 'Moving heads, washes, beams and strobes', 'Site lighting', 'LED walls and visuals'],
        },
    },
    'stroom': {
        'nr': '04', 'home': 'takels.jpg', 'hero': 'sc-20.jpg', 'inset': ('latch.jpg', 'Bocholtz'), 'strip': ['rack.jpg', 'sc-22.jpg', 'sc-21.jpg'],
        'credit': True,
        'gear': ['Stroomplan', 'Stroomverdeling', 'Truss', 'Rigging', 'Glasvezel', 'Art-Net'],
        'gear_t': {'de': ['Stromplan', 'Stromverteilung', 'Traversen', 'Rigging', 'Glasfaser', 'Art-Net'],
                   'en': ['Power plan', 'Power distribution', 'Truss', 'Rigging', 'Fibre', 'Art-Net']},
        'nl': {
            'titel': 'Stroom en infra', 'seo': ('Stroom, truss en infra voor evenementen | GTF Franzen',
                                                'Wij maken het stroomplan, verzorgen de stroomverdeling en bouwen truss en rigging voor festivals en buitenevenementen in Nederland, België en Duitsland.'),
            'kort': 'Stroomplan, verdeling over het terrein, truss en rigging. Zodat alles de hele dag blijft draaien.',
            'sub': 'Stroomplan, stroomverdeling, truss en rigging. Zodat alles op het terrein de hele dag blijft draaien.',
            'lead': 'Op een weiland begint alles bij stroom. Daar beginnen wij ook.',
            'tekst': ['We maken het stroomplan, regelen de stroom en verzorgen de verdeling over het hele terrein. Daarnaast bouwen we truss en rigging voor podia en lichtplannen, en leggen we het netwerk aan voor geluid, licht en video.'],
            'krijg': ['Stroomplan en stroomverdeling', 'Aansluitingen voor podium, bars en standhouders', 'Truss en rigging', 'Glasvezel- en datanetwerk'],
        },
        'de': {
            'titel': 'Strom und Infra', 'seo': ('Strom, Traversen und Infrastruktur für Veranstaltungen | GTF Franzen',
                                                'Wir erstellen den Stromplan, übernehmen die Stromverteilung und bauen Traversen und Rigging für Festivals und Open-Air-Veranstaltungen.'),
            'kort': 'Stromplan, Verteilung über das Gelände, Traversen und Rigging. Damit den ganzen Tag alles läuft.',
            'sub': 'Stromplan, Stromverteilung, Traversen und Rigging. Damit auf dem Gelände den ganzen Tag alles läuft.',
            'lead': 'Auf einer Wiese beginnt alles mit Strom. Da fangen wir auch an.',
            'tekst': ['Wir erstellen den Stromplan, organisieren den Strom und übernehmen die Verteilung über das ganze Gelände. Außerdem bauen wir Traversen und Rigging für Bühnen und Lichtpläne und legen das Netzwerk für Ton, Licht und Video.'],
            'krijg': ['Stromplan und Stromverteilung', 'Anschlüsse für Bühne, Bars und Aussteller', 'Traversen und Rigging', 'Glasfaser- und Datennetz'],
        },
        'en': {
            'titel': 'Power and infra', 'seo': ('Power, truss and infrastructure for events | GTF Franzen',
                                                'We make the power plan, handle power distribution and build truss and rigging for festivals and outdoor events.'),
            'kort': 'Power plan, distribution across the site, truss and rigging. So everything keeps running all day.',
            'sub': 'Power plan, power distribution, truss and rigging. So everything on site keeps running all day.',
            'lead': 'In an empty field, everything starts with power. So that is where we start too.',
            'tekst': ['We make the power plan, arrange the power and handle distribution across the whole site. We also build truss and rigging for stages and lighting rigs, and lay the network for sound, lighting and video.'],
            'krijg': ['Power plan and distribution', 'Connections for stage, bars and vendors', 'Truss and rigging', 'Fibre and data network'],
        },
    },
}

MATRIX = 'https://fenno03-web.github.io/matrix-eil-site/'
MATRIX_TXT = {
    'nl': ('Samen met MATRIX E.I.L.', 'Voor lichtontwerp, LED en visuals werken we samen met MATRIX E.I.L. uit Bocholtz.', 'Naar MATRIX E.I.L.'),
    'de': ('Zusammen mit MATRIX E.I.L.', 'Für Lichtdesign, LED und Visuals arbeiten wir mit MATRIX E.I.L. aus Bocholtz zusammen.', 'Zu MATRIX E.I.L.'),
    'en': ('Together with MATRIX E.I.L.', 'For lighting design, LED and visuals we work together with MATRIX E.I.L. from Bocholtz.', 'Visit MATRIX E.I.L.'),
}

# ---------------------------------------------------------------- Projecten
# Bij ZLF nooit "volledige productie" schrijven: GTF deed daar de techniek.
PROJECTEN = [
    {'naam': 'ZLF', 'jaar': '2025', 'img': None,
     'nl': 'Stroom en infra, licht, geluid, video, siteverlichting en omroep', 'de': 'Strom und Infra, Licht, Ton, Video, Geländebeleuchtung und Beschallung', 'en': 'Power and infra, lighting, sound, video, site lighting and public address'},
    {'naam': 'Amstel Gold Race', 'jaar': '2025 — 2026', 'img': 'amstel.jpg',
     'nl': 'Omroep langs het parcours', 'de': 'Beschallung entlang der Strecke', 'en': 'Public address along the course'},
    {'naam': 'Oud Limburgs Schuttersfeest', 'jaar': '2024', 'img': 'ols.jpg',
     'nl': 'Omroep over het terrein en op de jurywagens', 'de': 'Beschallung über das Gelände und auf den Jurywagen', 'en': 'Public address across the site and on the jury vehicles'},
    {'naam': 'Sportclub’25 · 100 jaar', 'jaar': '2025', 'img': 'sc-goud.jpg',
     'nl': 'Live productie', 'de': 'Live-Produktion', 'en': 'Live production'},
    {'naam': 'BVV Kalk aan de Books', 'jaar': '—', 'img': None,
     'nl': 'Live productie', 'de': 'Live-Produktion', 'en': 'Live production'},
    {'naam': 'CV De Pankes', 'jaar': '—', 'img': None,
     'nl': 'Live productie', 'de': 'Live-Produktion', 'en': 'Live production'},
]

# ---------------------------------------------------------------- Uit het magazijn (eigen voorraad, november 2026)
UITGELICHT = [('300+', {'nl': 'Omroephoorns', 'de': 'Hornlautsprecher', 'en': 'Horn speakers'}, {'nl': 'Omroep · 100V', 'de': 'Beschallung · 100 V', 'en': 'Public address · 100V'}),
              ('32×', 'Bose 802', 'Audio'), ('24×', 'DMT Pixelmesh E12.5', 'Video · LED'), ('14×', 'Showtec Polar 340 WashFX', {'nl': 'Licht', 'de': 'Licht', 'en': 'Lighting'}),
              ('12×', 'Helix S5000 Q4', {'nl': 'Licht', 'de': 'Licht', 'en': 'Lighting'}), ('8×', 'd&amp;b audiotechnik E8', 'Audio'),
              ('8×', 'Dynacord Madras M18', 'Audio · sub'), ('4×', 'Infinity Furion S601', {'nl': 'Licht · profile', 'de': 'Licht · Profiler', 'en': 'Lighting · profile'}),
              ('1×', 'Soundcraft Vi1', 'Audio · FOH')]

# Verhuurcatalogus: selectie uit de eigen voorraad (zonder kabels, kleine accessoires en flightcases)
CATALOGUS = [
    ('omroep', 'stack.jpg', {'nl': 'Omroep', 'de': 'Beschallung', 'en': 'Public address'}, [
        ('Omroephoorns', {'nl': 'Meer dan 300 stuks', 'de': 'Über 300 Stück', 'en': 'More than 300'}),
        ('100V-versterkers', {'nl': 'Voor omroep over lange afstanden', 'de': 'Für Beschallung über lange Strecken', 'en': 'For PA over long distances'}),
        ('Speakermicrofoons', {'nl': 'Voor speaker en jury', 'de': 'Für Sprecher und Jury', 'en': 'For announcers and judges'})]),
    ('geluid', 'odin.jpg', {'nl': 'Geluid', 'de': 'Ton', 'en': 'Sound'}, [
        ('d&amp;b audiotechnik E8', {'nl': 'Fullrange-luidspreker', 'de': 'Fullrange-Lautsprecher', 'en': 'Full-range loudspeaker'}),
        ('Dynacord Cobra 4', {'nl': 'Top, PWH en FAR, met amprack', 'de': 'Top, PWH und FAR, mit Amp-Rack', 'en': 'Top, PWH and FAR, with amp rack'}),
        ('Dynacord Cobra 2', {'nl': 'Subs met amprack', 'de': 'Subwoofer mit Amp-Rack', 'en': 'Subs with amp rack'}),
        ('Dynacord Madras M18', {'nl': 'Subwoofer', 'de': 'Subwoofer', 'en': 'Subwoofer'}),
        ('Dynacord Madras M15 / M212', {'nl': 'Fullrange', 'de': 'Fullrange', 'en': 'Full-range'}),
        ('Bose 802', {'nl': 'Compacte luidspreker', 'de': 'Kompaktlautsprecher', 'en': 'Compact loudspeaker'}),
        ('Dynacord M12 / AM12', {'nl': 'Podiummonitor', 'de': 'Bühnenmonitor', 'en': 'Stage monitor'}),
        ('ODIN SF-12A / SF-15A', {'nl': 'Sidefill', 'de': 'Sidefill', 'en': 'Side fill'}),
        ('Soundcraft Vi1', {'nl': 'Digitale mengtafel met glasvezel-stagebox', 'de': 'Digitalpult mit Glasfaser-Stagebox', 'en': 'Digital console with fibre stagebox'}),
        ('Sennheiser draadloos', {'nl': 'Microfoons, headsets en antennes', 'de': 'Mikrofone, Headsets und Antennen', 'en': 'Microphones, headsets and antennas'}),
        ('BSS DI-boxen', {'nl': 'DI', 'de': 'DI', 'en': 'DI'}),
        ('Showgear MAT-350', {'nl': 'Line-array-toren', 'de': 'Line-Array-Turm', 'en': 'Line array tower'})]),
    ('licht', 'sc-27.jpg', {'nl': 'Licht', 'de': 'Licht', 'en': 'Lighting'}, [
        ('Infinity Furion S601 / S201', {'nl': 'Profile moving heads', 'de': 'Profile Moving Heads', 'en': 'Profile moving heads'}),
        ('Showtec Shark The Meg Beam One', {'nl': 'Beam', 'de': 'Beam', 'en': 'Beam'}),
        ('Showtec Polar 340 WashFX', {'nl': 'Wash moving head', 'de': 'Wash Moving Head', 'en': 'Wash moving head'}),
        ('Showtec Polar 300 Hybrid', {'nl': 'Hybride moving head', 'de': 'Hybrid Moving Head', 'en': 'Hybrid moving head'}),
        ('Showtec Phantom 3R Hybrid', {'nl': 'Hybride moving head', 'de': 'Hybrid Moving Head', 'en': 'Hybrid moving head'}),
        ('Showtec Phantom Matrix FX', {'nl': 'Effect', 'de': 'Effekt', 'en': 'Effect'}),
        ('Helix S5000 Q4 / S4000 Q4', {'nl': 'Profielspot, met filters en barndoors', 'de': 'Profilscheinwerfer mit Filtern und Torblenden', 'en': 'Profile spot, with filters and barn doors'}),
        ('Showtec Performer 3000 LED', {'nl': 'Theaterspot', 'de': 'Theaterscheinwerfer', 'en': 'Theatre spot'}),
        ('Infinity TF-300 Fresnel', {'nl': 'Fresnel, warm wit', 'de': 'Fresnel, warmweiß', 'en': 'Fresnel, warm white'}),
        ('Infinity IW-1240 / IPW-150', {'nl': 'Wash en sunpanel', 'de': 'Wash und Sunpanel', 'en': 'Wash and sun panel'}),
        ('Showtec Octostrip MKII', {'nl': 'Pixelbar', 'de': 'Pixelbar', 'en': 'Pixel bar'}),
        ('Showtec Sunstrip Active', {'nl': 'Retro-effect', 'de': 'Retro-Effekt', 'en': 'Retro effect'}),
        ('Stage Blinder FLEX Blaze', {'nl': 'Blinder', 'de': 'Blinder', 'en': 'Blinder'}),
        ('Eurolite IP PIX Strobe / Spectra Strobe', {'nl': 'Strobe', 'de': 'Strobe', 'en': 'Strobe'}),
        ('FOS Phantom Bar IP65', {'nl': 'Bar voor buiten', 'de': 'Bar für außen', 'en': 'Outdoor bar'}),
        ('Laserworld DS-3000', {'nl': 'Laser', 'de': 'Laser', 'en': 'Laser'})]),
    ('video', 'sc-06.jpg', {'nl': 'Video', 'de': 'Video', 'en': 'Video'}, [
        ('DMT Pixelmesh E12.5', {'nl': 'LED-panelen voor wanden en schermen', 'de': 'LED-Panels für Wände und Screens', 'en': 'LED panels for walls and screens'})]),
    ('effecten', 'sc-30.jpg', {'nl': 'Effecten', 'de': 'Effekte', 'en': 'Effects'}, [
        ('Antari F-4 Fazer', {'nl': 'Hazer', 'de': 'Hazer', 'en': 'Hazer'}),
        ('MagicFX Stage Flame', {'nl': 'Vlameffect', 'de': 'Flammeneffekt', 'en': 'Flame effect'}),
        ('Showgear SF-250', {'nl': 'Ventilator', 'de': 'Ventilator', 'en': 'Fan'})]),
    ('rigging', 'sc-32.jpg', {'nl': 'Truss en rigging', 'de': 'Traversen und Rigging', 'en': 'Truss and rigging'}, [
        ('Milos truss', {'nl': '0,5 tot 5 meter', 'de': '0,5 bis 5 Meter', 'en': '0.5 to 5 metres'}),
        ('Single tube', {'nl': '2 meter', 'de': '2 Meter', 'en': '2 metres'}),
        ('Showtec Wind-Up Lightstand', {'nl': 'Lichtstatief, 4 meter', 'de': 'Lichtstativ, 4 Meter', 'en': 'Lighting stand, 4 metres'}),
        ('Dynacord FG600', {'nl': 'Vliegframe', 'de': 'Flugrahmen', 'en': 'Fly frame'})]),
    ('infra', 'rack.jpg', {'nl': 'Data en infra', 'de': 'Daten und Infra', 'en': 'Data and infra'}, [
        ('Glasvezel', {'nl': 'Op haspel', 'de': 'Auf Trommel', 'en': 'On drum'}),
        ('CAT6', {'nl': 'Op haspel', 'de': 'Auf Trommel', 'en': 'On drum'}),
        ('Art-Net nodes', {'nl': '8 universes', 'de': '8 Universen', 'en': '8 universes'}),
        ('Pixelcontrollers', {'nl': 'Voor LED en pixelbars', 'de': 'Für LED und Pixelbars', 'en': 'For LED and pixel bars'})]),
]

CAT_UI = {
    'nl': {'items': 'items', 'op': '✓ Op de lijst', 'voeg': 'Op de lijst', 'een': 'item op uw aanvraaglijst', 'meer': 'items op uw aanvraaglijst',
           'hoe': 'Zet items op uw aanvraaglijst en verstuur de lijst in één keer.', 'mailintro': 'Graag een prijs voor de volgende items:'},
    'de': {'items': 'Artikel', 'op': '✓ Auf der Liste', 'voeg': 'Auf die Liste', 'een': 'Artikel auf Ihrer Anfrageliste', 'meer': 'Artikel auf Ihrer Anfrageliste',
           'hoe': 'Setzen Sie Artikel auf Ihre Anfrageliste und senden Sie sie auf einmal.', 'mailintro': 'Bitte um einen Preis für folgende Artikel:'},
    'en': {'items': 'items', 'op': '✓ On the list', 'voeg': 'Add to list', 'een': 'item on your request list', 'meer': 'items on your request list',
           'hoe': 'Add items to your request list and send it in one go.', 'mailintro': 'Please send a price for the following items:'},
}

# ---------------------------------------------------------------- Nieuws
NIEUWS = [
    {'slug': {'nl': 'nieuws-nieuwe-website.html', 'de': 'aktuelles-neue-website.html', 'en': 'news-new-website.html'},
     'datum': {'nl': 'November 2026', 'de': 'November 2026', 'en': 'November 2026'}, 'iso': '2026-11-09', 'img': 'desk-led.jpg', 'gallery': [],
     'nl': ('Een nieuwe website', 'Met een verhuurcatalogus, en voortaan ook in het Duits en Engels.',
            ['We hebben een nieuwe website. Hier vindt u wat we doen: geluid, omroep, licht en video, en stroom en infra. Ook staat er een selectie uit onze eigen voorraad, die u kunt huren.',
             'De site is er nu ook in het Duits en Engels.',
             'Op deze nieuwspagina laten we voortaan zien waar we mee bezig zijn.']),
     'de': ('Eine neue Website', 'Mit Mietkatalog, und ab jetzt auch auf Deutsch und Englisch.',
            ['Wir haben eine neue Website. Hier finden Sie, was wir machen: Ton, Beschallung, Licht und Video sowie Strom und Infrastruktur. Dazu eine Auswahl aus unserem eigenen Bestand, die Sie mieten können.',
             'Die Seite gibt es jetzt auch auf Deutsch und Englisch.',
             'Hier zeigen wir künftig, woran wir arbeiten.']),
     'en': ('A new website', 'With a rental catalogue, and now in German and English too.',
            ['We have a new website. It shows what we do: sound, public address, lighting and video, and power and infrastructure. It also lists a selection of our own equipment that you can hire.',
             'The site is now available in German and English as well.',
             'From now on, this is where we show what we are working on.'])},
    {'slug': {'nl': 'nieuws-amstel-gold-race.html', 'de': 'aktuelles-amstel-gold-race.html', 'en': 'news-amstel-gold-race.html'},
     'datum': {'nl': '2026', 'de': '2026', 'en': '2026'}, 'iso': '2026-04-01', 'img': 'amstel-hoorn.jpg', 'gallery': [],
     'nl': ('Weer langs de Amstel Gold Race', 'Ook in 2026 hingen onze hoorns langs het parcours.',
            ['Langs het parcours van de Amstel Gold Race verzorgen wij de omroep. Zo hoort het publiek langs de weg wat er in de koers gebeurt.',
             'U herkent onze hoorns aan de opdruk FRANZEN BOCHOLTZ.']),
     'de': ('Wieder beim Amstel Gold Race', 'Auch 2026 hingen unsere Hörner entlang der Strecke.',
            ['Entlang der Strecke des Amstel Gold Race sorgen wir für die Beschallung. So hört das Publikum am Straßenrand, was im Rennen passiert.',
             'Sie erkennen unsere Hörner an der Aufschrift FRANZEN BOCHOLTZ.']),
     'en': ('Back along the Amstel Gold Race', 'Our horns lined the course again in 2026.',
            ['We provide the public address along the Amstel Gold Race course, so the crowd at the roadside hears what is happening in the race.',
             'You will recognise our horns by the FRANZEN BOCHOLTZ lettering.'])},
    {'slug': {'nl': 'nieuws-sportclub-25.html', 'de': 'aktuelles-sportclub-25.html', 'en': 'news-sportclub-25.html'},
     'datum': {'nl': '2025', 'de': '2025', 'en': '2025'}, 'iso': '2025-06-01', 'img': 'sc-13.jpg', 'gallery': ['sc-18.jpg', 'sc-14.jpg', 'sc-15.jpg', 'sc-19.jpg', 'sc-29.jpg'], 'credit': True,
     'nl': ('100 jaar Sportclub’25', 'Het jubileumfeest in Bocholtz, met de live productie door ons.',
            ['Sportclub’25 uit Bocholtz bestond 100 jaar, en dat werd gevierd. Wij verzorgden de live productie.',
             'Truss, moving heads, LED en een volle zaal: zo ziet een thuiswedstrijd er voor ons het liefst uit.']),
     'de': ('100 Jahre Sportclub’25', 'Das Jubiläumsfest in Bocholtz, mit der Live-Produktion von uns.',
            ['Sportclub’25 aus Bocholtz wurde 100 Jahre alt, und das wurde gefeiert. Wir haben die Live-Produktion übernommen.',
             'Traversen, Moving Heads, LED und ein voller Saal: So sieht ein Heimspiel für uns am liebsten aus.']),
     'en': ('Sportclub’25 turns 100', 'The anniversary party in Bocholtz, with live production by us.',
            ['Sportclub’25 from Bocholtz turned 100, and that called for a party. We took care of the live production.',
             'Truss, moving heads, LED and a packed hall: our favourite kind of home game.'])},
]

# ---------------------------------------------------------------- Pagina-specifieke teksten
TXT = {
    'nl': {
        'home_seo': ('GTF Franzen | Geluid, omroep, licht en stroom voor evenementen', 'GTF Franzen uit Bocholtz verzorgt geluid, 100V-omroep, licht, video en stroom voor evenementen in Nederland, België en Duitsland. Eigen materiaal, eigen ploeg, sinds de jaren zestig.'),
        'h1': 'Wij maken<br>het hoorbaar.',
        'hero_p': 'Geluid, omroep, licht, video en stroom voor evenementen in Nederland, België en Duitsland. Met eigen materiaal en een eigen ploeg, vanuit Bocholtz.',
        'intro': 'Wij doen dit al sinds de jaren zestig. <em>Dat kan geen enkele andere partij in de regio zeggen.</em> U heeft één aanspreekpunt, en dat zijn de mensen die uw evenement ook opbouwen en draaien.',
        'meters': [('±1960', 'sinds'), ('300+', 'omroephoorns'), ('100+', 'evenementen per jaar'), ('3', 'landen: NL · BE · DE')],
        'show': 'Sportclub’25 · 100 jaar · Bocholtz', 'show_r': 'Live productie: GTF',
        'mag_kop': 'Uit ons<br>magazijn', 'mag_p': 'Bijna alles wat wij inzetten is van onszelf. Ook te huur, met of zonder technicus. Prijzen op aanvraag.', 'mag_note': 'Selectie uit de eigen voorraad',
        'werk_kop': 'Werk', 'nieuws_kop': 'Nieuws',
        'roots_label': 'Sinds de jaren zestig', 'roots_kop': 'Zelfde naam.<br>Zelfde aanpak.',
        'roots_p': ['Het begon met zelfgebouwde speakers en een bus met hoorns op het dak. Het materiaal is meegegroeid, de manier van werken niet.',
                    'U belt met de mensen die uw evenement ook bouwen. Geen accountmanager ertussen, geen verrassingen op de dag zelf.'],
        'roots_btn': 'Ons verhaal',
        # verhuur
        'verhuur_seo': ('Verhuur geluid, licht, omroep en truss | Verhuurcatalogus | GTF Franzen', 'Huur geluid, licht, 100V-omroep, LED en truss uit de eigen voorraad van GTF Franzen in Bocholtz. Met of zonder technicus. Prijzen op aanvraag.'),
        'verhuur_h1': 'Verhuur', 'verhuur_sub': 'Een selectie uit onze eigen voorraad. Te huur met of zonder technicus, voor evenementen in Nederland, België en Duitsland.',
        'verhuur_intro': 'Prijzen op aanvraag. Stuur ons wat u nodig heeft en voor welke datum, dan krijgt u snel een prijs en advies over wat past.',
        'verhuur_btn': 'Prijs aanvragen', 'verhuur_onderwerp': 'Verhuuraanvraag',
        # projecten
        'proj_seo': ('Projecten | GTF Franzen', 'Een selectie van evenementen waarvoor GTF Franzen geluid, omroep, licht, video en stroom verzorgde, zoals ZLF, de Amstel Gold Race en het Oud Limburgs Schuttersfeest.'),
        'proj_h1': 'Projecten', 'proj_sub': 'Een selectie van het werk van de afgelopen jaren. Van omroep langs een parcours tot de techniek voor een heel festivalterrein.',
        # nieuws
        'nieuws_seo': ('Nieuws | GTF Franzen', 'Nieuws van GTF Franzen uit Bocholtz: projecten, materiaal en wat we verder doen.'),
        'nieuws_h1': 'Nieuws', 'nieuws_sub': 'Waar we mee bezig zijn.',
        # over
        'over_seo': ('Over GTF Franzen | Sinds de jaren zestig uit Bocholtz', 'GTF Franzen is een familiebedrijf uit Bocholtz dat sinds de jaren zestig geluid, omroep en later licht, video en stroom voor evenementen verzorgt.'),
        'over_h1': 'Over ons', 'over_sub': 'Sinds de jaren zestig uit Bocholtz. Nog steeds dezelfde familie, nog steeds dezelfde aanpak.',
        'over_lead': 'Wat begon met zelfgebouwde speakers in Bocholtz, is na meer dan zestig jaar een technisch bedrijf voor evenementen in drie landen.',
        'over_p': ['Rond 1960 begonnen we met de verhuur van geluid. Al snel kwam daar omroep bij: onze hoorns met FRANZEN BOCHOLTZ erop werden een vertrouwd beeld op schuttersfeesten, wielerkoersen en optochten in Limburg.',
                   'Daarna volgden licht, video en stroom. Het materiaal werd groter, de evenementen ook. Wat bleef: we zijn een familiebedrijf, en u spreekt direct met de mensen die het werk doen.'],
        'waarden': [('Persoonlijk', 'U heeft één aanspreekpunt, van de eerste vraag tot de laatste kabel. Iemand die uw evenement kent.'),
                    ('Eigen materiaal', 'Bijna alles wat we inzetten is van onszelf, en wordt door ons onderhouden. Dat maakt ons snel en betrouwbaar.'),
                    ('Ervaring', 'Meer dan zestig jaar evenementen. Er is weinig wat we nog niet zijn tegengekomen.')],
        'gebied_kop': 'Werkgebied', 'gebied_p': 'Bocholtz ligt op de grens. Aken ligt op tien minuten, Maastricht en Luik zijn dichtbij. We werken in heel Nederland, België en Duitsland.',
        # contact
        'contact_seo': ('Contact | GTF Franzen', 'Neem contact op met GTF Franzen in Bocholtz voor geluid, omroep, licht, video en stroom voor uw evenement.'),
        'contact_h1': 'Contact', 'contact_sub': 'Vertel ons over uw evenement. U krijgt antwoord van de mensen die het ook gaan bouwen.',
        'f': {'naam': 'Naam', 'organisatie': 'Organisatie', 'mail': 'E-mailadres', 'datum': 'Datum van het evenement', 'locatie': 'Locatie', 'bericht': 'Wat heeft u nodig?', 'stuur': 'Versturen',
              'note': 'Uw mailprogramma opent met het bericht klaar om te versturen.'},
    },
    'de': {
        'home_seo': ('GTF Franzen | Ton, Beschallung, Licht und Strom für Veranstaltungen', 'GTF Franzen aus Bocholtz (NL, bei Aachen) liefert Ton, 100-Volt-Beschallung, Licht, Video und Strom für Veranstaltungen in Deutschland, den Niederlanden und Belgien. Eigenes Material, eigenes Team, seit den sechziger Jahren.'),
        'h1': 'Wir machen<br>es hörbar.',
        'hero_p': 'Ton, Beschallung, Licht, Video und Strom für Veranstaltungen in Deutschland, den Niederlanden und Belgien. Mit eigenem Material und eigenem Team, aus Bocholtz bei Aachen.',
        'intro': 'Wir machen das seit den sechziger Jahren. <em>Das kann kein anderer Anbieter in der Region sagen.</em> Sie haben einen Ansprechpartner, und das sind die Leute, die Ihre Veranstaltung auch aufbauen und betreuen.',
        'meters': [('±1960', 'seit'), ('300+', 'Hornlautsprecher'), ('100+', 'Veranstaltungen pro Jahr'), ('3', 'Länder: NL · BE · DE')],
        'show': 'Sportclub’25 · 100 Jahre · Bocholtz', 'show_r': 'Live-Produktion: GTF',
        'mag_kop': 'Aus unserem<br>Lager', 'mag_p': 'Fast alles, was wir einsetzen, gehört uns. Auch zu mieten, mit oder ohne Techniker. Preise auf Anfrage.', 'mag_note': 'Auswahl aus dem eigenen Bestand',
        'werk_kop': 'Arbeit', 'nieuws_kop': 'Aktuelles',
        'roots_label': 'Seit den sechziger Jahren', 'roots_kop': 'Gleicher Name.<br>Gleiche Haltung.',
        'roots_p': ['Angefangen hat es mit selbstgebauten Lautsprechern und einem Bus mit Hörnern auf dem Dach. Das Material ist mitgewachsen, die Art zu arbeiten nicht.',
                    'Sie sprechen mit den Leuten, die Ihre Veranstaltung auch aufbauen. Kein Vermittler dazwischen, keine Überraschungen am Tag selbst.'],
        'roots_btn': 'Unsere Geschichte',
        'verhuur_seo': ('Verleih Ton, Licht, Beschallung und Traversen | Mietkatalog | GTF Franzen', 'Mieten Sie Ton, Licht, 100-Volt-Beschallung, LED und Traversen aus dem eigenen Bestand von GTF Franzen in Bocholtz bei Aachen. Mit oder ohne Techniker. Preise auf Anfrage.'),
        'verhuur_h1': 'Verleih', 'verhuur_sub': 'Eine Auswahl aus unserem eigenen Bestand. Zu mieten mit oder ohne Techniker, für Veranstaltungen in Deutschland, den Niederlanden und Belgien.',
        'verhuur_intro': 'Preise auf Anfrage. Schicken Sie uns, was Sie brauchen und für welches Datum, dann bekommen Sie schnell einen Preis und eine Empfehlung.',
        'verhuur_btn': 'Preis anfragen', 'verhuur_onderwerp': 'Mietanfrage',
        'proj_seo': ('Projekte | GTF Franzen', 'Eine Auswahl von Veranstaltungen, für die GTF Franzen Ton, Beschallung, Licht, Video und Strom geliefert hat, etwa ZLF, das Amstel Gold Race und das Oud Limburgs Schuttersfeest.'),
        'proj_h1': 'Projekte', 'proj_sub': 'Eine Auswahl der letzten Jahre. Von der Beschallung entlang einer Rennstrecke bis zur Technik für ein ganzes Festivalgelände.',
        'nieuws_seo': ('Aktuelles | GTF Franzen', 'Neuigkeiten von GTF Franzen aus Bocholtz: Projekte, Material und mehr.'),
        'nieuws_h1': 'Aktuelles', 'nieuws_sub': 'Woran wir arbeiten.',
        'over_seo': ('Über GTF Franzen | Seit den sechziger Jahren aus Bocholtz', 'GTF Franzen ist ein Familienunternehmen aus Bocholtz (NL), das seit den sechziger Jahren Ton, Beschallung und später Licht, Video und Strom für Veranstaltungen liefert.'),
        'over_h1': 'Über uns', 'over_sub': 'Seit den sechziger Jahren aus Bocholtz. Immer noch dieselbe Familie, immer noch dieselbe Haltung.',
        'over_lead': 'Was mit selbstgebauten Lautsprechern in Bocholtz begann, ist nach über sechzig Jahren ein Technikunternehmen für Veranstaltungen in drei Ländern.',
        'over_p': ['Um 1960 haben wir mit dem Verleih von Tontechnik angefangen. Bald kam die Beschallung dazu: Unsere Hörner mit der Aufschrift FRANZEN BOCHOLTZ wurden auf Schützenfesten, Radrennen und Umzügen in Limburg ein vertrautes Bild.',
                   'Danach folgten Licht, Video und Strom. Das Material wurde größer, die Veranstaltungen auch. Geblieben ist, dass wir ein Familienunternehmen sind, bei dem Sie direkt mit den Leuten sprechen, die die Arbeit machen.'],
        'waarden': [('Persönlich', 'Sie haben einen Ansprechpartner, von der ersten Frage bis zum letzten Kabel. Jemand, der Ihre Veranstaltung kennt.'),
                    ('Eigenes Material', 'Fast alles, was wir einsetzen, gehört uns und wird von uns gewartet. Das macht uns schnell und zuverlässig.'),
                    ('Erfahrung', 'Über sechzig Jahre Veranstaltungen. Es gibt wenig, was wir noch nicht erlebt haben.')],
        'gebied_kop': 'Einsatzgebiet', 'gebied_p': 'Bocholtz liegt direkt an der Grenze, zehn Minuten von Aachen. Maastricht und Lüttich sind nah. Wir arbeiten in ganz Deutschland, den Niederlanden und Belgien.',
        'contact_seo': ('Kontakt | GTF Franzen', 'Kontaktieren Sie GTF Franzen in Bocholtz bei Aachen für Ton, Beschallung, Licht, Video und Strom für Ihre Veranstaltung.'),
        'contact_h1': 'Kontakt', 'contact_sub': 'Erzählen Sie uns von Ihrer Veranstaltung. Wir antworten gern auf Deutsch.',
        'f': {'naam': 'Name', 'organisatie': 'Organisation', 'mail': 'E-Mail-Adresse', 'datum': 'Datum der Veranstaltung', 'locatie': 'Ort', 'bericht': 'Was brauchen Sie?', 'stuur': 'Senden',
              'note': 'Ihr E-Mail-Programm öffnet sich mit der fertigen Nachricht.'},
    },
    'en': {
        'home_seo': ('GTF Franzen | Sound, public address, lighting and power for events', 'GTF Franzen from Bocholtz provides sound, 100V public address, lighting, video and power for events in the Netherlands, Belgium and Germany. Our own equipment and crew, since the sixties.'),
        'h1': 'We make<br>it heard.',
        'hero_p': 'Sound, public address, lighting, video and power for events in the Netherlands, Belgium and Germany. With our own equipment and our own crew, from Bocholtz.',
        'intro': 'We have been doing this since the sixties. <em>No one else in the region can say that.</em> You get one point of contact, and that is the people who build and run your event.',
        'meters': [('±1960', 'since'), ('300+', 'horn speakers'), ('100+', 'events a year'), ('3', 'countries: NL · BE · DE')],
        'show': 'Sportclub’25 · 100 years · Bocholtz', 'show_r': 'Live production: GTF',
        'mag_kop': 'From our<br>warehouse', 'mag_p': 'Almost everything we use is our own. It is also for hire, with or without a technician. Prices on request.', 'mag_note': 'Selection from our own stock',
        'werk_kop': 'Work', 'nieuws_kop': 'News',
        'roots_label': 'Since the sixties', 'roots_kop': 'Same name.<br>Same approach.',
        'roots_p': ['It started with home-built speakers and a van with horns on the roof. The equipment has grown, the way we work has not.',
                    'You talk to the people who will build your event. No account manager in between, no surprises on the day.'],
        'roots_btn': 'Our story',
        'verhuur_seo': ('Sound, lighting, PA and truss hire | Rental catalogue | GTF Franzen', 'Hire sound, lighting, 100V public address, LED and truss from GTF Franzen’s own stock in Bocholtz, near Aachen and Maastricht. With or without a technician. Prices on request.'),
        'verhuur_h1': 'Rental', 'verhuur_sub': 'A selection from our own stock. For hire with or without a technician, for events in the Netherlands, Belgium and Germany.',
        'verhuur_intro': 'Prices on request. Send us what you need and for which date, and you will quickly get a price and advice on what fits.',
        'verhuur_btn': 'Request a price', 'verhuur_onderwerp': 'Rental enquiry',
        'proj_seo': ('Projects | GTF Franzen', 'A selection of events for which GTF Franzen provided sound, public address, lighting, video and power, such as ZLF, the Amstel Gold Race and the Oud Limburgs Schuttersfeest.'),
        'proj_h1': 'Projects', 'proj_sub': 'A selection of recent work. From public address along a race course to the technical side of an entire festival site.',
        'nieuws_seo': ('News | GTF Franzen', 'News from GTF Franzen in Bocholtz: projects, equipment and more.'),
        'nieuws_h1': 'News', 'nieuws_sub': 'What we are working on.',
        'over_seo': ('About GTF Franzen | From Bocholtz since the sixties', 'GTF Franzen is a family business from Bocholtz that has provided sound, public address and later lighting, video and power for events since the sixties.'),
        'over_h1': 'About us', 'over_sub': 'From Bocholtz since the sixties. Still the same family, still the same approach.',
        'over_lead': 'What started with home-built speakers in Bocholtz is, after more than sixty years, a technical company for events in three countries.',
        'over_p': ['We started around 1960 by hiring out sound equipment. Public address soon followed: our horns reading FRANZEN BOCHOLTZ became a familiar sight at shooting festivals, cycling races and parades across Limburg.',
                   'Lighting, video and power came next. The equipment got bigger, and so did the events. What stayed is that we are a family business, where you speak directly with the people doing the work.'],
        'waarden': [('Personal', 'You have one point of contact, from the first question to the last cable. Someone who knows your event.'),
                    ('Our own equipment', 'Almost everything we use is our own and maintained by us. That makes us quick and reliable.'),
                    ('Experience', 'More than sixty years of events. There is little we have not come across.')],
        'gebied_kop': 'Where we work', 'gebied_p': 'Bocholtz sits right on the border. Aachen is ten minutes away, Maastricht and Liège are close. We work throughout the Netherlands, Belgium and Germany.',
        'contact_seo': ('Contact | GTF Franzen', 'Contact GTF Franzen in Bocholtz for sound, public address, lighting, video and power for your event.'),
        'contact_h1': 'Contact', 'contact_sub': 'Tell us about your event. We are happy to reply in English.',
        'f': {'naam': 'Name', 'organisatie': 'Organisation', 'mail': 'Email address', 'datum': 'Date of the event', 'locatie': 'Location', 'bericht': 'What do you need?', 'stuur': 'Send',
              'note': 'Your email app opens with the message ready to send.'},
    },
}

# ---------------------------------------------------------------- Hulpfuncties
def rel(lang):
    return '' if lang == 'nl' else '../'


def url(key, lang, frm):
    """Link van een pagina in taal `frm` naar pagina `key` in taal `lang`."""
    s = SLUG[key][lang]
    if frm == lang:
        return s
    return rel(frm) + PREFIX[lang] + s


def img(name, lang, alt='', cls='', eager=False):
    c = f' class="{cls}"' if cls else ''
    load = ' fetchpriority="high"' if eager else ' loading="lazy"'
    return f'<img src="{rel(lang)}assets/foto/{name}" alt="{alt}"{c}{load} decoding="async">'


def org(lang):
    o = {
        '@context': 'https://schema.org', '@type': 'LocalBusiness', '@id': BASE + '#gtf',
        'name': 'GTF Franzen', 'alternateName': 'Franzen Bocholtz', 'url': BASE, 'logo': BASE + 'assets/foto/logo.png',
        'image': BASE + 'assets/foto/og.jpg', 'slogan': 'Sound - Light - Vision',
        'description': TXT[lang]['home_seo'][1],
        'areaServed': [{'@type': 'Country', 'name': n} for n in ('Nederland', 'België', 'Deutschland')],
        'address': {'@type': 'PostalAddress', 'streetAddress': STRAAT, 'postalCode': POSTCODE,
                    'addressLocality': PLAATS, 'addressRegion': 'Limburg', 'addressCountry': 'NL'},
        'knowsAbout': ['Geluidstechniek', 'Lichttechniek', '100V-omroep', 'Omroepinstallaties', 'ELA-Anlagen', 'Public address systems',
                       'LED-wanden', 'Stroomverdeling', 'Eventtechniek'],
        'makesOffer': [{'@type': 'Offer', 'itemOffered': {'@type': 'Service', 'name': DIENST[k][lang]['titel'],
                                                          '@id': BASE + PREFIX[lang] + SLUG[k][lang] + '#dienst'}} for k in DIENSTEN],
    }
    if MAIL:
        o['email'] = MAIL
    if TEL:
        o['telephone'] = TEL
    return o


def crumbs_ld(items):
    return {'@context': 'https://schema.org', '@type': 'BreadcrumbList',
            'itemListElement': [{'@type': 'ListItem', 'position': i + 1, 'name': n, 'item': BASE + u} for i, (n, u) in enumerate(items)]}


def faq_ld(faq):
    return {'@context': 'https://schema.org', '@type': 'FAQPage',
            'mainEntity': [{'@type': 'Question', 'name': q, 'acceptedAnswer': {'@type': 'Answer', 'text': a}} for q, a in faq]}


def strip_tags(s):
    return s.replace('<br>', ' ').replace('<em>', '').replace('</em>', '').replace('&amp;', '&')


# ---------------------------------------------------------------- Kop en voet
def head(lang, key, title, desc, alts, image='og.jpg', ld=None):
    path = PREFIX[lang] + (alts[lang] if alts else '')
    canon = BASE + (path if not path.endswith('index.html') else path[:-10])
    links = ''
    if alts:
        for l in LANGS:
            p = PREFIX[l] + alts[l]
            links += f'\n<link rel="alternate" hreflang="{l}" href="{BASE}{p[:-10] if p.endswith("index.html") else p}">'
        p = alts['nl']
        links += f'\n<link rel="alternate" hreflang="x-default" href="{BASE}{p[:-10] if p.endswith("index.html") else p}">'
    lds = ''.join(f'\n<script type="application/ld+json">{json.dumps(x, ensure_ascii=False)}</script>' for x in (ld or []))
    r = rel(lang)
    return f'''<!DOCTYPE html>
<html lang="{lang}">
<head>
<meta charset="utf-8">
<meta name="viewport" content="width=device-width, initial-scale=1">
<title>{title}</title>
<meta name="description" content="{escape(desc)}">
<link rel="canonical" href="{canon}">{links}
<meta name="theme-color" content="#060608">
<meta property="og:type" content="website">
<meta property="og:site_name" content="GTF Franzen">
<meta property="og:locale" content="{LOCALE[lang]}">
<meta property="og:title" content="{escape(title)}">
<meta property="og:description" content="{escape(desc)}">
<meta property="og:url" content="{canon}">
<meta property="og:image" content="{BASE}assets/foto/{image}">
<meta name="twitter:card" content="summary_large_image">
<link rel="icon" type="image/png" sizes="48x48" href="{r}assets/foto/icon-48.png">
<link rel="apple-touch-icon" href="{r}assets/foto/icon-180.png">
<link rel="preconnect" href="https://fonts.googleapis.com">
<link rel="preconnect" href="https://fonts.gstatic.com" crossorigin>
<link rel="stylesheet" href="{FONTS}">
<link rel="stylesheet" href="{r}assets/css/site.css?v={ver('assets/css/site.css')}">{lds}
</head>
<body class="no-js">
'''


def header(lang, key, alts):
    u = UI[lang]
    nav = ''.join(f'<a href="{url(k, lang, lang)}"{" aria-current=\"page\"" if k == key else ""}>{u["nav"][k]}</a>'
                  for k in ('geluid', 'omroep', 'licht', 'stroom', 'verhuur', 'projecten', 'nieuws', 'over'))
    langs = ''
    for l in LANGS:
        if l == lang:
            langs += f'<b>{l.upper()}</b>'
        elif alts:
            langs += f'<a href="{rel(lang) + PREFIX[l] + alts[l]}" hreflang="{l}" lang="{l}" title="{TAAL[l]}">{l.upper()}</a>'
    return f'''<a class="skip" href="#main">{u["skip"]}</a>
<header class="top pad">
  <a class="logo" href="{url('home', lang, lang)}"><img src="{rel(lang)}assets/foto/logo.png" alt="GTF Franzen · Franzen Bocholtz · Sound - Light - Vision" width="1600" height="457"></a>
  <nav id="nav" aria-label="{u["menu"]}">{nav}<a class="mob-only" href="{url('contact', lang, lang)}">{u["contact"]}</a></nav>
  <div class="r"><span class="lang m">{langs}</span><a class="btn" href="{url('contact', lang, lang)}">{u["contact"]}</a>
  <button class="burger" aria-label="{u["menu"]}" aria-expanded="false" aria-controls="nav"><span></span><span></span></button></div>
</header>
<main id="main">
'''


def cta(lang, bg=None, subject=None):
    u = UI[lang]
    sub = quote(subject or u['onderwerp'])
    return f'''<section class="cta pad" id="contact">
  {img(bg, lang) if bg else ''}
  <div class="t rv">
    <span class="m red">{u["contact"]}</span>
    <h2 class="x">{u["cta_kop"]}</h2>
    <p>{u["cta_txt"]}</p>
    <a class="mail" href="mailto:{MAIL}?subject={sub}">{MAIL}</a>
  </div>
</section>'''


def footer(lang, alts):
    u = UI[lang]
    d = ''.join(f'<a href="{url(k, lang, lang)}">{u["nav"][k]}</a>' for k in DIENSTEN)
    m = ''.join(f'<a href="{url(k, lang, lang)}">{u["nav"][k]}</a>' for k in ('verhuur', 'projecten', 'nieuws', 'over', 'contact') if k != 'contact') + f'<a href="{url("contact", lang, lang)}">{u["contact"]}</a>'
    t = ''.join(f'<a href="{rel(lang) + PREFIX[l] + (alts[l] if alts else "index.html")}" hreflang="{l}" lang="{l}">{TAAL[l]}</a>' for l in LANGS)
    tel = f'<br><a href="tel:{TEL}">{TEL_TXT or TEL}</a>' if TEL else ''
    return f'''</main>
<footer class="pad">
  <div class="cols">
    <div><img src="{rel(lang)}assets/foto/logo.png" alt="GTF Franzen" width="1600" height="457" loading="lazy"><p style="margin:0;max-width:360px">{u["foot"]}</p></div>
    <div><span class="m">{u["diensten"]}</span>{d}</div>
    <div><span class="m">{u["meer"]}</span>{m}</div>
    <div><span class="m">{u["adres"]}</span>GTF Franzen<br>{STRAAT}<br>{POSTCODE} {PLAATS}<br><a href="mailto:{MAIL}">{MAIL}</a>{tel}
      <span class="m" style="margin-top:26px">{u["taal"]}</span>{t}</div>
  </div>
  <div class="end m"><span>&copy; <span data-year>2026</span> GTF Franzen · Sound - Light - Vision</span><a href="{rel(lang)}privacy.html" hreflang="nl">{u["privacy"]}</a></div>
</footer>
<script src="{rel(lang)}assets/js/site.js?v={ver('assets/js/site.js')}" defer></script>
</body>
</html>
'''


BUILT = []      # (pad, alternates)


def write(lang, key, alts, title, desc, body, image='og.jpg', ld=None):
    path = PREFIX[lang] + alts[lang]
    html = head(lang, key, title, desc, alts, image, ld) + header(lang, key, alts) + body + '\n' + footer(lang, alts)
    out = ROOT / path
    out.parent.mkdir(parents=True, exist_ok=True)
    out.write_text(html)
    BUILT.append((path, alts))
    return path


def phero(lang, imgname, crumb, h1, sub, btns='', label='', short=False, alt=''):
    return f'''<section class="phero{' short' if short else ''}">
  {img(imgname, lang, alt, eager=True)}
  <div class="t pad">
    <p class="crumb m"><a href="{url('home', lang, lang)}">GTF Franzen</a> / {crumb}{f' <span>{label}</span>' if label else ''}</p>
    <h1 class="x">{h1}</h1>
    {f'<p class="sub">{sub}</p>' if sub else ''}
    {f'<div class="btns">{btns}</div>' if btns else ''}
  </div>
</section>'''


def meters(lang):
    bars = ['ggggg yyr', 'ggggg yy.', 'ggggg y..', 'gggg ....']
    out = ''
    for (b, s), pat in zip(TXT[lang]['meters'], bars):
        us = ''.join(f'<u class="{ {"g": "g", "y": "y", "r": "r"}[c]}"></u>' if c in 'gyr' else '<u></u>' for c in pat.replace(' ', ''))
        out += f'<div><b>{b}</b><span>{s}</span><i aria-hidden="true">{us}</i></div>'
    return f'<div class="meters rv">{out}</div>'


def loc(v, lang):
    return v[lang] if isinstance(v, dict) else v


def jobs(lang):
    rows = ''
    for p in PROJECTEN:
        ph = img(p['img'], lang, p['naam']) if p['img'] else f'<img class="lg" src="{rel(lang)}assets/foto/logo.png" alt="" loading="lazy">'
        rows += f'<div class="job"><div class="ph">{ph}</div><h3>{p["naam"]}</h3><p>{p[lang]}</p><span class="m">{p["jaar"]}</span></div>'
    return f'<div class="jobs rv">{rows}</div>'


def news_cards(lang, n=3):
    out = ''
    for a in NIEUWS[:n]:
        t, k, _ = a[lang]
        out += f'''<a class="post rv" href="{a["slug"][lang]}"><div class="ph">{img(a["img"], lang, t)}</div><span class="m">{a["datum"][lang]}</span><h3>{t}</h3><p>{k}</p></a>'''
    return f'<div class="news">{out}</div>'


# ---------------------------------------------------------------- Home
def home(lang):
    u, t = UI[lang], TXT[lang]
    slides = [('sc-rood.jpg', 'Podium met rode lichtbundels boven een vol publiek'), ('faders.jpg', 'Faders van een mengtafel in rood en blauw licht'),
              ('linearray.jpg', 'Gevlogen line array in rood licht'), ('sc-03.jpg', 'Podium met paarse en groene lichtbundels')]
    sl = ''.join(f'<div class="sl{" on" if i == 0 else ""}">{img(f, lang, a if i == 0 else "", eager=(i == 0))}</div>' for i, (f, a) in enumerate(slides))
    dots = ''.join(f'<span{" class=\"on\"" if i == 0 else ""}></span>' for i in range(len(slides)))
    chans = ''
    for k in DIENSTEN:
        d, dl = DIENST[k], DIENST[k][lang]
        gear = d.get('gear_t', {}).get(lang, d['gear'])
        tags = ''.join(f'<li>{g.replace("&", "&amp;") if "&amp;" not in g else g}</li>' for g in gear)
        chans += f'''<a class="chan" href="{url(k, lang, lang)}">
    {img(d["home"], lang)}
    <div class="in pad">
      <div class="hd m"><span class="red">CH {d["nr"]}</span><span>{dl["titel"]}</span></div>
      <div>
        <h2 class="x">{dl["titel"].replace(" en ", "<br>en ").replace(" und ", "<br>und ").replace(" and ", "<br>and ") if len(dl["titel"]) > 12 else dl["titel"]}</h2>
        <p>{dl["kort"]}{(' ' + MATRIX_TXT[lang][1]) if d.get('matrix') else ''}</p>
        <ul class="tags m">{tags}</ul>
        <span class="go">{u["lees"]} →</span>
      </div>
    </div>
    <div class="inset">{img(d["inset"][0], lang)}<div class="m">{d["inset"][1]}</div></div>
  </a>
'''
    gear = ''.join(f'<a href="{url("verhuur", lang, lang)}"><b>{n}</b><strong>{loc(naam, lang)}</strong><span class="m">{loc(cat, lang)}</span></a>' for n, naam, cat in UITGELICHT)
    body = f'''<section class="hero">
  {sl}
  <div class="t pad">
    <h1 class="x">{t["h1"]}</h1>
    <div class="row">
      <div><p>{t["hero_p"]}</p><div class="dots" aria-hidden="true">{dots}</div></div>
      <div class="btns"><a class="btn" href="{url('contact', lang, lang)}">{u["cta"]}</a><a class="btn ghost" href="#werk">{u["werk"]}</a></div>
    </div>
  </div>
</section>

<section class="intro pad">
  <p class="big rv">{t["intro"]}</p>
  {meters(lang)}
</section>

<section class="show">
  {img('sc-beams.jpg', lang, 'Lichtshow boven het publiek')}
  <div class="pad lab"><span class="m"><span class="red">{u["live"]}</span> &nbsp;{t["show"]}</span><span class="m">{t["show_r"]} · {u["credit"]}</span></div>
</section>

<section class="chs" id="diensten" aria-label="{u["diensten"]}">
  {chans}</section>

<section class="sec pad" id="magazijn">
  <div class="shd rv"><h2 class="x h2">{t["mag_kop"]}</h2><p>{t["mag_p"]}</p></div>
  <div class="gear rv">{gear}</div>
  <div class="more rv"><span class="m" style="color:var(--dim)">{t["mag_note"]}</span><a class="btn" href="{url('verhuur', lang, lang)}">{u["naar_verhuur"]}</a></div>
</section>

<div class="strip" aria-hidden="true">{img('sc-strobe.jpg', lang)}{img('grill.jpg', lang)}{img('sc-groen.jpg', lang)}</div>

<section class="sec pad" id="werk">
  <div class="shd rv"><h2 class="x h2">{t["werk_kop"]}</h2><a class="btn ghost" href="{url('projecten', lang, lang)}">{u["nav"]["projecten"]}</a></div>
  {jobs(lang)}
</section>

<section class="roots">
  <div class="img">{img('bus.jpg', lang, 'De oude GTF-bus met hoorns op het dak')}</div>
  <div class="tx rv">
    <span class="m red">{t["roots_label"]}</span>
    <h2 class="x">{t["roots_kop"]}</h2>
    {''.join(f'<p>{p}</p>' for p in t["roots_p"])}
    <div class="btns"><a class="btn ghost" href="{url('over', lang, lang)}">{t["roots_btn"]}</a></div>
  </div>
</section>

<section class="sec pad">
  <div class="shd rv"><h2 class="x h2">{t["nieuws_kop"]}</h2><a class="btn ghost" href="{url('nieuws', lang, lang)}">{u["terug"]}</a></div>
  {news_cards(lang)}
</section>

{cta(lang, bg='sc-crowd.jpg')}'''
    return write(lang, 'home', SLUG['home'], t['home_seo'][0], t['home_seo'][1], body, ld=[org(lang)])


# ---------------------------------------------------------------- Dienstpagina
def dienst(lang, k):
    u, d, dl = UI[lang], DIENST[k], DIENST[k][lang]
    gear = d.get('gear_t', {}).get(lang, d['gear'])
    tags = ''.join(f'<li>{g if "&amp;" in g else g.replace("&", "&amp;")}</li>' for g in gear)
    faq = ''.join(f'<details><summary>{q}</summary><p>{a}</p></details>' for q, a in dl.get('faq', []))
    faq_sec = f'''<section class="sec pad alt faq">
  <div class="two">
    <h2 class="x h2 rv" style="font-size:clamp(26px,4.4vw,72px)">{u["faq"]}</h2>
    <div class="rv">{faq}</div>
  </div>
</section>''' if faq else ''
    mx = MATRIX_TXT[lang]
    matrix = f'''<section class="sec pad partner">
  <div class="two rv">
    <div><span class="boxhd m">Partner</span><h2 class="x h2" style="font-size:clamp(28px,4vw,64px)">{mx[0]}</h2></div>
    <div class="txt"><p class="lead">{mx[1]}</p><a class="btn ghost" href="{MATRIX}" rel="noopener">{mx[2]} ↗</a></div>
  </div>
</section>''' if d.get('matrix') else ''
    andere = ''.join(f'<a class="btn ghost" href="{url(o, lang, lang)}">{u["nav"][o]}</a>' for o in DIENSTEN if o != k)
    credit = f'<p class="m" style="color:var(--dim);margin-top:10px">{u["credit"]}</p>' if d.get('credit') else ''
    body = f'''{phero(lang, d["hero"], dl["titel"], dl["titel"].replace(" en ", "<br>en ").replace(" und ", "<br>und ").replace(" and ", "<br>and "), dl["sub"],
                f'<a class="btn" href="{url("contact", lang, lang)}">{u["cta"]}</a><a class="btn ghost" href="{url("verhuur", lang, lang)}">{u["nav"]["verhuur"]}</a>', label=f'CH {d["nr"]}', alt=dl["titel"])}

<section class="sec pad" id="dienst">
  <div class="two">
    <div class="txt rv"><p class="lead">{dl["lead"]}</p>{''.join(f'<p>{p}</p>' for p in dl["tekst"])}<ul class="tags m" style="margin-top:30px">{tags}</ul></div>
    <div class="rv"><span class="boxhd m">{u["krijgt"]}</span><ul class="list">{''.join(f'<li>{x}</li>' for x in dl["krijg"])}</ul></div>
  </div>
</section>

<div class="strip{' n2' if len(d["strip"]) == 2 else ''}" aria-hidden="true">{''.join(img(f, lang) for f in d["strip"])}</div>
<div class="pad">{credit}</div>

{matrix}
{faq_sec}

<section class="sec tight pad">
  <div class="btns rv">{andere}</div>
</section>

{cta(lang, subject=dl["titel"])}'''
    alts = SLUG[k]
    ld = [org(lang)] + ([faq_ld(dl['faq'])] if dl.get('faq') else []) + [
          {'@context': 'https://schema.org', '@type': 'Service', '@id': BASE + PREFIX[lang] + alts[lang] + '#dienst', 'name': dl['titel'],
           'serviceType': dl['titel'], 'description': dl['seo'][1], 'provider': {'@id': BASE + '#gtf'},
           'areaServed': org(lang)['areaServed'], 'url': BASE + PREFIX[lang] + alts[lang], 'inLanguage': lang},
          crumbs_ld([('GTF Franzen', PREFIX[lang]), (dl['titel'], PREFIX[lang] + alts[lang])])]
    return write(lang, k, alts, dl['seo'][0], dl['seo'][1], body, image=d['hero'], ld=ld)


# ---------------------------------------------------------------- Verhuur
def verhuur(lang):
    u, t, c = UI[lang], TXT[lang], CAT_UI[lang]
    sub = quote(t['verhuur_onderwerp'])
    side = ''.join(f'<a href="#{cid}"><span>{loc(naam, lang)}</span><span class="m">{len(items)}</span></a>' for cid, _, naam, items in CATALOGUS)
    cats = ''
    for i, (cid, im, naam, items) in enumerate(CATALOGUS):
        rows = ''.join(f'''<li><div><b>{n}</b><span>{loc(o, lang)}</span></div><button type="button" class="add" data-item="{escape(strip_tags(n))}" aria-pressed="false"><span class="on">{c["op"]}</span><span class="off">+ {c["voeg"]}</span></button></li>''' for n, o in items)
        cats += f'''<section class="ccat rv" id="{cid}">
    <header>{img(im, lang)}<div><span class="m red">{i + 1:02d} · {len(items)} {c["items"]}</span><h2 class="x">{loc(naam, lang)}</h2></div></header>
    <ul class="crows">{rows}</ul>
  </section>'''
    body = f'''{phero(lang, 'faders2.jpg', t["verhuur_h1"], t["verhuur_h1"], t["verhuur_sub"], label=u["prijs"], short=True)}

<section class="sec pad catalog">
  <div class="cgrid">
    <aside class="cside">
      <nav aria-label="{t["verhuur_h1"]}">{side}</nav>
      <div class="cinfo"><p>{t["verhuur_intro"]}</p><p class="m">{c["hoe"]}</p></div>
    </aside>
    <div class="cmain">{cats}</div>
  </div>
</section>

<div class="cbar" data-mail="{MAIL}" data-subject="{t["verhuur_onderwerp"]}" data-intro="{escape(c["mailintro"])}">
  <span><b data-count>0</b> <span data-label-one="{c["een"]}" data-label-more="{c["meer"]}">{c["meer"]}</span></span>
  <button type="button" class="btn" data-send>{t["verhuur_btn"]}</button>
</div>

{cta(lang, subject=t["verhuur_onderwerp"])}'''
    alts = SLUG['verhuur']
    ld = [org(lang), crumbs_ld([('GTF Franzen', PREFIX[lang]), (t['verhuur_h1'], PREFIX[lang] + alts[lang])])]
    return write(lang, 'verhuur', alts, t['verhuur_seo'][0], t['verhuur_seo'][1], body, image='faders2.jpg', ld=ld)


# ---------------------------------------------------------------- Projecten
def projecten(lang):
    u, t = UI[lang], TXT[lang]
    body = f'''{phero(lang, 'sc-02.jpg', t["proj_h1"], t["proj_h1"], t["proj_sub"], short=True)}

<section class="sec pad">
  {jobs(lang)}
</section>

<section class="show">
  {img('sc-07.jpg', lang, 'Podium van Sportclub’25 in blauw licht')}
  <div class="pad lab"><span class="m"><span class="red">{u["live"]}</span> &nbsp;{TXT[lang]["show"]}</span><span class="m">{u["credit"]}</span></div>
</section>

{cta(lang)}'''
    alts = SLUG['projecten']
    return write(lang, 'projecten', alts, t['proj_seo'][0], t['proj_seo'][1], body, image='sc-02.jpg',
                 ld=[org(lang), crumbs_ld([('GTF Franzen', PREFIX[lang]), (t['proj_h1'], PREFIX[lang] + alts[lang])])])


# ---------------------------------------------------------------- Nieuws
def nieuws(lang):
    t = TXT[lang]
    body = f'''{phero(lang, 'faders3.jpg', t["nieuws_h1"], t["nieuws_h1"], t["nieuws_sub"], short=True)}

<section class="sec pad">
  {news_cards(lang, n=len(NIEUWS))}
</section>

{cta(lang)}'''
    alts = SLUG['nieuws']
    return write(lang, 'nieuws', alts, t['nieuws_seo'][0], t['nieuws_seo'][1], body,
                 ld=[org(lang), crumbs_ld([('GTF Franzen', PREFIX[lang]), (t['nieuws_h1'], PREFIX[lang] + alts[lang])])])


def artikel(lang, a):
    u, t = UI[lang], TXT[lang]
    titel, kort, alinea = a[lang]
    credit = f'<p class="m" style="color:var(--dim)">{u["credit"]}</p>' if a.get('credit') else ''
    body = f'''{phero(lang, a["img"], f'<a href="{url("nieuws", lang, lang)}">{t["nieuws_h1"]}</a>', titel, kort, label=a["datum"][lang], short=True)}

<section class="sec pad">
  <div class="article rv">
    {''.join(f'<p>{p}</p>' for p in alinea)}
    <div class="btns" style="margin-top:40px"><a class="btn ghost" href="{url('nieuws', lang, lang)}">← {u["terug"]}</a><a class="btn" href="{url('contact', lang, lang)}">{u["cta"]}</a></div>
  </div>
  {f'<div class="gallery rv">{"".join(img(f, lang) for f in a["gallery"])}</div>' if a["gallery"] else ''}
  {credit}
</section>

{cta(lang)}'''
    alts = a['slug']
    ld = [org(lang), {'@context': 'https://schema.org', '@type': 'NewsArticle', 'headline': titel, 'description': kort, 'datePublished': a['iso'],
                      'image': BASE + 'assets/foto/' + a['img'], 'inLanguage': lang, 'publisher': {'@id': BASE + '#gtf'},
                      'mainEntityOfPage': BASE + PREFIX[lang] + alts[lang]},
          crumbs_ld([('GTF Franzen', PREFIX[lang]), (t['nieuws_h1'], PREFIX[lang] + SLUG['nieuws'][lang]), (titel, PREFIX[lang] + alts[lang])])]
    return write(lang, 'nieuws', alts, f'{titel} | GTF Franzen', kort, body, image=a['img'], ld=ld)


# ---------------------------------------------------------------- Over ons
def over(lang):
    u, t = UI[lang], TXT[lang]
    waarden = ''.join(f'<div class="rv"><b>{i + 1:02d}</b><h3>{h}</h3><p>{p}</p></div>' for i, (h, p) in enumerate(t['waarden']))
    body = f'''{phero(lang, 'bus.jpg', t["over_h1"], t["over_h1"], t["over_sub"], label='±1960', alt='De oude GTF-bus met hoorns op het dak')}

<section class="sec pad">
  <div class="two">
    <p class="state rv" style="font-size:clamp(26px,2.8vw,44px)">{t["over_lead"]}</p>
    <div class="txt rv">{''.join(f'<p>{p}</p>' for p in t["over_p"])}</div>
  </div>
  {meters(lang)}
</section>

<div class="strip" aria-hidden="true">{img('console-lijn.jpg', lang)}{img('sc-12.jpg', lang)}{img('console-knoppen.jpg', lang)}</div>

<section class="sec pad">
  <div class="steps">{waarden}</div>
</section>

<section class="sec pad alt">
  <div class="two">
    <h2 class="x h2 rv" style="font-size:clamp(26px,4.4vw,72px)">{t["gebied_kop"]}</h2>
    <div class="txt rv"><p class="lead">{t["gebied_p"]}</p><p class="m" style="color:var(--mut)">{u["werkgebied"]}</p></div>
  </div>
</section>

{cta(lang)}'''
    alts = SLUG['over']
    return write(lang, 'over', alts, t['over_seo'][0], t['over_seo'][1], body, image='bus.jpg',
                 ld=[org(lang), crumbs_ld([('GTF Franzen', PREFIX[lang]), (t['over_h1'], PREFIX[lang] + alts[lang])])])


# ---------------------------------------------------------------- Contact
def contact(lang):
    u, t = UI[lang], TXT[lang]
    f = t['f']
    tel = f'<li><span class="m">{u["tel"]}</span><a href="tel:{TEL}">{TEL_TXT or TEL}</a></li>' if TEL else ''
    body = f'''{phero(lang, 'sc-dj.jpg', t["contact_h1"], t["contact_h1"], t["contact_sub"], short=True)}

<section class="sec pad">
  <div class="two">
    <form class="f rv" data-mail="{MAIL}" data-subject="{u["onderwerp"]}">
      <label>{f["naam"]}<input name="naam" autocomplete="name" required></label>
      <label>{f["organisatie"]}<input name="organisatie" autocomplete="organization"></label>
      <label>{f["datum"]}<input name="datum"></label>
      <label>{f["locatie"]}<input name="locatie"></label>
      <label class="full">{f["bericht"]}<textarea name="bericht" required></textarea></label>
      <div class="full"><button class="btn" type="submit">{f["stuur"]}</button></div>
      <p class="note full">{f["note"]}</p>
    </form>
    <ul class="info rv">
      <li><span class="m">{u["mail"]}</span><a href="mailto:{MAIL}">{MAIL}</a></li>
      {tel}
      <li><span class="m">{u["adres"]}</span>GTF Franzen<br>{STRAAT}<br>{POSTCODE} {PLAATS}</li>
      <li><span class="m">{TXT[lang]["gebied_kop"]}</span>{u["werkgebied"]}</li>
    </ul>
  </div>
</section>'''
    alts = SLUG['contact']
    return write(lang, 'contact', alts, t['contact_seo'][0], t['contact_seo'][1], body,
                 ld=[org(lang), crumbs_ld([('GTF Franzen', PREFIX[lang]), (t['contact_h1'], PREFIX[lang] + alts[lang])])])


# ---------------------------------------------------------------- Privacy en 404 (alleen NL)
def privacy():
    body = f'''<section class="sec pad" style="padding-top:180px">
  <p class="crumb m"><a href="index.html">GTF Franzen</a> / Privacy</p>
  <h1 class="x h2" style="margin:18px 0 50px">Privacy&shy;verklaring</h1>
  <div class="article">
    <p>GTF Franzen gaat zorgvuldig om met uw gegevens. Als u contact opneemt of een offerte aanvraagt, gebruiken we uw naam, contactgegevens en de informatie over uw evenement alleen om uw aanvraag te beantwoorden en uw evenement voor te bereiden.</p>
    <p>We delen uw gegevens niet met derden, behalve als dat nodig is voor de uitvoering van uw evenement en altijd in overleg. We bewaren gegevens niet langer dan nodig.</p>
    <p>Deze website gebruikt geen tracking-cookies. Lettertypen worden geladen via Google Fonts.</p>
    <p>Wilt u weten welke gegevens we van u hebben, of wilt u ze laten verwijderen? Neem dan <a href="contact.html">contact</a> met ons op.</p>
  </div>
</section>'''
    alts = {'nl': 'privacy.html', 'de': 'privacy.html', 'en': 'privacy.html'}
    html = head('nl', 'privacy', 'Privacy | GTF Franzen', 'Privacyverklaring van GTF Franzen.', None) + header('nl', 'privacy', None) + body + footer('nl', None)
    (ROOT / 'privacy.html').write_text(html.replace('<link rel="canonical" href="' + BASE + '">', f'<link rel="canonical" href="{BASE}privacy.html">'))
    BUILT.append(('privacy.html', None))


def notfound():
    body = '''<section class="phero">
  <img src="/gtf-franzen-site/assets/foto/takels.jpg" alt="">
  <div class="t pad">
    <p class="crumb m">404</p>
    <h1 class="x">Deze pagina<br>bestaat niet.</h1>
    <p class="sub">Seite nicht gefunden · Page not found</p>
    <div class="btns"><a class="btn" href="/gtf-franzen-site/">GTF Franzen</a><a class="btn ghost" href="/gtf-franzen-site/de/">Deutsch</a><a class="btn ghost" href="/gtf-franzen-site/en/">English</a></div>
  </div>
</section>'''
    html = head('nl', '404', 'Pagina niet gevonden | GTF Franzen', 'Deze pagina bestaat niet.', None) + header('nl', '404', None) + body + footer('nl', None)
    # 404 wordt vanaf elk pad geserveerd: absolute paden
    html = html.replace('href="assets/', 'href="/gtf-franzen-site/assets/').replace('src="assets/', 'src="/gtf-franzen-site/assets/')
    for k in SLUG:
        html = html.replace(f'href="{SLUG[k]["nl"]}"', f'href="/gtf-franzen-site/{SLUG[k]["nl"]}"')
    html = html.replace('href="privacy.html"', 'href="/gtf-franzen-site/privacy.html"').replace('href="de/', 'href="/gtf-franzen-site/de/').replace('href="en/', 'href="/gtf-franzen-site/en/')
    html = html.replace('<meta name="description"', '<meta name="robots" content="noindex">\n<meta name="description"')
    (ROOT / '404.html').write_text(html)


# ---------------------------------------------------------------- Oude adressen doorsturen
REDIRECTS = {
    'diensten.html': 'index.html#diensten', 'licht.html': 'licht-en-video.html', 'stroom-aggregaten.html': 'stroom-en-infra.html',
    'eventproductie.html': 'index.html#diensten', 'evenementen.html': 'projecten.html', 'festival.html': 'projecten.html',
    'bedrijfsevent.html': 'index.html', 'bruiloft-feest.html': 'index.html', 'dorpsfeest-carnaval.html': 'projecten.html',
    'vereniging-jubileum.html': 'projecten.html', 'schuttersfeest-omroep.html': 'omroep-100v.html', 'werkgebied.html': 'over-ons.html',
    'werkwijze.html': 'over-ons.html', 'over.html': 'over-ons.html', 'project-amstel-gold-race.html': 'projecten.html',
    'project-sportclub-jubileum.html': 'projecten.html', 'project-woeesj-stock.html': 'projecten.html',
    'de-100v-ela-anlage-mieten.html': 'de/100v-ela-anlage-mieten.html', 'en-100v-pa-system-hire.html': 'en/100v-pa-system-hire.html',
}


def redirects():
    for old, new in REDIRECTS.items():
        (ROOT / old).write_text(f'''<!DOCTYPE html>
<html><head><meta charset="utf-8"><title>GTF Franzen</title>
<link rel="canonical" href="{BASE}{new.split('#')[0].replace('index.html', '')}">
<meta name="robots" content="noindex">
<meta http-equiv="refresh" content="0; url={new}">
</head><body><a href="{new}">GTF Franzen</a></body></html>
''')


# ---------------------------------------------------------------- Sitemap
def sitemap():
    def loc_(p):
        return BASE + (p[:-10] if p.endswith('index.html') else p)
    urls = ''
    for p, alts in BUILT:
        x = ''
        if alts:
            x = ''.join(f'<xhtml:link rel="alternate" hreflang="{l}" href="{loc_(PREFIX[l] + alts[l])}"/>' for l in LANGS)
            x += f'<xhtml:link rel="alternate" hreflang="x-default" href="{loc_(alts["nl"])}"/>'
        urls += f'<url><loc>{loc_(p)}</loc>{x}</url>\n'
    (ROOT / 'sitemap.xml').write_text('<?xml version="1.0" encoding="UTF-8"?>\n<urlset xmlns="http://www.sitemaps.org/schemas/sitemap/0.9" '
                                      f'xmlns:xhtml="http://www.w3.org/1999/xhtml">\n{urls}</urlset>\n')
    (ROOT / 'robots.txt').write_text(f'User-agent: *\nAllow: /\n\nSitemap: {BASE}sitemap.xml\n')


if __name__ == '__main__':
    for d in ('de', 'en'):
        shutil.rmtree(ROOT / d, ignore_errors=True)
    for lang in LANGS:
        home(lang)
        for k in DIENSTEN:
            dienst(lang, k)
        verhuur(lang)
        projecten(lang)
        nieuws(lang)
        for a in NIEUWS:
            artikel(lang, a)
        over(lang)
        contact(lang)
    privacy()
    notfound()
    redirects()
    sitemap()
    print(f'Gebouwd: {len(BUILT)} pagina\'s, {len(REDIRECTS)} doorverwijzingen')
