#!/bin/python

import math
import os
import random
import re
import sys



#
# Complete the 'scatterPalindrome' function below.
#
# The function is expected to return an INTEGER_ARRAY.
# The function accepts STRING_ARRAY strToEvaluate as parameter.
#

def scatterPalindrome(strToEvaluate):
    lst_ans = []
    for str_eval in strToEvaluate:
        lst_all_substrings = []
        lst_possible_palindromes = []
        length_string = len(str_eval)
        for idx_one in range(length_string):
            for idx_two in range(length_string):
                lst_all_substrings.append(str_eval[idx_one:idx_two+1])
        lst_all_substrings = [element for element in lst_all_substrings if element != ""]
        for element in lst_all_substrings:
            split_list = list(element)
            dict_count = {character:0 for character in split_list}
            for character in split_list:
                dict_count[character] = dict_count[character] + 1
            if (len(element) % 2) == 0:
                occ_chk_lst = [val%2 for val in dict_count.values()]
                if 1 not in occ_chk_lst:
                    lst_possible_palindromes.append(element)
            else:
                occ_chk_lst = [val%2 for val in dict_count.values()]
                if occ_chk_lst.count(1) == 1:
                    lst_possible_palindromes.append(element)
        lst_ans.append(len(lst_possible_palindromes))
    return lst_ans


if __name__ == '__main__':
    fptr = open(os.environ['OUTPUT_PATH'], 'w')

    strToEvaluate_count = int(raw_input().strip())

    strToEvaluate = []

    for _ in xrange(strToEvaluate_count):
        strToEvaluate_item = raw_input()
        strToEvaluate.append(strToEvaluate_item)

    result = scatterPalindrome(strToEvaluate)

    fptr.write('\n'.join(map(str, result)))
    fptr.write('\n')

    fptr.close()
