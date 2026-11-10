from database import (
    add_evidence,
    get_all_evidence,
    update_evidence,
    delete_evidence
)

def add_new_evidence(case_id, evidence_name, evidence_type,
                     description, collected_date):

    add_evidence(
        case_id,
        evidence_name,
        evidence_type,
        description,
        collected_date
    )