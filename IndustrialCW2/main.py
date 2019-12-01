import matplotlib.pyplot as plt
import json
import sys
import re
import pycountry
from pycountry_convert import country_alpha2_to_continent_code, country_name_to_country_alpha2

# Suggestion: Move this data into a 'User' class in order to use more advanced lang. features - Cory
userData = dict()
userCountryCode = dict()
userContinentCode = dict()
browserCountDict = dict()

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
                if "MSIE" in userData[i]['visitor_useragent']:
                    browser = "Internet Explorer"
                if "Safari" in userData[i]['visitor_useragent']:
                    browser = "Safari"
                    if "Chrome" in userData[i]['visitor_useragent']:
                        browser = "Chrome"
                        if "OPR" in userData[i]['visitor_useragent']:
                            browser = "Opera"

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
            continent = continents[country_alpha2_to_continent_code(userData[country]['visitor_country'])]
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

def task2A():
    documentID = "131203154832-9b8594b7ec211f7e1a0782fd9883a42c"
    #documentID = input("Enter the document ID: ") ------- UNCOMMENT ONCE FINISHED TESTING
    countryCount(documentID)
    countryPrint()

def task2B():
    documentID = "131203154832-9b8594b7ec211f7e1a0782fd9883a42c"
    continentCount(documentID)
    continentPrint()

def task3():
    #documentID = "131203154832-9b8594b7ec211f7e1a0782fd9883a42c"
    documentID = "140213050612-d83f236552a901d6cb841455905805cc"
    browserCount(documentID)
    browserPrint()

def main():
    #Do this for all tasks
    fileLocation = input("Enter JSON datset file location: ")
    readJSON(fileLocation)

    #task2A()
    #task2B()
    task3()

# CHECK IF THIS IS MAIN FILE
if __name__ == "__main__":
    main()
