#!/bin/bash

read -p "Enter a string: " ONE_STRING
RES=`echo $ONE_STRING | wc -c`
expr $RES - 1