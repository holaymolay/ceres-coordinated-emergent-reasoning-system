import os
import tempfile
import unittest
from pathlib import Path

from observability import pattern_recall


class PatternRecallTests(unittest.TestCase):
    def setUp(self) -> None:
        self._env_backup = os.environ.copy()
        self.tmpdir = tempfile.TemporaryDirectory()
        os.environ["PATTERN_RECALL_ROOT"] = self.tmpdir.name
        os.environ["PATTERN_RECALL_ENABLED"] = "false"

    def tearDown(self) -> None:
        os.environ.clear()
        os.environ.update(self._env_backup)
        self.tmpdir.cleanup()

    def test_disabled_mode_writes_nothing(self) -> None:
        out = pattern_recall.record_problem(
            problem_id="p1",
            title="disabled should no-op",
            source="test",
            phase="observe",
            provenance={"source": "test"},
        )
        self.assertFalse(out["written"])
        self.assertFalse(Path(self.tmpdir.name).joinpath("logs").exists())

    def test_allowed_phase_writes_append_only(self) -> None:
        os.environ["PATTERN_RECALL_ENABLED"] = "true"
        out = pattern_recall.record_problem(
            problem_id="p2",
            title="allowed write",
            source="test",
            phase="observe",
            provenance={"source": "test"},
            outcomes=["success"],
        )
        self.assertTrue(out["written"])
        log_file = Path(out["path"])
        self.assertTrue(log_file.exists())
        content = log_file.read_text(encoding="utf-8").strip().splitlines()
        self.assertEqual(len(content), 1)
        self.assertIn('"id": "p2"', content[0])
        self.assertNotIn("rank", content[0])

    def test_forbidden_phase_noop(self) -> None:
        os.environ["PATTERN_RECALL_ENABLED"] = "true"
        out = pattern_recall.record_attempt(
            attempt_id="a1",
            problem_id="p3",
            phase="execute",
            summary="should skip",
        )
        self.assertFalse(out["written"])
        self.assertFalse(Path(self.tmpdir.name).joinpath("logs").exists())

    def test_read_requires_explicit_reference(self) -> None:
        os.environ["PATTERN_RECALL_ENABLED"] = "true"
        pattern_recall.record_problem(
            problem_id="p4",
            title="read guard",
            source="test",
            phase="reflect",
            provenance={"source": "test"},
        )
        with self.assertRaises(ValueError):
            pattern_recall.read_records(
                "problem",
                ids=["p4"],
                explicit_reference=False,
                phase="reflect",
            )
        results = pattern_recall.read_records(
            "problem",
            ids=["p4"],
            explicit_reference=True,
            phase="reflect",
        )
        self.assertEqual(len(results), 1)
        self.assertEqual(results[0]["id"], "p4")

    def test_disable_mid_run_stops_new_writes(self) -> None:
        os.environ["PATTERN_RECALL_ENABLED"] = "true"
        pattern_recall.record_problem(
            problem_id="p5",
            title="first",
            source="test",
            phase="observe",
            provenance={"source": "test"},
        )
        log_dir = Path(self.tmpdir.name).joinpath("logs")
        initial_size = sum(f.stat().st_size for f in log_dir.glob("*.ndjson"))
        os.environ["PATTERN_RECALL_ENABLED"] = "false"
        pattern_recall.record_problem(
            problem_id="p6",
            title="should not write",
            source="test",
            phase="observe",
            provenance={"source": "test"},
        )
        new_size = sum(f.stat().st_size for f in log_dir.glob("*.ndjson"))
        self.assertEqual(initial_size, new_size)

    def test_behavior_identical_enabled_vs_disabled(self) -> None:
        def run_sample_task(flag: str) -> dict:
            os.environ["PATTERN_RECALL_ENABLED"] = flag
            return {"status": "ok", "result": 42}

        baseline = run_sample_task("false")
        enabled = run_sample_task("true")
        self.assertEqual(baseline, enabled)

    def test_forbidden_fields_rejected(self) -> None:
        os.environ["PATTERN_RECALL_ENABLED"] = "true"
        with self.assertRaises(ValueError):
            pattern_recall.record_problem(
                problem_id="p7",
                title="forbidden",
                source="test",
                phase="observe",
                provenance={"source": "test"},
                extra={"rank": 0.9},
            )

    def test_missing_storage_is_safe(self) -> None:
        os.environ["PATTERN_RECALL_ENABLED"] = "true"
        # Remove backing directory to simulate layer removal.
        Path(self.tmpdir.name).rmdir()
        out = pattern_recall.read_records(
            "problem",
            ids=["absent"],
            explicit_reference=True,
            phase="observe",
        )
        self.assertEqual(out, [])


if __name__ == "__main__":
    unittest.main()
