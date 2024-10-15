class Solution:
    def removeElement(self, nums, val: int) -> int:
        p1 = p2 = 0
        while p2<len(nums):
            if  nums[p2] != val:
                nums[p1] = nums[p2]
                p1 +=1               
            p2 += 1
        return p1
    def removeElement1(self, nums, val: int) -> int:
        k=0
        for num in nums:
            if num !=val:
                k +=1
        return k
            

        












if __name__ == '__main__':
    A = Solution()
    nums = [3,2,2,3]
    val = 3
    print(A.removeElement(nums,val))