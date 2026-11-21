#!/usr/bin/env python3
"""Configure signed release builds for the pinned Flutter Gradle Kotlin template.

Never persists keystores in Git or CI artifacts. Validates all required secrets.
"""
from __future__ import annotations
import base64
import os
from pathlib import Path
import re
import sys

root = Path("vendor/clubTivi/android")
gradle = root / "app/build.gradle.kts"
secrets = ("IPTV_ANDROID_KEYSTORE_BASE64", "IPTV_ANDROID_STORE_PASSWORD",
           "IPTV_ANDROID_KEY_PASSWORD", "IPTV_ANDROID_KEY_ALIAS")
missing = [name for name in secrets if not os.environ.get(name)]
if missing:
    sys.exit("Missing signing secrets: " + ", ".join(missing))
if not gradle.is_file():
    sys.exit("Flutter Gradle app file not found. Prepare branded clubTivi first.")

target = Path(os.environ.get("RUNNER_TEMP", "/tmp")) / "iptv-plus-release.jks"
try:
    target.write_bytes(base64.b64decode(
        os.environ["IPTV_ANDROID_KEYSTORE_BASE64"], validate=True))
except (ValueError, base64.binascii.Error):
    sys.exit("Keystore secret must be valid base64")
if target.stat().st_size < 128:
    sys.exit("Signing keystore is too small")
target.chmod(0o600)
properties = {
    "storeFile": target.as_posix(),
    "storePassword": os.environ["IPTV_ANDROID_STORE_PASSWORD"],
    "keyPassword": os.environ["IPTV_ANDROID_KEY_PASSWORD"],
    "keyAlias": os.environ["IPTV_ANDROID_KEY_ALIAS"]
}
for name, value in properties.items():
    if not value or "\n" in value or "\r" in value:
        sys.exit("Invalid secret value for " + name)
    # Java .properties uses escapes; reject unescaped delimiters and keep
    # passwords from appearing in any CI command.
    if "\\" in value or "=" in value or ":" in value:
        sys.exit("Secret " + name + " contains unsupported properties delimiter")
props_file = root / "key.properties"
props_file.write_text("".join(k + "=" + v + "\n" for k, v in properties.items()), encoding="utf-8")
props_file.chmod(0o600)
content = gradle.read_text(encoding="utf-8")
if "signingConfigs.getByName(\"release\")" in content:
    sys.exit("Release signing already configured; refusing duplicate injection")
if "buildTypes {" not in content or "android {" not in content:
    sys.exit("Unknown Flutter Gradle template")
prefix = """import java.io.FileInputStream
import java.util.Properties

val iptvSigning = Properties().apply {
    load(FileInputStream(rootProject.file("key.properties")))
}

"""
signing = """    signingConfigs {
        create("release") {
            keyAlias = iptvSigning.getProperty("keyAlias")
            keyPassword = iptvSigning.getProperty("keyPassword")
            storeFile = file(iptvSigning.getProperty("storeFile"))
            storePassword = iptvSigning.getProperty("storePassword")
        }
    }

"""
content = prefix + content
content = content.replace("    buildTypes {", signing + "    buildTypes {", 1)
found = "// IPTV+ downstream: debug signing removed; signed release requires external CI credentials."
if found not in content:
    sys.exit("Expected IPTV+ debug-signing removal marker is missing")
content = content.replace(found,
    'signingConfig = signingConfigs.getByName("release")', 1)
gradle.write_text(content, encoding="utf-8")
print("IPTV+ Flutter release signing configured (secrets hidden).")
