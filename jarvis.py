import smtplib
import sys
from email.mime.text import MIMEText
import pyttsx3
import speech_recognition as sr
import datetime
import os
import cv2
import random
import webbrowser
import pywhatkit as kit
import wikipedia
from requests import get
import time

engine = pyttsx3.init("sapi5")
voices = engine.getProperty("voices")
engine.setProperty("voice", voices[1].id)

# Добавете останалите контакти тук
contacts = {
    "number one": "Your email",
    "number two": "",
    "number three": "",
}


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
    hour = datetime.datetime.now().hour
    minutes = datetime.datetime.now().minute

    if 0 <= hour <= 11:
        info = f"Good morning sir. The time is currently {hour:02}:{minutes:02}. Today is {datetime.datetime.now().date()}."
        speak(info)

    elif 12 <= hour <= 18:
        info = f"Good afternoon sir. The time is currently {hour:02}:{minutes:02}. Today is {datetime.datetime.now().date()}."
        speak(info)
    else:
        info = f"Good evening sir. The time is currently {hour:02}:{minutes:02}. Today is {datetime.datetime.now().date()}."
        speak(info)

    speak("Please tell me how can I help you sir?")


# send email
def send_email(to, content):
    sender_email = 'emil.ivanchev.petkov@abv.bg'
    receiver_email = to
    subject = 'Test Email'
    message = content

    # Въвеждане на потребителското име и паролата на акаунта на ABV.bg
    username = 'emil.ivanchev.petkov@abv.bg'
    password = 'kknn44oo'

    try:
        # Създаване на съобщението
        msg = MIMEText(message)
        msg['Subject'] = subject
        msg['From'] = sender_email
        msg['To'] = receiver_email

        # Настройка на SMTP сървъра на ABV.bg
        smtp_server = 'smtp.abv.bg'
        smtp_port = 465

        # Изпращане на имейла
        with smtplib.SMTP_SSL(smtp_server, smtp_port) as server:
            server.login(username, password)
            server.sendmail(sender_email, receiver_email, msg.as_string())
        print('Email sent successfully!')
    except Exception as e:
        print('An error occurred while sending the email:', str(e))


if __name__ == "__main__":
    wish()

    while True:

        query = takecommand().lower()

        if "open notepad" in query:
            notepad = "C:\\Windows\\System32\\notepad.exe"
            os.startfile(notepad)

        elif "open cmd" in query:
            os.system("start cmd")

        elif "open camera" in query:
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
            try:
                speak("searching for information in Wikipedia...")
                query = query.replace("wikipedia", "")
                result = wikipedia.summary(query, sentences=2)
                speak("according to wikipedia")
                speak(result)
            except:
                speak("I'm sorry, I couldn't find any information in Wikipedia. Try again.")
                pass

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

        elif "send email" in query:
            while True:
                speak("To whom should I send the email?")
                contact_name = takecommand().lower()
                try:
                    receiver_email = contacts[contact_name]
                    break
                except KeyError:
                    speak("I'm sorry, the contact is not found in the address book. Please try again.")

            speak("What should be the content of the email?")
            content = takecommand().lower()
            send_email(receiver_email, content)

        elif "open pictures" in query:
            pictures_path = "C:\\Users\\emili\\OneDrive\\Pictures"
            os.path.exists(pictures_path)
            os.startfile(pictures_path)

        elif "turn off" in query:
            speak("thanks for using me sir, have a good day!")
            sys.exit()
