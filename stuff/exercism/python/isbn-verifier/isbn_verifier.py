def retn_act_num(num):
	if num.isdigit():
		return int(num)
	elif num == 'X':
		return 10

def verify(isbn):
	cln_isbn = list(filter(str.isalnum, isbn))
	if (len(cln_isbn) != 10) | (not set(cln_isbn).issubset('0123456789X')) | ('X' in cln_isbn[0:len(cln_isbn)-1]):
		return False
	else:
		ver_isbn = 0
		for x in range(10):
			ver_isbn += (retn_act_num(cln_isbn[x]) * (10-x))
		return ver_isbn % 11 == 0