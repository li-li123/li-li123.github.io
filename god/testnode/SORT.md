## 排序
### 插入排序
#### 基本思想
1. 从第一个元素开始，该元素可以认为已经被排序
2. 取下一个元素tem，从已排序的元素序列从后往前扫描
3. 如果该元素大于tem，则将发元素移到下一位
4. 重复步骤3，直到找到已排序元素中小于等于tem的元素
5. tem插入到该元素的后面，如果已排序所有元素都大于tem，则将tem插入到下表为0的位置
6. 重复步骤2~5
#### 方法分析一：
1. j = i-1：的意思是指key是从i位置取出的，然后key只需要和前面的元素进行比较
2. while j >=0 and key < param[j]:如果key前面的数比key大，则继续循环继续查找，直到碰到第一个比key小的数之后不再进入循环
   while （条件）：{
      循环体语句
   }
   while循环的执行过程是：先判断条件是否成立，如果成立则执行循环体语句，然后再次判断条件是否成立，如果成立则再次执行循环体语句，以此类推，知道条件不成立时跳出循环。
3. param[j+1] = key：如果param[j]<key,则吧key插入param[i]后面
#### 代码实现
```python
def InsertSort(self,param):
        # 首先判断列表是否为空，
        if len(param) <= 1:
            return param
        else:
            # 从第2个数开始比较
            for i in range(1,len(param)):
                # 首先将第2个数存在key里面
                key = param[i]
                # 然后从key开始依次向前遍历
                j = i-1
                # j不为负且key的值比前面的数小，都会进行下面的操作
                while j >=0 and key < param[j]:
                    # 第一步：先把key前面的数往后挪一位
                    param[j+1] = param[j]
                    # 为下一个数比较做准备，j向前移一位
                    j =j- 1
                # 当key>param[j]时，将key插入到j所指的下一个位置
                param[j+1] = key
            return param
```

```python
    def InsertStort(self,param):
        for end in range(1,len(param)):
            for start in range(0,end):
                if param[start] > param[end]:
                    param[start],param[end] = param[end],param[start]
        return param
```
#### 图片
#### 直接插入排序的特性总结
1. 时间复杂度：最坏情况下为O(N*N),此时待排序列为逆序，或者说接近逆序
               最好情况下为O(N),此时待排序为升序，或者说接近升序。
2. 空间复杂度：O(1),它是一种稳定的排序算法
### 希尔排序

### 选择排序
#### 基本思想
1. 选择排序就是将待排序数组中最小数放在最前面，将最大数放在最小位置（这一步要求将最小位置和最大位置记录下来，在遍历待排序的元素时将最小元素和最大元素算出来）
### 堆排序
 
### 冒泡排序
#### 代码实现
```python
    def BubbleSort(self,arr):
        n = len(arr)
        for i in range (n):
            for j in range(0,n-i-1):
                if arr[j]>arr[j+1]:
                    arr[j],arr[j+1] = arr[j+1],arr[j]

        return arr
```

### 快速排序递归实现

### 快速排序hoare版本
### 快速排序挖坑法
