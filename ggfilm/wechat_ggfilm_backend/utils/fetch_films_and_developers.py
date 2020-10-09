# -*- coding: utf-8 -*-
import logging
__Logger = logging.getLogger('films_and_developers_fetcher')
__Logger.setLevel(logging.INFO)
__Formatter = logging.Formatter("[%(asctime)-15s][%(levelname)-5s] %(message)s", datefmt="%Y-%m-%d %H:%M:%S")
__FileHandler = logging.FileHandler('log/films_and_developers_fetcher.log', 'w')
__FileHandler.setFormatter(__Formatter)
__Logger.addHandler(__FileHandler)

import requests
import ujson as json

from bs4 import BeautifulSoup

from common import RequestHeaders


def callback_func(r, *args, **kwargs):
    __Logger.info('fetch films and developers on <{}>'.format(r.url))
    if r.status_code == 200:
        __Logger.info('response status code: {}'.format(r.status_code))
    else:
        __Logger.warning('failed to fetch, response status code: {}'.format(r.status_code))


def main():
    url = 'https://www.digitaltruth.com/chart/print.php'

    r = requests.get(url, headers=RequestHeaders, hooks=dict(response=callback_func))
    if r.status_code == 200:
        soup = BeautifulSoup(r.text, 'lxml')
        try:
            main_body = soup.find(name='div', attrs={'id': 'mainbody'})
            columnmakers = main_body.find_all(name='div', attrs={'class': 'columnmaker'})

            links = columnmakers[0].find_all(name='a')
            films = [a.get_text().strip() for a in links]
            with open('tmp/films.json', 'w') as fd:
                fd.write(json.dumps(films, indent=4))

            links = columnmakers[1].find_all(name='a')
            developers = [a.get_text().strip() for a in links]
            with open('tmp/developers.json', 'w') as fd:
                fd.write(json.dumps(developers, indent=4))
        except Exception as e:
            __Logger.error('failed to parse, err: {}'.format(e))
            sys.exit(1)


if __name__ == '__main__':
    import sys
    sys.exit(int(main() or 0))
