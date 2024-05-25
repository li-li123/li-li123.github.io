def calc(self,number):
    sum =0
    for n in number:
        sum += n*n
    return sum
    
print(calc([1,2,3]))