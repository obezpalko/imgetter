#!/usr/bin/env python
"""
get images from the site
"""
import random
import sys
import time
from urllib.parse import urlparse, unquote
from pyquery import PyQuery as pq
from .tools import get_file_name, save_file, printProgressBar
from .imagesite import ImageSite
import logging
import urllib3
import glob

http = urllib3.PoolManager()


class ImageFapSite(ImageSite):
    def __init__(self, album_page):
        ImageSite.__init__(self, album_page)
        self.title = ''
        self.image_list = []
        # try to parse url
        # 2 variants are possible
        # https://www.imagefap.com/pictures/7342272/Bdsm-art-by-Pichard?gid=7342272&view=0
        # https://www.imagefap.com/pictures/8758244/Saud?gen=
        # https://www.imagefap.com/gallery.php?gid=8341668&gen=
        # https://www.imagefap.com/gallery/4080098
        self.gid, self.title = urlparse(album_page).path.split('/')[-2:]
        self.album_q = pq(url=album_page, opener=lambda url, **kw: http.urlopen('GET', url).data)
        self.title = unquote(self.album_q('title')[0].text_content().split(' Porn Pics & Porn GIFs')[0])
        self.image_pages = []
        for t in self.album_q('a').parents('table').items():
            image_link = t('a').attr('href')
            if image_link.startswith('/photo/'):
                self.image_pages.append(f"https://www.imagefap.com{t('tr a').attr('href')}")
        first_thumb = self.album_q("img[alt*='{}']".format(self.title.replace("'", "\\'")))[0].get('src')
        self.first_file_id = get_file_name(urlparse(first_thumb).path)
        self.images = list()
        self.total_images = -1
        self.data_loaded = False


    def download(self):
        i = 0
        album_path = f"albums/imagefap.com/{self.gid}-{self.title}"
        for i, p in enumerate(self.image_pages):
            image_id = p.split('/')[4]
            glob_match = glob.glob(f"{album_path}/{image_id}.*")
            if len(glob_match) > 0:
                logging.debug(f'file already exists {glob_match}')
                continue
            time.sleep(random.random()*3)
            page_q = pq(url=p, opener=lambda url, **kw: http.urlopen('GET', url).data)
            img_file_name = page_q('img#mainPhoto').attr('alt')[len(self.title)+3:]
            img_src = page_q('img#mainPhoto').attr('src')
            logging.debug(f"{img_src} {img_file_name}")

            file_name, result_code, reason = save_file(img_src, album_path)
            if result_code > 0:
                time.sleep(random.random()*2)
            printProgressBar(i, len(self.image_pages), prefix='Progress:', suffix='Complete', length=50)

    def __repr__(self):
        return f"{self.title} gid:{self.gid} fid:{self.first_file_id} total:{self.total_images}"  # + "\n" + "\n".join(self.images)


if __name__ == '__main__':

    # album_page = 'https://www.imagefap.com/pictures/7342272/Bdsm-art-by-Pichard'  # ?gid=7342272&view=2'
    try:
        album_pages = sys.argv[1:]
    except IndexError:
        album_pages = ['https://www.imagefap.com/gallery.php?gid=1558558&gen=']
    #     print('Please specify album page')
    #     sys.exit(1)
    for album_page in album_pages:
        album = ImageFapSite(f'{album_page}&view=2')  # view=2 - single page view
        print(album)
        album.download()
