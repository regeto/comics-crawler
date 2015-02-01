import glob
import gzip
import io
import os
import urllib.request


class Crawler:
    site = ""
    url = ""
    search = ""
    illegal_characters = ['<', '>', ':', '"', '/', '\\', '|', '?', '*']
    verbose = False

    def search_series(self, title):
        # Search for comic by its name, then return a list of matches
        return list()

    def get_chapters(self, series_url):
        # Parse series for chapters, then return a list of dicts consisting of the chapter url and other relevant info
        # Implemented in subclass
        return list()

    def get_pages(self, chapter_url):
        # Parse chapter for pages, then return a list of page urls
        # Implemented in subclass
        return list()

    def get_html(self, url):
        # Get html from url and return it as a string
        response = urllib.request.urlopen(url)
        return response.read().decode("utf-8", 'ignore')

    def get_html_gzip(self, url):
        # Get html from url when the server sends you gzip data and return it as a string
        headers = {"User-Agent": "Mozilla/5.0 (X11; U; Linux i686) Gecko/20071127 Firefox/2.0.0.11",
                   "Accept-Encoding": "gzip"}
        response = urllib.request.urlopen(urllib.request.Request(url, headers=headers))
        read = response.read()
        bi = io.BytesIO(read)
        gf = gzip.GzipFile(fileobj=bi, mode="rb")
        return gf.read().decode("utf-8", 'ignore')

    def get_name_for_file_system(self, name):
        return (''.join([char for char in name if char not in self.illegal_characters])).strip()

    def get_file_extension(self, file_url):
        return self.get_complete_file_name(file_url).split(".")[-1]

    def get_file_name(self, file_url):
        return '.'.join(self.get_complete_file_name(file_url).split(".")[:-1])

    def get_complete_file_name(self, file_url):
        return file_url.split("/")[-1].split("?")[0]

    def do_download_file(self, url, path):
        urllib.request.urlretrieve(url, path)

    def download_updates(self, original_updates):
        updates = original_updates[:]  # creates a copy of that list
        chapters = len(updates)
        if chapters < 1:
            return
        length_c = len(str(chapters))
        total = 0
        pages = 0
        for update in updates:
            total += len(update['pages'])
        for i in range(chapters):
            length = len(str(i+1))
            istr = '0' * (length_c - length) + str(i+1)
            print("Loading: " + " [", end="")
            arrow = int((pages / total) * 19)
            print(('=' * arrow) + '>' + (' ' * (18-arrow)), end="")
            print("] (" + istr + "/" + str(chapters) + ")", end="\r")
            self.download_update(updates[i])
            pages += len((original_updates.pop(0))['pages'])
        print("Finished  [" + ('=' * 19) + "] (" + str(chapters) + "/" + str(chapters) + ")")
        print("Downloaded " + str(chapters) + " updates for a total of " + str(pages) + " images.")

    def download_update(self, update):
        if not update['path'] == "" and not update['path'][-1] == "/":
            update['path'] += "/"
        if not os.path.exists(update['path']):
            os.makedirs(update['path'])
        for url, file in update['pages']:
            self.do_download_file(url, file)

    def get_updates(self, series_url, path):
        if not path == "" and not path[-1] == "/":
            path += "/"
        chapters = self.get_chapters(series_url)
        count_chapters = len(chapters)
        if count_chapters < 1:
            return
        length_count = len(str(count_chapters))
        updates = []
        pages_count = 0
        for i in range(count_chapters):
            length = len(str(i+1))
            istr = '0' * (length_count - length) + str(i+1)
            print("Checking " + series_url + " for updates (" + istr + "/" + str(count_chapters) + ")", end="\r")
            chapter = chapters[i]
            name = self.get_name_for_file_system(chapter['name'])
            cpath = path + name
            if glob.glob(cpath):
                continue
            pages = self.get_pages(chapter['url'])
            update = dict(
                path=cpath,
                pages=[]
            )
            for page in pages:
                update['pages'].append((page['url'], cpath + "/" + page['name']))
            updates.append(update)
            pages_count += len(update['pages'])
        print()
        if updates:
            print("Found " + str(len(updates)) + " updates, " + str(pages_count) + " images in total.")
        else:
            print("Found no updates.")
        return updates


    def download_chapter(self, chapter_url, path="", force=False):
        """Download a single chapter of a series

        :param chapter_url: URL linking to the chapter overview
        :param path: path to save the chapter to
        :param force: download regardless of chapter's existence
        :return: False if chapter will not be downloaded, True after completion
        """
        if not path == "" and not path[-1] == "/":
            path += "/"
        if os.path.exists(path) and not force:
            if self.verbose:
                print("The folder at \"" + path + "\" already exists. This chapter has been skipped.")
            return False
        pages = self.get_pages(chapter_url)
        if not os.path.exists(path):
            if self.verbose:
                print("Creating folder at \"" + path + "\".")
            os.makedirs(path)
        print("Downloading chapter from " + chapter_url + ".")
        for page in pages:
            page_name = self.get_name_for_file_system(page['name'])
            if self.verbose:
                print("Downloading file \"" + page_name + "\".")
            self.do_download_file(page['url'], path + page_name)
        if self.verbose:
            print("Chapter completed.")
        return True

    def download_chapter_webcomic(self, chapter_url, path="", chapter_name="", force=False):
        """Download the images of a single chapter of a series

        :param chapter_url: URL linking to the chapter overview
        :param path: path to save the images to
        :param chapter_name: the chapter's name
        :param force: download regardless of chapter's existence
        :return: False if no image will be downloaded, True after completion
        """
        # can be tricked by folders named 'path + chapter_name + "." + something' but that's hardly important
        files = glob.glob(path + chapter_name + ".*")
        if files and not force:
            return False
        page = self.get_pages(chapter_url)[0]
        page_url = page['url']
        page_name = chapter_name + "." + self.get_file_extension(page_url)
        if self.verbose:
            print("Downloading file \"" + page_name + "\".")
        self.do_download_file(page_url, path + page_name)
        return True

    def download_series(self, series_url, path="", limit=0, force=False, webcomic=False, oneshot=False):
        """Download chapters of a series

        :param series_url: URL linking to the series overview page
        :param path: path to save the series to
        :param limit: maximum amount of chapters to download. Leave at 0 for no limit.
        :param force: download regardless of chapter's existence.
        :param webcomic: download all images from all chapters into a single directory.
        :param oneshot: download all images from the single chapter into a single directory
        :return: None
        """
        if not path == "" and not path[-1] == "/":
            path += "/"
        if oneshot and os.path.exists(path):
            return
        chapters = self.get_chapters(series_url)
        print("Checking " + series_url + " for updates.")

        if not os.path.exists(path) and not oneshot:
            if self.verbose:
                print("Creating folder at \"" + path + "\".")
            os.makedirs(path)
        count = 0
        for chapter in chapters:
            if limit != 0:
                count += 1
            if count > limit:
                break
            chapter_url = chapter['url']
            chapter_path = path
            if not oneshot:
                chapter_name = self.get_name_for_file_system(chapter['name'])
                chapter_path += chapter_name
            if webcomic:
                success = self.download_chapter_webcomic(chapter_url, path, chapter_name, force)
            else:
                success = self.download_chapter(chapter_url, chapter_path, force)
            if (limit != 0) and not success:
                count -= 1
        if self.verbose:
            print("Series completed.")


