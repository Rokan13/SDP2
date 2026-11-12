import sqlite3

def connect_db():
    conn = sqlite3.connect("caseclosed.db")
    conn.execute("PRAGMA foreign_keys = ON")
    return conn

def create_tables():
    conn = connect_db()
    cursor = conn.cursor()

    # 1. Cases Table
    cursor.execute("""
        CREATE TABLE IF NOT EXISTS cases (
            case_id INTEGER PRIMARY KEY AUTOINCREMENT,
            case_title TEXT NOT NULL,
            case_type TEXT,
            description TEXT,
            location TEXT,
            incident_date TEXT,
            status TEXT DEFAULT 'Unsolved'
        )
    """)

    # 2. Suspects Table
    cursor.execute("""
        CREATE TABLE IF NOT EXISTS suspects (
            suspect_id INTEGER PRIMARY KEY AUTOINCREMENT,
            case_id INTEGER,
            suspect_name TEXT NOT NULL,
            age INTEGER,
            occupation TEXT,
            address TEXT,
            FOREIGN KEY (case_id) REFERENCES cases(case_id)
            ON DELETE CASCADE
        )
    """)

    # 3. Statements Table
    cursor.execute("""
        CREATE TABLE IF NOT EXISTS statements (
            statement_id INTEGER PRIMARY KEY AUTOINCREMENT,
            case_id INTEGER,
            suspect_id INTEGER,
            statement_text TEXT,
            alibi TEXT,
            statement_date TEXT,
            FOREIGN KEY (case_id) REFERENCES cases(case_id)
            ON DELETE CASCADE,
            FOREIGN KEY (suspect_id) REFERENCES suspects(suspect_id)
            ON DELETE CASCADE
        )
    """)

    # 4. Evidence Table
    cursor.execute("""
        CREATE TABLE IF NOT EXISTS evidence (
            evidence_id INTEGER PRIMARY KEY AUTOINCREMENT,
            case_id INTEGER,
            evidence_name TEXT NOT NULL,
            evidence_type TEXT,
            description TEXT,
            collected_date TEXT,
            FOREIGN KEY (case_id) REFERENCES cases(case_id)
            ON DELETE CASCADE
        )
    """)

    # 5. Case Solutions Table

    cursor.execute("""
    CREATE TABLE IF NOT EXISTS case_solutions (
        solution_id INTEGER PRIMARY KEY AUTOINCREMENT,
        case_id INTEGER UNIQUE,
        real_culprit_id INTEGER,
        explanation TEXT NOT NULL,
        FOREIGN KEY (case_id) REFERENCES cases(case_id)
        ON DELETE CASCADE,
        FOREIGN KEY (real_culprit_id) REFERENCES suspects(suspect_id)
        ON DELETE CASCADE
    )
    """)
    conn.commit()
    conn.close()

# Add Case Method
def add_case(case_title, case_type, description, location, incident_date):
    conn = connect_db()
    cursor = conn.cursor()

    cursor.execute("""
        INSERT INTO cases (
            case_title,
            case_type,
            description,
            location,
            incident_date
        )
        VALUES (?, ?, ?, ?, ?)
    """, (case_title, case_type, description, location, incident_date))

    conn.commit()
    conn.close()

    print("New Case Added Successfully!")

# View Cases Method
def get_all_cases():
    conn = connect_db()
    cursor = conn.cursor()

    cursor.execute("SELECT * FROM cases")
    cases = cursor.fetchall()

    conn.close()
    return cases 

# Update Case Method
def update_case(case_id, case_title, case_type, description, location, incident_date):
    conn = connect_db()
    cursor = conn.cursor()

    cursor.execute("""
        UPDATE cases
        SET case_title = ?,
            case_type = ?,
            description = ?,
            location = ?,
            incident_date = ?
        WHERE case_id = ?
    """, (case_title, case_type, description, location, incident_date, case_id))

    conn.commit()
    conn.close()

    print("Case Updated Successfully!")

# Delete Case Method
def delete_case(case_id):
    conn = connect_db()
    cursor = conn.cursor()

    cursor.execute(
        "DELETE FROM cases WHERE case_id = ?",
        (case_id,)
    )

    conn.commit()
    conn.close()

    print("Case Deleted Successfully!")

# Add Suspect Method
def add_suspect(case_id, suspect_name, age, occupation, address):
    conn = connect_db()
    cursor = conn.cursor()

    cursor.execute("""
        INSERT INTO suspects (
            case_id,
            suspect_name,
            age,
            occupation,
            address
        )
        VALUES (?, ?, ?, ?, ?)
    """, (case_id, suspect_name, age, occupation, address))

    conn.commit()
    conn.close()

    print("Suspect Added Successfully!")

# View Suspects Method
def get_all_suspects(case_id):
    conn = connect_db()
    cursor = conn.cursor()

    cursor.execute(
        "SELECT * FROM suspects WHERE case_id = ?",
        (case_id,)
    )

    suspects = cursor.fetchall()

    conn.close()
    return suspects

# Update Suspect Method
def update_suspect(suspect_id, suspect_name, age, occupation, address):
    conn = connect_db()
    cursor = conn.cursor()

    cursor.execute("""
        UPDATE suspects
        SET suspect_name = ?,
            age = ?,
            occupation = ?,
            address = ?
        WHERE suspect_id = ?
    """, (suspect_name, age, occupation, address, suspect_id))

    conn.commit()
    conn.close()

    print("Suspect Updated Successfully!")

# Delete Suspect Method
def delete_suspect(suspect_id):
    conn = connect_db()
    cursor = conn.cursor()

    cursor.execute(
        "DELETE FROM suspects WHERE suspect_id = ?",
        (suspect_id,)
    )

    conn.commit()
    conn.close()

    print("Suspect Deleted Successfully!")

    # Add Evidence Method
def add_evidence(case_id, evidence_name, evidence_type, description, collected_date):
    conn = connect_db()
    cursor = conn.cursor()

    cursor.execute("""
        INSERT INTO evidence (
            case_id,
            evidence_name,
            evidence_type,
            description,
            collected_date
        )
        VALUES (?, ?, ?, ?, ?)
    """, (case_id, evidence_name, evidence_type, description, collected_date))

    conn.commit()
    conn.close()

    print("Evidence Added Successfully!")

# View Evidence Method
def get_all_evidence(case_id):
    conn = connect_db()
    cursor = conn.cursor()

    cursor.execute(
        "SELECT * FROM evidence WHERE case_id = ?",
        (case_id,)
    )

    evidence = cursor.fetchall()

    conn.close()
    return evidence

# Update Evidence Method
def update_evidence(evidence_id, evidence_name, evidence_type, description, collected_date):
    conn = connect_db()
    cursor = conn.cursor()

    cursor.execute("""
        UPDATE evidence
        SET evidence_name = ?,
            evidence_type = ?,
            description = ?,
            collected_date = ?
        WHERE evidence_id = ?
    """, (evidence_name, evidence_type, description, collected_date, evidence_id))

    conn.commit()
    conn.close()

    print("Evidence Updated Successfully!")

# Delete Evidence Method
def delete_evidence(evidence_id):
    conn = connect_db()
    cursor = conn.cursor()

    cursor.execute(
        "DELETE FROM evidence WHERE evidence_id = ?",
        (evidence_id,)
    )

    conn.commit()
    conn.close()

    print("Evidence Deleted Successfully!")

    # =====================================
# STATEMENT MANAGEMENT
# =====================================

# Add Statement Method
def add_statement(case_id, suspect_id, statement_text, alibi, statement_date):
    conn = connect_db()
    cursor = conn.cursor()

    cursor.execute("""
        INSERT INTO statements (
            case_id,
            suspect_id,
            statement_text,
            alibi,
            statement_date
        )
        VALUES (?, ?, ?, ?, ?)
    """, (case_id, suspect_id, statement_text, alibi, statement_date))

    conn.commit()
    conn.close()

    print("Statement Added Successfully!")

# View Statements Method
def get_all_statements(case_id):
    conn = connect_db()
    cursor = conn.cursor()

    cursor.execute(
        "SELECT * FROM statements WHERE case_id = ?",
        (case_id,)
    )

    statements = cursor.fetchall()

    conn.close()
    return statements

# Update Statement Method
def update_statement(statement_id, statement_text, alibi, statement_date):
    conn = connect_db()
    cursor = conn.cursor()

    cursor.execute("""
        UPDATE statements
        SET statement_text = ?,
            alibi = ?,
            statement_date = ?
        WHERE statement_id = ?
    """, (statement_text, alibi, statement_date, statement_id))

    conn.commit()
    conn.close()

    print("Statement Updated Successfully!")

# Delete Statement Method
def delete_statement(statement_id):
    conn = connect_db()
    cursor = conn.cursor()

    cursor.execute(
        "DELETE FROM statements WHERE statement_id = ?",
        (statement_id,)
    )

    conn.commit()
    conn.close()

    print("Statement Deleted Successfully!")

# CASE SOLUTION

# Add Case Solution Method
def add_solution(case_id, real_culprit_id, explanation):
    conn = connect_db()
    cursor = conn.cursor()

    cursor.execute("""
        INSERT INTO case_solutions (
            case_id,
            real_culprit_id,
            explanation
        )
        VALUES (?, ?, ?)
    """, (case_id, real_culprit_id, explanation))

    conn.commit()
    conn.close()

    print("Case Solution Added Successfully!")

    # View Case Solution Method
def get_solution(case_id):
    conn = connect_db()
    cursor = conn.cursor()

    cursor.execute("""
        SELECT
            case_solutions.solution_id,
            case_solutions.case_id,
            suspects.suspect_id,
            suspects.suspect_name,
            case_solutions.explanation
        FROM case_solutions
        JOIN suspects
        ON case_solutions.real_culprit_id = suspects.suspect_id
        WHERE case_solutions.case_id = ?
    """, (case_id,))

    solution = cursor.fetchone()

    conn.close()
    return solution

if __name__ == "__main__":
    create_tables()

    # Create Test Case
    add_case(
        "Final Test Case",
        "Investigation",
        "Testing statement and report.",
        "Dhaka",
        "2026-11-04"
    )

    cases = get_all_cases()
    case_id = cases[-1][0]

    # Create Test Suspect
    add_suspect(
        case_id,
        "David",
        28,
        "Teacher",
        "Dhaka"
    )

    suspects = get_all_suspects(case_id)
    suspect_id = suspects[-1][0]

    # =================================
    # TEST STATEMENT METHODS
    # =================================

    add_statement(
        case_id,
        suspect_id,
        "I was at home.",
        "Stayed at home during the incident.",
        "2026-11-04"
    )

    statements = get_all_statements(case_id)
    statement_id = statements[-1][0]

    print("Statements:", statements)

    update_statement(
        statement_id,
        "I was at work.",
        "Was at the office during the incident.",
        "2026-11-04"
    )

    print("Updated Statements:", get_all_statements(case_id))

    delete_statement(statement_id)

    print("Remaining Statements:", get_all_statements(case_id))

    # =================================
    # TEST CASE SOLUTION METHODS
    # =================================

    add_solution(
    case_id,
    suspect_id,
    "David had access to the location and the evidence connects him to the crime."
    )

    solution = get_solution(case_id)

    print("Case Solution:", solution)
    

