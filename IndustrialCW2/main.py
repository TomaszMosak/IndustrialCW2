import matplotlib
import json
import sys
import re

userData = dict()
userCountryCode = dict()
userContinentCode = dict()

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




def main():
    fileLocation = input("Enter JSON datset file location: ")
    readJSON(fileLocation)



# CHECK IF THIS IS MAIN FILE
if __name__ == "__main__":
    main()
