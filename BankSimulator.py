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
                None
        except ValueError:
            print("Please enter an integer")

Valid_Age()