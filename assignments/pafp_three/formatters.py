# Portion of the solution that contains the functions that format the output delivered by the functions that implement the algorithms, and print the output in the way that is required by the questions.

# Function to format and print the output of the function that implements topological sort.
def format_top_sort(result):
	# Printing the header line.
	print "The topological sort of the first graph is:\n\nVertex\tNumber"
	# Iterating through the argument passed to the function, that is the unformatted output passed to the function by the topological sort function, which here is a list.
	for i in xrange(len(result)):
		# Translating the node number into the vertex name like A, B, etc. and then printing it along with the rank/sorting number as per topological sort.
		print trns_node[result[i]] + "\t" + str(i+1)

# Function to format and print the output of the function that implements Dijkstra's algorithm.
def format_dijkstra(result, start_node):
	# Printing the header line.
	print "Shortest path for the graph: "
	# Iterating through the result generated from the function that implements Dijkstra's algorithm, which is a list of costs from the source node.
	for ind in xrange(len(result)):
		# Now printing each node with it's actual name, using the trns_node dictionary, and then printing the cost alongside it.
		print "Shortest path from " + trns_node[start_node] + " to " + trns_node[ind + 1] + " is of distance " + str(result[ind])

# Function to format and print the output of the function that implements Kruskal's algorithm.
def format_kruskal(result):
	# Printing the header line.
	print "The edges in the minimum spanning tree are:"
	# Converting the list of edges wherein the vertices are node numbers, into a list of edges wherein the vertices are node names i.e. A, B, etc. and printing the list.
	print [(trns_node[edge[0]],trns_node[edge[1]]) for edge in result[0]]
	# Printing the second argument, i.e. the cost of the minimum spanning tree.
	print "It's cost is " + str(result[1]) + "."

# Function to format and print the output of the function that implements the algorithm that finds articulation points in a graph.
def format_articulation(result):
	# The result received from the caller is a list of True/False values which indicate whether a node is an articulation point or not. So we iterate through it using the inbuilt enumerate function and take the vertices of those elements which have a True boolean to their cell.
	result = [index+1 for index, value in enumerate(result) if value == True]
	# Now we translate those number representations of those nodes into letter representations, using the trns_node dictionary.
	result = [trns_node[element] for element in result]
	# Finally, we print the result in the given format.
	print "The articulation points of the given graph are " + ', '.join(result) + "."

# Function to format and print the output of the function that implements the algorithm that finds the strongly connected components of a graph.
def format_scc(result):
	print "The strongly connected components of the graph are:"
	for res in result:
		print res