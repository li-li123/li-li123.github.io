# 使用if语句处理列表
1. 对列表中特定的值做特殊处理
2. 高效地管理不断变化的情形
### 检查特殊元素
1.循环输出列表元素 
```python
requested_toppings = ['mushrooms', 'green peppers', 'extra cheese']
for requested_topping in requested_toppings:
    print("Adding " + requested_topping + ".")
print("\nFinished making your pizza!")
```
### 确定列表不是空的
1. 判断列表是否为空
```python
requested_toppings = ['mushrooms', 'green peppers', 'extra cheese']
if requested_toppings:
    for requested_topping in requested_toppings:
        print("Adding " + requested_topping + ".")
    print("\nFinished making your pizza!")
else:
    print("Are you sure you want a plain pizza?")
```
### 使用多个列表
1. 检查一个列表中的元素是否在另一个列表中
```python
available_toppings = ['mushrooms', 'olives', 'green peppers', 'pepperoni', 'pineapple', 'extra cheese']
requested_toppings = ['mushrooms', 'french fries', 'extra cheese']
for requested_topping in requested_toppings:
    if requested_topping in available_toppings:
        print("Adding"+ requested_topping +",")
    else:
        print("Sorry, we don't have " + requested_topping + ".")
```
