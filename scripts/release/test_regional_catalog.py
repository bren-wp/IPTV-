import sys
from pathlib import Path
import unittest

sys.path.insert(0, str(Path(__file__).resolve().parents[2] / "tools" / "clubtivi"))
from catalog import SOURCES, GROUPS, validate, as_flutter_entries, as_flutter_groups

class RegionalCatalogTests(unittest.TestCase):
    def test_catalog_directory_is_https_unique_and_opt_in(self):
        validate()
        self.assertGreaterEqual(len(SOURCES), 40)
        self.assertEqual(len(SOURCES), len({s["id"] for s in SOURCES}))
        self.assertTrue(all(s["url"].startswith("https://iptv-org.github.io/iptv/") for s in SOURCES))

    def test_region_priority_and_category_variety(self):
        self.assertEqual(GROUPS[:4], ["🇭🇷 Hrvatska", "🇸🇮 Slovenija",
                          "🇧🇦 Bosna i Hercegovina", "🇷🇸 Srbija"])
        names = " ".join(s["name"] for s in SOURCES)
        for label in ("Sport", "Filmovi", "Serije", "Crtani", "Dječji",
                      "Vijesti", "Dokumentarci", "Glazba", "Obrazovanje"):
            self.assertIn(label, names)

    def test_rendered_flutter_entries(self):
        out = as_flutter_entries()
        self.assertEqual(out.count("FreeTvProvider("), len(SOURCES))
        self.assertIn("group: '🇭🇷 Hrvatska'", out)
        self.assertIn("Ostali javni izvori", as_flutter_groups())
        self.assertNotIn("http://", out)

if __name__ == "__main__":
    unittest.main()
