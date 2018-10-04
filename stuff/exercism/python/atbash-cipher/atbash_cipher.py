from string import maketrans
import re

def two_way_func(text):
	key = 'abcdefghijklmnopqrstuvwxyz'
	return filter(str.isalnum,text.lower()).translate(maketrans(key,key[::-1]))

def encode(plain_text):
	return re.sub(r'([a-z0-9]{5})(?=[a-z0-9]+)',r'\1 ',two_way_func(plain_text))

def decode(ciphered_text):
	return two_way_func(ciphered_text)
