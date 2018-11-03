import json

def dns_ans_three():
	ans_dict = {}
	while True:
		dom = raw_input("Enter the domain: ")
		typ = raw_input("Enter the type: ")
		exist_val = ans_dict.get(dom)
		if  type(exist_val) is list:
			nw_lst = exist_val + [typ]
			ans_dict.update({dom:nw_lst})
		elif isinstance(exist_val, basestring):
			nw_lst = [ans_dict.get(dom),typ]
			ans_dict.update({dom:nw_lst})
		elif exist_val == None:
			ans_dict.update({dom:typ})
		if input("Enter 0 to end or any other number to continue: ") == 0:
			break
	return json.dumps(ans_dict)

def dns_ans_four():
	ans_dict = {}
	while True:
		dom = raw_input("Enter the domain: ")
		n = input("How many responses did the query have?")
		rsp_lst = []
		print "Enter the " + str(n) + " response types:"
		for i in xrange(n):
			rsp_lst.append(raw_input(str(i+1) + ": "))
		if len(rsp_lst) == 1:
			rsp_lst = rsp_lst[0]
		ans_dict.update({dom:rsp_lst})
		if input("Enter 0 to end or any other number to continue: ") == 0:
			break
	return json.dumps(ans_dict)

def dns_ans_five():
	ans_list = []
	while True:
		ans_list.append(raw_input("Enter the IP address returned with A record: "))
		if input("Enter 0 to end or any other number to continue: ") == 0:
			break
	return json.dumps(ans_list)


def dns_ans_six():
	ans_list = []
	while True:
		ans_list.append(raw_input("Enter the domains returned with CNAME record: "))
		if input("Enter 0 to end or any other number to continue: ") == 0:
			break
	return json.dumps(ans_list)


def dns_ans_seven():
	ans_list = []
	while True:
		ans_list.append(raw_input("Enter the domains returned with MX record: "))
		if input("Enter 0 to end or any other number to continue: ") == 0:
			break
	return json.dumps(ans_list)


def dns_ans_eight():
	ans_dict = {}
	ans_dict.update({"domain":raw_input("Enter the domain of the chosen MX server: ")})
	ans_dict.update({"ip":raw_input("Enter the IP address of the chosen MX server: ")})
	ans_dict.update({"preference":raw_input("Enter the preference value of the chosen MX server: ")})
	return json.dumps(ans_dict)


dict_que = {
	3: dns_ans_three,
	4: dns_ans_four,
	5: dns_ans_five,
	6: dns_ans_six,
	7: dns_ans_seven,
	8: dns_ans_eight
}
ch = input("Enter the question number for which you want to generate a JSON string for:")
print "\n" + dict_que.get(ch)()