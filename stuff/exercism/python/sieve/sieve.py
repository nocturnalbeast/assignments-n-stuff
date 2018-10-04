from math import sqrt

def sieve(limit):
    numbers = range(2,limit+1)
    for i in range(2,int(sqrt(limit))+1):
    	for j in range(i,limit):
    		if (i*j) in numbers:
    			numbers.remove(i*j)
    return numbers