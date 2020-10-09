# -*- coding: utf-8 -*-
import datetime
import hashlib
import logging
__Logger = logging.getLogger('records_fetcher')
__Logger.setLevel(logging.INFO)
__Formatter = logging.Formatter("[%(asctime)-15s][%(levelname)-5s] %(message)s", datefmt="%Y-%m-%d %H:%M:%S")
__FileHandler = logging.FileHandler('log/records_fetcher.log', 'w')
__FileHandler.setFormatter(__Formatter)
__Logger.addHandler(__FileHandler)
import pathlib

import requests
import tqdm
import ujson as json

from bs4 import BeautifulSoup
from ratelimit import limits, RateLimitException, sleep_and_retry

from common import RequestHeaders


@sleep_and_retry
@limits(calls=90, period=900)
def http_request(session, url, date):
    session.get(url=url, headers=RequestHeaders, hooks={"response": hook_factory(date=date)}) 


def hook_factory(*factory_args, **factory_kwargs):
    def response_hook(response, *request_args, **request_kwargs):
        date = factory_kwargs["date"]

        __Logger.info('fetch record on <{}>'.format(response.url))
        if response.status_code == 200:
            __Logger.info('response status code: {}'.format(response.status_code))
        elif response.status_code == 429:
            raise RateLimitException("api response: 429", 5)
        else:
            _Logger.warning('failed to fetch, response status code: {}'.format(response.status_code))
            return

        if response.text == "":
            return

        response.encoding = "utf-8"
        soup = BeautifulSoup(response.text, "lxml")
        try:
            main_text = soup.find(name='div', attrs={'class': 'maintext'})
            records_table = main_text.find(name='table', attrs={'class': 'mdctable'})
            records_trs = records_table.find_all(name='tr')[1:]

            records = []
            for tr in records_trs:
                tds = tr.find_all(name='td')
                record = {}
                record['Film'] = tds[0].get_text().strip()
                record['Developer'] = tds[1].get_text().strip()
                record['Dilution'] = tds[2].get_text().strip()
                record['ASA/ISO'] = tds[3].get_text().strip()
                record['35mm'] = tds[4].get_text().strip()
                record['120'] = tds[5].get_text().strip()
                record['Sheet'] = tds[6].get_text().strip()
                record['Temp'] = tds[7].get_text().strip()
                record['Notes'] = tds[8].get_text().strip()
                records.append(record)

            with open('tmp/record_{}_{}.json'.format(md5hash(response.url), date), 'w') as fd:
                fd.write(json.dumps(records, indent=4))
        except Exception as e:
            __Logger.error('failed to parse, err: {}'.format(e))
        return None
    return response_hook


def md5hash(fn):
    h = hashlib.md5()
    h.update(str.encode(fn))
    return h.hexdigest()


def callback_func(r, *args, **kwargs):
    __Logger.info('fetch records on <{}>'.format(r.url))
    if r.status_code == 200:
        __Logger.info('response status code: {}'.format(r.status_code))
    else:
        __Logger.warning('failed to fetch, response status code: {}'.format(r.status_code))


def has_fetched(url, date):
    f = pathlib.Path('tmp/record_{}_{}.json'.format(md5hash(url), date))
    return f.exists()


def main():
    url = 'https://www.digitaltruth.com/chart/print.php'

    r = requests.get(url, headers=RequestHeaders, hooks=dict(response=callback_func))
    if r.status_code == 200:
        urls = []

        soup = BeautifulSoup(r.text, 'lxml')
        try:
            main_body = soup.find(name='div', attrs={'id': 'mainbody'})
            columnmaker = main_body.find_all(name='div', attrs={'class': 'columnmaker'})[0]
            links = columnmaker.find_all(name='a')
            urls = ['https://www.digitaltruth.com/chart/' + a['href'].strip() for a in links]
            with open('tmp/links.json', 'w') as fd:
                fd.write(json.dumps(urls, indent=4))
            __Logger.info('{} links to be fetched'.format(len(urls)))
        except Exception as e:
            __Logger.error('failed to parse, err: {}'.format(e))
            sys.exit(1)

        with requests.Session() as session:
            for url in tqdm.tqdm(urls):
                if not has_fetched(url, datetime.date.today()):
                    http_request(session, url, datetime.date.today())
                else:
                    __Logger.info('since we has fetched <{}>, ignore it'.format(url))


if __name__ == '__main__':
    import sys
    sys.exit(int(main() or 0))
