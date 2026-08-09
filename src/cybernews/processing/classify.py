import re


CATEGORIES = {
    "vulnerability": [
        r"\bcve-\d{4}-\d+\b",
        r"\bvulnerability\b",
        r"\bexploit\b",
        r"\bzero[- ]day\b",
        r"\brce\b",
        r"\bremote code execution\b",
    ],
    "malware": [
        r"\bmalware\b",
        r"\bransomware\b",
        r"\btrojan\b",
        r"\bstealer\b",
        r"\bbotnet\b",
        r"\bbackdoor\b",
    ],
    "breach": [
        r"\bdata breach\b",
        r"\bbreached\b",
        r"\bdata leak\b",
        r"\bstolen data\b",
    ],
    "threat_actor": [
        r"\bapt\d+\b",
        r"\bthreat actor\b",
        r"\bhacker group\b",
        r"\bcybercriminal\b",
    ],
}


def classify(title: str, summary: str | None) -> str:
    text = f"{title} {summary or ''}".lower()

    scores: dict[str, int] = {}

    for category, patterns in CATEGORIES.items():
        scores[category] = sum(
            1
            for pattern in patterns
            if re.search(pattern, text)
        )

    best_category = max(
        scores,
        key=scores.get,
    )

    if scores[best_category] == 0:
        return "other"

    return best_category