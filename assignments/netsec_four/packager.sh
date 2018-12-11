#!/bin/bash

# Just a script to package the solution into the format I need.

ROLL='P2CSN18006'
INPF_ONE='udp_create.py'
OUTF_ONE='udp_create.py'
INPF_TWO='udp_parse.py'
OUTF_TWO='udp_parse.py'

rm -rf $ROLL
rm $ROLL.tar

mkdir $ROLL/1 -p
mkdir $ROLL/2 -p

cp $INPF_ONE $ROLL/1/$OUTF_ONE
cp $INPF_TWO $ROLL/2/$OUTF_TWO

tar -cf ./$ROLL.tar $ROLL

rm -rf $ROLL

echo 'Done!'
