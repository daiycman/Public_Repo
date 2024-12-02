##########################################################################################################################
# Script Name: FMC Change Network and Host Names
# Author: Joe Smith
# Date: 2022-10-14
# Description: This script utilizes the Cisco FMC API's to read through a CSV of FMC Objects that have updated names
#             From a previously pulled report from FMC APIs. For each record in the CSV it will set the new name to the
#             JSON body with the FMC Object ID to update the name within the FMC.
#             This script is not utilizing the fireREST library. The token request functionality can be replaced with that
##########################################################################################################################

# importing needed libraries
import requests
import json
import csv
from requests.auth import HTTPBasicAuth
import getpass
import urllib3


urllib3.disable_warnings(urllib3.exceptions.InsecureRequestWarning)



# Setting the variables that are needed for the script. Fill out with the information of the desired FMC
deviceURLorIP = ""
username = ""
# will prompt the CLI for an entry of the password for the username provided. This will not be shown on the CLI
password = getpass.getpass()
# File location with the file name ex:C:\\Users\\FoldertoWhateverLocation\\CSV.csv'
fileDirectory = f''

# Because we are not using the firerest Library we need to handle the access token manually 
generateTokenURL = 'https://' + deviceURLorIP + '/api/fmc_platform/v1/auth/generatetoken'

# posting the username and password to get an access token
tokenRequest = requests.post(generateTokenURL, verify=False, auth=HTTPBasicAuth(username,password))

# setting the variables from the request with the access token
access_token = tokenRequest.headers["X-auth-access-token"]
refresh_token = tokenRequest.headers["X-auth-refresh-token"]
domainUUID = tokenRequest.headers["DOMAIN_UUID"]

tokenRequest.close

# creating headers with the valid access token
headers = {
    "X-auth-access-token": access_token,
    "content-type": "application/json",
    "Accept": "*/*"
}

# opening the file where the network/host names are located
csvFILE = open(fileDirectory, newline='')

csvWriter = csv.DictReader(csvFILE, delimiter=',')

# loop through the rows of the CSV to grab the new name of the network object to update
for items in csvWriter:

    if items['type'] == 'Network':

        networkaddressURL = 'https://' + deviceURLorIP + '/api/fmc_config/v1/domain/' + domainUUID + '/object/networks/' + items['id']

        jsonBody = {

            "value": items['value'],
            "id": items['id'],
            "name": items['name']

        }

        networkaddressRequest = requests.put(networkaddressURL, data= json.dumps(jsonBody), verify=False, headers=headers)

        print(networkaddressRequest)

    elif items['type'] == 'Host':
        
        networkaddressURL = 'https://' + deviceURLorIP + '/api/fmc_config/v1/domain/' + domainUUID + '/object/hosts/' + items['id']

        jsonBody = {

            "value": items['value'],
            "id": items['id'],
            "name": items['name']

        }

        networkaddressRequest = requests.put(networkaddressURL, data= json.dumps(jsonBody), verify=False, headers=headers)

        print(networkaddressRequest)



# closing the file
csvFILE.close()
