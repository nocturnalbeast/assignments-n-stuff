#!/bin/bash

# Radxa setup script - part one

# get new list with better mirrors
echo "deb http://mirror.cse.iitk.ac.in/debian jessie main contrib non-free" >> newlist.list
echo "deb-src http://mirror.cse.iitk.ac.in/debian jessie main contrib non-free" >> newlist.list
echo "deb http://mirror.cse.iitk.ac.in/debian jessie-updates main contrib non-free" >> newlist.list
echo "deb-src http://mirror.cse.iitk.ac.in/debian jessie-updates main contrib non-free" >> newlist.list
echo "deb http://mirror.cse.iitk.ac.in/debian-security jessie/updates main contrib non-free" >> newlist.list
echo "deb-src http://mirror.cse.iitk.ac.in/debian-security jessie/updates main contrib non-free" >> newlist.list

# replace the list with the new one
cp /etc/apt/sources.list ./list.bak
sudo mv ./newlist.list /etc/apt/sources.list

# setup ethernet interface
echo "Enter the IP address end:"
read ADDR
echo "#source-directory /etc/network/interfaces.d" >> ./newinterfaces
echo "" >> ./newinterfaces
echo "auto lo" >> ./newinterfaces
echo "iface lo inet loopback" >> ./newinterfaces
echo "" >> ./newinterfaces
echo "auto eth0" >> ./newinterfaces
echo "iface eth0 inet static" >> ./newinterfaces
echo "address 192.168.219.${ADDR}" >> ./newinterfaces
echo "netmask 255.255.254.0" >> ./newinterfaces
echo "#gateway 192.168.219.1" >> ./newinterfaces
echo "#dns-nameservers 10.30.60.2 10.30.8.102" >> ./newinterfaces

# move configuration file to proper location
cp /etc/network/interfaces ./interfaces.bak
sudo mv ./newinterfaces /etc/network/interfaces