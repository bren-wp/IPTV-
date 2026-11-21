# IPTV+ — jedinstveni Flutter/clubTivi engine

Flutter verzija clubTivi (Apache 2.0, pinned submodule) glavni je player za Android, Android TV i Windows. Tauri/React ostaje prototip. Jedno izdanje s Android ID `com.brendigo.iptvplus` i `FeatureGate.setTier(AppTier.pro)` uklanja Free/Pro podjelu i njezina ograničenja. To ne uključuje pretplate na TV sadržaj.

`tools/clubtivi/prepare.py` primjenjuje IPTV+ ikonu, splash, teme, početnu stranicu, TV navigaciju, regionalne izvore i sigurnu provjeru GitHub izdanja. `assets/screens/` sadrži 39 vizualnih koncepata za 3 platforme (nisu screenshots).

`.github/workflows/verified-release.yml` gradi jedan APK, AAB, Portable.exe i Setup.exe te provjerava potpise i strukturnu valjanost paketa. Dovoljan je **jedan trajni** Android signing key (četiri GitHub Secrets). Prvi objedinjeni cilj je verzija `0.2.0`.

Sljedeće faze: svi zasloni 1:1 prema referencama, kvaliteta reprodukcije/EPG-a i M3U izvora, D-pad i safe-area testovi, puni security/dead code audit, sigurnost lozinki i dopuštenja sadržaja te fizički uređaji. Stari Free/Pro app ID-ovi ne mogu se izravno nadograditi na novi.
