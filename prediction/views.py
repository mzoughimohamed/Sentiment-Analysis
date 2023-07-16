from django.shortcuts import render
from django.http import JsonResponse
import joblib
import os
import re
from django.conf import settings

# Create your views here.
def index(request):
    return render(request,"predict.html")
def response(request):
    emotion=""
    Comment=""
    if request.method=="POST":
        result=[]
        emo=[]
        SGD=joblib.load(os.path.join(settings.BASE_DIR,'prediction/Models/SGDClassifier1gram.sav'))
        SVC=joblib.load(os.path.join(settings.BASE_DIR,'prediction/Models/MultinomialNB3gram.sav'))
        LR=joblib.load(os.path.join(settings.BASE_DIR,'prediction/Models/LogisticRegression1gram.sav'))
        KNC=joblib.load(os.path.join(settings.BASE_DIR,'prediction/Models/LinearSVC1gram.sav'))
        Comment=request.POST.get("comment")
        Clean_Comment=lower_case(Comment)
        Clean_Comment=clean_diacritics(Clean_Comment)
        Clean_Comment=remove_links(Clean_Comment)
        Clean_Comment=preprocess(Clean_Comment)
        Clean_Comment=re.sub(r'(\w)\1{2,}',r'\1',Clean_Comment)
        result.append(SGD.predict([Clean_Comment]))
        result.append(SVC.predict([Clean_Comment]))
        result.append(LR.predict([Clean_Comment]))
        result.append(KNC.predict([Clean_Comment]))
        
        for item in result :
            if item=="0":
                emo.append("Sad")
            if item=="1":
                emo.append("Angry")
            if item=="2":
                emo.append("Happy")
            if item=="3":
                emo.append("Neutral")
    return render(request,"predict.html",{
        "etat":True,
        "emotion":"emotion",
        "Comment":Comment,
        "emo":emo,
            })
    ####################################function for cleaning##################################s
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