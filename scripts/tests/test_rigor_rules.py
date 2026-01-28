import unittest

from scripts import rigor_rules


class RigorRulesTests(unittest.TestCase):
    def test_spec_map_symmetry_passes(self) -> None:
        spec_clauses = ["S-1", "S-2"]
        verifier_ids = ["V-1", "V-2"]
        spec_map = [
            {"spec_clause_id": "S-1", "verifier_id": "V-1"},
            {"spec_clause_id": "S-2", "verifier_id": "V-2"},
        ]
        errors = rigor_rules.validate_spec_map(spec_clauses, verifier_ids, spec_map)
        self.assertEqual(errors, [])

    def test_spec_map_missing_fails(self) -> None:
        spec_clauses = ["S-1", "S-2"]
        verifier_ids = ["V-1", "V-2"]
        spec_map = [
            {"spec_clause_id": "S-1", "verifier_id": "V-1"},
        ]
        errors = rigor_rules.validate_spec_map(spec_clauses, verifier_ids, spec_map)
        self.assertTrue(any("missing" in err for err in errors))

    def test_networked_requires_nondeterminism_manifest(self) -> None:
        task_meta = {"networked": True}
        errors = rigor_rules.require_nondeterminism_manifest(task_meta, None)
        self.assertTrue(any("nondeterminism" in err for err in errors))


if __name__ == "__main__":
    unittest.main()
