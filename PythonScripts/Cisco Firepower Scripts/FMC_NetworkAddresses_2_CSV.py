##########################################################################################################################
# Script Name: FMC Gather Network Objects
# Author: Joe Smith
# Date: 2022-10-13
# Description: This script utilizes the Cisco FMC API's to print a CSV of FMC Network and Host objects
#             This script is not utilizing the fireREST library. The token request functionality can be replaced with that
##########################################################################################################################

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
# File location with the file name ex:C:\\Users\\FoldertoWhateverLocationToSave\\CSV.csv'
fileDirectory = r''

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
    "X-auth-access-token": access_token
}

getNetworksURL = 'https://' + deviceURLorIP + '/api/fmc_config/v1/domain/' + domainUUID + '/object/networks?limit=1000'

# Grabbing network objects from FMC
networks = requests.get(getNetworksURL, verify=False, headers=headers)

# Taking the Networks and turning them into json for better sorting
jsonobject1 = networks.json()

# jsonobject1 = json.loads(jsonobject1)

networks.close

csvFILE = open(fileDirectory, 'w', newline='')

csvWriter = csv.writer(csvFILE)

count = 0

# Looping through all of the network objects and grabbing the contents of the object example its IP
for items in jsonobject1['items']:

    networkaddressURL = 'https://' + deviceURLorIP + '/api/fmc_config/v1/domain/' + domainUUID + '/object/networks/' + items['id']

    networkaddressRequest = requests.get(networkaddressURL, verify=False, headers=headers)

    print(networkaddressRequest)

    networkaddress = networkaddressRequest.json()

    # this is to establish the first line of the CSV header "keys" and then moving on to the rest of the data values
    if count == 0:
 
        # Writing headers of CSV file
        csvheader = networkaddress.keys()
        csvWriter.writerow(csvheader)
        count += 1

    # Writing data of CSV file
    csvWriter.writerow(networkaddress.values())

networkaddressRequest.close

# establishing the hosts URL and grabbing all of the FMC host objects
getNetworksURL = 'https://' + deviceURLorIP + '/api/fmc_config/v1/domain/' + domainUUID + '/object/hosts?limit=1000'

hosts = requests.get(getNetworksURL, verify=False, headers=headers)

# converting objects to json
jsonobject2 = hosts.json()

# jsonobject1 = json.loads(jsonobject1)

hosts.close

# looping through host objects to get the contents
for host in jsonobject2['items']:

    networkHostURL = 'https://' + deviceURLorIP + '/api/fmc_config/v1/domain/' + domainUUID + '/object/hosts/' + host['id']

    networkHostRequest = requests.get(networkHostURL, verify=False, headers=headers)

    print(networkHostRequest)

    networkhosts = networkHostRequest.json()

    # Writing data of CSV file
    csvWriter.writerow(networkhosts.values())

networkHostRequest.close

csvFILE.close()
