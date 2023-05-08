#!/usr/bin/env python
"""
tools and basic classes
"""
import os
import http.cookiejar
from typing import Dict
import requests.utils
import urllib3

# from html.parser import HTMLParser
from urllib.parse import urlparse
import logging

# from html.entities import name2codepoint

import requests
# import time
import sys

logging.basicConfig(filename='imgetter.log', encoding='utf-8', level=logging.DEBUG)

USER_AGENT = (
                'Mozilla/5.0 (X11; Linux x86_64) '
                'AppleWebKit/537.36 (KHTML, like Gecko) '
                'Chrome/102.0.0.0 Safari/537.36'
             )

COOKIES = http.cookiejar.LWPCookieJar()
COOKIES.load('.cookies')
HEADERS = requests.utils.default_headers()
HEADERS.update({'User-Agent': USER_AGENT})
http3 = urllib3.PoolManager()


def get_attr(attrs: list, attr: str):
    for attr_name, attr_value in attrs:
        if attr_name == attr:
            return attr_value
    return None


def get_page(url: str, headers: Dict = False, cookies: Dict = False):
    """ get page """

    if cookies:
        _cookies = cookies
    else:
        _cookies = COOKIES
    if headers:
        _headers = headers
    else:
        _headers = {
                'user-agent': USER_AGENT,
                'referer': url,
                }
    request = requests.get(
            url,
            headers=_headers,
            cookies=_cookies,
            )
    return request.text


def save_file(file_url: str, dst_dir: str, file_name: str = None, headers: dict = None, cookies: dict = None):
    if not os.path.isdir(dst_dir):
        os.mkdir(dst_dir)
    dst_file_name = os.path.join(
        dst_dir,
        os.path.basename(urlparse(file_url).path) if file_name is None else file_name)

    _cookies = COOKIES if cookies is None else cookies
    _headers = HEADERS if headers is None else headers
    _headers['Cookie'] = ';'.join([ f'{x.name}={x.value}' for x in _cookies ])
    if os.path.exists(dst_file_name):
        logging.debug(f'url: {file_url} status: 0, reason: already downloaded dst: {dst_file_name}')

        return dst_file_name, 0, 'already downloaded'
    request_image = http3.request('GET', file_url, headers=_headers)
    # try:
    #     request_image = requests.get(file_url, stream=True, headers=_headers, cookies=_cookies)
    # except requests.exceptions.ConnectionError:
    #     return dst_file_name, -1, 'connection error'
    # #  except requests.exceptions.MissingSchema:
    # #      return dst_file_name, -1, 'missing schema'

    if request_image.status == 200:
        with open(dst_file_name, 'wb') as f:
            # for chunk in request_image.da:
            f.write(request_image.data)
    logging.debug(f'url: {file_url} status: {request_image.status}, reason: {request_image.reason} dst: {dst_file_name}')
    return dst_file_name, request_image.status, request_image.reason


def get_file_name(file_path):
    (head, tail) = os.path.split(file_path)
    (file_name, ext) = os.path.splitext(tail)
    return file_name


# Print iterations progress
def printProgressBar(iteration, total, prefix='', suffix='', decimals=1, length=100, fill='█', print_end="\r"):
    """
    Call in a loop to create terminal progress bar
    @params:
        iteration   - Required  : current iteration (Int)
        total       - Required  : total iterations (Int)
        prefix      - Optional  : prefix string (Str)
        suffix      - Optional  : suffix string (Str)
        decimals    - Optional  : positive number of decimals in percent complete (Int)
        length      - Optional  : character length of bar (Int)
        fill        - Optional  : bar fill character (Str)
        print_end    - Optional  : end character (e.g. "\r", "\r\n") (Str)
    """
    percent = ("{0:." + str(decimals) + "f}").format(100 * (iteration / float(total)))
    filled_length = int(length * iteration // total)
    bar = fill * filled_length + '-' * (length - filled_length)
    print(f'\r{prefix} |{bar}| {percent}% {suffix}', end=print_end)
    # Print New Line on Complete
    if iteration == total:
        print()


if __name__ == '__main__':
    print('imgetter classes and tools')
    try:
        print(save_file(sys.argv[1], 'tmp'))
    except IndexError:
        print(save_file('https://cdn.imagefap.com/images/full/63/710/710717099.jpg?end=1614172686&secure=0715f1e51a9ff08dc66bf', 'tmp'))
