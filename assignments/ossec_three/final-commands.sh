#!/bin/bash

# make command to clean working directory
make clean

# make command to compile the module
make modules

# command to insert module
sudo insmod ftrace-hook.ko

# dmesg to view kernel level messages
dmesg --follow

# command to remove the module from the kernel
sudo rmmod ftrace-hook
