
from fetlife import FetLifeSite


def dispatcher(url:str):
    if url.find('fetlife.com') > 0:
        return FetLifeSite(url)


if __name__ == '__main__':
    import sys

    if len(sys.argv) == 1 or sys.argv[1] == '-':
        # read from stdin
        try:
            while True:
                img = sys.stdin.readline()
                if img == '':
                    break
                print(dispatcher(img.rstrip()))

        except EOFError:
            pass
    else:
        for img in sys.argv[1:]:
            print(dispatcher(img.rstrip()))
