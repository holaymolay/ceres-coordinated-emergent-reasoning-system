import json
import os
import shutil
import subprocess
import sys
import tempfile
import unittest
from pathlib import Path

REPO_ROOT = Path(__file__).resolve().parents[2]
RUN_SCRIPT = REPO_ROOT / "scripts" / "iteration" / "run.py"


def run_cmd(cmd, cwd=None, env=None):
    env_final = os.environ.copy()
    if env:
        env_final.update(env)
    return subprocess.run(
        cmd,
        cwd=cwd,
        env=env_final,
        capture_output=True,
        text=True,
        check=False,
    )


class IterationToolTests(unittest.TestCase):
    def setUp(self) -> None:
        self.tmp = tempfile.TemporaryDirectory()
        self.repo = Path(self.tmp.name)
        self.backlog = self.repo / "backlog.json"
        self.progress = self.repo / "progress.jsonl"

    def tearDown(self) -> None:
        self.tmp.cleanup()

    def _write_backlog(self, items) -> None:
        self.backlog.write_text(json.dumps(items), encoding="utf-8")

    def test_deterministic_selection_tie_break(self) -> None:
        items = [
            {"id": "b", "priority": 5, "passes": False},
            {"id": "a", "priority": 5, "passes": False},
            {"id": "c", "priority": 4, "passes": False},
        ]
        self._write_backlog(items)
        result = run_cmd(
            [
                sys.executable,
                str(RUN_SCRIPT),
                "--backlog",
                str(self.backlog),
                "--progress",
                str(self.progress),
                "--dry-run",
            ],
            cwd=self.repo,
        )
        self.assertEqual(result.returncode, 0, result.stderr)
        payload = json.loads(result.stdout)
        self.assertEqual(payload["selected_id"], "a")

    def test_dry_run_performs_no_writes(self) -> None:
        items = [{"id": "a", "priority": 1, "passes": False}]
        self._write_backlog(items)
        before = self.backlog.read_text(encoding="utf-8")
        result = run_cmd(
            [
                sys.executable,
                str(RUN_SCRIPT),
                "--backlog",
                str(self.backlog),
                "--progress",
                str(self.progress),
                "--dry-run",
            ],
            cwd=self.repo,
        )
        self.assertEqual(result.returncode, 0, result.stderr)
        after = self.backlog.read_text(encoding="utf-8")
        self.assertEqual(before, after)
        self.assertFalse(self.progress.exists())

    def test_writes_limited_to_owned_files(self) -> None:
        items = [{"id": "a", "priority": 1, "passes": False}]
        self._write_backlog(items)
        sentinel = self.repo / "sentinel.txt"
        sentinel.write_text("keep", encoding="utf-8")
        result = run_cmd(
            [
                sys.executable,
                str(RUN_SCRIPT),
                "--backlog",
                str(self.backlog),
                "--progress",
                str(self.progress),
                "--set-pass",
                "true",
            ],
            cwd=self.repo,
        )
        self.assertEqual(result.returncode, 0, result.stderr)
        self.assertTrue(self.progress.exists())
        self.assertEqual(sentinel.read_text(encoding="utf-8"), "keep")
        files = sorted(p.name for p in self.repo.iterdir())
        self.assertEqual(files, ["backlog.json", "progress.jsonl", "sentinel.txt"])

    def test_removal_does_not_break_core_imports(self) -> None:
        temp_root = Path(self.tmp.name) / "minimal"
        scripts_dir = temp_root / "scripts"
        scripts_dir.mkdir(parents=True, exist_ok=True)
        shutil.copy(REPO_ROOT / "scripts" / "doctor.py", scripts_dir / "doctor.py")
        result = run_cmd(
            [sys.executable, "-c", "import scripts.doctor; print('ok')"],
            cwd=temp_root,
            env={"PYTHONPATH": str(temp_root)},
        )
        self.assertEqual(result.returncode, 0, result.stderr)
        self.assertIn("ok", result.stdout)


if __name__ == "__main__":
    unittest.main()
