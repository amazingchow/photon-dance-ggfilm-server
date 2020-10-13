# -*- coding: utf-8 -*-
import logging
logging.basicConfig(
    filename='wechat_ggfilm_backend/utils/log/update_checker.log',
    filemode='w',
    format='[%(asctime)-15s][%(levelname)-5s] %(message)s',
    datefmt='%Y-%m-%d %H:%M:%S',
    level=logging.INFO,
)

import requests

from bs4 import BeautifulSoup
from selenium import webdriver
from selenium.common.exceptions import NoSuchElementException
from selenium.common.exceptions import TimeoutException
from selenium.common.exceptions import WebDriverException
from selenium.webdriver.common.desired_capabilities import DesiredCapabilities
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC

from .common import RequestHeaders

import os
os.environ.setdefault("DJANGO_SETTINGS_MODULE", "ggfilm.settings")
import django
django.setup()
from .utils import esc_replace_view2db
from ..models import FilmRecord
from ..models import FilmRecordUpdateLocker
from ..models import MassiveDevChartFilm


def parse_link(html):
    soup = BeautifulSoup(html, 'lxml', from_encoding='utf-8')

    try:
        trs = soup.find_all(name='tr')[1:]
        for tr in trs:
            try:
                tds = tr.find_all(name='td')

                film = tds[0].get_text().strip()
                developer = tds[1].get_text().strip()
                dilution = tds[2].get_text().strip()
                asa_iso = tds[3].get_text().strip()
                a35mm = tds[4].get_text().strip()
                a120 = tds[5].get_text().strip()
                sheet = tds[6].get_text().strip()
                temp = tds[7].get_text().strip()

                notes_link = tds[8].find(name='a')
                notes = ''
                if notes_link != None:
                    link = notes_link.get('href').strip()
                    link = 'https://www.digitaltruth.com/' + link
                    r = requests.get(link, headers=RequestHeaders)
                    if r.status_code == 200:
                        soup_inner = BeautifulSoup(r.text, 'lxml', from_encoding='utf8')
                        try:
                            notes = soup_inner.find_all(name='tr')[1].find_all(name='td')[-1].get_text().strip()
                        except Exception as e:
                            logging.error('failed to parse, err: {}'.format(e))
                    else:
                        logging.error('failed to fetch {}, err: {}'.format(r.url, e))
                
                # 检查是否需要添加新记录
                try:
                    obj = FilmRecord.objects.using('massive_dev_chart_primary').get(
                            film=esc_replace_view2db(film),
                            developer=esc_replace_view2db(developer),
                            dilution=esc_replace_view2db(dilution),
                            asa_iso=esc_replace_view2db(asa_iso),
                            temp=esc_replace_view2db(temp),
                        )
                    obj.a35mm = a35mm
                    obj.a120 = a120
                    obj.sheet = sheet
                    obj.notes = notes
                    obj.save(using='massive_dev_chart_primary')
                    logging.info('update one film record')
                except FilmRecord.DoesNotExist:
                    obj = FilmSearch(
                            film=esc_replace_view2db(film),
                            developer=esc_replace_view2db(developer),
                            dilution=esc_replace_view2db(dilution),
                            asa_iso=esc_replace_view2db(asa_iso),
                            a35mm=esc_replace_view2db(a35mm),
                            a120=esc_replace_view2db(a120),
                            sheet=esc_replace_view2db(sheet),
                            temp=esc_replace_view2db(temp),
                            notes=esc_replace_view2db(notes),
                        )
                    obj.save(using='massive_dev_chart_primary')
                    logging.info('insert one film record')
                
                try:
                    MassiveDevChartFilm.objects.using('massive_dev_chart_primary').get(
                        name=esc_replace_view2db(film),
                    )
                except MassiveDevChartFilm.DoesNotExist:
                    obj = MassiveDevChartFilm(name=esc_replace_view2db(film))
                    obj.save(using='massive_dev_chart_primary')
                    logging.info('insert one film')
            except Exception as e:
                logging.error('failed to parse, err: {}'.format(e))
    except Exception as e:
        logging.error('failed to parse, err: {}'.format(e))


def callback_func(r, *args, **kwargs):
    logging.info('fetch last updated time on <{}>'.format(r.url))
    if r.status_code == 200:
        logging.info('response status code: {}'.format(r.status_code))
    else:
        logging.warning('failed to fetch, response status code: {}'.format(r.status_code))


def main():
    track_url = 'https://www.digitaltruth.com/devchart.php?doc=search'

    r = requests.get(track_url, headers=RequestHeaders, hooks=dict(response=callback_func))
    if r.status_code == 200:
        soup = BeautifulSoup(r.text, 'lxml')
        try:
            main_box = soup.find(name='div', attrs={'id': 'mdcmainbox'})
            intro = main_box.find(name='div', attrs={'id': 'mdcintro'})
            form = intro.find(name='form', attrs={'name': 'idForm'})
            text = form.get_text().strip()
            
            fr = open('wechat_ggfilm_backend/utils/last_updated.txt', 'r')
            last_updated = fr.readline()
            fr.close()
            if last_updated != text:
                fw = open('wechat_ggfilm_backend/utils/last_updated.txt', 'w')
                fw.write(text)
                fw.close()
                logging.info('we need to update the database')

                try:
                    d_cap = dict(DesiredCapabilities.PHANTOMJS)
                    d_cap["phantomjs.page.settings.userAgent"] = 'Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/84.0.4147.105 Safari/537.36'
                    d_cap["phantomjs.page.settings.loadImages"] = False
                    driver = webdriver.PhantomJS(
                            executable_path='/usr/local/bin/phantomjs',
                            desired_capabilities=d_cap,
                            service_args=[
                                '--load-images=no',          # 禁止加载图片
                                '--disk-cache=yes',          # 开启浏览器缓存
                                '--ignore-ssl-errors=true',  # 忽略HTTPS错误
                                '--ssl-protocol=TLSv1',
                            ]
                        )
                    driver.set_window_size(1280, 1024)        
                    try:
                        driver.get(track_url)
                        try:
                            links_wrapper = WebDriverWait(driver, 10).until(
                                EC.presence_of_element_located((By.XPATH, "//form[@name='idForm']"))
                            )
                            link = WebDriverWait(links_wrapper, 10).until(
                                EC.presence_of_element_located((By.TAG_NAME, "a"))
                            )
                            link.click()

                            time.sleep(2)
                            parse_link(driver.page_source)
                        except NoSuchElementException as e:
                            logging.error('failed to parse, err: {}'.format(e))
                    except TimeoutException as e:
                        logging.error('failed to fetch {}, err: {}'.format(track_url, e))
                    finally:
                        driver.close()
                except WebDriverException as e:
                    logging.error('failed to create web driver using phantomjs, err: {}'.format(e))             
            else:
                logging.warning('no need to update database')
        except Exception as e:
            logging.error('failed to parse, err: {}'.format(e))


if __name__ == '__main__':
    # under ${project_root}/ggfilm, execute 'python -m wechat_ggfilm_backend.utils.check_update'

    import sys
    sys.exit(int(main() or 0))
