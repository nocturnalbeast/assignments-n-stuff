#!/bin/bash

# update package lists before starting
sudo apt update
# install all necessary packages for KVM
sudo apt install qemu-kvm libvirt-clients libvirt-daemon-system bridge-utils virt-manager
# add the current user to the libvirt group
sudo adduser $USER libvirt
# add the current user to the libvirt-qemu group
sudo adduser $USER libvirt-qemu