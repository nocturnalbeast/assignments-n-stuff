# Basic functions and classes that are not used in the solution, but are used as reference for the implementation of more complex algorithms and classes.

class Stack:
    def __init__(self):
        self.elements = []

    def is_empty(self):
        return len(self.elements) == 0

    #def is_full(self):
    #    return len(self.elements) == 100 #testvalue

    def size(self):
        return len(self.elements)

    def push(self,value):
        self.elements.append(value)
    
    def pop(self):
        self.elements.pop()

class Queue:
    def __init__(self):
        self.elements = []

    def is_empty(self):
        return len(self.elements) == 0

    #def is_full(self):
    #    return len(self.elements) == 100 #testvalue

    def size(self):
        return len(self.elements)

    def enqueue(self,value):
        self.elements.append(value)
    
    def dequeue(self):
        self.elements.pop(0)

def bfs(adj_list,root_node):
    que = Queue()
    visited = [False for i in xrange(len(adj_list))]
    que.enqueue(root_node)
    visited[root_node-1] = True
    while (not que.is_empty()):
        vertex = que.dequeue()
        for nghbr in adj_list[vertex-1]:
            if not visited[nghbr-1]:
                que.enqueue(nghbr)
                visited[nghbr-1] = True

def dfs_iterative(adj_list,root_node):
    stk = Stack()
    visited = [False for i in xrange(len(adj_list))]
    stk.push(root_node)
    visited[root_node-1] = True
    while (not stk.is_empty()):
        vertex = stk.pop()
        for nghbr in adj_list[vertex-1]:
            if not visited[nghbr-1]:
                stk.push(nghbr)
                visited[nghbr-1] = True

def reset_visited(size):
    visited = [False for i in xrange(size)]

visited = []
def dfs_recursive(adj_list,node):
    visited[node-1] = True
    for nghbr in adj_list[node-1]:
        if not visited[node-1]:
            dfs_recursive(adj_list,nghbr)

def connected_components(adj_list):
    count = 0
    for node in xrange(len(adj_list)):
        if not visited[node-1]:
            dfs_recursive(adj_list,node)
            count += 1
    return count

