from bs4 import BeautifulSoup
import requests
import speech_recognition as sr
import pyttsx3


def pparse(pagedic,url):
    page = requests.get(url)
    soup = BeautifulSoup(page.content, 'html.parser')
    '''paras = soup.select('h2 + p')
    hedkey = paras[2].find_previous_sibling('h2').span.get_text()
    print(hedkey)'''
    heading_tags = ["h2", "h3"]
    #print(soup.find_all(heading_tags))
    for section in soup.find_all(heading_tags):
        nextNode = section
        flag = True
        #print(nextNode)
        try:
            hed = nextNode.span.get_text()
            #print(hed)
            bdy = ""
        except AttributeError:
            flag = False
        while flag:
            try:
                nextNode = nextNode.nextSibling
            except:
                #print("eeg")
                break
            try:
                tag_name = nextNode.name
                #print(tag_name)
            except AttributeError:
                tag_name = ""
            #if tag_name == "p":
            try:
                bdy += nextNode.get_text()
            except AttributeError:
                pass
            #print(nextNode.get_text())
            if tag_name == "h2" or tag_name == "h3" or tag_name == "h1":
                pagedic[hed]=bdy
                break
            else:
                pass
    #print(pagedic)


pagdic = {}
url="https://en.wikipedia.org/wiki/Pranab_Mukherjee"
pparse(pagdic, url)
print(pagdic.keys())
print(pagdic['Illness and death'])