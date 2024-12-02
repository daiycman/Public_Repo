##########################################################################################################################
# Script Name: Indicators of Compromise Automation
# Author: Joe Smith
# Date: 2023-09-17
# Description: This script is created for taking in self hosted threat feeds of SHA256 Hashes, IPs, and Domains and upload them to 
#              Cisco sites in order to block items identified as malicious that were not caught by Cisco.
#              Utilizes: Cisco CSE and Cisco Umbrella
##########################################################################################################################

import requests
import os
import time
import sys
from requests.auth import HTTPBasicAuth
import urllib3
import json
import smtplib
from email.message import EmailMessage
import re

urllib3.disable_warnings(urllib3.exceptions.InsecureRequestWarning)

version = "1.0"

# Setting URL variables
mal_Hash = ""
mal_URL_Domain_IP = ""

# Setting CLient IDs
secureX_Client_ID = ''
umbrella_Client_ID = ''
cse_Client_ID = ''

# Setting needed GUIDS
cse_simple_GUID = ''
umbrella_dest_GUI = ''

# This function will email an email to the team members when there is a system error and the program ends without completion
def sendEmail(flow,content):

    msg = EmailMessage()


    msg['Subject'] = f'IOC Automation - Flow "{flow}" has failed'
    msg['From'] = ''
    msg['To'] = ''
    msg.set_content(f'The Flow "{flow}" automation pipeline has failed with error {content}')

    server = smtplib.SMTP('**IP**')
    server.send_message(msg)
    server.quit()

# Gathering bad Domains and URLs from a Threat Stream web server
# Returns the list of Domains and URLs. If it does not receive the expected 200 from the server it will prompt an email send and exit the program with the reason
def get_Mal_Domains_URLs(mal_URL):
    content = requests.get(mal_URL, verify=False)

    # Closing Connection
    content.close()

    if content.status_code != 200:
        sendEmail('Get Domains and URLs', content)
        sys.exit(f'Failed to get Domains and URLs {content}')

    info = content.text.split()

    return (info)

# Gathering bad SHA256 Hashes from the a Threat Stream web server
# Returns the list of Hashes. If it does not receive the expected 200 from the server it will prompt an email send and exit the program with the reason
def get_Mal_Hashes(mal_Hash):
    content = requests.get(mal_Hash, verify=False)

    # Closing Connection
    content.close()    

    if content.status_code != 200:
        sendEmail('Get Hashes', content)
        sys.exit(f'Failed to get hashes {content}')

    info = content.text.split()

    return (info)

# SecureX API Login ingesting the Client ID and API Key from password vault gathered in the pipeline 
# **not being used currently as CSE lists are using V2. this is for future proofing as CSE v3 APIs require a secureX login prior to a CSE login**
# Returns the access token. If it does not receive the expected 200 from the server it will prompt an email send and exit the program with the reason
def secureXLogin(secureX_Client_ID,secureX_API_Key):
    headers = {"Content-type": "application/x-www-form-urlencoded", "Accept": "application/json"}
    data = "grant_type=client_credentials"
    url = 'https://visibility.amp.cisco.com/iroh/oauth2/token'

    content = requests.post(url, auth=HTTPBasicAuth(secureX_Client_ID, secureX_API_Key), headers=headers, data=data)

    # Closing Connection
    content.close()

    if content.status_code != 200:
        sendEmail('SecureXLogin', content)
        sys.exit(f'SecureX Failed to Authenticate with {content}')

    content = content.json()

    return (content['access_token'])


# CSE Version 3 API Login using the SecureX Access Token from SecureX API Login Function **not being used currently as CSE lists are using V2. this is for future proofing**
# Returns the access token. If it does not receive the expected 200 from the server it will prompt an email send and exit the program with the reason
def CSELoginV3(secureX_Auth):

    headers = {'Content-type': 'application/x-www-form-urlencoded', 'Accept': 'application/json' , 'Authorization': secureX_Auth}
    data = "grant_type=client_credentials"
    url = 'https://api.amp.cisco.com/v3/access_tokens'

    content = requests.post(url, headers=headers, data=data)

    # Closing Connection
    content.close()

    if content.status_code != 200:
        sendEmail('CSELoginV3', content)
        sys.exit(f'CSELoginV3 Failed to Authenticate with {content}')

    content = content.json()

    return (content['access_token'])

# Umbrella API Login ingesting the Client ID and API Key from password vault gathered in the pipeline
# Returns the access token. If it does not receive the expected 200 from the server it will prompt an email send and exit the program with the reason
def umbrellaLogin(umbrella_Client_ID, umbrella_API_Key):
    headers = {"Content-type": "application/x-www-form-urlencoded", "Accept": "application/json"}
    data = "grant_type=client_credentials"
    url = 'https://api.umbrella.com/auth/v2/token'

    content = requests.post(url, auth=HTTPBasicAuth(umbrella_Client_ID, umbrella_API_Key), headers=headers, data=data)

    # Closing Connection
    content.close()

    if content.status_code != 200:
        sendEmail('UmbrellaLogin', content)
        sys.exit(f'Umbrella Failed to Authenticate with {content}')

    content = content.json()

    return (content['access_token'])

# CSE Version 2 API using basic auth using the URL generated from the Main for loop .to update simple custom list with the SHA256 items from get_Mal_Hashes function
def CSE_Update_Simple_List(url, hash):

    # Listing out the list of hashes being added for review if needed
    print(f'Adding hash: {hash} to the simple detection list\n')

    # First trying to complete the post function to the API if it fails it will wait 3 seconds and try again
    try:
        content = requests.post(url)
    except ConnectionError: 
        print('Connection Error Waiting 3 seconds')
        time.sleep(3)
        content = requests.post(url)

    # Gathering Headers for comparison below
    rateLimitRemaining = content.headers['X-RateLimit-Remaining']
    rateLimitRemaining = int(rateLimitRemaining)
    rateLimitReset = content.headers['X-RateLimit-Reset']
    rateLimitReset = int(rateLimitReset)

    # Closing Connection
    content.close()

    # Because CSE has a limited amount of API calls that can happen per minute we are verifying that the header of remaining calls is not lower than 5
    # if it is less than 5 the function will wait for the remainder of the time until reset and then continue
    if rateLimitRemaining < 5:
        print(f'Rate limit is less than 5 waiting {rateLimitReset} seconds to reset rate limit\n')
        time.sleep(rateLimitReset)

    # If the status code is 409 that means the hash is already in the list and will skip
    if content.status_code == 409:
        print(f"Hash: {hash} has already been added, continuing with next additions\n")
        return
    
    if content.status_code == 201:
        return
    
    # We are expecting a 201 returned from CSE. If we don't see a 201 we will exit the program and send an email
    if content.status_code != 201:
        sendEmail('CSE Hash Import', content)
        sys.exit(f'Cisco Secure Endpoint Web request failed with {content}')

# Umbrella update the destination list with the destination that is needed. Also including the ID and Key if the API Token expires during usage
# This function will return the token to the main for loop for continued use. Whether or not the token is refreshed during the function
def Umbrella_Update_Destination_List(token, guid, dest, umbrellaID, umbrellaKey):

    print(f'Adding destination: {dest} to the destination list\n')
    
    # Setting headers and url with the Token and Dest GUID and URL/Domain destination
    token = token
    data = [{"destination": dest}]
    headers = {"Content-type": "application/json", "Authorization": f"Bearer {token}"}
    url = f'https://api.umbrella.com/policies/v2/destinationlists/{guid}/destinations'

    # First trying to complete the post function to the API if it fails it will wait 3 seconds and try again
    try:
        content = requests.post(url, headers=headers, json=data)
    except ConnectionError: 
        print('Umbrella connection Error Waiting 3 seconds\n')
        time.sleep(3)
        content = requests.post(url, headers=headers, data=data)

    # Gathering Headers for comparison below
    rateLimitRemaining = content.headers['RateLimit-Remaining']
    rateLimitRemaining = int(rateLimitRemaining)
    rateLimitReset = content.headers['RateLimit-Reset']
    rateLimitReset = int(rateLimitReset)

    # Because Umbrella has a limited amount of API calls that can happen per minute we are verifying that the header of remaining calls is not lower than 5
    # if it is less than 5 the function will wait for the remainder of the time until reset and then continue
    if rateLimitRemaining < 5:
        print(f'Rate limit is less than 5 waiting {rateLimitReset} seconds to reset rate limit\n')
        time.sleep(rateLimitReset)

    # During testing got weird 502 errors which are a bad gateway. Trying to add a sleep timer and try again to see if that fixes it
    if content.status_code == 502:
        print('Umbrella connection 502 Waiting 3 seconds\n')
        time.sleep(3)
        content = requests.post(url, headers=headers, data=data)

    # If we recieve a 401, most likely our Token has expired. This will call the umbrella login again to renew our Token
    # This will return the token to the main for loop for continued use
    if content.status_code == 401:
        print(f"API Token Expired. Renewing API Token\n")
        token = umbrellaLogin(umbrellaID, umbrellaKey)
        headers = {"Content-type": "application/json", "Authorization": f"Bearer {token}"}
        content = requests.post(url, headers=headers, data=data)
        return token
    
    # Expected status code
    # This will return the token to the main for loop for continued use    
    if content.status_code == 200:
        return token
    
    # We are expecting a 200 returned from Umbrella. If we don't see a 201 we will exit the program and send an email
    if content.status_code != 200:
        sendEmail('Umbrella IOCs Import', content)
        sys.exit(f'Umbrella Web request failed with {content}')

    # Closing Connection
    content.close()


if __name__ == "__main__":

    # Completing all Client IDs and Keys from global initializations + password vault
    secureX_ID = secureX_Client_ID
    umbrella_ID = umbrella_Client_ID
    cse_ID = cse_Client_ID
    umbrella_Key = os.getenv('Umbrella_API_Key')
    secureX_Key = os.getenv('SecureX_API_Key')
    cse_V2_Key = os.getenv('CSE_API_Key')

    # Setting all GUIDs that will be needed
    cse_GUID = cse_simple_GUID
    umbrella_GUID = umbrella_dest_GUI

    # Retrieving all information from Information Security Lists
    hash_List = get_Mal_Hashes(mal_Hash)
    umbrella_List = get_Mal_Domains_URLs(mal_URL_Domain_IP)

    # Looping through hashes and calling the cse Updater function
    for hash in hash_List:
        url = f'https://{cse_ID}:{cse_V2_Key}@api.amp.cisco.com/v1/file_lists/{cse_GUID}/files/{hash}'

        CSE_Update_Simple_List(url, hash)

    umbrella_AuthToken = umbrellaLogin(umbrella_ID, umbrella_Key)

    # Looping through domains and URLs and calling the Umbrella Updater function
    for items in umbrella_List:
        if re.match('http.*?:\/\/(?:[0-9]{1,3}\.){3}[0-9]{1,3}', items):
            print(f'Skipping {items} because it is an IP\n')
            continue
        else:
            returnToken = Umbrella_Update_Destination_List(umbrella_AuthToken, umbrella_GUID, items, umbrella_ID, umbrella_Key)
            umbrella_AuthToken = returnToken