from pathlib import Path
import sys


def get_app_dir():
    if getattr(sys, "frozen", False):
        return Path(sys.executable).parent
    else:
        return Path(__file__).resolve().parent.parent


def validate_resources():
    required_files = [
        CATALOG_PATHS["rw"],
        CATALOG_PATHS["math"],
        RW_COMBINED_QUESTIONS_PATH,
        MATH_COMBINED_QUESTIONS_PATH,
        RW_COMBINED_SOLUTIONS_PATH,
        MATH_COMBINED_SOLUTIONS_PATH
    ]

    missing = [
        str(path) for path in required_files if not path.exists()
    ]

    return missing


APP_DIR = get_app_dir()

CATALOG_PATHS = {
    "rw": APP_DIR / "resources" /  "catalogs" / "rw_catalog.json",
    "math": APP_DIR / "resources" /  "catalogs" / "math_catalog.json"
}

SKILL_CATALOG_PATHS = {
    "rw": APP_DIR / "resources" /  "catalogs" / "rw_skills_catalog.json",
    "math": APP_DIR / "resources" /  "catalogs" / "math_skills_catalog.json"
}

BANK_DIR = APP_DIR / "resources" / "bank"
SOLUTIONS_DIR = APP_DIR / "resources" /  "solns"
GENERATED_DIR = APP_DIR / "generated"
GENERATED_DIR.mkdir(exist_ok=True)

RW_COMBINED_QUESTIONS_PATH = BANK_DIR / "rw_combined_questions.pdf"
RW_COMBINED_SOLUTIONS_PATH = SOLUTIONS_DIR / "rw_combined_answers.pdf"
MATH_COMBINED_QUESTIONS_PATH = BANK_DIR / "math_combined_questions.pdf"
MATH_COMBINED_SOLUTIONS_PATH = SOLUTIONS_DIR / "math_combined_answers.pdf"


CATALOG_REPORT_PATH = GENERATED_DIR / "catalog_blank_results.txt"

RW_LEARNING_AREAS = {"LA1": ["Craft and Structure", []], "LA2": ["Information and Ideas", []],
                     "LA3": ["Standard English Conventions", []], "LA4": ["Expression of Ideas", []]}

MATH_LEARNING_AREAS = {"Algebra", "Advanced Math", "Problem-Solving and Data Analysis", "Geometry and Trigonometry"}

DIFFICULTY_LEVELS = {'Easy', 'Medium', 'Hard'}
