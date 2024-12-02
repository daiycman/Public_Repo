##########################################################################################################################
# Script Name: Cloudflare Retrieve DNS Records
# Author: Joe Smith
# Date: 2023-12-10
# Description: This script utilizes the Cloudflare APIs to parse through DNS records of your DNS zone
##########################################################################################################################

import requests
import dns
import dns.resolver
import os

# These are some functions to grab a resolution of a URL
# def get_dns_record():

#     record = dns.resolver.resolve('', 'A')


#     for IPval in record:
#         value = IPval.to_text()

#     return value

# def get_public_ip(): 
#     try: 
#         response = requests.get('https://httpbin.org/ip') 
#         if response.status_code == 200: 
#             ip_data = response.json() 
#             public_ip = ip_data.get('origin') 
#             public_ip = str(public_ip)
#             return public_ip 
#         else: 
#             print(f"Failed to retrieve IP (Status code: {response.status_code})") 
#     except Exception as e: 
#         print(f"Error: {e}") 
 
# # Get and print the public IP address 
# public_ip = get_public_ip() 
# dns_ip = get_dns_record()

# if public_ip != dns_ip:
#     print(f"Your public IP address is: {public_ip}") 

# API URL for your DNS zone records. Replace with your zone ID found in your Cloudflare Dashboard
url = "https://api.cloudflare.com/client/v4/zones/**YourZoneInformation**/dns_records/" 

# API keys in the environment variables to pull
authKey = os.getenv('cloudFlare_API_KEY')
authToken = os.getenv('cloudFlare_API_Token')
authToken = 'Bearer ' + str(authToken)

# Setting header json
headers = {
    "Content-Type": "application/json",
    "X-Auth-Email": "**youremail**",
    "X-Auth-Key": authKey,
    "Authorization": authToken
}

response = requests.get(url, headers=headers)
response = response.json()

# print(response['result']['content'])

# printing A record names
for record in response['result']:
    if record['type'] == 'A':
        name, id = record['name'], record['id']
        print(id)