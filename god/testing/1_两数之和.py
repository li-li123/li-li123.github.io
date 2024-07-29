class Solution:
    def twoSum(self, nums, target):
        if len(nums) ==0:
            return []
        num_dic = {}
        for i in range(len(nums)):
            if nums[i] not in num_dic.keys():
                need = target-nums[i] 
                num_dic[need] = i
            else:
                return [ num_dic[nums[i]],i]



if '__main__' == __name__:
    nums = [3,2,3]
    A = Solution()
    print(A.twoSum(nums,6))