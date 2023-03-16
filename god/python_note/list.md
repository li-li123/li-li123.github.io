## 列表

### 列表的遍历

```python
list_a = [[1,2,3],[4,5,6],[7,8,9]]
for i in range(len(list_a)):
    for j in range(len(list_a[i])):
        print(list_a[i][j],end=',')
```

方法一：切片的索引方式

注意事项：切片一个完整的切片是包含三个参数和两个冒号" : " ,用于分隔三个参数(start_index、end_index、step)

当只有一个“:”时，默认第三个参数step=1；当一个“:”也没有时，start_index=end_index，表示切取start_index指定的那个元素

切片索引没有边界的限制

```Python
List_a = [[1,2,3],[4,5,6],[7,8,9]]
print (List_a[:4])
```

### 列表的合并和

```python
list_a = [1,2,3]
list_b = [4,5,6]
print(list_a + list_b)
print(list_a *3)
```

列表增长

appenf的增长是囫囵个的添加

```python
list_a = [1,2,3]
list_b = [4,5,6]
list_a.append(4)
list_a.append(list_b)
```
