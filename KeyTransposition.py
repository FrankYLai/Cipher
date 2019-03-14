import math as m
import random

def Order(key):
    list=[]

    for i in range(len(key)):
        smaller=0
        for j in range(len(key)):
            if ord(key[i])>ord(key[j]):
                smaller += 1
        while smaller in list:
            smaller += 1
        list.append(smaller)

    return list


def TranspositionCipher(text,key):
    order=Order(key)
    column=len(key)
    row=m.ceil(len(text)/len(key))
    cipherChunks=[]



    for i in range(column):
        temp=""
        pointer=i
        while (pointer<len(text)):
            temp+=text[pointer]
            pointer+=column

        cipherChunks.append(temp)

    cipherMessage=""
    # print(order)
    for i in order:
        cipherMessage+=cipherChunks[i]

    return cipherMessage

def TranspositionDecipher(text,key):
    order=Order(key)
    column=len(key)
    row=m.floor(len(text)/column)
    longCol=len(text)%column

    messageChunks=['']*column
    index=0
    for i in range(column):
        messageChunks[order[i]]=(text[index:index+row+int(order[i]<longCol)])
        index+=(row+int(order[i]<longCol))
    #
    # for i in messageChunks:
    #     print(i)

    finalMessage=""
    for j in range(row+1):
        for i in range(column):
            if j<row or i<longCol:
                try:
                    finalMessage += messageChunks[i][j]
                    # print (finalMessage)
                except IndexError:
                    print("the message is: ",messageChunks[i])
                    print("The Value of I is: ", i," The value of J is: ",j)
                    print("the row size(J) is: ", row)
                    print("the key size(I) is: ",len(key))


    return finalMessage





times=0
check=True
while (check):

    keySize=random.randint(5,16)
    key=""
    for x in range(keySize):
        key+= chr(random.randint(1,256))
    textSize=random.randint(64,512)
    text=""
    for x in range(textSize):
        text+= chr(random.randint(1,256))


    A=TranspositionCipher(text,key)
    B=TranspositionDecipher(A,key)

    times+=1
    print (times)

    if (text!=B):
        check=False
        print("text: ",text)
        print("key: ",key)
        print("times: ", times)


# while True:
#     keySize=random.randint(5,16)
#     key=""
#     for x in range(keySize):
#         key+= chr(random.randint(1,256))
#
#     print(Order(key))
#     if(max(Order(key))!=len(Order(key))-1):
#         print("fail")
#         break


# A=TranspositionCipher("1234567890","21")
    # B=TranspositionDecipher(A,"21")