from cybernews.sources.rss import RSSSource

TheHackersNews = RSSSource(
    name="TheHackersNews",
    feed_url="https://feeds.feedburner.com/TheHackersNews",
)

BleepingComputer = RSSSource(
    name="BleepingComputer",
    feed_url="https://www.bleepingcomputer.com/feed/",
)

KrebsOnSecurity = RSSSource(
    name="KrebsOnSecurity",
    feed_url="https://krebsonsecurity.com/feed/",
)

DarkReading = RSSSource(
    name="DarkReading",
    feed_url="https://www.darkreading.com/rss.xml",
)

SecurityWeek = RSSSource(
    name="SecurityWeek",
    feed_url="https://www.securityweek.com/feed/",
)

TheRecord = RSSSource(
    name="TheRecord",
    feed_url="https://therecord.media/feed",
)

SecurityAffairs = RSSSource(
    name="SecurityAffairs",
    feed_url="https://securityaffairs.co/feed",
)

GrahamCluley = RSSSource(
    name="GrahamCluley",
    feed_url="https://www.grahamcluley.com/feed/",
)

SophosNews = RSSSource(
    name="SophosNews",
    feed_url="https://news.sophos.com/en-us/feed/",
)

SchneierOnSecurity = RSSSource(
    name="SchneierOnSecurity",
    feed_url="https://www.schneier.com/blog/atom.xml",
)

CISA = RSSSource(
    name="CISA",
    feed_url="https://www.cisa.gov/uscert/ncas/all.xml",
)

UK_NCSC = RSSSource(
    name="UK_NCSC",
    feed_url="https://www.ncsc.gov.uk/api/1/services/v1/all-rss-feed.xml",
)

CERT_FR = RSSSource(
    name="CERT_FR",
    feed_url="https://www.cert.ssi.gouv.fr/feed/",
)

CERT_PL = RSSSource(
    name="CERT_PL",
    feed_url="https://cert.pl/en/rss.xml",
)

NCSC_NL = RSSSource(
    name="NCSC_NL",
    feed_url="https://feeds.ncsc.nl/nieuws.rss",
)

CERT_UA = RSSSource(
    name="CERT_UA",
    feed_url="https://cert.gov.ua/api/articles/rss",
)

ENISA = RSSSource(
    name="ENISA",
    feed_url="https://www.enisa.europa.eu/media/news-items/news-wires/RSS",
)

CERT_EU_ThreatIntel = RSSSource(
    name="CERT_EU_ThreatIntel",
    feed_url="https://cert.europa.eu/publications/threat-intelligence-rss",
)

CERT_EU_Advisories = RSSSource(
    name="CERT_EU_Advisories",
    feed_url="https://cert.europa.eu/publications/security-advisories-rss",
)

DNSC = RSSSource(
    name="DNSC",
    feed_url="https://dnsc.ro/feed",
)

SOURCES = [
    # Global news
    TheHackersNews,
    BleepingComputer,
    KrebsOnSecurity,
    DarkReading,
    SecurityWeek,
    TheRecord,
    SecurityAffairs,
    GrahamCluley,
    SophosNews,
    SchneierOnSecurity,
    # National CERTs
    CISA,
    UK_NCSC,
    CERT_FR,
    CERT_PL,
    NCSC_NL,
    CERT_UA,
    # EU-level
    ENISA,
    CERT_EU_ThreatIntel,
    CERT_EU_Advisories,
    # Romania
    DNSC,
]