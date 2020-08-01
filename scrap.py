import sys
import requests
from pprint import pprint
from bs4 import BeautifulSoup
import os
import time
import random
import argparse
from datetime import datetime
CWD = os.getcwd() + "/subs/"
BASE_URL = "https://kitsunekko.net"
URL = "https://kitsunekko.net/dirlist.php?dir=subtitles/japanese/&sort=date&order=desc"

def newShow(showTitle,websiteDate):
    ''' 
        returns TRUE if the website has a newer version of the folder 
        or if the show doesn't exist on your computer
    '''
    lastModified = datetime.strptime(time.ctime(os.path.getmtime(CWD+"/"+showTitle)),"%a %b %d %H:%M:%S %Y")
    websiteDate = datetime.strptime(websiteDate,"%b %d %Y %I:%M:%S %p")
    #if showTitle == "Ace of Diamond Act II": print(websiteDate>lastModified), sys.exit()
    # past < present ==> TRUE
    return websiteDate > lastModified

def getNumberOfFiles(folderName='.'):
    if folderName != '.': folderName = CWD + folderName
    '''
        returns the number of the files (only files) of the current working directory
    '''
    return len([name for name in os.listdir(folderName) if os.path.isfile(name)])

def getter(url):
    return requests.get(url)

def downloader(link,fileName,fileSize):
    '''
        Downloads the file if it doesn't exist and sleeps for a second after 
        it has done downloading
    '''
    if os.path.isfile(fileName) and (os.stat(fileName).st_size == fileSize):
        print(fileName,"exists, skipping it")
    else:
        print("Downloading",fileName,"to",os.getcwd())
        r = getter(BASE_URL+link)
        with open(fileName,"wb") as f:
            f.write(r.content)
        print("Sleeping")
        time.sleep(1)

def createFolder(directory,check=False):
    '''
        Creates a directory if doesn't exist and 
        chdirs into it when check is True
    '''
    if not os.path.exists(directory):
        try: 
            os.makedirs(directory)
        except OSError as e:
            print(e)
            sys.exit()
    if check:
        os.chdir(directory)

def findRows(requestResponse):
    '''
        Finds the rows and encapuslates the data into a list
        FORMAT ==> [name of the show/file,link,date on the website,size of the file]
    '''
    soup = BeautifulSoup(requestResponse.content, 'html.parser')
    table = soup.find("table")
    data = []
    rows = table.find_all('tr')
    for row in rows:
        cols = row.find_all('td')
        size = 0
        for ele in cols:
            if ele.find('a') is not None:
                link = ele.find('a')['href']
                if link[0] != "/":
                    link = "/" + link
                title = ele.text.strip()
            else:
                if ele['class'] == ['tdright']:
                    date = ele['title']
                elif ele['class'] == ['tdleft']:
                    size = ele['title']
        data.append([title,link,date,size])
    return data
    
def removeShows(showInformation):
    finalList = []
    for show in showInformation:
        title,_,date,_ = show
        if newShow(title,date):
            finalList.append(show)
        else:
            print("Removing",title,"from the queue")
    return finalList

parser = argparse.ArgumentParser()
parser.add_argument("--sync", help="changes the mode to sync mode",
                    action="store_true")
args = parser.parse_args()
createFolder('subs',True)