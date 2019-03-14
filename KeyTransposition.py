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



    for i in range(column):
        temp=""
        pointer=i
        while (pointer<len(text)):
            temp+=text[pointer]
            pointer+=column

        cipherChunks.append(temp)

    cipherMessage=""
    print(order)
    for i in order:
        cipherMessage+=cipherChunks[i]

    return cipherMessage

def TranspositionDecipher(text,key): #perhaps more efficient
    order=Order(key)
    column=len(key)
    row=m.floor(len(text)/column)
    longCol=len(text)%column



    messageChunks=['']*column
    index=0
    for i in range(column):
        messageChunks[order[i]]=(text[index:index+row+int(order[i]<longCol)])
        index+=(row+int(order[i]<longCol))

    for i in messageChunks:
        print(i)

    finalMessage=""
    for j in range(row+1):
        for i in range(column):
            if j<row or i<longCol:

                finalMessage += messageChunks[i][j]
                print (finalMessage)
    return finalMessage



A=TranspositionCipher("hello how are you, my name is frank, nice to meet you","SHA67")
print(len(A))
print(A)
B=TranspositionDecipher(A,'SHA67')
print(B)