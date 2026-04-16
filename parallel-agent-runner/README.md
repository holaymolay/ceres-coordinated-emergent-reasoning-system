# CERES Parallel Agent Runner

Runs multiple agent commands (e.g., Codex CLI) in parallel with configurable concurrency, logging, and basic error handling.

## Usage
```bash
# Example: run three codex execs in parallel with max 2 concurrent
python parallel_runner.py --concurrency 2 \
  --cmd "codex exec --task task1" \
  --cmd "codex exec --task task2" \
  --cmd "codex exec --task task3"
```

## Flags
- `--cmd`: command to run (repeatable)
- `--concurrency`: max parallel processes (default: 2)
- `--log-file`: optional path to append structured logs (JSONL)

## Notes
- Outputs stdout/stderr for each command; returns non-zero if any command fails.
- Future: swap command runner to target other LLM CLIs (Gemini, etc.).
- Integrate with CERES governance: ensure commands originate from approved Task Plan entries.
