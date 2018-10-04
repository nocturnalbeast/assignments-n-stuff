def transpose(input_lines):
	print list(input_lines)
	nrml_ip = normalize(list(input_lines))
	trns = []
	for i in xrange(len(nrml_ip[0])):
		trns.append(ret_column(nrml_ip,i))
	return trns

def normalize(ip_ln):
	for i in reversed(range(1,len(ip_ln))):
		if len(ip_ln[i]) > len(ip_ln[i-1]):
			ip_ln[i-1] = ip_ln[i-1] + " " * (len(ip_ln[i]) - len(ip_ln[i-1]))
	return ip_ln

def ret_column(ip_ln,index):
	colmn = ""
	for i in ip_ln:
		colmn = colmn + i[index]
	return colmn