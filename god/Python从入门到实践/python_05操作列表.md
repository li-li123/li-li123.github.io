# 操作列表
## 遍历整个列表
```python
class List_Operate():
    list_b = [40, 50, 60, 70]
    def list_traverse(self):
        for i in self.list_b:
            print(i)


if __name__ == '__main__':
    parament = List_Operate()
    parament.list_traverse()
```
### 深入研究循环
for 循环
## 创建数值列表
### 使用函数range()
### 使用ranger创建数字列表

```python

class List_Operate():
    list_b = [40, 50, 60, 70]
    def list_traverse(self):
        for i in self.list_b:
            print(i,end='、')
    def list_num_20(self):
        for number in range(20):
            print(number, end='、')

    def list_num_1000000(self):
        
if __name__ == '__main__':
    parament = List_Operate()
    parament.list_traverse()
    print('\n')
    parament.list_num_20()
    print('\n')
```
## 使用列表的一部分

