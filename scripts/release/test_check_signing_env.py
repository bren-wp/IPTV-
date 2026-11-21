import os
from pathlib import Path
import subprocess
import sys
import tempfile
import unittest

SCRIPT = Path(__file__).with_name("check_signing_env.py")
KEYS = (
    "IPTV_FREE_KEYSTORE_BASE64", "IPTV_FREE_STORE_PASSWORD",
    "IPTV_FREE_KEY_PASSWORD", "IPTV_FREE_KEY_ALIAS",
    "IPTV_PRO_KEYSTORE_BASE64", "IPTV_PRO_STORE_PASSWORD",
    "IPTV_PRO_KEY_PASSWORD", "IPTV_PRO_KEY_ALIAS",
)


class SigningGateTests(unittest.TestCase):
    def run_gate(self, event, complete):
        with tempfile.TemporaryDirectory() as path:
            output = Path(path) / "github-output"
            summary = Path(path) / "summary"
            env = {k: v for k, v in os.environ.items() if k not in KEYS}
            env.update({"GITHUB_EVENT_NAME": event, "GITHUB_OUTPUT": str(output),
                        "GITHUB_STEP_SUMMARY": str(summary)})
            if complete:
                env.update({key: "dummy-value" for key in KEYS})
            result = subprocess.run([sys.executable, str(SCRIPT)], env=env,
                                    capture_output=True, text=True, check=False)
            return result, output.read_text(), summary.read_text()

    def test_automatic_push_does_not_fail_without_signing_keys(self):
        result, output, summary = self.run_gate("push", False)
        self.assertEqual(result.returncode, 0)
        self.assertIn("ready=false", output)
        self.assertIn("NOT published", summary)
        self.assertNotIn("dummy-value", result.stdout)

    def test_manual_release_rejects_missing_signing_keys(self):
        result, output, _ = self.run_gate("workflow_dispatch", False)
        self.assertNotEqual(result.returncode, 0)
        self.assertIn("ready=false", output)

    def test_complete_signing_env_activates_release(self):
        result, output, summary = self.run_gate("push", True)
        self.assertEqual(result.returncode, 0)
        self.assertIn("ready=true", output)
        self.assertIn("signing configured", summary)


if __name__ == "__main__":
    unittest.main()
