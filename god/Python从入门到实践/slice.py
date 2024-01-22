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
