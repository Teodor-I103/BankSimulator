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
        elif user_choice is None: #If user exits the menu from top right corner
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
        elif "," in username:
            msgbox("Username cannot contain a comma.")
        else:
            break
    username = username.strip() #Removes any spaces after the username
    while True:
        password = passwordbox("Please enter a password: ", "Bank Simulator")
        if password is None:
            Login_Selection() #Returns the user to login or sign up menu
        elif len(password) < 6: #Check password length
            msgbox("Password must be at least 6 characters long.")
        elif "," in password:
            msgbox("Password cannot contain a comma.")
        else:
            confirm_password = passwordbox("Please confirm your password: ", "Bank Simulator")
            if confirm_password is None:
                Login_Selection() #Returns the user to login or sign up menu
            elif password == confirm_password:
                break
            else:
                msgbox("Passwords do not match")
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
            msgbox("Too many incorrect attempts.")
            Login_Selection() #Retunrs the user to login or sign up menu
            break
        password = passwordbox(f"Incorrect password, you have {MAX_TRIES - password_tries} tries left.\nPlease enter a password: ", "Bank Simulator")
        password_tries += 1
        if password is None:
            Login_Selection() #Returns the user to login or sign up menu
    msgbox(f"Welcome {username}!")
    Banking_Menu(username, users) #Proceed to banking menu

#Main banking menu for transactions
def Banking_Menu(username, users):
    while True:
        banking_choice = buttonbox(f"Your current balance is: ${users[username]['balance']:.2f}", "Banking Menu", BANKING_CHOICES)
        if banking_choice == "Withdraw":
            Withdraw(username, users) #Proceeds to withdraw function
        elif banking_choice == "Deposit":
            Deposit(username, users) #Proceeds to deposit function
        elif banking_choice == "Display Transactions":
            Transaction_History(username, users) #Proceeds to transaction history function
        elif banking_choice == "Logout":
            exit_confirmation = buttonbox("Are you sure you wish to logout", "Bank Simulator", ["Yes", "No"])
            if exit_confirmation == "Yes":
                msgbox("You have logged out of your account")
                Login_Selection()
                break

#Append a transaction to the transaction log
def Log_Transaction(username, message):
    with open(TRANSACTION_FILE, "a") as f:
        f.write(f"{username}: {message}\n")

#Withdraw money from user's balance
def Withdraw(username, users):
    while True:
        amount = enterbox(f"Your current balance is: ${users[username]['balance']:.2f}\nPlease enter how much you would like to withdraw:")
        if amount is None: #Check if the user pressed cancel
            break
        try:
            amount = float(amount)
            if amount <= 0: #Check if the amount is positive
                msgbox("Please enter an amount greater than 0")
            elif amount > users[username]["balance"]: #Check if the amount is greater than the balance
                msgbox("Not enough balance available.")
            else:
                users[username]["balance"] -= amount
                save_users(users)
                Log_Transaction(username, f"Withdrew ${amount:.2f}")
                msgbox(f"Withdrawal successful!\nYou have withdrawn ${amount:.2f}")
                break
        except ValueError:
            msgbox("Please enter a number")

#Deposit money to user's balance
def Deposit(username, users):
    while True:
        amount = enterbox("Please enter how much you would like to deposit:")
        if amount is None: #Check if the user pressed cancel
            return
        try:
            amount = float(amount)
            if amount <= 0: #Check if the amount is positive
                msgbox("Please enter an amount greater than 0")
            elif amount > 10000:
                msgbox("Cannot deposit more than $10,000 at a time.")
            else:
                users[username]["balance"] += amount
                save_users(users)
                Log_Transaction(username, f"Deposited ${amount:.2f}")
                msgbox(f"Deposit successful!\nYou have deposited ${amount:.2f}")
                return
        except ValueError:
            msgbox("Please enter a number")

#Show transaction history for all users (optionally could be filtered per user)
def Transaction_History(username, users):
    transaction_message = []
    try:
        with open(TRANSACTION_FILE, "r") as f:
            for line in f:
                if line.startswith(f"{username}: "): #Only shows transaction for current user
                    transaction_message.append(line)
    except FileNotFoundError:
        msgbox("No transactions found.")
    transaction_message.append(f"Current Balance: ${users[username]['balance']:.2f}")
    textbox("Transaction History", "Bank Simulator", transaction_message)

#Program starts here
Login_Selection()