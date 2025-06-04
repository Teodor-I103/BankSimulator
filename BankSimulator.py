import getpass

#Constants for allowed age range and filenames
MAXIMUM_AGE = 18
MINIMUM_AGE = 13
USER_FILE = "users.txt"
TRANSACTION_FILE = "transactions.txt"
LINE = "==================================="


#Main menu for login, sign up, or exit
def Login_Selection():
    while True:
        try:
            user_choice = int(input(f"{LINE}\n1. Login\n2. Sign Up\n3. Exit\n{LINE}\nEnter an option: "))
            if user_choice == 1:
                Login() #Proceed to login
            elif user_choice == 2:
                Valid_Age() #Procceed to age validation
            elif user_choice == 3:
                print("Goodbye!")
                quit() #Exit the program
            else:
                print("Please enter 1, 2 or 3")
        except ValueError:
            print("Please enter a number")

#Load all users from the file into a dictionary
def Load_Users():
    users = {}
    try:
        with open(USER_FILE, "r") as f:
            for line in f:
                username, password, balance = line.strip().split(",")
                users[username] = {"password": password, "balance": float(balance)}
    except FileNotFoundError:
        pass  #File will be created later if it doesn't exist
    return users

#Save the user dictionary back to the file
def save_users(users):
    with open(USER_FILE, "w") as f:
        for username, password in users.items():
            f.write(f"{username},{password['password']},{password['balance']}\n")

#Function to validate user's age
def Valid_Age():
    while True:
        try:
            user_age = int(input("Please enter your age: "))
            if user_age > MAXIMUM_AGE:
                print("You are too old to create an account.\nGoodbye!")
                break
            elif 0 < user_age < MINIMUM_AGE:
                print("You are too young to create an account.\nGoodbye!")
                break
            elif user_age <= 0:
                print("Enter an integer above 0")
            else:
                Sign_Up() #Proceed to Sign up menu
        except ValueError:
            print("Please enter an integer")

#Function to handle user sign up
def Sign_Up():
    users = Load_Users()
    while True:
        username = input("Please enter a username, or 'exit' to return to menu: ").strip()
        lowered_username = username.lower()
        if lowered_username == "exit":
            Login_Selection() #Returns the user to login or sign up menu
        if username == "":
            print("Please enter a valid username")
        elif username in users:
            print("Username already exists. Try another.")
        else:
            break
    while True:
        password = getpass.getpass("Please enter a password, or 'exit' to return to menu: ")
        lowered_password = password.lower()
        if lowered_password == "exit":
            Login_Selection() #Returns the user to login or sign up menu
        if len(password) < 6: #Check password length
            print("Password must be at least 6 characters long.")
        else:
            break
    #Save the new user with starting balance of $0.00
    users[username] = {"password": password, "balance": 0.0}
    save_users(users)
    print("Account created successfully!\n")
    Login_Selection()

#Handles logging in an existing user
def Login():
    users = Load_Users()
    username = input("Please enter a username, or 'exit' to return to menu: ").strip()
    lowered_username = username.lower()
    if lowered_username == "exit":
        Login_Selection() #Returns the user to login or sign up menu
    while username not in users: #Check if username exists
        print("Please enter a valid username")
        username = input("Enter your username: ").strip()
    while True: #Check for password
        password = getpass.getpass("Please enter a password, or 'exit' to return to menu: ")
        lowered_password = password.lower()
        if lowered_password == "exit":
            Login_Selection() #Returns the user to login or sign up menu
        if password == "":
            print("You must enter a password")
        else:
            break
    while users[username]["password"] != password: #Validate password
        print("Incorrect password.")
        password = input("Please enter your password: ")
    print(f"{LINE}\nWelcome {username}!")
    Banking_Menu(username, users)

#Main banking menu for transactions
def Banking_Menu(username, users):
    print(f"Your current balance is: ${users[username]['balance']}")
    while True:
        try:
            banking_choice = int(input(f"1. Withdraw\n2. Deposit\n3. Display Transanctions\n4. Logout\n{LINE}\nPlease enter a choice: "))
            if banking_choice == 1:
                Withdraw(username, users)
            elif banking_choice == 2:
                Deposit(username, users)
            elif banking_choice == 3:
                Transanction_History(username, users)
            elif banking_choice == 4:
                print("You have logged out of your account")
                Login_Selection()
            else:
                print("Enter 1, 2, 3, or 4")
        except ValueError:
            print("Please enter a number")

#Append a transaction to the transaction log
def Log_Transaction(username, message):
    with open(TRANSACTION_FILE, "a") as f:
        f.write(f"{username}: {message}\n")

#Withdraw money from user's balance
def Withdraw(username, users):
    while True:
        withdraw_amount = float(input("Please enter how much you would like to withdraw: $"))
        if withdraw_amount <= 0:
            print("Please enter an amount greater than 0")
        else:
            if withdraw_amount > users[username]["balance"]: #Check if withdrawal amount exceeds balance
                print("Not enough balance available.")
            else: #Proceed with withdrawal
                users[username]["balance"] -= withdraw_amount
                print(f"Withdrawal successful!\nYou have withdrawn ${withdraw_amount}\n{LINE}")
                save_users(users)
                Log_Transaction(username, f"Withdrawed ${withdraw_amount}")
                Banking_Menu(username, users) #Returns the user to banking menu

#Deposit money to user's balance
def Deposit(username, users):
    while True:
        deposit_amount = float(input("Please enter how much you would like to deposit: $"))
        if deposit_amount <= 0:
            print("Please enter an amount greater than 0")
        else:
            break
    users[username]["balance"] += deposit_amount
    print(f"Deposit successful!\nYou have deposited ${deposit_amount}\n{LINE}")
    save_users(users)
    Log_Transaction(username, f"Deposited ${deposit_amount}")
    Banking_Menu(username, users) #Returns the user to banking menu

#Show transaction history for all users (optionally could be filtered per user)
def Transanction_History(username, users):
    try:
        with open(TRANSACTION_FILE, "r") as f:
            for line in f:
                print(line)
    except FileNotFoundError:
        print("No transactions found.")
    print(LINE)
    Banking_Menu(username, users) #Returns the user to banking menu

#Program starts here
Valid_Age()