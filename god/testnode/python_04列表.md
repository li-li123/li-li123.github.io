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
