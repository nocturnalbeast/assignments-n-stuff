import re

def abbreviate(words):
    word_list = re.findall(r'[A-Z]+', words.upper())
    acronym = ''
    for word in word_list:
    	acronym += word[0]
    return acronym