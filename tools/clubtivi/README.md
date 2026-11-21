# IPTV+ — jedna aplikacija s clubTivi engineom

Primarni engine: Apache-2.0 [clubTivi](https://github.com/clubanderson/clubTivi), zaključan kao Git submodule `vendor/clubTivi` na `ac690553a7aba33e8f91db653e1ac74e74a9e3b4`. Njegovo autorstvo ne mijenja se.

```bash
git clone --recurse-submodules https://github.com/bren-wp/IPTV-.git
cd IPTV-
npm install
npm run tauri -- icon assets/brand/iptv-plus-icon.svg
python3 tools/clubtivi/prepare.py --icon-png src-tauri/icons/128x128@2x.png --icon-ico src-tauri/icons/icon.ico --version 0.2.0
cd vendor/clubTivi
flutter pub upgrade
flutter analyze --no-fatal-infos --no-fatal-warnings
flutter test
flutter build apk --debug
```

Windows native: `flutter build windows --release`. Nema više `--edition` argumenta ni dvaju package ID-ova: `com.brendigo.iptvplus` koristi trajno omogućene prethodne Pro funkcije. Automatizacija gradi nepotpisani APK/AAB bez GitHub Secrets; Android zahtijeva potpis za instalaciju i Play. Sve promjene ovisnosti moraju proći Flutter testove.

Za screenshotove, prava sadržaja i licence vidi `assets/screens`, `THIRD_PARTY_NOTICES.md` i `docs/DEPENDENCIES.md`.
