from django.http import HttpResponse
from django.shortcuts import render


def index(request):
    return HttpResponse("欢迎访问龟龟摄影公众号服务!!!")