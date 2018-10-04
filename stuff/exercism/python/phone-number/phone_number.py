class Phone(object):
	def __init__(self, phone_number):
		self.number = filter(str.isdigit,phone_number)
		if len(self.number) == 11 and self.number[0] == '1':
			self.number = self.number[1:]
		self.area_code, self.exchange_code = self.number[0:3], self.number[3:6]
		if len(self.number) != 10 or self.exchange_code[0] in ['0','1'] or self.area_code[0] in ['0','1']:
			raise ValueError("Invalid number!")

	def pretty(self):
		return '(' + self.area_code + ') ' + self.exchange_code + '-' + self.number[6:]