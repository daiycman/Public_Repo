# DNS Testing

### Author: Joe Smith

### Date: 2024-12-06

### Description: This describes how I set up my lab for comparing Cloudflare, NextDNS, OpenDNS, and Quad9

--- 

## PreReqs
- Set up accounts for Cloudflare, NextDNS, and if you want OpenDNS/Umbrella
- Set up, if you dont have it, a Linux desktop to run the bash script

## Gathering Malicious Domains
- I used https://urlhaus.abuse.ch/api/#hostfile
![alt text](<../../Photos/Cloudflare/DNS/Screenshot 2025-03-02 095703.png>)

- If you navigate to urlhause.abouse.ch you can click on the Access Data to see all of the options to choose from
![alt text](<../../Photos/Cloudflare/DNS/Screenshot 2025-03-02 095738.png>)

- Since I used the Hostfile you can click and download that file or use the [script I used here:](PythonScripts\URLHausExtract.py) 

## Linux Bash Script

- This is the script that I got from lawrence systems to run the test

        #!/bin/bash
        # Bulk DNS Lookup
        # Generates a CSV of DNS lookups from a list of domains.   
        #    
        # File name/path of domain list:    
        domain_list='Domains.txt' # One FQDN per line in file.    
        #    
        # IP address of the nameserver used for lookups:    
        ns1_ip='1.1.1.1' # Cloudflare    
        ns2_ip='9.9.9.9' # Quad9    
        ns3_ip='172.64.36.1' # Cloudflare Account Free Hosted    
        ns4_ip='45.90.28.131' # NextDNS Free
        ns5_ip='45.90.28.41' # NextDNS Custom
        ns6_ip='94.140.14.14' # Adguard Free
        ns7_ip='208.67.222.222' # OpenDNS
        #    
        # Seconds to wait between lookups:    
        loop_wait='1' # Is set to 1 second.    
            
        echo "Domain name, $ns1_ip,$ns2_ip,$ns3_ip,$ns4_ip,$ns5_ip,$ns6_ip,$ns7_ip "; # Start CSV    
        for domain in `cat $domain_list` # Start looping through domains    
        do    
            ip1=`dig @$ns1_ip +short $domain |tail -n1`; # IP address lookup DNS Server1    
            ip2=`dig @$ns2_ip +short $domain |tail -n1`; # IP address lookup DNS server2    
            ip3=`dig @$ns3_ip +short $domain |tail -n1`; # IP address lookup DNS server3    
            ip4=`dig @$ns4_ip +short $domain |tail -n1`; # IP address lookup DNS server4    
            ip5=`dig @$ns5_ip +short $domain |tail -n1`; # IP address lookup DNS server5    
            ip6=`dig @$ns6_ip +short $domain |tail -n1`; # IP address lookup DNS server6
            ip7=`dig @$ns7_ip +short $domain |tail -n1`; # IP address lookup DNS server7
                    echo "$domain,$ip1,$ip2,$ip3,$ip4,$ip5,$ip6,$ip7";    
        #    sleep $loop_wait # Pause before the next lookup to avoid flooding NS    
        done; 