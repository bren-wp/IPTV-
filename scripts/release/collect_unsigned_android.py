#!/usr/bin/env python3
"""Verify and collect unsigned Android packages.

Unsigned APKs cannot be installed. Unsigned AABs are not Play-ready.
Never generate or consume signing keys here.
"""
from __future__ import annotations

import argparse
from pathlib import Path
import shutil
import subprocess
import zipfile


def find_package(root: Path, suffix: str) -> Path:
    candidates = []
    for directory in [root / "build/app/outputs", root / "android/app/build/outputs"]:
        if not directory.exists():
            continue
        for item in directory.rglob("*"):
            if not item.is_file() or item.suffix.lower() != suffix:
                continue
            if "release" not in item.name.lower() or "debug" in item.name.lower():
                continue
            candidates.append(item)
    if not candidates:
        raise RuntimeError(f"Missing unsigned {suffix} Gradle release output")
    # Prefer the original Gradle output, not the copied Flutter post-build APK.
    candidates.sort(key=lambda p: (
        "-unsigned" not in p.name.lower() if suffix == ".apk" else False,
        "outputs/apk/" not in p.as_posix() if suffix == ".apk" else
            "outputs/bundle/" not in p.as_posix(),
        len(str(p)),
    ))
    return candidates[0]


def verify_unsigned(apk: Path, aab: Path) -> None:
    for path, manifest in (
        (apk, "AndroidManifest.xml"),
        (aab, "base/manifest/AndroidManifest.xml"),
    ):
        if path.stat().st_size < 100_000 or not zipfile.is_zipfile(path):
            raise RuntimeError(f"Invalid Android package: {path}")
        with zipfile.ZipFile(path) as arc:
            entries = arc.namelist()
            if manifest not in entries:
                raise RuntimeError(f"Android manifest missing: {path}")
            signatures = [
                entry for entry in entries
                if entry.upper().startswith("META-INF/") and
                entry.upper().endswith((".SF", ".RSA", ".DSA", ".EC"))
            ]
            if signatures:
                raise RuntimeError(f"JAR signature detected in unsigned {path}")
    # ZIP signatures alone cannot detect APK v2/v3 blocks. apksigner can.
    signer = shutil.which("apksigner")
    if not signer:
        import os
        sdk = Path(os.environ.get("ANDROID_HOME", ""))
        match = sorted(sdk.glob("build-tools/*/apksigner"))
        signer = str(match[-1]) if match else None
    if not signer:
        raise RuntimeError("apksigner required to prove APK is unsigned")
    result = subprocess.run([signer, "verify", str(apk)],
                            capture_output=True, text=True, check=False)
    if result.returncode == 0:
        raise RuntimeError("APK is signed; unsigned release must not publish")


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("--root", type=Path, required=True)
    parser.add_argument("--directory", type=Path, required=True)
    parser.add_argument("--version", required=True)
    args = parser.parse_args()

    apk = find_package(args.root, ".apk")
    aab = find_package(args.root, ".aab")
    verify_unsigned(apk, aab)
    args.directory.mkdir(parents=True, exist_ok=True)
    outputs = (
        (apk, args.directory / f"IPTV-Plus-v{args.version}-Unsigned.apk"),
        (aab, args.directory / f"IPTV-Plus-v{args.version}-Unsigned.aab"),
    )
    for original, target in outputs:
        shutil.copy2(original, target)
        print(f"Validated unsigned package: {target.name}")
    print("Unsigned APK is NOT installable; unsigned AAB is NOT Play-ready.")


if __name__ == "__main__":
    main()
