import words
import random
import state as count_score

def get_random_word():
    return list(random.choice(words.words))

def get_jumbled_word(random_word):
    return ''.join(random.sample(random_word, len(random_word)))

def compare_word(guess, jumbled_word, original_word):
    letter_match = ""
    is_invalid_attempt = False
    if(len(guess) == len(jumbled_word)):
        for i in range(0,len(guess)):
            if guess[i] == original_word[i]:
                letter_match += guess[i]
            else:
                letter_match += "*"
    else:
        print("Count of letters do not match.")
        is_invalid_attempt = True
    if(guess == original_word):
        print("You win!")
        count_score.record_win()
        count_score.init_attempts()
    else:
        if not is_invalid_attempt:
            print(f"Correct letters in position: {letter_match}")
        print(f"{count_score.attempts_left} attempts left")
        count_score.record_failed_attempt()
        time.sleep(1)
    return letter_match