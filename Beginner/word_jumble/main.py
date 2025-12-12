import state as count_score
import game
import os

def print_header():
    print("****************** WORD JUMBLE *******************")

def game_menu():
    os.system("cls")
    print_header()
    print("\n\n1. Play Game")
    print("\n2. Check Score")
    print("\n3. Exit")
def main():
    choice = 1
    while choice != 3:
        game_menu()
        choice = int(input("\n\n Input: "))
        if choice == 1:
            game.play_game()
        elif choice == 2:
            os.system("cls")
            print_header()
            print("\n\n\nScorecard:")
            count_score.show_score()
            input("\n\n\nPress Enter to continue...")



if __name__ == "__main__":
    main()

