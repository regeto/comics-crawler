from crawler import Crawler
import re


class OotsCrawler(Crawler):
    site = "The Order of the Stick"
    url = "http://www.giantitp.com"
    search = None

    def get_chapters(self, series_url=""):
        html = self.get_html(self.url + "/comics/oots.html")
        regex = "\"ComicList\">(.*?)<A href=\"(.*?)\">(.*?)</A>"
        reg = re.compile(regex)
        r = reg.findall(html)
        r.reverse()
        ret = [None] * len(r)
        pos = 0
        for chapter in r:
            chapter_url = self.url + chapter[1]
            chapter_name = chapter[0] + chapter[2]
            ret[pos] = dict(url=chapter_url, name=chapter_name)
            pos += 1
        return ret


    def get_pages(self, chapter_url):
        html = self.get_html(chapter_url)
        regex = "(\/comics\/images\/.*?)\""
        reg = re.compile(regex)
        r = reg.findall(html)
        ret = [dict(url=self.url + r[0])]
        return ret
