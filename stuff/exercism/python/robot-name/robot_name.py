import string
from random import choice, randint

class Robot(object):
	
	def __init__(self,name='XX000'):
		self.name = name

	def reset(self):
		if self.name != None:
			self.name = ''
		self.name = choice(string.ascii_uppercase) + choice(string.ascii_uppercase) + str(randint(0, 9)) + str(randint(0, 9)) + str(randint(0, 9))
