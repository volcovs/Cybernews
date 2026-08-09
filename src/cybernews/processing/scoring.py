import re

from cybernews.models import Article


def score_article(article: Article) -> float:
    score = 0.0

    text = (
        f"{article.title} "
        f"{article.summary or ''}"
    ).lower()

    # Vulnerabilities
    if article.cves:
        score += 20

    if "zero-day" in text or "zero day" in text:
        score += 25

    if "actively exploited" in text:
        score += 30

    if "remote code execution" in text or "rce" in text:
        score += 15

    # Malware / attacks
    if "ransomware" in text:
        score += 15

    if "supply chain" in text:
        score += 15

    # Major impact indicators
    if "critical infrastructure" in text:
        score += 15

    if "millions" in text:
        score += 10

    return min(score, 100)