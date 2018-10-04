from math import sqrt

def gen_prime_list(num):
    numbers = range(2,num+1)
    for i in range(2,int(sqrt(num))+1):
    	for j in range(i,num):
    		if (i*j) in numbers:
    			numbers.remove(i*j)
    return numbers

def nth_prime(positive_number):
	return gen_prime_list(positive_number**2)[positive_number]
