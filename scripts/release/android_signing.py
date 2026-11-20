#!/usr/bin/env python3
"""Configure release signing for the Tauri-generated Android Gradle project.
Secrets are injected by GitHub Actions; private keys are never committed.
"""
import base64
import os
from pathlib import Path
import re

required = ("IPTV_ANDROID_KEYSTORE_BASE64", "IPTV_ANDROID_STORE_PASSWORD", "IPTV_ANDROID_KEY_PASSWORD", "IPTV_ANDROID_KEY_ALIAS")
missing = [key for key in required if not os.environ.get(key)]
if missing:
    raise SystemExit("Missing required Android signing secrets: " + ", ".join(missing))

android = Path("src-tauri/gen/android")
gradle = android / "app/build.gradle.kts"
if not gradle.is_file():
    raise SystemExit("Run 'tauri android init --ci' first: app/build.gradle.kts not found.")

key_path = (Path(os.environ.get("RUNNER_TEMP", "/tmp")) / "iptvplus-release-keystore.jks").resolve()
try:
    key_path.write_bytes(base64.b64decode(os.environ["IPTV_ANDROID_KEYSTORE_BASE64"], validate=True))
except (ValueError, Exception) as exc:
    raise SystemExit(f"Invalid base64 keystore secret: {type(exc).__name__}") from None
if key_path.stat().st_size < 128:
    raise SystemExit("Keystore file too small.")
key_path.chmod(0o600)
props = {
    "storeFile": str(key_path),
    "storePassword": os.environ["IPTV_ANDROID_STORE_PASSWORD"],
    "keyPassword": os.environ["IPTV_ANDROID_KEY_PASSWORD"],
    "keyAlias": os.environ["IPTV_ANDROID_KEY_ALIAS"],
}
# Java properties escaping; values containing a newline are rejected.
for name, value in props.items():
    if "\n" in value or "\r" in value:
        raise SystemExit(f"Invalid newline in signing value {name}")
(android / "keystore.properties").write_text("".join(f"{k}={v}\n" for k, v in props.items()), encoding="utf-8")
(android / "keystore.properties").chmod(0o600)

source = gradle.read_text(encoding="utf-8")
if 'signingConfigs.getByName("release")' in source:
    raise SystemExit("Release signing already configured; review manually.")
if "buildTypes {" not in source or 'getByName("release")' not in source:
    raise SystemExit("Unexpected Gradle template. Cannot safely inject signing configuration.")
imports = "import java.io.FileInputStream\nimport java.util.Properties\n"
if "import java.io.FileInputStream" not in source:
    source = imports + source
config = """signingConfigs {
        create("release") {
            val properties = Properties()
            val propertiesFile = rootProject.file("keystore.properties")
            properties.load(FileInputStream(propertiesFile))
            keyAlias = properties.getProperty("keyAlias")
            keyPassword = properties.getProperty("keyPassword")
            storeFile = file(properties.getProperty("storeFile"))
            storePassword = properties.getProperty("storePassword")
        }
    }

    """
source = source.replace("buildTypes {", config + "buildTypes {", 1)
source, count = re.subn(r'(getByName\("release"\)\s*\{)', r'\1\n            signingConfig = signingConfigs.getByName("release")', source, count=1)
if count != 1:
    raise SystemExit("Unable to activate release signing.")
gradle.write_text(source, encoding="utf-8")
print("Android signing configured (credentials redacted).")
