import sys
import pyttsx3
import speech_recognition as sr
import datetime
import os
import cv2
import random
import webbrowser
import pywhatkit as kit
import smtplib
import wikipedia as wikipedia
from requests import get

engine = pyttsx3.init("sapi5")
voices = engine.getProperty("voices")
# print(voices[0].id)
engine.setProperty("voices", voices[0].id)


# text to speech
def speak(audio):
    engine.say(audio)
    print(audio)
    engine.runAndWait()


# to convert voice into text
def takecommand():
    r = sr.Recognizer()
    with sr.Microphone() as source:
        print("Listening...")
        r.pause_threshold = 1
        audio = r.listen(source, timeout=60, phrase_time_limit=0)

    try:
        print("Recognizing...")
        query = r.recognize_google(audio, language="en")
        print(f"user said: {query}")

    except Exception as e:
        speak("Say that again please...")
        return "none"

    return query


# to wish
def wish():
    hour = int(datetime.datetime.now().hour)

    if 0 <= hour <= 12:
        speak("Good morning")
    elif 12 > hour <= 18:
        speak("Good afternoon")
    else:
        speak("Good evening")

    speak("Please tell me how can I help you sir?")


# send email
def send_email(to, content):
    my_email = "emil.ivanchev.petkov@gmail.com"
    my_password = "emil17031992"
    server = smtplib.SMTP("smtp.gmail.com", 587)
    server.ehlo()
    server.starttls()
    server.login(my_email, my_password)
    server.sendmail(my_email, to, content)
    server.close()


if __name__ == "__main__":
    wish()

    while True:

        query = takecommand().lower()

        if "open notepad" in query:
            notepad = "C:\\Windows\\System32\\notepad.exe"
            os.startfile(notepad)

        elif "open cmd" in query:
            os.system("start cmd")

        elif "open the camera" in query:
            cap = cv2.VideoCapture(0)
            while True:
                ret, img = cap.read()
                cv2.imshow("webcam", img)
                k = cv2.waitKey(50)
                if k == 27:
                    break

            cap.release()
            cv2.destroyAllWindows()

        elif "play music" in query:
            music_path = "C:\\Users\\emili\\Music"
            songs = os.listdir(music_path)

            os.startfile(os.path.join(music_path, random.choice(songs)))

        elif "show me my ip address" in query:
            ip = get("https://api.ipify.org").text
            speak(f"Your IP address is {ip}")

        elif "wikipedia" in query:
            speak("searching for information in Wikipedia...")
            query = query.replace("wikipedia", "")
            result = wikipedia.summary(query, sentences=2)
            speak("according to wikipedia")
            speak(result)

        elif "open youtube" in query:
            speak("sir, what should i search on youtube?")
            play_video = takecommand().lower()
            kit.playonyt(play_video)

        elif "open google" in query:
            speak("sir, what should i search on google?")
            search = takecommand().lower()
            webbrowser.open(search)

        elif "open facebook" in query:
            webbrowser.open("http://www.facebook.com")

        elif "open pornhub" in query:
            webbrowser.open("http://www.pornhub.com")

        elif "open sportal.bg" in query:
            webbrowser.open("http://www.sportal.bg")

        # elif "send email" in query:
        #     try:
        #         speak("what should i say?")
        #         content = takecommand().lower()
        #         to = "emil.ivanchev.petkov@gmail.com"
        #         send_email(to, content)
        #         speak("Email has been sent to Emil")
        #
        #     except Exception as e:
        #         print(e)

        elif "turn off" in query:
            speak("thanks for using me sir, have a good day!")
            sys.exit()

