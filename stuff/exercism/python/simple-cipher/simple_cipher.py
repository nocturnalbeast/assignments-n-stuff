import string, random

class Cipher(object):

	key = None

	def __init__(self, key=None):
		if key == None:
			self.key = ''.join(random.choice(string.ascii_lowercase) for i in range(30))
		else:
			if (filter(str.isalpha,key) != key) | (key != key.lower()) | (key == ''):
				raise ValueError("Invalid key!")
			self.key = key

	def two_way_func(self,enc_dec,text):
		tw_lst = list(text)
		if len(text) > len(self.key):
			self.key = (self.key * ((len(text)/len(self.key)) + 1))[:len(text)]
		for i in range(len(text)):
			tw_lst[i] = chr(ord(tw_lst[i]) + (enc_dec * (ord(self.key[i]) - ord('a'))))
			if ord(tw_lst[i]) > ord('z'):
				tw_lst[i] = chr(ord(tw_lst[i]) - 26)
			if ord(tw_lst[i]) < ord('a'):
				tw_lst[i] = chr(ord(tw_lst[i]) + 26)
		return ''.join(tw_lst)

	def encode(self, text):
		return self.two_way_func(1,text)

	def decode(self, text):
		return self.two_way_func(-1,text)

