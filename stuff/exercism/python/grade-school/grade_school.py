class School(object):
	def __init__(self):
		self.nme_lst = [[], [], [], [], [], [], [], [], [], []]

	def add_student(self, name, grade):
		self.nme_lst[grade-1].append(name)

	def roster(self):
		srtd_lst = []
		for lst in self.nme_lst:
			srtd_lst += sorted(lst)
		return srtd_lst

	def grade(self, grade_number):
		return sorted(self.nme_lst[grade_number-1])