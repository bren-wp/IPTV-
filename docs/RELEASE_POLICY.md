# IPTV+ — jedan proizvod, četiri instalacijske datoteke

**Više nema Free i Pro verzija.** Jedan IPTV+ s uključenim svim postojećim naprednim clubTivi mogućnostima i Android identifikatorom `com.brendigo.iptvplus`.

Za svaki `vX.Y.Z` Release zahtijeva:

1. `IPTV-Plus-vX.Y.Z.apk` — potpisani Android APK
2. `IPTV-Plus-vX.Y.Z.aab` — potpisani Android App Bundle
3. `IPTV-Plus-vX.Y.Z-Portable.exe` — Windows bez instalacije
4. `IPTV-Plus-vX.Y.Z-Setup.exe` — Windows NSIS instalacija

Uz `SHA256SUMS.txt`, `IPTV-Plus-vX.Y.Z-Branding.zip` i `RELEASE-NOTES.md`. Nikad ne objavljuj djelomični release, placeholder ili neprovjereni APK/AAB.

## Trajni ključ i GitHub Secrets

Potrebna su samo **četiri** privatna Repository secrets:

- `IPTV_ANDROID_KEYSTORE_BASE64`
- `IPTV_ANDROID_STORE_PASSWORD`
- `IPTV_ANDROID_KEY_PASSWORD`
- `IPTV_ANDROID_KEY_ALIAS`

Postavi ih u GitHub → Settings → Secrets and variables → Actions → New repository secret. Ne objavljuj privatne ključeve, keystore ni lozinke u chatu, issueu ili repozitoriju. Bez tajni automatski release se jasno preskače, a ručno zatraženi release završava pogreškom.

## Uvjeti

Nakon povećanja `package.json` i `src-tauri/tauri.conf.json` na novu verziju, GitHub Actions mora dovršiti Flutter testove, stvarni Android release i provjere potpisa oba Android paketa, Windows Portable+Setup izgradnju, validaciju četiri strukturalno prepoznatljive datoteke i SHA-256. Izdanje je `prerelease` dok fizički uređaji i potpuni sigurnosni/visual QA nisu dokumentirani.

**Novi Android package ID nije automatska nadogradnja nekadašnjih `.free` i `.pro` aplikacija.** Ako su već na Play Storeu, prijelaz zahtijeva zaseban plan migracije. Windows EXE preporučuje se potpisati code-sign certifikatom.

Branding ZIP sadrži svih 39 SVG koncepata iz `assets/screens` i originalne ikone. To nisu stvarne snimke zaslona izgrađene aplikacije. Prava na ponuđene streamove i njihove logotipe/EPG provjeravaju se zasebno; premium Arena Sport nije uključen bez autorizacije.

Dodatno: [Ovisnosti](DEPENDENCIES.md) · [Arhitektura](ENGINE_MIGRATION.md).
