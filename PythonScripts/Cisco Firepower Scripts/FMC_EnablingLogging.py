##########################################################################################################################
# Script Name: FMC Enable Logging
# Author: Joe Smith
# Date: 2023-09-13
# Description: This script utilizes the Cisco FMC API's to gather what the current policy Logging settings are
#             If it determines that the logging is wrong based on the creators need
#             It will change the JSON variable to the correct setting and use the FMC APIs to update the rule on the FMC.
##########################################################################################################################

# importing needed libraries
from fireREST import FMC
from getpass import getpass
import csv
import time

# Setting the variables that are needed for the script. Fill out with the information of the desired FMC
fmcAddress = ""
userName = ""
# will prompt the CLI for an entry of the password for the username provided. This will not be shown on the CLI
password = getpass()
# Enter the FMC Policy Name that we want to run this on. This is case sensitive
policyName = ''

# File location with the file name ex:C:\\Users\\FoldertoWhateverLocationToSave\\CSV.csv'
fileDirectory = f''

fmc = FMC(hostname=fmcAddress,username=userName,password=password)

# Grabbing all rules inside the listed policy
policyrules = fmc.policy.accesspolicy.accessrule.get(container_name=policyName)

# opening/creating the file 
csvFILE = open(fileDirectory, 'w', newline='')

csvWriter = csv.writer(csvFILE)

# Writing the first row of data
csvWriter.writerow(('name', 'action', 'logBegin', 'logEnd', 'enableSyslog', 'sendEventsToFMC'))

startTime = time.time()

changed = False

# Looping through all policies to understand the logging enabled and changing the logging to the desired state
# If the logging needs to be changed it will change the json value and set the "changed" variable to True
for policy in policyrules:
    
    if (policy['sendEventsToFMC'] == False):
        policy['sendEventsToFMC'] = True
        changed = True

    if (policy['enableSyslog'] == False):
        policy['enableSyslog'] = True
        changed = True

    if (policy['action'] == 'BLOCK'):
        if(policy['logBegin'] == False):
            policy['logBegin'] = True
            changed = True

    elif (policy['action'] == 'BLOCK_RESET'):     
         if(policy['logBegin'] == False):
            policy['logBegin'] = True
            changed = True 

    else:
        if(policy['logBegin'] == True):
            policy['logBegin'] = False
            changed = True

        if(policy['logEnd'] == False):
            policy['logEnd'] = True
            changed = True
    
    # if the logging on the policy needs to be changed change it with the changed JSON information
    if (changed == True):
        # updating rule
        fmc.policy.accesspolicy.accessrule.update(container_name=policyName,data=policy)
        # Writing data of CSV file
        csvWriter.writerow((policy['name'], policy['action'], policy['logBegin'], policy['logEnd'], policy['enableSyslog'], policy['sendEventsToFMC']))
    
    changed = False

# printing how log it takes to change all of the policies
print(f'Elapsed Time: {time.time()-startTime}')

# Closes the file
csvFILE.close()