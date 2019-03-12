import math as m


def Order(key):
    list=[]

    for i in range(len(key)):
        smaller=0
        for j in range(len(key)):
            if ord(key[i])>ord(key[j]):
                smaller += 1
        if smaller in list:
            smaller += 1
        list.append(smaller)

    return list


def TranspositionCipher(text,key):
    order=Order(key)
    column=len(key)
    row=m.ceil(len(text)/len(key))
    cipherChunks=[]

    print(order)
    for i in range(row):
        temp=""
        pointer=i
        while (pointer<len(text)):
            temp+=text[pointer]
            pointer+=column

        cipherChunks.append(temp)

    cipherMessage=""
    for i in order:
        cipherMessage+=cipherChunks[i]

    return cipherMessage


print(TranspositionCipher("what is your name","abcd"))