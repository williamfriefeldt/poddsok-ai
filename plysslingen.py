import speech_recognition as sr
import keyboard as key

class Plyssningen:

    def __init__(self, podcast, episode, time):
        self.podcast = podcast
        self.episode = episode
        self.time = time
        self.file = open( "test_res.txt", "w" )

    def __str__(self):
        return self.podcast + ' ' + self.episode + ' ' + str(self.time[0])+str(self.time[1])+':'+str(self.time[2])+str(self.time[3])

    def writeInfo(self):
        self.file.write( "Podcast: " + self.podcast + "\n" + "Episode: " + self.episode + "\n=======================\n")

    def record():
        print( 'Recording...')
        key.press_and_release('play/pause media')
        r = sr.Recognizer()
        mic = sr.Microphone()
        try:
            with mic as source:
                r.adjust_for_ambient_noise(source)
                audio = r.record(source, duration=8)
                result(audio, r)
        except AssertionError as e:
            print( "There was an error in the recording:")
            print(e)
            print(mic)
            start()

    def result(audio, r):
        key.press_and_release('play/pause media')
        time['second'] += 10
        if time['second'] > 60:
            time['minute'] += 1
            time['second'] = time['second'] % 60
        try:
            print( "=== Result ===" )
            file.write( str(time['minute'])+':'+str(time['second']) + ' : ' + r.recognize_google(audio, language='sv-SE') + "\n" )
            print( "==============" )
        except:
            print( 'Could not find sound :/' )
        start()



