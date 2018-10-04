SUBLIST = 'sub'
SUPERLIST = 'super'
EQUAL = 'eq'
UNEQUAL = 'uneq'

def check_lists(first_list, second_list):
	sup_flag = False
	bool_ins = False
	if len(first_list) > len(second_list):
		first_list , second_list = second_list , first_list
		sup_flag = True
	if first_list == second_list:
		return EQUAL
	elif len(second_list) > len(first_list):
		for i in range(len(second_list)-len(first_list)+1):
			if second_list[i:i+len(first_list)] == first_list:
				bool_ins = True
				break
		if bool_ins:
			if sup_flag:
				return SUPERLIST
			else:
				return SUBLIST
	if not bool_ins:
		return UNEQUAL