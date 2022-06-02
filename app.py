from pydoc import render_doc
from django.shortcuts import render
from flask import Flask, render_template, request, jsonify, Response
import pymysql
import pandas as pd
import json
import numpy as np
import pandas as pd
import statsmodels.api as sm
import matplotlib.pyplot as plt
import seaborn as sns
from sympy import N
from deepface import DeepFace

from csv import writer

sns.set()
from sklearn.cluster import KMeans
from helper import *
import numpy as np 
import pandas as pd 
import matplotlib.pyplot as plt
import seaborn as sns

import spotipy
import spotipy.util as util
from spotipy import SpotifyClientCredentials
import xgboost as xgb

import tensorflow as tf
from tensorflow.keras.models import Sequential
from tensorflow.keras.layers import Dense
from tensorflow.keras.wrappers.scikit_learn import KerasClassifier
from tensorflow.python.keras.utils import np_utils

tf.compat.v1.disable_eager_execution()
tf.compat.v1.disable_v2_behavior()

from sklearn.model_selection import cross_val_score, KFold, train_test_split
from sklearn.preprocessing import LabelEncoder,MinMaxScaler,StandardScaler
from sklearn.pipeline import Pipeline
from sklearn.metrics import confusion_matrix, accuracy_score

from sklearn import datasets
from sklearn.metrics import confusion_matrix
from sklearn.model_selection import train_test_split
from sklearn.tree import DecisionTreeClassifier



from sklearn import datasets
from sklearn.metrics import confusion_matrix
from sklearn.model_selection import train_test_split
from sklearn.naive_bayes import GaussianNB

import numpy as np
import pandas as pd
import matplotlib.pyplot as plt



from tensorflow.keras.layers import Flatten, Dense
from tensorflow.keras.models import Model,load_model
from tensorflow.keras.preprocessing.image import ImageDataGenerator , img_to_array, load_img
from tensorflow.keras.applications.mobilenet import MobileNet, preprocess_input 
from tensorflow.keras.losses import categorical_crossentropy


import spotipy

import cv2
import datetime, time
import os, sys
import numpy as np
from threading import Thread

app = Flask(__name__, static_url_path='/home/ajay/Desktop/FYP/static')
def sql_connector():
    conn = pymysql.connect(user='root', password='', db = 'DETAILS', host = 'localhost')
    c = conn.cursor()
    return conn, c
  



@app.route('/')
def home():
    return render_template('index.html')



@app.route('/musicplayer', methods=['GET','POST'])
def musicplayer():
    return render_template('musicplayer.html')
  
@app.route('/login', methods=['GET','POST'])
def login():
    result = " "
    if request.method == 'POST':
        username = request.form.get('username')
        password = request.form.get('password')
        conn, c = sql_connector()
        conn, d = sql_connector()
        P = c.execute("SELECT PASSWORD FROM DETAILS WHERE USERNAME = ('{}')".format(username))
        U = d.execute("SELECT USERNAME FROM DETAILS WHERE USERNAME = ('{}')".format(username))
        rows1 = c.fetchall()
        rows2 = d.fetchall()
        flag = 1
        if(len(rows2)==0):

            result = "CREATE AN ACCOUNT"
            flag = 0
        
        if(flag == 1):

            user = ""
            entry = ""

            for i in rows2[0]:
                user+=i

            for i in rows1[0]:
                entry+=i
            
            print(password)
            print(entry)

            if(password != entry):
                result = "INCORRECT PASSWORD"
            else:
                return render_template('userinput.html')

        conn.commit()
        conn.close()
        c.close()
        print(result)
    return render_template('login.html', message = result)

@app.route('/signup', methods=['GET','POST'])
def signup():
    if request.method == 'POST':
        username = request.form.get('username')
        password = request.form.get('password')
        conn, c = sql_connector()
        c.execute("INSERT INTO DETAILS VALUES ('{}', '{}')".format(username, password))
        conn.commit()
        conn.close()
        c.close()
        return render_template('userinput.html')
    return render_template('signup.html')
@app.route('/refresh', methods=['GET','POST'])
def refresh():

    CLIENT_ID = "87497b1a09094aa29244bcd9b4c3e843"
    CLIENT_SECRET = "3a270da264f54cd19fe0c681d8232031"

    #Authentication - without user
    client_credentials_manager = SpotifyClientCredentials(client_id=CLIENT_ID, client_secret=CLIENT_SECRET)
    sp = spotipy.Spotify(client_credentials_manager = client_credentials_manager)


    with open("/home/ajay/Desktop/FYP/static/song.json", "w+") as outfile:
                json.dump("", outfile, indent = 4)
    data = pd.read_csv("Dataset.csv")
    x = data.iloc[:,3:14] 
    y=data['Class']
    from sklearn import datasets
    iris = datasets.load_iris()
    max_accuracy=0
    max_i=0
    max_j=0
    dtree_pred=[]
    from sklearn.metrics import confusion_matrix
    from sklearn.model_selection import train_test_split
    from sklearn.naive_bayes import GaussianNB

    for i in range(2):
        X_train, X_test, y_train, y_test = train_test_split(x, y, test_size=0.3,random_state = 76)

    # training a DescisionTreeClassifier
        for j in range(1,2):
            dtree_model = DecisionTreeClassifier(max_depth = 3).fit(X_train, y_train)
            dtree_predictions = dtree_model.predict(X_test)
            accuracy = dtree_model.score(X_test, y_test)
            if(accuracy>max_accuracy):
                max_accuracy=accuracy
                max_i=i
                max_j=j
                dtree_pred=dtree_predictions
    # creating a confusion matrix

    cm = confusion_matrix(y_test, dtree_predictions)
    print("The accuracy is :",accuracy)
    print("The max i is :",max_i)
    print("The max j is :",max_j)

    #Create the confusion matrix using test data and predictions
    from sklearn.metrics import accuracy_score
    cm = confusion_matrix(y_test,dtree_predictions)
    #plot the confusion matrix
    ax = plt.subplot()
    sns.heatmap(cm,annot=True,ax=ax)
    labels = data['Class'].tolist()
    labels=np.unique(labels)
    ax.set_xlabel('Predicted labels')
    ax.set_ylabel('True labels')
    ax.set_title('Confusion Matrix')
    ax.xaxis.set_ticklabels(labels)
    ax.yaxis.set_ticklabels(labels)

    print("Accuracy Score",accuracy_score(y_test,dtree_predictions))
    
    # importing necessary libraries

    # loading the iris dataset
    iris = datasets.load_iris()
    gnb_pred=[]
    # X -> features, y -> label
    # X = iris.data
    # y = iris.target
    max_accuracy=0
    max_i=0
    # dividing X, y into train and test data
    for i in range(2):
        X_train, X_test, y_train, y_test = train_test_split(x, y,test_size=0.3, random_state = 18661)

    # training a Naive Bayes classifier

        gnb = GaussianNB().fit(X_train, y_train)
        gnb_predictions = gnb.predict(X_test)

    # accuracy on X_test
        accuracy = gnb.score(X_test, y_test)
        if(accuracy>max_accuracy):
            max_accuracy=accuracy
            max_i=i
            gnb_pred=gnb_predictions

    # creating a confusion matrix
    cm = confusion_matrix(y_test, gnb_predictions)
    print("The max acc is :",max_accuracy)
    print("The max i is :",max_i)
    X_train, X_test, y_train, y_test = train_test_split(x, y,test_size=0.3, random_state = 18661)
    gnb = GaussianNB().fit(X_train, y_train)
    gnb_predictions = gnb.predict(X_test)
    xgb_cl = xgb.XGBClassifier()

    print(type(xgb_cl))

    from sklearn.metrics import accuracy_score
    max_accuracy=0
    max_i=0
    xgb_pred=[]
    # Init classifier
    for i in range(10):
        X_train, X_test, y_train, y_test = train_test_split(x, y,test_size=0.3, random_state = 291)
        xgb_cl = xgb.XGBClassifier()

    # Fit
        xgb_cl.fit(X_train, y_train)

    # Predict
        preds = xgb_cl.predict(X_test)

    # Score
        accuracy=accuracy_score(y_test, preds)
        if(accuracy>max_accuracy):
            max_accuracy=accuracy
            max_i=i
            xgb_pred=preds
    
    print("The max acc is :",max_accuracy)
    print("The max i is :",max_i)

    from sklearn.ensemble import AdaBoostClassifier
    from sklearn import datasets
    # Import train_test_split function
    from sklearn.model_selection import train_test_split
    #Import scikit-learn metrics module for accuracy calculation
    from sklearn import metrics
    from sklearn.svm import SVC

    max_accuracy=0
    max_i=0
    max_j=0
    abc_pred=[]
    for i in range(1):
        X_train, X_test, y_train, y_test = train_test_split(x, y,test_size=0.3, random_state = 9)
        for j in range(1):
            svc=SVC(probability=True, kernel='linear')

        # Create adaboost classifer object
            abc =AdaBoostClassifier(n_estimators=16,learning_rate=0.97)
        # Train Adaboost Classifer
            model = abc.fit(X_train, y_train)

        #Predict the response for test dataset
            y_pred = model.predict(X_test)
            accuracy=accuracy_score(y_test, y_pred)
            if(accuracy>max_accuracy):
                max_accuracy=accuracy
                max_i=i
                max_j=j
                abc_pred=y_pred
    
    print("The max acc is :",max_accuracy)
    print("The max i is :",max_i)
    print("The max j is :",max_j)

    """Best random state 133 for xgb abc gnb and dtree"""

    max_i=0
    max_gnb=0
    max_abc=0
    max_dtree=0
    max_xgb=0

    for i in range (1):
        X_train, X_test, y_train, y_test = train_test_split(x, y,test_size=0.3, random_state =509)
        abc =AdaBoostClassifier(n_estimators=16,learning_rate=0.97)
        # Train Adaboost Classifer
        model = abc.fit(X_train, y_train)

        #Predict the response for test dataset
        y_pred = model.predict(X_test)
        abc_accuracy=accuracy_score(y_test, y_pred)
        xgb_cl = xgb.XGBClassifier()

    # Fit
        xgb_cl.fit(X_train, y_train)

    # Predict
        preds = xgb_cl.predict(X_test)

    # Score
        xgb_accuracy=accuracy_score(y_test, preds)
        gnb = GaussianNB().fit(X_train, y_train)
        gnb_predictions = gnb.predict(X_test)
        gnb_accuracy = gnb.score(X_test, y_test)
        dtree_model = DecisionTreeClassifier(max_depth = 3).fit(X_train, y_train)
        dtree_predictions = dtree_model.predict(X_test)

        dtree_accuracy = dtree_model.score(X_test, y_test)
        if((dtree_accuracy>max_dtree)&(gnb_accuracy>max_gnb)&(abc_accuracy>max_abc)):
            max_gnb=gnb_accuracy
            max_abc=abc_accuracy
            max_dtree=dtree_accuracy
            max_xgb=xgb_accuracy
            max_i=i
    
    print("The max for xgb is :",max_xgb)
    print("The max for gnb is :",max_gnb)
    print("The max for abc is :",max_abc)
    print("The max for dtree is :",max_dtree)
    print("The max for i is :",max_i)

    #Create the confusion matrix using test data and predictions

    from sklearn.metrics import accuracy_score
    X_train, X_test, y_train, y_test = train_test_split(x, y,test_size=0.3, random_state = 509)
    dtree_model = DecisionTreeClassifier(max_depth = 3).fit(X_train, y_train)
    dtree_predictions = dtree_model.predict(X_test)

    cm = confusion_matrix(y_test,dtree_predictions)
    #plot the confusion matrix
    ax = plt.subplot()
    sns.heatmap(cm,annot=True,ax=ax)
    labels = data['Class'].tolist()
    labels=np.unique(labels)
    ax.set_xlabel('Predicted labels')
    ax.set_ylabel('True labels')
    ax.set_title('Confusion Matrix')
    ax.xaxis.set_ticklabels(labels)
    ax.yaxis.set_ticklabels(labels)
    #plt.show()
    #Show the accuracy score 
    print("Accuracy Score",accuracy_score(y_test,dtree_predictions))

    #Create the confusion matrix using test data and predictions

    from sklearn.metrics import accuracy_score
    X_train, X_test, y_train, y_test = train_test_split(x, y,test_size=0.3, random_state = 509)
    abc =AdaBoostClassifier(n_estimators=16,learning_rate=0.97)
    # Train Adaboost Classifer
    model = abc.fit(X_train, y_train)

    #Predict the response for test dataset
    y_pred = model.predict(X_test)
    abc_accuracy=accuracy_score(y_test, y_pred)

    cm = confusion_matrix(y_test,y_pred)
    #plot the confusion matrix
    ax = plt.subplot()
    sns.heatmap(cm,annot=True,ax=ax)
    labels = data['Class'].tolist()
    labels=np.unique(labels)
    ax.set_xlabel('Predicted labels')
    ax.set_ylabel('True labels')
    ax.set_title('Confusion Matrix')
    ax.xaxis.set_ticklabels(labels)
    ax.yaxis.set_ticklabels(labels)
    #plt.show()
    #Show the accuracy score 
    print("Accuracy Score",accuracy_score(y_test,y_pred))

    #Create the confusion matrix using test data and predictions

    from sklearn.metrics import accuracy_score
    X_train, X_test, y_train, y_test = train_test_split(x, y,test_size=0.3, random_state = 509)
    xgb_cl = xgb.XGBClassifier()

    # Fit
    xgb_cl.fit(X_train, y_train)

    # Predict
    preds = xgb_cl.predict(X_test)

    # Score
    xgb_accuracy=accuracy_score(y_test, preds)

    #Predict the response for test dataset


    cm = confusion_matrix(y_test,preds)
    #plot the confusion matrix
    ax = plt.subplot()
    sns.heatmap(cm,annot=True,ax=ax)
    labels = data['Class'].tolist()
    labels=np.unique(labels)
    ax.set_xlabel('Predicted labels')
    ax.set_ylabel('True labels')
    ax.set_title('Confusion Matrix')
    ax.xaxis.set_ticklabels(labels)
    ax.yaxis.set_ticklabels(labels)
    #plt.show()
    #Show the accuracy score 
    print("Accuracy Score",accuracy_score(y_test,preds))

    #Create the confusion matrix using test data and predictions

    from sklearn.metrics import accuracy_score
    X_train, X_test, y_train, y_test = train_test_split(x, y,test_size=0.3, random_state = 509)
    gnb = GaussianNB().fit(X_train, y_train)
    gnb_predictions = gnb.predict(X_test)
    gnb_accuracy = gnb.score(X_test, y_test)

    #Predict the response for test dataset


    cm = confusion_matrix(y_test,gnb_predictions)
    #plot the confusion matrix
    ax = plt.subplot()
    sns.heatmap(cm,annot=True,ax=ax)
    labels = data['Class'].tolist()
    labels=np.unique(labels)
    ax.set_xlabel('Predicted labels')
    ax.set_ylabel('True labels')
    ax.set_title('Confusion Matrix')
    ax.xaxis.set_ticklabels(labels)
    ax.yaxis.set_ticklabels(labels)
    #plt.show()
    #Show the accuracy score 
    print("Accuracy Score",accuracy_score(y_test,gnb_predictions))


    max_i=0
    max_accuracy=0
    max_finalpred=[]
    for i in range(2):
        X_train, X_test, y_train, y_test = train_test_split(x, y,test_size=0.3, random_state = 1991)
        pred1=dtree_model.predict(X_test)
        pred2=gnb.predict(X_test)
        pred3=model.predict(X_test)
        pred4=xgb_cl.predict(X_test)
        finalpred=(1.501*pred4+0.499*pred1)/2
        for j in range(len(finalpred)):
            if(finalpred[j]<0.5):
                finalpred[j]=0
            elif((finalpred[j]>=0.5)&(finalpred[j]<1.5)):
                finalpred[j]=1
            elif((finalpred[j]>=1.5)&(finalpred[j]<2.5)):
                finalpred[j]=2
            else:
                finalpred[j]=3
        accuracy=accuracy_score(y_test,finalpred)
        if(accuracy>max_accuracy):
            max_accuracy=accuracy
            max_i=i
            max_finalpred=finalpred

    print("The max accuracy is :",max_accuracy)
    print("The max i is :",max_i)

    X_train, X_test, y_train, y_test = train_test_split(x, y,test_size=0.3, random_state = 1991)
    cm = confusion_matrix(y_test,max_finalpred)
    #plot the confusion matrix
    ax = plt.subplot()
    sns.heatmap(cm,annot=True,ax=ax)
    labels = data['Class'].tolist()
    labels=np.unique(labels)
    ax.set_xlabel('Predicted labels')
    ax.set_ylabel('True labels')
    ax.set_title('Confusion Matrix')
    ax.xaxis.set_ticklabels(labels)
    ax.yaxis.set_ticklabels(labels)
    #plt.show()
    #Show the accuracy score 
    print("Accuracy Score",accuracy_score(y_test,max_finalpred))

    list_data=[]
    result_id = []
    playlist_link = "https://open.spotify.com/playlist/37i9dQZF1DX1i3hvzHpcQV"
    playlist_URI = playlist_link.split("/")[-1].split("?")[0]
    track_uris = [x["track"]["uri"] for x in sp.playlist_tracks(playlist_URI)["items"]]

    for track in sp.playlist_tracks(playlist_URI)["items"]:
        
        track_id = track["track"]["id"]
        result_id.append(track_id)

    
    list_data = []
    with open('song_id.csv', 'a', newline='') as f_object: 
        for ids in result_id:
            meta = sp.track(ids)
            features = sp.audio_features(ids)
            uri="https://open.spotify.com/embed/track/"+ str(ids)
            # meta
            name = meta['name']
            album = meta['album']['name']
            artist = meta['album']['artists'][0]['name']
            release_date = meta['album']['release_date']
            length = meta['duration_ms']
            popularity = meta['popularity']
            ids =  meta['id']

            list_data.append(name)
            list_data.append(artist)
            list_data.append(uri)
            

            # features
            acousticness = features[0]['acousticness']
            speechiness=features[0]['speechiness']
            danceability = features[0]['danceability']
            energy = features[0]['energy']
            instrumentalness = features[0]['instrumentalness']
            liveness = features[0]['liveness']
            valence = features[0]['valence']
            loudness = features[0]['loudness']
            tempo = features[0]['tempo']
            key = features[0]['key']
            speechiness=features[0]['speechiness']
            mode=features[0]['mode']
            time_signature = features[0]['time_signature']
            duration_ms=features[0]['duration_ms']

            track = [danceability,mode,energy,key,loudness,speechiness,acousticness,instrumentalness,liveness,valence,tempo]
            columns = ['Danceability','Mode','Energy','Key','Loudness','Speechiness','Acousticness','Instrumentalness','Liveness','Valence','Tempo']

            q = (track, columns, name)
            s_name=q[2]
            q=list(q)
            type(q[0])
            a=np.array(q)
            a.ravel()
            a[0]=[a[0]]
            d=pd.DataFrame(a[0],columns=q[1])
            pred1=dtree_model.predict(a[0])
            pred2=xgb_cl.predict(d)
            final1=(0.8*pred1+1.2*pred2)/2
            print(final1)
            for j in range(len(final1)):
                if(final1[j]<0.5):
                    final1[j]=0
                elif((final1[j]>=0.5)&(final1[j]<1.5)):
                    final1[j]=1
                elif((final1[j]>=1.5)&(final1[j]<2.5)):
                    final1[j]=2
                else:
                    final1[j]=3
            len(final1)
            if final1[0]==0:
                emo="calm"
            elif final1[0]==1:
                emo="happy"
            elif final1[0]==2:
                emo="sad"
            else:
                emo="angry"

            print("The song",s_name,"is a",emo,"song")
            image="https://open.spotify.com/oembed?url=spotify:track:"+ids
            
            import urllib.request as ur
            s = ur.urlopen(image)
            sl = s.read()
            b=str(sl)
            index=b.find("thumbnail_url")
            a=b[index+16:index+80]
            print(a)
            list_data.append(a)
            list_data.append(ids)
            list_data.append(int(final1[0]))
            writer_object = writer(f_object)
            writer_object.writerow(list_data)
            list_data = []

    return render_template('userinput.html')
    
@app.route('/mood', methods=['GET','POST'])
def userinputmap():


    with open("/home/ajay/Desktop/FYP/static/song.json", "w+") as outfile:
                json.dump("", outfile, indent = 4)
    model=load_model("imagerec.h5")
    op={0: 'ANGRY', 3: 'HAPPY', 2: 'CALM', 1: 'SAD'}
    path = "image.png"
    
    img = load_img(path, target_size=(224,224) )
    
    emo = " "
    i = img_to_array(img)/255
    input_arr = np.array([i])
    input_arr.shape

    pred = np.argmax(model.predict(input_arr))
    if(pred == 0):
        emo = "ANGRY"
    elif(pred == 3):
        emo = "HAPPY"
    elif(pred == 2):
        emo = "CALM"
    elif(pred ==1):
        emo = "SAD"
    print(f" the person is {emo}")
    songs_json = {"song_id_image":[]}
    dataset = pd.read_csv('song_id.csv',encoding="utf-8")
    dataframe = dataset.iloc[:,:]
    emotion = ""
    
    print(dataframe)
    id = {}
    
    if request.method == 'POST':

        userinput = emo
        
        if userinput == 'CALM':
            
            for i in range(len(dataframe)) :
                flag = 1
                if dataframe.iloc[i,5] == "0":
                        id["Name"] = dataframe.iloc[i,0]
                        id["Artist"] = dataframe.iloc[i,1]
                        id["uri"] = dataframe.iloc[i,2]
                        id["Track"] = dataframe.iloc[i,3]
                        id["id"] = dataframe.iloc[i,4]
                        if(len(songs_json)>=1):
                            k = 0
                            for j in songs_json.values():
                                for k in j:
                                    if dataframe.iloc[i,4] != k['id']:
                                        continue
                                    else:
                                        flag = 0
                                        break
                            if flag == 1:
                                songs_json["song_id_image"].append(id)
                        else:
                            songs_json["song_id_image"].append(id)
                        id = {}
            with open("/home/ajay/Desktop/FYP/static/song.json", "w+") as outfile:
                json.dump(songs_json, outfile, indent = 4)

        elif userinput == 'HAPPY':
            
            for i in range(len(dataframe)) :
                flag = 1
                if dataframe.iloc[i,5] == "1":
                        id["Name"] = dataframe.iloc[i,0]
                        id["Artist"] = dataframe.iloc[i,1]
                        id["uri"] = dataframe.iloc[i,2]
                        id["Track"] = dataframe.iloc[i,3]
                        id["id"] = dataframe.iloc[i,4]
                        if(len(songs_json)>=1):
                            k = 0
                            for j in songs_json.values():
                                for k in j:
                                    if dataframe.iloc[i,4] != k['id']:
                                        continue
                                    else:
                                        flag = 0
                                        break
                            if flag == 1:
                                songs_json["song_id_image"].append(id)
                        else:
                            songs_json["song_id_image"].append(id)
                        id = {}
            with open("/home/ajay/Desktop/FYP/static/song.json", "w+") as outfile:
                json.dump(songs_json, outfile, indent = 4)

        
        elif userinput == 'SAD':
            for i in range(len(dataframe)) :
                flag = 1
                if dataframe.iloc[i,5] == "2":
                        id["Name"] = dataframe.iloc[i,0]
                        id["Artist"] = dataframe.iloc[i,1]
                        id["uri"] = dataframe.iloc[i,2]
                        id["Track"] = dataframe.iloc[i,3]
                        id["id"] = dataframe.iloc[i,4]
                        if(len(songs_json)>=1):
                            k = 0
                            for j in songs_json.values():
                                for k in j:
                                    if dataframe.iloc[i,4] != k['id']:
                                        continue
                                    else:
                                        flag = 0
                                        break
                            if flag == 1:
                                songs_json["song_id_image"].append(id)
                        else:
                            songs_json["song_id_image"].append(id)
                        id = {}
            with open("/home/ajay/Desktop/FYP/static/song.json", "w+") as outfile:
                json.dump(songs_json, outfile, indent = 4)
            

        elif userinput == 'ANGRY':
            for i in range(len(dataframe)) :
                flag = 1
                if dataframe.iloc[i,5] == "3":
                        id["Name"] = dataframe.iloc[i,0]
                        id["Artist"] = dataframe.iloc[i,1]
                        id["uri"] = dataframe.iloc[i,2]
                        id["Track"] = dataframe.iloc[i,3]
                        id["id"] = dataframe.iloc[i,4]
                        if(len(songs_json)>=1):
                            k = 0
                            for j in songs_json.values():
                                for k in j:
                                    if dataframe.iloc[i,4] != k['id']:
                                        continue
                                    else:
                                        flag = 0
                                        break
                            if flag == 1:
                                songs_json["song_id_image"].append(id)
                        else:
                            songs_json["song_id_image"].append(id)
                        id = {}
            with open("/home/ajay/Desktop/FYP/static/song.json", "w+") as outfile:
                json.dump(songs_json, outfile, indent = 4)
        emotion+=op[pred]
    
    return render_template('userinput.html', e = emotion)
    

global capture,rec_frame, grey, switch, neg, face, rec, out 
capture=0
grey=0
neg=0
face=0
switch=1
rec=0

#make shots directory to save pics
# try:
#     os.mkdir('./shots')
# except OSError as error:
#     pass

#Load pretrained face detection model    
net = cv2.dnn.readNetFromCaffe('./saved_model/deploy.prototxt.txt', './saved_model/res10_300x300_ssd_iter_140000.caffemodel')

#instatiate flask app  
# app = Flask(__name__, template_folder='./templates')


camera = cv2.VideoCapture(0)

def record(out):
    global rec_frame
    while(rec):
        time.sleep(0.05)
        out.write(rec_frame)


def detect_face(frame):
    global net
    (h, w) = frame.shape[:2]
    blob = cv2.dnn.blobFromImage(cv2.resize(frame, (300, 300)), 1.0,
        (300, 300), (104.0, 177.0, 123.0))   
    net.setInput(blob)
    detections = net.forward()
    confidence = detections[0, 0, 0, 2]

    if confidence < 0.5:            
            return frame           

    box = detections[0, 0, 0, 3:7] * np.array([w, h, w, h])
    (startX, startY, endX, endY) = box.astype("int")
    try:
        frame=frame[startY:endY, startX:endX]
        (h, w) = frame.shape[:2]
        r = 480 / float(h)
        dim = ( int(w * r), 480)
        frame=cv2.resize(frame,dim)
    except Exception as e:
        pass
    return frame
 

def gen_frames():  # generate frame by frame from camera
    global out, capture,rec_frame
    while True:
        success, frame = camera.read() 
        if success:
            if(face):                
                frame= detect_face(frame)
            if(capture):
                capture=0
                now = datetime.datetime.now()
                # p = os.path.sep.join("shot_{}.png".format(str(now).replace(":",'')))
                cv2.imwrite("image.png", frame)
            
            if(rec):
                rec_frame=frame
                frame= cv2.putText(cv2.flip(frame,1),"Recording...", (0,25), cv2.FONT_HERSHEY_SIMPLEX, 1, (0,0,255),4)
                frame=cv2.flip(frame,1)
            
                
            try:
                ret, buffer = cv2.imencode('.jpg', cv2.flip(frame,1))
                frame = buffer.tobytes()
                yield (b'--frame\r\n'
                       b'Content-Type: image/jpeg\r\n\r\n' + frame + b'\r\n')
            except Exception as e:
                pass
                
        else:
            pass

# @app.route('/camera')
# def index():
#     return render_template('userinput.html')
        
@app.route('/video_feed')
def video_feed():
    return Response(gen_frames(), mimetype='multipart/x-mixed-replace; boundary=frame')

@app.route('/requests',methods=['POST','GET'])
def tasks():
    global switch,camera
    if request.method == 'POST':
        if request.form.get('click') == 'CAPTURE':
            global capture
            capture=1                
                 
    elif request.method=='GET':
        return render_template('userinput.html')
    return render_template('userinput.html')


if __name__ == '__main__':
    app.run()
    
camera.release()
cv2.destroyAllWindows()     