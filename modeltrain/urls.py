from django.urls import path
from . import views
urlpatterns = [
    path('',views.index,name="index"),
    path('metrics',views.trainmetrics,name="metrics"),
    path('filedownload',views.filedownload,name="filedownload")
]