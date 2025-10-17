import random

def inputNumber(random_integer):
    guessNumber = int(input("Enter number (0 to 100): "))
    global counter
    counter = counter - 1
    if(counter==100):
        return
    if(counter !=0):
        numberGuesser(guessNumber)
    else:
        print(f"You lose! :(, the number is {random_integer}")



def numberGuesser(number):
    global random_integer
    while counter != 0:
        match number:
            case number if number > random_integer: 
                print(f"High! {counter} attempts left") 
                inputNumber(random_integer)
            case number if number < random_integer:
                print(f"Low!  {counter} attempts left")
                inputNumber(random_integer)
            case _:
                print("You win! :)")
                exit()
print("Number guesser!!!!!!!!")
random_integer = random.randint(1, 100)
counter = 10
inputNumber(random_integer)