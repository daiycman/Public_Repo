##########################################################################################################################
# Script Name: Send an Email
# Author: Joe Smith
# Date: 2023-04-11
# Description: This is a script sends an email using a text file as the body and adding an attachment file
##########################################################################################################################

$emails = Import-Csv 'C:\Users\joes\emails.csv'
$to = $emails.Email
$subject = "Titles"
$body = Get-Content 'C:\Users\joes\EmailBody.txt' -Raw
$attachment = 'C:\Users\joeS\TroubleshootingSteps.docx'

$mailParam = @{
    To = ""
    Bcc = $to
    From = ""
    Subject = $subject
    Body = $body
    Attachments = $attachment
    SmtpServer = ""
}

# Send Email
Send-MailMessage @mailParam -Priority High