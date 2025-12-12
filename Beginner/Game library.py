import sys


class Game:
    """_summary_ Class to maintain games related attributes
    """
    def __init__(self, title, publisher, is_borrowed):
        self.title = title
        self.publisher = publisher
        self.is_borrowed = is_borrowed

class Library:
    """_summary_ Class to manage the Library functionalities
    """
    def __init__(self):
        self.games=[Game("Red Dead Redemption","Rockstar Games",False),
                   Game("Ghost of Tsushima","Sucker Punch",False),
                   Game("Elden Ring","From Software",False),
                   Game("Helldivers 2","Arrowhead",False),
                   Game("Death Stranding","Kojima Productions",False)]
        
    def add_new_game(self):
        is_continue = True
        while is_continue:
            title = input("Enter the game title: ")
            publisher = input("Enter the publisher: ")
            is_borrowed = False
            self.games.append(Game(title,publisher,is_borrowed))
            print(f"New game {title} added successfully!")
            choice = input("\nDo you want to add another game (y/n)?")
            match choice.lower():
                case "y":
                    print()
                case "n":
                    is_continue = False
                case _:
                    print("Invalid choice.")

    def borrow_game(self):
        is_continue = True
        while is_continue:
            is_borrowed = False
            game_borrow = input("Enter the game title you want to borrow: ")
            for game in self.games:
                if game.title.lower() == game_borrow.lower():
                    game.is_borrowed=True
                    is_borrowed = True
                    print(f"Game {game_borrow} borrowed!")
            if is_borrowed == False:
                print("Game not found.")
            choice = input("\nDo you want to borrow another game (y/n)?")
            match choice.lower():
                case "y":
                    print()
                case "n":
                    is_continue = False
                case _:
                    print("Invalid choice.")

    def return_game(self):
        print("Game titles borrowed: ")
        count = 0
        for game in self.games:
            if game.is_borrowed == True:
                count += 1
                print(game.title)
        print()
        while count != 0:
            game_return = input("Enter the game title you want to return: ")
            found = False
            for game in self.games:
                if game.title.lower() == game_return.lower() and game.is_borrowed:
                    game.is_borrowed = False
                    print(f"Game {game_return} has been successfully returned.")
                    found = True
                    count -= 1
                    break
            if not found:
                print("Game not found or not borrowed.")
            if count != 0: 
                choice = input("\nDo you want to return another game (y/n)?")
                match choice.lower():
                    case "y":
                        print()
                    case "n":
                        count = 0
                    case _:
                        print("Invalid choice.")

    def display_games(self):
        print("Title \t\t Publisher \t\t Borrowed")
        for game in self.games:
            print(f"{game.title}\t{game.publisher}\t{game.is_borrowed}")

    def display_menu(self):
        print("-------------------Game Library-----------------")
        print("\n1. Add a new game")
        print("\n2. Borrow a game")
        print("\n3. Return a game")
        print("\n4. View all games")
        print("\n5. Exit")

def main():
    library = Library()
    choice = 4
    while choice != 5:
        library.display_menu()
        choice = int(input("Input : "))
        if choice == 1:
            library.add_new_game()
        elif choice == 2:
            library.borrow_game()
        elif choice == 3:
            library.return_game()
        elif choice == 4:
            library.display_games()
        elif choice == 5:
            print("Thank you!")
            sys.exit()
        else:
            print(" Invalid choice. \n")

main()


