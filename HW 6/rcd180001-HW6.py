from bs4 import BeautifulSoup
import requests
import re
from urllib import request
import os
import pickle

import nltk
from nltk import sent_tokenize
from nltk import word_tokenize
from nltk.corpus import stopwords

def main():
    #Make folder to store data
    folder = "Data"
    mode = 0o666
    parent = os.path.dirname(__file__)
    path = os.path.join(parent, folder)
    if not os.path.exists(path):
        os.mkdir(path)

    #Obtain URLs and Scrape Text
    webCrawler()
    fileNum = textScrape()
    sentTokenizer(fileNum)
    frequencies = importantTerms(fileNum)
    
    #Reverse sort dictionary by value and print 25 most common terms
    sortedFreq = dict(sorted(frequencies.items(), key=lambda item:item[1], reverse=True))
    print("Top 25 Terms")
    i = 1
    for key in sortedFreq:
        print(i, key, ":", frequencies[key])
        i += 1

        if i == 26:
            break
    
    #Print top 10 important terms
    print("\nTop 10 Important Terms")
    print("1 film :", frequencies["film"])
    print("2 director :", frequencies["director"])
    print("3 looper :", frequencies["looper"])
    print("4 jedi :", frequencies["jedi"])
    print("5 knives :", frequencies["knives"])
    print("6 critics :", frequencies["critics"])
    print("7 september :", frequencies["september"])
    print("8 episode :", frequencies["episode"])
    print("9 brick :", frequencies["brick"])
    print("10 johnson :", frequencies["johnson"])

    #Create knowledge base
    facts = {"film":"Joseph Gordon-Levitt is in all his movies, either as a character or shows up in a cameo",
    "director":"Rian Johnson was inspired to become a film director after seeing Annie Hall",
    "looper":"The script was featured on the 2010 Blacklist; a list of the most liked unmade scripts of the year",
    "jedi":"The Porgs species in the films were created because Puffins kept getting into the movie",
    "knives":"Rian Johnson came up with the idea of Knives Out after making Brick",
    "critics":"He is married to Karina Longworth, a movie writer and critic",
    "september":"Looper was released on September",
    "episode":"He directed 3 episodes of Breaking Bad, including Ozymandias",
    "brick":"The film's use of language is inspired by Dashiell Hammett novels",
    "johnson":"He is in a folk band with his brother Nathan Johnson"}

    pickle.dump(facts, open('HW 6/Data/knowledgeBase.p', 'wb'))

#Obtains relevant urls
def webCrawler():
    starter_url = "https://www.google.com/search?client=firefox-b-1-d&sxsrf=ALiCzsbIRt9qA09ixVqNpuEOjYr8BpxPBA:1664861141705&q=Rian+Johnson&stick=H4sIAAAAAAAAAOPgE-LVT9c3NMzKLYw3tixKUeLUz9U3sDDIrazSEstOttJPy8zJBRNWKZlFqckl-UWLWHmCMhPzFLzyM_KK8_N2sDLuYmfiYAAAHussrksAAAA&sa=X&ved=2ahUKEwixkM6H68X6AhWYj2oFHVqICDMQmxMoAHoECGQQAg&biw=958&bih=926&dpr=1"
    req = requests.get(starter_url)
    data = req.text
    soup = BeautifulSoup(data,"lxml")

    #Stores urls relating to rian johnson
    parent = os.path.dirname(__file__)
    path = os.path.join(parent, "Data")
    fileName = os.path.join(path, "rianJohnsonURL.txt")
    
    file = open(fileName, 'w')

    #Go through each url and check if it's related
    urlList = []
    for link in soup.find_all('a'):
        link_str = str(link.get('href'))
        if ('Rian' in link_str or 'rian' in link_str or 'imdb' in link_str or 'wikipedia' in link_str) and ('instagram' not in link_str):
            if link_str.startswith('/url?q='):
                link_str = link_str[7:]
            if '&' in link_str:
                i = link_str.find('&')
                link_str = link_str[:i]
            if (link_str not in urlList) and (link_str.startswith('http') and 'google' not in link_str):
                urlList.append(link_str)
                file.write(link_str + "\n")
                    
    file.close()

#Scrape texts from urls
def textScrape():
    #Open file
    parent = os.path.dirname(__file__)
    path = os.path.join(parent, "Data")
    fileName = os.path.join(path, "rianJohnsonURL.txt")
    file = open(fileName, 'r')
    urlLine = file.readlines()

    #Obtain text from the website
    fileNum = 0
    for url in urlLine:
        html = request.urlopen(re.sub(r'[\n]', '', url)).read().decode('utf8')
        soup = BeautifulSoup(html,"lxml")

        #Remove script and style elements
        for script in soup(["script", "style"]):
            script.extract()
        
        #Get text without newlines and tabs
        text =  re.sub(r'[\r\t\n]', '', soup.get_text());
        
        #Writes text to file
        fileName = "rianJohnson" + str(fileNum) + ".txt"
        fullPath = os.path.join(path, fileName)
        txtFile = open(fullPath, 'w')
        txtFile.write(text)
        txtFile.close()
        fileNum += 1

    file.close()
    return fileNum

#Sentence tokenizes each file
def sentTokenizer(fileNum):
    #Get data folder
    parent = os.path.dirname(__file__)
    folder = os.path.join(parent, "Data")

    #Go through each file
    for num in range(fileNum):
        #Open and reads file
        fileName = "rianJohnson" + str(num) + ".txt"
        file = open(os.path.join(folder, fileName), "r")
        text = file.read()
        file.close()

        #Tokenize sentences
        sentences = sent_tokenize(text)

        #Writes tokens to a file
        fileName = "rianJohnsonSent" + str(num) + ".txt"
        file = open(os.path.join(folder, fileName), "w")
        
        for s in sentences:
            file.write("%s\n" % s)

        file.close()

#Extract important terms
def importantTerms(fileNum):
    #Get data folder
    parent = os.path.dirname(__file__)
    folder = os.path.join(parent, "Data")

    #Get term frequency
    termFreq = {}
    for num in range(fileNum):
        #Open File
        fileName = "rianJohnsonSent" + str(num) + ".txt"
        file = open(os.path.join(folder, fileName), "r")

        #Read Lines
        lines = file.readlines()
        for l in lines:
            #Preprocess text
            text = re.sub(r'[\W\d_]',' ', l.lower())
            stop_words = set(stopwords.words('english'))
            tokens = word_tokenize(text)
            tokens = [t for t in tokens if not t in stop_words]

            #Add each token and count frequency
            for t in tokens:
                if t not in termFreq.keys():
                    termFreq[t] = 1
                else:
                    termFreq[t] += 1

        
        file.close()

    return termFreq
    

if __name__ == "__main__":
    main()