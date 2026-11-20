# Tehnička arhitektura

## Zašto Tauri 2 za Android i Windows
Jedna React/TypeScript implementacija olakšava dijeljenje UX-a, pregleda i testova; Tauri 2 pruža nativni Rust host za Windows i Android. Android TV je posebno QA područje, ne automatski dovršen cilj. Početna verzija koristi minimalna Tauri dopuštenja.

- UI: React 19 + Vite 6 + TypeScript + CSS tokens + Lucide.
- Player: HTML5 `video` i hls.js; kompatibilnost ovisi o streamu, WebViewu i CORS pravilima.
- Uvoz: lokalna datoteka/tekst M3U, uz ograničenja veličine i URL schemea.
- Pohrana: samo postavke i ID-ovi favorita u `localStorage`, bez trajnog čuvanja izvora/credentials.
- Rust host: osnovni Tauri shell, bez opasnih IPC naredbi i bez nedeklariranih pluginova.
- CI: TypeScript provjera, frontend build i parser testovi. Windows/Android release posao nije još konfiguriran.

## Pokretanje
```bash
npm install
npm run dev           # browser UX preview
npm test
npm run build
npm run tauri dev     # Windows s instaliranim Rustom i WebView2
npm run tauri android init
npm run tauri android dev
```

Prije `tauri android init` instalirati Android Studio, SDK/NDK i Android targete prema [službenom Tauri vodiču](https://v2.tauri.app/start/prerequisites/). Za Windows release treba generirati i provjeriti produkcijske ikone (`npm run tauri icon assets/brand/iptv-plus-icon.svg`), zatim `npm run tauri build`.

## Ograničenja
- Ne dolazi s IPTV streamovima, EPG rasporedom, pretplatama ili kodom za zaobilaženje DRM-a.
- CORS, stream formati i prava pristupa mogu onemogućiti prikaz.
- Potrebni su native Android/Windows build testovi prije izdavanja.
- Bazni CSS je responsivan, ali pixel-perfect fizička podudarnost i Android TV D-pad nisu verificirani.
