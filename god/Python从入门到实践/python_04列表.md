# 列表简介
## 列表是什么
按特定顺序排列的元素组成
### 列表可变，可以直接对列表操作增删改查
#### 列表新增
append()批量增加列表元素
extend() 逐个增加列表元素
### 列表删除
1. del 删除第一个元素
2. pop 删除最后一个元素
3. remove 删除指定的元素
### 列表修改
```python
class List_main():
    list_b = [40, 50, 60, 70]

    def list_append(self, list_a):
        self.list_b.append(list_a)
        return self.list_b

    def list_extend(self, list_a):
        self.list_b = [40, 50, 60, 70]
        self.list_b.extend(list_a)
        return self.list_b

    def list_del(self):
        del self.list_b[0]
        return self.list_b
    def list_pop(self):
        self.list_b.pop()
        return self.list_b
    def list_remove(self):
        self.list_b.remove(1)
        return self.list_b
    def list_revise(self,element):
        self.list_b[1] = element
        return self.list_b
if __name__ == '__main__':
    list_init = [10, 20, 30]
    list_init1 = [1, 2.3]
    parament1 = List_main()
    print(parament1.list_append(list_init))
    print(parament1.list_extend(list_init1))
    print(parament1.list_del())
    print(parament1.list_pop())
    print(parament1.list_remove())
    print(parament1.list_revise(90))
```
### 访问列表元素
```python
bicycles = ['trek', 'cannondale', 'redline', 'specialized'] 
print(bicycles[0])
```

1. 
### 列表索引
索引从0开始
1. 将索引指定为负数，从后往前索引。不能越界
## 列表

### 列表的遍历

```python
list_a = [[1,2,3],[4,5,6],[7,8,9]]
for i in range(len(list_a)):
    for j in range(len(list_a[i])):
        print(list_a[i][j],end=',')
```

切片的索引方式

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

首先假设一个最小值min_num，通常是min_um=list[0],然后会和后面的每一个列表元素进行比较，遇到更小的值时便将min_num替换为该值，如此循环直至列表遍历完成，最后的min_num值便是最小值，因为遍历了list中的每一个元素，所以时间复杂度尾n

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

appen()、extend()区别append()是在列表末尾添加新的对象（即整体添加至列表中），也可以单个元素的添加。

```Python

    def list_appden(self,list_a):
        self.list_b = [1,2,3,4,5,6,7,8,9,0]
        self.list_b.append(list_a)
        return self.list_b
```

extend()可以合并两个列表，list1.extend(list2),意思是将list2中的元素按顺序添加至list1中
