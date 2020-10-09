import re

from django.http import HttpResponse
from django.shortcuts import render
from django.views.decorators.cache import cache_page

from . import models


@cache_page(60 * 60 * 24)
def index(request):
    return HttpResponse("欢迎访问龟龟摄影公众号服务!!!")


@cache_page(60 * 60 * 24)
def labbox_guide(request):
    return render(request, "labboxguide.html")


@cache_page(60 * 60 * 24)
def labbox_petfilmlist(request):
    return render(request, "petfilmlist.html")


@cache_page(60 * 60 * 24)
def labbox_tutorials_120loading(request):
    return render(request, "tutorials-120loading.html")


@cache_page(60 * 60 * 24)
def labbox_tutorials_135loading(request):
    return render(request, "tutorials-135loading.html")


@cache_page(60 * 60 * 24)
def labbox_tutorials_changingmodules(request):
    return render(request, "tutorials-changingmodules.html")


@cache_page(60 * 60 * 24)
def labbox_tutorials_filmguide(request):
    return render(request, "tutorials-filmguide.html")


@cache_page(60 * 60 * 24)
def labbox_tutorials_hubreels120(request):
    return render(request, "tutorials-hubreels120.html")


@cache_page(60 * 60 * 24)
def labbox_tutorials_hubreels135(request):
    return render(request, "tutorials-hubreels135.html")


@cache_page(60 * 60 * 24)
def labbox_tutorials_knob(request):
    return render(request, "tutorials-knob.html")


@cache_page(60 * 60 * 24)
def labbox_tutorials_module120(request):
    return render(request, "tutorials-module120.html")


@cache_page(60 * 60 * 24)
def labbox_tutorials_module135(request):
    return render(request, "tutorials-module135.html")


@cache_page(60 * 60 * 24)
def labbox_tutorials_pouringemptying(request):
    return render(request, "tutorials-pouringemptying.html")


def esc_replace_view2db(s):
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


def esc_replace_db2view(s):
    s = s.replace("//", "/") 
    s = s.replace("''", '"')  
    s = s.replace("/[", "[") 
    s = s.replace("/]", "]") 
    s = s.replace("/%", "%") 
    s = s.replace("/&","&")
    s = s.replace("/_", "_") 
    s = s.replace("/(", "(") 
    s = s.replace("/)", ")")
    return s


@cache_page(60 * 60 * 24)
def select_film(request):
    films_35mm_query_set = models.FilmRecord.objects.exclude(a35mm="").\
        values_list('film', flat=True).distinct()
    films_35mm = [esc_replace_db2view(q) for q in films_35mm_query_set]
    films_35mm.sort()
    films_35mm_cnt = len(films_35mm)

    films_120_query_set = models.FilmRecord.objects.exclude(a120="").\
        values_list('film', flat=True).distinct()
    films_120 = [esc_replace_db2view(q) for q in films_120_query_set]
    films_120.sort()
    films_120_cnt = len(films_120)

    films_sheet_query_set = models.FilmRecord.objects.exclude(sheet="").\
        values_list('film', flat=True).distinct()
    films_sheet = [esc_replace_db2view(q) for q in films_sheet_query_set]
    films_sheet.sort()
    films_sheet_cnt = len(films_sheet)

    return render(request, "searcher-select-film.html", {
            "films_35mm": films_35mm,
            "films_35mm_cnt": films_35mm_cnt,
            "films_120": films_120,
            "films_120_cnt": films_120_cnt,
            "films_sheet": films_sheet,
            "films_sheet_cnt": films_sheet_cnt,
        })


def select_developer(request):
    source = request.GET.get("source")
    film = esc_replace_view2db(request.GET.get("film").replace('^', '+'))

    developer_query_set = []
    if source == "35毫米":
        developer_query_set = models.FilmRecord.objects.filter(film=film).\
            exclude(a35mm="").values_list('developer', flat=True).distinct()
    elif source == "120":
        developer_query_set = models.FilmRecord.objects.filter(film=film).\
            exclude(a120="").values_list('developer', flat=True).distinct()
    elif source == "页片":
        developer_query_set = models.FilmRecord.objects.filter(film=film).\
            exclude(sheet="").values_list('developer', flat=True).distinct()
    
    developers = [esc_replace_db2view(q) for q in developer_query_set]
    developers.sort()
    developers_cnt = len(developers)

    return render(request, "searcher-select-developer.html", {
            "nav": {
                "source": source,
                "film": esc_replace_db2view(film),
            },
            "developers": developers,
            "developers_cnt": developers_cnt,
        })


def select_dilution(request):
    source = request.GET.get("source")
    film = esc_replace_view2db(request.GET.get("film").replace('^', '+'))
    developer = esc_replace_view2db(request.GET.get("developer").replace('^', '+'))

    dilution_query_set = []
    if source == "35毫米":
        dilution_query_set = models.FilmRecord.objects.filter(film=film).\
            exclude(a35mm="").filter(developer=developer).\
                values_list('dilution', flat=True).distinct()
    elif source == "120":
        dilution_query_set = models.FilmRecord.objects.filter(film=film).\
            exclude(a120="").filter(developer=developer).\
                values_list('dilution', flat=True).distinct()
    elif source == "页片":
        dilution_query_set = models.FilmRecord.objects.filter(film=film).\
            exclude(sheet="").filter(developer=developer).\
                values_list('dilution', flat=True).distinct()
    
    dilutions = [esc_replace_db2view(q) for q in dilution_query_set]
    dilutions.sort()
    dilutions_cnt = len(dilutions)

    return render(request, "searcher-select-dilution.html", {
            "nav": {
                "source": source,
                "film": esc_replace_db2view(film),
                "developer": esc_replace_db2view(developer),
            },
            "dilutions": dilutions,
            "dilutions_cnt": dilutions_cnt,
        })


def select_iso(request):
    source = request.GET.get("source")
    film = esc_replace_view2db(request.GET.get("film").replace('^', '+'))
    developer = esc_replace_view2db(request.GET.get("developer").replace('^', '+'))
    dilution = esc_replace_view2db(request.GET.get("dilution").replace('^', '+'))

    iso_query_set = []
    if source == "35毫米":
        iso_query_set = models.FilmRecord.objects.filter(film=film).\
            exclude(a35mm="").filter(developer=developer).filter(dilution=dilution).\
                values_list('asa_iso', flat=True).distinct()
    elif source == "120":
        iso_query_set = models.FilmRecord.objects.filter(film=film).\
            exclude(a120="").filter(developer=developer).filter(dilution=dilution).\
                values_list('asa_iso', flat=True).distinct()
    elif source == "页片":
        iso_query_set = models.FilmRecord.objects.filter(film=film).\
            exclude(sheet="").filter(developer=developer).filter(dilution=dilution).\
                values_list('asa_iso', flat=True).distinct()
    
    asa_iso_list = [esc_replace_db2view(q) for q in iso_query_set]
    asa_iso_list.sort()
    asa_iso_list_cnt = len(asa_iso_list)

    return render(request, "searcher-select-iso.html", {
            "nav": {
                "source": source,
                "film": esc_replace_db2view(film),
                "developer": esc_replace_db2view(developer),
                "dilution": esc_replace_db2view(dilution),
            },
            "asa_iso_list": asa_iso_list,
            "asa_iso_list_cnt": asa_iso_list_cnt,
        })


def show_detail_info(request):
    source = request.GET.get("source")
    film = esc_replace_view2db(request.GET.get("film").replace('^', '+'))
    developer = esc_replace_view2db(request.GET.get("developer").replace('^', '+'))
    dilution = esc_replace_view2db(request.GET.get("dilution").replace('^', '+'))
    iso = esc_replace_view2db(request.GET.get("asa_iso").replace('^', '+'))

    result_query = None
    time = ""
    if source == "35毫米":
        result_query = models.FilmRecord.objects.filter(film=film).\
            exclude(a35mm="").filter(developer=developer).filter(dilution=dilution).filter(asa_iso=iso)[0]
        time = result_query.a35mm
    elif source == "120":
        result_query = models.FilmRecord.objects.filter(film=film).\
            exclude(a120="").filter(developer=developer).filter(dilution=dilution).filter(asa_iso=iso)[0]
        time = result_query.a120
    elif source == "页片":
        result_query = models.FilmRecord.objects.filter(film=film).\
            exclude(sheet="").filter(developer=developer).filter(dilution=dilution).filter(asa_iso=iso)[0]
        time = result_query.sheet

    temperature = result_query.temp.split("C")[0]

    note_list = []
    if result_query.notes != "":
        note_orders = esc_replace_db2view(result_query.notes)
        note_orders = re.findall(r"\[(.*?)\]", note_orders)
        for note_order in note_orders:
            if note_order == "46":
                pass
            else:
                note = models.MassiveDevChartNote.objects.get(note=esc_replace_view2db('[{}]'.format(note_order))).remark
                note_list.append(esc_replace_db2view(note))
    has_note = len(note_list)
    
    return render(request, "searcher-select-detail-info.html", {
            "nav": {
                "source": source,
                "film": esc_replace_db2view(film),
                "developer": esc_replace_db2view(developer),
                "dilution": esc_replace_db2view(dilution),
                "asa_iso": esc_replace_db2view(iso),
            },
            "time": time,
            "temperature": esc_replace_db2view(temperature),
            "has_note": has_note,
            "note_list": note_list,
        })
