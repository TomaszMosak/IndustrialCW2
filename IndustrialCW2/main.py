import matplotlib.pyplot as plt
import matplotlib.mlab as lab
import json
import sys
import re
import pycountry
import numpy as np
import tkinter as tkr
from tkinter import * #IMPORTS ALL GUI COMPONENTS
from pycountry_convert import country_alpha2_to_continent_code, country_name_to_country_alpha2
import graphviz as graph
import click
from graphviz import Digraph as diG
import os

# Suggestion: Move this data into a 'User' class in order to use more advanced lang. features - Cory
userData = dict()

@click.command()
@click.option('-g', is_flag=True, help="Include following: '-g' for GUI. Optional Command")
@click.option('-u', default=None, help="Include following: '-u Visitor UUID'. Optional Command")
@click.option('-d', default=None, help="Include following: '-d Document UUID'. Required Command")
@click.option('-t', default="", required=True, help="Include following '-t Task ID'. Required Command \tCan be one of the following: 2a, 2b, 3, 4, 5, 6")
@click.option('-f', default="", required=True, help="Include following '-f Filename' Required Command")
def runFromTerminal(g:str,u:str,d:str,t:str,f:str):
    if g:
        GUI()
    if f == "":
        print('Error: File Location not specified')
    else:
        try:
            readJSON(f)
            whatTask(t,d,u)
        except:
            print('Error: Use --help to find required format')


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

def createGraph(dictionary):
    x = list(dictionary.keys())
    plt.bar(x, height=list(dictionary.values()))
    plt.xticks(x, x)
    plt.show()


#TASK2A START
def countryCount(documentID):
    userCountryCode = dict()
    for country in range(0, len(userData)):
        if 'visitor_country' in userData[country] and 'env_doc_id' in userData[country]:
            if userData[country]['env_doc_id'] == documentID:
                dictKey = userData[country]['visitor_country']
                if dictKey in userCountryCode:
                    userCountryCode[dictKey] += 1
                else:
                    userCountryCode[dictKey] = 1
    return userCountryCode


#TASK2A END

#TASK2B START
def continentCount(documentID):
    userContinentCode = dict()
    continents = {
    'NA': 'North America',
    'SA': 'South America',
    'AS': 'Asia',
    'OC': 'Australia',
    'AF': 'Africa',
    'EU': 'Europe'
}
    for country in range(0, len(userData)):
            try:
                if userData[country]["visitor_country"] == 'ZZ':
                    continent = 'UNKNOWN'
                elif userData[country]['visitor_country'] == 'AP': #Asia/Pacific Region
                    continent = 'Asia'
                elif userData[country]['visitor_country'] in continents.keys():
                    continent = userData[country]['visitor_country']
                else:
                    continent = continents[country_alpha2_to_continent_code(userData[country]['visitor_country'])]
            except:
                continent = 'NOT ISO3166'
            if 'env_doc_id' in userData[country]:
                if userData[country]['env_doc_id'] == documentID:
                    dictKey = continent
                    if dictKey in userContinentCode:
                        userContinentCode[dictKey] += 1
                    else:
                        userContinentCode[dictKey] = 1
    return userContinentCode

#TASK2B END

#TASK 3 START

    # Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/51.0.2704.103 Safari/537.36 ---> CHROME
    # Mozilla/5.0 (Macintosh; Intel Mac OS X x.y; rv:42.0) Gecko/20100101 Firefox/42.0 ---> Firefox
    # Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/51.0.2704.106 Safari/537.36 OPR/38.0.2220.41 ---> OPERA
    # Mozilla/5.0 (iPhone; CPU iPhone OS 10_3_1 like Mac OS X) AppleWebKit/603.1.30 (KHTML, like Gecko) Version/10.0 Mobile/14E304 Safari/602.1 ---> SAFARI
    # Mozilla/5.0 (compatible; MSIE 9.0; Windows Phone OS 7.5; Trident/5.0; IEMobile/9.0) ---> INTERNET EXPLORER
def browserCount(documentID):
    browser = ""
    browserCountDict = dict()
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

                if browser == "":
                    browser = "Other Browser"
                if browser in browserCountDict:
                    browserCountDict[browser] += 1
                else:
                    browserCountDict[browser] = 1
    return browserCountDict

#TASK 3 END

#TASK 4 START

def getReaders(documentID):
    #userData -> json
    readers = list()
    for i in range(0, len(userData)):
        if 'env_doc_id' in userData[i] and 'visitor_uuid' in userData[i]:
            if userData[i]['env_doc_id'] == documentID and userData[i]['visitor_uuid'] not in readers:
                    readers.append(userData[i]['visitor_uuid'])
    return readers


def getDocuments(visitorID):
    documents = list()
    for i in  range(0, len(userData)):
        if 'env_doc_id' in userData[i] and 'visitor_uuid' in userData[i]:
            if userData[i]['visitor_uuid'] == visitorID and userData[i]['env_doc_id'] not in documents:
                    documents.append(userData[i]['env_doc_id'])
    return documents

def alsoLikes(documentID, visitorID: str = None):
    documentsList = []
    docCount = []
    if visitorID is None:
        for visitor in getReaders(documentID):
            for document in getDocuments(visitor):
                documentsList.append(document)
    else:
        for document in getDocuments(visitorID):
            documentsList.append(document)

    while documentID in documentsList:
        documentsList.remove(documentID)

    for document in documentsList:
        docCount.append((document, documentsList.count(document)))
    print(sorted(list(dict.fromkeys(docCount)), key=lambda x: x[1], reverse=True))
    return sorted(list(dict.fromkeys(docCount)), key=lambda x: x[1], reverse=True)

def alsoLikesTop10(documentID, visitorID: str = None):
    return alsoLikes(documentID, visitorID)[:10]

#TASK 4 END

#TASK 5 START

def alsoLikesList(documentID, visitorID: str = None):
    visitors = []
    resultList = []
    if visitorID is None:
        for visitor in getReaders(documentID):
            for document in getDocuments(visitor):
                visitors.append((document, visitor))
    else:
        for visitor in getReaders(documentID):
            if visitor == visitorID:
                visitors.append((documentID, visitor))
            else:
                for document in getDocuments(visitor):
                    visitors.append((document, visitor))
    for i in range(0, len(visitors)):
        if visitors[i][0] in dict(resultList).keys():
            for r in resultList:
                if r[0] == visitors[i][0]:
                    r[1].append(visitors[i][1])
        else:
            resultList.append((visitors[i][0], [visitors[i][1]]))
    return sorted(resultList, key=lambda x: len(x[1]), reverse=True)

def alsoLikesGraph(documentID, visitorID: str = None):
    tupleList = alsoLikesList(documentID, visitorID)

    tupleListIndex = []

    for i in range(0, len(tupleList)):
        tempList = []
        for visitor in tupleList[i][1]:
            tempList.append(visitor)
        tupleListIndex.append(tempList)
    allVisits = []

    for Visits in tupleListIndex:
        for entry in Visits:
            allVisits.append(entry)
    for visitor in allVisits:
        counter = allVisits.count(visitor)
        if counter == 1:
            allVisits.remove(visitor)


    g = diG(comment='Visitors also liked...', strict=True)
    for entry in tupleList:
        document = entry[0]

        g.node(document, document[-4:], shape="circle", style="filled", color="lightpink")

        for visitor in entry[1]:
            if f"\t{visitor}" not in g.body and visitor in allVisits:
                g.node(visitor, visitor[-4:], shape="box", style="filled", color="lightskyblue")
                g.edge(visitor, document)

    g.node(documentID, documentID[-4:], color="green", style="filled")
    if visitorID is not None:
        g.node(visitorID, visitorID[-4:], color="green", style="filled")
        g.edge(visitorID, documentID)

    g.node(tupleList[1][0], tupleList[1][0][-4:], shape="circle", style="filled", color="red")
    return g
#TASK 5 END

#TASK 6 - GUI
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

    fileLoc = tkr.Button(mainframe,
                   text="Choose File",
                   command= lambda:  fileLocation.set(filedialog.askopenfilename(initialdir = os.path.dirname(os.path.abspath(__file__))
                   ,title = "Select file",filetypes = (("json files","*.json"),("all files","*.*"))))
    )
    fileLoc.grid(column=1, row=1, sticky=(W, E))
    tkr.Label(mainframe, text="File Location").grid(column=0, row=1, sticky=W)

    docName = tkr.Entry(mainframe, width=40, textvariable=documentID)
    docName.grid(column=1, row=3, sticky=(W, E))
    tkr.Label(mainframe, text="Document UUID").grid(column=0, row=3, sticky=W)

    visitorName = tkr.Entry(mainframe, width=40, textvariable=visitorID)
    visitorName.grid(column=1, row=4, sticky=(W, E))
    tkr.Label(mainframe, text="Visitor UUID").grid(column=0, row=4, sticky=W)


    choices = [ 'Views by Country','Views by Continent','Views by Browser','Also Like','Also Like - Graph']
    task.set('Views by Country') # set the default option
    popupMenu = OptionMenu(mainframe, task, *choices)
    Label(mainframe, text="Choose a Task").grid(row = 2, column = 0, sticky=W)
    popupMenu.grid(row = 2, column =1)
    fileLocation.trace("w", lambda name, index, mode, fileN=fileLocation: readJSON(fileN.get()))
    button = tkr.Button(mainframe, text="Run task!", command= lambda: whatTask(task.get(), documentID.get(), visitorID.get()))
    button.grid(row = 5, column =1)
    for child in mainframe.winfo_children():
        child.grid_configure(padx=5, pady=5)

    base.mainloop()

def whatTask(task, documentID, visitorID):
    if visitorID == "":
        visitorID = None
    if documentID == "":
        documentID = None

    if task == 'Views by Country' or task == '2a':
        createGraph(countryCount(documentID))
    if task == 'Views by Continent' or task == '2b':
        createGraph(continentCount(documentID))
    if task == 'Views by Browser' or task == '3':
        createGraph(browserCount(documentID))
    if task == 'Also Like' or task == '4':
        for likes in alsoLikesTop10(documentID, visitorID):
            print(likes)
        # TEST DOC_ID ------- "130325130327-d5889c2cf2e642b6867cb9005e12297f"
    if task == 'Also Like - Graph' or task == '5':
        grh = alsoLikesGraph(documentID, visitorID)
        grh.render("alsoLikesGraph.ps", view=True)
    if task == '6':
        GUI()
    else:
        print('Error: No valid task selected.')
#TASK 6 END - GUI

def main():
    runFromTerminal()
# CHECK IF THIS IS MAIN FILE
if __name__ == "__main__":
    main()
