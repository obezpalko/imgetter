#!/usr/bin/env python3
"""
get images from the fetlife
"""
import random
import sys
import time
from urllib.parse import urlparse, unquote, parse_qs
from pyquery import PyQuery as pq
from imgetter.tools import get_page, get_file_name, save_file, printProgressBar, HEADERS, COOKIES, http3
from imgetter.imagesite import ImageSite
import logging
import urllib3


class FetLifeSite(ImageSite):
    def __init__(self, album_page):
        ImageSite.__init__(self, album_page)
        self.title = ''
        self.image = None
        _headers = HEADERS
        _headers['Cookie'] = ';'.join([ f'{x.name}={x.value}' for x in COOKIES ])
        _page = http3.request('GET', album_page, headers=_headers)
        # print(_page.data)
        self.album_q = pq(_page.data)
        self.title = unquote(self.album_q('title')[0].text_content().replace("'s Pics | FetLife", ''))
        (_, _, self.user_id, _, self.picture_id) = urlparse(album_page).path.split('/')
        try:
            img_src = self.album_q('img.object-contain').attr('srcset').split(', ')[-1].split(' ')[0]
        except AttributeError:
            img_src = self.album_q('img.object-contain').attr('src')
        _headers['Referer'] = album_page
        save_file(
            img_src,
            f'albums/fetlife.com/{self.user_id}-{self.title}',
            file_name=f'{self.picture_id}.jpg',
            headers=_headers, cookies={}
        )
        print(f'albums/fetlife.com/{self.user_id}-{self.title}/{self.picture_id}.jpg')

    def __repr__(self):
        return f'albums/fetlife.com/{self.user_id}-{self.title}/{self.picture_id}.jpg'


if __name__ == '__main__':
    # print(f'name: {__name__}')
    # print(f'argv: {sys.argv}')
    try:
        pages = sys.argv[1:]
    except IndexError:
        pages = ['https://fetlife.com/users/11791649/pictures/107444433?sp=46']
    for page in pages:
        page = FetLifeSite(page)
        #  album.reload_album()
        #  album.download()
        #
