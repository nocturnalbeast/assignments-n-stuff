#!/bin/bash

# Just a script to package the solution into the format I need.

ROLL='P2CSN18006'
INPF='subnetv2.py'
OUTF='subnet.py'

rm -rf $ROLL
rm $ROLL.tar

mkdir $ROLL/1 -p
cp $INPF $ROLL/1/$OUTF

tar -cf ./$ROLL.tar $ROLL

rm -rf $ROLL

echo 'Done!'