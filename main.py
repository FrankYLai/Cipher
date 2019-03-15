import CipherMachine

def main():
    while True:
        cipher= CipherMachine.CipherMachine()

        dir=input("input file directory: ")
        while not cipher.Open(dir):
            dir = input("error file directory: ")



        while not cipher.password(input("input password(your password must be correct to decrypt)")):
            pass

        cipher.start()




if __name__=="__main__":
    main()