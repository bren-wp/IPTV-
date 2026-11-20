#!/usr/bin/env python3
import os
from pathlib import Path
import shutil
import sys

if len(sys.argv) != 4:
    raise SystemExit("Usage: collect_android.py <edition:Free|Pro> <version> <output-dir>")
edition, version, directory = sys.argv[1:]
if edition not in ("Free", "Pro"):
    raise SystemExit("Invalid edition.")
root = Path("src-tauri/gen/android/app/build/outputs")
if not root.is_dir():
    raise SystemExit("Android output folder not found.")
output = Path(directory)
output.mkdir(parents=True, exist_ok=True)
for kind in ("apk", "aab"):
    items = [
        p for p in root.rglob("*." + kind)
        if "release" in p.name.lower() and "unsigned" not in p.name.lower() and p.is_file()
    ]
    if not items:
        raise SystemExit("No signed release " + kind + " found")
    items.sort(key=lambda p: ("universal" not in str(p).lower(), -p.stat().st_size, str(p)))
    if len(items) > 1 and "universal" not in str(items[0]).lower():
        raise SystemExit(f"Ambiguous release {kind} artifact(s): {items}")
    dest = output / f"IPTV-Plus-v{version}-{edition}.{kind}"
    shutil.copy2(items[0], dest)
    print(f"{kind.upper()}: {dest}, {dest.stat().st_size} bytes")
