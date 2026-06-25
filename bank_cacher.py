import json
from pypdf import PdfReader, PdfWriter
import pathlib
import re


learning_area_key = {"LA1": ["Craft and Structure", []], "LA2": ["Information and Ideas", []],
                     "LA3": ["Standard English Conventions", []], "LA4": ["Expression of Ideas", []]}
difficulty_levels = ['Easy', 'Medium', 'Hard']
skill_list = []
skill_pattern = r"Skill\s+([\s\S]+?)\s+Di"
learning_area_pattern = r"Domain\s+([\s\S]+?)\s+Skill"
id_pattern = r'ID:\s*(.*)'
difficulty_pattern = r'culty:\s*(.*)'
answer_pattern = r'Correct Answer:\s*([A-Z])'


def initial_config():
    """
    Check if combined question/answer files exist, create combined files if not
    :return:
    """
    if not pathlib.Path('solns/combined_answers.pdf').exists():
        combine_answers()
    if not pathlib.Path('bank/combined_questions.pdf').exists():
        combine_questions()
    return None


def read_file(path):
    """
    Creates PDF reader object
    :param path: Filepath of pdf file to be read
    :return: The object. I don't like writing these
    """
    target_file = pathlib.Path(path)
    file_reader = PdfReader(target_file)
    return file_reader


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


def combine_answers():
    """
    Creates one large pdf from the various solution files
    :return: Nothing
    """
    # Only run this once
    # Create combined solution file
    answer_merger = PdfWriter()
    soln_dir = pathlib.Path('solns')
    for file in soln_dir.iterdir():
        answer_merger.append(file)
    combined_path = 'solns/combined_answers.pdf'
    answer_merger.write(combined_path)
    answer_merger.close()
    return None


def combine_questions():
    """
    Same as the answer function but this time for the files without answers
    :return:
    """
    # Creates one big file with all questions contained within
    question_merger = PdfWriter()
    bank_directory = pathlib.Path('bank')
    for file in bank_directory.iterdir():
        question_merger.append(file)
    combined_path = 'bank/combined_questions.pdf'
    question_merger.write(combined_path)
    question_merger.close()
    return None


def verify_master_copies():
    """
    Ensures that master files exist
    :return: Errors mostly
    """
    # Alternate logic for debugging
    if 'debug' in str(pathlib.Path.cwd()):
        return True
    if not pathlib.Path('solns/combined_answers.pdf').exists():
        raise Exception('Combined solution file not found. Please run initial config to generate it')
    if not pathlib.Path('bank/combined_questions.pdf').exists():
        raise Exception('Combined question file not found. Please run initial config to generate it')


def catalog_questions():
    """
    Scrape through the combined answer file to catalog all question info
    :return:
    """
    question_catalog = {}
    # Verify and load combined solution file
    verify_master_copies()
    combined_answers = read_file('solns/combined_answers.pdf')
    combined_pages = combined_answers.pages
    # Begin iterating through pages
    for i in range(len(combined_pages)):
        # Flag for pages containing information on multiple pages
        single_page = True
        current_text = combined_pages[i].extract_text()
        if i + 1 < len(combined_pages):
            next_text = combined_pages[i + 1].extract_text()
        else:
            next_text = current_text
        # Grab question ID
        current_id = extract_question_id(current_text)
        # Skip to next page if no question ID is present
        if not current_id:
            continue
        if current_id not in question_catalog.keys():
            question_catalog[current_id] = {
                "learning_area": None,
                "skill": None,
                "difficulty": None,
                "answer": None,
                "answer_key_page": [],
                "blank_question_page": [],
            }
        # Check if correct answer, difficulty, learning area, skill exist on current page

        # Learning area
        if extract_learning_area(current_text):
            question_catalog[current_id]["learning_area"] = extract_learning_area(current_text)
        else:
            question_catalog[current_id]["learning_area"] = extract_learning_area(next_text)
            single_page = False

        # Skill
        if extract_skill(current_text):
            question_catalog[current_id]["skill"] = extract_skill(current_text)
        else:
            question_catalog[current_id]["skill"] = extract_skill(next_text)
            single_page = False

        # Difficulty
        if extract_question_difficulty(current_text):
            question_catalog[current_id]["difficulty"] = extract_question_difficulty(current_text)
        else:
            question_catalog[current_id]["difficulty"] = extract_question_difficulty(next_text)
            single_page = False

        # Answer
        if extract_answer(current_text):
            question_catalog[current_id]["answer"] = extract_answer(current_text)
        else:
            question_catalog[current_id]["answer"] = extract_answer(next_text)
            single_page = False

        # Check flag and add appropriate marker
        if not single_page:
            print(f'Adding {[i, i + 1]}')
            question_catalog[current_id]["answer_key_page"] = [i + 1, i + 2]
        else:
            print(f'Adding {[i]}')
            question_catalog[current_id]["answer_key_page"] = [i + 1]

        # Validate list length
        #if len(question_catalog[current_id]) != 5:
        #    print(f'Error on page {i + 1}')

    return question_catalog


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
        print(question[2])
        for item in difficulty_filter:
            if item in question:
                trimmed_catalog[entry] = question
    return trimmed_catalog


def trim_blank_copy(filtered_catalog, master_blank):
    """
    Creates a blank version of all questions to be answered
    :param filtered_catalog: Catalog of questions to be included
    :param master_blank: PDF Reader object of combined blank copy
    :return: None, saves a PDF of selected questions
    """
    final_questions = consolidate_pages(filtered_catalog)
    trimmed_writer = PdfWriter()
    for page in final_questions:
        trimmed_writer.add_page(master_blank.pages[page])
    trimmer = open('output.pdf', 'wb')
    trimmed_writer.write(trimmer)
    trimmer.close()
    trimmed_writer.close()
    print('Trimmed sample generated')
    return None


def trim_answer_key(filtered_catalog, combined_answers):
    """
    Same as blank copy but with the answers
    :param filtered_catalog:
    :param combined_answers:
    :return:
    """
    # Please fucking refactor me soon before this gets too confusing in two weeks
    final_questions = consolidate_answer_pages(filtered_catalog)
    trimmed_writer = PdfWriter()
    for page in final_questions:
        trimmed_writer.add_page(combined_answers.pages[page])
    trimmer = open('solution_output.pdf', 'wb')
    trimmed_writer.write(trimmer)
    trimmer.close()
    trimmed_writer.close()
    print('Trimmed sample generated')
    return None


def add_blank_pages_to_catalog(catalog):
    blank_pages = PdfReader('bank/combined_questions.pdf').pages
    for i in range(len(blank_pages)):
        current_text = blank_pages[i].extract_text()
        current_id = extract_question_id(current_text)
        if current_id:
            catalog[current_id].append([i])
    return catalog


def update_cache(catalog):
    """
    I don't know why I was so dedicated the word cache. It isn't even appropriate here
    :param catalog:
    :return:
    """
    with open('catalog.json', 'w') as f:
        json.dump(catalog, f, indent=2)
        f.close()
    print('Catalog updated')
    return None


def consolidate_pages(catalog):
    """
    Creates a list of only page indices in the provided catalog
    :param catalog: Dictionary of questions to be included in final copy
    :return: List of only page indices
    """
    page_list = []
    for entry in catalog.keys():
        page_list.extend(catalog[entry][-1])
    return page_list


def consolidate_answer_pages(catalog):
    """
    Guess
    :param catalog:
    :return:
    """
    page_list = []
    for entry in catalog.keys():
        page_list.extend(catalog[entry][-2])
    return page_list


def generate_catalog():
    """
    I am sleepy
    :return:
    """
    working_catalog = catalog_questions()
    working_catalog = add_blank_pages_to_catalog(working_catalog)
    update_cache(working_catalog)
    return working_catalog

#######################################################################################################################
# Not my code
# TODO: Rewrite this myself

def save_catalog_blank_results(
        matched_ids,
        missing_from_catalog,
        missing_blank_pages,
        output_path="catalog_blank_results.txt"
):
    """
    Save a report showing how well blank-question pages were matched
    to the existing answer-key catalog.
    """

    with open(output_path, "w") as file:
        file.write("Catalog Blank Results\n")
        file.write("=====================\n\n")

        file.write("Summary\n")
        file.write("-------\n")
        file.write(f"Matched blank questions: {len(matched_ids)}\n")
        file.write(f"Blank IDs not found in answer catalog: {len(missing_from_catalog)}\n")
        file.write(f"Answer catalog IDs missing blank pages: {len(missing_blank_pages)}\n\n")

        file.write("Blank IDs not found in answer catalog\n")
        file.write("-------------------------------------\n")

        if missing_from_catalog:
            for question_id, page_index in missing_from_catalog:
                file.write(f"- {question_id} on blank PDF page {page_index + 1}\n")
        else:
            file.write("None\n")

        file.write("\nAnswer catalog IDs missing blank pages\n")
        file.write("-------------------------------------\n")

        if missing_blank_pages:
            for question_id in missing_blank_pages:
                file.write(f"- {question_id}\n")
        else:
            file.write("None\n")


def save_catalog(catalog, output_path="catalog.json"):
    """
    Save the full question catalog to a JSON file.

    Args:
        catalog: Dictionary containing question metadata and page numbers.
        output_path: Where the catalog should be saved.
    """

    with open(output_path, "w") as file:
        json.dump(catalog, file, indent=4)



def catalog_blank(catalog):
    """
    Scan the combined blank-question PDF and add blank-question page numbers
    to the existing question catalog.
    """

    blank_pages = PdfReader("bank/combined_questions.pdf").pages

    matched_ids = []
    missing_from_catalog = []

    # Make sure every entry has the blank-question field
    for question_id in catalog:
        if "blank_question_page" not in catalog[question_id]:
            catalog[question_id]["blank_question_page"] = []

    for i in range(len(blank_pages)):
        current_text = blank_pages[i].extract_text()
        current_id = extract_question_id(current_text)

        if not current_id:
            continue

        if current_id in catalog:
            catalog[current_id]["blank_question_page"].append(i + 1)
            matched_ids.append(current_id)
        else:
            missing_from_catalog.append((current_id, i + 1))

    missing_blank_pages = []

    for question_id, question_data in catalog.items():
        if not question_data["blank_question_page"]:
            missing_blank_pages.append(question_id)

    save_catalog_blank_results(
        matched_ids,
        missing_from_catalog,
        missing_blank_pages
    )

    save_catalog(catalog)

    return catalog

# No longer needed, catalog mildly verified
#result = catalog_questions()
#catalog_blank(result)