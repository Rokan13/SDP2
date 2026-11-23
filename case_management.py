
from database import (
    add_case as db_add_case,
    get_all_cases as db_get_all_cases,
    get_case_by_id as db_get_case_by_id,
    update_case as db_update_case,
    delete_case as db_delete_case,
    get_complete_case as db_get_complete_case
)


# Required fields for a case
REQUIRED_CASE_FIELDS = [
    "case_id",
    "case_title",
    "case_type",
    "description",
    "difficulty_level"
]

# Valid difficulty levels
VALID_DIFFICULTIES = ["Easy", "Medium", "Hard"]


def validate_case_data(case_data):
    """Check whether case information is valid."""

    if not isinstance(case_data, dict):
        raise TypeError("Case data must be a dictionary.")

    for field in REQUIRED_CASE_FIELDS:
        value = case_data.get(field)

        if value is None or str(value).strip() == "":
            raise ValueError(field + " is required.")

    difficulty = case_data["difficulty_level"]

    if difficulty not in VALID_DIFFICULTIES:
        raise ValueError("Difficulty must be Easy, Medium or Hard.")


def create_case(case_data):
    """Create a new case."""

    validate_case_data(case_data)

    return db_add_case(case_data)


def get_all_cases():
    """Get all cases from the database."""

    return db_get_all_cases()


def get_case_details(case_id):
    """Get complete case information without revealing the solution."""

    if not isinstance(case_id, str) or case_id.strip() == "":
        raise ValueError("Case ID is required.")

    return db_get_complete_case(case_id)


def update_case(case_id, case_data):
    """Update an existing case."""

    if not isinstance(case_id, str) or case_id.strip() == "":
        raise ValueError("Case ID is required.")

    if not isinstance(case_data, dict) or len(case_data) == 0:
        raise ValueError("Case update data is required.")

    # Get the existing case
    old_case = db_get_case_by_id(case_id)

    if old_case is None:
        return False

    # Copy the existing case information
    updated_data = old_case.copy()

    # Add the new information
    for field in case_data:
        updated_data[field] = case_data[field]

    # Check required text fields
    fields = ["case_title", "case_type", "description"]

    for field in fields:
        value = updated_data.get(field)

        if not isinstance(value, str) or value.strip() == "":
            raise ValueError(field + " cannot be empty.")

    # Check difficulty level
    if updated_data["difficulty_level"] not in VALID_DIFFICULTIES:
        raise ValueError("Invalid difficulty level.")

    return db_update_case(case_id, updated_data)


def delete_case(case_id):
    """Delete a case."""

    if not isinstance(case_id, str) or case_id.strip() == "":
        raise ValueError("Case ID is required.")

    return db_delete_case(case_id)


def search_cases(keyword):
    """Search cases by title, ID, type, location or description."""

    if not isinstance(keyword, str) or keyword.strip() == "":
        return []

    keyword = keyword.strip().lower()

    cases = db_get_all_cases()
    matched_cases = []

    search_fields = [
        "case_id",
        "case_title",
        "case_type",
        "description",
        "location"
    ]

    for case in cases:
        for field in search_fields:
            value = str(case.get(field) or "").lower()

            if keyword in value:
                matched_cases.append(case)
                break

    return matched_cases


def filter_cases(case_type=None, difficulty_level=None):
    """Filter cases by type and difficulty level."""

    if difficulty_level:
        if difficulty_level not in VALID_DIFFICULTIES:
            raise ValueError("Invalid difficulty level.")

    cases = db_get_all_cases()
    filtered_cases = []

    for case in cases:

        # Check case type
        if case_type:
            current_type = str(case.get("case_type") or "").lower()

            if current_type != case_type.lower():
                continue

        # Check difficulty level
        if difficulty_level:
            if case.get("difficulty_level") != difficulty_level:
                continue

        filtered_cases.append(case)

    return filtered_cases
