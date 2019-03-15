from enum import Enum
import math as m
import hashlib
import random

class status(Enum):
    IDLE = 1
    CIPHER = 2
    DECIPHER = 3

class CipherMachine:

    mode=status.IDLE
    password=""
    hashed=""

    def __init__(self):#initializer
        self.mode = status.IDLE

    def __del__(self):
        self.infile.close()

    def changeMode(self, status):
        self.mode=status

    def Open(self,fileDir):
        self.fileDir=fileDir
        try:
            self.infile=open(self.fileDir, "r")
            if fileDir.endswith(".crypt"):
                self.mode=status.DECIPHER
                print("run1")
            else:
                self.mode=status.CIPHER
                print('run2')
            return True
        except FileNotFoundError:
            return False

    def password(self, key):
        self.password=key
        self.hashed=hashlib.sha256(self.password.encode()).hexdigest()

        if self.mode==status.DECIPHER:
            if self.infile.read(len(self.hashed))!=self.hashed:
                self.infile.close()
                self.infile.open(self.fileDir,'r')
                return False

        return True



    def Order(self,key):
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

    def TranspositionCipher(self, text, key):
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

    def TranspositionDecipher(self,text, key):
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

    def ceasarCipher(self, text, key):

        newtext = ""
        index = 0

        for i in range(len(text)):
            newtext += chr(ord(text[i]) + ord(key[index]))
            index += 1
            if index == len(key):
                index = 0

        return newtext

    def ceasarDecipher(self, text, key):
        newtext = ""
        index = 0

        for i in range(len(text)):
            newtext += chr(ord(text[i]) - ord(key[index]))
            index += 1
            if index == len(key):
                index = 0

        return newtext

    def isEOF(self,block,size):
        pass

    def Encrypt(self):
        name="encryption/"
        for i in range(10):
            name+=chr(random.randint(ord('a'),ord('z')))
        name+=".crypt"

        with open(name,"w") as outfile:
            outfile.write(self.hashed)#make sure to delete once second stage is implemented
            outfile.write(self.fileDir+'|')
            index=0
            block=self.infile.read(ord(self.hashed[index]))
            while len(block)==ord(self.hashed[index]):
                outfile.write(self.TranspositionCipher(block,self.password))
                index+=1
                if index==len(self.hashed):
                    index-=len(self.hashed)
                block = self.infile.read(ord(self.hashed[index]))



    def Decrypt(self):
        name=""
        readNext=self.infile.read(1)
        while readNext!="|":
            name+=readNext
            readNext=self.infile.read(1)

        with open(name,'w') as outfile:
            index=0
            block = self.infile.read(ord(self.hashed[index]))
            while len(block) == ord(self.hashed[index]):
                outfile.write(self.TranspositionDecipher(block, self.password))
                index += 1
                if index == len(self.hashed):
                    index -= len(self.hashed)
                block = self.infile.read(ord(self.hashed[index]))




    def start(self):

        print(self.password, " ", self.fileDir)
        if self.mode==status.CIPHER:
             self.Encrypt()
        elif self.mode==status.DECIPHER:
            self.Decrypt()
        else:
            print("error determining mode please include a file you would like to encrypt/decrypt")









