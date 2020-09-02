from flask import Flask, render_template, request, send_file, jsonify
import pyrebase
from collections import OrderedDict
import os
import keyboard as key
from flask_moment import Moment
from plysslingen import Plyssningen

config = {
    "apiKey": "AIzaSyC3Jx94GLlQlmMd36cFYonw2MrfTXf4YPE",
    "authDomain": "poddsok.firebaseapp.com",
    "databaseURL": "https://poddsok.firebaseio.com",
    "projectId": "poddsok",
    "storageBucket": "poddsok.appspot.com",
    "messagingSenderId": "621533942583",
    "appId": "1:621533942583:web:f4b8822a1fdb41470e00b2",
    "measurementId": "G-L7RKMPYTB6"
}

app = Flask(__name__)
moment = Moment(app)

podcasts = []

def getPodcasts():
    if len(podcasts) == 0:
        firebase = pyrebase.initialize_app(config)
        db = firebase.database()
        data = db.child().get()
        values = data.val()
        for key in values:  
            podcasts.append( { 'title': key, 'episodes':values[key] } )
    return podcasts  

@app.route('/')
def index():
    podcasts = getPodcasts()
    episodes = None
    return render_template('main.html', data = { 'podcasts': podcasts, 'episodes': None})

@app.route('/handle_podcast', methods=['POST'])
def handle_podcast():
    podcasts = getPodcasts()
    podcasts.sort(key=lambda x: x['title'])
    pod = request.form['pod']
    i = 0
    while i < len(podcasts):
        if(pod == podcasts[i]['title']):
            podcast = podcasts[i]
            del podcasts[i]
            podcasts.insert(0, podcast)
        i += 1
    episodes = podcast['episodes']
    return render_template('main.html', data = { 'podcasts': podcasts, 'episodes': episodes})

@app.route('/handle_episode', methods=['POST'])
def handle_episode():
    podcasts = getPodcasts()
    episodes = podcasts[0]['episodes']
    episode = request.form['episode']
    i = 0
    for ep in episodes:
        if episodes[ep]['name'].strip() == episode:
            chosenEp = episodes[ep]
            firstEp = episodes['ep1']
            del episodes[ep]
            episodes['ep1'] = chosenEp
            episodes[ep] = firstEp
            break
    return render_template('main.html', data = { 'podcasts': podcasts, 'podcast': podcasts[0]['title'], 'episodes': episodes, 'episode': episode })

@app.route('/to_recording', methods=['POST'])
def to_recording():
    episode = request.args.get('episode').replace(' ','_')
    podcast = request.args.get('podcast').replace(' ','_')
    time = getTime()
    recordInstance = Plyssningen( podcast, episode, time )
    recordInstance.writeInfo()
    return render_template('recording.html', data = { 'podcast':podcast, 'episode':episode })

@app.route('/download/<path:filename>.txt')
def download(filename):
    return send_file('test_res.txt', attachment_filename='')

timeCount=[0,0,0,0]
def getTime():
    if timeCount[3] == 9:
        timeCount[2] += 1
        timeCount[3] = 0
    else:
        timeCount[3] += 1
    if timeCount[2] == 6:
        timeCount[1] += 1
        timeCount[2] = 0
    if timeCount[1] == 6:
        timeCount[0] += 1
        timeCount[1] = 0
    return timeCount

@app.route('/time')
def time():
    time = getTime()
    timeString = str(time[0])+str(time[1])+':'+str(time[2])+str(time[3])
    return jsonify(timeString)
