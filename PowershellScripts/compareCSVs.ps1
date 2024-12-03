##########################################################################################################################
# Script Name: Compare CSVs
# Author: Joe Smith
# Date: 2023-04-13
# Description: This script utilizes powershell to compare two CSVs. This one is looking for users logged into Machines
##########################################################################################################################

$csvwrapper = @()

$usernames = Import-Csv 'C:\Users\joes\Documents\Usernames.csv'
$MainsetComputers = Import-Csv 'C:\Users\joes\usernames2.csv'

foreach($user in $usernames){

    $u = $user.Users

    foreach($c in $MainsetComputers){
       $loggedin = $c.LoggedIn


       if($loggedin.Contains($u)){
            
        $csvwrapper += New-Object psobject -Property @{

            Name = $u;
            ComputerName = $c.ComputerName;
            Guid = $c.AgentId;

        }

       }


    }
}

$csvwrapper | Select Name, ComputerName, Guid | export-csv 'C:\Users\joes\compareoutput.csv' -NoTypeInformation 