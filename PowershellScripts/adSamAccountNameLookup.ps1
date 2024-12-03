##########################################################################################################################
# Script Name: Retrieve samAccountname from AD
# Author: Joe Smith
# Date: 2023-01-23
# Description: This script utilizes powershell ad components to ingest a list of usernames and return samAccountname and 
#              email from AD and send it to a csv
##########################################################################################################################

$names = Import-Csv 'C:\Users\joes\Documents\usernames.csv'
$username = $null
$lookedUP = @()
#$failed = @()

ForEach($username in $names){

    try {
        $username = $username.Name
        $userNameWildCard = $userName + "*"


        $lookedup += Get-ADUser -Filter {name -like $userNameWildCard} -Properties DisplayName, samAccountName | Where-Object {$_.samAccountName -notlike "*-*"}

    }
    catch {
        $username.Name
    }

}
$lookedUP | Select-Object @{Label='Name';Expression={$_.DisplayName}}, @{Label='UserName';Expression={$_.samAccountName}}, @{Label='Email';Expression={$_.UserPrincipalName}} | 

Export-Csv 'C:\Users\joeS\Documents\users.csv' -NoTypeInformation 