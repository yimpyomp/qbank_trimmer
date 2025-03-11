from pypdf import PdfReader, PdfWriter
import pathlib
import os
import pickle
import re


learning_area_key = {"LA1": ["Craft and Structure", []], "LA2": ["Information and Ideas", []],
                     "LA3": ["Standard English Conventions", []], "LA4": ["Expression of Ideas", []]}
difficulty_levels = ['ez', 'med', 'hard']
skill_list = []
skill_pattern = r"Skill\s+([\s\S]+?)\s+Di"
learning_area_pattern = r"Domain\s+([\s\S]+?)\s+Skill"
id_pattern = r'ID:\s*(.*)'
difficulty_pattern = r'Question Difficulty:\s*(.*)'
answer_pattern = r'Correct Answer:\s*([A-Z])'


def initial_config():
    if not pathlib.Path('solns/combined_answers.pdf').exists():
        combine_answers()
    if not pathlib.Path('bank/combined_questions.pdf').exists():
        combine_questions()
    return None


def read_file(path):
    target_file = pathlib.Path(path)

    file_reader = PdfReader(target_file)
    return file_reader


def extract_skill(page_text):
    match = re.search(skill_pattern, page_text, re.DOTALL)
    if match:
        return match.group(1).strip()
    else:
        return None


def extract_learning_area(page_text):
    match = re.search(learning_area_pattern, page_text, re.DOTALL)
    if match:
        return match.group(1).strip()
    else:
        return None


def extract_question_id(page_text):
    match = re.search(id_pattern, page_text)
    if match:
        return match.group(1)
    else:
        return None


def extract_question_difficulty(page_text):
    match = re.search(difficulty_pattern, page_text)
    if match:
        return match.group(1)
    else:
        return None


def combine_answers():
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
    print(pathlib.Path.cwd())
    # Alternate logic for debugging
    if 'debug' in str(pathlib.Path.cwd()):
        return True
    if not pathlib.Path('solns/combined_answers.pdf').exists():
        raise Exception('Combined solution file not found. Please run initial config to generate it')
    if not pathlib.Path('bank/combined_questions.pdf').exists():
        raise Exception('Combined question file not found. Please run initial config to generate it')


def catalog_questions():
    question_catalog = {}
    # Verify and load combined solution file
    verify_master_copies()
    combined_answers = read_file('solns/combined_answers.pdf')
    combined_pages = combined_answers.pages
    # Begin iterating through pages
    for i in range(len(combined_pages)):
        current_text = combined_pages[i].extract_text()
        if i + 1 < len(combined_pages):
            next_text = combined_pages[i + 1].extract_text()
        else:
            next_text = current_text
        # Grab question ID
        current_id = extract_question_id(current_text)
        if not current_id:
            pass
        if current_id not in question_catalog.keys():
            question_catalog[current_id] = []
        # Check if correct answer, difficulty, learning area, skill exist on current page
        if extract_learning_area(current_text):
            question_catalog[current_id].append(extract_learning_area(current_text))
        else:
            print('LA fallback')
            question_catalog[current_id].append(extract_learning_area(next_text))
        if extract_skill(current_text):
            question_catalog[current_id].append(extract_skill(current_text))
        else:
            print('skill fallback')
            question_catalog[current_id].append(extract_skill(next_text))

    print(question_catalog)
    return question_catalog



