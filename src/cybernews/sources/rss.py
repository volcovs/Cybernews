from dataclasses import dataclass

import feedparser


@dataclass
class RawArticle:
    title: str
    url: str
    source: str
    published: str | None
    summary: str | None


class RSSSource:
    def __init__(self, name: str, feed_url: str):
        self.name = name
        self.feed_url = feed_url

    def fetch(self) -> list[RawArticle]:
        feed = feedparser.parse(self.feed_url)

        if feed.bozo and not feed.entries:
            raise RuntimeError(
                f"Failed to parse RSS feed: {self.feed_url}"
            )

        articles: list[RawArticle] = []

        for entry in feed.entries:
            title = entry.get("title", "").strip()
            url = entry.get("link", "").strip()

            if not title or not url:
                continue

            articles.append(
                RawArticle(
                    title=title,
                    url=url,
                    source=self.name,
                    published=entry.get("published"),
                    summary=entry.get("summary"),
                )
            )

        return articles