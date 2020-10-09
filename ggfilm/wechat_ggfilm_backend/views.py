from django.http import HttpResponse
from django.shortcuts import render
from django.views.decorators.cache import cache_page


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
