from math import sqrt

def prime_factors(natural_number):
	pf_lst = []
	while natural_number % 2 == 0:
		pf_lst.append(2)
		natural_number /= 2
	for i in xrange(3,int(sqrt(natural_number))+1,2):
		while natural_number % i == 0:
			pf_lst.append(i)
			natural_number /= i
	if natural_number > 2:
		pf_lst.append(natural_number)
	return pf_lst