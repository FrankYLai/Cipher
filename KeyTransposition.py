import math as m
import random
import hashlib
import chardet

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

def ceasarCipher(text, key):

    newtext=""
    index=0

    for i in range(len(text)):
        newtext += chr(ord(text[i])+ord(key[index]))
        index+=1
        if index == len(key):
            index=0

    return newtext

def ceasarDecipher(text, key):
    newtext=""
    index=0

    for i in range(len(text)):
        newtext += chr(ord(text[i]) - ord(key[index]))
        index += 1
        if index == len(key):
            index = 0

    return newtext

# times=0
# check=True
# while (check):
#
#     keySize=random.randint(5,16)
#     key=""
#     for x in range(keySize):
#         key+= chr(random.randint(1,256))
#     textSize=random.randint(64,512)
#     text=""
#     for x in range(textSize):
#         text+= chr(random.randint(1,256))
#
#
#     A=TranspositionCipher(text,key)
#     B=TranspositionDecipher(A,key)
#
#     C=ceasarCipher(text,key)
#     D=ceasarDecipher(C,key)
#
#     times+=1
#     print (times)
#
#     if (text!=B):
#         check=False
#         print("text: ",text)
#         print("key: ",key)
#         print("times: ", times)
#
#     if (text!=D):
#         check=False
#         print("text: ",text)
#         print("key: ",key)
#         print("times: ", times)

# hashed=hashlib.sha256(input("put password in here: ").encode()).hexdigest()
# for i in range (5):
#     hashed=hashlib.sha256(hashed.encode()).hexdigest()
#     print(hashed[1])
#     print(len(hashed))

# rawdata = open('1984.txt', 'rb').read(2000)
# result = chardet.detect(rawdata)
# print (result)
# print (result['encoding'])

detector = chardet.UniversalDetector()
detector.reset()
with open("1984.txt", mode='rb') as f:
    for b in f:
        detector.feed(b)
        if detector.done: break
detector.close()
print( detector.result)

