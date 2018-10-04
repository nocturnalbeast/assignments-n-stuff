import re, operator

dict_oprs = {
	"plus" : operator.add,
	"minus" : operator.sub,
	"multiplied" : operator.mul,
	"divided" : operator.div
}

def isint(strn):
	try:
		int(strn)
		return True
	except ValueError:
		return False

def isopr(strn):
	return strn in dict_oprs.keys()

def calculate(question):
	lst_que = re.split(" ",re.sub(r'What\sis\s|\?|\sby','',question))
	for i in lst_que:
		if not isint(i) and not isopr(i):
			raise ValueError("Invalid question!")
	while len(lst_que) > 1:
		lst_que = [dict_oprs.get(lst_que[1])(int(lst_que[0]),int(lst_que[2]))] + lst_que[3:]
	return lst_que[0]