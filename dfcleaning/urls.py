from django.urls import path,include
from . import views
urlpatterns = [
    path('',views.home,name="home"),
    path('result',views.result,name="result"),
    path('download',views.download,name="download")
]