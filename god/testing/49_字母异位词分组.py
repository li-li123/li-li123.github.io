class Solution:
    def groupAnagrams(self, strs):
        
        letters = [chr(x) for x in range(97,123)]

        if len(strs) == 0:
            return []
        mark_dic ={}
        for element in strs:
            mark = ''
            for x in letters:
                if x in element:
                    mark = mark + x +str(element.count(x))
                else:
                    continue
            if mark not in mark_dic:
                mark_dic[mark] = [element]
            else:
                mark_dic[mark].append(element)
        result = []
        for key,value in mark_dic.items():
            result.append(value)
        return result



if '__main__' == __name__:
    strs = ["eat", "tea", "taan", "ate", "nat", "bat"]
    A = Solution()
    print(A.groupAnagrams(strs))