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
```python
alice_1 = {}
alice_1['color']='green'
alice_1['point']=5
print(alice_1)
```
### 修改字典中的值
要修改字典中的值，可一次制定自点名、用方括号括起的键以及与该键相关联的新值。
```python
alien_0 = {'color': 'green'}
print("The alien is " + alien_0['color'] + ".")
alien_0['color'] = 'yellow'
print("The alien is now " + alien_0['color'] + ".") 
```
对一个能够以不同速度移动的外星人的位置进行跟踪。为此，我们将存储该外星人的当前速度，并据此确定该外星人将向右移动多远：
```python
alien_0 = {'x_position': 0, 'y_position': 25, 'speed': 'medium'}
print("Original x-position: " + str(alien_0['x_position']))
# 向右移动外星人
# 据外星人当前速度决定将其移动多远
if alien_0['speed'] =='slow':
    x_increment = 1
else:
    x_increment = 3

alien_0['x_position'] = alien_0['x_position']+x_increment
print("New x-position: " + str(alien_0['x_position']))
```
### 删除键-值对
```python
alien_0 = {'x_position': 0, 'y_position': 25, 'speed': 'medium'}
print(alien_0)
del alien_0['speed']
print(alien_0)
```
### 由类似对象组成的字典
```python
favorite_languages = {
 'jen': 'python',
 'sarah': 'c',
 'edward': 'ruby',
 'phil': 'python',
 }

print("Sarah's favorite language is " + favorite_languages['sarah'].title() + '.')
```
