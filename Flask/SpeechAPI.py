# -*- coding: utf-8 -*-
"""
Created on Fri Nov 23 01:02:03 2018

@author: viren
"""

from flask import Flask
app = Flask(__name__)

import logging
logging.basicConfig(level=logging.DEBUG)

import speech_recognition as rs
import pyttsx3
import json
import requests

import pyaudio
import audioop
import math
import threading

import time

import speech_recognition as sr

RASA_URL = "http://127.0.0.1:5005/webhooks/rest/webhook"

# Microphone stream config.
CHUNK = 1024  # CHUNKS of bytes to read each time from mic
FORMAT = pyaudio.paInt16
CHANNELS = 1
RATE = 16000
THRESHOLD = 400  # The threshold intensity that defines silence
                  # and noise signal (an int. lower than THRESHOLD is silence).

SILENCE_LIMIT = 1  # Silence limit in seconds. The max ammount of seconds where
                   # only silence is recorded. When this time passes the
                   # recording finishes and the file is delivered.
        
def audio_int(num_samples=50):
    """ Gets average audio intensity of your mic sound. You can use it to get
        average intensities while you're talking and/or silent. The average
        is the avg of the 20% largest intensities recorded.
    """
        
    p = pyaudio.PyAudio()

    stream = p.open(format=FORMAT,
                    channels=CHANNELS,
                    rate=RATE,
                    input=True,
                    frames_per_buffer=CHUNK)

    values = [math.sqrt(abs(audioop.avg(stream.read(CHUNK), 4))) 
              for x in range(num_samples)] 
    values = sorted(values, reverse=True)
    r = sum(values[:int(num_samples * 0.2)]) / int(num_samples * 0.2)
    print(" Average audio intensity is ", r)
    stream.close()
    p.terminate()
    
    if r > THRESHOLD:
        listen(0)
    
    threading.Timer(SILENCE_LIMIT, audio_int).start()
    
def listen(x):
    r=rs.Recognizer()
    #if x == 0:
        #print('say Hi. How can I help?')
    with rs.Microphone() as source:
        audio=r.listen(source)
    try:
        text = r.recognize_google(audio)
        y = process(text.lower())
        return(y)
    except:
        if x == 1:
            print('say Good Bye!')
        else:
            print('say I did not get that. Please say again.')
            listen(1)

def process(text):
 #   ''''''''''''''''''''''''''''''''''''''''''''''''
 #   '''''''Your application goes here ''''''''''''''
 #   ''''''''''''''''''''''''''''''''''''''''''''''''
    engine = pyttsx3.init()
    engine.say('Good morning.')
    engine.runAndWait()
    
def sendRequest(message):
    # sending post request and saving response as response object
    reqObj = {}
    reqObj['sender'] = "U123"
    reqObj['message'] = message
    return requests.post(url = RASA_URL, data = reqObj) 
    
def speakResponse(engine, val):
    engine.say(val)
    engine.setProperty('rate', 130)
    engine.runAndWait()
    
def processResponse(response):
    
    engine = pyttsx3.init()
    data_arr = json.load(response)
    isEnterEmail = False
    buttonArr = []
    for data in data_arr:
        for key in data:
            if key == 'text':
                val = data[key]
                if val.lower() == 'enter email to send details!':
                    isEnterEmail = True
                else:
                    speakResponse(engine, val)
            elif key == 'button':
                buttonArr = data[key]
    
    if isEnterEmail:
        val = 'Would you like to receive list of top restaurants to your registered email id?'
        speakResponse(engine, val)
    elif buttonArr:
        for button in buttonArr:
            for key in button:
                if key == 'payload':
                    val = button[key]
                    speakResponse(engine, val)
    

# this is called from the background thread
def callback(recognizer, audio):
    # received audio data, now we'll recognize it using Google Speech Recognition
    try:
        # for testing purposes, we're just using the default API key
        # to use another API key, use `r.recognize_google(audio, key="GOOGLE_SPEECH_RECOGNITION_API_KEY")`
        # instead of `r.recognize_google(audio)
        print("Enter callback")
        text = recognizer.recognize_google(audio)
        #text = recognizer.recognize_sphinx(audio)
        print("Text: " + text)
        print("Google Speech Recognition thinks you said " + text)
        
        # sending request to RASA bot
        response = sendRequest(text)
        
        # process response
        processResponse(response)
        
    except sr.UnknownValueError:
        print("Google Speech Recognition could not understand audio")
    except sr.RequestError as e:
        print("Could not request results from Google Speech Recognition service; {0}".format(e))

@app.route('/')
def index():
    #audio_int()
    r = sr.Recognizer()
    m = sr.Microphone()
    #r.energy_threshold = 300
    with m as source:
        r.adjust_for_ambient_noise(source, duration=5)  # we only need to calibrate once, before we start listening
    
    # start listening in the background (note that we don't have to do this inside a `with` statement)
    
    stop_listening = r.listen_in_background(m, callback)
    # `stop_listening` is now a function that, when called, stops background listening
    
    # do some unrelated computations for 5 seconds
    #for _ in range(50): time.sleep(0.1)  # we're still listening even though the main thread is doing other things
    
    # calling this function requests that the background listener stop listening
    #stop_listening(wait_for_stop=False)
    
    # do some more unrelated things
    #while True: time.sleep(0.1)
    return "success"

if __name__ == "__main__":
    app.run(debug=True)