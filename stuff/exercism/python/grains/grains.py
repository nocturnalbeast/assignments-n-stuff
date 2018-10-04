def check_range(integer_number):
	if integer_number not in range(1,65):
		raise ValueError("Out of bounds!")

def on_square(integer_number):
	check_range(integer_number)
	return 2**(integer_number-1)

def total_after(integer_number):
	check_range(integer_number)
	sum = 0
	for i in range(integer_number):
		sum += 2**i
	return sum