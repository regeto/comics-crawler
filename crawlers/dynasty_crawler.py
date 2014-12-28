import re
from crawlers import Crawler


class DynastyCrawler(Crawler):
    site = "Dynasty Scans"
    url = "http://dynasty-scans.com"
    search = "http://dynasty-scans.com/search?q=%s"

    def get_chapters(self, series_url):
        html = self.get_html(series_url)
        regex = re.compile("<dd>(.*?)</dd>", re.DOTALL)
        r = regex.findall(html)
        reg_url = re.compile("href=\"(/chapters/.*?)\" class")
        reg_name = re.compile("class=\"name\">(.*?)</a>")
        reg_date = re.compile("<small>released (.*?)</small>")
        ret = [None] * len(r)
        pos = 0
        for x in r:
            url = self.url + reg_url.findall(x)[0]
            name = reg_name.findall(x)[0]
            # TODO: date formatting
            # DynastyReader already lists these sorted so that's awesome
            date = reg_date.findall(x)[0]
            ret[pos] = dict(url=url, name=name, date=date)
            pos += 1
        return ret

    def get_pages(self, chapter_url):
        html = self.get_html(chapter_url)
        regex = "var pages = \[\{(.*?\")\}\];"
        reg = re.compile(regex)
        r = reg.findall(html)[0].split("},")
        regex_url = "\"image\":\"(.*?)\""
        reg_url = re.compile(regex_url)
        regex_name = "\"name\":\"(.*?)\""
        reg_name = re.compile(regex_name)
        ret = [None] * len(r)
        pos = 0
        for x in r:
            url = self.url + reg_url.findall(x)[0]
            name = reg_name.findall(x)[0] + "." + self.get_file_extension(url)
            ret[pos] = dict(url=url, name=name)
            pos += 1
        return ret
