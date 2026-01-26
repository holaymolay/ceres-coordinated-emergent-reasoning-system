import json
import tempfile
import unittest
from pathlib import Path

from scripts import verify_verifier_evidence


class VerifierEvidenceTests(unittest.TestCase):
    def setUp(self) -> None:
        self.tmp = tempfile.TemporaryDirectory()
        self.repo = Path(self.tmp.name)
        self.objective = self.repo / "objective-contract.json"
        self.evidence = self.repo / "verifier-evidence.json"

    def tearDown(self) -> None:
        self.tmp.cleanup()

    def _write_objective(self, claims, mode="advisory") -> None:
        payload = {
            "goal": "test",
            "status": "committed",
            "success_criteria": ["criterion"],
            "verifiable_claims": claims,
            "verifier_evidence_policy": {"mode": mode},
        }
        self.objective.write_text(json.dumps(payload), encoding="utf-8")

    def _write_evidence(self, records) -> None:
        payload = {"records": records}
        self.evidence.write_text(json.dumps(payload), encoding="utf-8")

    def test_passes_when_evidence_present(self) -> None:
        self._write_objective([
            {"id": "claim-1", "description": "check", "verifier_type": "exec"}
        ], mode="enforce")
        self._write_evidence([
            {
                "spec_id": "spec-1",
                "claim_id": "claim-1",
                "verifier_type": "exec",
                "verifier_input_ref": "input.txt",
                "verifier_output_ref": "output.txt",
                "pass_fail": "pass",
                "timestamp": "2026-01-01T00:00:00Z",
            }
        ])
        result = verify_verifier_evidence.main([
            "--objective",
            str(self.objective),
            "--evidence",
            str(self.evidence),
            "--mode",
            "enforce",
        ])
        self.assertEqual(result, 0)

    def test_fails_when_evidence_missing(self) -> None:
        self._write_objective([
            {"id": "claim-1", "description": "check", "verifier_type": "exec"}
        ], mode="enforce")
        result = verify_verifier_evidence.main([
            "--objective",
            str(self.objective),
            "--evidence",
            str(self.evidence),
            "--mode",
            "enforce",
        ])
        self.assertEqual(result, 1)


if __name__ == "__main__":
    unittest.main()
