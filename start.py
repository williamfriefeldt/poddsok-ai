''' 
Imports:
- Flask: Framework to use Python in browser
- Pyrebase: Lib to call Firebase (database) in Python
- Collections: OrderedDict, data type from FB
- FlaskMoment: Display date and time
- Plyssningen: Speech recognition class, see plyssningen.py
- Threading: To start Plyssningen while giving status to html
'''
from flask import Flask, render_template, request, send_file, jsonify, redirect
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
app = Flask( __name__ )
moment = Moment( app )
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

chosenEps = []
def getEpisodes( nrOfEps, episode, nr ):
    if nrOfEps != None:
        chosenEps.clear()
        for i in range( int( nrOfEps ) ):
            chosenEps.append( None )
    else:
        chosenEps[nr] = episode
    return chosenEps

def chosenEpsSet():
    return chosenEps

#Redirect user to main view and fetch podcasts
@app.route('/')
def index():
    podcasts = getPodcasts()
    podcasts.sort( key = lambda x: x['title'] )
    episodes = None
    return render_template('main.html', data = { 
        'podcasts': podcasts, 
        'episodes': None,
        'nrOfEps': None,
        'infoText': 'Välj den podcast som ska transkriberas' 
    })

#When podcasts choosen => display episodes
@app.route( '/handle_podcast', methods = ['POST'] )
def handle_podcast():
    podcasts = getPodcasts()
    pod = request.form['pod']
    i = 0
    while i < len( podcasts ):
        if pod == podcasts[i]['title']:
            podcast = podcasts[i]
            del podcasts[i]
            podcasts.insert( 0, podcast )
        i += 1
    return render_template( 'main.html', data = { 
        'podcasts': podcasts, 
        'episodes': None, 
        'nrOfEps': 0,
        'infoText': 'Välj de avsnitt som ska transkriberas' 
    })

@app.route( '/handle_nrOfEps', methods = ['POST'] )
def handle_nrOfEps():
    podcasts = getPodcasts()
    nrOfEps = request.form['nrOfEps']
    episodes = list( podcasts[0]['episodes'].items() )
    episodes.sort( key = lambda x: x[1]['nr'] )
    episodes = dict( episodes )
    chosenEps = getEpisodes( nrOfEps, None, None )
    nrOfChosenEps = 0
    for ep in chosenEps:
        if ep != None:
            nrOfChosenEps += 1
    chosenEpsLength = len(chosenEps)
    return render_template( 'main.html', data = { 
        'podcasts': podcasts, 
        'episodes': episodes,
        'nrOfEps': int( nrOfEps ),
        'nrOfChosenEps': int( nrOfChosenEps ),
        'chosenEps': chosenEps,
        'chosenEpsLength': int( chosenEpsLength ),
        'infoText': 'Välj de avsnitt som ska transkriberas' 
    })

#When episodes choosen => display button for next view
@app.route( '/handle_episode', methods = ['POST'] )
def handle_episode():
    nrOfEps = request.args.get( 'nrOfEps' )
    nr = int( request.args.get( 'epNr' ) )
    podcasts = getPodcasts()
    episodes = podcasts[0]['episodes']
    episodeNr = int( request.form['episode'].split( '.' )[0] )
    i = 0
    listEpisodes = list( episodes.items() )
    for ep in listEpisodes:
        if ep[1]['nr'] == episodeNr:
            listEpisodes.remove(ep)
            listEpisodes.sort( key = lambda x: x[1]['nr'] )
            listEpisodes.insert(0, ep)
            chosenEps = getEpisodes( None, ep[1], nr )
            break
    episodes = dict(listEpisodes)
    nrOfChosenEps = 0
    for ep in chosenEps:
        if ep != None:
            nrOfChosenEps += 1
    chosenEpsLength = len(chosenEps)
    return render_template( 'main.html', data = { 
        'podcasts': podcasts, 
        'podcast': podcasts[0]['title'], 
        'episodes': episodes, 
        'chosenEps': chosenEps, 
        'nrOfEps': int( nrOfEps ),
        'nrOfChosenEps': int( nrOfChosenEps ),
        'chosenEpsLength': int( chosenEpsLength ),
        'infoText': 'Öppna avsnittet i Spotify och fortsätt till inspelning' 
    })

#Redirect user to recording view and set file info for Plyssningen
resultList = []
@app.route( '/to_recording', methods = ['POST'] )
def to_recording():
    resultList = []
    podcast = request.args.get( 'podcast' ).replace( ' ', '_' )
    currentEp = int( request.args.get( 'currentEp' ) )
    print(podcast)
    print(currentEp)
    try:
        episode = chosenEpsSet()[ currentEp ]
    except IndexError:
        return render_template( 'main.html', data = { 
        'podcasts': getPodcasts(), 
        'episodes': None,
        'nrOfEps': None,
        'infoText': 'Välj den podcast som ska transkriberas' 
    })
    recordInstance.setAttr( podcast, episode )
    recordInstance.writeInfo()
    return render_template( 'recording.html', data = { 
        'podcast': podcast, 
        'episode': episode, 
        'chosenEps': chosenEpsSet() 
    })

#Save file to computer
@app.route( '/download/<path:filename>.txt' )
def download( filename ):
    return send_file( 'text-files/' + filename + '.txt', attachment_filename = '' )

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
    if timeCount[1] == 10:
        timeCount[0] += 1
        timeCount[1] = 0
    recordInstance.time = timeCount
    return timeCount

#Start recording
@app.route( '/time' )
def time():
    timeList = request.args.get( 'time' ).split( ':' );
    minutes = "".join(timeList[0].split(' ')).strip('\n')
    minutesInt = int(minutes[0])*10 + int(minutes[1])
    if int( recordInstance.episode['length'] ) >= minutesInt:
        seconds = "".join(timeList[1].split(' '))
        timeList[0::1] = [ int(minutes[0]), int(minutes[1]) ]
        timeList[2::1] = [ int(seconds[0]), int(seconds[1]) ]
        recordInstance.time = timeList
        recordStatus = 'Spelar in...'
        recordMic = threading.Thread( target = recordInstance.startMicrophone, args = () )
        recordMic.start()
        return jsonify( { 'recordStatus': recordStatus } )
    else:
        return jsonify( { 'recordStatus': 'Avsnittet färdig avlyssnat!' })

#Check and handle recording status
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

#Save recording result to txt-file and show in view
@app.route( '/saveResult' )
def saveResult():
    recordInstance.setTime()
    timeString = str( recordInstance.time[0] ) + str( recordInstance.time[1] ) + ':' + str( recordInstance.time[2] ) + str( recordInstance.time[3] )
    resultList.append( { 'time': timeString, 'text': '"' + recordInstance.audioRes + '"' } )
    return jsonify( resultList )

@app.route('/openSpotify')
def openSpotify():
    print('spotify:episode:1kEr0FqisHG4T6inFzC2iM')
    return jsonify({"redirect": 'spotify:episode:0UPKQhbGXM5Iih9zDhVU9p'})
      

