#!/usr/bin/env python
"""
tools and basic classes
"""
import os
# import random
# from abc import ABC
from html.parser import HTMLParser
from urllib.parse import urlparse, parse_qs

# from html.entities import name2codepoint

import requests
# import time
import sys

USER_AGENT = (
                'Mozilla/5.0 (Linux; Android 4.4.2; Nexus 4 Build/KOT49H) '
                'AppleWebKit/537.36 (KHTML, like Gecko) '
                'Chrome/34.0.1847.114 Mobile Safari/537.36'
             )

def get_attr(attrs: list, attr: str):
    for attr_name, attr_value in attrs:
        if attr_name == attr:
            return attr_value
    return None

def get_page(page, headers=False, cookies=False):
    """ get page """

    if cookies:
        _cookies = cookies
    else:
        _cookies = dict()
    if headers:
        _headers = headers
    else:
        _headers = {
                'user-agent': USER_AGENT,
                'referer': page,
                }
    request = requests.get(
            page,
            headers=_headers,
            cookies=_cookies,
            )
    return request.text

def save_file(file_url:str, dst_dir:str):
    if not os.path.isdir(dst_dir):
        os.mkdir(dst_dir)
    dst_file_name = os.path.join(
        dst_dir,
        os.path.basename(urlparse(file_url).path))
    if os.path.exists(dst_file_name):
        return dst_file_name, 0, 'already downloaded'
    try:
        request_image = requests.get(file_url, stream=True, headers={'user-agent': USER_AGENT,})
    except requests.exceptions.ConnectionError:
        return dst_file_name, -1, 'connection error'
    if request_image.status_code == 200:
        with open(dst_file_name, 'wb') as f:
            for chunk in request_image:
                f.write(chunk)
    return dst_file_name, request_image.status_code, request_image.reason

def get_file_name(file_path):
    (head, tail) = os.path.split(file_path)
    (file_name, ext) = os.path.splitext(tail)
    return file_name

class ImageSite:
    def __init__(self, start_page, parser):
        self.start_page = start_page
        self.parser = parser

# Print iterations progress
def printProgressBar (iteration, total, prefix = '', suffix = '', decimals = 1, length = 100, fill = '█', printEnd = "\r"):
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
        printEnd    - Optional  : end character (e.g. "\r", "\r\n") (Str)
    """
    percent = ("{0:." + str(decimals) + "f}").format(100 * (iteration / float(total)))
    filledLength = int(length * iteration // total)
    bar = fill * filledLength + '-' * (length - filledLength)
    print(f'\r{prefix} |{bar}| {percent}% {suffix}', end = printEnd)
    # Print New Line on Complete
    if iteration == total: 
        print()

if __name__ == '__main__':
    print('imggetter classes and tools')
    try:
        print(save_file(sys.argv[1], 'tmp'))
    except IndexError:
        print(save_file('https://cdn.imagefap.com/images/full/63/710/710717099.jpg?end=1614172686&secure=0715f1e51a9ff08dc66bf', 'tmp'))