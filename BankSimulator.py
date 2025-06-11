import getpass
from easygui import *

#Constants for allowed age range and filenames
MAXIMUM_AGE = 18
MINIMUM_AGE = 13
USER_FILE = "users.txt"
TRANSACTION_FILE = "transactions.txt"
MAX_TRIES = 4
BANKING_CHOICES = ["Withdraw", "Deposit", "Display Transactions", "Logout"]

#Main menu for login, sign up, or exit
def Login_Selection():
    while True:
        user_choice = buttonbox("Welcome to my bank simulator!\nChoose an option:", "Bank Menu", ["Login", "Sign Up", "Exit"])
        if user_choice == "Login":
            Login()
        elif user_choice == "Sign Up":
            Valid_Age()
        elif user_choice == "Exit":
            exit_confirmation = buttonbox("Are you sure you wish to exit?", "Bank Simulator", ["Yes", "No"])
            if exit_confirmation == "Yes":
                msgbox("Goodbye!")
                quit()

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
        user_age = enterbox("Please enter your age: ", "Bank Simulator")
        if user_age is None:
            Login_Selection() #Returns the user to login or sign up menu
        try:
            user_age = int(user_age)
            if user_age <= 0:
                msgbox("Please enter an integer above 0")
            elif user_age > MAXIMUM_AGE or user_age < MINIMUM_AGE:
                msgbox("Users must be within ages 13 - 18 to create an account")
            else:
                Sign_Up() #Proceed to sign up
        except ValueError:
            msgbox("Please enter an integer")

#Function to handle user sign up
def Sign_Up():
    users = Load_Users()
    while True:
        username = enterbox("Please enter a username: ", "Bank Simulator")
        if username is None:
            Login_Selection() #Returns the user to login or sign up menu
        elif username == "":
            msgbox("Please enter a valid username")
        elif username in users:
            msgbox("Username already exists. Try another.")
        else:
            break
    username = username.strip() #Removes any spaces after the username
    while True:
        password = passwordbox("Please enter a password: ", "Bank Simulator")
        if password is None:
            Login_Selection() #Returns the user to login or sign up menu
        elif len(password) < 6: #Check password length
            msgbox("Password must be at least 6 characters long.")
        else:
            break
    #Save the new user with starting balance of $0.00
    users[username] = {"password": password, "balance": 0.0}
    save_users(users)
    msgbox("Account created successfully!")
    Login_Selection()

#Handles logging in an existing user
def Login():
    users = Load_Users()
    username = enterbox("Please enter a username: ", "Bank Simulator")
    if username is None:
        Login_Selection() #Returns the user to login or sign up menu
    username = username.strip() #Removes any spaces after the username
    while username not in users: #Check if username exists
        msgbox("Please enter a valid username")
        username = enterbox("Enter your username: ")
        if username is None:
            Login_Selection() #Returns the user to login or sign up menu
        username = username.strip() #Removes any spaces after the username
    password_tries = 1
    password = passwordbox("Please enter a password: ", "Bank Simulator")
    if password is None:
        Login_Selection() #Returns the user to login or sign up menu
    while users[username]["password"] != password:
        if password_tries >= MAX_TRIES:
            print("Too many incorrect attempts.")
            Login_Selection() #Retunrs the user to login or sign up menu
        print(f"Incorrect password, you have {MAX_TRIES - password_tries} tries left.")
        password = passwordbox("Please enter a password: ", "Bank Simulator")
        password_tries += 1
        if password is None:
            Login_Selection() #Returns the user to login or sign up menu
    msgbox(f"Welcome {username}!")
    Banking_Menu(username, users) #Proceed to banking menu

#Main banking menu for transactions
def Banking_Menu(username, users):
    print(f"Your current balance is: ${users[username]['balance']}")
    while True:
        banking_choice = buttonbox(f"Your current balance is: ${users[username]['balance']:.2f}", "Banking Menu", BANKING_CHOICES)
        if banking_choice == "Withdraw":
            Withdraw(username, users)
        elif banking_choice == "Deposit":
            Deposit(username, users)
        elif banking_choice == "Display Transactions":
            Transaction_History(username, users)
        elif banking_choice == "Logout":
            exit_confirmation = buttonbox("Are you sure you wish to logout", "Bank Simulator", ["Yes", "No"])
            if exit_confirmation == "Yes":
                msgbox("You have logged out of your account")
                Login_Selection()

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
                Log_Transaction(username, f"Withdrew ${withdraw_amount}")
                print(f"Your current balance is: ${users[username]['balance']}")
                break #Returns the user to banking menu

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
    print(f"Your current balance is: ${users[username]['balance']}")

#Show transaction history for all users (optionally could be filtered per user)
def Transaction_History(username, users):
    try:
        with open(TRANSACTION_FILE, "r") as f:
            for line in f:
                if line.startswith(f"{username}: "): #Only shows transaction for current user
                    print(line)
    except FileNotFoundError:
        print("No transactions found.")
    print(LINE)
    Banking_Menu(username, users) #Returns the user to banking menu

#Program starts here
Login_Selection()