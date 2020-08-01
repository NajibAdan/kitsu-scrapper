from scrap import createFolder,getter,findRows,removeShows,URL,BASE_URL,getNumberOfFiles,downloader,CWD
from datetime import datetime
import os
import time
def main():
    page = getter(URL)
    finalShows = findRows(page)
    for show in finalShows:
        showTitle,showLink,showDate,showSize = show
        print("Picking",showTitle,"from the queue.",finalShows.index(show)+1,"/",len(finalShows))
        createFolder(showTitle,True)
        if showSize != 0:
            downloader(showLink,showTitle,int(showSize))
        else:
            page = getter(BASE_URL+showLink)
            showData = findRows(page)
            numberOfFiles = getNumberOfFiles(showTitle)
            if numberOfFiles == len(showData):
                print('Skipping',showTitle)
            elif numberOfFiles > len(showData):
                # ADD A FUNCTION TO THE DELETE UNNECESSARY FILES
                with open("/home/lain/kitsu/files with a lot of files",'a') as f:
                    string = showTitle + " " + str(numberOfFiles) + " " + str(len(showData))+'\n'
                    f.write(string)
                pass
            else:
                for fileData in showData:
                    filename,link,_,fileSize = fileData
                    downloader(link,filename,int(fileSize))
        os.chdir(CWD)
if __name__ == "__main__":
    main()