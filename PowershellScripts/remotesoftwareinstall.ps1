##########################################################################################################################
# Script Name: Remote Install on Windows Server
# Author: Joe Smith
# Date: 2022-08-03
# Description: This is a script to attempt to install an msi remotely from a different server. It sort of works sometimes not
#              Was a fun try at a problem for installs
##########################################################################################################################

$Servers = Import-Csv -Path "C:\Script\testPCs.csv"
$packageName= "filename.msi"
$Folder= "\\sharedDrive\SoftwareShare\$packageName"
$credentials = Get-Credential 'domain\username'
$softwareName = ""


Foreach ($Server in $Servers) {

$ServerName = $Server.Name
$Test = Test-Path -path "\\$ServerName\c$\Temp\"

If ($Test -eq $True) {
    
    Write-Host "`nPath exists, hence installing software on $ServerName."

}

Else {
    
    (Write-Host "`nPath doesnt exists, hence Creating foldet on $ServerName and starting installation") , (New-Item -ItemType Directory -Name Temp -Path "\\$ServerName\c$")

}


Write-Host "Copying Files to C:\Temp\"


Copy-Item $Folder "\\$ServerName\c$\Temp\"

Write-Host "Second Part :- Installing Software on $ServerName"


$s = New-PSSession -ComputerName $ServerName -Credential $credentials

Invoke-Command -Session $s  -ScriptBlock {
    
   ( Start-Process -FilePath Powershell.exe -Verb RunAs -Wait -ArgumentList "Invoke-Expression 'c:\Temp\$Using:packageName /quiet /qn'"), (Remove-Item -path "C:\Temp\$Using:packageName" -ErrorAction Ignore )

}

Write-Host "Checking for the installed software, please wait"


Start-Sleep -Seconds 03

$installed = Invoke-Command -Session $s -ScriptBlock {



(Get-ItemProperty HKLM:\Software\Microsoft\Windows\CurrentVersion\Uninstall\* | Where { $_.DisplayName -eq $Using:softwareName }) -ne $null

}

if ($installed){
   
   Write-Host "Software has been installed on $ServerName`n`n"

   $ServerName | Out-File "C:\Script\CompletedServers.csv" -Append
}
Else{

    Write-Host "Software was NOT installed on $ServerName`n`n"

    $ServerName | Out-File "C:\Script\NotCompletedServers.csv" -Append

}

Remove-PSSession -Session $s 


}