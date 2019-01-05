#!/bin/bash

# Radxa setup script - part two

# update and install software
sudo apt update
sudo apt upgrade
sudo apt autoremove
sudo apt autoclean

# install python2 and python3 pips
sudo apt install python3-pip -y
sudo apt install python-pip -y

# install pyserial library
sudo apt install python-serial python3-serial -y

# install VNC server
sudo apt install tightvncserver
vncserver
vncserver -kill :1
mv ~/.vnc/xstartup ~/.vnc/xstartup.bak
touch ~/.vnc/xstartup
sudo sed -i '$ \#\!/bin/bash\nxrdb \$HOME\/\.Xresources\nexec mate-session \&' ~/.vnc/xstartup
sudo chmod +x ~/.vnc/xstartup

# install mosquitto
sudo apt install mosquitto mosquitto-clients -y
sudo systemctl disable mosquitto.service