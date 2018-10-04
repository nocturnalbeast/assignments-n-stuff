def distance(strand_a, strand_b):
	if len(strand_a) != len(strand_b):
		raise ValueError("Strings are not of the same length!")
	hamm_dist = 0
	for i in range(len(strand_a)):
		if strand_a[i] != strand_b[i]:
			hamm_dist += 1
	return hamm_dist
	