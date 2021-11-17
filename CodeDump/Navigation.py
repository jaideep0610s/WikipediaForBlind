from bs4 import BeautifulSoup as soup 
from urllib.request import urlopen as uReq
import re
import wikipedia
import requests
import speech_recognition as sr
import pyttsx3
import AppKit


r = sr.Recognizer()


S = requests.Session()

engine = pyttsx3.init() #tts engine
inp = "Say the topic to be searched " 
engine.say(inp) # asli text to speech
engine.runAndWait()
with sr.Microphone() as source:
    r.adjust_for_ambient_noise(source)
    AppKit.NSBeep()
    audio_data = r.record(source, duration=5)
    try:
        # using google speech recognition
        search = r.recognize_google(audio_data)
    except:
        comm=("Sorry, I did not get that")
        engine.say(comm) # asli text to speech
        engine.runAndWait()
topic = search.split(" ")
#search = input("Enter topic to be searched: ")
seed_url = "https://en.wikipedia.org/wiki/"

for i in range(0, len(topic)):
    if i==0:
        seed_url+= topic[i]
    else:
        seed_url += "_" + topic[i]

print(seed_url)

uClient = uReq(seed_url)
page_html = uClient.read()

page_soup = soup(page_html,"html.parser")
div = page_soup.find(id = "toc")

uls = div.find(name = "ul")
li = uls.find_all(name = "li", recursive = False)

headings = []

for i in li:
    a = i.find_all("a")
    subheading=[]
    for link in a:
        #print(link)
        subheading.append(link)
    headings.append(subheading)
    #headings.append(a)
#print(headings)

curr = 0

curr_section=0

msg=("Sorry, I did not get that")

while(curr!= len(headings)):
    h = headings[curr][0]
    heading = h.getText()
    engine = pyttsx3.init() #tts engine
    engine.say(heading) # asli text to speech
    engine.runAndWait()
    #print(heading)
    ques = ("Do you want to read this")
    engine.say(ques) # asli text to speech
    engine.runAndWait()
    #inp = input("Do you want to read this (y/next/prev): ")
    with sr.Microphone() as source:
        r.adjust_for_ambient_noise(source)
        AppKit.NSBeep()
        audio_data = r.record(source, duration=5)
        try:
        # using google speech recognition
            text = r.recognize_google(audio_data)
            valid_text = ['next heading', 'previous heading', 'yes']
            #res = [ele for ele in valid_text if(ele in text)]
            #print("apna word haina : " + str(bool(res)))
            print(text)
            if text == "next heading":
                if(curr == len(headings) -1):
                    comm ="We have reached the end of the page."
                    engine.say(comm) # asli text to speech
                    engine.runAndWait()
                    #print("We have reached the end of the page.")
                curr_section += len(headings[curr])
                curr+=1
            if text == "previous heading":
                if(curr == 0):
                    comm ="This is the first heading."
                    engine.say(comm) # asli text to speech
                    engine.runAndWait()
                    #print("This is the first heading. ")
                curr-=1
                curr_section -= len(headings[curr])
            if text == "yes":
                URL = "https://en.wikipedia.org/w/api.php"

                PARAMS = {
                    "action": "parse",
                    "section" : str(curr_section+1),
                    "page": search,
                    "prop": "wikitext",
                    "format": "json"
                }

                R = S.get(url=URL, params=PARAMS)
                DATA = R.json()

                data = DATA["parse"]["wikitext"]["*"]
                engine.say(data) # asli text to speech
                engine.runAndWait()
                #print(DATA["parse"]["wikitext"]["*"])
                curr_section += len(headings[curr])
                curr+=1
            
        except:
            comm=("Sorry, I did not get that")
            engine.say(comm) # asli text to speech
            engine.runAndWait()
            #print(comm)

    '''if(inp == "y"):

        URL = "https://en.wikipedia.org/w/api.php"

        PARAMS = {
            "action": "parse",
            "section" : str(curr_section+1),
            "page": search,
            "prop": "wikitext",
            "format": "json"
        }

        R = S.get(url=URL, params=PARAMS)
        DATA = R.json()

        print(DATA["parse"]["wikitext"]["*"])
        curr_section += len(headings[curr])
        curr+=1

    elif(inp == "next"):
        if(curr == len(headings) -1):
            print("We have reached the end of the page.")
        curr_section += len(headings[curr])
        curr+=1
    else:
        if(curr == 0):
            print("This is the first heading. ")
        curr-=1
        curr_section -= len(headings[curr])'''



