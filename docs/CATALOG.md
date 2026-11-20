# IPTV+ — ugrađeni katalog i prava streamanja

## Korisnički cilj
Korisnik otvori IPTV+, odabere Hrvatsku / Sloveniju / BiH / Srbiju, kategoriju, kanal i pritisne **Gledaj**. Nema IPTV+ registracije, reklama ni obveznog M3U unosa.

## Trenutačno stanje
Automatski javni katalog **još nije napunjen ni priključen na produkcijski player**. `public/catalog/approved.json` je kontrolirani prazan početni manifest. To znači da IPTV+ ne smije obećavati besplatni pristup Arena Sport kanalima, drugim premium TV sadržajima ili streamovima za koje nemamo pisanu dozvolu.

## Pravila za svaki novi kanal
1. Naziv, zemlja, vrsta sadržaja i službena adresa emitera.
2. URL streama i dopuštenje za ugradnju u IPTV+ (poveznica na uvjete ili pisana dozvola).
3. Dozvoljena područja gledanja, tokeni, DRM, geo-ograničenja i ograničenja broja streamova.
4. Prava na logo, slike i EPG provjeravaju se zasebno.
5. Automatizirani provjerivač testira zdravlje izvora bez zaobilaženja DRM-a ili ograničenja.
6. Prava se evidentiraju, datiraju i periodično ponovo provjeravaju prije uključivanja u izdanje.

Sama dostupnost streama u javnoj M3U listi nije dovoljna za ugradnju u službeni IPTV+ katalog.
