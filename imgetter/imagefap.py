#!/usr/bin/env python
"""
get images from the site
"""
import random
import sys
import time
from urllib.parse import urlparse, unquote
from pyquery import PyQuery as pq
from .tools import ImageSite, get_file_name, save_file, printProgressBar


class ImageFapSite(ImageSite):
    def __init__(self, album_page):
        ImageSite.__init__(self, album_page, None)
        self.title = ''
        self.image_list = []
        # try to parse url
        # 2 variants are possible
        # https://www.imagefap.com/pictures/7342272/Bdsm-art-by-Pichard?gid=7342272&view=0
        # https://www.imagefap.com/pictures/8758244/Saud?gen=
        # https://www.imagefap.com/gallery.php?gid=8341668&gen=
        # https://www.imagefap.com/gallery/4080098
        self.gid, self.title = urlparse(album_page).path.split('/')[-2:]
        self.album_q = pq(url=album_page)
        self.title = unquote(self.album_q('title')[0].text_content().split(' Porn Pics & Porn GIFs')[0])
        # print(self.title)
        # sys.exit()
        # self.gid = parse_qs(urlparse(album_page).query)['gid'][0]
        # first image thumnail
        first_thumb = self.album_q("img[alt*='{}']".format(self.title.replace("'", "\\'")))[0].get('src')
        # (_head, tail) = os.path.split(urlparse(first_thumb).path)
        # (self.first_file_id, _ext) = os.path.splitext(tail)
        self.first_file_id = get_file_name(urlparse(first_thumb).path)
        self.images = list()
        self.total_images = -1
        self.data_loaded = False

    def download(self):
        # self.load_album_data(self.first_file_id, self.gid)
        self.reload_album()
        for i, img in enumerate(self.images):
            # print(f"Download {img}")
            file_name, result_code, reason = save_file(img, f"albums/{self.gid}-{self.title}")
            if result_code > 0:
                time.sleep(random.random()*2)
            # idx = idx +1
            printProgressBar(i + 1, self.total_images, prefix='Progress:', suffix='Complete', length=50)
            # print("{:>{w}}/{:<{w}} {:3} {}".format(idx, self.total_images, result_code, file_name, w=number_len))

    def __repr__(self):
        return f"{self.title} gid:{self.gid} fid:{self.first_file_id} total:{self.total_images}"  # + "\n" + "\n".join(self.images)

    def reload_album(self):
        self.load_album_data(self.first_file_id, self.gid)

    def load_album_data(self, image_id: str, gid: str):
        if self.data_loaded:
            return
        _img = image_id
        while self.total_images <= 0 or self.total_images > len(self.images):
            page_q = pq(url=f"https://www.imagefap.com/photo/{_img}/?gid={gid}&idx={len(self.images)}&partial")

            if self.total_images <= 0:
                self.total_images = int(page_q('div#navigation')[0].get('data-total'))
            # print(page_q)
            new_images = list(page_q('div#navigation ul li a').map(lambda i, a: a.get('original')))
            if len(new_images) < 1:
                break

            self.images = self.images + new_images
            time.sleep(random.random()*3)
        self.data_loaded = True


if __name__ == '__main__':

    # album_page = 'https://www.imagefap.com/pictures/7342272/Bdsm-art-by-Pichard'  # ?gid=7342272&view=2'
    try:
        album_pages = sys.argv[1:]
    except IndexError:
        album_pages = ['https://www.imagefap.com/gallery.php?gid=1558558&gen=']
    #     print('Please specify album page')
    #     sys.exit(1)
    for album_page in album_pages:
        album = ImageFapSite(album_page)
        album.reload_album()
        print(album)
        album.download()
