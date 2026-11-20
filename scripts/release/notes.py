#!/usr/bin/env python3
from pathlib import Path
import sys
version = sys.argv[1]
Path("release/RELEASE-NOTES.md").write_text(f"""# IPTV+ v{version}

**IPTV+ Free / IPTV+ Pro** za Android i Windows.

## Sadržaj izdanja
- Free i Pro: potpisani Android APK i AAB (potrebni su unaprijed konfigurirani vlastiti upload ključevi).
- Free i Pro: Windows Setup.exe (NSIS) i samostalni Portable.exe (za rad je potreban WebView2).
- SHA256SUMS.txt te paket svih brending i koncept dizajn SVG slika.

## Važno
IPTV+ je reproduktor za legalne izvore. Ne uključuje nelicencirane premium TV programe ili pretplate.
Android TV, EPG, reprodukcija streamova i dostupnost pojedinih formata imaju ograničenja koja ovise o izvoru i uređaju.

Izvorni kod, upute i detaljne promjene: https://github.com/bren-wp/IPTV-
""", encoding="utf-8")
