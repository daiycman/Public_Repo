# Unraid Initial Settings

### Author: Joe Smith

### Date: 2024-12-27

### Description: This describes what first settings that I enabled and set up

--- 

### Settings Layout

![alt text](<../Photos/Unraid/Initial_Settings/Screenshot 2024-12-21 104210.png>)

## Date and Time

Only thing to change here would be to convert to your time zone. You could change the NTP if you have a particular NTP server you like to use

![alt text](<../Photos/Unraid/Initial_Settings/Screenshot 2024-12-21 104140.png>)

## Docker

By default the Docker settings are enabled. If you need to make certain changes Unraid will force you to disable it. Remember to enable it. 

![alt text](<../Photos/Unraid/Initial_Settings/Screenshot 2024-12-21 104154.png>)

## Management Access

Within the management access I enabled **SSH** and **Use SSL**. I wouldn't recommend enabling Telnet or UPnP

![alt text](<../Photos/Unraid/Initial_Settings/Screenshot 2024-12-21 104132.png>)

## NFS

If you have any linux boxes that don't support SMB for file shares, then you will need to enable NFS.

![alt text](<../Photos/Unraid/Initial_Settings/Screenshot 2024-12-21 104202.png>)

## SMB

SMB is enabled by default. I kept everything default, but you could change the workgroup name to be your domain if you would like but it doesn't do much for you

![alt text](<../Photos/Unraid/Initial_Settings/Screenshot 2024-12-30 123333.png>)

## FTP

If you need to have file transfers using FTP you can enable FTP but for me thats not something I need

![alt text](<../Photos/Unraid/Initial_Settings/Screenshot 2024-12-21 104225.png>)

## Syslog Server

I don't have the need for a syslog server or for my server to hold those syslogs

![alt text](<../Photos/Unraid/Initial_Settings/Screenshot 2024-12-30 123424.png>)

## VPN Manager

Unraid has the ability to host a wireguard VPN so you can remote back into your environment. I host my wireguard on my firewall

![alt text](<../Photos/Unraid/Initial_Settings/Screenshot 2024-12-30 123432.png>)