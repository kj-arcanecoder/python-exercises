import random

import os

class Hangman:
    def __init__(self):
        self.words = ["mountain", "treasure", "butterfly", "umbrella", "diamond", "festival", "horizon", "whisper", "adventure",
                      "sunshine", "blankets", "firewood", "rainfall", "sandwich", "airplane", "midnight", "hospital", "champion",
                      "calendar", "necklace", "gardenia", "painting", "notebook", "daydream", "beautiful", "birthday", "blossom",
                      "daughter", "tomorrow", "cupboard", "discover", "elephant", "friendship", "laughter", "distance", "movement",
                      "daughter", "memories", "marathon", "favorite", "language", "vacation", "football", "goodness", "mountain",
                      "shoulder", "triangle", "creative", "neighbor", "treasure"]
    
    def play_game(self):
        print("-----------------Hangman-----------------")
        count = 10
        word_guessed = False
        word = random.choice(self.words)
        word_guess = "_" * len(word)
        guessed_letters = set()
        while word != word_guess and count > 0:
            print(" ".join(word_guess))
            letter_guess = input("Enter a letter to guess: ").lower()
            correct_guess = False
            if letter_guess in guessed_letters:
                print("You already guessed that letter.")
                continue
            guessed_letters.add(letter_guess)
            for letter_index in range(len(word)):
                if(word[letter_index] == letter_guess):
                    word_guess_list = list(word_guess)
                    word_guess_list[letter_index] = letter_guess
                    word_guess = "".join(word_guess_list)
                    correct_guess = True
            if not correct_guess:
                count -= 1
            if word == word_guess:
                word_guessed = True
                print("You win!")
                self.words.remove(word)
                break
            if not word_guessed:
                print("\n")
                print(f"{count} attempts left")
        if not word_guessed:
            print(f"You lose, the word was {word}")

hangman = Hangman()
is_continue = True 
while is_continue == True:
    os.system("cls")
    hangman.play_game()
    choice = input("Do you want to continue (y/n): ")
    if choice == 'y' or choice == 'Y':
        continue
    elif choice == 'n' or choice == 'N':
        is_continue = False
    else:
        print("Invalid choice.")