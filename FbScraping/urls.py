from django.urls import path
from . import views
urlpatterns = [
    path('',views.homes,name="homes"),
    path('resulturl',views.resulturl,name="resulturl"),
    path('resultfile',views.resultfile,name='resultfile'),
    path('file',views.filescraper,name="file"),
    path('downloads',views.download,name="downloads"),
    path('telecharger',views.telecharger,name="telecharger"),
    path('downloadfull',views.downloadfull,name="downloadfull"),
    path('downloadjson',views.downloadjson,name="downloadjson"),
] 