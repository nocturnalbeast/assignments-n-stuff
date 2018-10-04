def rebase(input_base, digits, output_base):
	if input_base < 2 or output_base < 2:
		raise ValueError("Invalid base!")
	if digits == []:
		return []
	if sorted(digits)[0] < 0 or sorted(digits)[len(digits)-1] >= input_base:
		raise ValueError("Invalid digits!")
	dec = 0
	lst_reb = []
	for i in range(len(digits)):
		dec += digits[i] * (input_base**(len(digits) - 1 - i))
	while dec > 0:
		lst_reb.insert(0,dec%output_base)
		dec = int(dec/output_base)
	return lst_reb