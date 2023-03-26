from __future__ import print_function
from gtts import gTTS
import pyttsx3
#gtts is too slow better use pyttsx3 dont need to use file
import os
import time
import playsound
import speech_recognition as sr
from io import BytesIO
import math
import pyaudio
import datetime
import os.path
from google.auth.transport.requests import Request
from google.oauth2.credentials import Credentials
from google_auth_oauthlib.flow import InstalledAppFlow
from googleapiclient.discovery import build
from googleapiclient.errors import HttpError
# need to use virtual enviroment
#use google calendar api and integrated with the assisance
# If modifying these scopes, delete the file token.json.
SCOPES = ['https://www.googleapis.com/auth/calendar.readonly']
# creating lists for months, dates, days
#global variables for getting date function
MONTHS = ["january", "february", "march","april", "may", "june", "july", "september", "october", "november", "december"]
DAYS = ["mondays", "tuesday", "wednesday" , "thursday", "friday", "saturday", "sunday"]
DATES_extension = ["st" , "rd", "th" ]

#speak function return in sound whatever text or string is given as input 
def speak(text):
    engine = pyttsx3.init()
    engine.say(text)
    engine.runAndWait()



#authentication function is from google calenedar api where it grant us access to the users GC account
def authentication():
    """Shows basic usage of the Google Calendar API.
    Prints the start and name of the next 10 events on the user's calendar.
    """
    creds = None
    # The file token.json stores the user's access and refresh tokens, and is
    # created automatically when the authorization flow completes for the first
    # time.
    if os.path.exists('token.json'):
        creds = Credentials.from_authorized_user_file('token.json', SCOPES)
    # If there are no (valid) credentials available, let the user log in.
    if not creds or not creds.valid:
        if creds and creds.expired and creds.refresh_token:
            creds.refresh(Request())
        else:
            flow = InstalledAppFlow.from_client_secrets_file('credentials.json', SCOPES)
            creds = flow.run_local_server(port=0)
        # Save the credentials for the next run
        with open('token.json', 'w') as token:
            token.write(creds.to_json())

    
    service = build('calendar', 'v3', credentials=creds)
    return service



#function will return the next 10 events from GC
def events(service): 
        # Call the Calendar API
    now = datetime.datetime.utcnow().isoformat() + 'Z'  # 'Z' indicates UTC time
    print('Getting the upcoming 10 events')
    events_result = service.events().list(calendarId='primary', timeMin=now,maxResults=10, singleEvents=True,orderBy='startTime').execute()
    events = events_result.get('items', [])
    if not events:
        print('No upcoming events found.')
        return
    # Prints the start and name of the next 10 events
    for event in events:
        start = event['start'].get('dateTime', event['start'].get('date'))
        print(start, event['summary'])
 



# will obtain a voice input from the user and return it as a text
def get_audio_input():
    r = sr.Recognizer()#recognizer object 
    with sr.Microphone() as source:
        audio = r.listen(source)
        said = " "

        try:
            said =  r.recognize_google(audio)#can also use the google API to recognize what we have just said
            print(said)
        except Exception as e:
            print("Exception:" + str(e))
    return said

#create a function to get the date from the user through voice, however input is string
def get_date(text):
    # convert data into lowercase so it is easier for the code to find keywords
    texts = text.lower()
    # get todays date
    todays = datetime.date.today()

    if text.count("today") > 0: 
        return todays
    
    month = 0
    day = -1 
    year = todays.year
    dates = -1
    dext = 0

    # searches for key words in the text
    for word in texts.split(): 
        if word in MONTHS:
            month = MONTHS.index(word) + 1 

        elif word in DAYS:
            day = DAYS.index(word)
        
        elif word.isdigit():
            dates = int(word)

        elif word[-2:] in DATES_extension:
            if word.isdigit():
                dates = int(word) 
                print(dates)
#if the user gives a month that has already passed from today the program will assume you are talking about next year
    if month < todays.month and month != -1:
        year = year + 1

    if day < todays.day and month == -1 and day != -1:
        month = month + 1
    
    if month == -1 and dates == -1 and day != -1: 
        month = todays.month
        #.weekday reutrns the day of the week as an integer where monday would be 0 and sunday 6 
        current_day_of_week = todays.weekday()
        difference = day - current_day_of_week
        # in the case where the code takes a day of the week that has alreayd passed
        #wanting the day of next week so adding 7 days into the difference of days between today and the desired day 
        if difference < 0: 
            dif += 7
            if "next" in text.split():
                difference += 7
#.timedelta calculates the difference in dates and return that date that the user wants
        return todays + datetime.timedelta(difference)

    return datetime.date(month= month, dates = dates, year = year)

text = get_audio_input().lower()
print(get_date(text))


        

        



    









'''      
recording = sr.Recognizer()

with sr.Microphone() as source: 
    recording.adjust_for_ambient_noise(source)
    speak("Please Say something:")
    audio = recording.listen(source)

try:
    print("You said: n" + recording.recognize_google(audio))
except Exception as e:
    print(e)



mp3_fp = BytesIO()
tts = gTTS('hello', lang='en')
tts.write_to_fp(mp3_fp)
'''