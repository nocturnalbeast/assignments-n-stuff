# Complete solution. Each part is explained in detail in comments.
# Check constituent python files for complete documentation.
# The code is split into several sections; see section headers.

#######################################################################
# Class definitions for graphs and other structures used.
#######################################################################

class WeightedGraph():
	def __init__(self, adj_list):
		self.adj_list = adj_list
		self.verts = self.adj_list.keys()
		self.edges = []
		for vertex in self.verts:
			self.edges += [(vertex, pair[0], pair[1]) for pair in self.adj_list[vertex]]

class UnweightedGraph():
	def __init__(self, adj_list):
		self.adj_list = adj_list
		self.verts = self.adj_list.keys()
		self.edges = []
		for vertex in self.verts:
			self.edges += [(vertex, next_v) for next_v in self.adj_list[vertex]]

class UnionFind():
	def __init__(self, vert_num):
		self.parent = list(xrange(vert_num))
		self.rank = [0 for vert in xrange(vert_num)]

	def find(self, vert):
		if vert != self.parent[vert]:
			self.parent[vert] = self.find(self.parent[vert])
		return self.parent[vert]

	def union(self, v_one, v_two):
		root_one = self.find(v_one)
		root_two = self.find(v_two)
		if root_one == root_two:
			return
		if self.rank[root_one] > self.rank[root_two]:
			self.parent[root_two] = root_one
		else:
			self.parent[root_one] = root_two
			if self.rank[root_one] == self.rank[root_two]:
				self.rank[root_two] += 1

class SCCAdditional():
	def __init__(self, vert_num):
		self.visited = [False for i in xrange(vert_num)]
		self.stack = []
		self.op_list = []

class DijkstraAdditional():
	def __init__(self, vert_num):
		self.adj_matrix = [[0 for column in xrange(vert_num)] for row in xrange(vert_num)]
		self.distance = [65536] * vert_num
		self.shortest_pth_ts = [False] * vert_num

class ArtiAdditional():
	def __init__(self, vert_num):
		self.visited = [False] * vert_num
		self.discovery = [65536] * vert_num
		self.low = [65536] * vert_num
		self.parent = [-1] * vert_num
		self.arti_points = [False] * vert_num
		self.time_val = 0

#######################################################################
# Function to parse input and generate data as needed.
#######################################################################

def inp_parse(inputfile):
	with open(inputfile) as inp_file:
		inp_data = inp_file.readlines()
	inp_data = [map(int, ele_str.strip('\n').replace('  ',' ').split(' ')) for ele_str in inp_data]
	brk_list = [0,7,14,21,29,37,44]
	inp_data = {i+1:inp_data[brk_list[i]:brk_list[i+1]] for i in xrange(len(brk_list)-1)}
	root_dict = {}
	for i in xrange(1,7):
		lst = inp_data.get(i)
		adj_prim = []
		if i == 4 or i == 5:
			lst, root_dict[i] = lst[:-1], lst[len(lst)-1][0]
		for sub_lst in lst:
			num, lst_vert, lst_weight = sub_lst[0], sub_lst[1::2], sub_lst[2::2]
			adj_prim.append([(lst_vert[k],lst_weight[k]) for k in xrange(num)])
		inp_data[i] = {j+1:adj_prim[j] for j in xrange(len(adj_prim))}
	return inp_data, root_dict

#######################################################################
# Helper functions which prove useful at doing some repetitive tasks.
#######################################################################

def sort_edges_bw(adjlst_entry):
	adjlst_entry.sort(key=lambda e: e[1])
	return adjlst_entry

def sort_edgelist_bw(edgelist):
	edgelist.sort(key=lambda e: e[2])
	return edgelist

def conv_wei2unwei(adj_list):
	return {vertex:[pair[0] for pair in sort_edges_bw(adj_list[vertex])] for vertex in adj_list.keys()}

def gen_adj_matrix(adj_list):
	adj_matrix = [[0 for j in adj_list.keys()] for i in adj_list.keys()]
	for ele in adj_list.keys():
		for edge in adj_list[ele]:
			adj_matrix[ele-1][edge[0]-1] = edge[1]
	return adj_matrix

#######################################################################
# Implementations of algorithms used.
#######################################################################

##################################
# Topological Sort
##################################

def top_sort_kahn(graph_obj):
	sort_lst = []
	in_verts = [[] for i in xrange(7)]
	for vert in graph_obj.verts:
		for edge in graph_obj.adj_list[vert]:
			in_verts[edge-1].append(vert)
	nia_verts = [ind+1 for ind, ele in enumerate(in_verts) if ele == []]
	mod_adjlist = [item for key, item in graph_obj.adj_list.items()]
	while len(nia_verts) > 0:
		niavert = nia_verts.pop()
		sort_lst.append(niavert)
		temp_adj_entry = mod_adjlist[niavert-1][:]
		for nghbr in temp_adj_entry:
			mod_adjlist[niavert-1].remove(nghbr)
			in_verts[nghbr-1].remove(niavert)
			if in_verts[nghbr-1] == []:
				nia_verts.append(nghbr)
	return sort_lst

##################################
# Dijkstra's Algorithm
##################################

def find_minimum_edge(adj_matrix, add_d):
	minval = 65536
	for vert in xrange(len(adj_matrix)):
		if add_d.distance[vert] < minval and add_d.shortest_pth_ts[vert] == False:
			minval = add_d.distance[vert]
			min_vert = vert
	return min_vert

def dijkstra(adj_matrix, source, add_d):
	add_d.distance[source] = 0
	for i in xrange(len(adj_matrix)):
		min_edge = find_minimum_edge(adj_matrix, add_d)
		add_d.shortest_pth_ts[min_edge] = True
		for vert in xrange(len(adj_matrix)):
			if adj_matrix[min_edge][vert] > 0 and add_d.shortest_pth_ts[vert] == False and add_d.distance[vert] > add_d.distance[min_edge] + adj_matrix[min_edge][vert]:
				add_d.distance[vert] = add_d.distance[min_edge] + adj_matrix[min_edge][vert]

def dijkstra_wrapper(graph_obj, spec_node):
	data_add = DijkstraAdditional(len(graph_obj.verts))
	data_add.adj_matrix = gen_adj_matrix(graph_obj.adj_list)
	dijkstra(data_add.adj_matrix, spec_node, data_add)
	return data_add.distance

##################################
# Kruskal's Algorithm
##################################

def kruskal(graph_obj):
	res = []
	uf_set = UnionFind(len(graph_obj.verts))
	edges = sort_edgelist_bw(graph_obj.edges)
	e_num = 0
	while e_num < len(graph_obj.verts) - 1:
		n_one, n_two, weight = edges.pop(0)
		root_one = uf_set.find(n_one-1)
		root_two = uf_set.find(n_two-1)
		if root_one != root_two:
			e_num += 1
			res.append((n_one,n_two,weight))
			uf_set.union(root_one, root_two)
	return res, sum([ele[2] for ele in res])

##################################
# Finding articulation points
##################################

def arti_worker(adj_list, current, add_a):
	children = 0
	add_a.visited[current-1] = True
	add_a.discovery[current-1] = add_a.time_val
	add_a.low[current-1] = add_a.time_val
	add_a.time_val += 1
	for nghbr in adj_list[current]:
		if add_a.visited[nghbr-1] == False:
			add_a.parent[nghbr-1] = current
			children += 1
			arti_worker(adj_list, nghbr, add_a)
			add_a.low[current-1] = min(add_a.low[current-1], add_a.low[nghbr-1])
			if add_a.parent[current-1] == -1 and children > 1:
				add_a.arti_points[current-1] = True
			if add_a.parent[current-1] != -1 and add_a.low[nghbr-1] >= add_a.discovery[current-1]:
				add_a.arti_points[current-1] = True
		elif nghbr != add_a.parent[current-1]:
			add_a.low[current-1] = min(add_a.low[current-1], add_a.discovery[nghbr-1])

def arti_wrapper(graph_obj, start_node):
	data_add = ArtiAdditional(len(graph_obj.verts))
	arti_worker(graph_obj.adj_list, start_node, data_add)
	return data_add.arti_points

##################################
# Finding connected components
##################################

def scc_passone(adj_list, node, add_s):
	add_s.visited[node-1] = True
	for nghbr in adj_list[node]:
		if add_s.visited[nghbr-1] == False:
			scc_passone(adj_list, nghbr, add_s)
	add_s.stack.append(node)

def flip_graph(graph_obj):
	mod_edges = [(edge[1], edge[0]) for edge in graph_obj.edges]
	mod_adjlist = [[] for vert in graph_obj.verts]
	for edge in mod_edges:
		mod_adjlist[edge[0]-1].append((edge[1]))
	return mod_adjlist

def scc_passtwo(adj_list, node, add_s):
	add_s.visited[node-1] = True
	for nghbr in adj_list[node-1]:
		if add_s.visited[nghbr-1] == False:
			add_s.stack.remove(nghbr)
			scc_passtwo(adj_list, nghbr, add_s)
	print add_s.visited

def strng_conn_comp(graph_obj):
	add_data = SCCAdditional(len(graph_obj.verts))
	for vert in graph_obj.verts:
		if add_data.visited[vert-1] == False:
			scc_passone(graph_obj.adj_list, vert, add_data)
	mod_adjlist = flip_graph(graph_obj)
	add_data.visited = [False for i in xrange(len(graph_obj.verts))]
	while len(add_data.stack) != 0:
		ele = add_data.stack.pop()
		if add_data.visited[ele-1] == False:
			scc_passtwo(mod_adjlist, ele, add_data)

#######################################################################
# Data structure (dictionary) used for output.
#######################################################################

trns_node = {
	1:'A',
	2:'B',
	3:'C',
	4:'D',
	5:'E',
	6:'F',
	7:'G'
}

#######################################################################
# Formatting functions for the algorithm's output.
#######################################################################

def format_top_sort(result):
	print "The topological sort of the first graph is:\n\nVertex\tNumber"
	for i in xrange(len(result)):
		print trns_node[result[i]] + "\t" + str(i+1)

def format_dijkstra(result, start_node):
	print "Shortest path for the graph: "
	for ind in xrange(len(result)):
		print "Shortest path from " + trns_node[start_node] + " to " + trns_node[ind + 1] + " is of distance " + str(result[ind])

def format_kruskal(result):
	print "The edges in the minimum spanning tree are:"
	print [(trns_node[edge[0]],trns_node[edge[1]]) for edge in result[0]]
	print "It's cost is " + str(result[1]) + "."

def format_articulation(result):
	result = [index+1 for index, value in enumerate(result) if value == True]
	result = [trns_node[element] for element in result]
	print "The articulation points of the given graph are " + ', '.join(result) + "."

def format_scc(result):
	print "The strongly connected components of the graph are:"
	for res in result:
		print res

#######################################################################
# Main function to invoke all code written above.
#######################################################################

def main():
	data = inp_parse('input.dat')
	graph_objects = []
	for i in xrange(1,7):
		if i in [1,4,5,6]:
			graph_objects.append(UnweightedGraph(conv_wei2unwei(data[0][i])))
		else:
			graph_objects.append(WeightedGraph(data[0][i]))
	root_dict = data[1]
	print "\nProblem 1:\n"
	res_one = top_sort_kahn(graph_objects[0])
	format_top_sort(res_one)
	print "\nProblem 2:\n"
	res_two = dijkstra_wrapper(graph_objects[1],0)
	format_dijkstra(res_two, 1)
	print "\nProblem 3:\n"
	res_three = kruskal(graph_objects[2])
	format_kruskal(res_three)
	print "\nProblem 4:\n"
	res_four = arti_wrapper(graph_objects[3],root_dict[4])
	format_articulation(res_four)
	print "\nProblem 5:\n"
	res_five = arti_wrapper(graph_objects[4],root_dict[5])
	format_articulation(res_five)
	print "\nProblem 6:\n"
	#strng_conn_comp(graph_objects[5])

if __name__ == "__main__":
	main()