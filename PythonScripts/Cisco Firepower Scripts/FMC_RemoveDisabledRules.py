##########################################################################################################################
# Script Name: FMC Removed Disabled Rules
# Author: Joe Smith
# Date: 2023-09-27
# Description: This script utilizes the Cisco FMC API's to remove disabled rules from the desired Policy
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

# File location with the file name ex:C:\\Users\\FoldertoWhateverLocationToSave\\CSV.csv' This will be used to save a list of the names of the rules removed
fileDirectory = f''

fmc = FMC(hostname=fmcAddress,username=userName,password=password)

# print(fmc.policy.accesspolicy.get())

policyrules = fmc.policy.accesspolicy.accessrule.get(container_name=policyName)

csvFILE = open(fileDirectory, 'w', newline='')

csvWriter = csv.writer(csvFILE)

count = 0

csvWriter.writerow(['Name'])

startTime = time.time()

# Loop through all rules in the Access Control Policy in the FMC and checking if the rule is disabled
for policy in policyrules:
    # If the rule is disabled delete it
    if(policy['enabled'] == False):
        fmc.policy.accesspolicy.accessrule.delete(container_name=policyName, uuid=policy['id'])
        
        # Writing data of CSV file
        csvWriter.writerow([policy['name']])

print(f'Elapsed Time: {time.time()-startTime}')

csvFILE.close()