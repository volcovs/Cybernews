import json
from datetime import datetime, timezone

from cybernews.models import Article
from cybernews.storage.dropbox import DropboxStorage


class ArticleRepository:
    def __init__(self, storage: DropboxStorage):
        self.storage = storage

    def _path_for_date(self, date) -> str:
        return f"articles/{date.isoformat()}.jsonl"

    def save_articles(self, articles: list[Article]) -> None:
        if not articles:
            return

        grouped: dict[str, list[Article]] = {}

        for article in articles:
            date = article.fetched_at.date()
            grouped.setdefault(date.isoformat(), []).append(article)

        for date_string, batch in grouped.items():
            path = f"articles/{date_string}.jsonl"

            existing: list[Article] = []

            if self.storage.exists(path):
                content = self.storage.read_text(path)

                for line in content.splitlines():
                    if line.strip():
                        existing.append(
                            Article.model_validate_json(line)
                        )

            existing_ids = {
                article.id
                for article in existing
            }

            new_articles = [
                article
                for article in batch
                if article.id not in existing_ids
            ]

            if not new_articles:
                continue

            all_articles = existing + new_articles

            content = "\n".join(
                article.model_dump_json()
                for article in all_articles
            ) + "\n"

            self.storage.write_text(path, content)

    def load_date(self, date) -> list[Article]:
        path = self._path_for_date(date)

        if not self.storage.exists(path):
            return []

        content = self.storage.read_text(path)

        return [
            Article.model_validate_json(line)
            for line in content.splitlines()
            if line.strip()
        ]