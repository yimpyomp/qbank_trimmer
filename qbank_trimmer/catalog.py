from .pdf_tools import verify_master_copies, read_file
from .extraction import (
    extract_question_id,
    extract_learning_area,
    extract_question_difficulty,
    extract_answer,
    extract_skill,
    extract_metadata)
from pypdf import PdfReader
from .config import COMBINED_QUESTIONS_PATH, CATALOG_PATH, CATALOG_REPORT_PATH
import json
from .reports import save_catalog_blank_results
import pdfplumber


# Use this for RW questions only
def catalog_questions(answer_pdf_path):
    question_catalog = {}
    combined_answers = read_file(answer_pdf_path)
    pages = combined_answers.pages

    current_id = None

    for i, page in enumerate(pages):
        page_number = i + 1
        text = page.extract_text() or ""

        question_id = extract_question_id(text)

        if question_id:
            current_id = question_id
            metadata = extract_metadata(text)

            question_catalog[current_id] = {
                "learning_area": metadata["learning_area"],
                "skill": metadata["skill"],
                "difficulty": metadata["difficulty"],
                "answer": extract_answer(text),
                "answer_key_page": [page_number],
                "blank_question_page": [],
            }

            continue

        if current_id is not None:
            question_catalog[current_id]["answer_key_page"].append(page_number)

            continuation_answer = extract_answer(text)
            if (
                    question_catalog[current_id]["answer"] is None
                    and continuation_answer is not None
            ):
                question_catalog[current_id]["answer"] = continuation_answer

    return question_catalog


def generate_catalog(answer_pdf_path, question_pdf_path, subject):
    if subject == "rw":
        working_catalog = catalog_questions(answer_pdf_path)
        working_catalog = catalog_blank(working_catalog, question_pdf_path)
    elif subject == "math":
        working_catalog = catalog_math_solutions_plumber(answer_pdf_path)
        working_catalog = catalog_math_blank_plumber(question_pdf_path, working_catalog)

    save_catalog(working_catalog)

    return working_catalog


# Use this for rw only
def catalog_blank(catalog, questions_pdf_path):
    blank_pages = PdfReader(questions_pdf_path).pages
    current_id = None

    for i, page in enumerate(blank_pages):
        page_number = i + 1
        text = page.extract_text() or ""

        question_id = extract_question_id(text)

        if question_id:
            current_id = question_id

            if current_id in catalog:
                catalog[current_id]["blank_question_page"] = [page_number]

                metadata = extract_metadata(text)

                if catalog[current_id]["learning_area"] is None:
                    catalog[current_id]["learning_area"] = metadata["learning_area"]

                if catalog[current_id]["skill"] is None:
                    catalog[current_id]["skill"] = metadata["skill"]

                if catalog[current_id]["difficulty"] is None:
                    catalog[current_id]["difficulty"] = metadata["difficulty"]

            continue

        if current_id is not None and current_id in catalog:
            catalog[current_id]["blank_question_page"].append(page_number)

    return catalog


def save_catalog(catalog, output_path=CATALOG_PATH):
    with open(output_path, "w") as f:
        json.dump(catalog, f, indent=4)


def load_catalog(catalog_path=CATALOG_PATH):
    with open(catalog_path, "r") as f:
        return json.load(f)


def catalog_math_solutions_plumber(answer_pdf_path):
    # Initialize dictionary to hold catalog
    question_catalog = {}

    # Store previous question ID
    last_id = None

    # Begin iterating through file
    with pdfplumber.open(answer_pdf_path) as pdf:
        for page_index, page in enumerate(pdf.pages):
            # Get text and info tables for the page
            page_text = page.extract_text() or ""
            page_table = page.extract_table()
            page_number = page_index + 1
            # Check if page contains a question ID, add number to previous entry if not
            current_id = extract_question_id(page_text)
            if current_id:
                last_id = current_id
            if not current_id:
                if last_id in question_catalog:
                    question_catalog[last_id]["answer_key_page"].append(page_number)
                continue

            if current_id not in question_catalog:
                question_catalog[current_id] = {"learning_area": None,
                                                "skill": None,
                                                "difficulty": None,
                                                "answer": None,
                                                "answer_key_index": [],
                                                "answer_key_page": [],
                                                "blank_question_index": [],
                                                "blank_question_page": []}

            question_catalog[current_id]["answer_key_index"].append(page_index)
            question_catalog[current_id]["answer_key_page"].append(page_number)
            current_answer = extract_answer(page_text)
            if current_answer:
                question_catalog[current_id]["answer"] = current_answer

            if page_table and len(page_table) >= 2 and len(page_table[1]) >= 5:
                question_catalog[current_id]["learning_area"] = page_table[1][2]
                question_catalog[current_id]["skill"] = page_table[1][3]
                question_catalog[current_id]["difficulty"] = page_table[1][4]

    return question_catalog


def catalog_math_blank_plumber(blank_pdf_path, math_catalog):
    # Initialize last question ID
    last_id = None
    # Open blank pdf
    with pdfplumber.open(blank_pdf_path) as pdf:
        # Iterate through the pages
        for page_index, page in enumerate(pdf.pages):
            # Get page number, extract tables and text
            page_number = page_index + 1
            page_table = page.extract_table()
            page_text = page.extract_text() or ""

            # Attempt to extract question ID
            current_id = extract_question_id(page_text)

            if current_id:
                last_id = current_id
                math_catalog[current_id]["blank_question_index"].append(page_index)
                math_catalog[current_id]["blank_question_page"].append(page_number)


            else:
                if last_id in math_catalog:
                    math_catalog[last_id]["blank_question_index"].append(page_index)
                    math_catalog[last_id]["blank_question_page"].append(page_number)
                continue

    return math_catalog


