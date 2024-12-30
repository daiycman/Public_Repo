# Unraid Initial Install of Plex App

### Author: Joe Smith

### Date: 2024-12-26

### Description: This describes how to do the initial install of the Plex app on Unraid

--- 

## Install Plex App
- Go to Apps
- Search **Plex Media Server**
- Install the official **Plex-Media-Server** App
  ![alt text](<../Photos/Unraid/PlexInstall/Screenshot 2024-12-22 131849.png>)

## Configure Plex Docker
On first install Unraid will automatically prompt you to configure the docker, but if you need to go back later the Plex Docker is in the Docker Tab
- Give the Docker a name if you want to change the default
- Network Type:
  - Host - assigned the IP address of the Unraid Server to the Docker Container
  - Custom : br0 - This gives you the ability to assign a separate IP address to the docker Container
-  Host Path 2:
   -  Assign a share folder for the transcode folder. It doesnt matter much. Just pick a folder or create one for this docker
-  Host Path 3:
   -  Same thing as Host 2. Assign it a folder or create one
  
  ![alt text](<../Photos/Unraid/PlexInstall/Screenshot 2024-12-22 131934.png>)
  
  ![alt text](<../Photos/Unraid/PlexInstall/Screenshot 2024-12-22 131951.png>)

-  Add Additional paths for Linking our Unraid Share files to the docker container
   -  Click on Add another path
   -  Config Type: Path
   -  Name: Give it a name
   -  Container Path: This is what you will see inside of the plex server example: /Movies
   -  Host Path: The folder in the Unraid Share that hosts the files you want to use in Plex
   -  Access Mode: Read/Write
   -  Click on Add
  
    ![alt text](<../Photos/Unraid/PlexInstall/Screenshot 2024-12-22 133625.png>) 
    
    ![alt text](<../Photos/Unraid/PlexInstall/Screenshot 2024-12-22 133655.png>)

-  Click apply
  
  ![alt text](<../Photos/Unraid/PlexInstall/Screenshot 2024-12-22 133705.png>)

  ![alt text](<../Photos/Unraid/PlexInstall/Screenshot 2024-12-22 132026.png>) 
  
  ![alt text](<../Photos/Unraid/PlexInstall/Screenshot 2024-12-22 132036.png>)

## Configure Plex Server

This will configure the movies sections to get Plex to recognize your files on Unraid

- From the Unraid Dashboard
- Right Click on the Plex Media Server Icon and Click WebUI
  
  ![alt text](<../Photos/Unraid/PlexInstall/Screenshot 2024-12-22 132227.png>)

- Plex should load
- Sign into the Plex Server with your account or create an account
- From the Plex Home
- Click More
  
  ![alt text](<../Photos/Unraid/PlexInstall/Screenshot 2024-12-22 133720.png>)

- Click on the elipses on the right of the server name
- Click on Manage Server -> Settings
  
  ![alt text](<../Photos/Unraid/PlexInstall/Screenshot 2024-12-22 133801.png>)

- On the left go down to libraries
  
  ![alt text](<../Photos/Unraid/PlexInstall/Screenshot 2024-12-22 133818.png>)

- Click on **add Library**
  
  ![alt text](<../Photos/Unraid/PlexInstall/Screenshot 2024-12-22 133825.png>)

- Select the type of media you are going to link. Click next
  
  ![alt text](<../Photos/Unraid/PlexInstall/Screenshot 2024-12-22 133830.png>)

- Click **Browse for Media Folder**
  
  ![alt text](<../Photos/Unraid/PlexInstall/Screenshot 2024-12-22 133837.png>)

- Find the Folder that you created above
  
  ![alt text](<../Photos/Unraid/PlexInstall/Screenshot 2024-12-22 133846.png>)

- Click **Add Library**
  
  ![alt text](<../Photos/Unraid/PlexInstall/Screenshot 2024-12-22 133852.png>)
  
- Repeat for the other types of media