import argparse
from pathlib import Path
from qbank_trimmer.config import CATALOG_PATHS, GENERATED_DIR
from app import generate_questions, create_catalog


def parse_arguments():
    parser = argparse.ArgumentParser(
        description="Generate custom collections of SAT questions"
    )

    parser.add_argument(
        "-s",
        "--subject",
        choices={"rw", "math"},
        required=True,
        help="Subject to generate questions for"
    )

    parser.add_argument(
        "-c",
        "--count",
        type=int,
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
        "-k",
        "--skill",
        # TODO: Add list of options
        help="Optional skill filter",
    )

    parser.add_argument(
        "--catalog-path",
        help="Optional override path to a saved catalog.json."
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

    parser.add_argument(
        "--generate-catalog",
        action="store_true",
        help="Generate a new catalog from the provided question and answer PDFs."
    )

    parser.add_argument(
        "--questions-source",
        default="bank/combined_questions.pdf",
        help="Path to the combined blank-question PDF."
    )

    parser.add_argument(
        "--answers-source",
        default="solns/combined_answers.pdf",
        help="Path to the combined answer PDF."
    )

    parser.add_argument(
        "--catalog-only",
        help="Generate catalogs only",
        action="store_true"
    )


    return parser.parse_args()


def main():
    args = parse_arguments()

    settings = {"subject": args.subject,
                "count": args.count,
                "difficulty": args.difficulty,
                "learning_area": args.learning_area,
                "skill": args.skill,

                "catalog_path": args.catalog_path,

                "questions_output": Path(args.questions_output),
                "answers_output": Path(args.answers_output)
                }

    if args.generate_catalog:
        print(f"Generating catalog...")
        catalog_file = create_catalog(settings)

        print(f"Catalog saved to {catalog_file}")

        if args.catalog_only:
            return

    print("Generating questions...")
    generate_questions(settings)
    print("Done")


if __name__ == "__main__":
    main()