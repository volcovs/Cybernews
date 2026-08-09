from datetime import datetime, timezone
import hashlib
from urllib.parse import urlsplit, urlunsplit

from cybernews.models import Article
from cybernews.sources.rss import RawArticle


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


def normalize(raw: RawArticle) -> Article:
    return Article(
        id=article_id(raw.url),
        title=raw.title,
        url=canonicalize_url(raw.url),
        source=raw.source,
        fetched_at=datetime.now(timezone.utc),
        summary=raw.summary,
    )