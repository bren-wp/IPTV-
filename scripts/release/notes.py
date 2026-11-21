#!/usr/bin/env python3
"""Write release notes for the single full-featured IPTV+ app."""
from pathlib import Path
import sys

version = sys.argv[1]
Path("release").mkdir(exist_ok=True)
Path("release/RELEASE-NOTES.md").write_text(f"""# IPTV+ v{version}

**Jedno IPTV+ izdanje, bez Free/Pro podjele**, za Android, Android TV i Windows.

## Datoteke izdanja
- IPTV-Plus-v{version}.apk — Android release APK
- IPTV-Plus-v{version}.aab — Google Play Android App Bundle
- IPTV-Plus-v{version}-Portable.exe — Windows bez instalacije
- IPTV-Plus-v{version}-Setup.exe — Windows NSIS instalacija
- SHA256SUMS.txt — SHA-256 zbrojevi
- IPTV-Plus-v{version}-Branding.zip — svi brending i dizajnerski SVG-ovi

Napredne Pro-tier funkcije koje clubTivi već implementira sada su uključene
u jedinstvenu aplikaciju bez prijave i reklamnih SDK-ova.

IPTV+ ne sadrži neovlaštene premium programe ni prava na TV sadržaje.
Sami GitHub M3U izvori nisu dozvola za emitiranje.

Repozitorij: https://github.com/bren-wp/IPTV-
""", encoding="utf-8")
