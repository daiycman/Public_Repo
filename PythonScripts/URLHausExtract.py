import requests
import re

# Download URLhaus feed
urlhaus_feed = "https://urlhaus.abuse.ch/downloads/hostfile/"
response = requests.get(urlhaus_feed)

# Regex to match domain-based URLs (excluding IPs)
# domain_regex = re.compile(r'(?!\d{1,3}\.\d{1,3}\.\d{1,3}\.\d{1,3})[a-zA-Z0-9.-]+\.(?:com|net|org)')
# domain_regex = re.compile(r'(?!\d{1,3}\.\d{1,3}\.\d{1,3}\.\d{1,3}\s)[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}$')
# domain_regex = re.compile(r'(?<=\s)([a-zA-Z0-9.-]+\.[a-zA-Z]{2,})')
domain_regex = re.compile(r'([a-zA-Z0-9.-]+\.[a-zA-Z]{2,})')
# File to save

path = r''

# Extract and filter URLs
valid_urls = set(domain_regex.findall(response.text))


#print(valid_urls)

# Save to file
with open(path, "w") as f:
    for url in valid_urls:
        f.write(url + "\n")

print(f"Extracted {len(valid_urls)} valid domain-based URLs.")
