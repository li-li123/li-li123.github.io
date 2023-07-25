## 排序
### 插入排序
#### 基本思想
1. 从第一个元素开始，该元素可以认为已经被排序
2. 取下一个元素tem，从已排序的元素序列从后往前扫描
3. 如果该元素大于tem，则将发元素移到下一位
4. 重复步骤3，直到找到已排序元素中小于等于tem的元素
5. tem插入到该元素的后面，如果已排序所有元素都大于tem，则将tem插入到下表为0的位置
6. 重复步骤2~5
```python
    def InsertStort1(self,param):
        for start in range(len(param)-1):
            end = start
            tem = param[end+1]
            while (end >= 0):
                if tem < param[end]:
                    param[end+1] = param[end]
                    end = end-1
                else:break
            param[end+1] =tem
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
#### 
### 希尔排序
### 选择排序
### 堆排序
 
### 冒泡排序
 
### 快速排序递归实现

### 快速排序hoare版本
### 快速排序挖坑法
