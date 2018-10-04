from operator import mul

def largest_product(series, size):
	if size < 0:
		raise ValueError("Invalid size!")
	subs = []
	for i in range(len(series)-size+1):
		subs.append(map(int,list(series[i:i+size])))
	for i in range(len(subs)):
		subs[i] = reduce(mul,subs[i],1)
	return max(subs)