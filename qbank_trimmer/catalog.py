from .pdf_tools import verify_master_copies, read_file
from .extraction import (
    extract_question_id,
    extract_learning_area,
    extract_question_difficulty,
    extract_answer,
    extract_skill)
from pypdf import PdfReader
from .config import COMBINED_QUESTIONS_PATH, CATALOG_PATH, CATALOG_REPORT_PATH
import json
from .reports import save_catalog_blank_results


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

    return question_catalog


def generate_catalog():
    working_catalog = catalog_questions()
    working_catalog = catalog_blank(working_catalog)
    save_catalog(working_catalog)
    return working_catalog


def catalog_blank(catalog):
    """
    Scan the combined blank-question PDF and add blank-question page numbers
    to the existing question catalog.
    """

    blank_pages = PdfReader(COMBINED_QUESTIONS_PATH).pages


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
        missing_blank_pages,
        output_path=CATALOG_REPORT_PATH
    )

    save_catalog(catalog)

    return catalog


def save_catalog(catalog, output_path=CATALOG_PATH):
    with open(output_path, "w") as f:
        json.dump(catalog, f, indent=4)


def load_catalog(catalog_path=CATALOG_PATH):
    with open(catalog_path, "r") as f:
        return json.load(f)
