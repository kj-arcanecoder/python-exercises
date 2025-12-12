import html
import logging
import random
import time

from . import quiz_api
from . import quiz_utils

logger = logging.getLogger(__name__)

def choose_mode_menu():
    """Displays the quiz type menu to the user
    """
    print("1. Speed round (8 questions)")
    print("2. Standard quiz (12 questions)")
    print("3. Extended challenge (20 questions) ")

def start_default_quiz(player_name):
    """Starting point of the default quiz mode

    Args:
        player_name (string): name of the player
    """
    logger.info("Starting default quiz")
    difficulty, category = None, None
    choose_quiz_mode(player_name, difficulty, category)
    
def start_custom_quiz(player_name):
    """Starting point of the default quiz mode

    Args:
        player_name (string): name of the player
    """
    logger.info("Starting custom quiz")
    
    difficulty = ""
    difficulties = ["easy","medium","hard"]
    while True:
        quiz_utils.clear_and_print_header("Trivia Quiz App - Custom Quiz")
        difficulty = input("\nEnter the difficulty (easy, medium, hard) : ").lower()
        if difficulty in difficulties:
            break
        else:
            print("Invalid choice, try again.")
    
    logger.info("Fetching the categories from the API")
    categories_list = quiz_api.get_raw_categories()
    if not categories_list:
        print("Failed to fetch the categories, try again after sometime.")
        time.sleep(2)
    else:
        category = ""
        while True:
            quiz_utils.clear_and_print_header("Trivia Quiz App - Custom Quiz")
            print("\nCategories\n")
            for i in range(len(categories_list)):
                if i % 2 == 0:
                    print(f"{i+1}. {categories_list[i]['name']}".ljust(60), end="")
                else:
                    print(f"{i+1}. {categories_list[i]['name']}")
            try:
                category_choice = int(input(f"\nEnter category choice (1 to {len(categories_list)}): "))
            except ValueError:
                print("Invalid choice, try again.")
            else:
                category = categories_list[category_choice-1]['id']
                break

        choose_quiz_mode(player_name, difficulty, category)

def choose_quiz_mode(player_name, difficulty, category):
    """Takes input from the user on the type of quiz they want to play,
    and sets up the game.

    Args:
        player_name (string): name of the player
        difficulty (string): difficulty of questions (if it is a custom quiz)
        category (string): category of questions (if it is a custom quiz)
    """
    mode_menu_choice = 0
    while True:
        if not difficulty and not category:
            quiz_utils.clear_and_print_header("Trivia Quiz App - Default Quiz")
        else:
            quiz_utils.clear_and_print_header("Trivia Quiz App - Custom Quiz")
        choose_mode_menu()
        try:
            mode_menu_choice = int(input("\nChoose the quiz mode (1, 2 or 3): "))
        except ValueError:
            print("Invalid choice, input again.")
            mode_menu_choice = 0
            time.sleep(1)
            continue
        else:
            match mode_menu_choice:
                case 1:
                    amount, round_type = 8, "Speed round"
                    setup_game(player_name, amount, difficulty, category, round_type)
                    break
                case 2:
                    amount, round_type = 12, "Standard quiz"
                    setup_game(player_name, amount, difficulty, category, round_type)
                    break
                case 3:
                    amount, round_type = 20, "Extended challenge"
                    setup_game(player_name, amount, difficulty, category, round_type)
                    break
                case _:
                    print("Invalid choice, input again.")
                    mode_menu_choice = 0
                    time.sleep(1)
                    continue

def setup_game(player_name, amount, difficulty, category, round_type):
    """Sets up the quiz by loading the questions from the API based on 
    difficulty and category and starts the quiz.

    Args:
        player_name (string): name of player
        amount (int): amount of questions
        difficulty (string): difficulty of quiz
        category (string): category of quiz
        round_type (string): type of quiz
    """
    print("Loading questions, please wait.")
    logger.info("Fetching the questions from the API.")
    questions = quiz_api.get_raw_dumps(amount, difficulty, category)
    if not questions:
        print(f"Failed to retreive the questions, "
                "check your connection or try again after sometime.")
        time.sleep(2)
    else:
        print(f"Questions fetched successfully, good luck {player_name}!")
        time.sleep(2)
        play_game(questions, round_type, player_name)
        
def play_game(questions, round_type, player_name):
    """Starts the quiz

    Args:
        questions (dict): dictionary of questions fetched from the API
        round_type (string): Type of quiz
        player_name (string): name of player
    """
    counter, result = 0, 0
    for question in questions:
        counter += 1
        logger.info(f"Displaying question {counter} to user for {round_type}")
        if question['type'] == "multiple":
            result = play_mcq_question(question, result, round_type, counter)
        else:
            result = play_bool_question(question, result, round_type, counter)
        input("\nPress Enter to continue...")
    correct_perc = round(float((result/counter)*100),2)
    logger.info(f"{round_type} completed, displaying the result.")
    show_quiz_summary(counter, result, correct_perc)
    logger.info(f"Storing the result for {player_name}")
    quiz_utils.store_results(player_name, counter, result, correct_perc)
    input("\nPress Enter to continue...")

def show_quiz_summary(counter, result, correct_perc):
    """Displays the summary of the quiz post completion.

    Args:
        counter (int): Total questions
        result (int): Correct answers count
        correct_perc (float): Correct percentage
    """
    print(f"\nGame over, here's the summary:")
    print(f"\nTotal questions: {counter}")
    print(f"Correct answers count: {result}")
    print(f"Correct percentage: {correct_perc}")
            
def play_mcq_question(question, result, round_type, counter):
    """Displays the content of a mcq question

    Args:
        question (dict): dictionary of a mcq question
        result (int): count of correct answers
        round_type (string): type of quiz
        counter (int): current count of question

    Returns:
        int: updated count of correct answers
    """
    choices = question['incorrect_answers'] 
    choices.append(question['correct_answer'])
    random.shuffle(choices)
    while True:
        quiz_utils.clear_and_print_header(f"{round_type}: Quesion {counter}")
        print(f"\nCategory : {html.unescape(question['category'])}")
        print(f"\n{html.unescape(question['question'])}\n")
        for i in range(len(choices)):
            if i % 2 == 0:
                print(f"{i+1}. {html.unescape(choices[i])}".ljust(60), end="")
            else:
                print(f"{i+1}. {html.unescape(choices[i])}")
        try:
            answer = int(input("\nEnter your answer: ")) - 1
        except ValueError:
            print("\nInvalid input, try again.")
            time.sleep(2)
            continue
        else:
            if answer in range(len(choices)):
                break
            else:
                print("\nInvalid input, try again.")
                time.sleep(2)
                continue
    if choices[answer] == question['correct_answer']:
        print("Correct answer! ")
        result += 1
    else:
        print(f"Incorrect answer, correct answer is "
              f"{html.unescape(question['correct_answer'])}")
    return result
    
def play_bool_question(question, result, round_type, counter):
    """Displays the content of a boolean question

    Args:
        question (dict): dictionary of a mcq question
        result (int): count of correct answers
        round_type (string): type of quiz
        counter (int): current count of question

    Returns:
        int: updated count of correct answers
    """
    choices = question['incorrect_answers']
    choices.append(question['correct_answer'])
    while True:
        quiz_utils.clear_and_print_header(f"{round_type}: Question {counter}")
        print(f"\nCategory : {html.unescape(question['category'])}")
        print(f"\n{html.unescape(question['question'])}\n")
        choices = sorted(choices, reverse=True)
        for i in range(len(choices)):
            if i % 2 == 0:
                print(f"{i+1}. {html.unescape(choices[i])}".ljust(45), end="")
            else:
                print(f"{i+1:>40}. {html.unescape(choices[i])}")
        try:
            answer = int(input("\nEnter your answer: ")) - 1
        except ValueError:
            print("\nInvalid input, try again.")
            time.sleep(2)
            continue
        else:
            if answer in range(len(choices)):
                break
            else:
                print("\nInvalid input, try again.")
                time.sleep(2)
                continue
    if choices[answer] == question['correct_answer']:
        print("Correct answer! ")
        result += 1
    else:
        print(f"Incorrect answer.")
    return result

def show_leaderboard():
    """Fetches and displays the leaderboard
    """
    logger.info("Fetching the leaderboard")
    leaderboard_dict = quiz_utils.load_leaderboard_to_display()
    print(f"{'Name':<30} {'Questions':<20}",end="")
    print(f"{'Correct Answers':<20} {'Correct Percentage':<20}")
    for player, stats in leaderboard_dict.items():
        print(f"{player:<30} {stats['questions_attempted']:<20}",end="")
        print(f"{stats['correct_answers']:<20} {stats['correct_percentage']:<20}")
    input("Press Enter to continue...")