# Unraid Initial Configuration

### Author: Joe Smith

### Date: 2024-12-26

### Description: This describes how to do the initial install of Unraid NAS

--- 

## PreReqs:
- 2GB+ USB with a Globally Unique Identifier (GUID)
  - USB's that I have used and has a GUID:
  ![alt text](<../Photos/Unraid/Initial_Install/Screenshot 2024-12-26 133323.png>)
- Hardware for the Unraid System
  - System in this build:
    - Supermicro X10DRU-i+ , Version 0123456789
    - Intel® Xeon® CPU E5-2680 v4 @ 2.40GHz
    - 32GB RAM

## Prepping the USB Drive
- Go to unraid.net and download the USB Flash Creator
  ![alt text](<../Photos/Unraid/Initial_Install/Screenshot 2024-12-26 132341.png>)
- Click on Product and getting started
  ![alt text](<../Photos/Unraid/Initial_Install/Screenshot 2024-12-26 132355.png>)
- Download for your OS
  ![alt text](<../Photos/Unraid/Initial_Install/Screenshot 2024-12-26 132401.png>)
- Once Download launch the USB Flash Creator
  ![alt text](<../Photos/Unraid/Initial_Install/Screenshot 2024-12-26 133129.png>)
- Select the Latest Unraid OS and the USB that your inserted (Ensure that the USB has A GUID!!!)
  ![alt text](<../Photos/Unraid/Initial_Install/Screenshot 2024-12-26 133136.png>)
  ![alt text](<../Photos/Unraid/Initial_Install/Screenshot 2024-12-26 133213.png>)
- Once you have selected those items click Next
  ![alt text](<../Photos/Unraid/Initial_Install/Screenshot 2024-12-20 143704.png>)
- Enter in the information for the server, IP address, Name, Netmask, Gateway, etc
  ![alt text](<../Photos/Unraid/Initial_Install/Screenshot 2024-12-20 143946.png>)
- Once you get the notification that the install in done, eject the USB and plug it into the server
  ![alt text](<../Photos/Unraid/Initial_Install/Screenshot 2024-12-20 144548.png>)

## Booting the server from USB

- Your server should boot directly from the USB as that should be the only drive that has an OS
  - If your server does not boot from the USB, reboot the server, and go into the BIOS
  - Select the USB from BIOS to be booted from
- You should see the USB having an output of a boot and should end up at a login screen
  ![alt text](<../Photos/Unraid/Initial_Install/Screenshot 2024-12-20 145359.png>)
- Go to a web browser and go to the IP address ex: http://192.168.89.215 or if you left the name default you should be able to navigate to unraid.local
- It will show the GUI and prompting for a new Password. Set a strong password
  ![alt text](<../Photos/Unraid/Initial_Install/Screenshot 2024-12-20 150445.png>)
- Once you set the password you will be prompted with the "start free 30 day trial" or "purchase key". Click on either one and be redirected to the Unraid Account manager
  ![alt text](<../Photos/Unraid/Initial_Install/Screenshot 2024-12-20 150549.png>)
- Login or create an account for Unraid
  
  ![alt text](<../Photos/Unraid/Initial_Install/Screenshot 2024-12-26 134300.png>)
- From the Unraid Account manager page, on the left side panel, click on start trial
  ![alt text](<../Photos/Unraid/Initial_Install/Screenshot 2024-12-26 134326.png>)
- Click on confirm trial start
  
  ![alt text](<../Photos/Unraid/Initial_Install/Screenshot 2024-12-26 134346.png>)
- Once completed you will be presented with this screen and when you click back to unraid you will see the Unraid server should Trial
  ![alt text](<../Photos/Unraid/Initial_Install/Screenshot 2024-12-26 134728.png>)
  ![alt text](<../Photos/Unraid/Initial_Install/Screenshot 2024-12-20 151014.png>)

## Assign your Parity and Disk for the Array

- Click on main and you will see a list of drop downs for your Parity and Disks
- Assign your Parity and Disk
  ![alt text](<../Photos/Unraid/Initial_Install/Screenshot 2024-12-20 150812.png>)
- Start your Array
  - This will kick off a parity check. My 12 TB Parity took ~ 26 hours
  ![alt text](<../Photos/Unraid/Initial_Install/Screenshot 2024-12-26 135216.png>)
- You will see that your disk is giving a warning. Check the box to "Yes, I want to do this" and then click on format to kick off the formatting
  ![alt text](<../Photos/Unraid/Initial_Install/Screenshot 2024-12-20 151115.png>)


---

That's it. You should be up and running Unraid on your new server.