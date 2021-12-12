from bs4 import BeautifulSoup
import requests
import speech_recognition as sr
import pyttsx3


def parapser(paras):
    de_split = paras.split("$$")
    '''for i in de_split:
        if i[0] == '[' :
            print(i)
            de_split.remove(i)'''
    print(de_split)
    for po in range(0, len(de_split), 2):
        #engine.say(de_split[po])
        #engine.say(de_split[po+1])
        pass

def a_tagModifier(soup,a_dic):
    fil = soup.find_all('a')
    #fil = filterNoneType(fil)
    for tag in fil:
        try:
            if tag.string != None :
                if tag.string[0] == '[':
                    tag.decompose()
                else:
                    a = len(tag.string)
                    a_dic[tag.string] = tag.get('href')
                    b = "$$"+tag.string+"$$"
                    tag.string = b
                    print(b)
                    print(tag.string)
        except AttributeError:
            pass


def pparse(pagedic,url, a_dic):
    page = requests.get(url)
    soup = BeautifulSoup(page.content, 'html.parser')
    a_tagModifier(soup, a_dic)
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
a_dic = {}
url="https://en.wikipedia.org/wiki/Pranab_Mukherjee"
pparse(pagdic, url , a_dic)
print(pagdic.keys())
print(pagdic['Illness and death'])
parapser(pagdic['Illness and death'])
print(a_dic)