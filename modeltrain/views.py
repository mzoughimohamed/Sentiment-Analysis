from django.shortcuts import render , HttpResponse
import pandas as pd
import numpy as np
from sklearn.model_selection import train_test_split, GridSearchCV
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.pipeline import make_pipeline
from sklearn.linear_model import LogisticRegression
from sklearn.ensemble import RandomForestClassifier
from sklearn.naive_bayes import MultinomialNB
from sklearn.svm import SVC
from sklearn.metrics import confusion_matrix, accuracy_score, f1_score,recall_score,precision_score,precision_recall_fscore_support
from sklearn.neighbors import KNeighborsClassifier
from sklearn.tree import DecisionTreeClassifier
from sklearn.linear_model import SGDClassifier
from sklearn.svm import LinearSVC
from sklearn.naive_bayes import MultinomialNB, BernoulliNB
from sklearn.pipeline import Pipeline
from django.http import JsonResponse
import joblib
import os
import zipfile
from django.conf import settings
# Create your views here.
def index(request):
    return render(request,"train.html")
def trainmetrics(request):
    error=True
    message="Votre fichier doit être de format xlsx"
    precision=[]
    data=[]
    recall=[]
    recall_w=[]
    precall=[]
    pf1=[]
    accurancy=[]
    labels=["LinearSVC","SVC","MultinomialNB","LogisticRegression","BernoulliNB","SGDClassifier","DecisionTreeClassifier","RandomForestClassifier","KNeighborsClassifier",]
    if request.method=="POST":
        file=request.FILES["document"]
        if(".xlsx" in file.name):
            data=pd.read_excel(file)
            feature = data.Comment
            target = data.Sentiment
            X_train, X_test, Y_train, Y_test = train_test_split(feature, target, test_size =.2, random_state=100)
            classifiers = [LinearSVC(),SVC(),MultinomialNB(),LogisticRegression(solver='liblinear',max_iter=10000),BernoulliNB(), SGDClassifier(), 
               DecisionTreeClassifier(max_depth=5),
               RandomForestClassifier(max_depth=5, n_estimators=10, max_features=1),
               KNeighborsClassifier(3)
               ]
            data=[]
            pf1=[]
            precision=[]
            precision_w=[]
            recall=[]
            recall_w=[]
            precall=[]
            f1=[]
            f1_w=[]
            accurancy=[]
            for g in (1,2,3):
                results=[]      
                i=0

                for alg in classifiers:
                    pipeline = Pipeline([
                                    ('vect', TfidfVectorizer(min_df=0.0001, max_df=0.95,
                                    analyzer='word', lowercase=False,
                                    ngram_range=(1, g))),
                                    ('clf', alg), ])
                    pipeline.fit(X_train.values.astype('U'), Y_train.values.astype('U'))
                    feature_names = pipeline.named_steps['vect'].get_feature_names()
                    prediction = pipeline.predict(X_test.values.astype("U"))
                    joblib.dump(pipeline,"media/models/"+labels[i]+str(g)+"gram"+".sav")
                    results.append(accuracy_score(Y_test.values.astype("U"), prediction.astype("U")))
                    if g==1:
                        precision.append(precision_score(Y_test.values.astype("U").astype("U"), prediction.astype("U"),average='macro'))
                        precision_w.append(precision_score(Y_test.values.astype("U").astype("U"), prediction.astype("U"),average='weighted'))
                        recall.append(recall_score(Y_test.values.astype("U"), prediction.astype("U"),average='macro'))
                        recall_w.append(recall_score(Y_test.values.astype("U"), prediction.astype("U"),average='weighted'))
                        f1.append(f1_score(Y_test.values.astype("U"), prediction.astype("U"),average='macro'))
                        f1_w.append(f1_score(Y_test.values.astype("U"), prediction.astype("U"),average='weighted'))
                        
                    i+=1
                if g==1:
                    precall.append(recall)
                    precall.append(recall_w)
                    data.append(precision)
                    data.append(precision_w)
                    pf1.append(f1)
                    pf1.append(f1_w)
                accurancy.append(results)
            error=False 
            message=""
    return render(request,"Trainresult.html",{
        "labels":labels,
        "data":accurancy,
        "precision":data,
        "recall":precall,
        "f1":pf1,
        "error":error,
        "message":message,
        })
def filedownload(request):
    labels=["LinearSVC","SVC","MultinomialNB","LogisticRegression","BernoulliNB","SGDClassifier","DecisionTreeClassifier","RandomForestClassifier","KNeighborsClassifier",]
    zf=zipfile.ZipFile('media/download.zip', 'w')
    for g in(1,2,3):
        for label in labels:
            zf.write("media/models/"+label+str(g)+"gram.sav")
    zf.close()
    zfr=open("media/download.zip",'rb')
    response = HttpResponse(zfr, content_type='application/force-download')
    response['Content-Disposition'] = 'attachment; filename="download.zip"' 
    return response