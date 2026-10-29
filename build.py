#!/usr/bin/env python3
"""Bouwt de HTML-pagina's van de GTF Franzen site uit gedeelde onderdelen. Draai: python3 build.py"""
import hashlib
import json
from pathlib import Path

ROOT = Path(__file__).parent

# ---------------------------------------------------------------- Gegevens
# Nog aan te vullen door de familie. Lege waarden worden niet getoond op de site.
MAIL = 'info@franzenbocholtz.nl'  # algemeen adres, wordt doorgestuurd
# Web3Forms access key (web3forms.com, aangemaakt met het algemene adres). Leeg = formulier opent een mail aan MAIL.
FORM_KEY = ''
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

NAV = [('diensten.html', 'Diensten'), ('evenementen.html', 'Evenementen'), ('projecten.html', 'Projecten'), ('over.html', 'Ons verhaal')]
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
     'tekst': 'Licht bepaalt hoe je event voelt, en hoe het eruitziet op elke foto en video. Samen met MATRIX E.I.L., dat draait op grote festivals en clubshows, verzorgen we lichtontwerp, voorprogrammering, visuals en live bediening. Zo krijgt ook een dorpsfeest of jubileum de kennis van de grote podia.',
     'punten': ['Lichtontwerp en previsualisatie', 'Programmering en live operation', 'LED, effecten, CO2 en confetti', 'Sfeerverlichting voor zalen en tenten']},
    {'slug': 'omroep', 'nr': '03', 'titel': 'Omroep & 100V', 'img': 'omroep.jpg',
     'kort': 'Waar we al generaties bekend om staan.',
     'tekst': 'Omroepinstallaties en 100V-systemen zitten in ons DNA. Op het Oud Limburgs Schuttersfeest (OLS) hingen meer dan 140 van onze hoorns en reden diverse jurywagens met onze omroep. Langs de Amstel Gold Race hangen ze langs het parcours. Over een groot terrein zorgen we dat iedereen hoort wat er gezegd wordt, betrouwbaar en goed verstaanbaar.',
     'punten': ['Tijdelijke en vaste omroepinstallaties', '100V-systemen over grote afstanden', 'Jurywagens en mobiele omroep', 'Schuttersfeesten, wielerkoersen en evenemententerreinen']},
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
    {'id': 'dorpsfeest', 'label': 'Dorpsfeest & carnaval', 'img': 'proj/woeesj-stock/01.jpg',
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
    {'id': 'gemeente', 'label': 'Omroep & grote terreinen', 'img': 'ols.jpg',
     'kop': 'Iedereen hoort het. Overal op het terrein.',
     'tekst': 'Schuttersfeesten, wielerklassiekers, herdenkingen en markten. Op het OLS, het Oud Limburgs Schuttersfeest, hingen meer dan 140 hoorns op 100V en reden er diverse jurywagens met onze omroep. Langs het parcours van de Amstel Gold Race hoort het publiek dankzij ons wat er in de koers gebeurt.',
     'regelen': ['Omroep op 100V over grote afstanden', 'Honderden hoorns op één terrein', 'Jurywagens en mobiele omroep', 'Spraak bij ceremonies en herdenkingen', 'Advies over de opzet vooraf']},
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
    ('Vandaag', 'De volgende generatie',
     'Het bedrijf is nog altijd in handen van de familie. De volgende generatie groeide op tussen de kabels en brengt met de eigen bedrijven MATRIX E.I.L. en ARGUS Systems nieuwe energie mee. Dezelfde betrokkenheid, met de techniek van nu.'),
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

# Eigen pagina per dienst, gekoppeld via 'slug' aan DIENSTEN
DIENST_PAGINAS = {
    'geluid': {
        'pagina': 'geluid.html',
        'seo': ('Geluid huren in Limburg | Geluidstechniek voor events | GTF Franzen',
                'Geluid huren met eigen technici voor festivals, feesten, bruiloften en bedrijfsevents in Zuid-Limburg, België en Duitsland. Familiebedrijf uit Bocholtz, eigen materiaal.'),
        'h1': 'Geluid voor<br>events in <em>Limburg.</em>',
        'sub': 'Geluidsverhuur met eigen technici · Waar het ooit begon',
        'intro': 'Met geluid is GTF Franzen ooit begonnen: met verhuur en speakers die we zelf bouwden. Vandaag leveren we geluid voor een speech in een zaal tot een volle festivalwei. Altijd met eigen materiaal en eigen mensen, die het systeem afstemmen op de ruimte, het publiek en wat er op het podium gebeurt.',
        'krijg': ['Geluidssysteem op maat van zaal, tent of open lucht', 'Mengtafel met bediening door onze eigen technicus', 'Podium- en monitorgeluid voor bands en artiesten', 'Draadloze microfoons voor speech en presentatie', 'Opbouw, soundcheck en afbouw', 'Rekening houden met geluidsnormen en omwonenden'],
        'aanpak': [('Afgestemd op de plek', 'Een tent klinkt anders dan een sporthal of een weiland. We kiezen het systeem en de opstelling op basis van de ruimte en het aantal mensen, zodat het overal goed klinkt en niet alleen vooraan.'),
                   ('Verstaanbaar én vol', 'Een speech moet je verstaan, een band moet je voelen. We zorgen voor allebei: heldere spraak en een vol geluid, zonder dat het pijn doet aan je oren.'),
                   ('Mensen achter de knoppen', 'Onze technicus staat achter de mengtafel en kent het materiaal door en door. Verandert er iets in het programma, dan schakelen we gewoon mee.')],
        'fotos': ['geluid.jpg', 'tent.jpg', 'zaal.jpg'],
        'events': ['festival', 'feest', 'bedrijf', 'dorpsfeest'],
        'projecten': ['sportclub-jubileum', 'woeesj-stock'],
        'faq': [('Komt er een technicus mee?', 'Bij bands, grotere feesten en events staat er altijd een technicus van ons bij. Zo weet je zeker dat het goed klinkt en hoef je zelf niet aan de knoppen te zitten. Voor kleinere toepassingen bespreken we samen wat handig is.'),
                ('Kunnen jullie geluid voor een band of artiest regelen?', 'Ja. We verzorgen podium- en monitorgeluid en stemmen vooraf af met de technische wensen van de artiesten.'),
                ('Wat kost geluid huren?', 'Dat hangt af van de locatie, het aantal gasten en het programma. Je krijgt altijd een vrijblijvende offerte op maat.')],
    },
    'licht': {
        'pagina': 'licht.html',
        'seo': ('Lichttechniek en lichtshow voor events | GTF Franzen en MATRIX E.I.L.',
                'Sfeerverlichting, lichtontwerp en lichtshows voor festivals, feesten en bedrijfsevents. GTF Franzen werkt samen met MATRIX E.I.L., bekend van grote festivals en clubshows.'),
        'h1': 'Licht dat<br>je event <em>maakt.</em>',
        'sub': 'Sfeerverlichting, lichtshows en visuals · Samen met MATRIX E.I.L.',
        'intro': 'Licht bepaalt hoe je event voelt, en hoe het eruitziet op elke foto en video. Voor licht en visuals werken we samen met MATRIX E.I.L., het lichtbedrijf uit onze eigen familie dat draait op grote festivals en clubshows. Die kennis van de grote podia nemen we mee naar jouw dorpsfeest, jubileum of bedrijfsevent.',
        'krijg': ['Sfeerverlichting voor zaal, tent en buitenlocatie', 'Lichtontwerp en voorprogrammering', 'Moving heads, LED en effecten', 'CO2, confetti en andere showeffecten', 'Visuals en LED-schermen', 'Live bediening tijdens de show'],
        'aanpak': [('Eerst de sfeer', 'We beginnen niet bij de lampen, maar bij het gevoel dat je wilt neerzetten. Warm en gezellig, strak en zakelijk of een volle festivalshow.'),
                   ('Vooraf ontworpen', 'Bij grotere shows ontwerpt MATRIX het licht vooraf en wordt de show voorgeprogrammeerd. Op de dag zelf is er dan tijd voor de details.'),
                   ('Live op de muziek', 'Tijdens de show staat er iemand achter de lichttafel die meegaat met de muziek en het programma. Geen standaardprogramma op de achtergrond.')],
        'fotos': ['licht.jpg', 'rig-rood.jpg', 'gala.jpg'],
        'events': ['festival', 'vereniging', 'bedrijf', 'feest'],
        'projecten': ['sportclub-jubileum', 'woeesj-stock'],
        'faq': [('Wat is MATRIX E.I.L.?', 'MATRIX E.I.L. is het licht- en showbedrijf uit de familie Franzen. MATRIX werkt op grote festivals en clubshows en verzorgt bij GTF Franzen het lichtontwerp, de visuals en de show. Voor jou blijft er één aanspreekpunt.'),
                ('Kunnen jullie ook alleen sfeerverlichting leveren?', 'Ja. Niet elk event heeft een lichtshow nodig. Soms is warme sfeerverlichting in een zaal of tent precies genoeg.'),
                ('Leveren jullie ook LED-schermen en visuals?', 'Ja. Samen met MATRIX E.I.L. leveren we LED-schermen en maken we visuals die passen bij je event.')],
    },
    'omroep': {
        'pagina': 'omroep-100v.html',
        'seo': ('Omroepinstallatie huren | 100V-omroep voor events | GTF Franzen',
                'Omroepinstallaties en 100V-systemen voor schuttersfeesten, wielerkoersen, optochten en grote terreinen. Bekend van het Oud Limburgs Schuttersfeest en de Amstel Gold Race.'),
        'h1': 'Omroep die<br>overal <em>aankomt.</em>',
        'sub': '100V-omroep en hoorns · Bekend van het OLS en de Amstel Gold Race',
        'intro': 'Omroep is waar GTF Franzen in Limburg al generaties om bekendstaat. Je herkent ons aan de hoorns met FRANZEN BOCHOLTZ erop. Op het Oud Limburgs Schuttersfeest hingen er meer dan 140, langs de Amstel Gold Race hangen ze langs het parcours. Over een groot terrein of een lange route zorgen we dat iedereen hoort wat er gezegd wordt.',
        'krijg': ['100V-omroep over grote afstanden', 'Hoorns op masten, palen en gebouwen', 'Omroep voor jurywagens en mobiele omroep', 'Omroep voor optochten en wielerkoersen', 'Microfoons voor speaker en presentator', 'Advies over de opzet vooraf'],
        'aanpak': [('Waarom 100V?', 'Met een 100V-systeem sluit je veel hoorns aan over lange afstanden, zonder dat het geluid wegvalt. Ideaal voor grote terreinen, parcoursen en optochten.'),
                   ('Het terrein in kaart', 'We kijken vooraf waar het publiek staat en waar de hoorns moeten hangen. Zo is de speaker overal te verstaan, zonder dat het op één plek te hard staat.'),
                   ('Ook onderweg', 'Met omroep op jurywagens en mobiele omroep reist het geluid mee met de optocht of de koers.')],
        'fotos': ['amstel-3.jpg', 'masten.jpg', 'ols.jpg'],
        'events': ['gemeente', 'dorpsfeest', 'festival'],
        'projecten': ['amstel-gold-race'],
        'faq': [('Wat is een 100V-omroepinstallatie?', 'Een systeem waarmee je veel luidsprekers of hoorns via lange kabels op één versterker aansluit. Het is betrouwbaar en geschikt voor grote terreinen, routes en gebouwen.'),
                ('Hoeveel hoorns kunnen jullie plaatsen?', 'Dat hangt af van het terrein. Op het Oud Limburgs Schuttersfeest hingen er meer dan 140. Kleiner kan natuurlijk ook.'),
                ('Doen jullie ook omroep voor jurywagens?', 'Ja. Op schuttersfeesten zoals het OLS reden diverse jurywagens met onze omroep.')],
    },
    'stroom': {
        'pagina': 'stroom-aggregaten.html',
        'seo': ('Aggregaat huren voor events | Stroomvoorziening | GTF Franzen',
                'Aggregaten en stroomverdeling voor festivals, feesttenten en buitenevents in Limburg. Veilige stroom voor podium, bars, koeling en foodtrucks.'),
        'h1': 'Stroom voor<br>je <em>buitenevent.</em>',
        'sub': 'Aggregaten en stroomverdeling · Voor tent, terrein en podium',
        'intro': 'Op een weiland, plein of parkeerplaats begint alles bij stroom. Wij leveren aggregaten en zorgen voor een veilige, overzichtelijke stroomverdeling. Zo blijven geluid, licht, bars, koeling en foodtrucks de hele dag gewoon draaien.',
        'krijg': ['Aggregaten voor kleine en grote events', 'Stroomverdeling en bekabeling over het terrein', 'Berekening van de stroombehoefte vooraf', 'Aansluitingen voor bars, koeling en foodtrucks', 'Veilige kabelroutes voor publiek', 'Afstemming met andere partijen op het terrein'],
        'aanpak': [('Eerst rekenen', 'We maken vooraf een overzicht van alles wat stroom nodig heeft. Zo weet je zeker dat er genoeg is en dat er niets uitvalt op het drukste moment.'),
                   ('Netjes verdeeld', 'Kabels lopen waar ze horen, met verdeelkasten op logische plekken. Veilig voor het publiek en makkelijk voor iedereen die moet aansluiten.'),
                   ('Eén partij voor alles', 'Omdat wij ook het geluid en licht doen, is alles op elkaar afgestemd. Geen discussie over wie verantwoordelijk is als er iets niet werkt.')],
        'fotos': ['stroom.jpg', 'tent.jpg', 'ols.jpg'],
        'events': ['festival', 'dorpsfeest', 'vereniging'],
        'projecten': ['sportclub-jubileum'],
        'faq': [('Hoe weet ik hoeveel stroom ik nodig heb?', 'Dat rekenen wij voor je uit. Geef door wat er op je terrein komt, zoals podium, bars, koeling en foodtrucks, dan bepalen we welk aggregaat en welke verdeling nodig is.'),
                ('Kunnen andere partijen op jullie stroom aansluiten?', 'Ja. We zorgen voor aansluitpunten voor bijvoorbeeld bars, cateraars en foodtrucks, en stemmen af wie wat nodig heeft.'),
                ('Kan ik alleen stroom bij jullie afnemen?', 'Dat kan. Maar het werkt vaak het prettigst als stroom, geluid en licht uit één hand komen.')],
    },
    'productie': {
        'pagina': 'eventproductie.html',
        'seo': ('Complete eventproductie in Limburg | Eén technische partner | GTF Franzen',
                'Complete technische productie voor festivals, jubilea en bedrijfsevents: geluid, licht, stroom, omroep en podium uit één hand, met één aanspreekpunt.'),
        'h1': 'Je hele productie,<br><em>één partner.</em>',
        'sub': 'Geluid, licht, stroom en omroep uit één hand',
        'intro': 'De kracht van GTF Franzen zit in het geheel. Geluid, licht, stroom, omroep en podiumtechniek komen bij ons uit één hand, met bijna volledig eigen materiaal en één aanspreekpunt. Je hoeft niet te schakelen tussen vijf leveranciers. Wij denken mee, plannen alles op elkaar af en staan er op de dag zelf.',
        'krijg': ['Eén aanspreekpunt voor alle techniek', 'Technische planning en draaiboek', 'Geluid, licht, stroom en omroep op elkaar afgestemd', 'Lichtontwerp en show met MATRIX E.I.L.', 'Afstemming met artiesten, catering en locatie', 'Opbouw, show en afbouw door onze eigen crew'],
        'aanpak': [('Samen plannen', 'We beginnen bij je programma en je locatie. Daaruit volgt wat er nodig is, wanneer het moet staan en wie wat doet.'),
                   ('Alles past op elkaar', 'Omdat alles van ons komt, past alles op elkaar. Van stroom en kabelroutes tot het moment waarop licht en geluid samen de show inzetten.'),
                   ('Op de dag zelf', 'Onze crew bouwt op, test alles en staat klaar tijdens het event: bij de mengtafel, bij de lichttafel en backstage.')],
        'fotos': ['proj/sportclub-jubileum/01.jpg', 'beurs.jpg', 'rig-groen.jpg'],
        'events': ['festival', 'vereniging', 'bedrijf'],
        'projecten': ['sportclub-jubileum', 'woeesj-stock'],
        'faq': [('Waarom alles bij één partij?', 'Eén partij betekent één planning, één aanspreekpunt en geen discussie over wie waarvoor verantwoordelijk is. Dat scheelt je tijd, overleg en stress.'),
                ('Werken jullie met de technische wensen van artiesten?', 'Ja. We stemmen vooraf af met de artiesten en hun technici, zodat alles klaarstaat wat ze nodig hebben.'),
                ('Komen jullie vooraf naar de locatie?', 'Bij grotere producties komen we graag langs. Zo weten we precies waar podium, stroom en techniek moeten komen.')],
    },
}

# Eigen pagina per soort event, gekoppeld via 'id' aan EVENTS
EVENT_PAGINAS = {
    'festival': {
        'pagina': 'festival.html',
        'seo': ('Festivaltechniek in Limburg | Geluid, licht en stroom | GTF Franzen',
                'Geluid, licht, stroom en omroep voor festivals in Zuid-Limburg, België en Duitsland. Alle podia op elkaar afgestemd, met één aanspreekpunt.'),
        'h1': 'Techniek voor<br>je <em>festival.</em>',
        'sub': 'Podia, omroep en stroom over het hele terrein',
        'intro': 'Meerdere podia, wisselende artiesten en duizenden bezoekers. Op een festival moet alles kloppen, en het moet op elkaar aansluiten. Wij plannen de techniek van alle stages, het terrein en de stroom als één geheel en houden het overzicht, van het eerste overleg tot de laatste act.',
        'aanpak': [('Alle podia op elkaar afgestemd', 'Elk podium krijgt het geluid en licht dat bij de acts past, zonder dat de stages elkaar in de weg zitten.'),
                   ('Het hele terrein', 'Stroom voor bars en foodtrucks, omroep voor mededelingen en verlichting voor looproutes. Ook dat hoort bij een festival dat klopt.'),
                   ('Een show om te onthouden', 'Met MATRIX E.I.L. ontwerpen we een lichtshow met effecten, CO2 en confetti die past bij je line-up.')],
        'fotos': ['proj/sportclub-jubileum/28.jpg', 'hero.jpg', 'rig-rood.jpg'],
        'diensten': ['geluid', 'licht', 'stroom', 'productie'],
        'projecten': ['woeesj-stock', 'sportclub-jubileum'],
        'faq': [('Kunnen jullie meerdere podia tegelijk verzorgen?', 'Ja. We plannen de techniek van alle podia samen, zodat alles op elkaar aansluit en je één aanspreekpunt hebt.'),
                ('Regelen jullie ook stroom voor het hele terrein?', 'Ja. We leveren aggregaten en stroomverdeling voor podia, bars, koeling en foodtrucks.'),
                ('Hoe vroeg moeten we beginnen met plannen?', 'Voor een festival het liefst ruim van tevoren, zeker in het zomerseizoen. Dan is er tijd om de locatie te bekijken en alles goed voor te bereiden.')],
    },
    'dorpsfeest': {
        'pagina': 'dorpsfeest-carnaval.html',
        'seo': ('Geluid en licht voor dorpsfeest, kermis en carnaval | GTF Franzen',
                'Techniek voor dorpsfeesten, kermis, carnaval en feesttenten in Zuid-Limburg. Tentgeluid, sfeerlicht, omroep voor optochten en stroom.'),
        'h1': 'Het hele dorp<br>op de <em>been.</em>',
        'sub': 'Kermis, carnaval, schuttersfeest en feesttent',
        'intro': 'Kermis, carnaval, een schuttersfeest of een avond in de feesttent. We komen zelf uit een Limburgs dorp en kennen de verenigingen, de locaties en de tradities. We weten wat er nodig is om er een avond van te maken waar nog lang over gepraat wordt.',
        'aanpak': [('Tent of zaal vol sfeer', 'Geluid dat de hele tent vult en sfeerlicht dat er warm uitziet, of het nu een middag voor jong en oud is of een avond tot in de late uurtjes.'),
                   ('Optocht en buitenprogramma', 'Met omroep langs de route en op het plein hoort iedereen wat er gebeurt, ook achteraan de optocht.'),
                   ('Snel schakelen', 'Verandert het programma? Komt er een extra act bij? Wij staan erbij en schakelen gewoon mee.')],
        'fotos': ['proj/woeesj-stock/01.jpg', 'tent.jpg', 'zaal.jpg'],
        'diensten': ['geluid', 'licht', 'omroep', 'stroom'],
        'projecten': ['woeesj-stock', 'sportclub-jubileum'],
        'faq': [('Verzorgen jullie ook carnavalszittingen?', 'Ja. Voor zittingen en feesten in zalen en tenten leveren we geluid, licht en waar nodig een podium.'),
                ('Kunnen jullie omroep voor een optocht regelen?', 'Ja. Omroep is een van onze specialiteiten. We zorgen dat de speaker langs de route en op het plein goed te verstaan is.'),
                ('Werken jullie ook met een beperkt budget?', 'Ja. Vertel ons wat je wilt en wat je budget is, dan denken we mee over wat haalbaar is.')],
    },
    'feest': {
        'pagina': 'bruiloft-feest.html',
        'seo': ('Geluid en licht voor je bruiloft of feest in Limburg | GTF Franzen',
                'Microfoons voor ceremonie en speeches, geluid voor band of dj en sfeerverlichting voor je bruiloft of feest. Familiebedrijf uit Bocholtz.'),
        'h1': 'Jullie dag,<br><em>zonder zorgen.</em>',
        'sub': 'Bruiloften, verjaardagen en besloten feesten',
        'intro': 'Van de ceremonie en de speeches tot de band en de dansvloer. Op zo’n dag wil je niet nadenken over kabels en microfoons. Wij zorgen dat alles klinkt en er mooi uitziet, en dat de techniek klaarstaat voordat de eerste gast binnenkomt. Jullie hoeven alleen maar te genieten.',
        'aanpak': [('Ceremonie en speeches', 'Draadloze microfoons die gewoon werken, zodat iedereen het jawoord en elke speech goed verstaat.'),
                   ('Band of dj', 'Geluid dat past bij de zaal en het aantal gasten. Vol op de dansvloer, prettig aan tafel.'),
                   ('Sfeer in de zaal', 'Sfeerverlichting die de ruimte warm maakt en zorgt voor mooie foto’s, van het diner tot de laatste dans.')],
        'fotos': ['zaal.jpg', 'gala.jpg', 'zaal-2.jpg'],
        'diensten': ['geluid', 'licht'],
        'projecten': [],
        'faq': [('Zijn jullie er de hele avond bij?', 'Dat stemmen we samen af. Bij een band of een uitgebreid programma blijft er een technicus. Bij een eenvoudiger opzet bouwen we op, testen we alles en spreken we af wanneer we terugkomen.'),
                ('Kunnen jullie ook op een buitenlocatie opbouwen?', 'Ja. Op een buitenlocatie regelen we ook de stroom, zodat je niet afhankelijk bent van wat er op de locatie aanwezig is.'),
                ('Wanneer moeten we boeken?', 'Hoe eerder hoe beter, zeker voor zaterdagen in het trouwseizoen.')],
    },
    'bedrijf': {
        'pagina': 'bedrijfsevent.html',
        'seo': ('Techniek voor bedrijfsevents en congressen | AV in Limburg | GTF Franzen',
                'Geluid, licht en techniek voor congressen, presentaties, personeelsfeesten en beurzen in Limburg en omgeving. Strak, professioneel en op tijd.'),
        'h1': 'Strak, zakelijk<br>en <em>op tijd.</em>',
        'sub': 'Congressen, presentaties, personeelsfeesten en beurzen',
        'intro': 'Een congres, presentatie, personeelsfeest, beurs of productlancering. De techniek moet gewoon werken en de boodschap moet aankomen. Wij zorgen voor heldere spraak, passend licht en een soepel verloop, en bouwen op en af zonder dat je er last van hebt.',
        'aanpak': [('De boodschap komt aan', 'Heldere spraak tot achter in de zaal en draadloze microfoons voor sprekers en panels.'),
                   ('Uitstraling die past', 'Podium- en sfeerverlichting en desgewenst LED-schermen in de stijl van je bedrijf of merk.'),
                   ('Regie tijdens het programma', 'Een technicus volgt het draaiboek, zodat elke spreker, video en overgang op het juiste moment komt.')],
        'fotos': ['gala.jpg', 'beurs.jpg', 'gebouw.jpg'],
        'diensten': ['geluid', 'licht', 'productie'],
        'projecten': [],
        'faq': [('Kunnen jullie buiten kantoortijden opbouwen?', 'Ja. We stemmen de opbouw af op de locatie en je programma, ook vroeg in de ochtend of de avond ervoor.'),
                ('Leveren jullie ook schermen voor presentaties?', 'Ja. Samen met MATRIX E.I.L. leveren we LED-schermen en zorgen we dat je presentaties goed in beeld komen.'),
                ('Werken jullie ook over de grens?', 'Ja. We werken in Nederland, België en Duitsland.')],
    },
    'vereniging': {
        'pagina': 'vereniging-jubileum.html',
        'seo': ('Techniek voor jubileum en verenigingsfeest | GTF Franzen',
                'Een jubileum, lustrum of concert voor je vereniging? GTF Franzen verzorgt de complete productie met geluid, licht, show en stroom. Bekend van Sportclub’25 100 jaar.'),
        'h1': 'Een jubileum<br>om <em>nooit</em> te vergeten.',
        'sub': 'Jubilea, lustra, concerten en verenigingsfeesten',
        'intro': 'Honderd jaar sportclub, een lustrum van de schutterij of een bijzonder concert van de harmonie. Voor zo’n moment wil je techniek die het verhaal van je vereniging groot maakt. Daar denken we graag in mee, ook met een beperkt budget. Voor Sportclub’25 in Bocholtz zetten we zo een productie neer waar het dorp nog over praat.',
        'aanpak': [('Het verhaal van je club', 'We denken mee over hoe je jubileum eruit moet zien en wat er op het programma staat, en vertalen dat naar techniek.'),
                   ('Een echte show', 'Met licht, effecten en visuals van MATRIX E.I.L. krijgt je jubileum de uitstraling van een groot podium.'),
                   ('Binnen je budget', 'Verenigingen werken vaak met vrijwilligers en een vast budget. We zijn eerlijk over wat er kan en wat het kost.')],
        'fotos': ['proj/sportclub-jubileum/14.jpg', 'proj/sportclub-jubileum/01.jpg', 'rig-staand.jpg'],
        'diensten': ['productie', 'geluid', 'licht', 'stroom'],
        'projecten': ['sportclub-jubileum'],
        'faq': [('Kunnen jullie een tent of zaal volledig aankleden?', 'Ja. Van geluid en licht tot stroom en podiumtechniek: we verzorgen de complete productie.'),
                ('Kunnen vrijwilligers van onze club helpen?', 'Zeker. We stemmen vooraf af wie wat doet, zodat iedereen weet waar hij of zij aan toe is.'),
                ('Wat deden jullie bij Sportclub’25?', 'Voor het honderdjarig bestaan van Sportclub’25 in Bocholtz verzorgden we de productie en techniek, met lichtontwerp, visuals en show door MATRIX E.I.L.')],
    },
    'gemeente': {
        'pagina': 'schuttersfeest-omroep.html',
        'seo': ('Omroep voor schuttersfeesten, wielerkoersen en grote terreinen | GTF Franzen',
                'Omroep op 100V voor schuttersfeesten, wielerkoersen, herdenkingen en markten. Meer dan 140 hoorns op het Oud Limburgs Schuttersfeest, omroep langs de Amstel Gold Race.'),
        'h1': 'Iedereen hoort het.<br><em>Overal.</em>',
        'sub': 'Schuttersfeesten, wielerkoersen, herdenkingen en markten',
        'intro': 'Op een groot terrein of langs een lange route moet iedereen kunnen horen wat er gebeurt. Op het Oud Limburgs Schuttersfeest hingen meer dan 140 hoorns van ons op 100V en reden diverse jurywagens met onze omroep. Langs het parcours van de Amstel Gold Race hoort het publiek dankzij ons wat er in de koers gebeurt.',
        'aanpak': [('Groot terrein, één geluid', 'Hoorns op de juiste plekken, zodat de speaker overal te verstaan is, van de tribune tot achter op het terrein.'),
                   ('Langs de route', 'Bij koersen en optochten volgt de omroep de route, met hoorns langs het parcours en mobiele omroep waar nodig.'),
                   ('Ervaring van generaties', 'Omroep is waar we groot mee zijn geworden. We weten wat werkt bij wind, regen en duizenden mensen.')],
        'fotos': ['ols.jpg', 'amstel-1.jpg', 'masten.jpg'],
        'diensten': ['omroep', 'stroom', 'geluid'],
        'projecten': ['amstel-gold-race'],
        'faq': [('Kunnen jullie een heel schuttersfeest van omroep voorzien?', 'Ja. Op het Oud Limburgs Schuttersfeest hingen meer dan 140 hoorns van ons en reden diverse jurywagens met onze omroep.'),
                ('Doen jullie ook omroep bij wielerwedstrijden?', 'Ja. Langs het parcours van de Amstel Gold Race verzorgen wij de omroep.'),
                ('Werken jullie ook voor gemeenten?', 'Ja. Voor herdenkingen, markten en andere evenementen in de openbare ruimte leveren we omroep en geluid.')],
    },
}

# Werkgebied: (naam, lengtegraad, breedtegraad, land)
PLAATSEN = [
    ('Bocholtz', 6.005, 50.818, 'NL'), ('Simpelveld', 5.982, 50.834, 'NL'), ('Kerkrade', 6.063, 50.866, 'NL'), ('Heerlen', 5.981, 50.888, 'NL'),
    ('Landgraaf', 6.03, 50.905, 'NL'), ('Brunssum', 5.97, 50.947, 'NL'), ('Valkenburg', 5.832, 50.865, 'NL'), ('Gulpen', 5.889, 50.815, 'NL'),
    ('Vaals', 6.019, 50.771, 'NL'), ('Maastricht', 5.69, 50.851, 'NL'), ('Sittard', 5.869, 50.998, 'NL'),
    ('Aken', 6.083, 50.776, 'DE'), ('Herzogenrath', 6.094, 50.87, 'DE'), ('Eschweiler', 6.27, 50.817, 'DE'),
    ('Kelmis', 6.0, 50.716, 'BE'), ('Eupen', 6.036, 50.63, 'BE'), ('Voeren', 5.79, 50.75, 'BE'), ('Tongeren', 5.464, 50.781, 'BE'),
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


def ring_txt(pid):
    return (f'<svg class="ring-txt" viewBox="0 0 1500 1500"><defs><path id="{pid}" d="M750 750m-560 0a560 560 0 1 1 1120 0a560 560 0 1 1-1120 0"/></defs>'
            f'<text><textPath href="#{pid}" textLength="3480" lengthAdjust="spacing">FRANZEN · BOCHOLTZ · SOUND · LIGHT · VISION ·</textPath></text></svg>')

TICKER = ''.join(f'<span>{t}</span>' for t in ('Oud Limburgs Schuttersfeest', 'Amstel Gold Race', 'Sportclub’25', 'Woeësj-Stock', 'Carnaval', 'Kermis', 'Bruiloften', 'Congressen', 'Jubilea', 'Optochten'))
CUES = ''.join(f'<li><span class="cue-nr">CUE {i:02d}</span><b>{t}</b><span>{w}</span></li>' for i, (t, w) in enumerate([
    ('Oud Limburgs Schuttersfeest', '140+ hoorns en jurywagens'), ('Amstel Gold Race', 'Omroep langs het parcours'),
    ('Sportclub’25, 100 jaar', 'Complete productie'), ('Woeësj-Stock', 'Festival in de feesttent')], 1))

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


def header(current, dark=True, sectie=None):
    cur = ' aria-current="page"'
    links = ''.join(f'<a href="{href}"{cur if href in (current, sectie) else ""}>{label}</a>' for href, label in NAV)
    return f'''<a class="skip" href="#main">Naar de inhoud</a>
<header class="site-header{' on-dark' if dark else ''}">
  <div class="wrap">
    <a class="logo" href="index.html" aria-label="GTF Franzen home">{LOGO}</a>
    <div class="vu" aria-hidden="true"><span class="vu-l">L</span><span class="vu-row" data-ch="0">{'<i></i>' * 16}</span><span class="vu-l">R</span><span class="vu-row" data-ch="1">{'<i></i>' * 16}</span></div>
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
        <p>Geluid, licht, omroep, stroom en complete producties. Familiebedrijf uit Bocholtz, al meer dan 50 jaar.</p>
      </div>
      <div>
        <h4>Diensten</h4>
        <ul>{''.join(f'<li><a href="{DIENST_PAGINAS[d["slug"]]["pagina"]}">{d["titel"]}</a></li>' for d in DIENSTEN)}</ul>
      </div>
      <div>
        <h4>Evenementen</h4>
        <ul>{''.join(f'<li><a href="{EVENT_PAGINAS[e["id"]]["pagina"]}">{e["label"]}</a></li>' for e in EVENTS)}</ul>
      </div>
      <div>
        <h4>GTF Franzen</h4>
        <ul><li><a href="over.html">Ons verhaal</a></li><li><a href="projecten.html">Projecten</a></li><li><a href="werkwijze.html">Werkwijze</a></li><li><a href="werkgebied.html">Werkgebied</a></li><li><a href="contact.html">Contact</a></li><li><a href="{MATRIX}" target="_blank" rel="noopener">MATRIX E.I.L.</a></li>{socials}</ul>
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
    nr = f'CH {nr}' if nr.isdigit() else nr
    return f'<p class="eyebrow reveal"><span>{nr}</span>{txt}</p>'


PLUG = '''<div class="power">
      <div class="power-track">
        <span class="cable" aria-hidden="true"></span>
        <button class="plug" type="button" aria-label="Steek de stekker in het stopcontact">
          <svg viewBox="0 0 120 70" aria-hidden="true"><rect x="0" y="22" width="20" height="26" rx="4" class="p-grip"/><rect x="16" y="8" width="58" height="54" rx="12" class="p-body"/><rect x="74" y="20" width="34" height="5" rx="2.5" class="p-pin"/><rect x="74" y="45" width="34" height="5" rx="2.5" class="p-pin"/><circle cx="45" cy="35" r="9" class="p-mark"/></svg>
        </button>
        <span class="socket" aria-hidden="true"><svg viewBox="0 0 90 90"><circle cx="45" cy="45" r="42" class="s-plate"/><circle cx="45" cy="45" r="30" class="s-cup"/><circle cx="45" cy="34" r="4.5" class="s-hole"/><circle cx="45" cy="56" r="4.5" class="s-hole"/><circle cx="45" cy="45" r="44" class="s-led"/></svg></span>
      </div>
      <p class="power-hint"><span class="off">Sleep de stekker erin</span><span class="on">Stroom staat erop. Nu jouw event.</span></p>
    </div>'''


def cta_band():
    return f'''<section class="cta-band">
  <div class="wrap reveal">
    {PLUG}
    <h2 class="display">Vertel ons wat je<br><em>van plan bent.</em></h2>
    <p class="lead">Een kort berichtje is genoeg. We denken vrijblijvend mee en sturen je een voorstel op maat.</p>
    <div class="btns"><a class="btn fill" href="contact.html">Vraag een offerte aan</a><a class="btn ghost" href="projecten.html">Bekijk ons werk</a></div>
  </div>
</section>'''


def page(name, title, desc, body, dark_header=True, ld=None, body_cls='', image='assets/img/og.jpg', extra_js='', sectie=None):
    global CURRENT
    CURRENT = name
    html = (head(title, desc, image=image, ld=ld) + f'\n<body class="{body_cls}">\n' + header(name, dark_header, sectie)
            + '\n<main id="main">\n' + body + '\n</main>\n' + footer(extra_js))
    (ROOT / name).write_text(html, encoding='utf-8')
    return name


# ---------------------------------------------------------------- Home
def home():
    diensten = ''.join(f'''
      <a class="svc reveal" href="{DIENST_PAGINAS[d["slug"]]["pagina"]}">
        <span class="svc-nr">CH {d["nr"]}</span>
        <svg class="scope" viewBox="0 0 200 40" preserveAspectRatio="none" aria-hidden="true"><path d="M0 20 Q 12.5 2 25 20 T 50 20 T 75 20 T 100 20 T 125 20 T 150 20 T 175 20 T 200 20"/></svg>
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
          <div class="btns"><a class="btn fill" href="contact.html?type={e["id"]}">Plan je {e["label"].split(" ")[0].lower()}</a><a class="btn ghost" href="{EVENT_PAGINAS[e["id"]]["pagina"]}">Meer hierover</a></div>
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
  <div class="hero-waves" aria-hidden="true">{ring_txt('ring-hero')}{mark('wave-mark')}<i></i><i></i><i></i></div>
  <div class="wrap hero-inner">
    <p class="hero-kicker"><span class="dot"></span>Familiebedrijf uit Bocholtz · NL · BE · DE</p>
    <h1 class="hero-title">Al 50 jaar<br>het geluid<br>van <em>Limburg.</em></h1>
    <p class="hero-lead">Van de omroep op het schuttersfeest tot de show op het festivalpodium. Familiebedrijf GTF Franzen regelt geluid, licht, stroom en complete producties, met eigen materiaal en één aanspreekpunt van begin tot eind.</p>
    <div class="btns"><a class="btn fill" href="contact.html">Vraag een offerte aan</a><a class="btn ghost" href="#evenement">Wat organiseer je?</a></div>
  </div>
</section>

<div class="ticker" aria-hidden="true"><div class="ticker-run">{TICKER}{TICKER}</div></div>

<section class="facts" aria-label="GTF Franzen in cijfers">
  <div class="wrap">
    <div class="fact reveal"><b data-count="50">50</b><sup>+</sup><span>jaar ervaring in geluid en techniek</span><i class="meter" aria-hidden="true"></i></div>
    <div class="fact reveal"><b data-count="100">100</b><sup>+</sup><span>projecten per jaar</span><i class="meter" aria-hidden="true"></i></div>
    <div class="fact reveal"><b data-count="140">140</b><sup>+</sup><span>100V-hoorns op één event, zoals het OLS</span><i class="meter" aria-hidden="true"></i></div>
    <div class="fact reveal"><b class="fact-txt">NL·BE·DE</b><span>van dorpsplein tot festivalterrein</span><i class="meter" aria-hidden="true"></i></div>
  </div>
</section>

<section class="section herken">
  <div class="wrap two">
    <div class="herken-img reveal"><img src="assets/img/amstel-2.jpg" alt="Hoorn met de naam Franzen Bocholtz langs het parcours van de Amstel Gold Race" loading="lazy"><span class="stamp" aria-hidden="true">{ring_txt('ring-stamp')}</span></div>
    <div>
      {eyebrow('01', 'Herkenbaar')}
      <h2 class="display reveal">Zie je deze hoorn?<br><em>Dan zijn wij er.</em></h2>
      <p class="lead reveal">Op schuttersfeesten, langs de Amstel Gold Race, bij optochten en op sportvelden in heel Limburg hangen hoorns met FRANZEN BOCHOLTZ erop. Al generaties lang. Het is onze naam, dus we zorgen dat het klopt.</p>
      <ol class="cues reveal">{CUES}</ol>
    </div>
  </div>
</section>

<section class="section intro">
  <div class="wrap two">
    <div>
      {eyebrow('02', 'Waarom één partner')}
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
      {eyebrow('03', 'Wat we doen')}
      <h2 class="display reveal">Alles voor een event<br><em>dat klopt.</em></h2>
    </div>
    <div class="svc-grid">{diensten}
    </div>
  </div>
</section>

<section class="section picker" id="evenement">
  <div class="wrap">
    <div class="sec-head">
      {eyebrow('04', 'Voor elk event')}
      <h2 class="display reveal">Wat ga jij<br><em>organiseren?</em></h2>
    </div>
    <div class="tabs reveal" role="tablist" aria-label="Soort event">{tabs}</div>
    <div class="panes">{panes}
    </div>
  </div>
</section>

<section class="section matrix">
  <div class="wrap two">
    <div class="matrix-img reveal"><img src="assets/img/licht.jpg" alt="Lichtshow met beams en LED boven een vol publiek" loading="lazy"><span class="matrix-tag">Licht · Video · Sfeer</span></div>
    <div>
      {eyebrow('05', 'Met MATRIX E.I.L.')}
      <h2 class="display reveal">De kennis van<br><em>de grote podia.</em></h2>
      <p class="lead reveal">Voor licht, video en sfeer werken we samen met MATRIX E.I.L., het licht- en showbedrijf uit onze eigen familie. MATRIX draait op grote festivals en clubshows als Electrisize, Boiler Room en ParkCity Live.</p>
      <p class="reveal">Die ervaring nemen we mee naar jouw event. MATRIX kijkt mee naar de sfeer, ontwerpt het licht, maakt visuals en zet LED-schermen neer. Zo krijgt een dorpsfeest, jubileum of bedrijfsevent de uitstraling van een groot podium, en heb jij nog steeds één aanspreekpunt.</p>
      <ul class="checks reveal"><li>Lichtontwerp en voorprogrammering</li><li>Video, visuals en LED-schermen</li><li>Advies over sfeer en beleving</li><li>Live bediening tijdens de show</li></ul>
      <a class="link-arrow reveal" href="{MATRIX}" target="_blank" rel="noopener">Bekijk MATRIX E.I.L.</a>
    </div>
  </div>
</section>

<section class="section story dark">
  <div class="wrap two">
    <div class="story-copy">
      {eyebrow('06', 'Ons verhaal')}
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

<section class="section">
  <div class="wrap">
    <div class="sec-head row">
      <div>{eyebrow('07', 'Projecten')}
      <h2 class="display reveal">Waar we<br><em>trots op zijn.</em></h2></div>
      <a class="link-arrow reveal" href="projecten.html">Alle projecten</a>
    </div>
    <div class="proj-grid">{proj}
    </div>
  </div>
</section>

<section class="section faq">
  <div class="wrap two">
    <div>
      {eyebrow('08', 'Veelgestelde vragen')}
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
      <a class="btn ghost reveal" href="{DIENST_PAGINAS[d["slug"]]["pagina"]}">Alles over {d["titel"].lower()}</a>
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
  <div class="wrap two">
    <div>{eyebrow('03', 'De familie')}<h2 class="display reveal">Je belt niet<br>met een <em>afdeling.</em></h2></div>
    <div>
      <p class="lead reveal">Bij GTF Franzen spreek je met de familie. Dezelfde mensen die je voorstel maken, staan op de dag zelf naast het podium. Geen callcenter, geen ticketnummer en geen gedoe over wie waarvoor verantwoordelijk is.</p>
      <ul class="checks reveal"><li>Al generaties in handen van de familie Franzen</li><li>Bijna volledig eigen materiaal, dat we door en door kennen</li><li>Eigen crew voor opbouw, show en afbouw</li><li>Licht en show door MATRIX E.I.L., ook uit de familie</li></ul>
    </div>
  </div>
</section>

<section class="section values">
  <div class="wrap two">
    <div>{eyebrow('04', 'Hoe we werken')}<h2 class="display reveal">Persoonlijk,<br><em>no-nonsense.</em></h2></div>
    <div>
      <p class="lead reveal">Persoonlijk contact, open communicatie en eerlijke samenwerking. Korte lijnen en een nuchtere aanpak. Een project moet bij ons niet alleen goed klinken of werken, het moet ook goed voelen.</p>
      <p class="reveal">Daarom kiezen we nooit voor een standaardoplossing, maar voor wat bij jouw event past. En voor licht en visuals werken we samen met <a href="{MATRIX}" target="_blank" rel="noopener">MATRIX E.I.L.</a>, het licht- en showbedrijf uit onze eigen familie. Zo blijft ook de nieuwste techniek in de familie.</p>
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
                body, image=cover, sectie='projecten.html')


# ---------------------------------------------------------------- Pagina per dienst en per event
EVENT_BY_ID = {e['id']: e for e in EVENTS}
DIENST_BY_SLUG = {d['slug']: d for d in DIENSTEN}
PROJ_BY_SLUG = {p['slug']: p for p in PROJECTEN}


def crumbs_ld(items):
    return {'@context': 'https://schema.org', '@type': 'BreadcrumbList', 'itemListElement': [
        {'@type': 'ListItem', 'position': i + 1, 'name': n, 'item': BASE + ('' if u == 'index.html' else u)} for i, (n, u) in enumerate(items)]}


def faq_ld(faq):
    return {'@context': 'https://schema.org', '@type': 'FAQPage', 'mainEntity': [
        {'@type': 'Question', 'name': q, 'acceptedAnswer': {'@type': 'Answer', 'text': a}} for q, a in faq]}


def proj_kaarten(slugs):
    return ''.join(f'''
      <a class="proj reveal" href="project-{p["slug"]}.html">
        <span class="proj-img"><img src="{cover_of(p)}" alt="{p["titel"]}" loading="lazy"></span>
        <span class="proj-meta">{p["plek"]} · {p["jaar"]}</span>
        <h3>{p["titel"]}</h3>
        <p>{p["sub"]}</p>
      </a>''' for p in (PROJ_BY_SLUG[s] for s in slugs))


def landing(soort, key):
    if soort == 'dienst':
        info, titel = DIENST_PAGINAS[key], DIENST_BY_SLUG[key]['titel']
        ouder, krijg, krijg_kop, type_q = ('Diensten', 'diensten.html'), info['krijg'], 'Wat je van ons krijgt', ''
        links = [(EVENT_PAGINAS[i]['pagina'], EVENT_BY_ID[i]['label'], EVENT_BY_ID[i]['kop']) for i in info['events']]
        links_kop, links_h2 = 'Voor welke events', 'Waar we dit<br><em>inzetten.</em>'
    else:
        info, titel = EVENT_PAGINAS[key], EVENT_BY_ID[key]['label']
        ouder, krijg, krijg_kop, type_q = ('Evenementen', 'evenementen.html'), EVENT_BY_ID[key]['regelen'], 'Dit regelen wij voor je', f'?type={key}'
        links = [(DIENST_PAGINAS[s]['pagina'], DIENST_BY_SLUG[s]['titel'], DIENST_BY_SLUG[s]['kort']) for s in info['diensten']]
        links_kop, links_h2 = 'Welke techniek', 'Alles uit<br><em>één hand.</em>'
    fotos = info['fotos']
    stappen = ''.join(f'<div class="lp-step reveal"><span class="step-nr">{i + 1:02d}</span><h3>{k}</h3><p>{t}</p></div>' for i, (k, t) in enumerate(info['aanpak']))
    rijen = ''.join(f'<a href="{u}"><b>{n}</b><span>{k}</span></a>' for u, n, k in links)
    faq = ''.join(f'<details class="reveal"><summary>{q}</summary><p>{a}</p></details>' for q, a in info['faq'])
    proj = f'''
<section class="section">
  <div class="wrap">
    <div class="sec-head row"><div>{eyebrow('04', 'Uit de praktijk')}<h2 class="display reveal">Zo zag het<br><em>eruit.</em></h2></div><a class="link-arrow reveal" href="projecten.html">Alle projecten</a></div>
    <div class="proj-grid{' two-up' if len(info['projecten']) > 1 else ' one-up'}">{proj_kaarten(info['projecten'])}
    </div>
  </div>
</section>''' if info['projecten'] else ''
    body = f'''<section class="pp-hero lp-hero">
  <img src="assets/img/{fotos[0]}" alt="" fetchpriority="high">
  <div class="wrap">
    <p class="crumb"><a href="{ouder[1]}">{ouder[0]}</a> / {titel}</p>
    <h1 class="display xl">{info["h1"]}</h1>
    <p class="pp-sub">{info["sub"]}</p>
    <div class="btns"><a class="btn fill" href="contact.html{type_q}">Vraag een offerte aan</a></div>
  </div>
</section>

<section class="section">
  <div class="wrap two">
    <div>{eyebrow('01', titel)}<p class="lead reveal">{info["intro"]}</p></div>
    <div class="lp-box reveal"><p class="pane-label">{krijg_kop}</p><ul class="checks">{"".join(f"<li>{k}</li>" for k in krijg)}</ul></div>
  </div>
</section>

<section class="section dark">
  <div class="wrap">
    <div class="sec-head">{eyebrow('02', 'Onze aanpak')}<h2 class="display reveal">Zo zorgen we<br><em>dat het klopt.</em></h2></div>
    <div class="lp-steps">{stappen}</div>
  </div>
</section>

<div class="lp-strip" aria-hidden="true">{"".join(f'<img src="assets/img/{f}" alt="" loading="lazy">' for f in fotos[1:])}</div>

<section class="section">
  <div class="wrap two">
    <div>{eyebrow('03', links_kop)}<h2 class="display reveal">{links_h2}</h2></div>
    <nav class="lp-links reveal" aria-label="{links_kop}">{rijen}</nav>
  </div>
</section>
{proj}
<section class="section faq">
  <div class="wrap two">
    <div>{eyebrow('?', 'Vragen over ' + titel.lower())}<h2 class="display reveal">Goed om<br><em>te weten.</em></h2></div>
    <div class="faq-list">{faq}</div>
  </div>
</section>

{cta_band()}'''
    ld = [ORG, crumbs_ld([('Home', 'index.html'), ouder, (titel, info['pagina'])]), faq_ld(info['faq'])]
    if soort == 'dienst':
        ld.append({'@context': 'https://schema.org', '@type': 'Service', 'name': titel, 'serviceType': titel, 'description': info['seo'][1],
                   'provider': {'@id': BASE + '#gtf'}, 'areaServed': ORG['areaServed'], 'url': BASE + info['pagina']})
    return page(info['pagina'], info['seo'][0], info['seo'][1], body, ld=ld, image=f'assets/img/{fotos[0]}',
                sectie=ouder[1])


def evenementen():
    kaarten = ''.join(f'''
      <a class="proj big reveal" href="{EVENT_PAGINAS[e["id"]]["pagina"]}">
        <span class="proj-img"><img src="assets/img/{e["img"]}" alt="{e["label"]}" loading="lazy"></span>
        <span class="proj-meta">{EVENT_PAGINAS[e["id"]]["sub"]}</span>
        <h3>{e["label"]}</h3>
        <p>{e["kop"]}</p>
      </a>''' for e in EVENTS)
    body = f'''<section class="page-hero">
  <div class="wrap">
    {eyebrow('—', 'Evenementen')}
    <h1 class="display xl reveal">Elk event<br><em>z’n eigen aanpak.</em></h1>
    <p class="lead reveal">Een bruiloft vraagt iets anders dan een schuttersfeest, en een congres iets anders dan een festival. Kies wat je organiseert en zie hoe we het aanpakken.</p>
  </div>
</section>
<section class="section" style="padding-top:0">
  <div class="wrap"><div class="proj-grid">{kaarten}
  </div></div>
</section>
{cta_band()}'''
    return page('evenementen.html', 'Evenementen | Techniek voor elk soort event | GTF Franzen',
                'Geluid, licht, omroep en stroom voor festivals, dorpsfeesten, carnaval, bruiloften, bedrijfsevents, jubilea en schuttersfeesten in Limburg en omgeving.',
                body, dark_header=False, ld=[ORG, crumbs_ld([('Home', 'index.html'), ('Evenementen', 'evenementen.html')])])


def werkgebied():
    import math
    lon0, lat0 = PLAATSEN[0][1], PLAATSEN[0][2]
    km = lambda lon, lat: ((lon - lon0) * 111.3 * math.cos(math.radians(lat0)), (lat0 - lat) * 111.3)
    # Wortelschaal: dichtbij krijgt meer ruimte, zodat de plaatsen rond Bocholtz leesbaar blijven
    straal = lambda d: 320 * math.sqrt(d / 50)
    cx, cy = 420, 380
    ringen = ''.join(f'<circle cx="{cx}" cy="{cy}" r="{straal(r):.0f}"/><text x="{cx + 6}" y="{cy - straal(r) - 8:.0f}" class="r-lbl">{r} km</text>' for r in (5, 15, 50))
    punten = ''
    for i, (n, lon, lat, land) in enumerate(PLAATSEN):
        dx, dy = km(lon, lat)
        d = math.hypot(dx, dy) or 1
        x, y = cx + dx / d * straal(d), cy + dy / d * straal(d)
        if i == 0:
            continue
        rechts = x < cx + 230 and n not in ("Kerkrade", "Valkenburg", "Maastricht")
        punten += f'<g class="pt {land.lower()}"><circle cx="{x:.0f}" cy="{y:.0f}" r="5"/><text x="{x + (10 if rechts else -10):.0f}" y="{y + 5:.0f}"{"" if rechts else " text-anchor=\"end\""}>{n}</text></g>'
    kaart = f'''<svg class="map" viewBox="0 0 840 740" role="img" aria-label="Werkgebied rond Bocholtz, met plaatsen in Nederland, België en Duitsland">
      <g class="rings">{ringen}</g>{punten}
      <g class="home"><circle cx="{cx}" cy="{cy}" r="14"/><circle cx="{cx}" cy="{cy}" r="26" class="pulse"/><text x="{cx}" y="{cy + 48}" text-anchor="middle">BOCHOLTZ</text></g>
    </svg>'''
    lijst = lambda land: ', '.join(n for n, _, _, l in PLAATSEN if l == land)
    body = f'''<section class="page-hero">
  <div class="wrap">
    {eyebrow('—', 'Werkgebied')}
    <h1 class="display xl reveal">Vanuit Bocholtz<br><em>de hele regio in.</em></h1>
    <p class="lead reveal">Bocholtz ligt precies op het drielandenpunt. Daardoor zitten we net zo snel in Aken of Kelmis als in Heerlen of Maastricht. We werken in heel Zuid-Limburg, de rest van Nederland, België en Duitsland.</p>
  </div>
</section>
<section class="section" style="padding-top:clamp(40px,6vw,80px)">
  <div class="wrap two">
    <div class="map-wrap reveal">{kaart}<p class="map-legend"><span class="nl">Nederland</span><span class="be">België</span><span class="de">Duitsland</span></p></div>
    <div>
      {eyebrow('01', 'Waar we werken')}
      <h2 class="display reveal">Drie landen,<br><em>één familie.</em></h2>
      <div class="regio reveal"><h3>Zuid-Limburg</h3><p>{lijst("NL")} en omgeving. Hier zijn we thuis en kennen we de zalen, tenten, sportvelden en verenigingen.</p></div>
      <div class="regio reveal"><h3>België</h3><p>{lijst("BE")} en de rest van Belgisch Limburg en de Oostkantons.</p></div>
      <div class="regio reveal"><h3>Duitsland</h3><p>{lijst("DE")} en de rest van de regio Aken.</p></div>
      <p class="reveal">Verder weg? Ook dan kijken we graag wat er mogelijk is. Voor grotere producties rijden we door heel Nederland.</p>
      <a class="btn fill reveal" href="contact.html">Vraag een offerte aan</a>
    </div>
  </div>
</section>
{cta_band()}'''
    return page('werkgebied.html', 'Werkgebied | Eventtechniek in Zuid-Limburg, België en Duitsland | GTF Franzen',
                'GTF Franzen uit Bocholtz levert geluid, licht, omroep en stroom in Zuid-Limburg (Heerlen, Kerkrade, Maastricht, Valkenburg), België (Kelmis, Eupen) en Duitsland (Aken).',
                body, dark_header=False, ld=[ORG, crumbs_ld([('Home', 'index.html'), ('Werkgebied', 'werkgebied.html')])])


# ---------------------------------------------------------------- Contact
def contact():
    actie = 'https://api.web3forms.com/submit' if FORM_KEY else f'mailto:{MAIL}'
    body = f'''<section class="page-hero contact-hero">
  <div class="wrap two">
    <div>
      {eyebrow('—', 'Offerte & contact')}
      <h1 class="display xl reveal">Jouw event<br><em>start hier.</em></h1>
      <p class="lead reveal">Vertel ons wat je van plan bent. Je hoeft nog niet alles te weten, daar helpen we je juist bij. Je krijgt snel een persoonlijke reactie van de familie.</p>
      {contact_list()}
    </div>
    <form class="quote-form reveal" data-mail="{MAIL}" data-key="{FORM_KEY}" action="{actie}" method="post">
      <input type="checkbox" name="botcheck" class="hp" tabindex="-1" autocomplete="off" aria-hidden="true">
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
    built = [home(), diensten(), *[landing('dienst', d['slug']) for d in DIENSTEN], evenementen(), *[landing('event', e['id']) for e in EVENTS],
             projecten(), *[project(p) for p in PROJECTEN], over(), werkwijze(), werkgebied(), contact(), privacy(), notfound()]
    sitemap(built)
    print('Gebouwd:', ', '.join(built))
