
class Solution:
    def moveZeroes(self, nums):
        if len(nums) == 0:
            return []
        k = 0
        while k <len(nums):
            if nums[k]==0:
                break     
            k=k+1
        for i in range(k+1,len(nums)):
            if nums[i] != 0:
                nums[k] = nums[i]
                nums[i]=0
                while k<len(nums):
                    if nums[k]==0:
                        break
                    k = k+1
        return nums
            
                





if __name__ == '__main__':
    nums = [1,0,0,3,4,0,8,3,0]
    A = Solution()
    print(A.moveZeroes(nums))