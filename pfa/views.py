from django.http import HttpResponse,HttpResponseRedirect,Http404
from django.shortcuts import render
from django.core.files.storage import FileSystemStorage
from . import settings
import os
def homepage (request):
    return render(request,"homepage.html")
def src(request):
    return HttpResponseRedirect("/scrape")
def clean(request):
    return HttpResponseRedirect("/cleaning")
def tr(request):
    return HttpResponseRedirect("/train")
def pr(request):
    return HttpResponseRedirect("/predict")


