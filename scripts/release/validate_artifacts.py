#!/usr/bin/env python3
"""Fail closed when any one of the required eight release files is missing."""
from pathlib import Path
import argparse
import hashlib
import zipfile

parser = argparse.ArgumentParser()
parser.add_argument("--directory", default="release")
parser.add_argument("--version", required=True)
args = parser.parse_args()
folder = Path(args.directory)
expected = []
for edition in ("Free", "Pro"):
    expected += [f"IPTV-Plus-v{args.version}-{edition}.{ext}" for ext in ("apk", "aab")]
    expected += [f"IPTV-Plus-v{args.version}-{edition}-{kind}.exe" for kind in ("Portable", "Setup")]
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
print("Eight required packages present, nontrivial, and structurally recognizable.")
checksums = [hashlib.sha256((folder / name).read_bytes()).hexdigest() + "  " + name for name in sorted(expected)]
(folder / "SHA256SUMS.txt").write_text("\n".join(checksums) + "\n", encoding="utf-8")
