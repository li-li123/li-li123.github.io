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
        number_sum = 0
        list_a =[]
        for number in range(1,1000001):
            list_a.append(number)
            number_sum = number_sum+number
        return list_a,max(list_a),min(list_a),number_sum

    def odd_number_0_20(self):
        odd_list =[]
        for odd_number in range(1,20,2):
            odd_list.append(odd_number)
        return odd_list

    def odd_number_3_30(self):
        odd_list = []
        for number in range(3,31):
            if number%3 == 0:
                odd_list.append(number)
        return odd_list



if __name__ == '__main__':
    parament = List_Operate()
    parament.list_traverse()
    print('\n')
    parament.list_num_20()
    print('\n')
    # print(parament.list_num_1000000())
    print('\n')
    print(parament.odd_number_0_20())
    print('\n')
    print(parament.odd_number_3_30())
```
## 切片
在Python中，切片是对序列型对象（如列表、字符串、元组等）的一种高级索引方法。切片的语法为：sequence[start:stop:step]，其中，start表示起始位置，默认为0；stop表示结束位置，默认为序列的长度；step表示步长，默认为1
```python
class Slice():
    players = ['charles', 'martina', 'michael', 'florence', 'eli'] 
    def list_slice(self):
        leng = len(self.players)
        list_a =self.players[:leng-1] 
        list_b = self.players[:leng:2]
        list_c = self.players[3:]
        list_d = self.players[::2]
        list_e = self.players[::-1]
        return list_a,list_b,list_c,list_d,list_e
if __name__=="__main__":
    parament = Slice()
    print(parament.list_slice())
```
### 遍历切片
```python
class Slice():
    players = [1,2,3,4,5,6,7,8,9,10] 
    def list_slice(self):
        leng = len(self.players)
        list_a =self.players[:leng] 
        list_b = self.players[:7:2] 
        list_c = self.players[5:] 
        list_d = self.players[::2] 
        list_e = self.players[::-1]
        list_f = self.players[5::-1] 
        return list_a,list_b,list_c,list_d,list_e,list_f

def getList(arr, start, end, step) :
    if start == None:
        start = 0
    if end == None:
        end = len(arr)
    if step == None:
        step = 1
    res = list()

    index = start
    if step < 0:    
        while index > end:
            res.append(arr[index])
            index += step
        while index < end:
            res.append(arr[end-1])
            end +=step
    else:
        while index < end:
            res.append(arr[index])
            index += step

    return res
        
if __name__=="__main__":
    parament = Slice()
    a = [1,2,3,4,5,6,7]
    print(parament.list_slice())
    print(getList(a,None,None,-1))

```
### 复制列表
1. 方法一：切片
```python
list_a = [1,2,3,4,5,6,7,8,9,10]
print(list_a[:])
```
2. 方法二：for循环遍历
```python
list_a = [1,2,3,4,5,6,7,8,9,10]
print(list_a[:])
list_b=[]
for number in list_a:
    list_b.append(number)
print(list_b)
```
