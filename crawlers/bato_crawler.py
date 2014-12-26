import re
from crawlers import Crawler


class BatoCrawler(Crawler):
    site = "Batoto"
    url = "http://bato.to"
    search = "http://bato.to/search?name=%s"

    def get_chapters(self, series_url):
        html = self.get_html_gzip(series_url)
        regex = "<tr class=\"row lang_English chapter_row\".*?>(.*?)<\/tr>"
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
            url = reg_url.findall(x)[0]
            name = reg_name.findall(x)[0]
            ret[pos] = dict(url=url, name=name)
            pos += 1
        return ret

    def get_pages(self, chapter_url):
        html = self.get_html_gzip(chapter_url)
        regex = "id=\"page_select\".*?>(.*?)<\/select"
        reg = re.compile(regex, re.DOTALL)
        r = reg.findall(html)[0].split("</option>")
        r.pop()
        regex_url = "\"(http:.*?)\""
        reg_url = re.compile(regex_url)
        regex_image = "<img id=\"comic_page\".*?src=\"(.*?)\""
        reg_image = re.compile(regex_image)
        ret = [None] * len(r)
        pos = 0
        for x in r:
            url = reg_url.findall(x)[0]
            html_image = self.get_html(url)
            actual_url = reg_image.findall(html_image)[0]
            name = url.split("/")[-1] + "." + self.get_file_extension(actual_url)
            ret[pos] = dict(url=actual_url, name=name)
            pos += 1
        return ret

