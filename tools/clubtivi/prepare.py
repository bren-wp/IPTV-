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
APP_ID = "com.brendigo.iptvplus"
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


def prepare(root: Path, icon_png: Path, icon_ico: Path, version: str, build_number: int) -> None:
    ensure_pristine(root)
    if not re.fullmatch(r"\d+\.\d+\.\d+", version) or build_number < 1:
        raise RuntimeError("Invalid semantic version/build number.")
    major, minor, patch = map(int, version.split("."))
    if minor >= 1000 or patch >= 1000 or major >= 1000:
        raise RuntimeError("Version components must be <1000 for monotonic Play versionCode")
    # Unified IPTV+ versionCode stays monotonic for updates.
    build_number = max(build_number, major * 1000000 + minor * 1000 + patch)
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
    # Current stable compatible release floor, verified on pub.dev Nov 2026.
    # Full lockfile refresh requires Flutter analyze + native build gates.
    for previous, current in (
        ("  dio: ^5.7.0", "  dio: ^5.11.1"),
        ("  drift: ^2.22.1", "  drift: ^2.35.4"),
        ("  drift_dev: ^2.22.1", "  drift_dev: ^2.35.4"),
        ("  shared_preferences: ^2.5.4", "  shared_preferences: ^2.5.6"),
        ("  media_kit: ^1.1.11", "  media_kit: ^1.2.6"),
        ("  go_router: ^14.8.1", "  go_router: ^18.1.4"),
    ):
        replace_required(pubspec, previous, current)
    mark_modified(pubspec, "#")

    app = root / "lib/app/app.dart"
    replace_required(app, "import 'router.dart';", "import 'router.dart';\nimport '../core/iptvplus_edition.dart';")
    replace_required(app, "title: 'clubTivi',", "title: iptvPlusTitle,")
    mark_modified(app, "//")

    # One unified app with all previously Pro-gated functionality.
    edition_file = root / "lib/core/iptvplus_edition.dart"
    edition_file.write_text(
        "// IPTV+ unified downstream branding; clubTivi copyright retained.\n"
        "const iptvPlusTitle = 'IPTV+';\n",
        encoding="utf-8",
    )

    main = root / "lib/main.dart"
    replace_required(main, "import 'app/app.dart';",
                     "import 'app/app.dart';\nimport 'core/feature_gate.dart';\nimport 'core/iptvplus_edition.dart';")
    replace_required(main, "  MediaKit.ensureInitialized();",
                     "  FeatureGate.setTier(AppTier.pro);\n  MediaKit.ensureInitialized();")
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

    # Resyncing an existing provider must not count as adding a new provider.
    provider_manager = root / "lib/features/providers/provider_manager.dart"
    replace_required(provider_manager,
                     "    await _checkProviderLimit();\n    await _db.upsertProvider(",
                     "    final current = await _db.getAllProviders();\n"
                     "    if (!current.any((p) => p.id == id)) await _checkProviderLimit();\n"
                     "    await _db.upsertProvider(")

    # Periodically refresh only sources the user explicitly added from our
    # regional directory. Errors never remove the last known channel list.
    manager_src = provider_manager.read_text(encoding="utf-8")
    class_anchor = "  /// Resolve missing logos for a set of channels."
    if class_anchor not in manager_src:
        raise RuntimeError("ProviderManager refresh insertion point changed")
    refresh_fn = """  /// Sync opted-in public IPTV+ directories; never scrape premium sources.
  Future<void> refreshIptvPlusPublicSources() async {
    final providers = await _db.getAllProviders();
    for (final provider in providers.where(
      (p) => p.id.startsWith('iptvplus-') && p.type == 'm3u')) {
      try {
        await refreshProvider(provider.id);
      } catch (error) {
        debugPrint('IPTV+ source refresh failed: $error');
      }
    }
  }

"""
    provider_manager.write_text(
        manager_src.replace(class_anchor, refresh_fn + class_anchor, 1),
        encoding="utf-8",
    )

    channels = root / "lib/features/channels/channels_screen.dart"
    replace_required(channels, "  Timer? _nowPlayingTimer;",
                     "  Timer? _nowPlayingTimer;\n  Timer? _iptvPlusRefreshTimer;")
    replace_required(channels, "    _loadSearchHistory();",
                     "    _loadSearchHistory();\n"
                     "    Future.microtask(() => ref.read(providerManagerProvider).refreshIptvPlusPublicSources());\n"
                     "    _iptvPlusRefreshTimer = Timer.periodic(const Duration(hours: 12), (_) {\n"
                     "      if (mounted) unawaited(ref.read(providerManagerProvider).refreshIptvPlusPublicSources());\n"
                     "    });")
    replace_required(channels, "    _nowPlayingTimer?.cancel();",
                     "    _nowPlayingTimer?.cancel();\n    _iptvPlusRefreshTimer?.cancel();")
    mark_modified(channels, "//")

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

    # Determine TV layout at route build time. Upstream routed before
    # MediaQuery/PlatformInfo detection, so Android TV could use mobile layout.
    old_routes = """  if (PlatformInfo.isTV) {
    return GoRouter(
      initialLocation: '/splash',
      routes: [
        ShellRoute(
          builder: (context, state, child) => TvShell(child: child),
          routes: sidebarRoutes,
        ),
        ...standaloneRoutes,
      ],
    );
  }

  // Non-TV: flat routes (original behavior)
  return GoRouter(
    initialLocation: '/splash',
    routes: [
      ...sidebarRoutes,
      ...standaloneRoutes,
    ],
  );"""
    new_routes = """  return GoRouter(
    initialLocation: '/splash',
    routes: [
      ShellRoute(
        builder: (context, state, child) {
          PlatformInfo.detectFromContext(context);
          return PlatformInfo.isTV ? TvShell(child: child) : child;
        },
        routes: sidebarRoutes,
      ),
      ...standaloneRoutes,
    ],
  );"""
    replace_required(router, old_routes, new_routes)

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

    # Never show another developer's releases as IPTV+ updates.
    update_service = root / "lib/data/services/app_update_service.dart"
    replace_required(update_service, "const _repo = 'clubanderson/clubTivi';",
                     "const _repo = 'bren-wp/IPTV-';")
    replace_required(update_service, "const _currentVersion = '0.4.0';",
                     f"const _currentVersion = '{version}';")
    replace_required(update_service,
                     "final filePath = '${dir.path}/clubtivi-update.apk';",
                     "final filePath = '${dir.path}/iptv-plus-update.apk';")
    # The upstream updater selected the first GitHub APK, potentially
    # offering the wrong package, and required Play-restricted
    # REQUEST_INSTALL_PACKAGES. Open the official verified release page instead.
    replace_required(update_service,
                     "if (name.endsWith('.apk')) {",
                     "if (name == 'iptv-plus-v$version.apk') {")
    replace_required(update_service,
                     "import 'package:dio/dio.dart';",
                     "import 'package:dio/dio.dart';")
    updater_data = update_service.read_text(encoding="utf-8")
    for import_line in ("import 'dart:io';\n",
                        "import 'package:flutter/services.dart';\n",
                        "import 'package:path_provider/path_provider.dart';\n"):
        updater_data = updater_data.replace(import_line, "")
    start = updater_data.find("  /// Download APK and trigger install via native FileProvider intent.")
    end = updater_data.find("\n}\n\n/// Compare semver strings.", start)
    if start < 0 or end < 0:
        raise RuntimeError("Unexpected clubTivi updater structure")
    updater_data = updater_data[:start] + updater_data[end:]
    updater_data = updater_data.replace(
        "  static const _channel = MethodChannel('io.github.clubanderson.clubtivi/installer');\n",
        "")
    update_service.write_text(updater_data, encoding="utf-8")

    screen = root / "lib/features/channels/channels_screen.dart"
    replace_required(screen, "if (release.apkDownloadUrl != null)",
                     "if (release.htmlUrl.isNotEmpty)")
    replace_required(screen, "_showDownloadDialog(release.apkDownloadUrl!);",
                     "launchUrl(Uri.parse(release.htmlUrl), mode: LaunchMode.externalApplication);")
    screen_data = screen.read_text(encoding="utf-8")
    start = screen_data.find("  Future<void> _showDownloadDialog(String apkUrl) async {")
    end = screen_data.find("  Future<void> _refreshNowPlaying() async {", start)
    if start < 0 or end < 0:
        raise RuntimeError("Unexpected clubTivi update dialog structure")
    screen_data = screen_data[:start] + screen_data[end:]
    screen.write_text(screen_data, encoding="utf-8")

    settings_screen = root / "lib/features/settings/settings_screen.dart"
    replace_required(settings_screen, "if (release.apkDownloadUrl != null)",
                     "if (release.htmlUrl.isNotEmpty)")
    replace_required(settings_screen, "'Download & Install'", "'Otvori službeno izdanje'")
    replace_required(settings_screen, "Navigator.pop(ctx, 'install')", "Navigator.pop(ctx, 'open')")
    replace_required(settings_screen,
                     "if (action == 'install' && release.apkDownloadUrl != null && context.mounted) {\n"
                     "    _downloadUpdate(context, release.apkDownloadUrl!);\n"
                     "  }",
                     "if (action == 'open' && release.htmlUrl.isNotEmpty && context.mounted) {\n"
                     "    await launchUrl(Uri.parse(release.htmlUrl), mode: LaunchMode.externalApplication);\n"
                     "  }")
    settings_data = settings_screen.read_text(encoding="utf-8")
    start = settings_data.find("Future<void> _downloadUpdate(BuildContext context, String apkUrl) async {")
    end = settings_data.find("class SettingsScreen extends ConsumerStatefulWidget {", start)
    if start < 0 or end < 0:
        raise RuntimeError("Unexpected settings update code structure")
    settings_data = settings_data[:start] + settings_data[end:]
    settings_screen.write_text(settings_data, encoding="utf-8")
    mark_modified(settings_screen, "//")

    mark_modified(update_service, "//")

    # Replace remaining visible upstream names without touching package imports.
    # Keep original GitHub source URL for correct Apache-2.0 attribution.
    for relative in ("lib/features/channels/channels_screen.dart",
                     "lib/features/settings/settings_screen.dart"):
        screen = root / relative
        data = screen.read_text(encoding="utf-8")
        data = data.replace("'clubTivi'", "'IPTV+'")
        data = data.replace("'clubTivi v", "'IPTV+ v")
        data = data.replace("clubTivi will save", "IPTV+ will save")
        data = data.replace("clubTivi supports", "IPTV+ supports")
        screen.write_text(data, encoding="utf-8")
        mark_modified(screen, "//")

    theme = root / "lib/app/theme.dart"
    for old, new in [
        ("Color(0xFF6C5CE7)", "Color(0xFF7C5CFF)"),
        ("Color(0xFF0A0A0F)", "Color(0xFF080D1C)"),
        ("Color(0xFF1A1A2E)", "Color(0xFF111A2C)"),
    ]:
        replace_required(theme, old, new)
    mark_modified(theme, "//")

    manifest = root / "android/app/src/main/AndroidManifest.xml"
    replace_required(manifest, 'android:label="clubTivi"', 'android:label="IPTV+"')
    # The original in-app APK installation permission isn't required for Google Play distribution.
    manifest.write_text(
        manifest.read_text(encoding="utf-8").replace(
            '    <uses-permission android:name="android.permission.REQUEST_INSTALL_PACKAGES"/>\n', ''
        ),
        encoding="utf-8",
    )
    # The old sideloading APK installer is obsolete now that updates open
    # official release pages. Remove its exported platform surface entirely.
    manifest_text = manifest.read_text(encoding="utf-8")
    start = manifest_text.find("        <!-- FileProvider for in-app APK install -->")
    end = manifest_text.find("        <!-- Don't delete the meta-data below.", start)
    if start < 0 or end < 0:
        raise RuntimeError("Expected upstream FileProvider section not found")
    manifest_text = manifest_text[:start] + manifest_text[end:]
    manifest.write_text(manifest_text, encoding="utf-8")
    installer = root / "android/app/src/main/kotlin/io/github/clubanderson/clubtivi/MainActivity.kt"
    installer.write_text(
        "package io.github.clubanderson.clubtivi\n\n"
        "// IPTV+ downstream: removed legacy APK sideload MethodChannel.\n"
        "// Original clubTivi engine licensed under Apache-2.0.\n"
        "import io.flutter.embedding.android.FlutterActivity\n\n"
        "class MainActivity : FlutterActivity()\n", encoding="utf-8")
    old_paths = root / "android/app/src/main/res/xml/file_paths.xml"
    if old_paths.is_file():
        old_paths.unlink()
    mark_modified(manifest, "<!--")

    # Flutter 3.50 / AGP 9: migrate to public Android DSL + built-in Kotlin.
    # The old plugin/kotlinOptions blocks are Kotlin DSL script errors under
    # Gradle 9, not harmless warnings. Do not restore the legacy escape hatches.
    wrapper = root / "android/gradle/wrapper/gradle-wrapper.properties"
    replace_required(wrapper, "gradle-8.14-all.zip", "gradle-9.5.0-all.zip")
    settings_gradle = root / "android/settings.gradle.kts"
    replace_required(settings_gradle,
                     'id("com.android.application") version "8.11.1" apply false',
                     'id("com.android.application") version "9.3.1" apply false')
    replace_required(settings_gradle,
                     'id("org.jetbrains.kotlin.android") version "2.2.20" apply false',
                     'id("org.jetbrains.kotlin.android") version "2.4.20" apply false')
    gradle_properties = root / "android/gradle.properties"
    properties_text = gradle_properties.read_text(encoding="utf-8")
    properties_text = "\n".join(
        line for line in properties_text.splitlines()
        if not line.startswith(("android.builtInKotlin=", "android.newDsl="))
    ) + "\n"
    gradle_properties.write_text(properties_text, encoding="utf-8")

    gradle = root / "android/app/build.gradle.kts"
    # AGP 9 built-in Kotlin makes the legacy KGP and kotlinOptions obsolete.
    replace_required(gradle, '    id("kotlin-android")\n', "")
    replace_required(gradle,
                     "    kotlinOptions {\n"
                     "        jvmTarget = JavaVersion.VERSION_17.toString()\n"
                     "    }\n\n", "")
    gradle_source = gradle.read_text(encoding="utf-8")
    flutter_marker = '\nflutter {\n'
    if flutter_marker not in gradle_source:
        raise RuntimeError("Flutter Gradle marker not found")
    gradle_source = gradle_source.replace(
        flutter_marker,
        "\nkotlin {\n"
        "    compilerOptions {\n"
        "        jvmTarget = org.jetbrains.kotlin.gradle.dsl.JvmTarget.JVM_17\n"
        "    }\n"
        "}\n" + flutter_marker,
        1,
    )
    gradle.write_text(gradle_source, encoding="utf-8")
    replace_required(gradle, 'applicationId = "io.github.clubanderson.clubtivi"', f'applicationId = "{APP_ID}"')
    replace_required(gradle, "minSdk = flutter.minSdkVersion", "minSdk = 24")
    # Signing with a debug key is not suitable for release. Never commit a private keystore.
    replace_required(gradle, 'signingConfig = signingConfigs.getByName("debug")',
                     '// IPTV+ downstream: debug signing removed; signed release requires external CI credentials.')
    mark_modified(gradle, "//")

    window_main = root / "windows/runner/main.cpp"
    replace_required(window_main, 'window.Create(L"clubTivi",', 'window.Create(L"IPTV+",')
    mark_modified(window_main, "//")

    cmake = root / "windows/CMakeLists.txt"
    replace_required(cmake, 'set(BINARY_NAME "clubtivi")', 'set(BINARY_NAME "iptvplus")')
    mark_modified(cmake, "#")

    resources = root / "windows/runner/Runner.rc"
    for old, new in [
        ('"FileDescription", "clubTivi"', '"FileDescription", "IPTV+"'),
        ('"ProductName", "clubTivi"', '"ProductName", "IPTV+"'),
        ('"InternalName", "clubtivi"', '"InternalName", "iptvplus"'),
        ('"OriginalFilename", "clubtivi.exe"', '"OriginalFilename", "iptvplus.exe"'),
    ]:
        replace_required(resources, old, new)
    # Retain original authorship while identifying downstream branding changes.
    replace_required(resources,
                     '"Copyright (C) 2026 io.github.clubanderson. All rights reserved."',
                     '"Original clubTivi contributors; downstream IPTV+ modifications (C) 2026 Brendigo."')
    mark_modified(resources, "//")
    print(f"Prepared unified IPTV+ based on clubTivi {UPSTREAM}.")
    print("Run: flutter pub get")
    print("Run: flutter build apk --release")
    print("Run: flutter build appbundle --release")
    print("All advanced Pro-tier features enabled; ten optional regional sources included.")
    print("WARNING: Android release signing and production checks remain required.")


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("--checkout", type=Path, default=DEFAULT_UPSTREAM)
    parser.add_argument("--icon-png", type=Path, required=True)
    parser.add_argument("--icon-ico", type=Path, required=True)
    parser.add_argument("--version", default="0.2.0")
    parser.add_argument("--build-number", type=int, default=1)
    args = parser.parse_args()
    try:
        prepare(args.checkout.resolve(), args.icon_png.resolve(), args.icon_ico.resolve(),
                args.version, args.build_number)
    except (RuntimeError, OSError, subprocess.CalledProcessError) as error:
        parser.exit(1, f"IPTV+ clubTivi preparation failed: {error}\n")


if __name__ == "__main__":
    main()
