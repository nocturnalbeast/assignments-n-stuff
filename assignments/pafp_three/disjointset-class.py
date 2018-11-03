class DisjointSet():
    def __init__(self,size):
        self.size = size
        self.elements = [num for num in xrange(self.size)]

    def find(self, ind_one, ind_two):
        return self.elements[ind_one] == self.elements[ind_two]

    def union(self, ind_one, ind_two):
        val = self.elements[ind_one]
        for ind in xrange(self.size):
            if self.elements[ind] == val:
                self.elements[ind] = self.elements[ind_two]