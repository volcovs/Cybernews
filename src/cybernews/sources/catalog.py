from cybernews.sources.rss import RSSSource


TheHackersNews = RSSSource(
    name="TheHackersNews",
    feed_url="https://feeds.feedburner.com/TheHackersNews",
)


SOURCES = [
    TheHackersNews,
]