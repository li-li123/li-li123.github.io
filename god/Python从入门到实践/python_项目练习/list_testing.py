
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

