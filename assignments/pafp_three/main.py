# Portion of the solution that orchestrates all other functions and provides the relevant output.

def main():
	# Calling the parsing function to generate the data from the file input.dat. Also to be noted, the data element will have the data of all the problems, and each problem can access it by calling data with the index number which will be the same as the question number. Full documentation of the parsing function is present in parser.py.
	data = inp_parse('input.dat')
	# Creating an empty list for storing all objects of the graph classes. They can be weighted or unweighted, the type does not matter.
	graph_objects = []
	# Now iterating through the range 1-6 (7 not included) to populate the list with the class objects. If the problem is either topological sorting, finding the articulation points or finding the strongly connected components, the graph does not require the weights so we use an unweighted graph class.
	for i in xrange(1,7):
		# Checking if the graph is the first, fourth, fifth or sixth graph, since the problems that run on those graphs do not need weights.
		if i in [1,4,5,6]:
			# If the above condition is satisfied, then convert the adjacency list to an unweighted adjacency list and create an instance of the UnweightedGraph class to build the data structures to represent the graph.
			graph_objects.append(UnweightedGraph(conv_wei2unwei(data[0][i])))
		# If the above condition isn't satisfied, then it means that the adjacency graph isn't to be modified since the problems that run on these graphs do need weights to function.
		else:
			# So create an instance of the WeightedGraph class instance for the adjacency lists that fall into this category.
			graph_objects.append(WeightedGraph(data[0][i]))
	# Extract the dictionary of the starting points for the implementation of the algorithm that finds articulation points from the data that was recieved from the input parsing function.
	root_dict = data[1]
	# Invoking the first algorithm - topological sort and calling it's formatting function as well.
	print "\nProblem 1:\n"
	res_one = top_sort_kahn(graph_objects[0])
	format_top_sort(res_one)
	# Invoking the second algorithm - Dijkstra's and calling it's formatting function as well.
	print "\nProblem 2:\n"
	res_two = dijkstra_wrapper(graph_objects[1],0)
	format_dijkstra(res_two, 1)
	# Invoking the third algorithm - Kruskal's and calling it's formatting function as well.
	print "\nProblem 3:\n"
	res_three = kruskal(graph_objects[2])
	format_kruskal(res_three)
	# Invoking the fourth algorithm - finding articulation points (first invocation) and calling it's formatting function as well.
	print "\nProblem 4:\n"
	res_four = arti_wrapper(graph_objects[3],root_dict[4])
	format_articulation(res_four)
	# Invoking the fourth algorithm - finding articulation points (second invocation) and calling it's formatting function as well.
	print "\nProblem 5:\n"
	res_five = arti_wrapper(graph_objects[4],root_dict[5])
	format_articulation(res_five)
	# Invoking the fifth algorithm - finding connected components and calling it's formatting function as well.
	print "\nProblem 6:\n"
	#strng_conn_comp(graph_objects[5])
	

# Simple statement to redirect execution to the main function.
if __name__ == "__main__":
	main()