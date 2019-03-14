from enum import Enum
import math as m
import random

class status(Enum):
    IDLE = 1
    CIPHER = 2
    DECIPHER = 3

class CipherMachine:

    def __init__(self,InputKey,status):
        self.key = InputKey
        self.mode = status

    def __del__(self):
        self.infile.close()


    def changeMode(self, status):
        self.mode=status

    def Open(self,fileDir):
        self.fileDir=fileDir
        self.infile=open(fileDir, "r")
        if fileDir.endswith(".crypt"):
            self.mode=status.DECIPHER
        else
            self.mode=status.CIPHER

    def Order(key):
        list = []

        for i in range(len(key)):
            smaller = 0
            for j in range(len(key)):
                if ord(key[i]) > ord(key[j]):
                    smaller += 1
            while smaller in list:
                smaller += 1
            list.append(smaller)

        return list

    def TranspositionCipher(text, key):
        order = self.Order(key)
        column = len(key)
        row = m.ceil(len(text) / len(key))
        cipherChunks = []

        for i in range(column):
            temp = ""
            pointer = i
            while (pointer < len(text)):
                temp += text[pointer]
                pointer += column

            cipherChunks.append(temp)

        cipherMessage = ""
        # print(order)
        for i in order:
            cipherMessage += cipherChunks[i]

        return cipherMessage

    def TranspositionDecipher(text, key):
        order = self.Order(key)
        column = len(key)
        row = m.floor(len(text) / column)
        longCol = len(text) % column

        messageChunks = [''] * column
        index = 0
        for i in range(column):
            messageChunks[order[i]] = (text[index:index + row + int(order[i] < longCol)])
            index += (row + int(order[i] < longCol))
        #
        # for i in messageChunks:
        #     print(i)

        finalMessage = ""
        for j in range(row + 1):
            for i in range(column):
                if j < row or i < longCol:
                    try:
                        finalMessage += messageChunks[i][j]
                        # print (finalMessage)
                    except IndexError:
                        print("the message is: ", messageChunks[i])
                        print("The Value of I is: ", i, " The value of J is: ", j)
                        print("the row size(J) is: ", row)
                        print("the key size(I) is: ", len(key))

        return finalMessage

    def ceasarCipher(text, key):

        newtext = ""
        index = 0

        for i in range(len(text)):
            newtext += chr(ord(text[i]) + ord(key[index]))
            index += 1
            if index == len(key):
                index = 0

        return newtext

    def ceasarDecipher(text, key):
        newtext = ""
        index = 0

        for i in range(len(text)):
            newtext += chr(ord(text[i]) - ord(key[index]))
            index += 1
            if index == len(key):
                index = 0

        return newtext
    
    def Encrypt(self):
        pass

    def Decrypt(self):
        pass



    def crypt(self):
        if self.mode==status.CIPHER:
             self.Encrypt()
        if self.mode==status.DECIPHER:
            self.Decrypt()

        else:
            print("please include a file you would like to encrypt/decrypt")









