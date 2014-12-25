import os
import urllib.request


class Crawler:
    site = ""
    url = ""
    search = ""

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

    def save_image(self, image_url, file, extension="jpg", path=""):
        # Save a file from image_url to path/file.extension
        if not os.path.exists(path):
            os.makedirs(path)
        urllib.request.urlretrieve(image_url, path + file + "." + extension)