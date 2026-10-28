# GTF Franzen website

Statische website (HTML/CSS/JS) voor GTF Franzen, Sound | Light | Vision. Gehost via GitHub Pages.

Pagina's worden gebouwd met `python3 build.py`. Pas teksten en gegevens aan in `build.py`, niet in de HTML-bestanden.

- `build.py`: alle inhoud (diensten, events, tijdlijn, projecten, FAQ) en de gedeelde header en footer
- `assets/css/style.css`: alle opmaak
- `assets/js/main.js`: menu, event-kiezer, fotogalerij en offerteformulier
- `assets/img/`: beelden

## Nog aan te vullen

- Contactgegevens bovenaan `build.py` (`TEL`, `ADRES`, `KVK`, socials). Lege velden worden niet getoond. Het offerteformulier mailt naar `MAIL`.
- Logo van GTF Franzen (nu een tijdelijk woordmerk)
- Eventueel portretten van Leon en Fenno
- Meer projecten en eventueel klantreacties
- Eigen domein: zet `BASE` in `build.py` en voeg een `CNAME`-bestand toe
