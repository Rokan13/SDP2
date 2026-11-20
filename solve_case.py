
from database import (
    get_solution,
    update_case_status
)



#             GET CASE SOLUTION

def get_case_solution(case_id):

    return get_solution(case_id)



#              CHECK ANSWER

def check_answer(case_id, selected_suspect_id):

    solution = get_solution(case_id)

    if solution is None:
        return False

    # Solution tuple:
    # (solution_id, case_id, suspect_id, suspect_name, explanation)

    correct_suspect_id = solution[2]

    if selected_suspect_id == correct_suspect_id:

        update_case_status(case_id, "Solved")

        return True

    return False


#           GET SOLUTION RESULT

def get_solution_result(case_id):

    solution = get_solution(case_id)

    if solution is None:
        return None

    return {
        "case_id": solution[1],
        "culprit_id": solution[2],
        "culprit_name": solution[3],
        "explanation": solution[4]
    }
