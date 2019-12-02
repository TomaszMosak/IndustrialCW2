import matplotlib.pyplot as plt
import json
import sys
import re
import pycountry
import numpy as np
import tkinter as tkr
from tkinter import * #IMPORTS ALL GUI COMPONENTS
from pycountry_convert import country_alpha2_to_continent_code, country_name_to_country_alpha2

# Suggestion: Move this data into a 'User' class in order to use more advanced lang. features - Cory
userData = dict()
userCountryCode = dict()
userContinentCode = dict()
browserCountDict = dict()
documentReaderDict = dict()
userReadDict = dict()


#USE THIS WITH ANY TASKS TO READ THE JSON FILE AND POPULATE userData dictionary
def readJSON(fileLocation):
    print('Reading JSON data from file', fileLocation)

    with open(fileLocation) as inputFile:
        jsonData = inputFile.read()
        #EACH ENTRY IS EVERYTHING BETWEEN { }
        inputArray = (input.group() for input in re.finditer(r'{.*}', jsonData))

        #initialize counter for the amount of users to index the users
        i = 0
        #Split the JSON data into a dictionary of each user
        for input in inputArray:
            currUser = json.loads(input)
            userData[i] = currUser
            i += 1

    print("The user dictionary has been successfully populated")

def getReaders(documentID):
    #userData -> json
    readers = list()
    for i in range(0, len(userData)):
        if 'env_doc_id' in userData[i] and 'visitor_uuid' in userData[i]:
            if userData[i]['env_doc_id'] == documentID:
                if not userData[i]['visitor_uuid'] in readers:
                    readers.append(userData[i]['visitor_uuid'])
    documentReaderDict[documentID] = readers
    return readers


def ReadDocuments(visitorID):
    documents = list()
    for i in  range(0, len(userData)):
        if 'env_doc_id' in userData[i] and 'visitor_uuid' in userData[i]:
            if userData[i]['visitor_uuid'] == visitorID:
                if not userData[i]['env_doc_id'] in documents:
                    documents.append(userData[i]['env_doc_id'])
    return documents

def alsoLikes(documentID):
    tempUsers = list()
    tempUsers = getReaders(documentID)
    tempDocs = list()
    outVal = list()
    for i in range(0, len(tempUsers)):
        tempDocs += ReadDocuments(tempUsers[i])

    retVal = dict()
    docIDs = []
    docReaders = []
    for i in range(0, len(tempDocs)):
        if tempDocs[i] not in docIDs:
            docIDs.append(tempDocs[i])
            docReaders.append(len(getReaders(tempDocs[i])))
    for i in range(0, len(docReaders)):
        for j in range(0, len(docReaders) - i):
            if(docReaders[i] > docReaders[j]):
                swap(docReaders, i, j)
                swap(docIDs, i, j)
    if(documentID in  docIDs):
        index = docIDs.index(documentID)
        docIDs.remove(documentID)
        del docReaders[index]

    for i in range(0, len(docIDs)):
        if docIDs[i] not in retVal.keys():
            retVal[docIDs[i]] = docReaders[i]


    return retVal

def swap(arr, i, j):
    temp = arr[j]
    arr[j] = arr[i]
    arr[i] = temp




    # Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/51.0.2704.103 Safari/537.36 ---> CHROME
    # Mozilla/5.0 (Macintosh; Intel Mac OS X x.y; rv:42.0) Gecko/20100101 Firefox/42.0 ---> Firefox
    # Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/51.0.2704.106 Safari/537.36 OPR/38.0.2220.41 ---> OPERA
    # Mozilla/5.0 (iPhone; CPU iPhone OS 10_3_1 like Mac OS X) AppleWebKit/603.1.30 (KHTML, like Gecko) Version/10.0 Mobile/14E304 Safari/602.1 ---> SAFARI
    # Mozilla/5.0 (compatible; MSIE 9.0; Windows Phone OS 7.5; Trident/5.0; IEMobile/9.0) ---> INTERNET EXPLORER
def browserCount(documentID):
    browser = ""
    for i in range(0, len(userData)):

        if 'visitor_useragent' in userData[i] and 'env_doc_id' in  userData[i]:
            if userData[i]['env_doc_id'] == documentID:
                if "Firefox" in userData[i]['visitor_useragent']:
                    browser = "Firefox"
                if "MSIE" in userData[i]['visitor_useragent'] or "Trident" in userData[i]['visitor_useragent']:
                    browser = "Internet Explorer"
                if "Opera" in userData[i]['visitor_useragent']:
                    browser = "Opera"
                if "Safari" in userData[i]['visitor_useragent']:
                    browser = "Safari"
                    if "Chrome" in userData[i]['visitor_useragent']:
                        browser = "Chrome"
                        if "OPR" in userData[i]['visitor_useragent']:
                            browser = "Opera"

                if browser = "":
                    browser = "Other Browser"
                if browser in browserCountDict:
                    browserCountDict[browser] += 1
                else:
                    browserCountDict[browser] = 1

def browserPrint():
    browsers = list(browserCountDict.keys())
    plt.bar(browsers, list(browserCountDict.values()))
    plt.xticks(browsers, browsers)
    plt.show()

#TASK2A START
def countryCount(documentID):
    for country in range(0, len(userData)):
        if 'visitor_country' in userData[country] and 'env_doc_id' in userData[country]:
            if userData[country]['env_doc_id'] == documentID:
                dictKey = userData[country]['visitor_country']
                if dictKey in userCountryCode:
                    userCountryCode[dictKey] += 1
                else:
                    userCountryCode[dictKey] = 1


def countryPrint():
    countries = list(userCountryCode.keys())
    plt.bar(countries, height=list(userCountryCode.values()))
    plt.xticks(countries, countries)
    plt.show()

#TASK2A END

#TASK2B START
def continentCount(documentID):
    continents = {
    'NA': 'North America',
    'SA': 'South America',
    'AS': 'Asia',
    'OC': 'Australia',
    'AF': 'Africa',
    'EU': 'Europe'
}
    for country in range(0, len(userData)):
        if userData[country]['visitor_country'] == 'ZZ':
            continent = 'UNKNOWN'
        elif userData[country]['visitor_country'] == 'AP': #Asia/Pacific Region
            continent = 'Asia'
        elif userData[country]['visitor_country'] in continents.keys():
            continent = userData[country]['visitor_country']
        else:
            continent = continents[country_alpha2_to_continent_code(userData[country]['visitor_country'])]
            if 'env_doc_id' in userData[country]:
                if userData[country]['env_doc_id'] == documentID:
                    dictKey = continent
                    if dictKey in userContinentCode:
                        userContinentCode[dictKey] += 1
                    else:
                        userContinentCode[dictKey] = 1

def continentPrint():
    continents = list(userContinentCode.keys())
    plt.bar(continents, height=list(userContinentCode.values()))
    plt.xticks(continents, continents)
    plt.show()
#TASK2B END

def GUI():
    base = Tk()
    base.title("Cory's and Tomasz's Coursework2")

    mainframe = tkr.Frame(base)
    mainframe.grid(column=0, row=0, sticky=(N, W, E, S)) #SETS EVERYTHING INTO GRID FORMAT. SIMILAR TO BOOTSTRAP IN WEB DEVELOPMENT
    base.columnconfigure(0, weight=1)
    base.rowconfigure(0, weight=1)

    fileLocation = StringVar()
    documentID = StringVar()
    visitorID = StringVar()
    task = StringVar(base)
    task.set("Task X") # default value

    fileLoc = tkr.Entry(mainframe, width=40, textvariable=fileLocation)
    fileLoc.grid(column=1, row=1, sticky=(W, E))
    tkr.Label(mainframe, text="File Location").grid(column=0, row=1, sticky=W)

    docName = tkr.Entry(mainframe, width=40, textvariable=documentID)
    docName.grid(column=1, row=3, sticky=(W, E))
    tkr.Label(mainframe, text="Document UUID").grid(column=0, row=3, sticky=W)

    visitorName = tkr.Entry(mainframe, width=40, textvariable=visitorID)
    visitorName.grid(column=1, row=4, sticky=(W, E))
    tkr.Label(mainframe, text="Visitor UUID").grid(column=0, row=4, sticky=W)


    choices = [ 'Task 2a','Task 2b','Task 3','Task 4','Task 5']
    task.set('Task 2a') # set the default option
    choices = sorted(choices)
    popupMenu = OptionMenu(mainframe, task, *choices)
    Label(mainframe, text="Choose a Task").grid(row = 2, column = 0, sticky=W)
    popupMenu.grid(row = 2, column =1)

    button = tkr.Button(mainframe, text="Run task!", command= lambda: whatTask(task.get(), documentID.get(), visitorID.get()))
    button.grid(row = 5, column =1)
    for child in mainframe.winfo_children():
        child.grid_configure(padx=5, pady=5)

#    fileLoc.focus()
    base.mainloop()

def whatTask(task, documentID, visitorID):
    if task == 'Task 2a':
        countryCount(documentID)
        countryPrint()
    if task == 'Task 2b':
        continentCount(documentID)
        continentPrint()
    if task == 'Task 3':
        browserCount(documentID)
        browserPrint()
    if task == 'Task 4':
        task4(documentID)
        # REALLY GOOD DOC_ID ------- "131224090853-45a33eba6ddf71f348aef7557a86ca5f"
    if task == 'Task 5':
        pass

def task2A():
    documentID = "131224090853-45a33eba6ddf71f348aef7557a86ca5f"
    #documentID = input("Enter the document ID: ") ------- UNCOMMENT ONCE FINISHED TESTING
    countryCount(documentID)
    countryPrint()

def task2B():
    documentID = "131224090853-45a33eba6ddf71f348aef7557a86ca5f"
    continentCount(documentID)
    continentPrint()

def task3():
    #documentID = "131203154832-9b8594b7ec211f7e1a0782fd9883a42c"
    documentID = "131224090853-45a33eba6ddf71f348aef7557a86ca5f"
    browserCount(documentID)
    browserPrint()

def task4(documentID):
    alsoDict = alsoLikes(documentID)
    docIDs = list(alsoDict.keys())
    for i in range(0, len(docIDs)):
        print("" + str(docIDs[i]) + " : " + str(alsoDict[docIDs[i]]))
    return docIDs[:10]

def main():
    #Do this for all tasks
    #fileLocation = input("Enter JSON datset file location: ")
    fileLocation = "datasets/issuu_final.json"
    readJSON(fileLocation)

    GUI()
    task2A()
    task2B()
    task3()
    task4()


# CHECK IF THIS IS MAIN FILE
if __name__ == "__main__":
    main()
