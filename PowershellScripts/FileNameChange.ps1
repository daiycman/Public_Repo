##########################################################################################################################
# Script Name: Rename files for a work project
# Author: Joe Smith
# Date: 2022-03-28
# Description: The ChangeFileName function takes the file name from the storePathInfo function and gathers the files from that directory
#              It filters on the extension of the files picking out the most common image extensions
#              if it matches it then creates the new name from the information gathered in the StorePathInfo and Main functions to create the name string
#              Then it changes the name of the files and keeps count of the number of photos that it changed
#              It then asks the user if they would like to rerun the script and starts the proccess as well
##########################################################################################################################

# ERROR Handling this function does have a try catch that is supposed to take the error and spit out the issue and prompt for a restart from user

function ChangeFileName {

    $files = Get-ChildItem -Path $filePath  
    $i = 0

    try {
        ForEach ( $file in $files ){
            $extension = [IO.Path]::GetExtension($file)

            if ($extension -eq '.jpeg'  -or $extension -eq '.jfif*' -or $extension -eq '.jpg' -or $extension -eq '.png'  ){
                
                if($file.Name -notmatch 'Install' ){

                    $oldFile = $file.FullName.ToString()
                    $newName = 'S' + $storeNumber + '-' + $workType + '-install-0' + $i.ToString() + '-' + $dateTime.ToString() + '.jpg'
                    Rename-Item -Path $oldFile -NewName $newName
                    
                    $i += 1

                }

    
            }
    
    
        }
        
        Write-Host 'You have successfully renamed ' $i ' files'
        
        $script:restartFunction = Read-Host -Prompt 'Would you like to re-use this script? (y for Yes, n to Exit)'
        
        if ($restartFunction.tolower() -eq 'y'){

            main

        }
        else {

            Read-Host 'Thank you for using the script. Press Enter to exit '

            exit 
        }
        
    }
    catch {

        Write-Host $_.Exception.Message `n 
        $NowExit = ''
        $NowExit = Read-Host 'Would you like to re-try this script? (y for Yes, n to Exit)'

        if($NowExit.tolower() -eq 'y'){

            main

        }
        else {

            exit 
        }
    }

}


# The storePathInfo function gathers the date, store, and file path of the files and verifies that the path is correct from the user 
# it does this by creating a while loop that ensures that the user enters a Y to ensure the correct path was entered

# ERROR HANDLING this function does a try catch and will spit of the error to the user and ends the script
# **NEED TO UPDATE AND INCLUDE A RESTART FUNCTION IF THE USER DEEMS IT APPROPRIATE**


function storePathInfo {

    try {
        $script:storeNumber = Read-Host  "Please enter your store number: "
        $script:dateTime = Get-Date -Format "MM-dd-yyyy"

        $script:pathCheck = 'n'
        while ($pathCheck.tolower() -eq 'n') {
            $script:filePath = Read-Host "Enter File Path: "
    
            $script:pathCheck = Read-Host  "You have entered the following path "  $filePath  " is this the correct path? (y for Yes, n to reenter) "

            Continue
        }

        changeFileName
    }
    catch {
        Write-Host $_
    }

    
}

# The main function prompts the user to enter a 1 or 2 to determine if it the post or pre install of the store
# Once it determines if it is a pre or post it updates the worktype variable with that and send the user to the storePathInfo function

# ERROR HANDLING this function verifies that a 1 or a 2 is entered or it will prompt the user with an error and ask them to reenter the answer

function main {
    
    $script:workType = ''
    $workType = Read-Host  "Please enter 1 for pre install or 2 for post install: "

    if ($workType -eq '1'){
        $workType = "Pre"
        storePathInfo
    
    
    }
    elseif ($workType -eq '2') {
        $workType = "Post"
        storePathInfo
    }
    else {
        Write-Output "You have entered the wrong variable"
        main
    }
}

main