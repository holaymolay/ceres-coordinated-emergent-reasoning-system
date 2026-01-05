from typing import List


def assess(prompt: str, issues: List[str], destructive: bool) -> str:
    if destructive:
        return "high"
    if any("cross-repo" in issue for issue in issues):
        return "high"
    if any("too short" in issue for issue in issues):
        return "medium"
    return "low"
