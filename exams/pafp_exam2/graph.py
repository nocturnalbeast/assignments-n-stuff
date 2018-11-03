# Question to input a graph and see whether it contains a cycle or not
# This is a solution that utilizes a technique akin to Kruskal's algorithm
# but strips all the unnecessary functionality for the minimal function,
# thus maximizing performance.

# Utilizing a simplified version of a complete graph class to handle the 
# inputs and convert it into the graph data.
class Graph:
    # Init function to initialize instance variables of a class.
    def __init__(self):
        # verts - the list of all the vertices. Initialized to an empty list.
        self.verts = []
        # adj_list - the adjacency list. Initialized to an empty dictionary.
        self.adj_list = {}
        # edges - the list of all the edges. Initialized to an empty list.
        self.edges = []

    # Function to handle input and convert into the graph class elements, thus creating
    # a finalized instance of the graph class.
    def set_graph(self):
        # Getting the number of vertices and assigning it to vert_num.
        vert_num = input("Enter the total number of vertices in the graph:")
        # Generating the list of all the vertices with a list comprehension.
        # The vertices are numbered like 1, 2, 3, 4 etc.
        self.verts = [vert for vert in xrange(1,vert_num+1)]
        # Generating an adjacency list, albeit with all the adjecency entries set to none
        # i.e. there will be vertices but no adjacency entries for all the vertices in the 
        # list.
        self.adj_list = {vert:[] for vert in self.verts}
        # Generating a list of possible edges, this is just for validation of input edges.
        # Each edge is a string like "1,2" etc.
        p_edges = [str(i) + ',' + str(j) for i in self.verts for j in self.verts if i < j]
        # Prompting the user to enter the edges.
        print "Enter the edges with vertices separated by comma. Enter 0 if done."
        # Infinite loop that is broken only when the user inputs the value '0'.
        while True:
            # The user is required to input a string that is either a valid edge input in
            # the form '1,2' etc. or the value '0' to signal the end of the set of edges.
            edge = raw_input("Edge: ")
            # If condition to break the loop if the input is the value '0'.
            if edge == '0':
                # Break statement.
                break
            # If the user inputs an edge instead of the value '0', then it is checked if
            # the edge or its reverse is present in the list of possible edges.
            # If yes, it will create respective entries in the adjacency list.
            elif edge in p_edges or edge[::-1] in p_edges:
                # Getting the vertices out of the string and sorting them.
                # Sorting is optional.
                nodes = sorted(edge.split(','))
                # Adding the second vertex to the adjacency list of the first vertex.
                self.adj_list[int(nodes[0])] += [int(nodes[1])]
                # Adding the first vertex to the adjacency list of the second vertex.
                self.adj_list[int(nodes[1])] += [int(nodes[0])]
        # Populating the initally empty list of edges with all possible 
        # that are essentially a list of tuples that contain two vertices.
        # The resulting list looks like this - [(1,2), (1,3), (2,3), (2,4)]
        self.edges = [(node,snode) for node in self.verts for snode in self.adj_list.get(node) if node < snode]

# This is the function that actually checks the graph instance to see whether the
# graph contains a cycle or not.
def kru_mod():
    # Generating an object of the graph class.
    gph = Graph()
    # Now calling the set_graph function to get values from the user and set up
    # the data elements of the class object.
    gph.set_graph()
    # Initalizing a list of all travelled vertices. Now an empty list.
    ver_lst = []
    # Iterating through all the edges in the graph using its edges list.
    for i in xrange(len(gph.edges)):
        # If both the vertices in the edge are present in the list of travelled
        # vertices, it means that this edge will create a cycle. Thus, stop the
        # function from further running by means of the return function that 
        # returns the result string.
        if gph.edges[i][0] in ver_lst and gph.edges[i][1] in ver_lst:
            # Return statement with the result string that is triggered when 
            # the above condition is fulfilled.
            return "The graph contains a cycle!"
        # If both the vertices in the edge are not present in the list of travelled
        # vertices, it means that the edge does not create a cycle, so the vertices
        # of the edge are added to the list of travelled vertices.
        else:
            # Adding the first vertex of the edge to the list of travelled vertices.
            ver_lst.append(gph.edges[i][0])
            # Adding the second vertex of the edge to the list of travelled vertices.
            ver_lst.append(gph.edges[i][1])
    # If the loop completes without triggering the condition necessary for the cycle
    # it means that there is no cycle, and thus end the function with the return
    # statement with the result string indicating that there is no cycle.
    return "The graph does not contain a cycle."

# Call the function to checks the graph instance to see whether it contains a cycle.
print kru_mod()
