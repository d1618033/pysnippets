import bs4
from urllib.request import urlopen
from functools import partial
import os

def get_html(url):
    return urlopen(url).read().decode()


def get_links(html):
    return map(lambda x: x['href'], bs4.BeautifulSoup(html).find_all('a'))


def correct_links(links, url):
    return map(partial(correct_link, url=url), links)


def correct_link(link, url):
    if link.startswith('/'):
        if url.endswith('/'):
            url = url[:-1]
        return url[:-1] + link
    else:
        return url


def filter_by_extension(links, ext):
    return filter(lambda link: link.split('.')[-1] == ext, links)


def main(url, ext):
    html = get_html(url)
    links = get_links(html)
    corrected_links = correct_links(links, url)
    filtered_links = filter_by_extension(corrected_links, ext)
    for link in filtered_links:
        print(link)


if __name__ == "__main__":
    import sys
    main(*sys.argv[1:])
        
