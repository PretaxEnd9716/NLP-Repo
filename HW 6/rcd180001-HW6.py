from cgitb import text
from bs4 import BeautifulSoup
import requests
import re
from urllib import request
import os

def main():
    #Make folder to store data
    folder = "Data"
    mode = 0o666
    parent = os.path.dirname(__file__)
    path = os.path.join(parent, folder)
    if not os.path.exists(path):
        os.mkdir(path)

    webCrawler()
    textScrape()

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
        if 'Rian' in link_str or 'rian' in link_str or 'imdb' in link_str or 'instagram' not in link_str:
            if link_str.startswith('/url?q='):
                link_str = link_str[7:]
            if '&' in link_str:
                i = link_str.find('&')
                link_str = link_str[:i]
            if (link_str not in urlList) and (link_str.startswith('http') and 'google' not in link_str and 'mashable' not in link_str and 'instagram' not in link_str):
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
        print(url)
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

    

if __name__ == "__main__":
    main()