import re
import urllib.parse
from crawlers import Crawler


class KawaiiCrawler(Crawler):
    site = "Kawaii Scans"
    url = "http://kawaii.ca/reader/"

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
        r_tmp = reg.findall(html)
        if not r_tmp:
            return False
        r = r_tmp[0]
        regex_page = "value=\"(.*?)\".*?>(.*?)<"
        reg_page = re.compile(regex_page)
        r_page = reg_page.findall(r)
        ret = [None] * len(r_page)
        pos = 0
        for x in r_page:
            url = chapter_url + x[0]
            html_image = self.get_html(url)
            regex_image = "<img src=\"(.*?)\".*?class=\"picture\" />"
            reg_image = re.compile(regex_image)
            r_image = reg_image.findall(html_image)[0]
            r_image = urllib.parse.quote(r_image)
            url_image = self.url + r_image
            name = x[1] + '.' + self.get_file_extension(url_image)
            ret[pos] = dict(url=url_image, name=name)
            pos += 1
        return ret
