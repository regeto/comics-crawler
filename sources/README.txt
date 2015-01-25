This folder is where you specify what series you want to download and update.

For every crawler, there should be a source file. So for the bato_crawler, there should be bato_sources.py.

Every sources file should only be a single list, names "sources". This list is composed of dicts, one for every series.
Here is how the dicts should look:

Required arguments:
     url -- url to the series. If possible, a series overview page that links to all the chapters.

Optional arguments:
     dir -- (str)  directory to download to.
   force -- (bool) download even if the chapter already exists
 oneshot -- (bool) if this is a oneshot (only has one chapter). Oneshots will be saved directly into the series folder.
webcomic -- (bool) if this is a webcomic (only one page per 'chapter'). Webcomics will not be split into folders per chapter.


If you don't know python, don't worry. Just copy-paste this entry once per series into the respective sources file
and edit the values to suit your needs. You can ignore everything following the # character, it will not be computed.

    dict(
        url="", # url to the series
        dir="", # folder where this series will be downloaded to, optional
        force=False, # true/False, optional
        oneshot=False, # true/False, optional
        webcomic=False, # true/False, optional
    ),

