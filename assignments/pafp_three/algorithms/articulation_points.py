# Portion of the solution that houses the implementation for the algorithm that finds articulation points in an undirected graph. There are two functions involved, the first one (arti_worker) is the one that performs the actual algorithm, while the second function (arti_wrapper) is the one that handles the data and calling of the first function.

# The function that implements the algorithm that finds articulation points in an undirected graph.
def arti_worker(adj_list, current, add_a):
	# Setting the number of children of the current node to zero.
	children = 0
	# Marking the current node as visited,	 using the visited array.
	add_a.visited[current-1] = True
	# Marking the time of discovery of the current node as the current value of the time value that's being tracked using the time_val in the additional data structure.
	add_a.discovery[current-1] = add_a.time_val
	# Marking the low number of the current node as the current value of the time value that's being tracked using the time_val in the additional data structure.
	add_a.low[current-1] = add_a.time_val
	# Incrementing the time value.
	add_a.time_val += 1
	# Iterating through the adjacency list entry of the current node to see all neighbouring edges.
	for nghbr in adj_list[current]:
		# If the neighbour has not been visited, then do the steps that entail.
		if add_a.visited[nghbr-1] == False:
			# Set the parent of the neighbouring node as the current node.
			add_a.parent[nghbr-1] = current
			# Increment the number of children of the current node by one.
			children += 1
			# Recursively call this function, but with the neighbouring node as the source node.
			arti_worker(adj_list, nghbr, add_a)
			# The low number of the current node is set to the minimum of the low numbers of the current node and the neighbouring node.
			add_a.low[current-1] = min(add_a.low[current-1], add_a.low[nghbr-1])
			# Checking to see whether this node is the root node or not.
			if add_a.parent[current-1] == -1 and children > 1:
				# If yes, then add this as an articulation point.
				add_a.arti_points[current-1] = True
			# Else if there is a parent for the current node and the low number of the neighbouring node is greater than or equal to the discovery number of the current node, then it means that this is an articulation point.
			if add_a.parent[current-1] != -1 and add_a.low[nghbr-1] >= add_a.discovery[current-1]:
			# If that condition holds true, then add this as an articulation point.
				add_a.arti_points[current-1] = True
		# If the neighbour has been visited, but is not the parent of the current node, then revise the low number of the current node.
		elif nghbr != add_a.parent[current-1]:
			# The low number of the current node becomes the minimum of the low number of the current node and the discovery time of the neighbouring node.
			add_a.low[current-1] = min(add_a.low[current-1], add_a.discovery[nghbr-1])

# The second function that initializes the additional data structure and handles the calling of the first function and the returning of the result.
def arti_wrapper(graph_obj, start_node):
	# Initializing the additional data structure with the number of vertices as the argument to initialize the structure.
	data_add = ArtiAdditional(len(graph_obj.verts))
	# Calling the first function with the requested start node and the instance of the additional data structure just created.
	arti_worker(graph_obj.adj_list, start_node, data_add)
	# Returning the result.
	return data_add.arti_points
