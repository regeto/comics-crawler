from crawlers import *
from sources import *

# directory prefix
# use this if the sources only list directories relative to some sort of comic folder
directory = ""

def update_batoto():
    do_update(BatoCrawler(), batoto.sources)

def update_dynasty():
    do_update(DynastyCrawler(), dynasty.sources)

def update_eden():
    do_update(EdenCrawler(), eden.sources)

def update_kawaii():
    do_update(KawaiiCrawler(), kawaii.sources)

def update_oots():
    do_update(OotsCrawler(), oots.sources)

def update_smackjeeves():
    do_update(SmackjeevesCrawler(), smackjeeves.sources)

def do_update(crawler, list):
    for series in list:
        crawler.download_series(series['url'],
                                directory + series['dir'],
                                force='force' in series,
                                oneshot='oneshot' in series,
                                webcomic='webcomic' in series,
                                )

def update_all():
    update_batoto()
    update_dynasty()
    update_eden()
    update_kawaii()
    update_oots()
    update_smackjeeves()

update_all()