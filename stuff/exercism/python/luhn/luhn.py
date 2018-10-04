import re

class Luhn(object):

	num = '0'
	cln_num = '0'

	def __init__(self, card_num):
		self.num = card_num
		self.cln_num = re.sub(r'\s',r'',self.num)

	def is_valid(self):
		if (filter(str.isdigit,self.cln_num) != self.cln_num) | (len(self.cln_num) < 2):
			return False
		else:
			sum = 0
			num_list = [int(x) for x in self.cln_num]
			leng_list = len(num_list)
			for i in range(leng_list):
				if (leng_list - i) % 2 == 0:
					num_list[i] *= 2
				if num_list[i] > 9:
					num_list[i] -= 9
				sum += num_list[i]
			return (sum % 10 == 0)