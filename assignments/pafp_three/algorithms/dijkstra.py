# Portion of the solution that houses the implementation for Dijkstra's algorithm. This implementation consists of three functions; the first is to find the minimum edge in the adjacency matrix, the second function is the actual implementation of Dijkstra's algorithm, and the third function is a wrapper function that handles all the calling and setup of the data, and the passing of the result as well.

# Function to find the minimum edge for each vertex amongst all its edges in the adjacency matrix.
def find_minimum_edge(adj_matrix, add_d):
	# Setting minimum value to a very high value initially.
	minval = 65536
	# Iterating through the adjacency matrix.
	for vert in xrange(len(adj_matrix)):
		# If a shorter edge is found and it is not part of the shortest path tree set, then do the section that entails.
		if add_d.distance[vert] < minval and add_d.shortest_pth_ts[vert] == False:
			# Minimum value will be now set to the distance of the vertex from the source node.
			minval = add_d.distance[vert]
			# And set the minimum edge vertex to the one just found.
			min_vert = vert
	# Return the vertex in the minimum edge.
	return min_vert

# Function that actually implements Dijkstra's algorithm.
def dijkstra(adj_matrix, source, add_d):
	# Setting the distance of the source node from the source node to zero.
	add_d.distance[source] = 0
	# Iterating through the vertices in the matrix.
	for i in xrange(len(adj_matrix)):
		# Finding the edge with the least distance from the source node.
		min_edge = find_minimum_edge(adj_matrix, add_d)
		# Adding the vertex in the mininum edge to the shortest path tree set.
		add_d.shortest_pth_ts[min_edge] = True
		# Now iterating through the vertices again, but this is just like row/column traversal in the matrix i.e. if the outer loop is traversing though rows, this loop is traversing through columns.
		for vert in xrange(len(adj_matrix)):
			# Now checking if an edge between the min_edge and the vertex exists and if it is not a part of the shortest path tree set and the distance of the vertex from the source node is greater than the sum of the distance of the min_edge from the source node and the cost of edge from the min_edge to the vertex in question.
			if adj_matrix[min_edge][vert] > 0 and add_d.shortest_pth_ts[vert] == False and add_d.distance[vert] > add_d.distance[min_edge] + adj_matrix[min_edge][vert]:
				# Now updating the distance of the vertex from the source node as the distance from the source node to the min_edge plus the cost of the edge from the min_edge to vert.
				add_d.distance[vert] = add_d.distance[min_edge] + adj_matrix[min_edge][vert]

# The function that sets up all the input and output for the other functions i.e. a wrapper function for the other two functions.
def dijkstra_wrapper(graph_obj, spec_node):
	# Initializing an instance of the additonal data structure used for this implementation.
	data_add = DijkstraAdditional(len(graph_obj.verts))
	# Generating an adjacency matrix out of the graph object's adjacency list.
	data_add.adj_matrix = gen_adj_matrix(graph_obj.adj_list)
	# Running the algorithm's implementation.
	dijkstra(data_add.adj_matrix, spec_node, data_add)
	# Finally returning the distance array, which is the expected result.
	return data_add.distance