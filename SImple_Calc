# Simple 4 by 4 Calculator
# Function for adding numbers
def add(x,y):
    return (x + y)

# Function for subtracting numbers
def sub(x,y):
    return (x - y)

# Function for multiplying numbers
def mul(x,y):
    return (x * y)

# Function for dividing numbers
def div(x,y):
    return (x/y)

play = 1

# while loop used to ask the user if he wants to play again
while (play == 1):
    print("\nSelect the operation you wish to do \n")
    print("1.Add")
    print("2.Subtract")
    print("3.Multiply")
    print("4.Divide \n")

    choice = int(input("Enter your choice of operation(1-4): "))

    x = float(input("\nEnter a number: "))
    y = float(input("Enter a second number: "))

# while loop to compare the choice and ask the user to re-enter if he enters the wrong choice
    while (choice):
        if (choice == 1):
            print("\n", x, "+", y, "is", add(x,y))
            break
        elif (choice == 2):
            print("\n", x, "-", y, "is", sub(x,y))
            break
        elif (choice == 3):
            print("\n", x, "*", y, "is", mul(x,y))
            break
        elif (choice == 4):
            print("\n", x, "/", y, "is", div(x,y))
            break
        else:
            print("\nIncorrect choice entered!!")
            print("Please enter a choice from 1 to 4 only!!")
            choice = int(input("\nEnter a choice again: "))

    answer = input("\nDo you wish to calculate again? (Y/N)")
    if (answer == 'Y' or answer == 'y'):
        play = 1
    else:
        print("\nThanks for calculating!")
        play = 0
        break
