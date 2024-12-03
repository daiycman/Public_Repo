##########################################################################################################################
# Script Name: Extract cert info
# Author: Joe Smith
# Date: 2023-01-23
# Description: This script utilizes powershell and Git's built in openssl on windows to take a pkcs12 Cert and makes the
#              key and cert available for usage in the BEGIN CERT format and key unencrypted to upload to whatever app
#              These need to be ran separately.
##########################################################################################################################


Start-Process "C:\Program Files\Git\usr\bin\openssl.exe" pkcs12 -in C:\Users\joes\Downloads\cert.pfx -nokeys -out C:\Users\joes\Downloads\cert.pem
Start-Process "C:\Program Files\Git\usr\bin\openssl.exe" pkcs12 -in C:\Users\joes\Downloads\cert.pfx -nocerts -out C:\Users\joes\Downloads\key.pem -nodes
Start-Process "C:\Program Files\Git\usr\bin\openssl.exe" rsa -in C:\Users\jose\Downloads\key.pem -out C:\Users\joes\Downloads\server.key