def classify(number):
	if number < 1:
		raise ValueError("Zero and negative numbers not allowed!")
	factors = []
	for i in range(1,number):
		if number % i == 0:
			factors.append(i)
	sum_nums = sum(factors)
	if sum_nums == number:
		return "perfect"
	elif sum_nums > number:
		return "abundant"
	elif sum_nums < number:
		return "deficient"