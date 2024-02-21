## 函数input（）的工作原理 
### 使用while循环
while 条件：
	循环体

符合循环条件的会进入循环。
### 让用户选择合适退出
```python
prompt = "\nTell me something,and I will repeat it back to you"
prompt += "\nEnter 'quit' to end the program"
message= ""
while message !='quit':
    message = input(prompt)
    print(message)
```
### 使用标志

```python
active = True
print("请选择：1.登录，2.退出")
result_select = ("请选择(1/2：")
result_select = input("请选择(1/2)：")
if result_select != 1:
    print(active)
else:
    print(result_select)
```
