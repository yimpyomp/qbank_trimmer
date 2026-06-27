import random


def normalize_filter_text(text):
    if text is None:
        return None
    return " ".join(text.split()).lower()


def filter_learning_areas(learning_area_filter, catalog):
    """
    Does what it says it does
    :param learning_area_filter: List of learning areas to be targeted
    :param catalog: Big ol json
    :return: dictionary of filtered stuff
    """
    trimmed_catalog = {}
    for entry in catalog.keys():
        question = catalog[entry]
        for item in learning_area_filter:
            if item in question:
                trimmed_catalog[entry] = question
    return trimmed_catalog


def filter_skills(skill_filter, catalog):
    """
    Like learning area filter but for skills
    :param skill_filter:
    :param catalog:
    :return:
    """
    trimmed_catalog = {}
    for entry in catalog.keys():
        question = catalog[entry]
        for item in skill_filter:
            if item in question:
                trimmed_catalog[entry] = question
    return trimmed_catalog


def filter_difficulty(difficulty_filter, catalog):
    """
    take a wild guess
    :param difficulty_filter:
    :param catalog:
    :return:
    """
    trimmed_catalog = {}
    for entry in catalog.keys():
        question = catalog[entry]
        for item in difficulty_filter:
            if item in question:
                trimmed_catalog[entry] = question
    return trimmed_catalog


def filter_catalog(catalog, learning_area=None, skill=None, difficulty=None):
    # New dictionary to store results
    filtered_catalog = {}

    for question_id, question_data in catalog.items():
        question_difficulty = normalize_filter_text(question_data["difficulty"])
        question_learning_area = normalize_filter_text(question_data["learning_area"])
        question_skill = normalize_filter_text(question_data["skill"])

        if difficulty is not None and question_difficulty != difficulty:
            continue

        if learning_area is not None and question_learning_area != learning_area:
            continue

        if skill is not None and question_skill != skill:
            continue

        if not question_data["blank_question_page"]:
            continue

        if not question_data["answer_key_page"]:
            continue

        filtered_catalog[question_id] = question_data

    return filtered_catalog


def select_questions(catalog, number_of_questions, randomize=True):
    if number_of_questions <= 0:
        raise ValueError("number_of_questions must be greater than 0")

    question_ids = catalog.keys()
    if randomize:
        selected_ids = random.sample(question_ids, number_of_questions)
    else:
        selected_ids = question_ids[:number_of_questions]

    selected_catalog = {}

    for item in selected_ids:
        selected_catalog[item] = catalog[item]

    return selected_catalog



