#!/usr/bin/env python
"""
get images from the site
"""
import os
import random
from abc import ABC
from html.parser import HTMLParser
from html.entities import name2codepoint

import requests
import time
import sys


def get_attr(attrs: list, attr: str):
    for attr_name, attr_value in attrs:
        if attr_name == attr:
            return attr_value
    return None


class EHentaiHTMLParser(HTMLParser, ABC):
    """parse html to get album title, image url and next page"""
    def __init__(self):
        HTMLParser.__init__(self)
        self.album_title = ''
        self.reading_title = False
        self.next_page = None
        self.image_url = None

    def handle_starttag(self, tag, attrs):
        self.reading_title = tag == 'h1'
        if self.next_page is None and tag == 'a' and get_attr(attrs, 'id') == 'next':
            self.next_page = get_attr(attrs, 'href')
        if self.image_url is None and tag == 'img' and get_attr(attrs, 'id') == 'img':
            self.image_url = get_attr(attrs, 'src')

    def handle_data(self, data):
        if self.reading_title:
            self.album_title = data

    def reset_page(self):
        self.album_title = ''
        self.reading_title = False
        self.next_page = None
        self.image_url = None


parser = EHentaiHTMLParser()


def get_page(start_page):
    """ main func """

    cookies = dict(
            nw='1',
            #  __cfduid='da4cdfffbef05b1c718a41617175d898e1609305536'
            __cfduid='db5a6b573b1dee15a28a40164542f9aba1609311463'
            )
    headers = {
            'user-agent': (
                'Mozilla/5.0 (Linux; Android 4.4.2; Nexus 4 Build/KOT49H) '
                'AppleWebKit/537.36 (KHTML, like Gecko) '
                'Chrome/34.0.1847.114 Mobile Safari/537.36'
                ),
            'referer': start_page,
            }
    request = requests.get(
            start_page,
            headers=headers,
            cookies=cookies,
            )
    parser.reset_page()
    parser.feed(request.text)
    return start_page, parser.next_page, parser.image_url, parser.album_title


if __name__ == '__main__':

    start_page = ''
    next_page = 'https://e-hentai.org/s/90eb55bee8/1544524-38'
    try:
        next_page = sys.argv[1]
    except IndexError:
        print("Please specify start page")
        sys.exit(1)
    while start_page != next_page:
        start_page, next_page, image_url, album_title = get_page(next_page)
        print(start_page)
        headers = {
            'user-agent': (
                'Mozilla/5.0 (Linux; Android 4.4.2; Nexus 4 Build/KOT49H) '
                'AppleWebKit/537.36 (KHTML, like Gecko) '
                'Chrome/34.0.1847.114 Mobile Safari/537.36'
            ),
            'referer': start_page,
        }
        if not os.path.isdir(album_title):
            os.mkdir(album_title)
        dst_file_name = os.path.join(album_title, os.path.basename(image_url))
        if os.path.exists(dst_file_name):
            print('already exists')
            continue

        request_image = requests.get(image_url, stream=True, headers=headers)

        if request_image.status_code == 200:

            with open(dst_file_name, 'wb') as f:
                for chunk in request_image:
                    f.write(chunk)

        time.sleep(random.random()*20)

