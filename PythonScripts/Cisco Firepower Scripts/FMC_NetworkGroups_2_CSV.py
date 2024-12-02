##########################################################################################################################
# Script Name: FMC Gather Network Groups
# Author: Joe Smith
# Date: 2022-10-13
# Description: This script utilizes the Cisco FMC API's to print a CSV of FMC Network groups
#             This script is not utilizing the fireREST library. The token request functionality can be replaced with that
##########################################################################################################################

import requests
import json
import csv
import getpass
from requests.auth import HTTPBasicAuth
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

networks = requests.get(getNetworksURL, verify=False, headers=headers)

jsonobject1 = networks.json()

# jsonobject1 = json.loads(jsonobject1)

networks.close

csvFILE = open(fileDirectory, 'w', newline='')

csvWriter = csv.writer(csvFILE)



for items in jsonobject1['items']:

    networkgroupURL = 'https://' + deviceURLorIP + '/api/fmc_config/v1/domain/' + domainUUID + '/object/networkgroups/' + items['id']

    networkgroupRequest = requests.get(networkgroupURL, verify=False, headers=headers)

    print(networkgroupRequest)

    networkgroup = networkgroupRequest.json()

    count = 0

    if count == 0:
        # Writing headers of CSV file
        csvheader = [networkgroup['name'],networkgroup['id']]
        csvWriter.writerow(csvheader)
        count += 1

    try:

        for objects in networkgroup["objects"]:

            # Writing data of CSV file
            csvWriter.writerow(objects.values())

    except:
        for objects in networkgroup["literals"]:

            # Writing data of CSV file
            csvWriter.writerow(objects.values())
    
    csvWriter.writerow('')

    
networkgroupRequest.close
csvFILE.close()
