# -*- coding: utf-8 -*-
import logging
__Logger = logging.getLogger('notes_fetcher')
__Logger.setLevel(logging.INFO)
__Formatter = logging.Formatter("[%(asctime)-15s][%(levelname)-5s] %(message)s", datefmt="%Y-%m-%d %H:%M:%S")
__FileHandler = logging.FileHandler('log/notes_fetcher.log', 'w')
__FileHandler.setFormatter(__Formatter)
__Logger.addHandler(__FileHandler)

import requests
import ujson as json

from bs4 import BeautifulSoup

from common import RequestHeaders


def callback_func(r, *args, **kwargs):
    __Logger.info('fetch notes on <{}>'.format(r.url))
    if r.status_code == 200:
        __Logger.info('response status code: {}'.format(r.status_code))
    else:
        __Logger.warning('failed to fetch, response status code: {}'.format(r.status_code))


def main():
    url = 'https://www.digitaltruth.com/chart/notes.php'

    r = requests.get(url, headers=RequestHeaders, hooks=dict(response=callback_func))
    if r.status_code == 200:
        soup = BeautifulSoup(r.text, 'lxml')
        try:
            main_text = soup.find(name='div', attrs={'class': 'maintext'})
            notes_table = main_text.find(name='table', attrs={'class': 'mdctable'})
            notes_trs = notes_table.find_all(name='tr')
            notes = {'[{}]'.format(tr.find_all(name='td')[0].get_text().strip()): tr.find_all(name='td')[1].get_text().strip() for tr in notes_trs}
            with open('tmp/notes.json', 'w') as fd:
                fd.write(json.dumps(notes, indent=4))
            __Logger.info('parse {} notes'.format(len(notes)))
        except Exception as e:
            __Logger.error('failed to parse, err: {}'.format(e))


if __name__ == '__main__':
    import sys
    sys.exit(int(main() or 0))
