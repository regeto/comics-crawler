from crawler import Crawler
import re


class BatoCrawler(Crawler):
    site = "Batoto"
    url = "http://bato.to"
    search = "http://bato.to/search?name=%s"

    def get_chapters(self, series_url):
        html = self.get_html(series_url)
        regex = "<tr class=\"row lang_English chapter_row\">(.*?)<\/tr>"
        reg = re.compile(regex, re.DOTALL)
        r = reg.findall(html)
        # reversed list because batoto lists the most recent chapter at the top
        r.reverse()
        regex_url = "<a href=\"(http:\/\/bato\.to\/read\/_\/.*?)\">"
        reg_url = re.compile(regex_url)
        regex_name = "<img.*?>(.*?)<\/a>"
        reg_name = re.compile(regex_name)
        ret = [None] * len(r)
        pos = 0
        for x in r:
            _url = reg_url.findall(x)[0]
            _name = reg_name.findall(x)[0]
            ret[pos] = dict(url=_url, name=_name)
            pos += 1
        return ret

    def get_pages(self, chapter_url):
        html = self.get_html(chapter_url)
        regex = "id=\"page_select\".*?>(.*?)<\/select"
        reg = re.compile(regex, re.DOTALL)
        r = reg.findall(html)[0].split("</option>")
        r.pop()
        regex_url = "\"(http:.*?)\""
        reg_url = re.compile(regex_url)
        ret = [None] * len(r)
        pos = 0
        for x in r:
            _url = reg_url.findall(x)[0]
            _name = _url.split("/")[-1]
            ret[pos] = dict(url=_url, name=_name)
            pos += 1
        return ret

