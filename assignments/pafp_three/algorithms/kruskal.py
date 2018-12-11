# Portion of the solution that houses the implementation for Kruskal's algorithm.

# This implementation consists of only one function that does it all.
def kruskal(graph_obj):
	# Initializing an empty list for the result, which is the minimum spanning tree.
	res = []
	# Generating an instance of the disjoint set class.
	uf_set = UnionFind(len(graph_obj.verts))
	# Generating a sorted list of edges which are sorted with respect to weight.
	edges = sort_edgelist_bw(graph_obj.edges)
	# Initializing the number of edges considered in the MST to zero.
	e_num = 0
	# Running in a loop till the number of edges reaches the maximum a MST can be up to i.e. one less than the number of vertices.
	while e_num < len(graph_obj.verts) - 1:
		# Removing the first edge in the list.
		n_one, n_two, weight = edges.pop(0)
		# Finding the root of the first vertex in the node using the find function of the disjoint set class.
		root_one = uf_set.find(n_one-1)
		# Finding the root of the second vertex in the node using the find function of the disjoint set class.
		root_two = uf_set.find(n_two-1)
		# Checking if the root of the vertices are the same.
		if root_one != root_two:
			# If yes, increment the number of edges by one, since this edge is approved.
			e_num += 1
			# Append the edge to the list of edges in the MST.
			res.append((n_one,n_two,weight))
			# Perform union operation on the root of both vertices to unify their trees.
			uf_set.union(root_one, root_two)
	# Finally return the list of edges in the MST and the sum of its costs.
	return res, sum([ele[2] for ele in res])