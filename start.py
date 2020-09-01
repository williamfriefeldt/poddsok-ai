from flask import Flask, render_template, request
import pyrebase

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

@app.route('/')
def index():
	return render_template('main.html')

@app.route('/handle_podcast', methods=['POST'])
def handle_podcast():
	firebase = pyrebase.initialize_app(config)
	db = firebase.database()
	user = db.child("alexochsigge").get()
	ep = user.val()['ep1']
	#podcast = request.form['podcast']

	return render_template('main.html', podcast = ep['name'])