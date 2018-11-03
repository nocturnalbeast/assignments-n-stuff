#!/bin/bash

if [[ $# != 1 ]]
 then
  echo "Number of arguments passed to the script is wrong."
  echo -e "Use the script like \"$0 argument\" instead."
  exit
fi
echo $1 | rev
