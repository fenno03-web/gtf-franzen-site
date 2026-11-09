# GTF Franzen website

Statische website (HTML/CSS/JS) voor GTF Franzen, Sound - Light - Vision. Gehost via GitHub Pages. In het Nederlands, Duits (`de/`) en Engels (`en/`).

Pagina's worden gebouwd met `python3 build.py`. Pas teksten en gegevens aan in `build.py`, niet in de HTML-bestanden.

- `build.py`: alle inhoud per taal (diensten, projecten, verhuurcatalogus, nieuws, FAQ), de gedeelde header en footer, structured data, hreflang, sitemap en doorverwijzingen van oude adressen
- `assets/css/site.css`: alle opmaak
- `assets/js/site.js`: menu, hero-diavoorstelling, inschuiven en contactformulier (opent een mail aan het algemene adres)
- `assets/foto/`: beelden en het logo

## Nieuws toevoegen

Voeg een item toe aan `NIEUWS` in `build.py` (titel, korte tekst en alinea's per taal, plus een foto) en draai `python3 build.py`.

## Nog aan te vullen

- `TEL` bovenaan `build.py`. Lege velden worden niet getoond.
- Foto's van ZLF, BVV Kalk aan de Books en CV De Pankes (nu een logo als plaatshouder)
- Eigen domein: zet `BASE` in `build.py` en voeg een `CNAME`-bestand toe
