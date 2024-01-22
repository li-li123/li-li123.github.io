# 变量和简单数据类型
## 变量
Python将始终记录变量的最新值
## 变量的命名和使用
- 变量名只能包含字母、数字和下划线。变量名可以字母或下划线打头，但不能以数字打
  头，例如，可将变量命名为message_1，但不能将其命名为1_message。
- 变量名不能包含空格，但可使用下划线来分隔其中的单词。例如，变量名greeting_message
  可行，但变量名greeting message会引发错误。
- 不要将Python关键字和函数名用作变量名，即不要使用Python保留用于特殊用途的单词，
  如print
- 变量名应既简短又具有描述性。例如，name比n好，student_name比s_n好，name_length 比length_of_persons_name好。 
- 慎用小写字母l和大写字母O，因为它们可能被人错看成1或0
## 字符串
### 修改字符串的大小写
1. title()将每个单词的首字母改为大写
```python
message = "hello world"
message=message.title()
print(message)
```
2.upper() 将字符串改为全部大写
3.lower（）将字符串改为全部小写
```python
print(message.upper())
print(message1.lower())
```
以上三种函数需要将变量存回到变量中。
4. iisupper() 判断字符串是否全部大写
5. islower() 判断字符串是否全部小写
```python
print(message.isupper())
print(message.islower())
```
### 合并（拼接）字符串
Python使用加号（+）来合并字符串
### 使用制表符或换行符来添加空白
\n,\t
### 删除空白
1. rstrip()能够找到字符串末尾多余的空白，需要将删除操作的结果存回到变量中
2. lstrip() 能够找到字符串开头多余的空白，需要将删除操作的结果存回到变量中
3. strip() 能够找到字符串开头和结尾多余的空白，需要将操作的结果存到变量中
```python
message = " hello world "
print(message.strip())
print(message.lstrip())
print(message)
message = message.lstrip()
print(message)
print(message.rstrip())
print(message)
message = message.rstrip()
print(message)
```
#### 使用字符串时避免语法错误
注意单双引号的使用
```python
message = "One of Python's strengths is its diverse community." 
```
## 数字
### 整数
对整数执行加减乘除立方
```python
print(3**3)
print(9**9)
```
###  浮点数
带小数点的数字都称为浮点数，对浮点数进行加减乘除
### 使用函数str()避免类型错误
将数字强制转换成字符串类型
```python
message = "Happy " + str(age) + "rd Birthday!"
```
