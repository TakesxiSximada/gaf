#! /usr/bin/env python
# -*- coding: utf-8 -*-
import os
import sys
import datetime
import argparse
import requests
import bs4


class PackageTable(object):
    def __init__(self,
                 github_url,
                 pypi_url,
                 watch_count,
                 star_count,
                 fork_count,
                 py_target,
                 download_last_month,
                 ):
        self.github_url = github_url
        self.pypi_url = pypi_url
        self.watch_count = watch_count
        self.star_count = star_count
        self.fork_count = fork_count
        self.py_target = py_target
        self.download_last_month = download_last_month

    def show(self):
        table_data = (
            ('Github URL', self.github_url),
            ('PyPI URL', self.pypi_url),
            ('watch数', self.watch_count),
            ('star数', self.star_count),
            ('fork数', self.fork_count),
            ('対象version', self.py_target),
            ('download last month', self.download_last_month),
        )

        header_max = max(len(header) for header, data in table_data)
        data_max = max(len(data) for header, data in table_data)
        header_pad_len = header_max + 10
        data_pad_len = data_max + 10

        header_pad_len = header_pad_len + 1 if header_pad_len % 2 else header_pad_len
        data_pad_len = data_pad_len + 1 if data_pad_len % 2 else data_pad_len

        fmt = '|{{:<{}}}|{{:<{}}}|'.format(header_pad_len, data_pad_len)
        print(fmt.format('  項目', datetime.datetime.now().strftime('  詳細(%Y/%m/%dの情報)')))
        print(fmt.format('-'*header_pad_len, '-'*data_pad_len))
        for header, data in table_data:
            print(fmt.format(header, data))


def main(argv=sys.argv[1:]):
    parser = argparse.ArgumentParser()
    parser.add_argument('url')
    args = parser.parse_args(argv)

    github_url = args.url
    package_name = os.path.basename(github_url)
    pypi_url = 'https://pypi.python.org/pypi/{}'.format(package_name)
    res = requests.get(pypi_url)
    py_target = '-'
    download_last_month = '-'
    if res.status_code == 200:
        soup = bs4.BeautifulSoup(res.text)
        download_last_month = soup.select('.nodot li span')[2].text.strip()
        versions = [t.text.strip().strip('Programming Language :: Python ::')
                    for t in soup.select('ul.nodot li a')
                    if t.text.strip().startswith('Programming Language :: Python ::')]
        py_target = ', '.join(versions) if versions else '???'
    else:
        pypi_url = '-'

    res = requests.get(github_url)
    soup = bs4.BeautifulSoup(res.text)
    tags = soup.find_all('a', class_='social-count')
    watch_count = tags[0].text.strip()
    star_count = tags[1].text.strip()
    fork_count = tags[2].text.strip()

    table = PackageTable(
        github_url=github_url,
        pypi_url=pypi_url,
        watch_count=watch_count,
        star_count=star_count,
        fork_count=fork_count,
        py_target=py_target,
        download_last_month=download_last_month,
        )
    table.show()

if __name__ == '__main__':
    sys.exit(main())
