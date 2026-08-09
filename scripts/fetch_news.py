from cybernews.processing.classify import classify
from cybernews.processing.normalize import (
    clean_summary,
    extract_cves,
    normalize,
)
from cybernews.processing.scoring import score_article
from cybernews.sources.catalog import SOURCES
from cybernews.storage.articles import ArticleRepository
from cybernews.storage.dropbox import DropboxStorage


def main() -> None:
    storage = DropboxStorage()
    repository = ArticleRepository(storage)

    total_fetched = 0
    total_new = 0

    for source in SOURCES:
        print(f"\nFetching {source.name}...")

        raw_articles = source.fetch()

        total_fetched += len(raw_articles)

        articles = []

        for raw in raw_articles:
            article = normalize(raw)

            article.category = classify(
                article.title,
                article.summary,
            )

            article.cves = extract_cves(
                article.title,
                article.summary,
            )

            article.importance_score = score_article(article)

            articles.append(article)

        new_articles = repository.save_articles(
            articles
        )

        total_new += len(new_articles)

        print(
            f"Fetched {len(articles)}, "
            f"new {len(new_articles)}"
        )

    print("\nDone.")
    print(f"Fetched: {total_fetched}")
    print(f"New:     {total_new}")


if __name__ == "__main__":
    main()