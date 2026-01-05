from typing import List


def validate(prompt: str) -> List[str]:
    """Return a list of structural issues with the prompt."""
    issues: List[str] = []
    if not prompt.strip():
        issues.append("Prompt is empty")
    words = prompt.strip().split()
    if len(words) < 3:
        issues.append("Prompt too short to classify deterministically")
    if "and" in prompt and prompt.count("?") > 1:
        issues.append("Contains multiple questions; ask one bounded question")
    if "all" in prompt.lower() and "repos" in prompt.lower():
        issues.append("Possible cross-repo instruction without scope")
    return issues
