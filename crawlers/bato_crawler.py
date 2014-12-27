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
        r = reg.findall(html)
        if r:
            r = r[0].split("</option>")
            r.pop()
            regex_url = "\"(http:.*?)\""
            reg_url = re.compile(regex_url)
            regex_image = "<img id=\"comic_page\".*?src=\"(.*?)\""
            reg_image = re.compile(regex_image)
            ret = [None] * len(r)
            pos = 0
            for x in r:
                url = reg_url.findall(x)[0]
                html_image = self.get_html_gzip(url)
                actual_url = reg_image.findall(html_image)[0]
                name = url.split("/")[-1] + "." + self.get_file_extension(actual_url)
                ret[pos] = dict(url=actual_url, name=name)
                pos += 1
        else:
            # webtoon with all images on one page
            # we could enable non-webtoon mode but not doing that saves us a bunch of site requests and time
            regex_div = "(<div style=\"width.*?\">(?:<img src=\'.*?\' alt=\'.*?\' \/><br\/>)*?<\/div>)"
            reg_div = re.compile(regex_div)
            r_div = reg_div.findall(html)
            regex_url = "src='(.*?)'"
            reg_url = re.compile(regex_url)
            r_url = reg_url.findall(r_div[0])
            ret = [None] * len(r_url)
            pos = 0
            for x in r_url:
                ret[pos] = dict(url=x, name=self.get_complete_file_name(x))
                pos += 1
        return ret

