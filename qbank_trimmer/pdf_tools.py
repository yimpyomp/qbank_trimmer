import pathlib
from pypdf import PdfReader, PdfWriter
from .config import COMBINED_QUESTIONS_PATH, COMBINED_SOLUTIONS_PATH


def initial_config():
    """
    Check if combined question/answer files exist, create combined files if not
    :return:
    """
    if not COMBINED_SOLUTIONS_PATH.exists():
        print("Combining solutions")
        combine_answers()
    if not COMBINED_QUESTIONS_PATH.exists():
        print("Combining questions")
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