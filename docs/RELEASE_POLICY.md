# IPTV+ — jedinstvena aplikacija, nepotpisana razvojna izdanja

IPTV+ je jedna aplikacija s uključenim naprednim funkcijama. U GitHub CI-u nisu potrebni privatni Android signing ključevi niti GitHub Actions Secrets.

## Četiri obvezne datoteke

- `IPTV-Plus-vX.Y.Z-Unsigned.apk` — **nepotpisani razvojni APK**; Android odbija instalaciju
- `IPTV-Plus-vX.Y.Z-Unsigned.aab` — **nepotpisani razvojni AAB**; Google Play odbija prijenos
- `IPTV-Plus-vX.Y.Z-Portable.exe` — Windows bez instalacijskog postupka
- `IPTV-Plus-vX.Y.Z-Setup.exe` — Windows NSIS instalacija

Release također uključuje SHA256SUMS, marketinški Branding ZIP i RELEASE-NOTES. Windows EXE nisu Authenticode potpisani.

**VAŽNO:** Nijedna potpuno nepotpisana Android aplikacija ne može se instalirati. Za funkcionalni APK na uređaju i AAB za Google Play kasnije je nužno potpisivanje, čak i kada se koristi besplatni lokalno generirani certifikat. Nemoj nepotpisane datoteke predstavljati kao instalacijske pakete.

Workflow ne koristi `sign_flutter_android.py`, ne provjerava Secrets i ne koristi privatne ključeve. Provjerava da Android APK nije potpisan te da je AAB bez JAR potpisa. Izdaje samo razvojni prerelease ako su svi paketi stvarno izgrađeni; ne stvara prazne ili lažne datoteke. Izvorni APK/AAB paketni ID je `com.brendigo.iptvplus`, različit od starih Free/Pro instalacija.

## Provjere

Flutter testovi, nativna Android i Windows izgradnja, sadržaj arhiva, četiri paketa, SHA-256. Fizčki Android/Windows/Android TV QA obvezan je prije bilo kakve tvrdnje o produkcijskoj spremnosti.

Brending: 39 SVG konceptnih prikaza i vlastite ikone. Prava TV sadržaja, slika i EPG-a uvijek se provjeravaju odvojeno.

[Ovisnosti](DEPENDENCIES.md)
