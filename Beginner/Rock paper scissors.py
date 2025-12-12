import random
from enum import Enum

class Rpc(Enum):
    ROCK = 'rock'
    PAPER = 'paper'
    SCISSORS = 'scissors'

class Game:
    def __init__(self):
        self.win = 0
        self.lose = 0

    def play(self):
        random_choice = random.choice(list(Rpc))
        try:
            user_input = input("Enter rock, paper or scissors: ").lower()
            choice = Rpc(user_input)
        except ValueError:
            print("Invalid input! Please enter rock, paper, or scissors.")
            return
        if (
            (choice == Rpc.PAPER and random_choice == Rpc.ROCK)
            or (choice == Rpc.ROCK and random_choice == Rpc.SCISSORS)
            or (choice == Rpc.SCISSORS and random_choice == Rpc.PAPER)
        ):
            print("You win!")
            self.win += 1
        elif choice == random_choice:
            print("It's a tie!")
        else:
            print(f"You lose, your opponent chose {random_choice.value}")
            self.lose += 1

def main():
    game = Game()
    continue_game = True
    while continue_game:
        game.play()
        a = input("Do you want to play again (y/n)? ")
        if a.lower() == "n":
            continue_game = False
    print(f"Final score: \n Wins: {game.win} \n Lose: {game.lose}")

if __name__ == "__main__":
    main()
