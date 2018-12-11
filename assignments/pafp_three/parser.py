# Part of the solution that parses the input file and provides a processed data structure which contains the data for each respective problem grouped together.

# This is the function that parses the input file.
def inp_parse(inputfile):
	# Reading the input into a list of strings.
	with open(inputfile) as inp_file:
		inp_data = inp_file.readlines()
	# Cleaning up input and breaking it into parts, one for each program.
	# This one's a big one liner to convert it all into whatever format the program needs.
	inp_data = [map(int, ele_str.strip('\n').replace('  ',' ').split(' ')) for ele_str in inp_data]
	# Specifying the start of each graph's data, with an additional entry for the end+1'th line.
	brk_list = [0,7,14,21,29,37,44]
	# Breaking the input data into graphs. Not exactly, but at least data grouped into a dictionary for a start.
	inp_data = {i+1:inp_data[brk_list[i]:brk_list[i+1]] for i in xrange(len(brk_list)-1)}
	# Root dictionary for those graphs that have the starting node. Currently empty.
	root_dict = {}
	# The actual conversion. Iterating through 1-6 for each graph number.
	for i in xrange(1,7):
		# Getting the primitive list of lists.
		lst = inp_data.get(i)
		# Creating an adjacency list.
		adj_prim = []
		# If graph number is 4/5 then take away the root.
		if i == 4 or i == 5:
			# Taking away the root element and storing in root_dict. Plus clears that entry from the primitive list of lists.
			lst, root_dict[i] = lst[:-1], lst[len(lst)-1][0]
		# Iterating through each vertex's entry for one graph.
		for sub_lst in lst:
			# Splitting the list into three parts; the number of entries, the nodes it connects to and the costs of said edges.
			num, lst_vert, lst_weight = sub_lst[0], sub_lst[1::2], sub_lst[2::2]
			# Now iterating through the list and parsing those elements previously made to generate a adjacency list entry for the node in question. Also appends it to the adjacency list for the graph.
			adj_prim.append([(lst_vert[k],lst_weight[k]) for k in xrange(num)])
		# Replacing the graph's primitive list of lists for the processed dictionary for the graph in question.
		inp_data[i] = {j+1:adj_prim[j] for j in xrange(len(adj_prim))}
	# Finally returning the data as a tuple, to the data element to whichever this function is called to.
	return inp_data, root_dict