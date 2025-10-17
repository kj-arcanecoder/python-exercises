import words
import utils as game_utils
import state as count_score

import os

def play_game():
    os.system("cls")
    random_word = game_utils.get_random_word()
    jumbled_word = game_utils.get_jumbled_word(random_word)

    print("****************** WORD JUMBLE *******************")
    guess = ""
    original_word = ''.join(random_word)
    count_score.init_attempts()

    while original_word != guess and count_score.attempts_left >= 0:
        print(f"\n\nWord to correctly assemble is: {jumbled_word}")
        guess = input("Enter your guess: ")
        if not guess.strip():
            print("Please enter a word.")
            continue
        letter_match = game_utils.compare_word(guess, jumbled_word, original_word)

    if count_score.attempts_left <= 0:
        print(f"You lose! The word was {original_word}")
        count_score.record_loss()
        input("\n\nPress Enter to continue...")
        break
        