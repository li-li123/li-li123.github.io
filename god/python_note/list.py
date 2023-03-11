
class Zml_text():

    def List_text(self):
        list_a = [[1,2,3],[4,5,6],[7,8,9]]
        for i in range(len(list_a)):
            for j in range(len(list_a[i])):
                print(list_a[i][j],end=',')
        print()

class A:
    name = 'clash A name'
    age = 10
    def printClassName(self):
        print(self.name)
        print(self.age)
    


class B(A):   #B继承A就是B继承A中所有的A的属性和方法

    # name = 'B'

    def printClassName(self):
        self.name = 'B'   # B继承了A之后，A中已经拥有的变量名在B中只需要继承使用即可，B中的变量名尽量减少和A中变量名重复
        # print(self.name)
        print(super().name)  #super（）就是找父类·
        print("======super=======")
        super().printClassName()  #直接继承A中的方法
        print("=================")
        # print('B')

# 所谓继承就是指：继承者能够直接使用被继承中的除了私有变量之外的所有的变量和方法
# 在被继承者的基础上，继承者还可以扩展独属于他自己的变量和方法，继承者在定义他自己的变量时需要注意不要和被继承者中的变量名重复，避免在后期调用时产生歧义
# 举例说明：A是B的父类，B除了继承了A中的变量和方法外，还可以扩展B独有的变量和方法，但是B在定义自己的变量时要避免和A中的变量名重复，
# 以免在调用时无法确定所使用的具体是谁的变量
    

if __name__ == '__main__':

    # a_obj = A()
    # a_obj.printClassName()
    # a_obj_2 = A()
    # a_obj_2.name = "wangning"
    # a_obj_2.age = 18
    # a_obj_2.printClassName()

    b_obj = B()
    # b_obj.printClassName()
    # B.printClassName(b_obj)
    # A.printClassName(b_obj)
    # print("=====")

    A.printClassName(super(B, b_obj))  #super(B，b_obj）super（）就是求某个参数的父类，像本句中就是求B的父类，然后将b_obj强转为B的父类即A
    # print("======")
    # A.printClassName(b_obj)
