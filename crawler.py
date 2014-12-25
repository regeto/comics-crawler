import os
import urllib.request


class Crawler:
    site = ""
    url = ""
    search = ""
    illegal_characters = ['<', '>', ':', '"', '/', '\\', '|', '?', '*']
    verbose = True

    def search_series(self, title):
        # Search for comic by its name, then return a list of matches
        return list()

    def get_chapters(self, series_url):
        # Parse series for chapters, then return a list of dicts consisting of the chapter url and other relevant info
        return list()

    def get_html(self, url):
        # Get html from url and return it as a string
        response = urllib.request.urlopen(url)
        return response.read().decode("utf-8")

    def get_pages(self, chapter_url):
        # Parse chapter for pages, then return a list of page urls
        return list()

    def get_name_for_file_system(self, name):
        return (''.join([char for char in name if char not in self.illegal_characters])).strip()

    def get_file_extension(self, file_url):
        return file_url.split("/")[-1].split(".")[-1]

    def get_file_name(self, file_url):
        return '.'.join(file_url.split("/")[-1].split(".")[:-1])

    def get_complete_file_name(self, file_url):
        return file_url.split("/")[-1]

    def do_download_file(self, url, path):
        urllib.request.urlretrieve(url, path)

    def download_chapter(self, chapter_url, path=""):
        if not path == "" and not path[-1] == "/":
            path += "/"
        if os.path.exists(path):
            if self.verbose:
                print("The folder at \"" + path + "\" already exists. This chapter has been skipped.")
            return False
        pages = self.get_pages(chapter_url)
        if self.verbose:
            print("Creating folder at \"" + path + "\".")
        os.makedirs(path)
        if self.verbose:
            print("Downloading chapter from " + chapter_url + ".")
        for page in pages:
            page_name = self.get_name_for_file_system(page['name'])
            if self.verbose:
                print("Downloading file \"" + page_name + "\".")
            self.do_download_file(page['url'], path + page_name)
        if self.verbose:
            print("Chapter completed.")
        return True

    def download_series(self, series_url, path="", limit = "0"):
        chapters = self.get_chapters(series_url)
        if not path == "" and not path[-1] == "/":
            path += "/"
        if not os.path.exists(path):
            if self.verbose:
                print("Creating folder at \"" + path + "\".")
            os.makedirs(path)
        count = 0
        for chapter in chapters:
            if limit != 0:
                count += 1
            if count > limit:
                break
            success = self.download_chapter(chapter['url'], path + self.get_name_for_file_system(chapter['name']))
            if (limit != 0) and not success:
                count -= 1


