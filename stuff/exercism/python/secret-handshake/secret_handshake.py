lst_encode = [
	"wink",
	"double blink",
	"close your eyes",
	"jump"
]

def handshake(code):
	action_lst = []
	lst = map(int,list(bin(code))[:1:-1])
	for i in range(min(len(lst),4)):
		if lst[i] == 1:
			action_lst.append(lst_encode[i])
	if code > 16:
		action_lst = action_lst[::-1]
	return action_lst

def secret_code(actions):
	code = 0
	rev_flg = False
	for action in actions:
		code += 2**(lst_encode.index(action))
	for i in range(len(actions)-1):
		if lst_encode.index(actions[i]) > lst_encode.index(actions[i+1]):
			rev_flg = True
			break
	return code + (int(rev_flg) * 16)