from crawler import Crawler
import re


class SmackjeevesCrawler(Crawler):
    site = "Smackjeeves"
    url = "smackjeeves.com"
    search = "http://www.smackjeeves.com/search.php?submit=submit&comic_title=%s"

    def get_chapters(self, series_url):
        prefix = series_url.split(".")[0] + "."
        html = self.get_html(series_url)
        regex = "<option.*?value=\"(/comics/.*?)\".*?>(.*?)<\/option>"
        reg = re.compile(regex)
        r = reg.findall(html)
        ret = [None] * len(r)
        pos = 0
        for x in r:
            ret[pos] = dict(url=prefix + self.url + x[0], name=x[1])
            pos += 1
        return ret

    def get_pages(self, chapter_url):
        html = self.get_html(chapter_url)
        regex = "src=\"(.*?)\".*?\"comic_image\""
        reg = re.compile(regex)
        r = reg.findall(html)
        ret = [dict(url=r[0])]
        return ret
