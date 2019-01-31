#!/bin/bash

# update lists
sudo apt update
# install build deps
sudo apt-get install build-essential libtool autotools-dev automake pkg-config bsdmainutils python3
# install program deps
sudo apt-get install libssl-dev libevent-dev libboost-system-dev libboost-filesystem-dev libboost-chrono-dev libboost-test-dev libboost-thread-dev
# software config deps
sudo apt-get install software-properties-common
# add bitcoin client repo
sudo add-apt-repository ppa:bitcoin/bitcoin
# update apt lists
sudo apt-get update
# optional deps, need for full function
sudo apt-get install libdb4.8-dev libdb4.8++-dev
sudo apt-get install libminiupnpc-dev
sudo apt-get install libzmq3-dev
# gui deps
sudo apt-get install libqt5gui5 libqt5core5a libqt5dbus5 qttools5-dev qttools5-dev-tools libprotobuf-dev protobuf-compiler
sudo apt-get install libqrencode-dev

# clone repo and cd
git clone https://github.com/bitcoin/bitcoin
cd ./bitcoin
# build
./autogen.sh
./configure
make
make install