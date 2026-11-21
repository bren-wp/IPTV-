"""Ensure unified IPTV+ release is intentionally unsigned and uses no secrets."""
from pathlib import Path
import unittest

ROOT = Path(__file__).resolve().parents[2]

class UnsignedReleasePolicyTests(unittest.TestCase):
    def test_no_android_signing_secrets_in_release_workflow(self):
        content = (ROOT / ".github/workflows/verified-release.yml").read_text(encoding="utf-8")
        self.assertNotIn("secrets.IPTV_ANDROID", content)
        self.assertNotIn("sign_flutter_android.py", content)
        self.assertNotIn("signing-readiness:", content)
        self.assertIn("collect_unsigned_android.py", content)
        collector = (ROOT / "scripts/release/collect_unsigned_android.py").read_text(encoding="utf-8")
        self.assertIn("-Unsigned.apk", collector)
        self.assertIn("-Unsigned.aab", collector)
        self.assertIn("apksigner", collector)

    def test_one_edition_only(self):
        content = (ROOT / "tools/clubtivi/prepare.py").read_text(encoding="utf-8")
        self.assertIn('APP_ID = "com.brendigo.iptvplus"', content)
        self.assertIn("FeatureGate.setTier(AppTier.pro)", content)
        self.assertNotIn("APP_IDS", content)
        self.assertNotIn('parser.add_argument("--edition"', content)

    def test_release_artifacts_explicitly_marked_unsigned(self):
        validator = (ROOT / "scripts/release/validate_artifacts.py").read_text(encoding="utf-8")
        notes = (ROOT / "scripts/release/notes.py").read_text(encoding="utf-8")
        self.assertIn("-Unsigned.apk", validator)
        self.assertIn("-Unsigned.aab", validator)
        self.assertIn("NE MOŽE se instalirati", notes)
        self.assertIn("Google Play", notes)

if __name__ == "__main__":
    unittest.main()
