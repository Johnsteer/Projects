class Solution(object):
    def twoSum(self, nums, target):
        
        hashmap = dict()
        result = list()
        
        for i, v in enumerate(nums):
            if hashmap.get(v) is None:
                hashmap[target - v ] = i
            else:
                result = [hashmap[v], i]    
                
        return result
