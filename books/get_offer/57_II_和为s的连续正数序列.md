## 题目

> [剑指 Offer 57 - II. 和为s的连续正数序列](https://leetcode-cn.com/problems/he-wei-sde-lian-xu-zheng-shu-xu-lie-lcof/)

输入一个正整数 target ，输出所有和为 target 的连续正整数序列（至少含有两个数）。

序列内的数字由小到大排列，不同序列按照首个数字从小到大排列。

 

示例 1：

```text
输入：target = 9
输出：[[2,3,4],[4,5]]
```


示例 2：

```text
输入：target = 15
输出：[[1,2,3,4,5],[4,5,6],[7,8]]
```


限制：

* 1 <= target <= 10^5




## 解题思路

滑动窗口算法适用于: **在一个区间内寻找需要的解**.   本题的思路在于滑动窗口算法, <span style='color: red'>一般的滑动窗口题目, 有一个固定的区间. 本题没有显示的固定区间, 如果把区间定义为连续正整数序列, 就是一般的滑动窗口题目</span>

```java
class Solution {
    public int[][] findContinuousSequence(int target) {
        int left = 1, right = 2, res = 3;
        List<Pair<Integer, Integer>> cache = new ArrayList<>();

        while (left < right){
           if(res<target){
               // 区间结果比要寻找的结果小, 扩大窗口
               right ++;
               res += right;
           }else if(res>target){
               // 区间结果比寻找的结果大, 缩小窗口
               res -= left;
               left ++;
           }else {
               // 找到一个解, 移动窗口, 重新寻找解
               cache.add(new Pair<>(left, right));
               res -= left;
               left ++;
           }
        }
        
        // 生成答案
        int[][] result = new int[cache.size()][];
        int position = 0;
        for(Pair<Integer, Integer> element : cache){
            int start = element.getKey(), end = element.getValue();
            int[] temp = new int[end - start + 1];
            for (int i = start, j = 0; i <=end ; i++, j++) {
                temp[j] = i;
            }
            result[position] = temp;
            position++;
        }

        return  result;

    }
}
```

