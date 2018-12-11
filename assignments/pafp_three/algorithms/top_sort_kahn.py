# Portion of the solution that houses the implementation for the algorithm that performs topological sorting on an directed graph.

# This implementation consists of only one function that does it all.
def top_sort_kahn(graph_obj):
	# Initializing an empty list to hold the sorted order of vertices.
	sort_lst = []
	# Initializing a list of lists to hold the list of incoming edges of each node, instead of the outgoing edges that are usually represented in an adjacency list.
	in_verts = [[] for i in xrange(7)]
	# Iterating through all vertices of the graph.
	for vert in graph_obj.verts:
		# Iterating through each edge in the adjacency list entry of each node.
		for edge in graph_obj.adj_list[vert]:
			# Appending the edge to the list of incoming edges.
			in_verts[edge-1].append(vert)
	# Finding the vertices that don't have any incoming edges and storing them in a list.
	nia_verts = [ind+1 for ind, ele in enumerate(in_verts) if ele == []]
	# Generating a modified adjacency list so that the program can handle it easier.
	mod_adjlist = [item for key, item in graph_obj.adj_list.items()]
	# Iterating in a while loop till there are no more vertices with no incoming edges.
	while len(nia_verts) > 0:
		# Removing the topmost element from the list of vertices with no incoming edges.
		niavert = nia_verts.pop()
		# Appending the popped element to the sorted list.
		sort_lst.append(niavert)
		# Taking a copy of the adjacency entry of the popped vertex.
		temp_adj_entry = mod_adjlist[niavert-1][:]
		# Now iterating through the list of neighbours in the adjacency list entry of the popped vertex.
		for nghbr in temp_adj_entry:
			# Removing the neighbour from the adjacency list.
			mod_adjlist[niavert-1].remove(nghbr)
			# Removing the popped element from the list of incoming edges for the neighbour.
			in_verts[nghbr-1].remove(niavert)
			# Checking if the list of incoming edges of the neighbour is empty.
			if in_verts[nghbr-1] == []:
				# If it is empty then append the neighbour to the list of vertices with no incoming edges.
				nia_verts.append(nghbr)
	# Finally return the list of sorted elements.
	return sort_lst