#!/bin/python

import math
import os
import random
import re
import sys



#
# Complete the 'lotteryCoupons' function below.
#
# The function is expected to return an INTEGER.
# The function accepts INTEGER n as parameter.
#

def lotteryCoupons(n):
    list_numbers = [str(i) for i in range(1,n+1)]
    for idx in range(len(list_numbers)):
        sum_num = [int(num) for num in list(list_numbers[idx])]
        list_numbers[idx] = sum(sum_num)
    dict_count = {num:0 for num in list_numbers}
    for num in list_numbers:
        dict_count[num] = dict_count[num] + 1
    return len([(key, dict_count[key]) for key in dict_count.keys() if dict_count[key] == max(dict_count.values())])

if __name__ == '__main__':
    fptr = open(os.environ['OUTPUT_PATH'], 'w')

    n = int(raw_input().strip())

    result = lotteryCoupons(n)

    fptr.write(str(result) + '\n')

    fptr.close()
