import argparse
from pathlib import Path
from qbank_trimmer.pdf_tools import initial_config
from qbank_trimmer.catalog import generate_catalog, save_catalog, catalog_blank, load_catalog
from qbank_trimmer.generation import generate_question_pdf, generate_answer_pdf
from qbank_trimmer.filters import filter_catalog, select_questions
from qbank_trimmer.config import CATALOG_PATH, GENERATED_DIR

def parse_arguments():
    parser = argparse.ArgumentParser(
        description="Generate custom collections of SAT questions"
    )

    parser.add_argument(
        "-c",
        "--count",
        type=int,
        required=True,
        help="Number of questions to include"
    )

    parser.add_argument(
        "-d",
        "--difficulty",
        choices=["Easy", "Medium", "Hard"],
        help="Optional difficulty filter"
    )

    parser.add_argument(
        "-l",
        "--learning-area",
        help="Optional learning area filter."
    )

    parser.add_argument(
        "-s",
        "--skill",
        # TODO: Add list of options
        help="Optional skill filter",
    )

    parser.add_argument(
        "--catalog",
        default=CATALOG_PATH,
        help="Path to the saved catalog JSON file."
    )

    parser.add_argument(
        "--questions-output",
        default=GENERATED_DIR / "selected_questions.pdf",
        help="Output path for the generated questions PDF."
    )

    parser.add_argument(
        "--answers-output",
        default=GENERATED_DIR / "selected_answers.pdf",
        help="Output path for the generated answers PDF."
    )

    parser.add_argument(
        "--no-random",
        action="store_true",
        help="Use the first matching questions instead of randomly sampling."
    )

    return parser.parse_args()


def main():
    args = parse_arguments()

    catalog_path = Path(args.catalog)
    questions_output_path = Path(args.questions_output)
    answers_output_path = Path(args.answers_output)

    print(f"Loading catalog from {catalog_path}...")
    catalog = load_catalog(catalog_path)

    print("Filtering catalog...")
    filtered_catalog = filter_catalog(
        catalog,
        difficulty=args.difficulty,
        learning_area=args.learning_area,
        skill=args.skill,
    )

    print(f"Found {len(filtered_catalog)} matching questions.")

    selected_catalog = select_questions(
        filtered_catalog,
        number_of_questions=args.count,
        randomize=not args.no_random,
    )

    print(f"Selected {len(selected_catalog)} questions.")

    question_pdf_path = generate_question_pdf(selected_catalog, questions_output_path)
    answer_pdf_path = generate_answer_pdf(selected_catalog, answers_output_path)

    print("Done.")
    print(f"Questions PDF: {question_pdf_path}")
    print(f"Answers PDF: {answer_pdf_path}")


if __name__ == "__main__":
    main()