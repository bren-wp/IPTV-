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

    # Activate the upstream's existing Free/Pro feature-gating instead of merely
    # changing the displayed edition name. Internal identifiers stay original.
    main = root / "lib/main.dart"
    replace_required(main, "import 'app/app.dart';",
                     "import 'app/app.dart';\nimport 'core/feature_gate.dart';\nimport 'core/iptvplus_edition.dart';")
    replace_required(main, "  MediaKit.ensureInitialized();",
                     "  FeatureGate.setTier(isIptvPlusPro ? AppTier.pro : AppTier.free);\n  MediaKit.ensureInitialized();")
    mark_modified(main, "//")

    # clubTivi already has a TV remote-friendly, one-click provider chooser.
    # Add regional GitHub public directories to its existing FreeTvProvider list.
    regional = [
        ("iptvplus-doubo-hr", "Hrvatska - Doubo", "https://cdn.jsdelivr.net/gh/streamline-iptv/iptv-playlists@dist/countries/hr.m3u"),
        ("iptvplus-doubo-ba", "BiH - Doubo", "https://cdn.jsdelivr.net/gh/streamline-iptv/iptv-playlists@dist/countries/ba.m3u"),
        ("iptvplus-doubo-rs", "Srbija - Doubo", "https://cdn.jsdelivr.net/gh/streamline-iptv/iptv-playlists@dist/countries/rs.m3u"),
        ("iptvplus-iptvorg-hr", "Hrvatska - iptv-org", "https://iptv-org.github.io/iptv/countries/hr.m3u"),
        ("iptvplus-iptvorg-si", "Slovenija - iptv-org", "https://iptv-org.github.io/iptv/countries/si.m3u"),
        ("iptvplus-iptvorg-ba", "BiH - iptv-org", "https://iptv-org.github.io/iptv/countries/ba.m3u"),
        ("iptvplus-iptvorg-rs", "Srbija - iptv-org", "https://iptv-org.github.io/iptv/countries/rs.m3u"),
        ("iptvplus-biskyt-live", "Javni TV - Legal Free IPTV", "https://biskyt.github.io/legalFreeIPTVplaylist/live.m3u"),
        ("iptvplus-biskyt-movies", "Filmovi - Legal Free IPTV", "https://biskyt.github.io/legalFreeIPTVplaylist/movies.m3u"),
        ("iptvplus-biskyt-series", "Serije - Legal Free IPTV", "https://biskyt.github.io/legalFreeIPTVplaylist/series.m3u"),
    ]
    presets = "\n".join(
        f"    FreeTvProvider(\n      id: '{identifier}',\n"
        f"      name: '{label}',\n      url: '{url}',\n"
        "      description: 'Vanjska javna zbirka; prava pojedinog programa nisu zajamcena.',\n"
        "      icon: Icons.public_rounded,\n    ),"
        for identifier, label, url in regional
    )
    providers = root / "lib/features/providers/providers_screen.dart"
    replace_required(providers, "  static const all = [", "  static const all = [\n" + presets)
    replace_required(providers, "title: const Text('IPTV Providers')", "title: const Text('IPTV+ · Izvori i liste')")
    replace_required(providers, "const _SectionHeader(title: 'Free TV Providers')",
                     "const _SectionHeader(title: 'Javne IPTV zbirke — prava sadržaja provjeriti')")
    mark_modified(providers, "//")

    # Resyncing an existing provider must not count as adding a new Free provider.
    provider_manager = root / "lib/features/providers/provider_manager.dart"
    replace_required(provider_manager,
                     "    await _checkProviderLimit();\n    await _db.upsertProvider(",
                     "    final current = await _db.getAllProviders();\n"
                     "    if (!current.any((p) => p.id == id)) await _checkProviderLimit();\n"
                     "    await _db.upsertProvider(")
    mark_modified(provider_manager, "//")

    # IPTV+ is the primary Flutter application UI, keeping clubTivi as the engine.
    # All screens remain platform-aware and must pass Android/TV/Windows visual QA.
    home_dir = root / "lib/features/home"
    home_dir.mkdir(parents=True, exist_ok=True)
    shutil.copyfile(ROOT / "tools/clubtivi/iptv_plus_home.dart",
                    home_dir / "iptv_plus_home.dart")
    shutil.copyfile(ROOT / "tools/clubtivi/iptv_plus_home_test.dart",
                    root / "test/iptv_plus_home_test.dart")

    router = root / "lib/app/router.dart"
    replace_required(router, "import '../features/channels/channels_screen.dart';",
                     "import '../features/channels/channels_screen.dart';\n"
                     "import '../features/home/iptv_plus_home.dart';")
    replace_required(router, "  final sidebarRoutes = [",
                     "  final sidebarRoutes = [\n    GoRoute(\n"
                     "      path: '/home',\n"
                     "      builder: (context, state) => const IptvPlusHomeScreen(),\n"
                     "    ),")
    mark_modified(router, "//")

    splash = root / "lib/features/splash/splash_screen.dart"
    replace_required(splash, "context.go('/');", "context.go('/home');")
    replace_required(splash, "assets/icon/clubtivi-icon.png",
                     "assets/icon/iptv-plus-icon.png")
    splash_data = splash.read_text(encoding="utf-8")
    splash_data = splash_data.replace("'clubTivi'", "'IPTV+'")
    splash_data = splash_data.replace("'live tv, your way'", "'Televizija po tvome'")
    splash_data = splash_data.replace("Color(0xFF6C5CE7)", "Color(0xFF7C5CFF)")
    splash_data = splash_data.replace("Color(0xFF0A0A0F)", "Color(0xFF080D1C)")
    splash.write_text(splash_data, encoding="utf-8")
    mark_modified(splash, "//")

    tv_shell = root / "lib/platform/tv/tv_shell.dart"
    replace_required(tv_shell,
        "_NavItem(icon: Icons.live_tv_rounded, label: 'Live TV', route: '/'),",
        "_NavItem(icon: Icons.home_rounded, label: 'Početna', route: '/home'),\n"
        "    _NavItem(icon: Icons.live_tv_rounded, label: 'TV uživo', route: '/'),")
    for old, new in [
        ("label: 'Guide'", "label: 'TV vodič'"),
        ("label: 'Providers'", "label: 'Izvori'"),
        ("label: 'EPG Map'", "label: 'EPG postavke'"),
        ("label: 'Settings'", "label: 'Postavke'"),
        ("'clubTivi'", "'IPTV+'"),
        ("Color(0xFF6C5CE7)", "Color(0xFF7C5CFF)"),
        ("Color(0xFF0D0D14)", "Color(0xFF080D1C)"),
    ]:
        if old in tv_shell.read_text(encoding="utf-8"):
            replace_required(tv_shell, old, new)
    mark_modified(tv_shell, "//")

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
    print("Free/Pro feature gate and ten optional regional/public presets applied.")
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
