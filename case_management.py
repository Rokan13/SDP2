
from database import (
    add_case as db_add_case,
    get_all_cases as db_get_all_cases,
    get_case_by_id as db_get_case_by_id,
    update_case as db_update_case,
    delete_case as db_delete_case,
    get_complete_case as db_get_complete_case,
    delete_solution as db_delete_solution
)


VALID_DIFFICULTIES = ("Easy", "Medium", "Hard")


def validate_case_id(case_id):
    """Check whether case ID is valid."""

    if not isinstance(case_id, str) or not case_id.strip():
        raise ValueError("Case ID is required.")

    return case_id.strip()


def validate_case_data(case_data):
    """Validate case information before saving."""

    if not isinstance(case_data, dict):
        raise ValueError("Case information must be a dictionary.")

    required_fields = (
        "case_id",
        "case_title",
        "case_type",
        "description"
    )

    for field in required_fields:
        value = case_data.get(field)

        if not isinstance(value, str) or not value.strip():
            raise ValueError(field.replace("_", " ").title() + " is required.")

    difficulty = case_data.get("difficulty_level", "Medium")

    if difficulty not in VALID_DIFFICULTIES:
        raise ValueError("Invalid difficulty level.")

    return True


def add_case(case_data):
    """Add a new case."""

    validate_case_data(case_data)

    clean_data = case_data.copy()

    for field in ("case_id", "case_title", "case_type", "description"):
        clean_data[field] = clean_data[field].strip()

    clean_data["difficulty_level"] = clean_data.get(
        "difficulty_level", "Medium"
    )

    result = db_add_case(clean_data)

    if result is None:
        raise ValueError("Case could not be added. Case ID may already exist.")

    return result


def get_all_cases():
    """Get all cases."""

    return db_get_all_cases()


def get_case_by_id(case_id):
    """Get one case using its ID."""

    case_id = validate_case_id(case_id)

    return db_get_case_by_id(case_id)


def get_case_details(case_id):
    """Get case information with suspects, statements and evidence."""

    case_id = validate_case_id(case_id)

    case_details = db_get_complete_case(case_id)

    if case_details is None:
        raise ValueError("Case does not exist.")

    return case_details


def update_case(case_id, case_data):
    """Update an existing case."""

    if not isinstance(case_data, dict):
        raise ValueError("Case data must be a dictionary.")

    case_id = validate_case_id(case_id)
    validate_case_data({
        "case_id": case_id,
        "case_title": case_data.get("case_title"),
        "case_type": case_data.get("case_type"),
        "description": case_data.get("description"),
        "difficulty_level": case_data.get("difficulty_level", "Medium")
    })

    clean_data = case_data.copy()

    for field in ("case_title", "case_type", "description"):
        clean_data[field] = clean_data[field].strip()

    clean_data["difficulty_level"] = clean_data.get(
        "difficulty_level", "Medium"
    )

    result = db_update_case(case_id, clean_data)

    if not result:
        raise ValueError("Case does not exist or could not be updated.")

    return True


def delete_case(case_id):
    """Delete a case and its solution."""

    case_id = validate_case_id(case_id)

    # Remove the solution first because its culprit uses ON DELETE RESTRICT.
    db_delete_solution(case_id)

    result = db_delete_case(case_id)

    if not result:
        raise ValueError("Case does not exist.")

    return True


def search_cases(search_text):
    """Search cases by ID, title, type, description or location."""

    if not isinstance(search_text, str):
        raise ValueError("Search text must be a string.")

    search_text = search_text.strip().lower()

    if not search_text:
        return get_all_cases()

    cases = get_all_cases()
    matched_cases = []

    searchable_fields = (
        "case_id",
        "case_title",
        "case_type",
        "description",
        "location"
    )

    for case in cases:
        for field in searchable_fields:
            value = case.get(field)

            if value and search_text in str(value).lower():
                matched_cases.append(case)
                break

    return matched_cases


def filter_cases(case_type=None, difficulty_level=None):
    """Filter cases by type and difficulty level."""

    if case_type is not None:
        if not isinstance(case_type, str) or not case_type.strip():
            raise ValueError("Invalid case type.")

    if difficulty_level is not None:
        if difficulty_level not in VALID_DIFFICULTIES:
            raise ValueError("Invalid difficulty level.")

    cases = get_all_cases()
    filtered_cases = []

    for case in cases:

        if case_type is not None:
            if case.get("case_type", "").lower() != case_type.strip().lower():
                continue

        if difficulty_level is not None:
            if case.get("difficulty_level") != difficulty_level:
                continue

        filtered_cases.append(case)

    return filtered_cases
