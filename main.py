import CipherMachine

def main():
    while True:
        cipher = CipherMachine.CipherMachine()


        while not cipher.Open(input("input file directory: ")):
            pass
        while not cipher.save_password(input("input password(your password must be correct to decrypt)")):
            pass
        cipher.start()


if __name__ == "__main__":
    main()
