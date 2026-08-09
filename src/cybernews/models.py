from datetime import datetime

from pydantic import BaseModel, HttpUrl


class Article(BaseModel):
    id: str

    title: str
    url: HttpUrl

    source: str

    published_at: datetime | None = None
    fetched_at: datetime

    summary: str | None = None

    category: str | None = None

    importance_score: float | None = None

    cves: list[str] = []