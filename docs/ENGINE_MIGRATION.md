# IPTV+ — odluka o glavnom engineu i fazna migracija

**Odluka:** Flutter izvedba projekta clubTivi, Apache 2.0, glavni je cilj za IPTV+ Android, Android TV i Windows. Tauri/React projekt ostaje razvojna referenca i rezervna varijanta; **nije** glavna baza za nove produkcijske binarne datoteke.

## Struktura
- `vendor/clubTivi` — zaključani originalni Flutter engine; bez direktnih ručnih promjena na upstream repozitoriju
- `tools/clubtivi/prepare.py` — ponovljiv overlay: naziv, boje, Free/Pro, izvorne IPTV+ ikone, regionalni direktorij, početni zaslon
- `tools/clubtivi/iptv_plus_home.dart` — autorski IPTV+ početni zaslon s funkcionalnom navigacijom
- `tools/clubtivi/iptv_plus_home_test.dart` — Flutter widget test početne stranice
- `assets/screens/` — 39 vizualnih koncepata kao QA specifikacija, **ne** potvrđeni screenshotovi
- `.github/workflows/verified-release.yml` — Flutter Android + Windows osam paketa (Free/Pro APK, AAB, Portable.exe, Setup.exe)
- `src/` i `src-tauri/` — stariji Tauri prototip za usporedbu dizajna i razvojnu rezervu

## Faze
1. **Faza A — osnovna migracija:** clubTivi kao Flutter engine, IPTV+ home, Free/Pro identitet, regionalni popis izvora, očuvane licence; CI widget testovi.
2. **Faza B — stabilan nativni build:** Android Free/Pro i Windows Free/Pro, potpuni Flutter Windows bundle u samostalni Portable.exe i NSIS Setup.exe, trajni Android ključevi.
3. **Faza C — puni IPTV+ UI:** svi zasloni prema 39 odobrenih koncepta, stvarna navigacija D-pad, mobilni safe areas, uključivo loading/error/empty/EPG/player stanja.
4. **Faza D — medijski sustav:** EPG/XMLTV, M3U/Xtream, više izvora, smart channel failover, autorizirane liste, performanse, sigurnost i lokalizacije.
5. **Faza E — produkcijski QA:** fizički uređaji, pravo korištenja programa, prijave i licence, sigurnost pohrane vjerodajnica, full dead code/security audit, potpis i verzionirana izdanja.

## Izdavanje i ograničenja

Svaka nova verzija treba osam ispravnih nativnih datoteka. GitHub workflow **ne objavljuje ništa** ako paket nije izgrađen ili APK/AAB nije potpisan; uspješan CI ne potvrđuje nužno funkcionalnost na svim uređajima. Automatska izdanja označena su `prerelease` dok produkcijski QA ne bude dokumentiran.

Windows Flutter aplikacija treba kompletnu mapu runnera. **Portable.exe sadrži puni Windows bundle** i privremeno ga raspakira u sistemsku privremenu mapu, pokrene aplikaciju te pokušava ukloniti datoteke po zatvaranju. Time nije potreban Setup, ali postavke Flutter enginea mogu se pohranjivati u korisnički profil. Jednostavno preimenovanje `iptvplus.exe` iz runnera **ne bi** bilo ispravno portable izdanje.

Free i Pro imaju različite Android package ID-ove i ugrađena feature-gate pravila. Broj Android verzije računa se monotono iz semantičke verzije kako Google Play update ne bi bio blokiran.

## Prava na kanale

Direktoriji GitHub lista ne jamče pravo korištenja sadržaja. Za unaprijed ponuđene kanale bez korisnikove aktivacije trebaju dokazi dozvole. Arena Sport i slični plaćeni sadržaji nisu uključeni bez autorizacije. Izbor javnog M3U izvora i otvorenost URL-a nisu pravna potvrda.

## Koraci za reviziju
- Pokrenuti `clubtivi-smoke.yml` za oba izdanja.
- Pokrenuti `flutter-native-smoke.yml` na Windows runneru i Android emulatoru/runneru; provjeriti pakete.
- Izraditi i odobriti **stvarne** snimke svakog ekrana uz usporedbu s konceptom.
- Postaviti tajne za Google Play upload ključeve, bez iznošenja u javni repozitorij.

## Sigurno ažuriranje Free/Pro izdanja

U clubTivi izvedbi IPTV+ provjerava izdanja na `bren-wp/IPTV-`, a ne na izvornom clubTivi računu. Pri prikazu nove verzije može ponuditi samo APK namijenjen odgovarajućem Free ili Pro izdanju; preuzimanje/instalacija ne obavljaju se automatski. Korisnik otvara službenu GitHub stranicu izdanja u vanjskom pregledniku. Uklonjen je prethodni Flutter/Android kod za sideloadanje APK-ova (`MethodChannel`, `FileProvider`, `REQUEST_INSTALL_PACKAGES`). To uklanja nepotrebno dopuštenje i izbjegava automatsko preskakanje pravila distribucije u trgovinama aplikacija.

Flutter/Android alatni lanac zaključan je na Flutter 3.50.1, Gradle 9.5.0, AGP 9.3.1 i Kotlin 2.4.20. Za kompatibilnost starih Flutter dodataka privremeno su uključene `android.newDsl=false` i `android.builtInKotlin=false`. Te postavke treba ukloniti kada svi dodaci budu spremni za novi DSL.
