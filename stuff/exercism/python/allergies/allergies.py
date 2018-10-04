class Allergies(object):

	dict_algs = {
		1 : "eggs",
		2 : "peanuts",
		3 : "shellfish",
		4 : "strawberries",
		5 : "tomatoes",
		6 : "chocolate",
		7 : "pollen",
		8 : "cats"
	}

	lst = []

	def __init__(self, score):
		if self.lst != []:
			self.lst = []
		if score >= 256:
			score -= 256
		alg_index = map(int, list(bin(score))[:1:-1])
		for i in range(len(alg_index)):
			if alg_index[i] == 1:
				self.lst.append(self.dict_algs.get(i+1))

	def is_allergic_to(self,item):
		return (item in self.lst)