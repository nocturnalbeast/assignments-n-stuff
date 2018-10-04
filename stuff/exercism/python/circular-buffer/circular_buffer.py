class BufferFullException(Exception):
	print "The buffer is full!"

class BufferEmptyException(Exception):
	print "The buffer is empty!"

class CircularBuffer(object):

	circ_buf_lst = []
	index = 0
	capacity = 0

	def __init__(self, capacity):
		self.circ_buf_lst = [None] * capacity
		self.capacity = capacity
		self.index = 0

	def read(self):
		if self.circ_buf_lst[self.index] == None:
			raise BufferEmptyException("Empty!")
		else:
			ele = self.circ_buf_lst[self.index]
			self.clear()
			return ele

	def write(self, data):
		if self.circ_buf_lst[(self.index + 1) % self.capacity] != None:
			raise BufferFullException("Full!")
		else:
			self.overwrite(data)

	def overwrite(self, data):
		self.index = (self.index + 1) % self.capacity
		self.circ_buf_lst[self.index] = data

	def clear(self):
		self.circ_buf_lst[self.index] = None
		if self.index == 0:
			self.index = self.capacity-1
		else:
			self.index -= 1

buf = CircularBuffer(2)
buf.write('1')
buf.write('2')
print buf.read()
print buf.read()