##########################################################################################################################
# Script Name: FMC Report Logging Settings
# Author: Joe Smith
# Date: 2023-09-13
# Description: This script utilizes the Cisco FMC API's to gather what the current policy Logging settings are
#             and will print that to a CSV for review
##########################################################################################################################

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

policyrules = fmc.policy.accesspolicy.accessrule.get(container_name=policyName)

csvFILE = open(fileDirectory, 'w', newline='')

csvWriter = csv.writer(csvFILE)

csvWriter.writerow(('name', 'action', 'logBegin', 'logEnd', 'enableSyslog', 'sendEventsToFMC'))

startTime = time.time()

changed = False

for policy in policyrules:

    if (policy['action'] == 'BLOCK'):
        if(policy['logBegin'] == False):
            changed = True
            
        if (policy['sendEventsToFMC'] == False):
            changed = True

        if (policy['enableSyslog'] == False):
            changed = True

    elif (policy['action'] == 'BLOCK_RESET'):     
        if(policy['logBegin'] == False):
            changed = True 
            
        if (policy['sendEventsToFMC'] == False):
            changed = True

        if (policy['enableSyslog'] == False):
            changed = True

    else:                 
        if (policy['sendEventsToFMC'] == False):
            changed = True

        if (policy['enableSyslog'] == False):
            changed = True

        if(policy['logBegin'] == True):
            changed = True

        if(policy['logEnd'] == False):
            changed = True
    
    if (changed == True):
        # Writing data of CSV file
        csvWriter.writerow((policy['name'], policy['action'], policy['logBegin'], policy['logEnd'], policy['enableSyslog'], policy['sendEventsToFMC']))
    
    changed = False



print(f'Elapsed Time: {time.time()-startTime}')

csvFILE.close()