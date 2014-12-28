import re
from crawlers import Crawler


class KawaiiCrawler(Crawler):
    site = "Kawaii Scans"
    url = "http://kawaii.ca"

    def get_chapters(self, series_url):
        if not series_url[-1] == "/":
            series_url += "/"
        html = self.get_html(series_url)
        regex = "<select name=\"chapter\".*?>(.*?)<\/select>"
        reg = re.compile(regex)
        r = reg.findall(html)[0]
        regex_chapters = "value=\"(.*?)\".*?>(.*?)<\/option>"
        reg_chapters = re.compile(regex_chapters)
        r_chapters = reg_chapters.findall(r)
        ret = [None] * len(r_chapters)
        pos = 0
        for x in r_chapters:
            url = series_url + x[0]
            name = x[1]
            ret[pos] = dict(url=url, name=name)
            pos += 1
        return ret

    def get_pages(self, chapter_url):
        if not chapter_url[-1] == "/":
            chapter_url += "/"
        html = self.get_html(chapter_url)
        regex = "<select name=\"page\".*?>(.*?)<\/select>"
        reg = re.compile(regex)
        r = reg.findall(html)[0]
        regex_page = "value=\"(.*?)\".*?>(.*?)<"
        reg_page = re.compile(regex_page)
        r_page = reg_page.findall(r)
        ret = [None] * len(r_page)
        pos = 0
        for x in r_page:
            url = chapter_url + x[0]
            name = x[1]
            ret[pos] = dict(url=url, name=name)
            pos += 1
        return ret
