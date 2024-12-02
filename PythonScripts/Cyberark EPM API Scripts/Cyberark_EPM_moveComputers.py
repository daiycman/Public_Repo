##########################################################################################################################
# Script Name: Cyberark EPM move computers
# Author: Joe Smith
# Date: 2023-10-10
# Description: This script utilizes the Cyberark EPM APIs to move computers from one set to another by each computers GUID
#              Which is pulled from other reports from whatever set you want to move the computers from
##########################################################################################################################

import requests
import getpass
import os
import json
import urllib3
from requests.auth import HTTPBasicAuth
from datetime import datetime
import csv
urllib3.disable_warnings(urllib3.exceptions.InsecureRequestWarning)

# Setting basic variables for the script **Change the setID when moving to the main set with 3e9c9337-56aa-4b2e-a449-f24d9173cd21
logonURL = 'https://login.epm.cyberark.com/EPM/API/Auth/EPM/Logon'
setID = ""
movetoSetID = ""
allguids = []

# File location with the file name ex:C:\\Users\\FoldertoWhateverLocation\\CSV.csv'
fileDirectory = r''

# Creating JSON body for logging in
password = getpass.getpass()

userNamepassWord = {

    "Username": "",

    "Password": password,

    "ApplicationID": "**your group ID**"
}

# Logging into CybearkEPM and grabbing the authentication token and storing into a variable for other
tokenRequest = requests.post(logonURL, verify=False, json=userNamepassWord)

tokenRequest.close

tokenRequest = tokenRequest.json()

authToken = "basic " + tokenRequest['EPMAuthenticationResult']

moveComputerNameURL = 'https://na000.epm.cyberark.com/EPM/API/Sets/' + setID + '/Computers/RedirectAgents'

# Creating authentication Token JSON header
headers = {
    "Authorization": authToken

}

csvFILE = open(fileDirectory, newline='')

csvWriter = csv.DictReader(csvFILE, delimiter=',')

for items in csvWriter:

    allguids.append(str(items['Guid']))

print(allguids)

jsonBody = {
"computerIds": allguids,
"destSetId": movetoSetID
}

moveMachinesRequest = requests.post(moveComputerNameURL, json=jsonBody, verify=False, headers=headers)

print(moveMachinesRequest)

csvFILE.close()