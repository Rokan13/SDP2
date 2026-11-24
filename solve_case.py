
from database import (
    add_solution as db_add_solution,
    get_solution as db_get_solution,
    update_solution as db_update_solution,
    delete_solution as db_delete_solution,
    get_case_by_id,
    get_suspects_by_case
)

from user_progress import (
    update_case_status,
    validate_user_id
)


def validate_solution(case_id, culprit_id, explanation):
    """Validate solution information."""

    if not isinstance(case_id, str) or not case_id.strip():
        raise ValueError("Case ID is required.")

    if isinstance(culprit_id, bool) or not isinstance(culprit_id, int):
        raise ValueError("Culprit ID must be an integer.")

    if culprit_id <= 0:
        raise ValueError("Invalid culprit ID.")

    if not isinstance(explanation, str) or not explanation.strip():
        raise ValueError("Solution explanation is required.")

    case_id = case_id.strip()

    case = get_case_by_id(case_id)

    if case is None:
        raise ValueError("Case does not exist.")

    suspects = get_suspects_by_case(case_id)

    culprit_found = False

    for suspect in suspects:
        if suspect["suspect_id"] == culprit_id:
            culprit_found = True
            break

    if not culprit_found:
        raise ValueError("Selected culprit does not belong to this case.")

    return True


def add_solution(case_id, culprit_id, explanation):
    """Add a solution for a case."""

    validate_solution(case_id, culprit_id, explanation)

    case_id = case_id.strip()

    existing_solution = db_get_solution(case_id)

    if existing_solution is not None:
        raise ValueError("A solution already exists for this case.")

    result = db_add_solution(
        case_id,
        culprit_id,
        explanation.strip()
    )

    if result is None:
        raise ValueError("Solution could not be added.")

    return result


def get_solution(case_id):
    """Get solution when the application is ready to reveal it."""

    if not isinstance(case_id, str) or not case_id.strip():
        raise ValueError("Case ID is required.")

    return db_get_solution(case_id.strip())


def update_solution(case_id, culprit_id, explanation):
    """Update an existing case solution."""

    validate_solution(case_id, culprit_id, explanation)

    case_id = case_id.strip()

    existing_solution = db_get_solution(case_id)

    if existing_solution is None:
        raise ValueError("Solution does not exist.")

    result = db_update_solution(
        case_id,
        culprit_id,
        explanation.strip()
    )

    if not result:
        raise ValueError("Solution could not be updated.")

    return True


def delete_solution(case_id):
    """Delete a case solution."""

    if not isinstance(case_id, str) or not case_id.strip():
        raise ValueError("Case ID is required.")

    result = db_delete_solution(case_id.strip())

    if not result:
        raise ValueError("Solution does not exist.")

    return True


def check_answer(case_id, selected_suspect_id):
    """Check whether the selected suspect is the actual culprit."""

    if not isinstance(case_id, str) or not case_id.strip():
        raise ValueError("Case ID is required.")

    if isinstance(selected_suspect_id, bool):
        raise ValueError("Invalid suspect ID.")

    if not isinstance(selected_suspect_id, int):
        raise ValueError("Suspect ID must be an integer.")

    if selected_suspect_id <= 0:
        raise ValueError("Invalid suspect ID.")

    case_id = case_id.strip()

    case = get_case_by_id(case_id)

    if case is None:
        raise ValueError("Case does not exist.")

    suspects = get_suspects_by_case(case_id)

    suspect_found = False

    for suspect in suspects:
        if suspect["suspect_id"] == selected_suspect_id:
            suspect_found = True
            break

    if not suspect_found:
        raise ValueError("Selected suspect does not belong to this case.")

    solution = db_get_solution(case_id)

    if solution is None:
        raise ValueError("Solution has not been added for this case.")

    is_correct = selected_suspect_id == solution["culprit_id"]

    return {
        "is_correct": is_correct,
        "culprit_id": solution["culprit_id"],
        "culprit_name": solution["culprit_name"],
        "explanation": solution["explanation"]
    }


def submit_case_answer(user_id, case_id, selected_suspect_id):
    """Check the answer and update progress if it is correct."""

    validate_user_id(user_id)

    result = check_answer(case_id, selected_suspect_id)

    if result["is_correct"]:
        update_case_status(user_id, case_id, "Solved")

    return result
