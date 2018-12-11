# Portion of the solution that contains the data structures that are used to represent the graphs and other graph-related objects in the problem.

# The first version of a graph data structure that is used to represent a graph. This is used for representing an unweighted graph and includes an input function of its own. This class is not really used in the solution, but is the basis on which other classes that represent graphs are modeled.
class PrimitiveGraph():
	# Initialisation function to declare and initalise the data members of the class.
	def __init__(self):
		# The array of vertices, initially set to a null value.
		self.verts = None
		# The adjacency list of the graph, initially set to a null value.
		self.adj_list = None
		# The list of all edges, with its generating function that is dependent on the list of vertices and the adjacency list, which is currently empty and thus generates an empty list as well.
		self.edges = [(node,snode) for snode in self.adj_list.get(node) for node in self.verts]

	# The input function that takes input from the user in runtime and populates the data members of the graph with the supplied data.
	def set_graph(self):
		# Prompting the user for the number of vertices.
		vert_num = input("Enter the number of vertices:")
		# Generating a list of vertices and assigning it to the respective data member of the class.
		self.verts = range(1,vert_num+1)
		# Generating an adjacency list, but with no edges in it.
		self.adj_list = {vert:[] for vert in self.verts}
		# Generating the list of all possible edges, to validate user input.
		possible_edges = [str(i) + ',' + str(j) for i in self.verts for j in self.verts]
		# Prompting the user for input.
		print "Enter the edges between vertices, separated by a comma:\nEnter 0 to end."
		# Running an infinite loop to obtain user input. If user enters 0, then break the loop.
		while True:
			# Prompt the user for input.
			edge = raw_input("Edge: ")
			# If condition to check whether the user has entered the input to terminate the input loop.
			if edge == '0':
				# If yes, break the loop.
				break
			# Else check if the edge is in the list of possible edges, to validate user input.
			elif edge in possible_edges:
				# Split the string into two parts, with comma as a delimiter.
				nodes = edge.split(',')
				# Since this is aimed to be a undirected graph, the edge has to be appended to the adjacency lists of both the vertices of the edge.
				self.adj_list[int(nodes[0])] += [int(nodes[1])]
				self.adj_list[int(nodes[1])] += [int(nodes[0])]

# This is a minimal, but refined version of the previous graph class, which includes support for weights in the graph elements. This class can be used for both directed and undirected graphs.
class WeightedGraph():
	# Initalisation function for the graph objects. Each object will receive an adjacency list as the argument to initalize the graph object, which is handled by this function.
	def __init__(self, adj_list):
		# Declaring and initalizing the adjacency list in the graph object by simply copying over the argument from the object creation, which is the adjacency list.
		self.adj_list = adj_list
		# Declaring and generating a list of vertices from the adjacency list.
		self.verts = self.adj_list.keys()
		# Declaring an empty list for the list of edges, which is a better structure than the adjacency list in some problems.
		self.edges = []
		# Now iterating through all the vertices, so that all the edges may be added into the list.
		for vertex in self.verts:
			# Adding all the edges that corresponding to the vertex in the iteration to the list of edges with a list comprehension.
			self.edges += [(vertex, pair[0], pair[1]) for pair in self.adj_list[vertex]]

# This is the same class as above, but modified to represent unweighted graphs. As before, this class can also be used to represent both directed and undirected graphs.
class UnweightedGraph():
	# Initalisation function for the graph objects. Each object will receive an adjacency list as the argument to initalize the graph object, which is handled by this function.
	def __init__(self, adj_list):
		# Declaring and initalizing the adjacency list in the graph object by simply copying over the argument from the object creation, which is the adjacency list.
		self.adj_list = adj_list
		# Declaring and generating a list of vertices from the adjacency list.
		self.verts = self.adj_list.keys()
		# Declaring an empty list for the list of edges, which is a better structure than the adjacency list in some problems.
		self.edges = []
		# Now iterating through all the vertices, so that all the edges may be added into the list.
		for vertex in self.verts:
			# Adding all the edges that corresponding to the vertex in the iteration to the list of edges with a list comprehension.
			self.edges += [(vertex, next_v) for next_v in self.adj_list[vertex]]

# This is the implementation of the disjoint set data structure, which is also called the union-find structure, due to the fact that it mainly defines two functions named union and find. This data structure is utilized in building the minimum spanning tree using Kruskal's algorithm.
class UnionFind():
	# Initalisation function for the data structure. Each object will receive a number which is the number of vertices of the graph as an argument, which is then handled by this function.
	def __init__(self, vert_num):
		# Declaring and initialising the parent array, which represents the parents of each node.
		self.parent = list(xrange(vert_num))
		# Declaring and initialising the rank array, which is self-explanatory. All the ranks are initally zero.
		self.rank = [0 for vert in xrange(vert_num)]

	# The first of the two functions in the disjoint set structure; the find function is used to find the parent/root node of a node.
	def find(self, vert):
		# Checking if the node is a singleton, i.e. if the node is not joined to any other nodes, or if the root node in the set is the node itself. If not then the next line is executed.
		if vert != self.parent[vert]:
			# If the parent of the node is not the node itself, then the function is recursively called to find the parent of the node.
			self.parent[vert] = self.find(self.parent[vert])
		# Finally return the parent of the node.
		return self.parent[vert]

	# The second function in the disjoint set structure; the union function is used to unify two vertices in the disjoint set, by acknowledging the edge between them.
	def union(self, v_one, v_two):
		# Finding the parent of the first and the second node.
		root_one = self.find(v_one)
		root_two = self.find(v_two)
		# If the nodes have the same parent, then there's nothing to do, since they are already connected.
		if root_one == root_two:
			return
		# Else if the rank of the first node is greater than that of the second node, then make the first node the parent of the second.
		if self.rank[root_one] > self.rank[root_two]:
			self.parent[root_two] = root_one
		# Else, the parent of the first node becomes the second node, and then if the rank of the first node is equal to that of the second node, then increment the parent's rank.
		else:
			self.parent[root_one] = root_two
			if self.rank[root_one] == self.rank[root_two]:
				self.rank[root_two] += 1

# This class groups the data that is used by the implementation of the algorithm that finds strongly connected components into one single class, so that a single instance of the class can be used throughout the multiple functions, and can do so without reference errors.
class SCCAdditional():
	# Initalization function for the data structure. Declares and initializes three lists, one to keep track of visited nodes, one to act as a stack, and one to hold the output.
	def __init__(self, vert_num):
		# The list to keep track of visited nodes is initially set to a list of booleans that are false, one for each node.
		self.visited = [False for i in xrange(vert_num)]
		# The list used for the stack is initially empty.
		self.stack = []
		# The list that holds the output is initially empty.
		self.op_list = []

# This class groups the data that is used by the implementation of Dijkstra's algorithm into one single class, so that a single instance of the class can be used throughout the multiple functions, and can do so without reference errors.
class DijkstraAdditional():
	# Initialization function for the data structure. Declares and initializes two lists; one to hold the distance of the vertices, and one to hold the status of the node, if it is in the shortest path tree set or not. It also includes a list of lists which acts like a matrix to hold the adjacency matrix.
	def __init__(self, vert_num):
		# Initializing the adjacency matrix with all zeroes for all possible edges.
		self.adj_matrix = [[0 for column in xrange(vert_num)] for row in xrange(vert_num)]
		# Initializing the distance for all the nodes from the starting node to something very large, which in this case is taken to be 65536.
		self.distance = [65536] * vert_num
		# Initializing the list that holds the status of the nodes with booleans that are all false.
		self.shortest_pth_ts = [False] * vert_num

# This class groups the data that is used by the implementation of the algorithm that finds articulation points in a graph into one single class, so that a single instance of the class can be used throughout the multiple functions, and can do so without reference errors.
class ArtiAdditional():
	# Initialization function for the data structure. Declares and initalizes five lists, a list to keep track of visited nodes, a list to keep track of the time/number of discovery, a list to keep track of low numbers of each nodes, a list to keep track of the parent of each node and a list to keep track of the status of each node, to see if each node is a articulation point or not. Also uses a time variable to be used in assigning time/iterational values to the discovery and low lists.
	def __init__(self, vert_num):
		# Initializing the list that keeps track of the visited nodes with boolean values that are all false.
		self.visited = [False] * vert_num
		# Initializing the list that keeps track of the discovery time with a high integer value.
		self.discovery = [65536] * vert_num
		# Initializing the list that keeps track of the low number with a high integer value.
		self.low = [65536] * vert_num
		# Initializing the list that keeps track of the parent of each node with -1, which means that there is currently no parent for each node now.
		self.parent = [-1] * vert_num
		# Initializing the list that keeps track of the status of the nodes for checking if they are articulation points or not, with boolean values that are all false, which means that none of them are currently an articulation point.
		self.arti_points = [False] * vert_num
		# Initializing the time value/iterational value as zero.
		self.time_val = 0