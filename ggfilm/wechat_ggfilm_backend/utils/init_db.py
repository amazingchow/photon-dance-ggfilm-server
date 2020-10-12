# -*- coding: utf-8 -*-
import glob
import logging
__Logger = logging.getLogger('init_db')
__Logger.setLevel(logging.INFO)
__Formatter = logging.Formatter("[%(asctime)-15s][%(levelname)-5s] %(message)s", datefmt="%Y-%m-%d %H:%M:%S")
__FileHandler = logging.FileHandler('utils/log/init_db.log', 'w')
__FileHandler.setFormatter(__Formatter)
__Logger.addHandler(__FileHandler)

import tqdm
import ujson as json

from .common import NoteMap

import os
os.environ.setdefault("DJANGO_SETTINGS_MODULE", "ggfilm.settings")
import django
django.setup()
from ..models import FilmRecord
from ..models import FilmRecordUpdateLocker
from ..models import MassiveDevChartDeveloper
from ..models import MassiveDevChartFilm
from ..models import MassiveDevChartNote


def esc_replace(s):
    s = s.replace("/", "//") 
    s = s.replace("'", "''")
    s = s.replace('"', "''")  
    s = s.replace("[", "/[") 
    s = s.replace("]", "/]") 
    s = s.replace("%", "/%") 
    s = s.replace("&","/&")
    s = s.replace("_", "/_") 
    s = s.replace("(", "/(") 
    s = s.replace(")", "/)")
    return s


def store_massive_dev_chart_films(fn, exist=False):
    if exist:
        MassiveDevChartFilm.objects.all().using('massive_dev_chart').delete()
    with open(fn, 'r') as fd:
        for name in json.loads(fd.read()):
            try:
                MassiveDevChartFilm.objects.using('massive_dev_chart').get(
                    name=esc_replace(name),
                )
            except MassiveDevChartFilm.DoesNotExist:
                f = MassiveDevChartFilm(name=esc_replace(name))
                f.save(using='massive_dev_chart')


def store_massive_dev_chart_developers(fn, exist=False):
    if exist:
        MassiveDevChartDeveloper.objects.all().using('massive_dev_chart').delete()
    with open(fn, 'r') as fd:
        for name in json.loads(fd.read()):
            try:
                MassiveDevChartDeveloper.objects.using('massive_dev_chart').get(
                    name=esc_replace(name),
                )
            except MassiveDevChartDeveloper.DoesNotExist:
                d = MassiveDevChartDeveloper(name=esc_replace(name))
                d.save(using='massive_dev_chart')


def store_massive_dev_chart_notes(fn, exist=False):
    if exist:
        MassiveDevChartNote.objects.all().using('massive_dev_chart').delete()
    with open(fn, 'r') as fd:
        for k, v in json.loads(fd.read()).items():            
            remark = v
            if k in NoteMap.keys():
                remark = NoteMap[k]

            try:
                MassiveDevChartNote.objects.using('massive_dev_chart').get(
                    note=esc_replace(k),
                )
            except MassiveDevChartNote.DoesNotExist:
                n = MassiveDevChartNote(note=esc_replace(k), remark=esc_replace(remark))
                n.save(using='massive_dev_chart')


def store_massive_dev_chart_records(fn):
    with open(fn, 'r') as fd:
        for record in json.loads(fd.read()):
            try:
                FilmRecord.objects.using('massive_dev_chart').get(
                    film=esc_replace(record['Film']),
                    developer=esc_replace(record['Developer']),
                    dilution=esc_replace(record['Dilution']),
                    asa_iso=esc_replace(record['ASA/ISO']),
                    a35mm=esc_replace(record['35mm']),
                    a120=esc_replace(record['120']),
                    sheet=esc_replace(record['Sheet']),
                    temp=esc_replace(record['Temp']),
                    notes=esc_replace(record['Notes']),
                )
            except FilmRecord.DoesNotExist:
                r = FilmRecord(
                    film=esc_replace(record['Film']),
                    developer=esc_replace(record['Developer']),
                    dilution=esc_replace(record['Dilution']),
                    asa_iso=esc_replace(record['ASA/ISO']),
                    a35mm=esc_replace(record['35mm']),
                    a120=esc_replace(record['120']),
                    sheet=esc_replace(record['Sheet']),
                    temp=esc_replace(record['Temp']),
                    notes=esc_replace(record['Notes']),
                )
                r.save(using='massive_dev_chart')


def init_massive_dev_chart_film_record_update_locker():
    l = FilmRecordUpdateLocker(name='film_record_update_locker')
    l.save(using='massive_dev_chart')


def main():
    store_massive_dev_chart_films('wechat_ggfilm_backend/utils/tmp/films.json')
    __Logger.info('store massive-dev-chart films')
    store_massive_dev_chart_developers('wechat_ggfilm_backend/utils/tmp/developers.json')
    __Logger.info('store massive-dev-chart developers')
    store_massive_dev_chart_notes('wechat_ggfilm_backend/utils/tmp/notes.json')
    __Logger.info('store massive-dev-chart notes')
    for fn in tqdm.tqdm(glob.glob('wechat_ggfilm_backend/utils/tmp/record_*.json')):
        store_massive_dev_chart_records(fn)
    __Logger.info('store massive-dev-chart film-records')
    init_massive_dev_chart_film_record_update_locker()
    __Logger.info('store massive-dev-chart film-record-update-locker')


if __name__ == '__main__':
    # under ${project_root}/ggfilm, execute 'python -m wechat_ggfilm_backend.utils.init_db'

    import sys
    sys.exit(int(main() or 0))
