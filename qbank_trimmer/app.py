from qbank_trimmer.catalog import load_catalog, generate_catalog, save_catalog
from qbank_trimmer.filters import filter_catalog, select_questions
from qbank_trimmer.generation import generate_question_pdf, generate_answer_pdf


def generate_questions(settings, progress_callback=None):
    if progress_callback:
        progress_callback("Loading catalog")
    catalog = load_catalog(settings["subject"], settings.get("catalog_path"))

    if progress_callback:
        progress_callback("Filtering catalog")
    filtered_catalog = filter_catalog(catalog, settings["learning_area"], settings["skill"], settings["difficulty"])

    if progress_callback:
        progress_callback("Selecting Questions")
    selected_questions = select_questions(filtered_catalog, settings["count"])

    if progress_callback:
        progress_callback("Generating question PDF")
    if not settings["questions_output_path"]:
        generate_question_pdf(selected_questions, settings["subject"])
    else:
        generate_question_pdf(selected_questions, settings["subject"], settings["questions_output_path"])

    if progress_callback:
        progress_callback("Creating solution PDF")
    if not settings["answers_output_path"]:
        generate_answer_pdf(selected_questions, settings["subject"])
    else:
        generate_answer_pdf(selected_questions, settings["subject"], settings["answers_output_path"])

    if progress_callback:
        progress_callback("Generation complete")


def create_catalog(settings):
    catalog = generate_catalog(settings["answers_source"], settings["questions_source"], settings["subject"])

    output_path = settings["catalog_path"]

    save_catalog(catalog, output_path)

    return output_path