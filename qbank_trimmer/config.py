from pathlib import Path

RW_BANK_DIR = Path("bank")
RW_SOLUTIONS_DIR = Path("solns")
MATH_BANK_DIR = RW_BANK_DIR / "math"
MATH_SOLUTIONS_DIR = RW_SOLUTIONS_DIR / "math"
GENERATED_DIR = Path("generated")

COMBINED_QUESTIONS_PATH = RW_BANK_DIR / "combined_questions.pdf"
COMBINED_SOLUTIONS_PATH = RW_SOLUTIONS_DIR / "combined_answers.pdf"
MATH_COMBINED_QUESTIONS_PATH = MATH_BANK_DIR / "math_combined_questions.pdf"
MATH_COMBINED_SOLUTIONS_PATH = MATH_SOLUTIONS_DIR / "math_combined_solutions.pdf"

CATALOG_PATH = GENERATED_DIR / "catalog.json"
CATALOG_REPORT_PATH = GENERATED_DIR / "catalog_blank_results.txt"

RW_LEARNING_AREAS = {"LA1": ["Craft and Structure", []], "LA2": ["Information and Ideas", []],
                     "LA3": ["Standard English Conventions", []], "LA4": ["Expression of Ideas", []]}

MATH_LEARNING_AREAS = {"Algebra", "Advanced Math", "Problem-Solving and Data Analysis", "Geometry and Trigonometry"}

DIFFICULTY_LEVELS = {'Easy', 'Medium', 'Hard'}
