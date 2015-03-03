from crawlers import *
from sources import *
from config import *

crawlers = [
    BatoCrawler(),
    DynastyCrawler(),
    EdenCrawler(),
    KawaiiCrawler(),
    KissCrawler(),
    OotsCrawler(),
]

sources = [
    batoto.sources,
    dynasty.sources,
    eden.sources,
    kawaii.sources,
    kiss.sources,
    oots.sources,
]

updates = []
for x in range(len(crawlers)):
    crawler = crawlers[x]
    source = sources[x]
    for src in source:
        updates += crawler.get_updates(src['url'], directory.global_prefix + src['dir'])
crawlers[0].download_updates(updates)
