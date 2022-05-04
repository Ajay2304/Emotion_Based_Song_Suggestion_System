from pydoc import render_doc
from django.shortcuts import render
from flask import Flask, render_template, request, jsonify
import pymysql
import pandas as pd
import json

def sql_connector():
    conn = pymysql.connect(user='root', password='', db = 'DETAILS', host = 'localhost')
    c = conn.cursor()
    return conn, c
  
app = Flask(__name__)


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

@app.route('/mood', methods=['GET','POST'])
def userinputmap():

    songs_json = []
    dataset = pd.read_csv('song_id.csv',encoding="utf-8")
    dataframe = dataset.iloc[:,0:6]
    emotion = ""
    print(dataframe)
    id = {}
    if request.method == 'POST':

        userinput = request.form.get('usermood')
        

        
        if userinput == 'CALM':
            
            for i in range(len(dataframe)) :
                if dataframe.iloc[i,5] == "0":
                        # id["id"] = dataframe.iloc[i,4]
                        id["Name"] = dataframe.iloc[i,0]
                        #id["Artist"] = dataframe.iloc[i,1]
                        id["uri"] = dataframe.iloc[i,2]
                        id["Track"] = dataframe.iloc[i,3]
                        
                        songs_json.append(id)
                        id = {}

        elif userinput == 'HAPPY':
            
            for i in range(len(dataframe)) :
                if dataframe.iloc[i,5] == "1":
                    
                        # id["id"] = dataframe.iloc[i,4]
                        id["Name"] = dataframe.iloc[i,0]
                        #id["Artist"] = dataframe.iloc[i,1]
                        id["uri"] = dataframe.iloc[i,2]
                        id["Track"] = dataframe.iloc[i,3]
                        songs_json.append(id)
                        id = {}

            # with open('happy.json', 'w+', encoding='utf-8') as f:
            #     f.write(json.dumps(songs_json, indent = 4)) 
            
        
        elif userinput == 'SAD':
            for i in range(len(dataframe)) :
                if dataframe.iloc[i,5] == "2":
                    
                        # id["id"] = dataframe.iloc[i,4]
                        id["Name"] = dataframe.iloc[i,0]
                        #id["Artist"] = dataframe.iloc[i,1]
                        id["uri"] = dataframe.iloc[i,2]
                        id["Track"] = dataframe.iloc[i,3]
                        songs_json.append(id)
                        id = {}
            # with open('sad.json', 'w+', encoding='utf-8') as f:
            #     f.write(json.dumps(songs_json, indent = 4)) 

        elif userinput == 'ANGRY':
            for i in range(len(dataframe)) :
                if dataframe.iloc[i,5] == "3":
                    
                        # id["id"] = dataframe.iloc[i,4]
                        id["Name"] = dataframe.iloc[i,0]
                        #id["Artist"] = dataframe.iloc[i,1]
                        id["uri"] = dataframe.iloc[i,2]
                        id["Track"] = dataframe.iloc[i,3]
                        songs_json.append(id)
                        id = {}
            # with open('angry.json', 'w+', encoding='utf-8') as f:
            #     f.write(json.dumps(songs_json, indent = 4)) 
        emotion+=userinput
    return render_template('userinput.html',jsonfile = songs_json, e = emotion)
        



# main driver function
if __name__ == '__main__':
  
    app.run()