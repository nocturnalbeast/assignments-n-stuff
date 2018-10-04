class NumArray(object):

    def __init__(self, nums):
        self.length = len(nums)
        self.nums = nums
        self.cache = {}
        self.cache_fun()

    def cache_fun(self):
        for i in xrange(len(self.nums)):
            for j in xrange(i+1,len(self.nums)):
                sum = 0
                for k in xrange(i,j):
                    sum += k
                self.cache[(i,j)] = sum

    def sumRange(self, i, j):
        return self.cache[(i,j)]