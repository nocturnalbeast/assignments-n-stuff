def factors(num,min_fct,max_fct):
	lst_fact = []
	for i in xrange(1,int(num**0.5)+1):
		if num % i == 0:
			if i in range(min_fct,max_fct+1) and num/i in range(min_fct,max_fct+1):
				lst_fact.append((i,num/i))
	return lst_fact

def largest_palindrome(min_factor, max_factor):
	if min_factor >= max_factor:
		raise ValueError("Invalid range!")
	flg = False
	for i in reversed(range(min_factor,max_factor+1)):
		for j in reversed(range(min_factor,i+1)):
			x = i*j
			if str(x) == str(x)[::-1]:
				return (x,factors(x,min_factor,max_factor))
				flg = True
	if not flg:
		raise ValueError("No elements in range!")

def smallest_palindrome(min_factor, max_factor):
	if min_factor >= max_factor:
		raise ValueError("Invalid range!")
	flg = False
	for i in range(min_factor,max_factor+1):
		for j in range(i,max_factor+1):
			x = i*j
			if str(x) == str(x)[::-1]:
				return (x,factors(x,min_factor,max_factor))
				flg = True
	if not flg:
		raise ValueError("No elements in range!")