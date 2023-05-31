
from cryptography.fernet import Fernet

# key=Fernet.generate_key()
# fernet=Fernet(key)

# hhh="Hello World"

# enc_key=fernet(key).encrypt(hhh.encode())
# print(enc_key)
# dce_key=fernet(key).decrypt(enc_key)

# print(dce_key.decode())


##################################################
class PasswordManager():

    def _init_(self):
        self.key = None
        self.masterPassword = None

    def run(self):
        try:
            with open ("key.key","r") as f:
                self.key = f.read().encode()
            
            with open ("password.txt","r") as f:
                key = f.readlines()
                print(key)
                a = key[0]
                print(a)
                b = a.split(":")
                print(b)
                c = b[1]
                print(c)

                verify = Fernet(self.key).decrypt(c.encode())
                print(verify.decode())

                if(input("Enter Master Password: ") == verify.decode()):
                    return True
                else:
                    return False
                    


        except:
            key = Fernet.generate_key()

            self.masterPassword = input("Enter Master Password:")
            self.masterPassword = Fernet(key).encrypt(self.masterPassword.encode())
            print(self.masterPassword)
            with open ("key.key","w") as f:
                f.write(key.decode())

            with open ("password.txt","w") as f:
                f.write(f"master:{self.masterPassword.decode()}")


    def storePassword(self,site,password):
        enc_password = Fernet(self.key).encrypt(password.encode())
        with open ("password.txt","a") as f:
            f.write(f"\n{site}:{enc_password.decode()}")

    
    def ReadPassword(self):
        with open("password.txt","r") as g:
            print("-----------------------------")
            for i in g.readlines():
                j=i.split(":")
                dec_passw=Fernet(self.key).decrypt(j[1].encode()).decode()
                print(f"{j[0]}=>{dec_passw}")
            print("-------------------------------")

            


p = PasswordManager()
if p.run():
    while True:
        print("1. Read password")    
        print("2. Store password")
        op = input("Enter Choice: ")
        if op == "1":
            p.ReadPassword()
        elif op == "2":
            site = input("Site: ")
            password = input("Password: ")
            p.storePassword(site,password)

        else:
            print("LOL")
