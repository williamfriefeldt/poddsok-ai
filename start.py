''' 
Imports:
- Flask: Framework to use Python in browser
- Pyrebase: Lib to call Firebase (database) in Python
- Collections: OrderedDict, data type from FB
- FlaskMoment: Display date and time
- Plyssningen: Speech recognition class, see plyssningen.py
- Threading: To start Plyssningen while giving status to html
'''
from flask import Flask, render_template, request, send_file, jsonify
import pyrebase
from collections import OrderedDict
from flask_moment import Moment
from plysslingen import Plyssningen
import threading

#Setup for Firebase
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

#Initialize app and Plysslingen
app = Flask(__name__)
moment = Moment(app)
recordInstance = Plyssningen()

#Get podcasts form FB
podcasts = []
def getPodcasts():
    if len( podcasts ) == 0:
        firebase = pyrebase.initialize_app( config )
        db = firebase.database()
        data = db.child().get()
        values = data.val()
        for key in values:  
            title = values[key]['info']['name']
            del values[key]['info']
            podcasts.append( { 'title': title, 'episodes': values[key] } )
    return podcasts  

#Redirect user to main view and fetch podcasts
@app.route('/')
def index():
    podcasts = getPodcasts()
    episodes = None
    return render_template('main.html', data = { 
        'podcasts': podcasts, 
        'episodes': None, 
        'infoText': 'Välj den podcast som ska transkriberas' 
    })

#When podcasts choosen => display episodes
@app.route( '/handle_podcast', methods = [ 'POST' ] )
def handle_podcast():
    podcasts = getPodcasts()
    podcasts.sort( key = lambda x: x['title'])
    pod = request.form['pod']
    i = 0
    while i < len(podcasts):
        if pod == podcasts[i]['title']:
            podcast = podcasts[i]
            del podcasts[i]
            podcasts.insert( 0, podcast )
        i += 1
    episodes = podcast['episodes']
    return render_template( 'main.html', data = { 
        'podcasts': podcasts, 
        'episodes': episodes, 
        'infoText': 'Välj det avsnitt som ska transkriberas' 
    })

#When episodes choosen => display button for next view
@app.route( '/handle_episode', methods = ['POST'] )
def handle_episode():
    podcasts = getPodcasts()
    episodes = podcasts[0]['episodes']
    episode = request.form['episode']
    i = 0
    episode = episode.split('.')[1]
    for ep in episodes:
        if episodes[ep]['name'] == episode:
            chosenEp = episodes[ep]
            firstEp = episodes[0]
            del episodes[ep]
            episodes[0] = chosenEp
            episodes[ep] = firstEp
    return render_template( 'main.html', data = { 
        'podcasts': podcasts, 
        'podcast': podcasts[0]['title'], 
        'episodes': episodes, 'episode': episode, 
        'infoText': 'Öppna avsnittet i Spotify och fortsätt till inspelning' 
    })

#Redirect user to recording view and set file info for Plyssningen
resultList = []
@app.route( '/to_recording', methods = ['POST'] )
def to_recording():
    resultList = []
    episode = request.args.get( 'episode' ).replace( ' ', '_' )
    podcast = request.args.get( 'podcast' ).replace( ' ', '_' )
    recordInstance.setAttr( podcast, episode )
    recordInstance.writeInfo()
    return render_template( 'recording.html', data = { 'podcast': podcast, 'episode': episode })

#Save file to computer
@app.route( '/download/<path:filename>.txt' )
def download( filename ):
    return send_file( 'test_res.txt', attachment_filename = '' )

#Update current recording time
def getTime(): 
    timeCount = recordInstance.time
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
    recordInstance.time = timeCount
    return timeCount

#Handle recording state / update html on recording status
@app.route( '/time' )
def time():
    recordStatus = 'Spelar in...'
    recordMic = threading.Thread( target = recordInstance.startMicrophone, args = () )
    recordMic.start()
    return jsonify( { 'recordStatus': recordStatus } )

@app.route( '/checkResult' )
def checkResult():
    if recordInstance.audioRes == 'Analyserar ljud...':
        time = recordInstance.time
    else:
        time = getTime()
    timeString = str( time[0] ) + str( time[1] ) + ':' + str( time[2] ) + str( time[3] )
    return jsonify( { 
        'time': timeString, 
        'recordRes': recordInstance.audioRes, 
        'isListening': recordInstance.isListening 
    })

@app.route( '/saveResult' )
def saveResult():
    recordInstance.setTime()
    timeString = str( recordInstance.time[0] ) + str( recordInstance.time[1] ) + ':' + str( recordInstance.time[2] ) + str( recordInstance.time[3] )
    resultList.append( '[ ' + timeString + ', "' + recordInstance.audioRes + '"' )
    return jsonify( resultList )

      

