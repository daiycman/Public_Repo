##########################################################################################################################
# Script Name: Remote File Purge
# Author: Joe Smith
# Date: 2024-06-27
# Description: This is a script to purge files older than two weeks from a shared server path e.g NAS
##########################################################################################################################

Param(
    [Parameter(Mandatory=$true)]
    [String]$SAcredential
    )

$user = 'domain\username'
$securePassword = ConvertTo-SecureString $SAcredential -AsPlainText -Force
$Credential = New-Object System.Management.Automation.PSCredential $user, $securePassword

$filepathFMCBackup = '\\server\backups'
$filepathFTDBackup = '\\server\remote-backups'

$filePath = "\\server\TestFolder\TestTestChild"

$currentDate = Get-Date

$cutOffDate = $currentDate.AddDays(-14)

New-PSDrive -Credential $Credential -Root $filepathFMCBackup -Name "T" -PSProvider FileSystem
New-PSDrive -Credential $Credential -Root $filepathFTDBackup -Name "U" -PSProvider FileSystem

$oldFMCFiles = Get-ChildItem -Path $filepathFMCBackup -File -Recurse | Where-Object {$_.LastWriteTime -lt $cutOffDate}

foreach ($file in $oldFMCFiles){
    try{ Remove-Item -Path $file.FullName -Force}
    catch {write-host "failed to remove $file"}

}

$oldFTDFiles = Get-ChildItem -Path $filepathFTDBackup -File -Recurse | Where-Object {$_.LastWriteTime -lt $cutOffDate}

foreach ($file in $oldFTDFiles){
    try{ Remove-Item -Path $file.FullName -Force}
    catch {write-host "failed to remove $file"}

}

Get-PSDrive T,U | Remove-PSDrive