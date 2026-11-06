import sys

from termcolor import colored
import bcrypt



class Auth:
    def __init__(self):
        self.username = None
        self.password = None

        
    def __call__(self):

        while True:
            self.echo_auth()

            choice = int(input("choice = "))

            if choice == 1:
                self.register()

            elif choice == 2:
                self.login()

    def echo_auth(self):
        text = """
        1.Register
        2.Login
        """

        print(text)

    def register(self):
        username = input("username = ")
        password = input("password = ")

        if self.username == username:
            print(colored("This username already exists",color="red"))
            return

        self.username = username
        self.password = self.hash_password(password)
        print(colored("Siz registratsiya qilindingiz","green"))

    def login(self):
        username = input("username = ")
        password = input("password = ")

        if self.username == username and self.check_password(password):
            print(colored("Siz login qilindizngiz",'green'))

            self.bankshot()            
            return

        print(colored("Username yoki parol noto'g'ri",'red'))

    def hash_password(self,password):
        s = bcrypt.gensalt()
        hash = bcrypt.hashpw(password.encode('utf-8'), s)

        return hash

    def check_password(self,password):
        return bcrypt.checkpw(password.encode('utf-8'),self.password)

    def echo_menu(self):
        text = """
        1.Balansni ko'rish
        2.Pul Qo'shish
        3.Pul yechish
        4.Exit
        """

        print(text)

    def bankshot(self):

        while True:
            self.echo_menu()

            choice = int(input("choice = "))

            if choice == 1:
                pass
            elif choice == 2:
                pass
            elif choice == 3:
                pass
            elif choice == 4:
                sys.exit("Dastur yakunlandi")

            



if __name__ == "__main__":
    auth = Auth()

    auth()