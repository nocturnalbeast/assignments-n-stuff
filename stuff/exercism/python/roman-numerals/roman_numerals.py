def ret_ro_man(digit, substring):
	#substring is like IVX, XLC, CDM, read wikipedia and try to understand the similar progressions on each digit's place. You might not even need that. Just read the function.
	roman = ''
	if digit == 9:
		roman += substring[0] + substring[2]
	elif digit >= 5:
		roman += substring[1] + substring[0]*(digit-5)
	elif digit == 4:
		roman += substring[0] + substring[1]
	elif digit >= 1:
		roman += substring[0]*digit
	return roman

def numeral(number):
	roman = ''
	digits = [int(i) for i in str(number)]
	for i in range(len(digits)):
		pos = len(digits) - i
		if pos == 4:
			roman += 'M'*digits[i]
		elif pos == 3:
			roman += ret_ro_man(digits[i],'CDM')
		elif pos == 2:
			roman += ret_ro_man(digits[i],'XLC')
		elif pos == 1:
			roman += ret_ro_man(digits[i],'IVX')
	return roman