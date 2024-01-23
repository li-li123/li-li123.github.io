# 元组
不可变列表
## 定义元组
元组看起来犹如列表，但使用圆括号而不是方括号来标识。定义元组后，就可以使用索引来
访问其元素，就像访问列表元素一样。
## 遍历元组中的所有值
1. 像列表一样，使用for循环遍历元组：
```python
set_a = (1,2,3,4,5,6,7,8,9,10)
for number in set_a:
    print(number,end='、')
```
## 修改元组
虽然不能修改元组的元素，但可以给存储元组的变量赋值。因此，如果要修改前述矩形的尺
寸，可重新定义整个元组
```python
dimensions = (200, 50)
print("Original dimensions:")
for dimension in dimensions:
    print(dimension)
dimensions = (400, 100)
print("\nModified dimensions:")
for dimension in dimensions:
     print(dimension)
```
