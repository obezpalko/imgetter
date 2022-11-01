import requests
import requests.utils
import http.cookiejar
from pyquery import PyQuery as pq
from .tools import HEADERS, COOKIES


class ImageSite:
    def __init__(self, start_page, **kwargs):
        self.start_page = start_page

    def get_page(self):
        r = pq(self.start_page, cookies=COOKIES, headers=HEADERS)
        print(r('title')[0].text_content())

    def __repr__(self):
        return f'{self.start_page}'


if __name__ == '__main__':
    import sys
    print('dispatch sites')
    for img in sys.argv[1:]:
        if img.find('fetlife.com') > 0:
            site = ImageSite('https://fetlife.com/users/12902255/pictures/108137987?sp=57')
        print(site)

