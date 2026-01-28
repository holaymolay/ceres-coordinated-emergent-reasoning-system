# CERES UI (Read-Only)

This is a read-only UI scaffold for inspecting CERES artifacts. It does not mutate state and does not bypass governance.

## How To Run

```bash
cd ui
python -m http.server 8080
```

Open `http://localhost:8080` in a browser.

Windows users should run this via WSL (no Windows-native support).

## Data Sources (read-only)

The UI attempts to load artifacts from the repo root using relative paths:
- Planning: `task_graph.json`, `concept_map.json`, `required_syncs.json` (from a detected output directory)
- Arbitration: `logs/arbitration-decision.json`
- Concepts: `logs/concept-graph.json` (optional)
- Enforcement: `logs/events.jsonl`
- Policy: `ceres.policy.yaml` (macro settings; displayed read-only with CLI guidance)

If an artifact is missing, the UI displays a placeholder and continues.
