class Solution:
    def twoSum(self, nums, target):
        for i in xrange(len(nums)):
            for j in xrange(i+1,len(nums)):
                if nums[i]+nums[j] == target:
                    return [i,j]
        return []