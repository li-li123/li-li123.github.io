# Day01
## 知识点一：拷贝与赋值的区别，is和‘==’的区别
### 深拷贝、浅拷贝、赋值
赋值：只是复制了新对象的引用，不会开辟新的内存空间。复制后，引用和内存id是一致的
浅拷贝：创建新对象，器内容是对原对象的引用，id不一致 ，
深拷贝：拷贝了父对象及其子对象，即复制了一块新的内存保存值

### ‘==’和is
- == 运算符比较的是两个变量所指代的值是否一致，只要求值一致即可
- is 比较的是对象，要求id一致，值一致
#### 示例：
```python
import copy
list_1 = [1, 2, [3, 4]]
list_2 = list_1
print(f'list_1的id{id(list_1)}')
print(f'list_2的id{id(list_2)}')
list_3 = copy.copy(list_1)
print(f'list_3的id{id(list_3)}')
list_4 = copy.deepcopy(list_1)
print(f'list_4的id{id(list_4)}')
print(list_2 is list_1)
print(list_3 is list_1)
print(list_3 == list_1)
print(list_4 is list_1)
print(list_4 == list_1)
```
运算结果：
```
list_1的id3244473736256
list_2的id3244473736256
list_3的id3244473900992
list_4的id3244473900864
True
False
True
False
True
```
## 知识点二：strip([字符串])
只要头尾包含有指定字符序列中的字符就删除
### 算法是：
从头删除
i ∈（0~len(str)）i = 0时，判断str[0] 是否∈chars中，存在则删除str[0]，继续遍历下一个，否则strs = str
从尾删除
j∈（len（strs),0) j= len(strs)时，判断strs[j]是否∈chars中，存在则删除strs[j]，继续往前遍历下一个，否则strss = strs， 
### 实现：
```python
def strip_result(str_name,chars)->str:
    strs = ''
    strss = ''
    for i in range(len(str_name)):
        if str_name[i] in chars:
            strs = str_name[i + 1:]
        else:
            break
    for j in range( len(strs)-1,0,-1):
        if strs[j] in chars:
            strss = strs[:j]
        else:
            return strss
str1 = "hello world hello world"
chars = "whedloe"
print(strip_result(str1,chars))
```
输出结果：
```
 world hello wor
```
### 示例
```python
str = "hello world hello world"
print(str.strip("whedlo"))
```
strip()删除头尾的字母，对被删除的字母没有固定顺序要求，
运算结果：
````
world hello wor
````
## 知识点三：‘+’的使用
### 字符串拼接
拼接符左右要求是字符串，字符串拼接处来的结果也是字符串
### 数值型加法
### 列表追加
```python
a,b = [1,2,3],['as','de','12']
print(a+b)
```
输出结果：
```
[1, 2, 3, 'as', 'de', '12']
```
## 知识点四： %的用处
### 数值运算
模运算-求余
```python
11%2
```
输出结果
```
1
```
### %操作符
表示方法：%[(name)][flags][width].[precision]typecode
- (name) 为命名
- flag中，+表示右对齐，-表示左对齐，''表示左侧填一个空格（目的是与负数对齐），0表示用0填充
-  width表示显示宽度
- precision表示小数点后的精度
- typecode：
```
%s 字符串 (采用str()的显示)
%r 字符串 (采用repr()的显示)
%c 单个字符
%b 二进制整数
%d 十进制整数
%i 十进制整数
%o 八进制整数
%x 十六进制整数
%e 指数 (基底写为e)
%E 指数 (基底写为E)
%f 浮点数
%F 浮点数，与上相同
%g 指数(e)或浮点数 (根据显示长度)
%G 指数(E)或浮点数 (根据显示长度)
%% 字符"%"
```
#### 示例1：
```python
print('dji%5.2f'%2.5)
```
输出结果：
```
dji 2.50
```
%5.2f：显示格式说明，5为显示宽度，2为小数点位数，f为浮点数类型
%2.5 ：该%为显示的内容来源，输出结果默认右对齐，2.50长度为4，故前面添加了一个空格

> ```python
> print('dji%-6.2f'%2.5)
> ```

输出结果：
```
dji2.50 
```
#### 示例2：
```python
print("%+7x" % 11)
```
十进制11转为十六进制整数为b，右对齐并增加+号，+b占两位，左侧添加5个空格。
输出结果：
```
     +b
```
## 表达式和赋值语句
```python
a='sedkf'
a*2
print(a)
```
输出结果：
```
sedkf
```
## B+Tree/Hash_Map/STL Map
- Hash ：根据散列值直接定位数据的存储地址，能够在长数据下找到需要的数据，更加适用于内存中的查找
- B+树：是树状结构，适合索引，对于磁盘数据 来说，索引更高效，也就是说针对磁盘存储的数据查找更高效
- STL_Map：就是红黑树，只在内存中建立二叉树，不能用于磁盘操作，但是在内存中查找性能的话比不上Hash
## None的数据类型
"None" 是 Python 中的一个特殊类型，表示一个空对象或者空值。在 Python 中，它是一个关键字，用于表示没有值或者空值。可以用 None 来初始化一个变量，或者作为函数的返回值。
```python
print(type(None))
print(type(type('')))
```
输出结果：
```
<class 'NoneType'>
<class 'type'>
```
## extend、insert、append使用方法
### extend()
extend()将列表一个一个元素添加到另一个列表中
```python
a=[]
a.extend([1,2,8,9])
print(a)
```
输出结果
```
[1, 2, 8, 9]
```
### insert()
insert(index,X)：将元素X添加到下标为index的位置上
```python
a.insert(3,4)
print(a)
```
输出结果
```
[1, 2, 8, 4, 9]
```
### append()
append()将列表整体添加至另一个列表
```python
a.append([5,6])
print(a)
```
输出结果
```
[1, 2, 8, 4, 9, [5, 6]]
```
## 字典的创建
### 方法一：
将两个列表/元组打包成一个元组对象，然后利用dict/list来构造相应的数据类型
```python
dic1 = {1:'a',2:'b'}
dic2 = {3:'c',4:'d'}
a=(1,2,3,4)
b=('a','b','c','d')
print(dict(zip(a,b)))
```
输出结果
```
{1: 'a', 2: 'b', 3: 'c', 4: 'd'}
```
### 方法二：
update()：方法添加键值对，如果键已经存在，则覆盖原有的值，如果键不存在，则添加键值对。
```python
dic1 = {1:'a',2:'b'}
dic2 = {3:'c',4:'d'}
dic1.update(dic2)
print(dic1)
```
输出结果
```
{1: 'a', 2: 'b', 3: 'c', 4: 'd'}
{1: 'a', 2: 'b', 3: 'c', 4: 'f'}
```
