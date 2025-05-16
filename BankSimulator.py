MAXIMUM_AGE = 18
MINIMUM_AGE = 13

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
        user_choice = int(input("1. Login\n2. Sign Up\n"))
        if user_choice == 1:
            Login()
            break
        elif user_choice == 2:
            Sign_Up()
            break
        else:
            print("please enter 1 or 2")

def Login():
    None
    
def Sign_Up():
    None
    
Valid_Age()