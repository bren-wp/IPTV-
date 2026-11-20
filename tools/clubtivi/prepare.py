#!/usr/bin/env python3
"""Prepare an independent IPTV+ branded clubTivi Flutter worktree.

The upstream checkout stays a tracked Apache-2.0 git submodule.
This script modifies ONLY a local checkout; it doesn't rewrite upstream
authors, package imports, license notices, or user secrets.
"""
from __future__ import annotations

import argparse
from pathlib import Path
import re
import shutil
import subprocess
import sys

UPSTREAM = "ac690553a7aba33e8f91db653e1ac74e74a9e3b4"
APP_IDS = {"free": "com.brendigo.iptvplus.free", "pro": "com.brendigo.iptvplus.pro"}
ROOT = Path(__file__).resolve().parents[2]
DEFAULT_UPSTREAM = ROOT / "vendor" / "clubTivi"


def replace_required(path: Path, old: str, new: str) -> None:
    data = path.read_text(encoding="utf-8")
    if old not in data:
        raise RuntimeError(f"clubTivi upstream changed. Required marker not found in {path}: {old[:70]}")
    path.write_text(data.replace(old, new, 1), encoding="utf-8")


def mark_modified(path: Path, comment: str) -> None:
    data = path.read_text(encoding="utf-8")
    if "IPTV+ downstream modification" not in data:
        body = "IPTV+ downstream modification by Brendigo; based on clubTivi Apache-2.0."
        marker = "<!-- " + body + " -->" if comment == "<!--" else comment + " " + body
        path.write_text(marker + "\n" + data, encoding="utf-8")


def ensure_pristine(root: Path) -> None:
    if not (root / "LICENSE").is_file() or not (root / "pubspec.yaml").is_file():
        raise RuntimeError("clubTivi checkout missing. Run 'git submodule update --init vendor/clubTivi'")
    revision = subprocess.check_output(
        ["git", "-C", str(root), "rev-parse", "HEAD"], text=True
    ).strip()
    if revision != UPSTREAM:
        raise RuntimeError(f"Expected pinned clubTivi revision {UPSTREAM}; got {revision}")
    dirty = subprocess.check_output(
        ["git", "-C", str(root), "status", "--porcelain"], text=True
    ).strip()
    if dirty:
        raise RuntimeError("clubTivi worktree has local changes. Use a fresh checkout to avoid overwriting edits.")


def prepare(root: Path, edition: str, icon_png: Path, icon_ico: Path, version: str, build_number: int) -> None:
    ensure_pristine(root)
    if edition not in APP_IDS:
        raise RuntimeError("Edition must be free or pro.")
    if not re.fullmatch(r"\d+\.\d+\.\d+", version) or build_number < 1:
        raise RuntimeError("Invalid semantic version/build number.")
    if not icon_png.is_file() or icon_png.stat().st_size < 300:
        raise RuntimeError("Provide a genuine IPTV+ PNG launcher icon, at least 300 bytes.")
    if not icon_ico.is_file() or icon_ico.stat().st_size < 300:
        raise RuntimeError("Provide a genuine IPTV+ ICO icon, at least 300 bytes.")

    # Brand graphics are generated from IPTV+'s own original SVG artwork.
    dst_png = root / "assets/icon/iptv-plus-icon.png"
    shutil.copyfile(icon_png, dst_png)
    shutil.copyfile(icon_png, root / "assets/icon/clubtivi-icon.png")
    shutil.copyfile(icon_ico, root / "windows/runner/resources/app_icon.ico")

    pubspec = root / "pubspec.yaml"
    replace_required(pubspec, 'description: "Open-source cross-platform IPTV player with intelligent EPG mapping, multi-provider stream failover, and remote control support."',
                     'description: "IPTV+ by Brendigo - independent downstream IPTV player derived from clubTivi."')
    replace_required(pubspec, "version: 0.4.0+5", f"version: {version}+{build_number}")
    updated = pubspec.read_text(encoding="utf-8").replace(
        'assets/icon/clubtivi-icon.png', 'assets/icon/iptv-plus-icon.png'
    )
    pubspec.write_text(updated, encoding="utf-8")
    mark_modified(pubspec, "#")

    app = root / "lib/app/app.dart"
    replace_required(app, "import 'router.dart';", "import 'router.dart';\nimport '../core/iptvplus_edition.dart';")
    replace_required(app, "title: 'clubTivi',", "title: iptvPlusTitle,")
    mark_modified(app, "//")

    edition_file = root / "lib/core/iptvplus_edition.dart"
    edition_file.write_text(
        "// IPTV+ downstream addition by Brendigo.\n"
        "const iptvPlusEdition = String.fromEnvironment('IPTV_EDITION', defaultValue: 'free');\n"
        "const isIptvPlusPro = iptvPlusEdition == 'pro';\n"
        "const iptvPlusTitle = isIptvPlusPro ? 'IPTV+ Pro' : 'IPTV+ Free';\n",
        encoding="utf-8",
    )

    theme = root / "lib/app/theme.dart"
    for old, new in [
        ("Color(0xFF6C5CE7)", "Color(0xFF7C5CFF)"),
        ("Color(0xFF0A0A0F)", "Color(0xFF080D1C)"),
        ("Color(0xFF1A1A2E)", "Color(0xFF111A2C)"),
    ]:
        replace_required(theme, old, new)
    mark_modified(theme, "//")

    manifest = root / "android/app/src/main/AndroidManifest.xml"
    replace_required(manifest, 'android:label="clubTivi"', f'android:label="IPTV+ {edition.title()}"')
    # The original in-app APK installation permission isn't required for Google Play distribution.
    manifest.write_text(
        manifest.read_text(encoding="utf-8").replace(
            '    <uses-permission android:name="android.permission.REQUEST_INSTALL_PACKAGES"/>\n', ''
        ),
        encoding="utf-8",
    )
    mark_modified(manifest, "<!--")

    gradle = root / "android/app/build.gradle.kts"
    replace_required(gradle, 'applicationId = "io.github.clubanderson.clubtivi"', f'applicationId = "{APP_IDS[edition]}"')
    replace_required(gradle, "minSdk = flutter.minSdkVersion", "minSdk = 24")
    # Signing with a debug key is not suitable for release. Never commit a private keystore.
    replace_required(gradle, 'signingConfig = signingConfigs.getByName("debug")',
                     '// IPTV+ downstream: debug signing removed; signed release requires external CI credentials.')
    mark_modified(gradle, "//")

    window_main = root / "windows/runner/main.cpp"
    replace_required(window_main, 'window.Create(L"clubTivi",', 'window.Create(L"IPTV+ ' + edition.title() + '",')
    mark_modified(window_main, "//")

    cmake = root / "windows/CMakeLists.txt"
    replace_required(cmake, 'set(BINARY_NAME "clubtivi")', 'set(BINARY_NAME "iptvplus")')
    mark_modified(cmake, "#")

    resources = root / "windows/runner/Runner.rc"
    for old, new in [
        ('"FileDescription", "clubTivi"', '"FileDescription", "IPTV+ ' + edition.title() + '"'),
        ('"ProductName", "clubTivi"', '"ProductName", "IPTV+ ' + edition.title() + '"'),
        ('"InternalName", "clubtivi"', '"InternalName", "iptvplus"'),
        ('"OriginalFilename", "clubtivi.exe"', '"OriginalFilename", "iptvplus.exe"'),
    ]:
        replace_required(resources, old, new)
    # Retain original authorship while identifying downstream branding changes.
    replace_required(resources,
                     '"Copyright (C) 2026 io.github.clubanderson. All rights reserved."',
                     '"Original clubTivi contributors; downstream IPTV+ modifications (C) 2026 Brendigo."')
    mark_modified(resources, "//")
    print(f"Prepared IPTV+ {edition.title()} based on clubTivi {UPSTREAM}.")
    print("Run: flutter pub get")
    print(f"Run: flutter build apk --release --dart-define=IPTV_EDITION={edition}")
    print(f"Run: flutter build appbundle --release --dart-define=IPTV_EDITION={edition}")
    print("WARNING: Android release signing and production checks remain required.")


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("--edition", required=True, choices=APP_IDS.keys())
    parser.add_argument("--checkout", type=Path, default=DEFAULT_UPSTREAM)
    parser.add_argument("--icon-png", type=Path, required=True)
    parser.add_argument("--icon-ico", type=Path, required=True)
    parser.add_argument("--version", default="0.1.0")
    parser.add_argument("--build-number", type=int, default=1)
    args = parser.parse_args()
    try:
        prepare(args.checkout.resolve(), args.edition,
                args.icon_png.resolve(), args.icon_ico.resolve(),
                args.version, args.build_number)
    except (RuntimeError, OSError, subprocess.CalledProcessError) as error:
        parser.exit(1, f"IPTV+ clubTivi preparation failed: {error}\n")


if __name__ == "__main__":
    main()
