'''
Imports:
- Speech Recognition: library to transcript audio through microphone
- Keyboard: Python access computer keyboard
'''
import speech_recognition as sr
import keyboard as key

#Class to start sound, record audio from microphone, analyze audio and return result to start.py.
class Plyssningen:
    '''
    Attributes:
     - Chosen podcast and episode
     - Current time
     - Text file to save result
     - Listening status
    '''
    def __init__( self ):
        self.podcast = ''
        self.episode = ''
        self.time = [ 0, 0, 0, 0 ]
        self.file = ''
        self.audioRes = ''
        self.isListening = False

    #Set podcast, episode and reset time
    def setAttr( self, podcast, episode ):
        self.podcast = podcast
        self.episode = episode
        self.time = [ 0, 0, 0, 0 ]

    #Save podcast and episode titles to text file
    def writeInfo( self ):
        self.file = open( "text-files/" + self.podcast + "_-_" + self.episode + '.txt' , "w+" )
        self.file.write( "Podcast: " + self.podcast + "\n" + "Episode: " + self.episode + "\n=======================\n" )
        self.file.close()

    #Save audio result and current time to text file
    def setTime( self ):
        self.file = open( "text-files/" + self.podcast + "_-_" + self.episode + '.txt' , "a+" )
        time = str( self.time[0] ) + str( self.time[1] ) + ':' + str( self.time[2] ) + str( self.time[3] )
        self.file.write( time + ' - "' + self.audioRes + '"\n' )
        self.file.close()

    def getAudioRes( self ):
        return self.audioRes

    def checkListening( self ):
        return self.isListening

    #Recording by starting computer audio and access microphone
    #When audio is recorded (after given duration), run self.result()
    def startMicrophone( self ):
        self.isListening = True
        self.audioRes = ''
        try:
            key.press_and_release( 'F8' )
        except ValueError:
            self.audioRes = 'Tillåtelse till tangentbord nekat, vänligen tillåt detta.'
            self.isListening = False
        r = sr.Recognizer()
        mic = sr.Microphone()
        try:
            with mic as source:
                r.adjust_for_ambient_noise( source )
                audio = r.record( source, duration = 15 )
                self.result( audio, r )
        except AssertionError as e:
            print( "There was an error in the recording:" )
            print( e )
            print( mic )

    #Handle result when recording is done
    def result( self, audio, r ):
        key.press_and_release('F8')
        self.audioRes = 'Analyserar ljud...'
        try:
            self.audioRes = r.recognize_google(audio, language='sv-SE')
            self.isListening = False
        except:
            self.audioRes = 'Hittade inget ljud'
            self.isListening = False
        



