# Unraid Link Aggregation Group Configuration with Cisco Switch

### Author: Joe Smith

### Date: 2024-12-26

### Description: This describes how to set up a LACP link aggregation group on unraid and the configurations needed on a Cisco switch for LACP port channel

--- 

## Network Setting on Unraid

- Go to Settings
- Go to Network Settings
  - If needed turn off VM Manager and Docker
- Change the bonding mode from **Active-backup** to **802.3ad**
- Click Apply

![alt text](<../Photos/Unraid/LAG_Configuration/Screenshot 2024-12-21 165935.png>)

![alt text](<../Photos/Unraid/LAG_Configuration/Screenshot 2024-12-21 165948.png>)


## Configure Cisco Switch

- Log into the Cisco switch
- Configure the switchports
  - Assign the switchport to a channel group. This will also create the port channel for the switch:
  
    channel-group x mode active

- Configure the port channel
  - Configure the portchannel as an access port
  - Configure the portchannel to the vlan
  - Make the port a spanning-tree portfast to make sure that the switch knows there is a host on the other side:
  
    switchport mode access
    switchport access vlan x
    spanning-tree portfast

![alt text](<../Photos/Unraid/LAG_Configuration/Screenshot 2024-12-21 170501.png>)

![alt text](<../Photos/Unraid/LAG_Configuration/Screenshot 2024-12-21 170510.png>)