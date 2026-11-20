# clubTivi → IPTV+ rebrand adapter (optional Flutter engine)

The official [clubanderson/clubTivi](https://github.com/clubanderson/clubTivi) application is **Apache-2.0** licensed and currently offers a substantially more complete Flutter IPTV player than the experimental Tauri media shell in this repository.

The original project is linked at `vendor/clubTivi` as a **pinned Git submodule**, commit `ac690553a7aba33e8f91db653e1ac74e74a9e3b4`. No code is copied or altered in the original upstream GitHub repository.

## Prepare an IPTV+ Flutter variant

1. Clone IPTV+ with submodules or run `git submodule update --init vendor/clubTivi`.
2. Generate **native original IPTV+ icons** from `assets/brand/iptv-plus-icon.svg` using Tauri CLI:
   `npm install && npm run tauri -- icon assets/brand/iptv-plus-icon.svg`
3. In a **clean, pinned submodule checkout** (use a throwaway clone or separate worktree), run:

```bash
python3 tools/clubtivi/prepare.py --edition free \
  --icon-png src-tauri/icons/128x128@2x.png \
  --icon-ico src-tauri/icons/icon.ico \
  --version 0.1.0 --build-number 1

cd vendor/clubTivi
flutter pub get
flutter run -d windows
```

Repeat from a **fresh submodule checkout** with `--edition pro`. The preparation script refuses to overwrite a previously modified worktree. Never reset a worktree containing work you want to keep.

## Scope of adapter

- Product titles in Flutter + native Android/Windows, Android package ID Free/Pro, icon paths/Windows native icon.
- IPTV+ colors from the approved brand and launcher logo.
- Android minimum SDK 24 and removal of unsupported Android in-app APK-install permission.
- Preserves Flutter package name `clubtivi` **internally** to avoid invalidating all Dart `package:clubtivi/...` references.
- Preserves original Apache 2.0 license, NOTICE/credit and clubTivi source authorship.
- Adds build-time Free/Pro edition flag and **different app names**, but **does not yet implement feature gates** in the original Flutter project.

## Current limitations

**This is an optional evaluation adapter, not a production replacement or release.** It has not passed the full Flutter native builds, has no configured release signing, Setup/Portable build, or pixel-perfect QA. It must not be substituted into the existing eight-artifact Tauri GitHub Release pipeline without an explicit, reviewed migration plan.

The full player UI and remote navigation of clubTivi are more mature; however, rebranding needs further localization and layout work to match the 39 IPTV+ screen concepts. The `IPTV+` brand must not imply endorsement by upstream.

## Rights
clubTivi provides no TV channels, subscription access or legitimate premium streams. The IPTV+ regional GitHub source browser is a distinct Tauri feature. Bringing that source logic into Flutter will require an explicit platform implementation and licensing review.

Source license: `vendor/clubTivi/LICENSE`. Additional notices: [THIRD_PARTY_NOTICES.md](../../THIRD_PARTY_NOTICES.md).
