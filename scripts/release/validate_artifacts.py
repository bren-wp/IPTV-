#!/usr/bin/env python3
"""Fail closed when any one of the required four release files is missing."""
from pathlib import Path
import argparse
import hashlib
import zipfile

parser = argparse.ArgumentParser()
parser.add_argument("--directory", default="release")
parser.add_argument("--version", required=True)
args = parser.parse_args()
folder = Path(args.directory)
expected = [
    f"IPTV-Plus-v{args.version}.apk",
    f"IPTV-Plus-v{args.version}.aab",
    f"IPTV-Plus-v{args.version}-Portable.exe",
    f"IPTV-Plus-v{args.version}-Setup.exe",
]
legacy = [p for p in folder.iterdir() if
          p.name.endswith(("-Free.apk", "-Pro.apk", "-Free.aab", "-Pro.aab",
                           "-Free-Portable.exe", "-Pro-Portable.exe",
                           "-Free-Setup.exe", "-Pro-Setup.exe"))]
if legacy:
    raise SystemExit("Old Free/Pro artifacts are forbidden in the unified release")
for name in expected:
    path = folder / name
    if not path.is_file() or path.stat().st_size < 100_000:
        raise SystemExit(f"Missing or suspiciously small release file: {name}")
    if path.suffix in (".apk", ".aab"):
        if not zipfile.is_zipfile(path):
            raise SystemExit(f"Not a valid ZIP-based Android package: {name}")
        with zipfile.ZipFile(path) as arc:
            names = arc.namelist()
            expected_file = "AndroidManifest.xml" if path.suffix == ".apk" else "base/manifest/AndroidManifest.xml"
            if expected_file not in names:
                raise SystemExit(f"Missing Android manifest in {name}")
    elif path.suffix == ".exe":
        with path.open("rb") as binary:
            if binary.read(2) != b"MZ":
                raise SystemExit(f"Not a PE Windows executable: {name}")
print("Four required packages present, nontrivial, and structurally recognizable.")
checksums = [hashlib.sha256((folder / name).read_bytes()).hexdigest() + "  " + name for name in sorted(expected)]
(folder / "SHA256SUMS.txt").write_text("\n".join(checksums) + "\n", encoding="utf-8")
