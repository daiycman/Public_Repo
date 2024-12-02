##########################################################################################################################
# Script Name: Cloudflare update DNS Record with IP
# Author: Joe Smith
# Date: 2023-12-10
# Description: This script utilizes the Cloudflare APIs to update the IP address of a record that is hosted. Because I live
#              With a dynamic IP that hosts my VPN solution i need to make sure that my houses public IP is always updated 
#              within cloudflare so my VPN clients can resolve the URL to the correct IP to connect
#              Because when i set up my domain in my homelab i used the same as the public domain i need to manually set
#              The records on my Domain Controllers if i ever need to call that URL i need them both to match to the IP
#              This also embeds powershell functions because i was too lazy to rewrite this in Powershell and windows works 
#              better with powershell and changing DC DNS records,
##########################################################################################################################

import requests
import os
import dns, dns.resolver
import subprocess, sys
import time
import logging


# Setting the Cloudflare API URL for your DNS record
# Replace with your zone and record UIDs
url = "https://api.cloudflare.com/client/v4/zones/**ZoneUID**/dns_records/**DNS UID**"

# setting the logging to the desktop and formating 
logging.basicConfig(filename='C:\\**LOCATIONtoSAVELOG**\\updateDNS.log', filemode='a', level=logging.INFO, format='%(asctime)s - %(levelname)s:%(message)s', datefmt='%m/%d/%Y %I:%M:%S %p')

# API call to cloudflare to retrieve current DNS record
def get_dns_record(headers):

    dnsresponse = requests.get(url, headers=headers)

    dnsresponse.close()

    # determining if we get the successful 200 response. if not exit the program and log error
    if dnsresponse.status_code != 200:
        logging.error(f'Failed to get CloudFlare DNS record with error code: {dnsresponse}')
        sys.exit(f'Failed to get CloudFlare DNS record with error code: {dnsresponse}')

    dnsresponse = dnsresponse.json()

    # Grabbing IP address from the JSON back from cloudflare
    dnsip = dnsresponse['result']['content']

    # return the IP from Cloudflare
    return dnsip

def get_local_dns_record(URLname):

    # Setting the resolver to a variable so we can edit it
    my_resolver = dns.resolver.Resolver()

    # setting the resolver to use the Domain Controller
    my_resolver.nameservers = ['**IP OF DC**']

    # resolving domain from the domain controller
    result = my_resolver.resolve(URLname, 'A')
    for ipval in result:
        value = ipval.to_text()

    # returning the local DNS record IP
    return value

# ingesting the current Public IP of the network and updating the domain on CloudFlare
def update_dns_record(ipaddress, URLname, headers):

    # creating the JSON for what Cloudflare accepts for the update API call
    updatedns = {
        "content": ipaddress,
        "name": URLname, # Replace
        "proxied": False,
        "type": "A",
        "ttl": 60
    }

    response = requests.put(url, headers=headers, json=updatedns)

    response.close()

    # determining if we get the successful 200 response. if not exit the program and log error
    if response.status_code != 200:
        logging.error(f'Failed to update CloudFlare DNS record with error code: {response}')
        sys.exit(f'Failed to update CloudFlare DNS record with error code: {response}')

    # logging sucessful update
    logging.info(f'Successfully updated CloudFlare DNS with the current Public IP: {ipaddress}')

    # printing sucessful update
    print(f'Successfully updated CloudFlare DNS with the current Public IP: {ipaddress}')

# Using a webpage to grab the network Public IP address
def get_public_ip(): 

    # trying to get the web page and erroring if it is not successful
    try: 
        response = requests.get('https://httpbin.org/ip') 

        # if the response code is 200 extract the public IP from the json and return the IP
        if response.status_code == 200: 
            ip_data = response.json() 
            public_ip = ip_data.get('origin') 
            public_ip = str(public_ip)
            return public_ip 
        else: 
            logging.error(f'Failed to update CloudFlare DNS record with error code: {response}')
            sys.exit(f'Failed to update CloudFlare DNS record with error code: {response}')
    except Exception as e: 
        print(f"Error: {e}") 

    response.close()

# Python running a powershell script to remove the old DNS record for the domain on the domain controller
def remove_local_dns():

    proc = subprocess.Popen(['powershell.exe', 'Remove-DnsServerResourceRecord -Name **DNSrecord** -ZoneName **DC ZoneName** -RRType A -Force'], stdout=subprocess.PIPE, stderr=subprocess.PIPE)

    proc.kill

# Python running a powershell script to add the new DNS record for the domain on the domain controller
def add_local_dns(ipaddress):
    proc = subprocess.Popen(['powershell.exe', f'Add-DnsServerResourceRecordA -Name **DNSrecord** -ZoneName **DC ZoneName** -AllowUpdateAny -IPv4Address {ipaddress} -TimeToLive 00:01:00'], stdout=subprocess.PIPE, stderr=subprocess.PIPE)

    proc.kill

if __name__ == "__main__":

    # Ingesting the API requirements from environment variables
    authKey = os.getenv('cloudFlare_API_KEY')
    authToken = os.getenv('cloudFlare_API_Token')
    authToken = 'Bearer ' + str(authToken)

    # Setting URL variable that is used to find the DNS record
    URLname = 'yourURLname' #replace

    # setting headers needed for the api call to cloudflare
    headers = {
        "Content-Type": "application/json",
        "X-Auth-Email": "**email of your admin**",
        "X-Auth-Key": authKey,
        "Authorization": authToken
    }

    # Get the public IP address of my home network
    public_ip = get_public_ip() 

    # Get the IP address hosted in Cloudflare
    dns_ip = get_dns_record(headers)

    # get local dns
    local_dns_record = get_local_dns_record(URLname)

    # Determining if the CloudFlare DNS record matches the Public IP address of the Network and then updating CloudFlare record if needed
    if dns_ip != public_ip:
        print(f"Your public IP address is: {public_ip}\n") 
        logging.info(f"Your public IP address is: {public_ip}")

        # Calling the update CloudFlare DNS record
        update_dns_record(public_ip, URLname, headers)
    else:
        print("Your public IP address is already up to date in CloudFlare\n")
        logging.info("Your public IP address is already up to date in CloudFlare")

    # Determining if the Domain Controller DNS record matches the Public IP Address of the Network and then removing the old record and adding the new record
    if local_dns_record != public_ip:
        print(f"Your current local dns record is: {local_dns_record}\n") 
        logging.info(f"Your current local dns record is: {local_dns_record}") 

        # Calling the removal and addition of the new local DNS record
        remove_local_dns()
        add_local_dns(public_ip)

        # Giving time for the Domain Controller to fully replicate prior to polling the DNS record
        time.sleep(3)
        local_dns_record = get_local_dns_record()

        # Print and log the new dns record from domain controller
        print(f'Your new local dns record is: ' + local_dns_record)
        logging.info(f'Your new local dns record is: ' + local_dns_record)
    else:
        print('Your local DNS is up to date')
        logging.info('Your local DNS is up to date')