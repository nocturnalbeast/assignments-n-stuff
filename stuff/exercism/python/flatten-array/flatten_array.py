otpt_lst = []

def flatten(inp_list):
	return list(act_flat(inp_list))

def act_flat(inp_list):
	if (type(inp_list) is tuple) | (type(inp_list) is list):
		for i in inp_list:
			for val in flatten(i):
				yield val
	elif (type(inp_list) is int) | (type(inp_list) is str):
		yield inp_list