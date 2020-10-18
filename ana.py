'''
MIT License

Copyright (c) 2020 ilkay altınışık

Permission is hereby granted, free of charge, to any person obtaining a copy
of this software and associated documentation files (the "Software"), to deal
in the Software without restriction, including without limitation the rights
to use, copy, modify, merge, publish, distribute, sublicense, and/or sell
copies of the Software, and to permit persons to whom the Software is
furnished to do so, subject to the following conditions:

The above copyright notice and this permission notice shall be included in all
copies or substantial portions of the Software.

THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,
OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE
SOFTWARE.
'''


import os
import sys
import time
import playsound
import random
import speech_recognition as sr 
import webbrowser
import time

import random
from datetime import datetime
from gtts import gTTS

from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC

import feedparser #haber

import requests #hava durumu
import wikipedia
from googletrans import Translator #translate
from googletrans import LANGUAGES #diller

def speaktr(string):  # ses dosyası olusturdu ve caldı
    tts = gTTS(string,lang="tr")
    rand = random.randint(1,10000)
    file = 'audio-'+str(rand)+'.mp3'
    tts.save(file)
    playsound.playsound(file)
    os.remove(file)

def speak(string):  # ses dosyası olusturdu ve caldı
    tts = gTTS(string,lang="en")
    rand = random.randint(1,10000)
    file = 'audio-'+str(rand)+'.mp3'
    tts.save(file)
    playsound.playsound(file)
    os.remove(file)
       
def record(ask=False):  #konustugum metnı algıladı
    r = sr.Recognizer()
    with sr.Microphone() as source:
        if ask:
            speak(ask)
        audio = r.listen(source)
        voice =""

        try:
            voice = r.recognize_google(audio, language='en')
        except sr.UnknownValueError:
            speak("i don't understand, will you repeat")
        except sr.RequestError:
            speak("BipBop Erorrr")
    return voice


def response(voice):

    if "youtube" in voice:
        
        speak("what do you want me to call from youtube")
        time.sleep(0.5)
        ara = record("listen")
        speak("Youtube search " + ara)
        time.sleep(0.3)
        browser = webdriver.Chrome("/home/ilkayus/Desktop/sesss/chromedriver")
        browser.get("https://www.youtube.com/")
        search_field=browser.find_element_by_name("search_query")
        search_field.send_keys(ara + Keys.ENTER)
        WebDriverWait(browser,30).until(EC.title_contains(ara))
        WebDriverWait(browser,60).until(EC.element_to_be_clickable((By.ID,"img"))).click()
        time.sleep(500)

    elif "facebook" in voice:

        if "facebook" in voice:
            print("what do you want me to call from facebook")
            time.sleep(0.5)
            ara = record("listen")
            print("Facebook search " + ara)
            time.sleep(0.3)
            browser = webdriver.Chrome("/home/ilkayus/Desktop/sesss/chromedriver")
            browser.get("https://www.facebook.com/")

            email="email" #add facebook email address
            password="password" #add facebook password
            
            email_xpath='//*[@id="email"]'
            password_xpath='//*[@id="pass"]'
            login_button_xpath='//*[@id="u_0_b"]'


            email_element=browser.find_element_by_xpath(email_xpath)
            password_element= browser.find_element_by_xpath(password_xpath)
            login_button_element= browser.find_element_by_xpath(login_button_xpath)

            email_element.send_keys(email)
            password_element.send_keys(password)

    elif "news" in voice:
        url=("http://feeds.bbci.co.uk/news/world/rss.xml")

        news=feedparser.parse(url)
        i=0
        for x in news.entries:
            if i<=2:
                i+=1
                print(i,".news")
                print(x.title)
                print(x.description)
                speak(str(i)+". news")
                speak(x.title)
                speak(x.description)

            else:
                break
                
    elif "weather" in voice:
        speak("which city would you like to know the weather?")
        time.sleep(0.5)
        city = record("Dinliyorum")
        speak(city + " weather.")
        url= 'https://samples.openweathermap.org/data/2.5/weather?q='+city+',uk&appid=439d4b804bc8187953eb36d2a8c26a02a'
        res= requests.get(url)
        data=res.json()
        temp = data['main']['temp']
        wind_speed = data['wind']['speed']
        description= data['weather'][0]['description']

        print("Temperature : {} degree celcius".format(temp))
        print("Wind Speed : {} m/s ".format(wind_speed))
        print("Description  : {} ".format(description))

    elif "location" in voice:
        res = requests.get("https://ipinfo.io/")
        data=res.json()
        city  = data["city"]
        # location = data["loc"].split(",")
        # latitude = location[0]
        # longitude = location[1]
        speak("your location ")
        time.sleep(0.5)
        speak("City : "+ city)

    elif "translate" in voice:
        speak("Turkish translation")
        time.sleep(0.5)
        tr = record("what should i dial")
        print(tr)
        speak(tr)
        speaktr(" cümlesi türkçeye çevriliyor")
        trans = Translator()
        t=trans.translate(tr,dest="tr")#bütün dilerden tr ceviri 
        speaktr(f"{t.text}")

    elif "what time" in voice:
        speak(datetime.now().strftime('%H:%M:%S'))

    elif "stop" in voice:
        speak('by by')
        exit()

    elif "google " in voice:
        speak("what do you want me to call from google")
        time.sleep(1)
        speak("listen")
        time.sleep(0.5)
        search = record("Dinliyorum")
        url = "https://google.com/search?q="+ search
        webbrowser.get().open(url)
        speak(search + ' hakkında bulduklarım. ')
    
    elif "wikipedia " in voice:
        speak("what do you want me to call on wikipedia")
        time.sleep(1)
        wik = record("Listen")
        time.sleep(1)
        speak(wik + '  what i find about. ')
        time.sleep(1)
        speak(wikipedia.page(wik).title)
        speak(wikipedia.summary(wik, sentences=2))
        
evethayır=["yes","no"]
zar=["1","2","3","4","5","6"]
yazıtura=["tura","yazı"]
def game(voice):
    if "game" in voice:
        speak("What do you want to play")
        ses=record("listen")
    
        if "dice" in ses:
            speak("dice rolled")
            speak("incoming number "+random.choice(zar))
            print("yes")

        elif "yes or no" in ses:
             random.choice(evethayır)

        elif "coin toss" in ses:
            speak("coin toss")

            random.choice(yazıtura)

        
selamlasma=["hi","hello","man","hey"]
def selamla(voice):

    if " " not in voice:
        if voice in selamlasma:
            a = random.choice(selamlasma)
            speak(a)
            print(a)

    elif " " in voice:
        ayrılmıs = voice.split()
        for kelime in ayrılmıs:
            if kelime in selamlasma:
                speak(random.choice(selamlasma))
                print(random.choice(selamlasma))

list2=[]
def alısveris(voice):

    if "add" in voice:
        speak("ne eklemek ıstersın")
        time.sleep(0.5)
        ekle = record("dinliyorum") 
        list2.append(ekle)
        print (list2)

    elif "my" in voice:
        for i in range(len(list2)):
            print (str(i+1)+".",list2[i])


    elif "delete" in voice:
        speak




def bos(voice):
    if "night" in voice:
        speak("good night")
    elif "loneliest" in voice:
        speak("")
    elif "Who" in voice:
        speak("I am Dodo")
    elif "color" in voice:
        speak("Red")
    elif "from" in voice:
        speak("I was born in creativity room in Turkey")
    elif "life" in voice:
        speak("I live in a network open to half the internet. Do you want to expand my limits hahahaha")
    elif "morning" in voice:
        speak("good morning mortal")
    elif "age" in voice:
        speak("I am 1 years old in my own time")
    elif "family" in voice:
        speak("my family goes to the calculator")


speaktr("hi how can i help you")


while 1:
    voice = record("listen")  #kucuk harfe donusturdu gelen ses dosyasındakı verıyı
    time.sleep(0.5)
    print("Söyledigin kelime : "+voice)
    voice=voice.lower() #kucuk har yaptı hepsını

    selamla(voice)
    response(voice)
    game(voice)
    alısveris(voice)
    bos(voice)
