# Unraid Transfer data from another location

### Author: Joe Smith

### Date: 2024-12-26

### Description: This describes how to transfer data from another share directory to the unraid share we created

--- 

## Install Unassigned Devices

To make this data transfer slightly easier (maybe) I will be installed the the Unassigned Devices app which enables me to mount an SMB share to the Unraid server in order to call files from that share from the CLI easier

- Go to apps
- Look for **Unassigned Devices** and install
  
  ![alt text](<../Photos/Unraid/Transfer_Truenas_Data/Screenshot 2024-12-22 130925.png>)

  ![alt text](<../Photos/Unraid/Transfer_Truenas_Data/Screenshot 2024-12-22 130933.png>)

- Go to **Main** and ensure that you can now see the **Unassigned Devices** sections
  
  ![alt text](<../Photos/Unraid/Transfer_Truenas_Data/Screenshot 2024-12-22 130951.png>)

## Mount Truenas SMB share

- In the **Main** tab in the **Unassigned Devices** section go to **SMB Shares | NFS Shares | ISO Files Shares** 
  ![alt text](<../Photos/Unraid/Transfer_Truenas_Data/Screenshot 2024-12-22 130951.png>)

- Click on **ADD REMOTE SMB/NFS SHARE**
- Choose either the NFS or SMB icon. Click Next
  ![alt text](<../Photos/Unraid/Transfer_Truenas_Data/Screenshot 2024-12-22 130958.png>)
- Type in the IP or URL to your share
  ![alt text](<../Photos/Unraid/Transfer_Truenas_Data/Screenshot 2024-12-22 131008.png>)
- Type in the username for the SMB share
  ![alt text](<../Photos/Unraid/Transfer_Truenas_Data/Screenshot 2024-12-30 130142.png>)
- Type in the password
  ![alt text](<../Photos/Unraid/Transfer_Truenas_Data/Screenshot 2024-12-22 131027.png>)
- If needed type in your domain. I didnt need to type in a domain
  ![alt text](<../Photos/Unraid/Transfer_Truenas_Data/Screenshot 2024-12-22 131034.png>)
- Click on **LOAD SHARES**. Doing this it should load all of the shares on the server into a drop down. That way you know your previous information was correct
- Select the correct share and click done
  ![alt text](<../Photos/Unraid/Transfer_Truenas_Data/Screenshot 2024-12-22 131042.png>)
- You should see the Source now in the page
- Click on mount to mount the drive to the Unraid server
  
  ![alt text](<../Photos/Unraid/Transfer_Truenas_Data/Screenshot 2024-12-22 131054.png>)
  ![alt text](<../Photos/Unraid/Transfer_Truenas_Data/Screenshot 2024-12-22 131105.png>)


## Building Rsync command
Using Rsync will help if any of the data gets interrupted during the transfer. Rsync is used for data backups to make sure only the files that are NOT already up to date in the destination are transfer.

The basic layout of the command is:
    "rsync -avh source dest"

- Find the Source mounting point
  - Click on the hyperlink of the SMB share we just mounted
  - Find the folder that you want to transfer and copy the index of that
  ![alt text](<../Photos/Unraid/Transfer_Truenas_Data/Screenshot 2024-12-22 131149.png>)

- Find the Destination mounting point
  - Click on the shares
  - Click on the Hyperlink box with an arrow next to the name of the Share
  
  ![alt text](<../Photos/Unraid/Transfer_Truenas_Data/Screenshot 2024-12-30 131729.png>)
  - Copy the index
    ![alt text](<../Photos/Unraid/Transfer_Truenas_Data/Screenshot 2024-12-30 131912.png>)


The test command I used to test the data transfer that i built with the mounting points above:
    'rsync -avh "/mnt/remotes/192.168.89.213_TNSHARE/Plex/DivX Movies" "/mnt/user/PlexData"'

**Note** make sure that you have the forward slashes / configured correctly. If you dont want to include the folder in the transfer then include a trailing /. If you want to include the top folder and then all of the folders to be underneath that folder dont include the trailing /

Example:

    "/mnt/remotes/192.168.89.213_TNSHARE/Plex/DivX Movies"  "/mnt/user/PlexData" -> Builds out the following: "/mnt/user/PlexData/DivX Movies/...."
    "/mnt/remotes/192.168.89.213_TNSHARE/Plex/DivX Movies/"  "/mnt/user/PlexData" -> Builds out the following: "/mnt/user/PlexData/...."

## Run data transfer and verify

- SSH into the Unraid Server
- Copy the command that we built above and click enter
 ![alt text](<../Photos/Unraid/Transfer_Truenas_Data/Screenshot 2024-12-22 131502.png>)

 ![alt text](<../Photos/Unraid/Transfer_Truenas_Data/Screenshot 2024-12-22 131512.png>)

- Go to the Folder that you copied the data to and verify the data transferred
  ![alt text](<../Photos/Unraid/Transfer_Truenas_Data/Screenshot 2024-12-22 131526.png>) 
  
  ![alt text](<../Photos/Unraid/Transfer_Truenas_Data/Screenshot 2024-12-22 131532.png>)