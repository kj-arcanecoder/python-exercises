import requests
import logging

logger = logging.getLogger(__name__)

base_url = "https://opentdb.com"

def get_raw_dumps(amount, difficulty, category):
    """Fetches the questions from the quiz API based on the
    parameters requested from the user.

    Args:
        amount (int): the amount of questions
        difficulty (string): the difficulty of questions
        category (string): the category of questions

    Returns:
        dictionary: dictionary of questions received from the API.
    """
    question_dumps_url = form_request_url(amount, difficulty, category)
    headers = {"Accept": "application/json"}
    try:
        r = requests.get(question_dumps_url, headers)
    except requests.exceptions.ConnectionError:
        logger.error(f"Failed to fetch the API {question_dumps_url}")
        return {}
    else:
        logger.info(f"URL={question_dumps_url} responseCode={r.status_code}" 
                    f"elapsedTime={r.elapsed} status={r.reason}")
        response_dict = r.json()
        questions_dict = response_dict['results']
        return questions_dict

def form_request_url(amount, difficulty, category):
    """Forms the url of the API based on the parameters requested by the user

    Args:
        amount (int): the amount of questions
        difficulty (string): the difficulty of questions
        category (string): the category of questions
        
    Returns:
        string: the final quiz api url
    """
    question_dumps_url = base_url + f"/api.php?amount={amount}"
    if difficulty:
        question_dumps_url += f"&difficulty={difficulty}"
    if category:
        question_dumps_url += f"&category={category}"
    return question_dumps_url

def get_raw_categories():
    """Fetches all category types for the quiz from the API

    Returns:
        list: list of all categories
    """
    category_url = base_url + "/api_category.php"
    headers = {"Accept": "application/json"}
    try:
        r = requests.get(category_url, headers)
    except requests.exceptions.ConnectionError:
        logger.error(f"Failed to fetch the API {category_url}")
        return []
    logger.info(f"URL={category_url} responseCode={r.status_code}" 
                f"elapsedTime={r.elapsed} status={r.reason}")
    response_dict = r.json()
    categories_list = response_dict['trivia_categories']
    return categories_list