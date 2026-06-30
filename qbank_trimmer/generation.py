import random
from pathlib import Path
from pypdf import PdfReader, PdfWriter

from .config import COMBINED_QUESTIONS_PATH, COMBINED_SOLUTIONS_PATH, GENERATED_DIR


def collect_blank_pages(catalog):
    page_numbers = []

    for question_data in catalog.values():
        page_numbers.extend(question_data["blank_question_page"])

    return page_numbers


def collect_answer_pages(catalog):
    answer_page_numbers = []

    for question_data in catalog.values():
        answer_page_numbers.extend(question_data["answer_key_page"])

    return answer_page_numbers


def write_pages_to_pdf(source_pdf_path, page_numbers, output_path):
    source_pdf_path = Path(source_pdf_path)
    output_path = Path(output_path)
    output_path.parent.mkdir(parents=True, exist_ok=True)

    reader = PdfReader(source_pdf_path)
    writer = PdfWriter()

    total_pages = len(reader.pages)

    for page_number in page_numbers:
        if page_number < 1 or page_number > total_pages:
            raise ValueError(
                f"Catalog requested page {page_number}, "
                f"but {source_pdf_path} only has {total_pages} pages."
            )

        page_index = page_number - 1
        writer.add_page(reader.pages[page_index])

    with open(output_path, "wb") as f:
        writer.write(f)

    return output_path


def generate_question_pdf(
        catalog,
        output_path=GENERATED_DIR / "selected_questions.pdf",
        source_pdf_path=COMBINED_QUESTIONS_PATH,
):
    page_numbers = collect_blank_pages(catalog)
    return write_pages_to_pdf(
        source_pdf_path,
        page_numbers=page_numbers,
        output_path=output_path,
    )


def generate_answer_pdf(
        catalog,
        output_path=GENERATED_DIR / "selected_answers.pdf",
        source_pdf_path=COMBINED_SOLUTIONS_PATH,
):
    page_numbers = collect_answer_pages(catalog)
    return write_pages_to_pdf(
        source_pdf_path,
        page_numbers=page_numbers,
        output_path=output_path,
    )




