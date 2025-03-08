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


def read_file(path):
    file_reader = PdfReader(path)
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


def make_master_copy():
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


