import speech_recognition as sr
import time
import os

# DEFINITIONS
file_limit = 20 # @param:  the maximum amount of wav files we want

# @ param is the number of files created before overwriting old files starting from 1.
def m2S(file_limit):
    print("m2S");
    r = sr.Recognizer()
    i = 1
    while True:
        if i >= file_limit:
            i = 1

        with sr.Microphone() as source:
            print("Say Something:")
            audio = r.record(source, duration = 4)

            file_name = "test" + str(i) +".wav"
            with open(file_name, "wb") as f:
                f.write(audio.get_wav_data())
        i+=1

# convert speech to wav file ordered from one to file_limit
# @ param is the number of files created before overwriting old files starting from 1.
def s2T(file_limit):
    # print("s2T is working")
    r = sr.Recognizer()
    i = 1
    while True:
        # reset i counter to i if we go beyond the limit of wav files we want
        if i >= file_limit:
            i = 1

        try:
            hello = sr.AudioFile('test' + str(i) + '.wav')
            with hello as source:
                audio = r.record(source)
            try:
                google_text = r.recognize_google(audio)
                convertTxt(google_text, i)

            # this exception is if there is nothing in the audio file
            except Exception as e:
                print("ERROR NO SOUND")

            os.remove('test' + str(i) + '.wav')
            i+=1

        # this exception is for if we dont have a audio file by that name
        except:
            print("...");
            time.sleep(3);
            
#@param is the translated google text file using the google speech API and
#the variable 'i' is from the counter to indicate the txt file per wav file
def convertTxt(google_text, i):
    print("changing to txt now!")
    file = open("txt" + str(i) + ".txt", "w")
    file.write(google_text)
    file.close()
