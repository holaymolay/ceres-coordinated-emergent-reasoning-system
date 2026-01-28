import json
import tempfile
import unittest
from pathlib import Path

from scripts import rigor_runner


def write_exec(path: Path, content: str) -> None:
    path.write_text(content, encoding="utf-8")
    path.chmod(0o755)


class RigorRunnerTests(unittest.TestCase):
    def setUp(self) -> None:
        self.tmp = tempfile.TemporaryDirectory()
        self.repo = Path(self.tmp.name)

    def tearDown(self) -> None:
        self.tmp.cleanup()

    def test_passing_and_failing_verifiers(self) -> None:
        ok_file = self.repo / "ok.txt"
        ok_file.write_text("OK\n", encoding="utf-8")

        pass_script = self.repo / "verifier_pass.sh"
        fail_script = self.repo / "verifier_fail.sh"

        write_exec(
            pass_script,
            "#!/usr/bin/env bash\nset -e\n[[ \"$(cat ok.txt)\" == \"OK\" ]]\n",
        )
        write_exec(
            fail_script,
            "#!/usr/bin/env bash\nset -e\n[[ \"$(cat ok.txt)\" == \"NO\" ]]\n",
        )

        verifiers = [
            {"id": "V-PASS", "command": str(pass_script)},
            {"id": "V-FAIL", "command": str(fail_script)},
        ]

        results = rigor_runner.run_verifiers(verifiers, cwd=self.repo)
        statuses = {entry["id"]: entry["status"] for entry in results}
        self.assertEqual(statuses["V-PASS"], "pass")
        self.assertEqual(statuses["V-FAIL"], "fail")

    def test_oracle_passes_verifier(self) -> None:
        output_file = self.repo / "output.txt"

        oracle_script = self.repo / "oracle.sh"
        verifier_script = self.repo / "verifier.sh"

        write_exec(
            oracle_script,
            "#!/usr/bin/env bash\nset -e\necho OK > output.txt\n",
        )
        write_exec(
            verifier_script,
            "#!/usr/bin/env bash\nset -e\n[[ \"$(cat output.txt)\" == \"OK\" ]]\n",
        )

        result = rigor_runner.run_oracle_and_verify(
            {"script": str(oracle_script)},
            [{"id": "V-1", "command": str(verifier_script)}],
            cwd=self.repo,
        )
        self.assertEqual(result["oracle"]["exit_code"], 0)
        self.assertEqual(result["verifiers"][0]["status"], "pass")

    def test_exploit_probe_is_always_flagged(self) -> None:
        probe_script = self.repo / "probe.sh"
        write_exec(
            probe_script,
            "#!/usr/bin/env bash\necho exploit\n",
        )
        result = rigor_runner.run_exploit_probe({"script": str(probe_script)}, cwd=self.repo)
        self.assertTrue(result["flagged"])
        self.assertEqual(result["status"], "flagged")

    def test_verify_cli_reports_fail(self) -> None:
        ok_file = self.repo / "ok.txt"
        ok_file.write_text("OK\n", encoding="utf-8")
        pass_script = self.repo / "verifier_pass.sh"
        fail_script = self.repo / "verifier_fail.sh"
        write_exec(
            pass_script,
            "#!/usr/bin/env bash\nset -e\n[[ \"$(cat ok.txt)\" == \"OK\" ]]\n",
        )
        write_exec(
            fail_script,
            "#!/usr/bin/env bash\nset -e\n[[ \"$(cat ok.txt)\" == \"NO\" ]]\n",
        )
        rigor_path = self.repo / "rigor.json"
        rigor_path.write_text(
            json.dumps(
                {
                    "verifiers": [
                        {"id": "V-PASS", "description": "ok", "command": str(pass_script)},
                        {"id": "V-FAIL", "description": "no", "command": str(fail_script)},
                    ]
                }
            ),
            encoding="utf-8",
        )
        from scripts import rigor

        result = rigor.main(["verify", "--rigor", str(rigor_path)])
        self.assertEqual(result, 1)


if __name__ == "__main__":
    unittest.main()
