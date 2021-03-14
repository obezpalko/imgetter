#!/usr/bin/env python
"""
tools and basic classes
"""
# import os
# import random
# from abc import ABC
from html.parser import HTMLParser
# from html.entities import name2codepoint

# import requests
# import time
# import sys

USER_AGENT = ("Mozilla/5.0 (Linux; Android 4.4.2; Nexus 4 Build/KOT49H) "
              "AppleWebKit/537.36 (KHTML, like Gecko) "
              "Chrome/34.0.1847.114 Mobile Safari/537.36")


def get_attr(attrs: list, attr: str):
    for attr_name, attr_value in attrs:
        if attr_name == attr:
            return attr_value
    return None

def get_page(page, headers=None):
    """ main func """

    if headers is None:
        _headers = {
                'user-agent': USER_AGENT,
                'referer': page,
                }
    else:
        _headers = headers
    request = requests.get(
            page,
            headers=_headers,
            )
    return request.text


class ImageSite:
    def __init__(self, album_page, parser):
        self.album_page = album_page
        self.parser = parser


if __name__ == '__main__':
    print('imggetter classes and tools')