import re
from .config import MATH_LEARNING_AREAS, DIFFICULTY_LEVELS


DOMAIN_NAMES = [
    "Craft and Structure",
    "Information and Ideas",
    "Standard English Conventions",
    "Expression of Ideas",
    "Algebra",
    "Advanced Math",
    "Problem-Solving and Data Analysis",
    "Geometry and Trigonometry",
]

DIFFICULTY_NAMES = {"Easy", "Medium", "Hard"}


id_pattern = re.compile(r"Question\s+ID:\s*([A-Za-z0-9]+)")
answer_pattern = re.compile(r"Correct Answer:\s*([^\n\r]+)")


def clean_extracted_text(text):
    if text is None:
        return None

    return " ".join(text.split())


def extract_question_id(page_text):
    match = id_pattern.search(page_text or "")
    if match:
        return clean_extracted_text(match.group(1))
    return None


def extract_answer(page_text):
    match = answer_pattern.search(page_text or "")
    if match:
        return clean_extracted_text(match.group(1))
    return None


def extract_metadata(page_text):
    text = clean_extracted_text(page_text or "")

    # PyPDF sometimes extracts SAT as "SA T" and Test as "T est"
    text = re.sub(r"\bS\s*A\s*T\b", "SAT", text)
    text = re.sub(r"\bT\s*est\b", "Test", text)

    row_match = re.search(
        r"Assessment\s+Test\s+Domain\s+Skill\s+Difficulty\s+(.+?)\s+Question\b",
        text,
        re.IGNORECASE,
    )

    if not row_match:
        return {
            "learning_area": None,
            "skill": None,
            "difficulty": None,
        }

    row = row_match.group(1)

    # Remove the Assessment/Test cells from the row.
    row = re.sub(
        r"^SAT\s+(Math|Reading\s+and\s+Writing)\s+",
        "",
        row,
        flags=re.IGNORECASE,
    )

    difficulty = None
    for possible_difficulty in DIFFICULTY_NAMES:
        if re.search(rf"\b{possible_difficulty}\b$", row):
            difficulty = possible_difficulty
            row = re.sub(rf"\b{possible_difficulty}\b$", "", row).strip()
            break

    learning_area = None
    skill = None

    # Sort longest first so "Problem-Solving and Data Analysis" wins
    # before any shorter accidental partial match.
    for possible_domain in sorted(DOMAIN_NAMES, key=len, reverse=True):
        if row.startswith(possible_domain):
            learning_area = possible_domain
            skill = row[len(possible_domain):].strip()
            break

    return {
        "learning_area": learning_area,
        "skill": skill,
        "difficulty": difficulty,
    }


def extract_learning_area(page_text):
    return extract_metadata(page_text)["learning_area"]


def extract_skill(page_text):
    return extract_metadata(page_text)["skill"]


def extract_question_difficulty(page_text):
    return extract_metadata(page_text)["difficulty"]


def repair_difficulty(skill, difficulty):
    if difficulty in DIFFICULTY_LEVELS:
        return skill, difficulty

    if not skill:
        return skill, difficulty

    skill_words = skill.split()

    matches = []
    for word in skill_words:
        if word in DIFFICULTY_LEVELS:
            matches.append(word)

    if len(matches) == 1:
        repaired_difficulty = matches[0]
        repaired_skill = " ".join(word for word in skill_words if word != repaired_difficulty)
        return repaired_skill, repaired_difficulty

    else:
        return skill, difficulty




