# IPTV+ — razvojni plan

## Implementirano u početnoj osnovi v0.1.0
- Tauri 2 + React + TypeScript dijeljena kodna baza (Android/Windows cilj).
- IPTV+ logo, SVG markentiški vizuali, responsive početni dizajn, 10 navigacijskih ekrana.
- Regionalni filteri HR/SI/BA/RS, kategorije, pretraživanje i favoriti.
- M3U uvoz s osnovnom validacijom te HTML5/hls.js reproduktor.
- Free/Pro **besplatni** način rada bez registracije i reklama; Pro trenutačno uključuje više lista i više favorita.
- Jedinični testovi parsera i GitHub Actions frontend CI.

## Sljedeće (nije implementirano)
### Faza 1 — stvarna funkcionalnost
- Stabilan provjeren Android i Windows build sa stvarnim ikonama, lockfileom i potpisivanjem.
- M3U URL uvoz, sigurna lokalna pohrana, osvježavanje i otkrivanje promjena.
- XMLTV EPG, kategorije VOD-a, resume, zvuk/titlovi, TV podrška, HLS stream fallback.
- Jasna prava pristupa legalnom katalogu iz službenih javnih izvora.

### Faza 2 — dovršavanje UX-a
- Produkcijski Android TV 10-foot UI s D-pad i EPG grid navigacijom.
- Izvori, favoriti i povijest uz sinkronizaciju lokalno ili eksplicitnom korisničkom radnjom.
- Lokalizacija: HR, SL, BS, SR, EN; roditeljska kontrola; pristupačnost.
- Uređivanje skupina, inteligentno pretraživanje i popisi za gledanje.

### Faza 3 — Pro i izdanja
- Napredni player i profili, snimanje samo ako je dopušteno, PiP i legalni catch-up.
- QA na fizičkim Android uređajima, Android TV i Windows 10/11.
- Security + dead code audit, provjera licenci ovisnosti, reproducibilni buildovi.
- Potpisani APK/AAB, Portable.exe i Setup.exe kroz provjerena GitHub izdanja.

Samo prolazak buildova, reprodukcijskih testova i licencne provjere opravdava oznaku produkcijskog izdanja.
