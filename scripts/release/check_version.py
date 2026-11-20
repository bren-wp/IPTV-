#!/usr/bin/env python3
"""Enforce one unique GitHub Release per application version."""
import json
import os
import re
import subprocess
import sys

version = json.load(open("package.json", encoding="utf-8"))["version"]
if not re.fullmatch(r"\d+\.\d+\.\d+", version):
    raise SystemExit(f"Unsupported version: {version!r}. Use MAJOR.MINOR.PATCH")
requested = os.environ.get("RELEASE_VERSION", "").strip()
if requested and requested != version:
    raise SystemExit(f"Requested version {requested} does not match package.json {version}")
tag = "v" + version
check = subprocess.run(["gh", "release", "view", tag], stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)
if check.returncode == 0:
    raise SystemExit(f"{tag} already exists: bump package.json and Tauri version before publishing again.")
tauri = json.load(open("src-tauri/tauri.conf.json", encoding="utf-8"))["version"]
if tauri != version:
    raise SystemExit(f"Tauri {tauri} differs from package.json {version}")
if "GITHUB_OUTPUT" in os.environ:
    with open(os.environ["GITHUB_OUTPUT"], "a", encoding="utf-8") as handle:
        handle.write(f"version={version}\ntag={tag}\n")
print(f"Release gate ready for {tag}")
