##########################################################################################################################
# Script Name: Create Session Key
# Author: Joe Smith
# Date: 2023-01-23
# Description: This script utilizes powershell to create a simple session key for various apps
##########################################################################################################################


$bytes = new-object "System.Byte[]" 30
(new-object System.Security.Cryptography.RNGCryptoServiceProvider).GetBytes($bytes)
[Convert]::ToBase64String($bytes)