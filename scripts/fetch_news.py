from cybernews.processing.normalize import normalize
from cybernews.sources.catalog import SOURCES
from cybernews.storage.articles import ArticleRepository
from cybernews.storage.dropbox import DropboxStorage


def main() -> None:
    storage = DropboxStorage()
    repository = ArticleRepository(storage)

    total_new = 0

    for source in SOURCES:
        print(f"\nFetching {source.name}...")

        raw_articles = source.fetch()

        articles = [
            normalize(article)
            for article in raw_articles
        ]

        print(f"Found {len(articles)} articles.")

        repository.save_articles(articles)

        total_new += len(articles)

    print(f"\nProcessed {total_new} articles.")


if __name__ == "__main__":
    main()