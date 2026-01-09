import json
import os
import subprocess
import tempfile
import textwrap
import unittest
from pathlib import Path

from scripts import doctor


class DoctorTests(unittest.TestCase):
    def setUp(self) -> None:
        self.tmp = tempfile.TemporaryDirectory()
        self.repo = Path(self.tmp.name)
        self.workspace = self.repo / ".ceres" / "workspace"
        self.workspace.mkdir(parents=True, exist_ok=True)
        self.env_backup = os.environ.copy()
        os.environ["CERES_WORKSPACE"] = str(self.workspace)
        os.environ["CERES_HOME"] = str(self.repo / ".ceres")
        self.cwd_backup = os.getcwd()
        os.chdir(self.repo)
        # stub legacy script for removal-proof check
        (self.repo / "scripts").mkdir(parents=True, exist_ok=True)
        (self.repo / "scripts" / "preflight.sh").write_text("#!/usr/bin/env bash\necho ok\n", encoding="utf-8")
        (self.repo / "scripts" / "preflight.sh").chmod(0o755)
        # stub wrappers
        bin_dir = self.repo / ".ceres" / "bin"
        bin_dir.mkdir(parents=True, exist_ok=True)
        for name in ("preflight", "start-session", "export-handover"):
            path = bin_dir / name
            path.write_text("#!/usr/bin/env bash\nexit 0\n", encoding="utf-8")
            path.chmod(0o755)

    def tearDown(self) -> None:
        os.environ.clear()
        os.environ.update(self.env_backup)
        os.chdir(self.cwd_backup)
        self.tmp.cleanup()

    def test_workspace_detected(self) -> None:
        finding = doctor.check_workspace(os.environ)
        self.assertEqual(finding.status, "ok")
        self.assertIn("workspace", finding.evidence)

    def test_workspace_missing(self) -> None:
        os.environ["CERES_WORKSPACE"] = str(self.repo / ".ceres" / "absent")
        finding = doctor.check_workspace(os.environ)
        self.assertEqual(finding.status, "warning")
        self.assertEqual(finding.id, "workspace_missing")

    def test_core_lock_mismatch(self) -> None:
        core_dir = Path(os.environ["CERES_HOME"]) / "core"
        core_dir.mkdir(parents=True, exist_ok=True)
        subprocess.run(["git", "init"], cwd=core_dir, check=True, capture_output=True)
        subprocess.run(["git", "config", "user.email", "test@example.com"], cwd=core_dir, check=True)
        subprocess.run(["git", "config", "user.name", "Test User"], cwd=core_dir, check=True)
        (core_dir / "README.md").write_text("core", encoding="utf-8")
        subprocess.run(["git", "add", "."], cwd=core_dir, check=True, capture_output=True)
        subprocess.run(["git", "commit", "-m", "init"], cwd=core_dir, check=True, capture_output=True)
        current = subprocess.run(
            ["git", "rev-parse", "HEAD"], cwd=core_dir, check=True, capture_output=True, text=True
        ).stdout.strip()
        lock_path = Path(os.environ["CERES_HOME"]) / "core.lock"
        lock_path.write_text(
            textwrap.dedent(
                f"""\
                remote: test
                ref: main
                commit: deadbeef
                """
            ),
            encoding="utf-8",
        )
        finding = doctor.check_core_lock(self.repo, os.environ)
        self.assertEqual(finding.id, "core_pin_mismatch")
        self.assertEqual(finding.status, "error")
        self.assertEqual(finding.evidence["current_commit"], current)

        # Align lock -> expect ok
        lock_path.write_text(
            textwrap.dedent(
                f"""\
                remote: test
                ref: main
                commit: {current}
                """
            ),
            encoding="utf-8",
        )
        finding_ok = doctor.check_core_lock(self.repo, os.environ)
        self.assertEqual(finding_ok.status, "ok")

    def test_wrapper_check_warns_when_missing(self) -> None:
        for name in ("preflight", "start-session", "export-handover"):
            (self.repo / ".ceres" / "bin" / name).unlink()
        finding = doctor.check_wrappers(self.repo)
        self.assertEqual(finding.status, "warning")
        self.assertIn("missing", finding.evidence)

    def test_main_json_output_deterministic(self) -> None:
        result = doctor.main(["--json"])
        self.assertEqual(result, 0)
        findings = doctor.run_checks(self.repo, os.environ)
        human = doctor.render_human(findings)
        self.assertIn("workspace", human)

    def test_emit_signals_optional(self) -> None:
        # Should not raise even if signals module absent; emit_signals handles missing gracefully.
        findings = doctor.run_checks(self.repo, os.environ)
        doctor.emit_signals(findings, env=os.environ)


if __name__ == "__main__":
    unittest.main()
