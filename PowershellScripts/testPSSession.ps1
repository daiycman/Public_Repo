##########################################################################################################################
# Script Name: Test PS Session
# Author: Joe Smith
# Date: 2022-08-10
# Description: This is just testing if I can create a powershell session on a remote server
##########################################################################################################################

$credentials = Get-Credential
$ServerName = ''

$s = New-PSSession -ComputerName $ServerName -Credential $credentials

if(-not($s))
{
    Write-Warning "$ServerName inaccessible!"
}
else
{
    Write-Host "Great! $ServerName is accessible!"
    Remove-PSSession $ServerName 
}