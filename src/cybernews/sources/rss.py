from dataclasses import dataclass
from datetime import datetime, timezone

import feedparser

@dataclass
class RawArticle:
    title: str
    url: str
    source: str
    published_at: datetime | None
    summary: str | None


class RSSSource:
    def __init__(self, name: str, feed_url: str):
        self.name = name
        self.feed_url = feed_url
        
    def fetch(self) -> list[RawArticle]:
        feed = feedparser.parse(self.feed_url)

        if feed.bozo and not feed.entries:
            return []

        articles: list[RawArticle] = []
        for entry in feed.entries:
            title = entry.get("title", "").strip()
            url = entry.get("link", "").strip()

            if not title or not url:
                continue

            published_at = None
            if entry.get("published_parsed"):
                published_at = datetime(
                    *entry.published_parsed[:6],
                    tzinfo=timezone.utc,
                )

            articles.append(
                RawArticle(
                    title=title,
                    url=url,
                    source=self.name,
                    published_at=published_at,
                    summary=entry.get("summary"),
                )
            )

        return articles
