
from database import (
    add_suspect as db_add_suspect,
    get_suspects_by_case as db_get_suspects_by_case,
    update_suspect as db_update_suspect,
    delete_suspect as db_delete_suspect,
    add_statement as db_add_statement,
    get_statements_by_case as db_get_statements_by_case,
    update_statement as db_update_statement,
    delete_statement as db_delete_statement
)


# Add a new suspect to a case
def add_suspect(case_id, suspect_data):
    if not case_id or not isinstance(suspect_data, dict):
        raise ValueError("Case ID and suspect information are required.")

    if not suspect_data.get("name"):
        raise ValueError("Suspect name is required.")

    return db_add_suspect(case_id, suspect_data)


# View suspects of a specific case
def get_suspects_by_case(case_id):
    if not case_id:
        raise ValueError("Case ID is required.")

    return db_get_suspects_by_case(case_id)


# Update suspect information
def update_suspect(suspect_id, suspect_data):
    if not isinstance(suspect_data, dict) or not suspect_data:
        raise ValueError("Suspect information is required.")

    if not suspect_data.get("name"):
        raise ValueError("Suspect name is required.")

    return db_update_suspect(suspect_id, suspect_data)


# Delete a suspect
def delete_suspect(suspect_id):
    return db_delete_suspect(suspect_id)


# Add a statement and alibi for a suspect
def add_statement(suspect_id, statement_data):
    if not isinstance(statement_data, dict):
        raise TypeError("Statement data must be a dictionary.")

    if not statement_data.get("statement"):
        raise ValueError("Statement is required.")

    return db_add_statement(suspect_id, statement_data)


# View all statements of a case
def get_statements_by_case(case_id):
    if not case_id:
        raise ValueError("Case ID is required.")

    return db_get_statements_by_case(case_id)


# View statements of a specific suspect
def get_statements_by_suspect(case_id, suspect_id):
    statements = db_get_statements_by_case(case_id)

    return [
        statement for statement in statements
        if statement.get("suspect_id") == suspect_id
    ]


# Update a statement
def update_statement(statement_id, statement_data):
    if not isinstance(statement_data, dict) or not statement_data.get("statement"):
        raise ValueError("Statement is required.")

    return db_update_statement(statement_id, statement_data)


# Delete a statement
def delete_statement(statement_id):
    return db_delete_statement(statement_id)