import re
from typing import Dict, List


def classify(prompt: str) -> Dict[str, object]:
    """Classify prompt intent and scope heuristically."""
    lowered = prompt.lower()
    intent: str = "task"
    if any(word in lowered for word in ["refactor", "cleanup"]):
        intent = "refactor"
    if any(word in lowered for word in ["doc", "readme"]):
        intent = "documentation"
    if any(word in lowered for word in ["question", "what", "how" ]) and len(prompt.split()) < 25:
        intent = "question"

    destructive = any(token in lowered for token in ["rm -rf", "delete", "drop database", "destroy"])
    repos: List[str] = []
    for name in ["governance-orchestrator", "readme-spec-engine", "spec-compiler", "ui-constitution", "ui-pattern-registry"]:
        if name in lowered:
            repos.append(name)

    return {
        "detected_intent": intent,
        "destructive": destructive,
        "repos": sorted(set(repos))
    }
