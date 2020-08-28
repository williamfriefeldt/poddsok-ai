import speech_recognition as sr
import keyboard as key

time = { 'minute':0, 'second': 0 }
file = open( "test_res.txt", "w" )

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
    
def start():
    opt = input("Start recording? j/n: ")
    if opt == "j" :
        record()
    else:
        opt = input("Avsluta? j/n: ")
        if opt == "n":
            start()
        else:
            file.close()

def main():
    print("Before recording, choose pod, episode and start time")
    pod = input("Podcast: ")
    episode = input("Episode: ")
    file.write( "Podcast: " + pod + "\n" + "Episode: " + episode + "\n=======================\n")
    time_inp = input("Start time (MM:SS): ")
    time_inp = time_inp.split(':')
    time['minute'] += int(time_inp[0])
    time['second'] += int(time_inp[1])
    start()

main()
