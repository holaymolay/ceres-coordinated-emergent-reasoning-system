import json
import os
import tempfile
import unittest
from datetime import datetime, timezone
from pathlib import Path
from typing import List, Dict

from observability import signals


class SignalsEmitterTests(unittest.TestCase):
    def setUp(self) -> None:
        self._env_backup = os.environ.copy()
        self.tmp = tempfile.TemporaryDirectory()
        self.workspace = Path(self.tmp.name) / ".ceres" / "workspace"
        self.workspace.mkdir(parents=True, exist_ok=True)
        os.environ["CERES_WORKSPACE"] = str(self.workspace)

    def tearDown(self) -> None:
        os.environ.clear()
        os.environ.update(self._env_backup)
        self.tmp.cleanup()

    def test_fail_closed_without_workspace(self) -> None:
        os.environ.pop("CERES_WORKSPACE", None)
        with self.assertRaises(FileNotFoundError):
            signals.emit_signals([], env=os.environ)

    def test_emit_appends_and_prints(self) -> None:
        buf: List[str] = []

        class Sink:
            def write(self, data: str) -> None:
                buf.append(data)

        findings: List[Dict] = [
            {
                "id": "core_pin_mismatch",
                "severity": "warning",
                "source": "doctor",
                "message": "core.lock does not match core submodule.",
            }
        ]
        emitted = signals.emit_signals(
            findings,
            config_state={"pattern_recall_enabled": True},
            env=os.environ,
            out=Sink(),
            now=datetime(2024, 1, 1, tzinfo=timezone.utc),
            last_audit_at="2023-09-01T00:00:00Z",
        )
        events_path = self.workspace / "events.jsonl"
        self.assertTrue(events_path.exists())
        lines = events_path.read_text(encoding="utf-8").strip().splitlines()
        # findings + config + overdue audit
        self.assertEqual(len(lines), 3)
        for line in lines:
            data = json.loads(line)
            self.assertIn("timestamp", data)
            self.assertNotIn("action", data)
        self.assertEqual(len(emitted), 3)
        self.assertTrue(any("core_pin_mismatch" in b for b in buf))
        self.assertTrue(any("pattern_recall_enabled" in b for b in buf))
        self.assertTrue(any("self_audit_overdue" in json.loads(line)["id"] for line in lines))

    def test_forbidden_fields_rejected(self) -> None:
        bad = [
            {
                "id": "workspace_missing",
                "severity": "warning",
                "message": "missing",
                "source": "doctor",
                "recommendation": "auto-fix",
            }
        ]
        with self.assertRaises(ValueError):
            signals.emit_signals(bad, env=os.environ)

    def test_deterministic_timestamp(self) -> None:
        now = datetime(2024, 2, 3, 4, 5, 6, tzinfo=timezone.utc)
        emitted = signals.emit_signals(
            [
                {
                    "id": "legacy_mode_active",
                    "severity": "info",
                    "source": "doctor",
                    "message": "legacy mode",
                }
            ],
            env=os.environ,
            now=now,
        )
        self.assertEqual(emitted[0]["timestamp"], "2024-02-03T04:05:06Z")


if __name__ == "__main__":
    unittest.main()
