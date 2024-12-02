##########################################################################################################################
# Script Name: Email Test
# Author: Joe Smith
# Date: 2023-10-10
# Description: This script utilizes the send email functionality in python that I was playing with for scripts
##########################################################################################################################

import smtplib
from email.message import EmailMessage

msg = EmailMessage()


msg['Subject'] = 'Test Subject'
msg['From'] = ''
msg['To'] = ''
msg.set_content('This is a test')

server = smtplib.SMTP('Domain/IP of SMTP server')
server.send_message(msg)
server.quit()