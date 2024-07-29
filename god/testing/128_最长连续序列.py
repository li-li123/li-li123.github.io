class Solution:
    def longestConsecutive(self, nums):
        min_num = nums[0]
        for num in nums:
            if min_num >num:
                min_num,num = num,min_num
            else:
                continue
        print(min_num)
        numlist=[]
        for num in nums:
           numlist[num-min_num] = 5
        print(numlist) 



if '__main__' == __name__:
    strs = [100,4,200,2,3,1]
    A = Solution()
    A.longestConsecutive(strs)