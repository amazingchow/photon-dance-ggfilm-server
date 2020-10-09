"""ggfilm URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/3.1/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.urls import path

from . import views

urlpatterns = [
    path('', views.index, name='index'),

    # 静态页面服务
    path('labbox/labboxguide', views.labbox_guide, name='labboxguide'),
    path('labbox/petfilmlist', views.labbox_petfilmlist, name='petfilmlist'),
    path('labbox/tutorials-120loading', views.labbox_tutorials_120loading, name='tutorials-120loading'),
    path('labbox/tutorials-135loading', views.labbox_tutorials_135loading, name='tutorials-135loading'),
    path('labbox/tutorials-changingmodules', views.labbox_tutorials_changingmodules, name='tutorials-changingmodules'),
    path('labbox/tutorials-filmguide', views.labbox_tutorials_filmguide, name='tutorials-filmguide'),
    path('labbox/tutorials-hubreels120', views.labbox_tutorials_hubreels120, name='tutorials-hubreels120'),
    path('labbox/tutorials-hubreels135', views.labbox_tutorials_hubreels135, name='tutorials-hubreels135'),
    path('labbox/tutorials-knob', views.labbox_tutorials_knob, name='tutorials-knob'),
    path('labbox/tutorials-module120', views.labbox_tutorials_module120, name='tutorials-module120'),
    path('labbox/tutorials-module135', views.labbox_tutorials_module135, name='tutorials-module135'),
    path('labbox/tutorials-pouringemptying', views.labbox_tutorials_pouringemptying, name='tutorials-pouringemptying'),

    # 动态查询服务
    path('search', views.select_film, name='searcher-select-film'),
    path('search/developer', views.select_developer, name='searcher-select-developer'),
    path('search/dilution', views.select_dilution, name='searcher-select-dilution'),
    path('search/asa_iso', views.select_iso, name='searcher-select-iso'),
    path('search/result', views.show_detail_info, name='searcher-show-detail-info'),
]