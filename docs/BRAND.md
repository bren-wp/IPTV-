# IPTV+ — brend i kompletna matrica ekrana

## Pozicioniranje
**IPTV+ — Televizija po tvome.** Jednostavna, brza i vizualno usklađena aplikacija za osobne, legalne IPTV izvore. Bez registracije ili reklamnih SDK-ova. Primarni katalog: Hrvatska, Slovenija, Bosna i Hercegovina, Srbija.

## Osnovni identitet
| Token | Vrijednost |
|---|---|
| Pozadina | `#080D1C` |
| Kartice | `#111A2C` |
| Istaknuti tekst | `#EEF1FF` |
| Sekundarni tekst | `#8897B5` |
| Glavna boja | `#7C5CFF` |
| Akcent | `#27D3C3` |
| Opasnost | `#FFB9C9` |
| Radius kartice | 14–18 px |
| Raster | 8 px, veći razmaci 16–32 px |
| Tipografija | Sistem + fallback font; ikone Lucide |

Logo je vlastiti vektorski simbol televizora i Play znaka s prepoznatljivim `+`. Grafike se nalaze u `assets/brand/`. SVG dokumentacija i koncepti ne tvrde da su snimke produkcijskog builda.

## Potpuna matrica ekrana i stanja

| Ekran | Mobile | Android TV | Windows | Stanje u v0.1 |
|---|---|---|---|---|
| Splash / uvodni ekran | Planirano | Planirano | Planirano | Brand asset postoji |
| Početna / hero / kategorije | ✔ | Responzivni pregled | ✔ | UI |
| TV uživo | ✔ | Fokus i tipkovničke kontrole | ✔ | UI + M3U korisnički unos |
| Video reproduktor | ✔ | Osnovne kontrole | ✔ | HLS/HTML5 osnovno |
| TV vodič (EPG) | ✔ | Pregled | ✔ | Ilustrativni raspored |
| Filmovi / VOD | ✔ | Pregled | ✔ | Filtriranje M3U oznaka |
| Serije | ✔ | Pregled | ✔ | Filtriranje M3U oznaka |
| Dječji sadržaj | ✔ | Pregled | ✔ | Filtriranje M3U oznaka |
| Favoriti | ✔ | ✔ | ✔ | Spremanje ID-ova lokalno |
| Pretraživanje | ✔ | ✔ | ✔ | Tekstualna pretraga |
| Države HR/SI/BA/RS | ✔ | ✔ | ✔ | Filteri i pregled |
| Izvori / M3U datoteka | ✔ | Planirana TV optimizacija | ✔ | Lokalni import |
| Xtream Codes | Planirano | Planirano | Planirano | Nije ugrađeno |
| URL / periodični refresh | Planirano | Planirano | Planirano | Nije ugrađeno |
| Postavke izgleda i Pro | ✔ | ✔ | ✔ | Funkcionalno |
| Izbor jezika HR/SL/BS/SR/EN | Planirano | Planirano | Planirano | Samo HR |
| Roditeljska kontrola/PIN | Planirano | Planirano | Planirano | Nije ugrađeno |
| Snimanje / catch-up / PiP | Planirano | Planirano | Planirano | Nije ugrađeno |
| Sigurna pohrana credencijala | Planirano | Planirano | Planirano | Nije ugrađeno |
| Legalni katalog + automatska prava | Planirano | Planirano | Planirano | Nije ugrađeno |

## Rasporedi
- **Mobile ≤620 px:** naslovna traka, 2–3 kolone sadržaja, donja navigacija, safe-area odmak, dodirne mete ≥44 px za ključne kontrole.
- **Tablet 621–890 px:** kompaktni bočni meni, dvije kolone TV kartica, prošireni prikaz.
- **Windows ≥891 px:** sidebar 244 px, kartice 3–4 u redu, lokalni modal player, tipkovnica + miš.
- **TV:** ista React struktura može poslužiti kao početni pregled; produkcijski fokus, D-pad, overscan, 10-foot UI i pravi Android TV build zahtijevaju zasebna fizička testiranja.
- Minimalni kontrast, `prefers-reduced-motion`, `:focus-visible`, jasna stanja pogreške, prazno stanje, stanje učitavanja i prekida streama.

## UI komponente
`Sidebar`, `Topbar`, `Hero`, `CategoryTile`, `RegionTile`, `ChannelTile`, `VideoPlayer`, `GuideGrid`, `SourcesPanel`, `SettingsPanel`, `BottomNav`, `EmptyState`, `Notice`.

## Pravila izvedbe
1. Bez dev-placeholder tekstova u produkcijskim izdanjima. Svi trenutačni demonstracijski prikazi **jasno su označeni**.
2. Isti dizajnerski tokeni na svim uređajima, ali platformi primjereni rasporedi.
3. Nema reklamnog SDK-a, obveznog računa, skrivenog servisa ili uvezenih piratskih lista.
4. Ne nazivati dizajnerske koncepte snimkama aplikacije.
5. Svaki merge zahtijeva vizualni QA na 360×800, 412×915, 1280×800, 1920×1080 i Android TV.
