def find_rc_p1(num):
	mid = int(num**0.5)
	if mid**2 == num:
		return (mid,mid)
	elif mid * (mid + 1) >= num:
		return (mid,mid+1)
	else:
		return (mid+1,mid+1)

def encode(plain_text):
	cln_str = filter(str.isalnum, plain_text.lower())
	(row,col) = find_rc_p1(len(cln_str))
	cln_str = cln_str + ' ' * ((row * col) - len(cln_str))
	mat_crypt = [[0 for i in range(col)] for j in range(row)]
	str_cont = 0
	for i in range(row):
		for j in range(col):
			mat_crypt[i][j] = cln_str[str_cont]
			str_cont += 1
	final_str = ''
	for i in range(col):
		for j in range(row):
			final_str += mat_crypt[j][i]
		final_str += ' '
	return final_str[:-1]