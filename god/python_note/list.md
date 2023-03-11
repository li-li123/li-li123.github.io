## 列表

### 列表的遍历

```python
list_a = [[1,2,3],[4,5,6],[7,8,9]]
for i in range(len(list_a)):
    for j in range(len(list_a[i])):
        print(list_a[i][j],end=',')
```

方法一：直接查询列表
