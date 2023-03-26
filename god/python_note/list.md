## 列表

### 列表的遍历

```python
list_a = [[1,2,3],[4,5,6],[7,8,9]]
for i in range(len(list_a)):
    for j in range(len(list_a[i])):
        print(list_a[i][j],end=',')
```

#### 切片的索引方式

注意事项：切片一个完整的切片是包含三个参数和两个冒号" : " ,用于分隔三个参数(start_index、end_index、step)

当只有一个“:”时，默认第三个参数step=1；当一个“:”也没有时，start_index=end_index，表示切取start_index指定的那个元素

切片索引没有边界的限制

```Python
List_a = [[1,2,3],[4,5,6],[7,8,9]]
print (List_a[:4])
```

也可以通过切片对列表进行修改，如下所示

```python
list_a = ['wang','xiao', 'ning']
list_b = ['zhang', 'meng','li']
list_a[0:2] =list_b[0:2]
print(list_a)
```

可以通过切片对列表进行添加

```python
list_a = ['wang','xiao', 'ning']
list_b = ['zhang', 'meng','li']
list_a[0:2] =list_b[0:2]
print(list_a)
list_a[1:2] = list_b
print(list_a)
```

#### 查找列表中最大或最小值

首先假设一个最小值min_num，通常是min_um=list[0],然后会和后面的每一个列表元素进行比较，遇到更小的值时便将min_num替换为该值，如此循环直至列表遍历完成，最后的min_num值便是一小值

```python
list_a = [4,5,67,8,2,1,9,90]
min_num = list_a[0]
for num in list_a:
    if num < min_num:
        min_num = num
print (min_num)
```

### 列表的合并

```python
list_a = [1,2,3]
list_b = [4,5,6]
print(list_a + list_b)
print(list_a *3)
```

### 列表增长

appenf的增长是囫囵个的添加

```python
list_a = [1,2,3]
list_b = [4,5,6]
list_a.append(4)
list_a.append(list_b)
```
