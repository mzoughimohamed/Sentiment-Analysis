
from django.contrib import admin
from django.urls import path,include
from . import views
from django.conf.urls.static import static
from . import settings
urlpatterns = [
    path('admin/', admin.site.urls),
    path('',views.homepage,name="homepage"),
    path('src',views.src,name="src"),
    path('tr',views.tr,name="tr"),
    path('pr',views.pr,name="pr"),
    path('clean',views.clean,name="clean"),
    path('scrape/',include("FbScraping.urls"),name="scrape"), 
    path('cleaning/',include("dfcleaning.urls"),name="cleaning"),
    path('train/',include("modeltrain.urls"),name="train"),
    path('predict/',include("prediction.urls"),name="predict"),   
]+static(settings.MEDIA_URL ,document_root=settings.MEDIA_ROOT)+static(settings.STATIC_URL ,document_root=settings.STATICFILES_DIRS)
if settings.DEBUG:
    urlpatterns +=static(settings.MEDIA_URL ,document_root=settings.MEDIA_ROOT)