class Graph():
    def __init__(self):
        self.verts = None
        self.adj_list = None
        self.edges = [(node,snode) for snode in self.adj_list.get(node) for node in self.verts]

    def get_nghbr(self,vert):
        return self.adj_list.get(vert)

    def get_edges(self):
        return self.edges
    
    def get_verts(self):
        return self.verts
    
    def get_adj_list(self):
        return self.adj_list

    def set_graph(self):
        vert_num = input("Enter the number of vertices:")
        self.verts = [vert for vert in xrange(1,vert_num+1)]
        self.adj_list = {vert:[] for vert in self.verts}
        possible_edges = [str(i) + ',' + str(j) for i in self.verts for j in self.verts]
        print "Enter the edges between vertices, separated by a comma:\nEnter 0 to end."
        while True:
            edge = raw_input("Edge: ")
            if edge == '0':
                break
            elif edge in possible_edges:
                nodes = edge.split(',')
                self.adj_list[int(nodes[0])] += [int(nodes[1])]
                self.adj_list[int(nodes[1])] += [int(nodes[0])]
