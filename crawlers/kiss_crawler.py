import re
from crawlers import Crawler


class KissCrawler(Crawler):
    site = "Kissmanga"
    url = "http://kissmanga.com"

    def get_chapters(self, series_url):
        html = self.get_html(series_url)
        regex = "<td>\n<a href=\"(.*?)\".*?>\n(.*?)<\/a>\n<\/td>"
        reg = re.compile(regex)
        r = reg.findall(html)
        r.reverse()
        ret = [None] * len(r)
        pos = 0
        for x in r:
            ret[pos] = dict(url=self.url + x[0], name=self.get_complete_file_name(x[0]))
            pos += 1
        return ret

    def get_pages(self, chapter_url):
        html = self.get_html(chapter_url)
        regex = "lstImages.push\(\"(.*?)\"\);"
        reg = re.compile(regex)
        r = reg.findall(html)
        ret = [None] * len(r)
        pos = 0
        for x in r:
            ret[pos] = dict(url=x, name=self.get_complete_file_name(x))
            pos += 1
        return ret
