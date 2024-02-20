# 嵌套
有时候需要键一系列字典存储在列表中，或将列表作为值存储在字典中，这成为嵌套。
### 字典列表
```python
alien_0 = {'color': 'green', 'points': 5}
alien_1 = {'color': 'yellow', 'points': 10}
alien_2 = {'color': 'red', 'points': 15}

aliens = [alien_0,alien_1,alien_2]
print(aliens)
for alien in aliens:
    print(alien)
```
2. 更符合现实的情形是，外星人不止三个，且每个外星人都是使用代码自动生成的。在下面的示例中，我们使用range()生成了30个外星人：
```python

aliens = []
for aliens_number in range(30):
    new_alien = {'color':'green','point':5,'speed':'slow'}
    aliens.append(new_alien)
for alien in aliens[:5]:
    print(alien)
print('...')
```
### 在字典中存储列表
```python
pizza = {'crust':'thick',
         'topping':['mushrooms','extra cheese']}
print ('You ordered a'+pizza['crust']+'-crust pizza'+"with the followering toppings:")
for topping in pizza['topping']:
    print('\t'+topping)
```
### 在字典中存储字典
