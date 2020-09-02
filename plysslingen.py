import speech_recognition as sr
import keyboard as key

class Plyssningen:

    def __init__(self):
        self.podcast = ''
        self.episode = ''
        self.time = ''
        self.file = ''
        self.audioRes = ''
        self.isListening = False

    def __str__(self):
        return self.podcast + ' ' + self.episode + ' ' + str(self.time[0])+str(self.time[1])+':'+str(self.time[2])+str(self.time[3])

    def setAttr(self, podcast, episode, time):
        self.podcast = podcast
        self.episode = episode
        self.time = time
        self.file = open( "test_res.txt", "w" )

    def writeInfo(self):
        self.file.write( "Podcast: " + self.podcast + "\n" + "Episode: " + self.episode + "\n=======================\n")

    def setTime(self, time):
        self.time = time
        self.file = open( "test_res.txt", "a+" )
        self.file.write(time + "\n")

    def getAudioRes(self):
        return self.audioRes

    def checkListening(self):
        return self.isListening

    def startMicrophone(self):
        self.isListening = True
        key.press_and_release('play/pause media')
        r = sr.Recognizer()
        mic = sr.Microphone()
        print('hej')
        try:
            with mic as source:
                r.adjust_for_ambient_noise(source)
                audio = r.record(source, duration=8)
                self.result(audio, r)
        except AssertionError as e:
            print( "There was an error in the recording:")
            print(e)
            print(mic)
            start()

    def result(self, audio, r):
        key.press_and_release('play/pause media')
        try:
            self.audioRes = r.recognize_google(audio, language='sv-SE')
        except:
            self.audioRes = 'Could not find sound :/'
        self.isListening = False



