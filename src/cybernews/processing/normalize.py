from datetime import datetime, timezone
import hashlib
import re
from urllib.parse import urlsplit, urlunsplit

from cybernews.models import Article
from cybernews.sources.rss import RawArticle
from cybernews.processing.classify import classify
from cybernews.processing.scoring import score_article


def canonicalize_url(url: str) -> str:
    parts = urlsplit(url.strip())

    return urlunsplit(
        (
            parts.scheme.lower(),
            parts.netloc.lower(),
            parts.path.rstrip("/"),
            parts.query,
            "",
        )
    )


def article_id(url: str) -> str:
    canonical_url = canonicalize_url(url)

    return hashlib.sha256(
        canonical_url.encode("utf-8")
    ).hexdigest()

from bs4 import BeautifulSoup

def clean_summary(summary: str | None) -> str | None:
    if not summary:
        return None

    text = BeautifulSoup(summary, "html.parser").get_text(
        " ",
        strip=True,
    )

    return text or None

CVE_PATTERN = re.compile(
    r"\bCVE-\d{4}-\d{4,7}\b",
    re.IGNORECASE,
)

def extract_cves(title: str, summary: str | None) -> list[str]:
    text = f"{title} {summary or ''}"

    return sorted(
        {
            match.upper()
            for match in CVE_PATTERN.findall(text)
        }
    )

def normalize(raw: RawArticle) -> Article:
    article = Article(
        id=article_id(raw.url),
        title=raw.title,
        url=canonicalize_url(raw.url),
        source=raw.source,
        published_at=raw.published_at,
        fetched_at=datetime.now(timezone.utc),
        summary=clean_summary(raw.summary),
        category=classify(raw.title, clean_summary(raw.summary)),
        cves=extract_cves(raw.title, clean_summary(raw.summary))
    )

    article.importance_score = score_article(article)
    return article