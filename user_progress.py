from database import (
    update_user_progress as db_update_user_progress,
    get_user_progress as db_get_user_progress,
    get_solved_cases as db_get_solved_cases,
    get_dashboard_data as db_get_dashboard_data,
    filter_cases as db_filter_cases
)


VALID_STATUSES = ("Solved", "Unsolved")
VALID_DIFFICULTIES = ("Easy", "Medium", "Hard")


def validate_user_id(user_id):
    """Check whether user ID is a positive integer."""

    if isinstance(user_id, bool) or not isinstance(user_id, int):
        raise ValueError("User ID must be an integer.")

    if user_id <= 0:
        raise ValueError("Invalid user ID.")

    return True


def validate_case_id(case_id):
    """Check whether case ID is valid."""

    if not isinstance(case_id, str) or not case_id.strip():
        raise ValueError("Case ID is required.")

    return True


def validate_status(status):
    """Check whether case status is valid."""

    if status not in VALID_STATUSES:
        raise ValueError("Invalid case status.")

    return True


def validate_case_type(case_type):
    """Check case type if provided."""

    if case_type is not None:
        if not isinstance(case_type, str) or not case_type.strip():
            raise ValueError("Invalid case type.")

    return True


def validate_difficulty(difficulty_level):
    """Check difficulty level if provided."""

    if difficulty_level is not None:
        if difficulty_level not in VALID_DIFFICULTIES:
            raise ValueError("Invalid difficulty level.")

    return True


def update_case_status(user_id, case_id, status):
    """Update the status of a case for one user."""

    validate_user_id(user_id)
    validate_case_id(case_id)
    validate_status(status)

    case_id = case_id.strip()

    current_cases = db_get_user_progress(user_id)

    for case in current_cases:
        if case["case_id"] == case_id:

            if case["status"] == "Solved" and status == "Unsolved":
                raise ValueError("A solved case cannot become unsolved.")

            break

    return db_update_user_progress(user_id, case_id, status)


def get_user_cases(user_id):
    """Get all cases and their progress for one user."""

    validate_user_id(user_id)

    return db_get_user_progress(user_id)


def get_solved_cases(user_id):
    """Get all solved cases for one user."""

    validate_user_id(user_id)

    return db_get_solved_cases(user_id)


def get_unsolved_cases(user_id):
    """Get all unsolved cases for one user."""

    validate_user_id(user_id)

    cases = db_get_user_progress(user_id)
    unsolved_cases = []

    for case in cases:
        if case["status"] == "Unsolved":
            unsolved_cases.append(case)

    return unsolved_cases


def get_user_dashboard(user_id):
    """Get total, solved and unsolved case counts for one user."""

    validate_user_id(user_id)

    return db_get_dashboard_data(user_id)


def filter_user_cases(
    user_id,
    case_type=None,
    status=None,
    difficulty_level=None
):
    """Filter cases using one user's progress."""

    validate_user_id(user_id)
    validate_case_type(case_type)
    validate_difficulty(difficulty_level)

    if status is not None:
        validate_status(status)

    cases = db_filter_cases(
        user_id,
        case_type,
        status,
        difficulty_level
    )

    # The current database function returns the status as user_status.
    # Convert it to status so all progress functions use the same key.
    for case in cases:
        if "user_status" in case:
            case["status"] = case.pop("user_status")

    return cases
