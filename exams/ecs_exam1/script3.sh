#!/bin/bash

if [[ $# != 2 ]]
 then
  echo "Error in the number of arguments! Try again."
  exit
 else
  echo "The sum is $[ $1 + $2 ]."
  echo "The product is $[ $1 * $2 ]."
fi