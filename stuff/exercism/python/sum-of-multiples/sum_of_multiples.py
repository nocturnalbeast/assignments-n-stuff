def sum_of_multiples(limit, multiples):
    if len(multiples) == 0:
    	return 0
    act_mults = []
    for i in range(1,limit+1):
    	for j in multiples:
    		if j*i < limit:
    			act_mults.append(j*i)
    return sum(set(act_mults))