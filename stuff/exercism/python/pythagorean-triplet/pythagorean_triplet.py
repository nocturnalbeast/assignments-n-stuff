from math import sqrt

def euclid_gcd(m,n):
	while n > 0:
		m,n = n,m%n
	return m

def primitive_triplets(number_in_triplet):
	if number_in_triplet % 2 != 0:
		raise ValueError("Odd number!")
	n_one = number_in_triplet / 2
	fact_pair = [(i,n_one/i) for i in xrange(1, int(sqrt(n_one)+1) )if n_one % i == 0]
	cop_fp = [(m,n) for (m,n) in fact_pair if euclid_gcd(n,m) == 1]
	triplet_set = [tuple(sorted((abs(m**2-n**2),2*m*n,m**2+n**2))) for (m,n) in cop_fp]
	return set(triplet_set)

def triplets_in_range(range_start, range_end):
	lst_trip = []
	for i in xrange(range_start,range_end+1):
		for j in xrange(i,range_end+1):
			pair = i**2 + j**2
			if (pair <= range_end**2) & ((int(sqrt(pair)))**2 == pair):
				lst_trip.append((i,j,int(sqrt(pair))))
	return set(lst_trip)

def is_triplet(triplet):
	trip_lst = sorted(list(triplet))
	return trip_lst[0]**2 + trip_lst[1]**2 == trip_lst[2]**2