# Javni GitHub izvori u IPTV+

## Što je implementirano

Aplikacija sadrži direktorij poznatih **vanjskih** GitHub javnih IPTV zbirki u `src/publicSources.ts`. Korisnik bira koju želi aktivirati. Aktivirani izvori preuzimaju se na uređaj, filtriraju po državi i kategoriji i periodički osvježavaju dok je aplikacija otvorena. Pohranjuju se **samo odabrani identifikatori izvora**, ne osjetljivi podaci ni redistribuirani video.

### Direktoriji

| Projekt | Podržane liste | Politika |
|---|---|---|
| [Doubo Public Channel Directory](https://github.com/streamline-iptv/iptv-playlists) | HR / BiH / RS | Filtriranje po domeni službenog emitera; CC BY 4.0 za izbor poveznica, ne za video |
| [iptv-org/iptv](https://github.com/iptv-org/iptv) | HR / SI / BiH / RS | Javno dopunjavana zajednička zbirka; prava pojedinog streama neprovjerena |
| [biskyt/legalFreeIPTVplaylist](https://github.com/biskyt/legalFreeIPTVplaylist) | Live / filmovi / serije | Objavljuje pravne podloge; oprez kod filmova jer trajanje autorskih prava nije isto u svakoj državi |

## Ograničenja

- Prisutnost URL-a na GitHubu **nije** licenca za emitiranje, reemitiranje ili uključivanje u službeni IPTV+ katalog.
- Ove liste su **izbor vanjskih izvora na zahtjev korisnika**, a ne unaprijed uključeni IPTV+ premium programi.
- Nikada se ne kopiraju tuđi DRM tokeni, naplatne vjerodajnice ili zaobilazi geoblokada.
- Imena jasno poznatih premium kanala poput Arena Sport namjerno se izostavljaju iz automatski učitanih javnih zbirki. To nije pravna provjera svih preostalih kanala.
- Izvorni GitHub projekt i njegov kredit prikazani su u aplikaciji.
- Preglednik/WebView i CORS mogu ograničiti dohvat nekih lista; u takvom slučaju prikazuje se pogreška, bez skrivenog proksiranja.
- IPTV+ ne jamči trajnu dostupnost ni reproducibilnost streama.

## Prije objave unaprijed uključenog kataloga

Za kanale koji se prikazuju pri prvom otvaranju *bez korisničke aktivacije izvora*, pravila su stroža: potreban je potvrđen legalni izvor, prava na korištenje loga, upis dokaza u `public/catalog/approved.json` i periodički audit. Trenutačno je službeni manifest prazan.

## Licenca i atribucija

*Doubo Public Channel Directory* distribuciju odabira poveznica navodi pod CC BY 4.0. IPTV+ sadrži izričitu atribuciju projekta i njegovu poveznicu, ali ta licenca ne daje prava na video. `iptv-org` i `biskyt` ostaju neovisni izvori.
