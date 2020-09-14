# coding = utf-8
from collections import Counter  #统计列表出现次数最多的元素
import numpy as np

print("输入序列： ")
inputstr = input()
print  (inputstr + "\n")

res = Counter(inputstr) #统计输入的每个字符的个数,res是一个字典类型
print (str(res))
# print(res)
#sortlist = sorted(res.iteritems(), lambda x, y : cmp(x[1], y[1]), reverse = True)
#print sortlist

M = len(res)
#print (M)
N = 5
A = np.zeros((M,5),dtype=object)  #生成M行5列全0矩阵

#A = [[0 for i in range(N)] for j in range(M)]

reskeys = list(res.keys())      #取字典res的键,按输入符号的先后顺序排列
# print(reskeys)
resvalue = list(res.values())   #取字典res的值
totalsum = sum(resvalue)        #输入一共有几个字符

# Creating Table

A[M-1][3] = 0
for i in range(M):
   A[i][0] = reskeys[i]      #第一列是res的键
   A[i][1] = resvalue[i]     #第二列是res的值
   A[i][2] = ((resvalue[i]*1.0)/totalsum)    #第三列是每个字符出现的概率
i=0
A[M-1][4] = A[M-1][2]
while i < M-1:                    #倒数两列是每个符号的区间范围，与输入符号的顺序相反
   A[M-i-2][4] = A[M-i-1][4] + A[M-i-2][2]
   A[M-i-2][3] = A[M-i-1][4]
   i+=1
print (A)

# Encoding

print("\n------- ENCODING -------\n" )
strlist = list(inputstr)
LEnco = []
UEnco = []
LEnco.append(0)
UEnco.append(1)

for i in range(len(strlist)):
    result = np.where(A == reskeys[reskeys.index(strlist[i])])           #满足条件返回数组下标(0,0),(1,0)
    addtollist = (LEnco[i] + (UEnco[i] - LEnco[i])*float(A[result[0],3]))
    addtoulist = (LEnco[i] + (UEnco[i] - LEnco[i])*float(A[result[0],4]))

    LEnco.append(addtollist)
    UEnco.append(addtoulist)

    tag = (LEnco[-1] + UEnco[-1])/2.0           #最后取区间的中点输出

LEnco.insert(0, " Lower Range")
UEnco.insert(0, "Upper Range")
print(np.transpose(np.array(([LEnco],[UEnco]),dtype=object)))  #np.transpose()矩阵转置
print("\nThe Tag is \n ")
print(tag)

# Decoding

print("\n------- DECODING -------\n" )
ltag = 0
utag = 1
decodedSeq = []
for i in range(len(inputstr)):
    numDeco = ((tag - ltag)*1.0)/(utag - ltag)    #计算tag所占整个区间的比例
    for i in range(M):
        if (float(A[i,3]) < numDeco < float(A[i,4])):   #判断是否在某个符号区间范围内

            decodedSeq.append(str(A[i,0]))
            ltag = float(A[i,3])
            utag = float(A[i,4])
            tag = numDeco

print("The decoded Sequence is \n ")
print("".join(decodedSeq))