# Portion of the solution that contains the functions that help in automating some repetitive tasks that are run in various parts of the code, thus lessening the complexity of the code.

# Function to sort the list of edges corresponding to a vertex by weight.
def sort_edges_bw(adjlst_entry):
	# Utilizing the inbuilt functions to sort the adjacency list with respect to the weight, which is the second entry in each tuple that signifies the edge.
	adjlst_entry.sort(key=lambda e: e[1])
	# Returning the sorted list entry to the caller.
	return adjlst_entry

# Function to sort the complete list of edges of a graph by weight.
def sort_edgelist_bw(edgelist):
	# Utilizing the inbuilt functions to sort the list of edges with respect to the weight, which is the third entry in each tuple that signifies the edge.
	edgelist.sort(key=lambda e: e[2])
	# Returning the sorted list of edges to the caller.
	return edgelist

# Function to remove all the weights in a weighted adjecency list, thus converting it into an adjacency list of an unweighted graph.
def conv_wei2unwei(adj_list):
	# Utilizing a dictionary comprehension to generate a dictionary, neglecting the weight from the previous adjacency list which is also a dictionary, and returning the generated dictionary to the caller.
	return {vertex:[pair[0] for pair in sort_edges_bw(adj_list[vertex])] for vertex in adj_list.keys()}

# Function to convert the adjacency list provided by the graph object into an adjacency matrix.
def gen_adj_matrix(adj_list):
	# Generating an empty list of lists which will serve as the adjacency matrix.
	adj_matrix = [[0 for j in adj_list.keys()] for i in adj_list.keys()]
	# Iterating through each vertex in the adjacency list.
	for ele in adj_list.keys():
		# Iterating through each entry in the adjacency list entry for a single vertex.
		for edge in adj_list[ele]:
			# Assigning the weight to the respective position on the matrix.
			adj_matrix[ele-1][edge[0]-1] = edge[1]
	# Finally returning the matrix to the caller.
	return adj_matrix
