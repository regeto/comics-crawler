import os
import urllib.request


class Crawler:
    site = ""
    url = ""
    search = ""
    illegal_characters = ['<', '>', ':', '"', '/', '\\', '|', '?', '*']

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

    def get_chapter_name(self, name):
        return ''.join([char for char in name if char not in self.illegal_characters])

    def save_chapter(self, chapter_name, image_urls, file_names, path=""):
        # Save all images in a list to the given path
        chapter = self.get_chapter_name(chapter_name)
        file_path = path + chapter + "/"
        if os.path.exists(file_path):
            print("The folder at \"" + file_path + "\" already exists. This chapter has been skipped.")
            return False
        if len(image_urls) != len(file_names):
            print("The url and name lists don't seem to fit together! This chapter has been skipped.")
            return False
        os.makedirs(file_path)
        for i in range(len(image_urls)):
            print("Retrieving image " + file_names[i] + "...")
            urllib.request.urlretrieve(image_urls[i], file_path + file_names[i])
        return True
