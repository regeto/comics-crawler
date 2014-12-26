import re

from crawlers.crawler import Crawler


class EdenCrawler(Crawler):
    site = "MangaEden"
    url = "http://mangaeden.com"
    search = "http://www.mangaeden.com/en-directory/?title=%s"

    def get_chapters(self, series_url):
        html = self.get_html(series_url)
        regex = "<a href=\"(\/en-manga\/.*?)\" class=\"chapterLink\">.*?<b>(.*?)</b>\\n</a>"
        reg = re.compile(regex, re.DOTALL)
        r = reg.findall(html)
        r.reverse()
        ret = [None] * len(r)
        pos = 0
        for x in r:
            url = self.url + r[pos][0]
            name = r[pos][1]
            ret[pos] = dict(url=url, name=name)
            pos += 1
        return ret

    def get_pages(self, chapter_url):
        html = self.get_html(chapter_url)
        regex_pagenum = "pageInfo\" class=\"ui-state-default\">1 of (.*?)<\/div>"
        reg = re.compile(regex_pagenum)
        r = reg.findall(html, re.DOTALL)
        regex_image = "id=\"mainImg\" src=\"(.*?)\""
        reg_image = re.compile(regex_image)
        pagemax = int(r[0])
        chapter_url_base = '/'.join(chapter_url.split("/")[:-2]) + '/'
        ret = [None] * pagemax
        for x in range(1, pagemax+1):
            page_url = chapter_url_base + str(x)
            page_html = self.get_html(page_url)
            image = "http:" + reg_image.findall(page_html)[0]
            ret[x-1] = dict(url=image, name=str(x) + "." + self.get_file_extension(image))
        return ret
