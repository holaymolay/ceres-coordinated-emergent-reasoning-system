#!/usr/bin/env python3
import json
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent

KNOWN_DIRS = {
    "ui-artifacts": "auto",
    "ui-contracts/examples": "event",
    "synchronizations/examples": "event",
    "skills/ui-intent-emit/examples": "intent",
    "concepts/ui-intent-protocol/handlers/reference": "intent",
}


def fail(file_path: Path, rule: str, suggestion: str) -> None:
    try:
        display_path = file_path.relative_to(ROOT)
    except ValueError:
        display_path = file_path
    message = (
        "UIP-STRUCTURAL-VIOLATION"
        f" | file: {display_path}"
        f" | rule: {rule}"
        f" | suggestion: {suggestion}"
    )
    print(message, file=sys.stderr)
    raise SystemExit(1)


def is_intent(path: Path) -> bool:
    return path.name.endswith(".intent.json")


def is_event(path: Path) -> bool:
    return path.name.endswith(".event.json")


def discover() -> list[dict[str, str]]:
    artifacts: dict[str, str] = {}

    for path in ROOT.rglob("*.intent.json"):
        artifacts[str(path)] = "intent"
    for path in ROOT.rglob("*.event.json"):
        artifacts[str(path)] = "event"

    for rel_dir, kind in KNOWN_DIRS.items():
        directory = ROOT / rel_dir
        if not directory.exists():
            continue
        for path in directory.glob("*.json"):
            if kind == "auto":
                if is_intent(path):
                    artifacts[str(path)] = "intent"
                elif is_event(path):
                    artifacts[str(path)] = "event"
                else:
                    continue
            else:
                artifacts[str(path)] = kind

    results = []
    for path_str, kind in sorted(artifacts.items()):
        path = Path(path_str)
        try:
            json.loads(path.read_text(encoding="utf-8"))
        except json.JSONDecodeError:
            fail(
                path,
                "valid-json",
                "Fix JSON syntax so the artifact can be parsed.",
            )
        results.append({"path": path_str, "type": kind})
    return results


def main() -> None:
    artifacts = discover()
    for artifact in artifacts:
        print(json.dumps(artifact, ensure_ascii=True))


if __name__ == "__main__":
    main()
