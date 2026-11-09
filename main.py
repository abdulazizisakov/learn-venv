import sys
from termcolor import colored
import bcrypt

class Auth:
    def __init__(self):
        # Bir nechta foydalanuvchini saqlash uchun lug'at (dictionary): 
        # {username: {"password": hash, "balance": 0.0}}
        self.users = {}
        # Hozirda tizimga kirgan foydalanuvchi
        self.current_user = None

    def __call__(self):
        while True:
            self.echo_auth()
            try:
                choice = int(input("choice = "))
            except ValueError:
                print(colored("Faqat raqam kiriting!", "red"))
                continue

            if choice == 1:
                self.register()
            elif choice == 2:
                self.login()
            else:
                print(colored("Noto'g'ri tanlov!", "red"))

    def echo_auth(self):
        text = """
        1. Register
        2. Login
        """
        print(text)

    def register(self):
        username = input("username = ")
        password = input("password = ")

        if username in self.users:
            print(colored("Bu username allaqachon mavjud", color="red"))
            return

        hashed_password = self.hash_password(password)
        # Yangi foydalanuvchi yaratamiz va boshlang'ich balansini 0.0 qilib qo'yamiz
        self.users[username] = {
            "password": hashed_password,
            "balance": 0.0
        }
        print(colored("Siz muvaffaqiyatli ro'yxatdan o'tdingiz!", "green"))

    def login(self):
        username = input("username = ")
        password = input("password = ")

        if username in self.users and self.check_password(password, self.users[username]["password"]):
            print(colored("Siz muvaffaqiyatli tizimga kirdingiz!", 'green'))
            self.current_user = username
            self.bankshot()            
            return

        print(colored("Username yoki parol noto'g'ri", 'red'))

    def hash_password(self, password):
        s = bcrypt.gensalt()
        hashed = bcrypt.hashpw(password.encode('utf-8'), s)
        return hashed

    def check_password(self, password, hashed_password):
        return bcrypt.checkpw(password.encode('utf-8'), hashed_password)

    def echo_menu(self):
        text = f"""
        --- Foydalanuvchi: {self.current_user} ---
        1. Balansni ko'rish
        2. Pul qo'shish
        3. Pul yechish
        4. Chiqish (Logout)
        0. Dasturdan chiqish (Exit)
        """
        print(text)

    def bankshot(self):
        while True:
            self.echo_menu()
            try:
                choice = int(input("choice = "))
            except ValueError:
                print(colored("Faqat raqam kiriting!", "red"))
                continue

            if choice == 1:
                self.view_balance()
            elif choice == 2:
                self.deposit()
            elif choice == 3:
                self.withdraw()
            elif choice == 4:
                print(colored("Hisobdan chiqildi.", "yellow"))
                self.current_user = None
                break  # Bank menyusidan chiqib, asosiy Auth menyusiga qaytadi
            elif choice == 5:
                sys.exit(colored("Dastur yakunlandi. Xayr!", "cyan"))
            else:
                print(colored("Noto'g'ri tanlov!", "red"))

    def view_balance(self):
        balance = self.users[self.current_user]["balance"]
        print(colored(f"Sizning balansingiz: {balance:,.2f} so'm", "blue"))

    def deposit(self):
        try:
            amount = float(input("Qo'shmoqchi bo'lgan summangizni kiriting: "))
            if amount <= 0:
                print(colored("Summa 0 dan katta bo'lishi kerak!", "red"))
                return
            
            self.users[self.current_user]["balance"] += amount
            print(colored(f"Muvaffaqiyatli! Hisobingizga {amount:,.2f} so'm qo'shildi.", "green"))
            self.view_balance()
        except ValueError:
            print(colored("Iltimos, to'g'ri raqam kiriting!", "red"))

    def withdraw(self):
        try:
            amount = float(input("Yechib olmoqchi bo'lgan summangizni kiriting: "))
            if amount <= 0:
                print(colored("Summa 0 dan katta bo'lishi kerak!", "red"))
                return
            
            current_balance = self.users[self.current_user]["balance"]
            if amount > current_balance:
                print(colored("Hisobingizda yetarli mablag' mavjud emas!", "red"))
                return

            self.users[self.current_user]["balance"] -= amount
            print(colored(f"Muvaffaqiyatli! Hisobingizdan {amount:,.2f} so'm yechildi.", "green"))
            self.view_balance()
        except ValueError:
            print(colored("Iltimos, to'g'ri raqam kiriting!", "red"))

if __name__ == "__main__":
    auth = Auth()
    auth()