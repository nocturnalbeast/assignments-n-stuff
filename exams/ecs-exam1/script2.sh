#!/bin/bash

for (( i=1 ; i < 11 ; i++ ))
do
 if [[ $(expr $i % 2) == 0 ]]
 then
  echo -e "$i\teven"
 else
  echo -e "$i\todd"
 fi
done