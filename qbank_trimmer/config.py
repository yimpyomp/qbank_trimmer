from pathlib import Path

BANK_DIR = Path("bank")
SOLUTIONS_DIR = Path("solns")
GENERATED_DIR = Path("generated")

COMBINED_QUESTIONS_PATH = BANK_DIR / "combined_questions.pdf"
COMBINED_SOLUTIONS_PATH = SOLUTIONS_DIR / "combined_answers.pdf"

CATALOG_PATH = GENERATED_DIR / "catalog.json"
CATALOG_REPORT_PATH = GENERATED_DIR / "catalog_blank_results.txt"

learning_area_key = {"LA1": ["Craft and Structure", []], "LA2": ["Information and Ideas", []],
                     "LA3": ["Standard English Conventions", []], "LA4": ["Expression of Ideas", []]}
difficulty_levels = ['Easy', 'Medium', 'Hard']

