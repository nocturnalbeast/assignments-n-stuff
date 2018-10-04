import re

class Matrix(object):

	mat = None
	rows = 0
	cols = 0

	def __init__(self, matrix_string):
		elements = map(int,re.findall(r'[0-9]+',matrix_string))
		self.rows = len(re.findall(r'[\n]',matrix_string)) + 1
		self.cols = len(elements) / self.rows
		self.mat = [[0 for i in range(self.cols)] for j in range(self.rows)]
		ele_cont = 0
		for i in range(self.rows):
			for j in range(self.cols):
				self.mat[i][j] = elements[ele_cont]
				ele_cont += 1

	def row(self, index):
		return self.mat[index]

	def column(self, index):
		col = []
		for i in range(self.rows):
			col.append(self.mat[i][index])
		return col