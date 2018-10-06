num_nodes = input("Enter the number of nodes:")
adj_list = {node:[] for node in xrange(1,num_nodes+1)}

print "Enter the edges between node numbers, separated by a comma:\nEnter 0 to end."

while True:
    vertice = raw_input("Vertice: ")
    if vertice == '0':
        break
    else:
        nodes = vertice.split(',')
        adj_list[int(nodes[0])] = adj_list[int(nodes[0])] + [int(nodes[1])]
        adj_list[int(nodes[1])] = adj_list[int(nodes[1])] + [int(nodes[0])]

for i in adj_list.keys():
    print i,":",adj_list[i]
