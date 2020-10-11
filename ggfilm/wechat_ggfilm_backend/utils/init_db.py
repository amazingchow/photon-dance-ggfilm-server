# -*- coding: utf-8 -*-
import glob

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
        MassiveDevChartFilm.objects.all().delete()
    with open(fn, 'r') as fd:
        for name in json.loads(fd.read()):
            try:
                MassiveDevChartFilm.objects.get(
                    name=esc_replace(name),
                )
            except MassiveDevChartFilm.DoesNotExist:
                f = MassiveDevChartFilm(name=esc_replace(name))
                f.save()


def store_massive_dev_chart_developers(fn, exist=False):
    if exist:
        MassiveDevChartDeveloper.objects.all().delete()
    with open(fn, 'r') as fd:
        for name in json.loads(fd.read()):
            try:
                MassiveDevChartDeveloper.objects.get(
                    name=esc_replace(name),
                )
            except MassiveDevChartDeveloper.DoesNotExist:
                d = MassiveDevChartDeveloper(name=esc_replace(name))
                d.save()


def store_massive_dev_chart_notes(fn, exist=False):
    if exist:
        MassiveDevChartNote.objects.all().delete()
    with open(fn, 'r') as fd:
        for k, v in json.loads(fd.read()).items():            
            remark = v
            if k in NoteMap.keys():
                remark = NoteMap[k]

            try:
                MassiveDevChartNote.objects.get(
                    note=esc_replace(k),
                )
            except MassiveDevChartNote.DoesNotExist:
                n = MassiveDevChartNote(note=esc_replace(k), remark=esc_replace(remark))
                n.save()


def store_massive_dev_chart_records(fn):
    with open(fn, 'r') as fd:
        for record in json.loads(fd.read()):
            try:
                FilmRecord.objects.get(
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
                r.save()


def init_massive_dev_chart_film_record_update_locker():
    l = FilmRecordUpdateLocker(name='film_record_update_locker')
    l.save()


def main():
    store_massive_dev_chart_films('wechat_ggfilm_backend/utils/tmp/films.json')
    store_massive_dev_chart_developers('wechat_ggfilm_backend/utils/tmp/developers.json')
    store_massive_dev_chart_notes('wechat_ggfilm_backend/utils/tmp/notes.json')
    for fn in tqdm.tqdm(glob.glob('wechat_ggfilm_backend/utils/tmp/record_*.json')):
        store_massive_dev_chart_records(fn)
    init_massive_dev_chart_film_record_update_locker()


if __name__ == '__main__':
    # under ${project_root}/ggfilm, execute 'python -m wechat_ggfilm_backend.utils.init_db'

    import sys
    sys.exit(int(main() or 0))
