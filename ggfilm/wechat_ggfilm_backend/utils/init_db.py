# -*- coding: utf-8 -*-
import glob
import logging
logging.basicConfig(
    filename='wechat_ggfilm_backend/utils/log/init_db.log',
    filemode='w',
    format='[%(asctime)-15s][%(levelname)-5s] %(message)s',
    datefmt='%Y-%m-%d %H:%M:%S',
    level=logging.INFO,
)

import tqdm
import ujson as json

from .common import NoteMap

import os
os.environ.setdefault("DJANGO_SETTINGS_MODULE", "ggfilm.settings")
import django
django.setup()
from .utils import esc_replace_view2db
from ..models import FilmRecord
from ..models import FilmRecordUpdateLocker
from ..models import MassiveDevChartDeveloper
from ..models import MassiveDevChartFilm
from ..models import MassiveDevChartNote


def store_massive_dev_chart_films(fn, exist=False):
    if exist:
        MassiveDevChartFilm.objects.all().using('massive_dev_chart_primary').delete()
    with open(fn, 'r') as fd:
        for name in json.loads(fd.read()):
            try:
                MassiveDevChartFilm.objects.using('massive_dev_chart_primary').get(
                    name=esc_replace_view2db(name),
                )
            except MassiveDevChartFilm.DoesNotExist:
                f = MassiveDevChartFilm(name=esc_replace_view2db(name))
                f.save(using='massive_dev_chart_primary')


def store_massive_dev_chart_developers(fn, exist=False):
    if exist:
        MassiveDevChartDeveloper.objects.all().using('massive_dev_chart_primary').delete()
    with open(fn, 'r') as fd:
        for name in json.loads(fd.read()):
            try:
                MassiveDevChartDeveloper.objects.using('massive_dev_chart_primary').get(
                    name=esc_replace_view2db(name),
                )
            except MassiveDevChartDeveloper.DoesNotExist:
                d = MassiveDevChartDeveloper(name=esc_replace_view2db(name))
                d.save(using='massive_dev_chart_primary')


def store_massive_dev_chart_notes(fn, exist=False):
    if exist:
        MassiveDevChartNote.objects.all().using('massive_dev_chart_primary').delete()
    with open(fn, 'r') as fd:
        for k, v in json.loads(fd.read()).items():            
            remark = v
            if k in NoteMap.keys():
                remark = NoteMap[k]

            try:
                MassiveDevChartNote.objects.using('massive_dev_chart_primary').get(
                    note=esc_replace_view2db(k),
                )
            except MassiveDevChartNote.DoesNotExist:
                n = MassiveDevChartNote(note=esc_replace_view2db(k), remark=esc_replace_view2db(remark))
                n.save(using='massive_dev_chart_primary')


def store_massive_dev_chart_records(fn):
    with open(fn, 'r') as fd:
        for record in json.loads(fd.read()):
            try:
                FilmRecord.objects.using('massive_dev_chart_primary').get(
                    film=esc_replace_view2db(record['Film']),
                    developer=esc_replace_view2db(record['Developer']),
                    dilution=esc_replace_view2db(record['Dilution']),
                    asa_iso=esc_replace_view2db(record['ASA/ISO']),
                    a35mm=esc_replace_view2db(record['35mm']),
                    a120=esc_replace_view2db(record['120']),
                    sheet=esc_replace_view2db(record['Sheet']),
                    temp=esc_replace_view2db(record['Temp']),
                    notes=esc_replace_view2db(record['Notes']),
                )
            except FilmRecord.DoesNotExist:
                r = FilmRecord(
                    film=esc_replace_view2db(record['Film']),
                    developer=esc_replace_view2db(record['Developer']),
                    dilution=esc_replace_view2db(record['Dilution']),
                    asa_iso=esc_replace_view2db(record['ASA/ISO']),
                    a35mm=esc_replace_view2db(record['35mm']),
                    a120=esc_replace_view2db(record['120']),
                    sheet=esc_replace_view2db(record['Sheet']),
                    temp=esc_replace_view2db(record['Temp']),
                    notes=esc_replace_view2db(record['Notes']),
                )
                r.save(using='massive_dev_chart_primary')


def init_massive_dev_chart_film_record_update_locker():
    l = FilmRecordUpdateLocker(name='film_record_update_locker')
    l.save(using='massive_dev_chart_primary')


def main():
    store_massive_dev_chart_films('wechat_ggfilm_backend/utils/tmp/films.json')
    logging.info('store massive-dev-chart films')
    store_massive_dev_chart_developers('wechat_ggfilm_backend/utils/tmp/developers.json')
    logging.info('store massive-dev-chart developers')
    store_massive_dev_chart_notes('wechat_ggfilm_backend/utils/tmp/notes.json')
    logging.info('store massive-dev-chart notes')
    for fn in tqdm.tqdm(glob.glob('wechat_ggfilm_backend/utils/tmp/record_*.json')):
        store_massive_dev_chart_records(fn)
    logging.info('store massive-dev-chart film-records')
    init_massive_dev_chart_film_record_update_locker()
    logging.info('store massive-dev-chart film-record-update-locker')


if __name__ == '__main__':
    # under ${project_root}/ggfilm, execute 'python -m wechat_ggfilm_backend.utils.init_db'

    import sys
    sys.exit(int(main() or 0))
