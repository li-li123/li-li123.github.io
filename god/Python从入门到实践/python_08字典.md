# 字典
## 使用字典
每个键都与一个值相关联，可以使用键来访问与之相关联的值。与键相关联的值可以使数字、字符串、列表乃至字典，
```python
dict_0 = {'color':'read',
          'points':5,
          'pizza':['mushrooms', 'olives', 'green peppers', 'pepperoni', 'pineapple', 'extra cheese'],
          }
print(dict_0)
```
### 访问字典中的值
1. 与键相关联的值，可一次制定字典名和方在方括号内的键
```python
print(dict_0['pizza'][2])
```
### 添加键值对
```python
alien_0 = {'color':'Green','points':5}
alien_0['x_position'] = 0
alien_0['y_position']=25
print(alien_0)
```
### 先创建一个字典
空字典添加键-值对，先使用空的花括号定义一个字典，在分行添加各个键-值对。
