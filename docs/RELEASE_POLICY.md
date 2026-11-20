# IPTV+ — pravila svakog izdanja

## Obavezne datoteke (8)
Za svaki `vX.Y.Z`:
```
IPTV-Plus-vX.Y.Z-Free.apk
IPTV-Plus-vX.Y.Z-Free.aab
IPTV-Plus-vX.Y.Z-Free-Portable.exe
IPTV-Plus-vX.Y.Z-Free-Setup.exe
IPTV-Plus-vX.Y.Z-Pro.apk
IPTV-Plus-vX.Y.Z-Pro.aab
IPTV-Plus-vX.Y.Z-Pro-Portable.exe
IPTV-Plus-vX.Y.Z-Pro-Setup.exe
SHA256SUMS.txt
IPTV-Plus-vX.Y.Z-Branding.zip
RELEASE-NOTES.md
```

## Obavezan release gate
**Ne objavljuj GitHub Release** dok obje verzije Android APK/AAB nisu stvarno potpisane, obje Windows varijante nisu izgrađene, sve osam datoteka ne postoje i kontrolni zbrojevi nisu generirani. Nikad ne zamjenjuj datoteke praznim placeholderima. Workflow služi za automatsku provjeru i publish tek nakon uspjeha.

## Priprema privatnih GitHub Secrets
Potrebni su trajni, privatni upload ključevi. **Nikad se ne commitaju u repo.** Za Free i Pro odvojeno postavi u GitHub Actions Secrets:

- `IPTV_FREE_KEYSTORE_BASE64`, `IPTV_FREE_STORE_PASSWORD`, `IPTV_FREE_KEY_PASSWORD`, `IPTV_FREE_KEY_ALIAS`
- `IPTV_PRO_KEYSTORE_BASE64`, `IPTV_PRO_STORE_PASSWORD`, `IPTV_PRO_KEY_PASSWORD`, `IPTV_PRO_KEY_ALIAS`

Za Google Play treba sačuvati isti signing ključ za sva iduća izdanja iste aplikacije. Izgubljeni ključevi mogu onemogućiti nastavak izdavanja. Potreban je odgovarajući Google Play App Signing proces.

Windows potpisi (.exe) dodatna su tema: `Setup.exe` i `Portable.exe` mogu se pokrenuti bez potpisa, ali za SmartScreen povjerenje i profesionalno izdanje preporučen je code-sign certifikat i autentikacijska provjera potpisa. Windows 'Portable' znači bez instalacije putem setupa, ali WebView2 može biti preduvjet, a lokalne postavke trenutačno nisu potpuno izolirane uz exe.

## Kada i kako se izdaje
- **Svako prihvaćeno razvojno izdanje** povećava verziju u `package.json` i `src-tauri/tauri.conf.json`, ažurira changelog, slike i docs.
- Push/merge na `main` ili ručni `workflow_dispatch` pokreće 4 nativna posla: Android Free/Pro i Windows Free/Pro.
- `validate_artifacts.py` provjerava osnovnu strukturu i prisutnost svih 8 paketa; Android build dodatno provjerava digitalne potpise.
- Tek nakon svih zelenih jobova paket se objavljuje kao **novi** GitHub Release s novom verzijom.
- Ako potrebni ključevi nedostaju, ako je build neispravan ili je neka datoteka neprisutna, Release se **ne smije objaviti**; ostaje CI neuspjeh koji zahtijeva popravak.

## Vizualna isporuka
- `assets/brand/`: primarni logo i izvorne ikone.
- `assets/screens/android/`: svih 13 Android koncept ekrana.
- `assets/screens/windows/`: svih 13 Windows koncept prozora.
- `assets/screens/android-tv/`: svih 13 Android TV koncept ekrana.
- `assets/previews/`: marketing banner i overview.
- U svakom izdanju paket `Branding.zip` uključuje sve te izvorne vektorske grafike.
- **SVG koncept nije isto što i screenshot stvarne aplikacije.** Prije stvarnog produkcijskog izdanja nužne su snimke aplikacije na fizičkim uređajima i usporedba s konceptom.

## Zakonito unaprijed uključeni izvori
Korisnik treba moći odabrati kanal bez ručnog dodavanja liste, ali samo za izvore za koje imamo dokazano dopuštenje. Trenutačni `public/catalog/approved.json` prazan je dok taj uvjet nije ispunjen. Premium Arena Sport i sličan sadržaj nije uključен bez prava.
