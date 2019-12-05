from tkinter import messagebox, filedialog
import matplotlib.pyplot as plt
import matplotlib.mlab as lab
import json
import sys
import re
import numpy as np
import tkinter as tkr
from tkinter import * #IMPORTS ALL GUI COMPONENTS
from pycountry_convert import country_alpha2_to_continent_code, country_name_to_country_alpha2
import graphviz as graph
import click as c
from graphviz import Digraph as diG
import os

os.environ["PATH"] += os.pathsep + r'C:\Program Files (x86)\release\bin' #PATH TO FILE TO THE GRAPHVIZ

userData = dict()

#This allows the user to use the terminal for the coursework. Task 7.
#Useful as it allows the user to type --help
@c.command()
@c.option('-g', is_flag=True, help="Include following: '-g' for GUI. Optional Command")

#REQUIRED FORMAT -u, -d, -t, -f
@c.option('-u', default=None, help="Include following: '-u Visitor UUID'. Optional Command")
@c.option('-d', default=None, help="Include following: '-d Document UUID'. Required Command")
@c.option('-t', default="", required=True, help="Include following '-t Task ID'. Required Command. Tasks: 2a, 2b, 3a, 3b, 4, 5, 6")
@c.option('-f', default="", required=True, help="Include following '-f Filename' Required Command")


def runFromTerminal(g:str,u:str,d:str,t:str,f:str):
    """
    Either creates a GUI for the user to use or takes the user input from terminal to complete tasks
    """
    if g:
        task6 = GUIClass()
        task6.GUI()
    else:
        try:
            readJSON(f)
            whatTask(t,d,u)
        except:
            print('Input Error: Use --help to find required format')


#USE THIS WITH ANY TASKS TO READ THE JSON FILE AND POPULATE userData dictionary
def readJSON(fileLocation):
    """
    Reads the input file and populates the userData Dictionary
    :param fileLocation: JSON file
    """
    print('Attempting to read JSON data from file', fileLocation)

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
    """
    Draws a matplotlib histogram with the use of the input Dictionary
    |Key - X Axis| |Value - Y Axis|
    :param dictionary : Dictionary to be displayed to user
    """
    data = list(dictionary.keys())
    plt.bar(data, height=list(dictionary.values()))
    plt.xticks(data, data)
    plt.show()

class Countries:
    # TASK2A START

    def countryCount(documentID):
        """
        Counts how many occurances of each contry appear for the given document
        :param documentID : Document UUID
        :return : Dictionary of countries and amount of occurances
        """
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

    # TASK2A END

    # TASK2B START
    def continentCount(documentID):
        """
        Counts how many occuraranes of each continent appear for the given document
        :param documentID : Document UUID
        :return : Dictionary of contienets and amount of occurances
        """
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
                elif userData[country]['visitor_country'] == 'AP':  # Asia/Pacific Region
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

    # TASK2B END


#TASK 3 START
class Browsers():

    def browserCountA(userData):
        """
        Counts occurances of each browser which displayed the input document
        :param documentID : Document UUID
        :return : Dictionary of browser names and amount of occurances
        """
        browser = ""
        browserCountDict = dict()
        for i in range(0, len(userData)):

            if 'visitor_useragent' in userData[i] and 'env_doc_id' in  userData[i]:
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

    def browserCountB(documentID):
        """
        Counts occurances of each browser which displayed the input document
        :param documentID : Document UUID
        :return : Dictionary of browser names and amount of occurances
        """
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

class AlsoLikes:

    def getReaders(documentID):
        """
        Finds all unique visitor UUIDs that read the input Document
        :param documentID : Document UUID
        :return : List of visitor UUIDs
        """
        readers = list()
        for i in range(0, len(userData)):
            if 'env_doc_id' in userData[i] and 'visitor_uuid' in userData[i]:
                if userData[i]['env_doc_id'] == documentID and userData[i]['visitor_uuid'] not in readers:
                        readers.append(userData[i]['visitor_uuid'])
        return readers

    def getDocuments(visitorID):
        """
        Finds all unique document UUIDs that the user has read
        :param visitorID : Visitor UUID
        :return : List of Document UUIDs
        """
        documents = list()
        for i in  range(0, len(userData)):
            if 'env_doc_id' in userData[i] and 'visitor_uuid' in userData[i]:
                if userData[i]['visitor_uuid'] == visitorID and userData[i]['env_doc_id'] not in documents:
                        documents.append(userData[i]['env_doc_id'])
        return documents

    def alsoLikes(documentID, visitorID: str = None):
        """
        Fetches which documents have also been read by users who read the input document. If a user is
        specified, only fetches documents read by that user
        :param documentID : Document UUID
        :param visitorID : Visitor UUID
        :return : Ordered list of Document UUIDs which also were read by visitors of the input Document UUID
        """
        documentsList = []
        docCount = []
        if visitorID is None:
            for visitor in AlsoLikes.getReaders(documentID):
                for document in AlsoLikes.getDocuments(visitor):
                    documentsList.append(document)
        else:
            for document in AlsoLikes.getDocuments(visitorID):
                documentsList.append(document)

        while documentID in documentsList:
            documentsList.remove(documentID)

        for document in documentsList:
            docCount.append((document, documentsList.count(document)))
        print(sorted(list(dict.fromkeys(docCount)), key=lambda x: x[1], reverse=True))
        return sorted(list(dict.fromkeys(docCount)), key=lambda x: x[1], reverse=True)

#TASK 4 END

#TASK 5 START
class GraphAlsoLikes:
    def alsoLikesList(documentID, visitorID: str = None):
        """
        Creates a list of tuples, Tuple{|First element = documentUUID| |Second element = visitorUUID|}
        :param documentID : Document UUID
        :param visitorID : Visitor UUID
        :return : Ordered tuple containing lists of document + visitor UUID
        """

        visitors = []
        resultList = []
        if visitorID is None:
            for visitor in AlsoLikes.getReaders(documentID):
                for document in AlsoLikes.getDocuments(visitor):
                    visitors.append((document, visitor))
        else:
            for visitor in AlsoLikes.getReaders(documentID):
                if visitor == visitorID:
                    visitors.append((documentID, visitor))
                else:
                    for document in AlsoLikes.getDocuments(visitor):
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
        """
        Creates a graph showing the connections between documents read by visitors of the input document
        in dot format
        :param documentID : Document UUID
        :param visitorID : visitor UUID
        :return : Digraph (can be rendered)
        """
        try:
            tupleList = GraphAlsoLikes.alsoLikesList(documentID, visitorID)

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
        except:
            print("Index Error: Failed to Draw Graph. Incorrect Input.")

#TASK 5 END

#TASK 6 - GUI
class GUIClass:
    def GUI(self):
        """
        Draws and Displays a GUI which supports the run of any tasks selected by the user
        """

        def errorGUI():
            """
            Popup error message, allows the user to know they forgot a required field
            """
            messagebox.showinfo('ERROR', 'Empty REQUIRED Input: Try Again')

        def validInput():
            """
            Makes sure that all the REQUIRED fields have been populated
            """
            inputs = []

            if task.get() == '3a' or task.get() == 'All views by Browser':
                inputs = [task.get(), fileLocation.get()]
            else:
                inputs = [task.get(), documentID.get(), fileLocation.get()]

            for local_input in inputs:
                if local_input == "":
                    return False
            return True

        base = Tk()
        base.title("Cory's and Tomasz's Coursework2 GUI")

        mainframe = tkr.Frame(base)
        mainframe.grid(column=0, row=0, sticky=(N, W, E, S)) #SETS EVERYTHING INTO GRID FORMAT. SIMILAR TO BOOTSTRAP IN WEB DEVELOPMENT
        base.columnconfigure(0, weight=1)
        base.rowconfigure(0, weight=1)

        fileLocation = StringVar()
        documentID = StringVar()
        visitorID = StringVar()
        task = StringVar(base)
        task.set("Task X") # default value

        #Creates a GUI to find the dataset
        fileLoc = tkr.Button(mainframe, text="Choose JSON Input File", command= lambda:  fileLocation.set(filedialog.askopenfilename(initialdir = os.path.dirname(os.path.abspath(__file__)), title = "Select file",filetypes = (("json files","*.json"),("all files","*.*")))))
        fileLoc.grid(column=1, row=1, sticky=(W, E))
        tkr.Label(mainframe, text="File Location").grid(column=0, row=1, sticky=W)

        docName = tkr.Entry(mainframe, width=40, textvariable=documentID)
        docName.grid(column=1, row=3, sticky=(W, E))
        tkr.Label(mainframe, text="Document UUID").grid(column=0, row=3, sticky=W)

        visitorName = tkr.Entry(mainframe, width=40, textvariable=visitorID)
        visitorName.grid(column=1, row=4, sticky=(W, E))
        tkr.Label(mainframe, text="Visitor UUID").grid(column=0, row=4, sticky=W)


        choices = [ 'Views by Country','Views by Continent','All views by Browser', 'Views by Browser','Also Like','Also Like - Graph']
        task.set('Views by Country') # set the default option
        popupMenu = OptionMenu(mainframe, task, *choices)
        Label(mainframe, text="Choose a Task").grid(row = 2, column = 0, sticky=W)
        popupMenu.grid(row = 2, column =1)
        #automatically updates the dataset to the user choice
        fileLocation.trace("w", lambda name, index, mode, fileN=fileLocation: readJSON(fileN.get()))
        button = tkr.Button(mainframe, width=20, text="RUN IT!", command= lambda: whatTask(task.get(), documentID.get(), visitorID.get()) if validInput() == True else errorGUI())
        button.grid(row = 5, column =1)
        for child in mainframe.winfo_children():
            child.grid_configure(padx=5, pady=5)

        base.mainloop()

#TASK 6 END - GUI

def whatTask(task, documentID, visitorID):

    """
    Based on GUI or Terminal user input runs the chosen task
    :param task : Task name
    :param documentID : Document UUID
    :param visitorID : VisitorUUID
    """

    if visitorID == "":
        visitorID = None
    if documentID == "":
        documentID = None

    if task == 'Views by Country' or task == '2a':
        createGraph(Countries.countryCount(documentID))
    if task == 'Views by Continent' or task == '2b':
        createGraph(Countries.continentCount(documentID))
    if task == 'All views by Browser' or task == '3a':
        createGraph(Browsers.browserCountA(userData))
    if task == 'Views by Browser' or task == '3b':
        createGraph(Browsers.browserCountB(documentID))
    if task == 'Also Like' or task == '4':
        top10 = AlsoLikes.alsoLikes(documentID, visitorID)[:10]
        for likes in top10:
            print(likes)
        # TEST DOC_ID ------- "130325130327-d5889c2cf2e642b6867cb9005e12297f"
    if task == 'Also Like - Graph' or task == '5':
        grh = GraphAlsoLikes.alsoLikesGraph(documentID, visitorID)
        grh.render("alsoLikesGraph.ps", view=True)
    if task == '6':
        GUIClass.GUI()


#________________________________________
# Main
#¯¯¯¯¯¯¯¯¯¯¯¯¯¯¯¯¯¯¯¯¯¯¯¯¯¯¯¯¯¯¯¯¯¯¯¯¯¯¯¯
def main():
    runFromTerminal()


if __name__ == "__main__":
    main()
#________________________________________
# Main
#¯¯¯¯¯¯¯¯¯¯¯¯¯¯¯¯¯¯¯¯¯¯¯¯¯¯¯¯¯¯¯¯¯¯¯¯¯¯¯¯
