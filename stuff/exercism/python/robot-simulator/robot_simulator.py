# Globals for the bearings
# Change the values as you see fit
NORTH = 0
EAST = 1
SOUTH = 2
WEST = 3

class Robot(object):

	pos_x = 0
	pos_y = 0
	bearing = 'N'
	coordinates = (0,0)

	def __init__(self, dirn=NORTH, x=0, y=0):
		self.pos_x = x
		self.pos_y = y
		self.bearing = dirn
		self.coordinates = (x,y)

	def turn_left(self):
		if self.bearing == NORTH:
			self.bearing = WEST
		else:
			self.bearing = self.bearing - 1

	def turn_right(self):
		self.bearing = (self.bearing + 1) % 4

	def advance(self):
		if self.bearing in [0,2]:
			self.pos_y += (self.bearing - 1)*(-1)
		elif self.bearing in [1,3]:
			self.pos_x += (self.bearing - 2)*(-1)
		self.coordinates = (self.pos_x,self.pos_y)

	def simulate(self, string):
		for i in string:
			if i == 'A':
				self.advance()
			elif i == 'L':
				self.turn_left()
			elif i == 'R':
				self.turn_right()