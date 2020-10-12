import logging
__Logger = logging.getLogger('tests')
__Logger.setLevel(logging.INFO)
__Formatter = logging.Formatter("[%(asctime)-15s][%(levelname)-5s] %(message)s", datefmt="%Y-%m-%d %H:%M:%S")
__FileHandler = logging.FileHandler('log/tests.log', 'w')
__FileHandler.setFormatter(__Formatter)
__Logger.addHandler(__FileHandler)
import os
os.environ.setdefault("DJANGO_SETTINGS_MODULE", "ggfilm.settings")

import django
django.setup()
import tqdm

from django.test import Client

from . import models
from .utils.utils import esc_replace_db2view
from .utils.utils import esc_replace_view2db


def film_access_testting(cli):
    response = cli.get('/search')
    if response.status_code != 200:
        __Logger.error("failed to access /search")

    films_35mm_query_set = models.FilmRecord.objects.exclude(a35mm="").\
        values_list('film', flat=True).distinct()
    films_35mm = [esc_replace_db2view(q) for q in films_35mm_query_set]
    if len(films_35mm) != 0:
        films_35mm.sort()
        for film in tqdm.tqdm(films_35mm):
            developer_access_testting(cli, "35毫米", film)
    else:
        __Logger.error("no 35mm film")

    films_120_query_set = models.FilmRecord.objects.exclude(a120="").\
        values_list('film', flat=True).distinct()
    films_120 = [esc_replace_db2view(q) for q in films_120_query_set]
    if len(films_120) != 0:
        films_120.sort()
        for film in tqdm.tqdm(films_120):
            developer_access_testting(cli, "120", film)
    else:
        __Logger.error("no 120 film")

    films_sheet_query_set = models.FilmRecord.objects.exclude(sheet="").\
        values_list('film', flat=True).distinct()
    films_sheet = [esc_replace_db2view(q) for q in films_sheet_query_set]
    if len(films_sheet) != 0:
        films_sheet.sort()
        for film in tqdm.tqdm(films_sheet):
            developer_access_testting(cli, "页片", film)
    else:
        __Logger.error("no sheet film")


def developer_access_testting(cli, source, film):
    path = '/search/developer?source={}&film={}'.format(source, film.replace("+", "^"))
    response = cli.get(path)
    if response.status_code != 200:
        __Logger.error("failed to access {}".format(path))
    else:
        developer_query_set = []
        if source == "35毫米":
            developer_query_set = models.FilmRecord.objects.filter(film=esc_replace_view2db(film)).\
                exclude(a35mm="").values_list('developer', flat=True).distinct()
        elif source == "120":
            developer_query_set = models.FilmRecord.objects.filter(film=esc_replace_view2db(film)).\
                exclude(a120="").values_list('developer', flat=True).distinct()
        elif source == "页片":
            developer_query_set = models.FilmRecord.objects.filter(film=esc_replace_view2db(film)).\
                exclude(sheet="").values_list('developer', flat=True).distinct()
        
        developers = [esc_replace_db2view(q) for q in developer_query_set]
        if len(developers) != 0:
            developers.sort()
            for developer in tqdm.tqdm(developers):
                dilution_access_testting(cli, source, film, developer)
        else:
            __Logger.error("no developer from {}".format(path))


def dilution_access_testting(cli, source, film, developer):
    path = '/search/dilution?source={}&film={}&developer={}'.format(source, 
        film.replace("+", "^"), developer.replace("+", "^"))
    response = cli.get(path)
    if response.status_code != 200:
        __Logger.error("failed to access {}".format(path))
    else:
        dilution_query_set = []
        if source == "35毫米":
            dilution_query_set = models.FilmRecord.objects.filter(film=esc_replace_view2db(film)).\
                exclude(a35mm="").filter(developer=esc_replace_view2db(developer)).\
                    values_list('dilution', flat=True).distinct()
        elif source == "120":
            dilution_query_set = models.FilmRecord.objects.filter(film=esc_replace_view2db(film)).\
                exclude(a120="").filter(developer=esc_replace_view2db(developer)).\
                    values_list('dilution', flat=True).distinct()
        elif source == "页片":
            dilution_query_set = models.FilmRecord.objects.filter(film=esc_replace_view2db(film)).\
                exclude(sheet="").filter(developer=esc_replace_view2db(developer)).\
                    values_list('dilution', flat=True).distinct()
        
        dilutions = [esc_replace_db2view(q) for q in dilution_query_set]
        if len(dilutions) != 0:
            dilutions.sort()
            for dilution in tqdm.tqdm(dilutions):
                iso_access_testting(cli, source, film, developer, dilution)
        else:
            __Logger.error("no dilution from {}".format(path))


def iso_access_testting(cli, source, film, developer, dilution):
    path = '/search/asa_iso?source={}&film={}&developer={}&dilution={}'.format(source, 
        film.replace("+", "^"), developer.replace("+", "^"), dilution.replace("+", "^"))
    response = cli.get(path)
    if response.status_code != 200:
        __Logger.error("failed to access {}".format(path))
    else:
        iso_query_set = []
        if source == "35毫米":
            iso_query_set = models.FilmRecord.objects.filter(film=esc_replace_view2db(film)).\
                exclude(a35mm="").filter(developer=esc_replace_view2db(developer)).\
                    filter(dilution=esc_replace_view2db(dilution)).values_list('asa_iso', flat=True).distinct()
        elif source == "120":
            iso_query_set = models.FilmRecord.objects.filter(film=esc_replace_view2db(film)).\
                exclude(a120="").filter(developer=esc_replace_view2db(developer)).\
                    filter(dilution=esc_replace_view2db(dilution)).values_list('asa_iso', flat=True).distinct()
        elif source == "页片":
            iso_query_set = models.FilmRecord.objects.filter(film=esc_replace_view2db(film)).\
                exclude(sheet="").filter(developer=esc_replace_view2db(developer)).\
                    filter(dilution=esc_replace_view2db(dilution)).values_list('asa_iso', flat=True).distinct()
        
        asa_iso_list = [esc_replace_db2view(q) for q in iso_query_set]
        if len(asa_iso_list) != 0:
            asa_iso_list.sort()
            for iso in tqdm.tqdm(asa_iso_list):
                result_access_testting(cli, source, film, developer, dilution, iso)
        else:
            __Logger.error("no iso from {}".format(path))


def result_access_testting(cli, source, film, developer, dilution, iso):
    path = '/search/result?source={}&film={}&developer={}&dilution={}&asa_iso={}'.format(source, 
        film.replace("+", "^"), developer.replace("+", "^"), dilution.replace("+", "^"), iso.replace("+", "^"))
    response = cli.get(path)
    if response.status_code != 200:
        __Logger.error("failed to access {}".format(path))
    else:
        result_query_set = []
        if source == "35毫米":
            result_query_set = models.FilmRecord.objects.filter(film=esc_replace_view2db(film)).\
                exclude(a35mm="").filter(developer=esc_replace_view2db(developer)).\
                    filter(dilution=esc_replace_view2db(dilution)).filter(asa_iso=esc_replace_view2db(iso))
        elif source == "120":
            result_query_set = models.FilmRecord.objects.filter(film=esc_replace_view2db(film)).\
                exclude(a120="").filter(developer=esc_replace_view2db(developer)).\
                    filter(dilution=esc_replace_view2db(dilution)).filter(asa_iso=esc_replace_view2db(iso))
        elif source == "页片":
            result_query_set = models.FilmRecord.objects.filter(film=esc_replace_view2db(film)).\
                exclude(sheet="").filter(developer=esc_replace_view2db(developer)).\
                    filter(dilution=esc_replace_view2db(dilution)).filter(asa_iso=esc_replace_view2db(iso))

        if len(result_query_set) == 0:
            __Logger.error("no result from {}".format(path))


if __name__ == "__main__":
    # under ${project_root}/ggfilm, execute 'python -m wechat_ggfilm_backend.tests'

    cli = Client()
    film_access_testting(cli)
