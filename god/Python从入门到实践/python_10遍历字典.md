# 遍历字典
### 遍历所有的建-值对
1. 字典存储有关网站用户的信息
```python
user_0 = {
    "username": 'efermi',
    'first':'enrico',
    'last':'fermi',
}
for key,value in user_0.items():
    print('\nkey:'+key)
    print('value:'+ value)
```
2. python不关心键-值对的存储顺序，而只跟踪键和值之间的关联关系
### 遍历字典中所有键
```python
user_0 = {
    "username": 'efermi',
    'first':'enrico',
    'last':'fermi',
}
for key in user_0.keys():
    print(key)
```

```python

favorite_languages = {
 'jen': 'python',
 'sarah': 'c',
 'edward': 'ruby',
 'phil': 'python',
 }

friend = ['phil','sarah']

for key in favorite_languages.keys():
    print(key.title())
    if key in friend:
        print("Hi"+key.title()+",I see you favorite language is "+favorite_languages[key].title()+"|")
```
### 按顺序遍历字典中的所有键
字典总是明确地记录键和值之间的关联关系，但获取字典的元素时，获取顺序是不可预测的。这不是问题，因为通常你想要的只是获取与键相关联的正确的值。
要以特定的顺序返回元素，一种办法是在for循环中对返回的键进行排序。为此，可使用函数sorted()来获得按特定顺序排列的键列表的副本
```python
favorite_languages = {
 'jen': 'python',
 'sarah': 'c',
 'edward': 'ruby',
 'phil': 'python',
 }
for key in sorted(favorite_languages.keys()):
    print(key.title() + ", thank you for taking the poll.")
```
### 遍历字典中的所有值
1. 可使用方法values()，它返回一个值列表，而不包含任何键。
```python
favorite_languages = {
 'jen': 'python',
 'sarah': 'c',
 'edward': 'ruby',
 'phil': 'python',
 }
for value in favorite_languages.values():
    print(value)
```
2. 以上做法只是把所有的的值列出来，但是没有考虑到去重问题。
```python
favorite_languages = {
 'jen': 'python',
 'sarah': 'c',
 'sarah1': 'c',
 'edward': 'ruby',
 'phil': 'python',
 }
favorte_list = []
for value in favorite_languages.values():
    favorte_list.append(value)
print(set(favorte_list))
```
