from enum import Enum
import math as m
import hashlib
import random
import chardet
import os

class status(Enum):
    IDLE = 1
    CIPHER = 2
    DECIPHER = 3

class CipherMachine:

    def __init__(self):  #initializer
        self.mode = status.IDLE
        self.password = ""
        self.hashed = ""
        self.fileDir = ""
        self.encoding = ""
        self.fileName = ""
        self.filePath = ""
        self.fileEncoding = ""

    def changeMode(self, status):
        self.mode=status


    def Open(self,fileDir):
        self.fileDir = fileDir
        list=fileDir.split("\\")
        self.fileName = list[len(list)-1]
        del list[-1]
        self.filePath = '\\'.join(list)

        try:
            detector = chardet.UniversalDetector()
            detector.reset()
            with open(self.fileDir, mode='rb') as f:
                for b in f:
                    detector.feed(b)
                    if detector.done: break
            detector.close()
            self.encoding = detector.result['encoding']

            if fileDir.endswith(".crypt"):
                self.mode = status.DECIPHER
            else:
                self.mode = status.CIPHER
            try:
                with open(self.fileDir,"r", encoding=self.encoding) as read_test:
                    read_test.read(1000)
            except UnicodeDecodeError:
                print("this type of file cannot be encrypted due to decoding error. try a different type of file")
                return False
            return True

        except FileNotFoundError:
            print("file not found, please make sure spelling is correct")
            return False

    def save_password(self, key):
        self.password = key
        self.hashed = hashlib.sha256(self.password.encode()).hexdigest()

        if self.mode == status.DECIPHER:
            with open(self.fileDir, 'r', encoding=self.encoding) as infile:
                if infile.read(len(self.hashed)) != self.hashed:
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


    def Encrypt(self):

        #stage 1 encode
        with open(self.fileDir,'r',encoding=self.encoding) as infile:
            with open("temp.crypt","w",encoding="UTF-8") as outfile:
                outfile.write(self.fileDir+'|')
                outfile.write(self.encoding + "|")
                index=0
                block=infile.read(ord(self.hashed[index]))
                while len(block)!=0:
                    outfile.write(self.ceasarCipher(self.TranspositionCipher(block,self.password),self.password))  #completes transposition before ceasar

                    index += 1
                    if index == len(self.hashed):
                        index -= len(self.hashed)
                    block = infile.read(ord(self.hashed[index]))

        os.remove(self.fileDir)

        # stage 2 encode
        name2 = ""
        if self.filePath!="":
            name2 += self.filePath + "\\"
        for i in range(10):
            name2 += chr(random.randint(ord('a'), ord('z')))
        name2 += ".crypt"

        with open("temp.crypt", 'r', encoding="UTF-8") as fin:
            with open(name2, 'w', encoding="UTF-8") as fout:
                fout.write(self.hashed)
                index = 0
                block = fin.read(ord(self.password[index]))

                while len(block) != 0:
                    fout.write(self.TranspositionCipher(block, self.password))
                    index += 1
                    if index == len(self.password):
                        index -= len(self.password)

                    block = fin.read(ord(self.password[index]))
        os.remove("temp.crypt")



    def Decrypt(self):
       # second stage decrypt
        with open(self.fileDir,'r',encoding="UTF-8") as fin:
            fin.read(len(self.hashed))
            with open('temp.crypt','w',encoding="UTF-8") as fout:
                index = 0
                block=fin.read(ord(self.password[index]))

                while len(block)!=0:
                    fout.write(self.TranspositionDecipher(block, self.password))
                    index += 1
                    if index == len(self.password):
                        index -= len(self.password)

                    block = fin.read(ord(self.password[index]))

        os.remove(self.fileDir)

        #first stage decrypt
        name=""
        if self.filePath != "":
            name = self.filePath + "\\"
        with open("temp.crypt",'r',encoding="UTF-8") as infile:
            readNext = infile.read(1)
            while readNext != "|":
                name += readNext
                readNext = infile.read(1)
            readNext = infile.read(1)
            while readNext != "|":
                self.fileEncoding += readNext
                readNext = infile.read(1)

            with open(name, 'w', encoding=self.fileEncoding) as outfile:
                index=0
                block = infile.read(ord(self.hashed[index]))
                while len(block) !=0:
                    outfile.write(self.TranspositionDecipher(self.ceasarDecipher(block, self.password),self.password))#completes ceasar before transposition
                    index += 1
                    if index == len(self.hashed):
                        index -= len(self.hashed)
                    block = infile.read(ord(self.hashed[index]))

        os.remove("temp.crypt")




    def start(self):

        print("your password is: ", self.password, " ", self.fileDir, " has been encrypted")
        if self.mode==status.CIPHER:
             self.Encrypt()
        elif self.mode==status.DECIPHER:
            self.Decrypt()
        else:
            print("error determining mode please include a file you would like to encrypt/decrypt")









