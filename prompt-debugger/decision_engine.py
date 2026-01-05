from typing import List, Tuple


def decide(issues: List[str], destructive: bool) -> Tuple[str, List[str]]:
    """Return status and suggested fixes."""
    suggested: List[str] = []
    status = "approved"
    if destructive:
        status = "rejected"
        suggested.append("Remove destructive instructions or scope them explicitly")
    elif issues:
        status = "needs-clarification"
        suggested.extend(issues)
    return status, suggested
