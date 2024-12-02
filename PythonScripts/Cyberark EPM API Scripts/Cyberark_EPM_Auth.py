##########################################################################################################################
# Script Name: Cyberark EPM get computers
# Author: Joe Smith
# Date: 2022-10-16
# Description: This script utilizes the Cyberark EPM APIs to pull a list of computers from the console
##########################################################################################################################

import requests
import json
import csv
from requests.auth import HTTPBasicAuth
import getpass
import urllib3


urllib3.disable_warnings(urllib3.exceptions.InsecureRequestWarning)



logonURL = 'https://login.epm.cyberark.com/EPM/API/Auth/EPM/Logon'
# File location with the file name ex:C:\\Users\\FoldertoWhateverLocationToSave\\CSV.csv'
fileDirectory = r''
password = getpass.getpass()

userNamepassWord = {

    "Username": "",

    "Password": password,

    "ApplicationID": "**yourgroupName"
}

tokenRequest = requests.post(logonURL, verify=False, json=userNamepassWord)

print(tokenRequest)


tokenRequest.close

tokenRequest = tokenRequest.json()

authToken = "basic " + tokenRequest['EPMAuthenticationResult']

# setID = ""
setID = ""

getNetworksURL = 'https://na000.epm.cyberark.com/EPM/API/Sets/' + setID + '/Computers?offset=5000&limit=5000'

headers = {
    "Authorization": authToken

}

computers = requests.get(getNetworksURL, verify=False, headers=headers)

jsonobject1 = computers.json()

computers.close

csvFILE = open(fileDirectory, 'w', newline='')

csvWriter = csv.writer(csvFILE)

print(computers)

count = 0

for items in jsonobject1['Computers']:

    if count == 0:
 
        # Writing headers of CSV file
        csvheader = items.keys()
        csvWriter.writerow(csvheader)
        count += 1

    # Writing data of CSV file
    csvWriter.writerow(items.values())

csvFILE.close