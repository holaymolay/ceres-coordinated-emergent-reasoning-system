import tempfile
import unittest
from pathlib import Path

from scripts import housekeeping


class HousekeepingTests(unittest.TestCase):
    def setUp(self) -> None:
        self.tmp = tempfile.TemporaryDirectory()
        self.repo = Path(self.tmp.name)
        self.todo = self.repo / "todo.md"
        self.completed = self.repo / "completed.md"

    def tearDown(self) -> None:
        self.tmp.cleanup()

    def test_sync_adds_completed_entry_and_clears_pending_note(self) -> None:
        self.todo.write_text(
            "# Todo\n\n## Current Focus\n- [x] Task A (completed locally; pending push hash)\n",
            encoding="utf-8",
        )
        self.completed.write_text("# Completed\n", encoding="utf-8")

        count, entries = housekeeping.sync_completed(
            todo_path=self.todo,
            completed_path=self.completed,
            push_hash="deadbeef",
            dry_run=False,
            include_all=True,
            prune=False,
        )
        self.assertEqual(count, 1)
        self.assertIn("Task A", entries[0])

        updated_todo = self.todo.read_text(encoding="utf-8")
        self.assertNotIn("pending push hash", updated_todo)
        completed_text = self.completed.read_text(encoding="utf-8")
        self.assertIn("Task A", completed_text)
        self.assertIn("push deadbeef", completed_text)

    def test_sync_skips_duplicate_entries(self) -> None:
        self.todo.write_text(
            "# Todo\n\n## Current Focus\n- [x] Task B\n",
            encoding="utf-8",
        )
        self.completed.write_text(
            "# Completed\n- [x] 2026-01-01 — Task B (push abcdef)\n",
            encoding="utf-8",
        )

        count, entries = housekeeping.sync_completed(
            todo_path=self.todo,
            completed_path=self.completed,
            push_hash="deadbeef",
            dry_run=False,
            include_all=True,
            prune=False,
        )
        self.assertEqual(count, 0)
        self.assertEqual(entries, [])

    def test_prune_removes_completed_tasks(self) -> None:
        self.todo.write_text(
            "# Todo\n\n## Current Focus\n- [x] Task C\n- [ ] Task D\n",
            encoding="utf-8",
        )
        self.completed.write_text(
            "# Completed\n- [x] 2026-01-01 — Task C (push abcdef)\n",
            encoding="utf-8",
        )

        count, entries = housekeeping.sync_completed(
            todo_path=self.todo,
            completed_path=self.completed,
            push_hash="deadbeef",
            dry_run=False,
            include_all=True,
            prune=True,
        )
        self.assertEqual(count, 0)
        updated = self.todo.read_text(encoding="utf-8")
        self.assertNotIn("Task C", updated)
        self.assertIn("Task D", updated)


if __name__ == "__main__":
    unittest.main()
