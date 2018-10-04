from collections import Counter

dict_discount = {
	3 : 80,
	4 : 160,
	5 : 200
}
def calculate_total(books):
	return eval_disc(dict(Counter(books)))

def eval_disc(set_lst):
	cost = 0
	while len(set_lst) != 0:
		if len(set_lst) in dict_discount.keys():
			cost += (800 - dict_discount.get(len(set_lst))) * len(set_lst)
			for i in set_lst.keys():
				set_lst[i] -= 1
			set_lst = {key : value for key, value in set_lst.items() if value != 0}
		else:
			cost += 800 * sum(set_lst.values())
			set_lst = {}
	return cost