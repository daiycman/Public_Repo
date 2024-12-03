##########################################################################################################################
# Script Name: Cyberark EPM Report
# Author: Joe Smith
# Date: 2024-03-28
# Description: This script utilizes the Cyberark EPM APIs to run a policy audit report, convert it into a csv, send it as 
#              an attachment to thee users manager and upload that CSV to a sharepoint folder
##########################################################################################################################


# setting basic varibles
$epmLogonURL = 'https://login.epm.cyberark.com/EPM/API/Auth/EPM/Logon' # login URL for CybearkEPM
$epmServerURL = '' # the server URL where EPM environment is hosted
$sharepointSiteID = '' # the team sharepoint ID
$sharepointDriveID = '' # folder information from the team sharepoint
$epmAuditFolderID = ''
$azureTenantID = '' # Azure tenent ID
$CyberarkEPM_SA_PW = [Environment]::GetEnvironmentVariable('CyberarkEPM_SA_PW') # this env variable is set within the azure pipeline from the PWV retrieval step
# $SPclientSecret = [Environment]::GetEnvironmentVariable('SP_CyberArkEPM_P_Secret') # using this for local testing only. the SP secret is pulled using the SP secret function below when the pipeline is ran
$keyVaultName = '' # The name of the key vault that houses the Service Principals secret
$azureSPClientID = '' # Cyberark EPM service principal client ID
$azureSPName = '' # The name of the sevice prinicipals secret
$month = (Get-Date).AddMonths(-1).tostring("MMMM") # setting month name for the file names
$fileName = "CyberkArk_EPM_Report_$month.csv" # setting the CSV file names
$global:managerEmails = @('')
$global:teamEmails = @('')



# This function builds a csv in memory in order to send a csv via email. Returns that csv
function ConvertTo-CSVEmailAttachment {
    Param(
        [Parameter(Mandatory=$true)]
        [String]$FileName,
        [Parameter(Mandatory=$true)]
        [Object]$PSObject,
        $Delimiter
        )
        If ($Delimiter -eq $null){$Delimiter = ","}
        $MS = [System.IO.MemoryStream]::new()
        $SW = [System.IO.StreamWriter]::new($MS)
        $SW.Write([String]($PSObject | convertto-csv -NoTypeInformation -Delimiter $Delimiter | % {($_).replace('"','') + [System.Environment]::NewLine}))
        $SW.Flush()
        $MS.Seek(0,"Begin") | Out-Null
        $CT = [System.Net.Mime.ContentType]::new()
        $CT.MediaType = "text/csv"
        Return [System.Net.Mail.Attachment]::new($MS,$FileName,$CT)
    }

# This function creates an email to send the recieptants information from this script
function SendEmail {
    Param(
        [Parameter(Mandatory=$true)]
        [Object]$toAddresses,
        [Parameter(Mandatory=$true)]
        [String]$subject,
        [Parameter(Mandatory=$true)]
        [String]$body,
        $attachment
        )

    $SMTPserver = ""
    $from = ""

    # needed to add in email batches because sometimes SMTP servers can only handle X amount of receipants per email send so we will send them in batches of 25
    $mailer = new-object Net.Mail.SMTPclient($SMTPserver)
    $batchsize = 25

    for ($i = 0; $i -lt $toAddresses.Count; $i += $batchsize){

        $msg = new-object Net.Mail.MailMessage
        $msg.From =$from
        $msg.Subject = $subject
        $msg.Body = $body
        $batch = $toAddresses[$i..([math]::Min($i + $batchsize - 1, $toAddresses.Count - 1))]
        $batch | ForEach-Object {$msg.Bcc.Add($_)}
        $msg.Bcc.Add('**mandatory email for verification**')
        $sentemail = $msg.Bcc

        if ($attachment -ne $null){
            $msg.Attachments.Add($attachment) #### This uses the attachment made using the function above. 
        }
        
        try {
            $mailer.send($msg)
            write-host "Successfully sent email to: $sentemail`n"
        }
        catch {
            Write-Error "An error occured while sending email `n"
            exit 1
        }

    }
    
    
}


# This function builds out the proper json and receives a token from cyberark using the username and password stored in the PWV. Returns access token. **Cyberkark is looking at moving to API Keys**
function CyberArkEPM_Login {

    # Creating JSON body for logging in
    $userNamepassWord = @{

        "Username" = ""

        "Password" = "$CyberarkEPM_SA_PW"

        "ApplicationID" = ""
    }

    $userNamepassWord = $userNamepassWord | ConvertTo-Json

    # Logging into CybearkEPM and grabbing the authentication token and storing into a variable for other    
    try {
        $tokenRequest = Invoke-WebRequest -Uri $epmLogonURL -Body $userNamepassWord -ContentType 'application/json' -Method Post 
        write-host "Successfully retrieved a CyberArk EPM Access token `n"
    }
    catch {
        if($_.Exception.Response){
            $httpstatuscode = $_.Exception.Response.statuscode.value__
            Write-Error "Failed to retrieve a CyberArk EPM access token with reponse: $httpstatuscode `n"
            
        }
        else{
            Write-Error "Failed to retrieve a CyberArk EPM access token `n"
        
        }
        SendEmail -toAddresses $global:teamEmails -subject 'Epm Audit Automation Failed' -body 'The EPM audit report failed on the CyberArk EPM retrieve Access Token'
        exit 1
    }

    $LoginConverted = $tokenRequest | ConvertFrom-Json

    $authToken = "basic " + $LoginConverted.EPMAuthenticationResult
    return $authToken
}

# Using the access token from the login function this function calls the audit report from cyberark and passes in the policy name and time of the elevation as filters
# then the function loops through all received data from the api call, pulls the necessary key value pairs, and formats the data into CSV friendly data
# this function then adds in the users Name and Manager name into the data key value pairs from AD utilizing two get functions 
# Returns the PS object for the report to be used in the csv generation for email and sharepoint
function GetEPMreport{
    Param(
        [Parameter(Mandatory=$true)]
        [String]$authToken
        )

    $loop = $true
    $epmReport = @()
    $firstdayofMonth = (Get-Date -Day 1).AddMonths(-1).ToString("yyyy-MM-dd")
    $datetime = $firstdayofMonth + 'T00:00:00Z'
    # 2024-04-01T00:00:00Z

    # creating json body for filters that are needed to be passed in the body of the request to pull only the information for the last month as well as the proper policies
    $filter = @"
    {
        "filter" : "(policyName CONTAINS \"5 - Modern\" OR policyName CONTAINS \"4 - Legacy\" AND arrivalTime GE $datetime)"
    }
"@
    # setting the headers for the request
    $headers = New-Object "System.Collections.Generic.Dictionary[[String],[String]]"
    $headers.Add('Accept','Application/Json')
    $headers.Add("Authorization", "$authToken")

    # The maximum number of audit events is 1000. The next cursor is a pseudorandom number generated by EPM to use for the continuation of calls
    # we must first set that nextcursor as "start" to begin the calls and then we can pull that number from the response and update it during the function to use if we need to make another call
    $nextCursor = "start"

    # we are using a loop function because of the nextcursor. If the next cursor becomes NULL the loop will break 
    while ($loop -eq $true) {

        $AuditReportURL = $epmServerURL + "/EPM/API/Sets/***/policyaudits/search?limit=1000&nextCursor=" + $nextCursor

        try {
            $getAuditReport = Invoke-WebRequest -Uri $AuditReportURL -Method Post -Body $filter -Headers $headers
        }
        catch {
            if($_.Exception.Response){
                $httpstatuscode = $_.Exception.Response.statuscode.value__
                Write-Error "Failed to get audit report with response: $httpstatuscode `n"
                
            }
            else{
                Write-Error "Failed to get audit report `n"
            
            }
            SendEmail -toAddresses $global:teamEmails -subject 'Epm Audit Automation Failed' -body 'The EPM audit report failed on the CyberArk EPM retrieve EPM Report'
            exit 1
            
        }

        $getAuditReport = $getAuditReport | ConvertFrom-Json

        # Checking if the nextcursor in the response is NULL. it will only be null on the last page of the response with no data in the response
        if ($getAuditReport.nextCursor -ne $null){

            # going through each event and pulling the required information and storing it in a PSobject
            # getting the user's Name and the users managers name
            # for csv files to work properly we are using the "," delimiter so we need to replace any "," that is pulled in the data with ";" to keep the csv consistent
            foreach ($policyevent in $getAuditReport.events){
                $usersplit = ($policyevent.userName -split "\\")[1]
                $username = GetUser -user $usersplit
                $manager = GetUserManager -user $usersplit
                $policyevent | Add-Member -Type NoteProperty -Name "User" -Value $username
                $policyevent | Add-Member -Type NoteProperty -Name "Manager" -Value $manager
                $policyevent.PSObject.Properties | ForEach-Object {
                    if ($_.Value -is [string]) {
                        $_.Value = $_.Value.Replace(',', ';')
                    }
                }
                $epmReport += $policyevent | Select-Object userName, User, computerName, Manager, fileName, PackageName, DisplayName, Hash, lastEventDate

            }
            # setting the nextcursor value if it is not NULL
            $nextCursor = $getAuditReport.nextCursor
        }
        # breaking the loop if the nextcursor is NULL
        else{
            $loop = $false
        }
        
    }

    return $epmReport

}

# Function to authenticate and get access token from your azure tenent utilizing the CyberarkEPM service principal and secret. Returns an access token
function Azure_Login {
    Param(
        [Parameter(Mandatory=$true)]
        [String]$SPclientSecret
        )

    # setting the login URL and the body with the service principal information
    $tokenUrl = "https://login.microsoftonline.com/$azureTenantID/oauth2/token"

    $body = "grant_type=client_credentials&client_id=$azureSPClientID&client_secret=$SPclientSecret&resource=https%3A%2F%2Fgraph.microsoft.com%2F"

    $headers = @{
        "Content-Type" = "application/x-www-form-urlencoded"
    }

    # receiving and returning the access token
    try {
        $tokenResponse = Invoke-RestMethod -Uri $tokenUrl -Method POST -Body $body -Headers $headers 
        write-host "successfully received an Azure Auth Token `n"
    }
    catch {
        if($_.Exception.Response){
            $httpstatuscode = $_.Exception.Response.statuscode.value__
            Write-Error "Failed to log into Azure and retrieve access token with response: $httpstatuscode `n"
            
        }
        else{
            Write-Error "Failed to log into Azure and retrieve access token `n"
        
        }
        SendEmail -toAddresses $global:teamEmails -subject 'Epm Audit Automation Failed' -body 'The EPM audit report failed on the Azure retrieve Access Token'
        exit 1
    }
    
    return $tokenResponse.access_token
}

# Function to create file in SharePoint using the epm report gathered in the report function
function Create_SharePointFile {
    Param(
        [Parameter(Mandatory=$true)]
        [Object]$fileContent,
        [Parameter(Mandatory=$true)]
        [String]$filename,
        [Parameter(Mandatory=$true)]
        [String]$accessToken
        )

    # setting the url and headers with the access token from the login function
    $filenamenew = $filename + ":"
    $siteApiUrl = "https://graph.microsoft.com/v1.0/sites/$sharepointSiteID/drives/$sharepointDriveID/items/$epmAuditFolderID/$filenamenew/content"

    $csvcontent = [String]($fileContent | convertto-csv -NoTypeInformation | % {($_).replace('"','') + [System.Environment]::NewLine})

    $headers = @{
        Authorization = "Bearer $accessToken"
        "Content-Type" = "text/csv"
    }
    
    try {
        Invoke-RestMethod -Uri $siteApiUrl -Method PUT -Headers $headers -Body $csvcontent
        Write-Host "File '$fileName' created successfully `n"
    }
    catch {
        Write-Error "Failed to create file in sharepoint `n"
        SendEmail -toAddresses $global:teamEmails -subject 'Epm Audit Automation Failed' -body 'The EPM audit report failed on the creation of the sharepoint file'
        exit 1
    }
    
}

# this function is called during the report api function to grab the display name of the user from the username that is reported in the API audit report
function GetUser{
    Param(
        [Parameter(Mandatory=$true)]
        [String]$user
        )

    try {
        $ADuser = Get-ADUser $user -properties DisplayName
        $displayname = $ADuser.DisplayName -replace ',',';'
    }
    catch {
        write-host "Could not find user: $user `n"
        $displayname = " "
    }
    return $displayname

}

# this function is called during the report api function to grab the display name of the user's manager's name from the username that is reported in the API audit report
function GetUserManager{
    Param(
        [Parameter(Mandatory=$true)]
        [String]$user
        )

    try {
        $usermanager = get-ADUser $user -properties Manager 
        $managerUN = $usermanager.Manager
        $managerName = Get-ADUser $managerUN -Properties DisplayName, UserPrincipalName
        $displayname = $managerName.DisplayName -replace ',',';'
        if($global:managerEmails -notcontains $managerName.UserPrincipalName){
            $global:managerEmails += $managerName.UserPrincipalName

        }
        
    }
    catch {
        Write-Host "Could not find manager for: $user `n"
        $displayname = " "
    }
    return $displayname

}

# this function is to retrieve the SP secret from azure
function GetSPSecret {
    
    $subContext = Set-AzContext -SubscriptionName ""

    try {
        $secret = Get-AzKeyVaultSecret -VaultName $keyVaultName -Name $azureSPName -AsPlainText -DefaultProfile $subContext
        Write-Host "Successfully retrieved the CyberArk SP Secret `n"
    }
    catch {
        Write-Error "Could not retrieve the CyberArk SP Secret secret `n"
        SendEmail -toAddresses $global:teamEmails -subject 'Epm Audit Automation Failed' -body 'The EPM audit report failed on the SP Secret Key retrieval'
        exit 1
    }
    return $secret

}

# The body of the script calling the functions

# Generate the CyberArk EPM console token
$EPMToken = CyberArkEPM_Login

# starts the api call to pull the report from EPM
$report = GetEPMreport -authToken $EPMToken

# retrieve service principal client secret from the password vault
$SPclientSecret = GetSPSecret

# Authenticate and get access token
$azureToken = Azure_Login -SPclientSecret $SPclientSecret

# this builds a csv file in memory to send as an attachment to the CyberArk EPM mailbox
$emailAttachmentFile = ConvertTo-CSVEmailAttachment -FileName $fileName -PSObject $report

# Create file in SharePoint
Create_SharePointFile -fileContent $report -filename $fileName -accessToken $azureToken

$managerBody = @"
Dear Manager,

whatever message


"@

$managerSubject = "Action Required: Review Elevated Privileges Usage by Direct Reports for $month"
SendEmail -toAddresses $global:managerEmails -subject $managerSubject -body $managerBody -attachment $emailAttachmentFile