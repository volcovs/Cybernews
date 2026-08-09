import feedparser

feed = feedparser.parse(
    "https://feeds.feedburner.com/TheHackersNews"
)

print("bozo:", feed.bozo)
print("entries:", len(feed.entries))

for entry in feed.entries[:5]:
    print(entry.title)
    print(entry.link)