
from database import (
    update_user_progress as db_update_user_progress,
    get_user_progress as db_get_user_progress,
    get_solved_cases as db_get_solved_cases,
    get_dashboard_data as db_get_dashboard_data,
    filter_cases as db_filter_cases
)


VALID_STATUSES = ["Solved", "Unsolved"]
VALID_DIFFICULTIES = ["Easy", "Medium", "Hard"]


def validate_user_id(user_id):
    """Validate user ID."""

    if not isinstance(user_id, int) or isinstance(user_id, bool):
        raise TypeError("User ID must be an integer.")

    if user_id <= 0:
        raise ValueError("User ID must be greater than zero.")


def validate_case_id(case_id):
    """Validate case ID."""

    if not isinstance(case_id, str):
        raise TypeError("Case ID must be a string.")

    if case_id.strip() == "":
        raise ValueError("Case ID is required.")


def validate_status(status):
    """Validate case status."""

    if status not in VALID_STATUSES:
        raise ValueError("Status must be Solved or Unsolved.")


def update_case_status(user_id, case_id, status):
    """Update a user's case progress."""

    validate_user_id(user_id)
    validate_case_id(case_id)
    validate_status(status)

    return db_update_user_progress(
        user_id,
        case_id.strip(),
        status
    )


def get_user_cases(user_id):
    """Get all cases with the user's progress."""

    validate_user_id(user_id)

    return db_get_user_progress(user_id)


def get_solved_cases(user_id):
    """Get all solved cases of a user."""

    validate_user_id(user_id)

    return db_get_solved_cases(user_id)


def get_unsolved_cases(user_id):
    """Get all unsolved cases of a user."""

    validate_user_id(user_id)

    cases = db_get_user_progress(user_id)

    unsolved_cases = []

    for case in cases:
        if case["status"] == "Unsolved":
            unsolved_cases.append(case)

    return unsolved_cases


def get_user_dashboard(user_id):
    """Get dashboard counts for a user."""

    validate_user_id(user_id)

    return db_get_dashboard_data(user_id)


def filter_user_cases(
    user_id,
    case_type=None,
    status=None,
    difficulty_level=None
):
    """Filter a user's cases."""

    validate_user_id(user_id)

    if case_type is not None:
        if not isinstance(case_type, str) or case_type.strip() == "":
            raise ValueError("Invalid case type.")

    if status is not None:
        validate_status(status)

    if difficulty_level is not None:
        if difficulty_level not in VALID_DIFFICULTIES:
            raise ValueError("Invalid difficulty level.")

    return db_filter_cases(
        user_id,
        case_type,
        status,
        difficulty_level
    )
