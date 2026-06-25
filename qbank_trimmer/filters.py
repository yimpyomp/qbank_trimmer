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