#!/usr/bin/env python3
"""Release signing gate: report absent GitHub Secrets before allocating build runners.

Never read key bytes into logs or save the values. Missing keys on an automatic
push do not pretend to create an edition-specific release; publication is
explicitly skipped. A manual release request without keys is an error.
"""
from __future__ import annotations

import os
from pathlib import Path

REQUIRED = (
    "IPTV_ANDROID_KEYSTORE_BASE64",
    "IPTV_ANDROID_STORE_PASSWORD",
    "IPTV_ANDROID_KEY_PASSWORD",
    "IPTV_ANDROID_KEY_ALIAS",
)


def report() -> bool:
    missing = [name for name in REQUIRED if not os.environ.get(name)]
    ready = not missing
    output = os.environ.get("GITHUB_OUTPUT")
    if output:
        with open(output, "a", encoding="utf-8") as fh:
            fh.write(f"ready={'true' if ready else 'false'}\n")
    summary_path = os.environ.get("GITHUB_STEP_SUMMARY")
    if missing:
        message = (
            "## IPTV+ release NOT published — signing not configured\n\n"
            "Missing **secret names** (not values): "
            + ", ".join(f"`{key}`" for key in missing)
            + "\n\nAdd these in **Settings → Secrets and variables → Actions → "
              "Repository secrets**. Keep original permanent IPTV+ signing key private.\n"
              "The Android and Windows native smoke checks remain separate. "
              "No placeholder APK/AAB or incomplete GitHub Release is allowed.\n"
        )
        print("RELEASE BLOCKED: missing signing secrets: " + ", ".join(missing))
        print("::warning title=IPTV+ release not published::Signing prerequisites are missing. See run summary.")
    else:
        message = "## IPTV+ release signing configured\n\nAll required IPTV+ secret names are populated. Native builds and signature validation follow.\n"
        print("Signing prerequisites are present. Actual certificates will be validated by the release build.")
    if summary_path:
        with open(summary_path, "a", encoding="utf-8") as fh:
            fh.write(message)
    return ready


if __name__ == "__main__":
    ready = report()
    if not ready and os.environ.get("GITHUB_EVENT_NAME") == "workflow_dispatch":
        raise SystemExit("Manual release rejected: configure the four Android signing secrets first.")
