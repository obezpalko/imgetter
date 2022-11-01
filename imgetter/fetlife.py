#!/usr/bin/env python3
"""
get images from the fetlife
"""
import random
import sys
import time
from urllib.parse import urlparse, unquote, parse_qs
from pyquery import PyQuery as pq
from imgetter.tools import get_file_name, save_file, printProgressBar, HEADERS, COOKIES
from imgetter.imagesite import ImageSite


class FetLifeSite(ImageSite):
    def __init__(self, album_page):
        ImageSite.__init__(self, album_page)
        self.title = ''
        self.image = None
        self.album_q = pq(url=album_page, cookies=COOKIES, headers=HEADERS)
        self.title = unquote(self.album_q('title')[0].text_content().replace("'s Pics | FetLife", ''))
        (_, _, self.user_id, _, self.picture_id) = urlparse(album_page).path.split('/')
        try:
            img_src = self.album_q('img.object-contain').attr('srcset').split(', ')[-1].split(' ')[0]
        except AttributeError:
            img_src = self.album_q('img.object-contain').attr('src')
        save_file(img_src, f'albums/fetlife.com/{self.user_id}-{self.title}', file_name=f'{self.picture_id}.jpg')

    def __repr__(self):
        return f'albums/fetlife.com/{self.user_id}-{self.title}/{self.picture_id}.jpg'


print(f'name: {__name__}')

if __name__ == '__main__':
    print(f'name: {__name__}')
    try:
        pages = sys.argv[1:]
    except IndexError:
        pages = ['https://fetlife.com/users/11791649/pictures/107444433?sp=46']
    for page in pages:
        page = FetLifeSite(page)
        #  album.reload_album()
        print(page)
        #  album.download()
print(f'name: {__name__}')
