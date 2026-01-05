import hashlib
from typing import Dict, List


def build(prompt: str, detected_intent: str, repos: List[str], risk_level: str, issues: List[str], status: str, suggested: List[str]) -> Dict[str, object]:
    prompt_id = hashlib.sha1(prompt.encode("utf-8")).hexdigest()
    return {
        "prompt_id": prompt_id,
        "status": status,
        "detected_intent": detected_intent,
        "scope": {
            "repos": repos,
            "concepts": []
        },
        "risk_level": risk_level,
        "issues": issues,
        "suggested_fix": suggested,
        "decision_rationale": rationale(status, issues, risk_level)
    }


def rationale(status: str, issues: List[str], risk_level: str) -> str:
    if status == "approved":
        return "No blocking issues detected; risk acceptable."
    if status == "needs-clarification":
        return f"Blocked by issues: {', '.join(issues)}"
    return f"Rejected due to issues: {', '.join(issues)} (risk {risk_level})"
