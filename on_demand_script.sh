#!/bin/bash

cd ~

# Let's get the repository
sudo dnf -y install git-all
git clone https://github.com/danielHett/personal-website

ls -a

# Get the folder that contains the index.html file. 
THE_PATH=$(find . -name "index.html")
PATH_PARTS=(${THE_PATH//\/index.html/ })
FOLDER_PATH=${PATH_PARTS[0]}  
echo $FOLDER_PATH

# Use that path to start the web server!
sudo /usr/bin/python3 -m http.server 80 -d $FOLDER_PATH