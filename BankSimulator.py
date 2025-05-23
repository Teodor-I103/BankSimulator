MAXIMUM_AGE = 18
MINIMUM_AGE = 13
USER_FILE = "users.txt"
TRANSACTION_FILE = "transactions.txt"
placeholder = "==================================="

def Valid_Age():
    while True:
        try:
            user_age = int(input("Please enter your age: "))
            if user_age > MAXIMUM_AGE:
                print("You are too old to use this program.\nGoodbye!")
                break
            elif 0 < user_age < MINIMUM_AGE:
                print("You are too young to use this program.\nGoodbye!")
                break
            elif user_age <= 0:
                print("Enter an integer above 0")
            else:
                Login_Selection()
        except ValueError:
            print("Please enter an integer")

def Login_Selection():
    while True:
        try:
            user_choice = int(input(f"{placeholder}\n1. Login\n2. Sign Up\n3. Exit\n{placeholder}\nEnter an option: "))
            if user_choice == 1:
                Login()
            elif user_choice == 2:
                Sign_Up()
            elif user_choice == 3:
                print("Goodbye!")
                quit()
            else:
                print("Please enter 1, 2 or 3")
        except ValueError:
            print("Please enter a number")
def Login():
    users = Load_Users()
    username = input("Enter your username: ").strip()
    while username not in users:
        print("Please enter a valid username")
        username = input("Enter your username: ").strip()
    password = input("Please enter your password: ")
    while users[username]["password"] != password:
        print("Incorrect password.")
        password = input("Please enter your password: ")
    print(f"{placeholder}\nWelcome {username}!")
    Banking_Menu(username, users)

def Banking_Menu(username, users):
    print(f"Your current balance is: ${users[username]["balance"]}")
    while True:
        try:
            banking_choice = int(input(f"1. Withdraw\n2. Deposit\n3. Display Transanctions\n4. Logout\n{placeholder}\nPlease enter a choice: "))
            if banking_choice == 1:
                Withdraw()
            elif banking_choice == 2:
                Deposit()
            elif banking_choice == 3:
                Transanction_History()
            elif banking_choice == 4:
                print("You have logged out of your account")
                Login_Selection()
            else:
                print("Enter 1, 2, 3, or 4")
        except ValueError:
            print("Please enter a number")


    
def Load_Users():
    users = {}
    try:
        with open(USER_FILE, "r") as f:
            for line in f:
                username, password, balance = line.strip().split(",")
                users[username] = {"password": password, "balance": float(balance)}
    except FileNotFoundError:
        pass
    return users

def save_users(users):
    with open(USER_FILE, "w") as f:
        for username, password in users.items():
            f.write(f"{username},{password["password"]},{password["balance"]}\n")

def Sign_Up():
    users = Load_Users()
    while True:
        username = input("Please enter a username: ").strip()
        if username == "":
            print("Please enter a valid username")
        elif username in users:
            print("Username already exists. Try another.")
        else:
            break
    while True:
        user_password = input("Please enter a password: ")
        if user_password == "":
            print("Please enter a valid password")
        else:
            break
    users[username] = {"password": user_password, "balance": 0.0}
    save_users(users)
    print("Account created successfully!\n")
    Login_Selection()
    
Valid_Age()