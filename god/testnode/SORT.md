## 排序
### 插入排序
#### 基本思想
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
