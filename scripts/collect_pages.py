#!/usr/bin/env python3
from mylog import mylog

from pathlib import Path
import requests
from lxml.html import fromstring as lxsoup
from urllib.parse import parse_qs, urljoin, urlparse

HOMEPAGE_URL = 'https://www.osha.gov/laws-regs/regulations/standardnumber'
TARGET_DIR = Path('data', 'collected', 'standards')


def page_path(url:str) -> Path:
    """
    when url is HOMEPAGE_URL, returns: collected/standards/index.html

    when url is a PART url, e.g.
        'https://www.osha.gov/laws-regs/regulations/standardnumber/1910'
         returns: 'collected/standards/1910/index.html'

    when url is a NUMBER page, e.g.
        'https://www.osha.gov/laws-regs/regulations/standardnumber/1910/1910.215'
         returns: 'collected/standards/1910/1910.215.html'
    """
    if url == HOMEPAGE_URL:
        return TARGET_DIR.joinpath('index.html')
    else:
        u = Path(url)
        if u.parent.name == 'standardnumber':
            return TARGET_DIR.joinpath(u.name, 'index.html')
        if u.parent.parent.name == 'standardnumber':
            return TARGET_DIR.joinpath(u.parent, f'{u.name}.html')
        else:
            raise ValueError(f"Unexpected url: {url}")





def fetch_and_save(url, target_path=None):
    """
    returns target_path when file has been freshly fetched or has otherwise been found
    """

    if target_path is None:
        target_path = page_path(url)

    def _existed_size(path):
        e = Path(path)
        if e.is_file():
            return e.stat().st_size
        else:
            return False

    def _save_file(content, target_path):
        target_path.parent.mkdir(exist_ok=True, parents=True)
        target_path.write_bytes(content)
        return target_path

    xb = _existed_size(target_path)

    if xb:
        mylog(f"{xb} bytes in {target_path}", label="Exists")
    else:
        mylog(url, label="Downloading")
        resp = requests.get(url)
        if resp.status_code == 200:
            _save_file(resp.content, target_path)
            mylog(target_path, f"{_existed_size(target_path)} bytes", label="Saved")

        else:
            print(resp.text)
            raise ValueError(f"Unexpected status code: `{resp.status_code}`")

    return target_path


def fetch_part_pages():
    def _read_homepage():
        _srcpath = fetch_and_save(HOMEPAGE_URL)
        txt = _srcpath.read_bytes()
        return lxsoup(txt)

    def _get_part_urls():
        paths = _read_homepage().xpath('//a[contains(@href, "laws-regs/regulations/standardnumber/")]/@href')
        urls = [urljoin(HOMEPAGE_URL, p) for p in paths]
        return urls

    _urls = _get_part_urls()

    mylog(f"Found {len(_urls)} part urls")
    for i, url in enumerate(_urls):
        mylog(f"({i+1}/{len(_urls)}) {url}", label="Fetching")
        fetch_and_save(url)




def main():
    fetch_part_pages()


if __name__ == '__main__':
    main()
