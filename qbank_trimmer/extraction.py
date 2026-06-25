import re

skill_pattern = r"Skill\s+([\s\S]+?)\s+Di"
learning_area_pattern = r"Domain\s+([\s\S]+?)\s+Skill"
id_pattern = r'ID:\s*(.*)'
difficulty_pattern = r'culty:\s*(.*)'
answer_pattern = r'Correct Answer:\s*([A-Z])'





def extract_skill(page_text):
    """
    Determines which skill is applicable to question
    :param page_text: Raw text of page
    :return: Skill of current page if found, none if not found
    """
    match = re.search(skill_pattern, page_text, re.DOTALL)
    if match:
        return match.group(1).strip()
    else:
        return None


def extract_learning_area(page_text):
    """
    Same as extract skill but for learning area
    :param page_text: I haven't slept in a while
    :return: I am not repeating myself
    """
    match = re.search(learning_area_pattern, page_text, re.DOTALL)
    if match:
        return match.group(1).strip()
    else:
        return None


def extract_question_id(page_text):
    """
    Oh look, another extract function. Would you care to guess what it does?
    :param page_text:
    :return:
    """
    match = re.search(id_pattern, page_text)
    if match:
        return match.group(1)
    else:
        return None


def extract_question_difficulty(page_text):
    """
    another one
    :param page_text:
    :return:
    """
    match = re.search(difficulty_pattern, page_text)
    if match:
        return match.group(1)
    else:
        return None


def extract_answer(page_text):
    """
    and another one
    :param page_text:
    :return:
    """
    match = re.search(answer_pattern, page_text)
    if match:
        return match.group(1)
    else:
        return None