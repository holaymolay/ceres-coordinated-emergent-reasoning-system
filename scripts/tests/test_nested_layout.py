import os
import shutil
import subprocess
import tempfile
import textwrap
import unittest
from pathlib import Path

REPO_ROOT = Path(__file__).resolve().parents[2]
WRAPPER_SRC = REPO_ROOT / ".ceres" / "bin"


def run(cmd, cwd, env=None):
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


def write_exec(path: Path, content: str) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(content, encoding="utf-8")
    path.chmod(0o755)


class NestedLayoutWrapperTests(unittest.TestCase):
    def setUp(self) -> None:
        self.tmp = tempfile.TemporaryDirectory()
        self.repo = Path(self.tmp.name) / "repo"
        self.repo.mkdir(parents=True, exist_ok=True)

    def tearDown(self) -> None:
        self.tmp.cleanup()

    def _copy_wrappers(self) -> Path:
        dest = self.repo / ".ceres" / "bin"
        shutil.copytree(WRAPPER_SRC, dest, dirs_exist_ok=True)
        return dest

    def _make_stub_preflight(self, target: Path) -> None:
        write_exec(
            target / "scripts" / "preflight.sh",
            textwrap.dedent(
                """\
                #!/usr/bin/env bash
                set -euo pipefail
                echo "workspace=${CERES_WORKSPACE:-unset} args:$*"
                out="${CERES_WORKSPACE:-.}/artifact.txt"
                mkdir -p "$(dirname "$out")"
                echo "artifact" > "$out"
                """
            ),
        )

    def test_parity_workspace_vs_legacy(self) -> None:
        bin_dir = self._copy_wrappers()
        self._make_stub_preflight(self.repo)

        workspace = self.repo / ".ceres" / "workspace"
        workspace.mkdir(parents=True, exist_ok=True)

        wrapper = bin_dir / "preflight"
        result_wrapper = run([str(wrapper)], cwd=self.repo)
        self.assertEqual(result_wrapper.returncode, 0, result_wrapper.stderr)

        result_legacy = run(
            [str(self.repo / "scripts" / "preflight.sh")],
            cwd=self.repo,
            env={"CERES_WORKSPACE": str(workspace)},
        )
        self.assertEqual(result_legacy.returncode, 0, result_legacy.stderr)
        self.assertEqual(result_wrapper.stdout.strip(), result_legacy.stdout.strip())
        self.assertEqual(
            (workspace / "artifact.txt").read_text(encoding="utf-8").strip(), "artifact"
        )

    def test_fallback_without_workspace(self) -> None:
        bin_dir = self._copy_wrappers()
        self._make_stub_preflight(self.repo)
        wrapper = bin_dir / "preflight"

        result_wrapper = run([str(wrapper)], cwd=self.repo)
        self.assertEqual(result_wrapper.returncode, 0, result_wrapper.stderr)
        out_path = self.repo / "artifact.txt"
        self.assertTrue(out_path.exists())

        result_direct = run(
            [str(self.repo / "scripts" / "preflight.sh")],
            cwd=self.repo,
            env={"CERES_WORKSPACE": str(self.repo)},
        )
        self.assertEqual(result_direct.returncode, 0, result_direct.stderr)
        self.assertEqual(result_wrapper.stdout.strip(), result_direct.stdout.strip())

    def test_core_lock_mismatch_fails_closed(self) -> None:
        bin_dir = self._copy_wrappers()
        core_dir = self.repo / ".ceres" / "core"
        (core_dir / "scripts").mkdir(parents=True, exist_ok=True)
        # Initialize minimal git repo to produce a commit hash.
        run(["git", "init"], cwd=core_dir)
        write_exec(core_dir / "scripts" / "preflight.sh", "#!/usr/bin/env bash\necho core\n")
        run(["git", "add", "."], cwd=core_dir)
        run(["git", "commit", "-m", "init"], cwd=core_dir)
        current_commit = (
            run(["git", "rev-parse", "HEAD"], cwd=core_dir).stdout.strip()
        )
        # Write mismatching core.lock
        lock_path = self.repo / ".ceres" / "core.lock"
        lock_path.parent.mkdir(parents=True, exist_ok=True)
        lock_path.write_text(
            f"remote: test\nref: test\ncommit: deadbeef\n", encoding="utf-8"
        )

        wrapper = bin_dir / "preflight"
        result = run([str(wrapper)], cwd=self.repo)
        self.assertNotEqual(result.returncode, 0)
        self.assertIn("core.lock commit", result.stderr)

        # Now align lock and expect success.
        lock_path.write_text(
            f"remote: test\nref: test\ncommit: {current_commit}\n", encoding="utf-8"
        )
        result_ok = run([str(wrapper)], cwd=self.repo)
        self.assertEqual(result_ok.returncode, 0, result_ok.stderr)

    def test_removal_of_ceres_falls_back_to_legacy(self) -> None:
        self._make_stub_preflight(self.repo)
        # Remove .ceres entirely
        shutil.rmtree(self.repo / ".ceres", ignore_errors=True)
        result = run([str(self.repo / "scripts" / "preflight.sh")], cwd=self.repo)
        self.assertEqual(result.returncode, 0, result.stderr)
        self.assertIn("workspace=", result.stdout)


if __name__ == "__main__":
    unittest.main()
