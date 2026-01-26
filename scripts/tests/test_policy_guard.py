import tempfile
import unittest
from pathlib import Path

from scripts import policy_guard


class PolicyGuardTests(unittest.TestCase):
    def setUp(self) -> None:
        self.tmp = tempfile.TemporaryDirectory()
        self.repo = Path(self.tmp.name)
        self.policy = self.repo / "ceres.policy.yaml"

    def tearDown(self) -> None:
        self.tmp.cleanup()

    def test_validate_policy_rejects_invalid(self) -> None:
        invalid = {"version": 0, "policy": {"rigor_level": "invalid"}}
        errors = policy_guard.validate_policy(invalid)
        self.assertTrue(errors)

    def test_warn_policy_flags_conflicts(self) -> None:
        policy = {
            "version": 1,
            "policy": {
                "rigor_level": "low",
                "autonomy_level": "advanced",
                "risk_tolerance": "low",
                "execution_continuity": "auto-safe",
                "observability_depth": "normal",
            },
        }
        warnings = policy_guard.warn_policy(policy)
        self.assertTrue(warnings)

    def test_diff_policy_detects_changes(self) -> None:
        current = {"policy": {"rigor_level": "low"}}
        proposed = {"policy": {"rigor_level": "high"}}
        diffs = policy_guard.diff_policy(current, proposed)
        self.assertEqual(diffs, ["policy.rigor_level: low -> high"])


if __name__ == "__main__":
    unittest.main()
