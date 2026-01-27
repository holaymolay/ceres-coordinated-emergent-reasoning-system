import tempfile
import unittest
from pathlib import Path

from scripts import policy_edit


class PolicyEditTests(unittest.TestCase):
    def setUp(self) -> None:
        self.tmp = tempfile.TemporaryDirectory()
        self.repo = Path(self.tmp.name)
        self.current = self.repo / "ceres.policy.yaml"
        self.proposed = self.repo / "ceres.policy.proposed.yaml"

    def tearDown(self) -> None:
        self.tmp.cleanup()

    def test_ensure_proposed_copies_current(self) -> None:
        self.current.write_text("version: 1\npolicy:\n  rigor_level: low\n", encoding="utf-8")
        created = policy_edit.ensure_proposed(self.current, self.proposed)
        self.assertTrue(created)
        self.assertTrue(self.proposed.exists())
        self.assertEqual(self.proposed.read_text(encoding="utf-8"), self.current.read_text(encoding="utf-8"))

    def test_ensure_proposed_no_overwrite(self) -> None:
        self.current.write_text("version: 1\npolicy:\n  rigor_level: low\n", encoding="utf-8")
        self.proposed.write_text("custom: true\n", encoding="utf-8")
        created = policy_edit.ensure_proposed(self.current, self.proposed)
        self.assertFalse(created)
        self.assertEqual(self.proposed.read_text(encoding="utf-8"), "custom: true\n")


if __name__ == "__main__":
    unittest.main()
