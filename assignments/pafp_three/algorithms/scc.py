# Portion of the solution that houses the implementation for the algorithm that finds strongly connnected components in an directed graph. There are two functions involved, the first one (arti_worker) is the one that performs the actual algorithm, while the second function (arti_wrapper) is the one that handles the data and calling of the first function.


# Function to run pass one of the DFS traversal on the graph and append the vertices onto the stack.
def scc_passone(adj_list, node, add_s):
	# Setting the visited entry for the current node to true, to reflect that the node has been visited.
    add_s.visited[node-1] = True
	# Traversing through the neighboring nodes in the adjacency list entry for the node.
    for nghbr in adj_list[node]:
		# Checking if the node has not been visited.
        if add_s.visited[nghbr-1] == False:
			# If not, then perform the DFS traversal on the node.
            scc_passone(adj_list, nghbr, add_s)
	# Append the node to the stack.
    add_s.stack.append(node)

# Function to flip the graph i.e. to reverse the direction of all the directed edges in the graph.
def flip_graph(graph_obj):
	# Generating the reversed list of edges using a list comprehension.
    mod_edges = [(edge[1], edge[0]) for edge in graph_obj.edges]
	# Generating an empty adjacency list, which is to be populated with the reversed edges.
    mod_adjlist = [[] for vert in graph_obj.verts]
	# Iterating through each edge in the list of reversed edges.
    for edge in mod_edges:
		# Populate the modified adjacency list with each reversed edge.
        mod_adjlist[edge[0]-1].append((edge[1]))
	# Finally return the modified adjacency list.
    return mod_adjlist 

# Function to perform DFS, but in a slightly different manner than compared to the first pass.
def scc_passtwo(adj_list, node, add_s):
	# Setting the visited entry to True for the current node.
    add_s.visited[node-1] = True
	# Iterating through each neighboring node in the adjacency list entry for the node.
    for nghbr in adj_list[node-1]:
		# Checking if the node has not been visited.
        if add_s.visited[nghbr-1] == False:
			# Removing the node from the stack.
            add_s.stack.remove(nghbr)
			# Recursively calling this function with the neighboring node as the argument.
            scc_passtwo(adj_list, nghbr, add_s)
	# Finally print the section of visited nodes which will provide the connected component that has been traversed upon in this iteration.
    print add_s.visited

# The wrapper function that implements the rest of the algorithm and handles the data and the output and the other functions.
def strng_conn_comp(graph_obj):
	# Generating an instance of the data structure used to hold the additional data for the implementation of this algorithm.
    add_data = SCCAdditional(len(graph_obj.verts))
	# Iterating through the vertices of the graph.
    for vert in graph_obj.verts:
		# Checking if the node has not been visited.
        if add_data.visited[vert-1] == False:
			# If not, then run DFS (pass one) on the node.
            scc_passone(graph_obj.adj_list, vert, add_data)
	# Now reverse the graph and obtain a reversed adjacency list.
    mod_adjlist = flip_graph(graph_obj)
	# Reset the visited array, by setting all false values for all nodes.
    add_data.visited = [False for i in xrange(len(graph_obj.verts))]
	# Checking if the stack is empty.
    while len(add_data.stack) != 0:
		# If not then pop the topmost element off the stack.
        ele = add_data.stack.pop()
		# Checking if the popped vertex hasn't been visited.
        if add_data.visited[ele-1] == False:
			# If not, then run DFS (pass two) on the vertex.
            scc_passtwo(mod_adjlist, ele, add_data)