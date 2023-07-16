from django.shortcuts import render
from django.http import HttpResponseRedirect,HttpResponse
import pandas as pd
import numpy as np
import string
import re
import os
from django.conf import settings
# Create your views here.
def home (request):
    return render(request,"inputdataset.html")
def result(request):
    if request.method=="POST":
        dict={"done":False,
        "message":"Une erreur s'est produite "}
        file=request.FILES["document"]
        print(file.name)
        if(".xlsx" in file.name):
            print(file.name)
            data=pd.read_excel(file,header=None,names=["Comment", "Sentiment"])
            data['Comment'] = data['Comment'].apply(lower_case)
            data['Comment'] = data['Comment'].apply(remove_links)
            data['Comment'] = data['Comment'].apply(clean_diacritics)
            data['Comment'] = data['Comment'].apply(preprocess)
            for com in range(len(data['Comment'])):
                S2 = data['Comment'][com]
                S2 = list(S2.rstrip())
                S2 = removeDuplicates(S2)
                S3 = "".join(S2)
                data['Comment'][com]=S3
            with open("dfcleaning/Sw/StopWords.txt", "r", encoding="utf8") as f:
                mylist = f.read().splitlines() 
            if(request.POST.get("stopwords")!=""):
                l=request.POST.get("stopwords").split(";")
                for elem in l :
                    mylist.append(elem)
                mylist = list(dict.fromkeys(mylist))
            data['Comment'] = data['Comment'].str.split(' ').apply(lambda x: ' '.join(k for k in x if k not in mylist))
            uniqueValues = data['Sentiment'].unique()
            data['Sentiment'] = data['Sentiment'].factorize()[0]
            data.to_excel("media/clean_data.xlsx")
            dict={
                "done":True,
                "message":"Done",
                "path":os.path.join(settings.BASE_DIR,'media/clean_data.xlsx')
            }
    return render(request,"CleanResult.html",dict)
def download(request):
    file_path = os.path.join(settings.BASE_DIR, 'media/clean_data.xlsx')
    if os.path.exists(file_path):
        with open(file_path, 'rb') as fh:
            response = HttpResponse(fh.read(), content_type="application/vnd.ms-excel")
            response['Content-Disposition'] = 'inline; filename=' + os.path.basename(file_path)
            return response
    raise Http404
###############################################Functions####################################
def lower_case (text):
    text = text.lower()
    return text
def remove_links (text):
    text = re.sub(r'http\S+', '', text)
    return text
def clean_diacritics (text):
    arabic_diacritics = re.compile("""
                             ّ    | # Shadda
                             َ    | # Fatha
                             ً    | # Tanwin Fath
                             ُ    | # Damma
                             ٌ    | # Tanwin Damm
                             ِ    | # Kasra
                             ٍ    | # Tanwin Kasr
                             ْ    | # Sukun
                             ـ     # Tatwil/Kashida
                         """, re.VERBOSE)
    text = re.sub(arabic_diacritics, '', text)
    return text
def clean_text(text):
    text = re.sub('[^\w]+|_', ' ', text, flags=re.U)
    text = re.sub('x005F', '', text)
    text = re.sub('x005D', '', text)
    text = re.sub('x000D', '', text)
    return text
def remove_emoji(text):
    regrex_pattern = re.compile(pattern = "["
        u"\U0001F600-\U0001F64F"  # emoticons
        u"\U0001F300-\U0001F5FF"  # symbols & pictographs
        u"\U0001F680-\U0001F6FF"  # transport & map symbols
        u"\U0001F1E0-\U0001F1FF"  # flags (iOS)
                           "]+", flags = re.UNICODE)
    return regrex_pattern.sub(r' ',text)

def clean_text(text):
    text = re.sub('[^\w]+|_', ' ', text, flags=re.U)
    text = remove_emoji(text)
    return text

def preprocess(text):
    
    text = clean_text(text)
    text=remove_emoji(text)

    text = re.sub("[إأآا]", "ا", text)
    text = re.sub("ى", "ي", text)
    text = re.sub("ؤ", "ء", text)
    text = re.sub("ئ", "ء", text)
    text = re.sub("ة", "ه", text)
    text = re.sub("گ", "ك", text)

    return text
def removeDuplicates(S):
    n = len(S)
    if (n < 2) :
        return 
    j = 0
    for i in range(n):
        if (S[j] != S[i]):
            j += 1
            S[j] = S[i]
    j += 1
    S = S[:j]
    return S