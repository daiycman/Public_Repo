##########################################################################################################################
# Script Name: Cyberark EPM Create JIT
# Author: Joe Smith
# Date: 2023-10-10
# Description: This script utilizes the Cyberark EPM APIs to create a Just In Time policy for users to be placed into the
#              Admininstrator group on their machine. This is designed to run in a azure Pipeline and from a Microsoft
#              Powerapps form that asks users for the information needed of themselves and their machine
##########################################################################################################################

import requests
import os
import urllib3
from datetime import datetime
import sys

# Disable cert warnings
urllib3.disable_warnings(urllib3.exceptions.InsecureRequestWarning)

# Setting basic variables for the script **Change the setID when moving to the main set with 3e9c9337-56aa-4b2e-a449-f24d9173cd21 **Test SetID: 2923039e-75ad-4e4c-8bcf-8cec621c39fd
logonURL = 'https://login.epm.cyberark.com/EPM/API/Auth/EPM/Logon'
setID = ""
password = os.getenv('CyberarkEPM_SA_PW')
machineName = os.getenv('WorkstationName')
userName = os.getenv('userName')

# Resetting the variables to be CyberArk Friendly
domainUserName = '**Domain***' + userName
machineName = " '" + machineName + "'"

# Setting a time date stamp for policy name
currentDateTime = datetime.now()
currentDateTime = currentDateTime.strftime("%Y-%m-%d %H:%M")

def CyberArkEPM_Login():

    # Creating JSON body for logging in
    userNamepassWord = {

        "Username": "",

        "Password": password,

        "ApplicationID": "**name of EPM Group**"
    }

    # Logging into CybearkEPM and grabbing the authentication token and storing into a variable for other
    tokenRequest = requests.post(logonURL, verify=False, json=userNamepassWord)

    tokenRequest.close

    if tokenRequest.status_code !=200:
        sys.exit(f'Failed to login {tokenRequest}')

    tokenRequest = tokenRequest.json()

    authToken = "basic " + tokenRequest['EPMAuthenticationResult']

    return authToken

def get_Computer_ID(headers):

    # This url is the URL listed at the top of your console URL. its a server group URL hosted by EPM
    getComputerNameURL = f'https://na000.epm.cyberark.com/EPM/API/Sets/{setID}/Computers?$filter=ComputerName eq {machineName}'

    # Takes the machine name, looks up the machine in the EPM console, and stores that ID for policy use
    computer = requests.get(getComputerNameURL, verify=False, headers=headers)

    jsonobject1 = computer.json()

    computer.close

    if computer.status_code !=200:
        sys.exit(f'Failed to login {computer}')

    computerAgentID = jsonobject1['Computers'][0]['AgentId']

    return computerAgentID

def create_JIT_Policy(headers, computerAgentID):

    # creating a policy name with the name Automated and date so we can look up the request if necessary
    policyCreatedDate = "Automated_TestMachine_JIT_" + str(currentDateTime)

    # Create the JIT Policy JSON body ingesting the variables set above
    createPolicyBody = {
        "Name": policyCreatedDate,
        "IsActive": "true",
        "IsAppliedToAllComputers": "false",
        "PolicyType": 40,
        "Action": 20,
        "Duration": "8",
        "KillRunningApps": "true",
        "Audit": "true",
        "Executors": [
                {
                    "Id": computerAgentID,
                    "Name": machineName,
                    "IsIncluded": "true",
                    "ExecutorType": 1
                }
            ],
        "Accounts": [
                {
                    "Sid": "",
                    "AccountType": 1,
                    "DisplayName": domainUserName,
                    "SamName": domainUserName
                }
            ],
        "IncludeADComputerGroups": [],
            "TargetLocalGroups": [
                {
                    "Sid": "",
                    "AccountType": 0,
                    "DisplayName": "Administrators",
                    "SamName": "Administrators"
                }
            ],
    }

    # Setting the policy URL for the JIT and posting the request to create the poilicy 
    createPolicyURL = f'https://na000.epm.cyberark.com/EPM/API/Sets/{setID}/Policies/Server'

    createPolicyCall = requests.post(createPolicyURL, verify=False, headers=headers, json=createPolicyBody)

    if createPolicyCall.status_code !=201:
        sys.exit(f'Failed to login {createPolicyCall}')

    

if __name__ == "__main__":

    authToken = CyberArkEPM_Login()

    # Creating authentication Token JSON header
    headers = {
        "Authorization": authToken

    }

    computerAgentID = get_Computer_ID(headers)

    create_JIT_Policy(headers,computerAgentID)