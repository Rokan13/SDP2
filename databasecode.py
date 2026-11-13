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

# =====================================
# CASE MANAGEMENT
# =====================================
def add_case(case_title, case_type, description, location, incident_date):
    conn = connect_db()
    cursor = conn.cursor()
    cursor.execute("""
        INSERT INTO cases (case_title, case_type, description, location, incident_date)
        VALUES (?, ?, ?, ?, ?)
    """, (case_title, case_type, description, location, incident_date))
    conn.commit()
    last_id = cursor.lastrowid
    conn.close()
    return last_id

def get_all_cases():
    conn = connect_db()
    cursor = conn.cursor()
    cursor.execute("SELECT * FROM cases")
    cases = cursor.fetchall()
    conn.close()
    return cases 

def update_case(case_id, case_title, case_type, description, location, incident_date):
    conn = connect_db()
    cursor = conn.cursor()
    cursor.execute("""
        UPDATE cases
        SET case_title = ?, case_type = ?, description = ?, location = ?, incident_date = ?
        WHERE case_id = ?
    """, (case_title, case_type, description, location, incident_date, case_id))
    conn.commit()
    conn.close()

def delete_case(case_id):
    conn = connect_db()
    cursor = conn.cursor()
    cursor.execute("DELETE FROM cases WHERE case_id = ?", (case_id,))
    conn.commit()
    conn.close()

# =====================================
# SUSPECT MANAGEMENT
# =====================================
def add_suspect(case_id, suspect_name, age, occupation, address):
    conn = connect_db()
    cursor = conn.cursor()
    cursor.execute("""
        INSERT INTO suspects (case_id, suspect_name, age, occupation, address)
        VALUES (?, ?, ?, ?, ?)
    """, (case_id, suspect_name, age, occupation, address))
    conn.commit()
    last_id = cursor.lastrowid
    conn.close()
    return last_id

def get_all_suspects(case_id):
    conn = connect_db()
    cursor = conn.cursor()
    cursor.execute("SELECT * FROM suspects WHERE case_id = ?", (case_id,))
    suspects = cursor.fetchall()
    conn.close()
    return suspects

def update_suspect(suspect_id, suspect_name, age, occupation, address):
    conn = connect_db()
    cursor = conn.cursor()
    cursor.execute("""
        UPDATE suspects
        SET suspect_name = ?, age = ?, occupation = ?, address = ?
        WHERE suspect_id = ?
    """, (suspect_name, age, occupation, address, suspect_id))
    conn.commit()
    conn.close()

def delete_suspect(suspect_id):
    conn = connect_db()
    cursor = conn.cursor()
    cursor.execute("DELETE FROM suspects WHERE suspect_id = ?", (suspect_id,))
    conn.commit()
    conn.close()

# =====================================
# EVIDENCE MANAGEMENT
# =====================================
def add_evidence(case_id, evidence_name, evidence_type, description, collected_date):
    conn = connect_db()
    cursor = conn.cursor()
    cursor.execute("""
        INSERT INTO evidence (case_id, evidence_name, evidence_type, description, collected_date)
        VALUES (?, ?, ?, ?, ?)
    """, (case_id, evidence_name, evidence_type, description, collected_date))
    conn.commit()
    conn.close()

def get_all_evidence(case_id):
    conn = connect_db()
    cursor = conn.cursor()
    cursor.execute("SELECT * FROM evidence WHERE case_id = ?", (case_id,))
    evidence = cursor.fetchall()
    conn.close()
    return evidence

def update_evidence(evidence_id, evidence_name, evidence_type, description, collected_date):
    conn = connect_db()
    cursor = conn.cursor()
    cursor.execute("""
        UPDATE evidence
        SET evidence_name = ?, evidence_type = ?, description = ?, collected_date = ?
        WHERE evidence_id = ?
    """, (evidence_name, evidence_type, description, collected_date, evidence_id))
    conn.commit()
    conn.close()

def delete_evidence(evidence_id):
    conn = connect_db()
    cursor = conn.cursor()
    cursor.execute("DELETE FROM evidence WHERE evidence_id = ?", (evidence_id,))
    conn.commit()
    conn.close()

# =====================================
# STATEMENT MANAGEMENT
# =====================================
def add_statement(case_id, suspect_id, statement_text, alibi, statement_date):
    conn = connect_db()
    cursor = conn.cursor()
    cursor.execute("""
        INSERT INTO statements (case_id, suspect_id, statement_text, alibi, statement_date)
        VALUES (?, ?, ?, ?, ?)
    """, (case_id, suspect_id, statement_text, alibi, statement_date))
    conn.commit()
    conn.close()

def get_all_statements(case_id):
    conn = connect_db()
    cursor = conn.cursor()
    cursor.execute("SELECT * FROM statements WHERE case_id = ?", (case_id,))
    statements = cursor.fetchall()
    conn.close()
    return statements

def update_statement(statement_id, statement_text, alibi, statement_date):
    conn = connect_db()
    cursor = conn.cursor()
    cursor.execute("""
        UPDATE statements
        SET statement_text = ?, alibi = ?, statement_date = ?
        WHERE statement_id = ?
    """, (statement_text, alibi, statement_date, statement_id))
    conn.commit()
    conn.close()

def delete_statement(statement_id):
    conn = connect_db()
    cursor = conn.cursor()
    cursor.execute("DELETE FROM statements WHERE statement_id = ?", (statement_id,))
    conn.commit()
    conn.close()

# =====================================
# CASE SOLUTION
# =====================================
def add_solution(case_id, real_culprit_id, explanation):
    conn = connect_db()
    cursor = conn.cursor()
    cursor.execute("""
        INSERT INTO case_solutions (case_id, real_culprit_id, explanation)
        VALUES (?, ?, ?)
    """, (case_id, real_culprit_id, explanation))
    conn.commit()
    conn.close()

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
        JOIN suspects ON case_solutions.real_culprit_id = suspects.suspect_id
        WHERE case_solutions.case_id = ?
    """, (case_id,))
    solution = cursor.fetchone()
    conn.close()
    return solution

# ডেমো বা স্যাম্পল কেস ডাটা ইনসার্ট করার ফাংশন
def seed_initial_data():
    conn = connect_db()
    cursor = conn.cursor()
    cursor.execute("SELECT COUNT(*) FROM cases")
    count = cursor.fetchone()[0]
    conn.close()

    # যদি ডাটাবেজে কোনো কেস না থাকে, তবে ডেমো কেস ইনসার্ট করবে
    if count == 0:
        # কেস ১
        c1_id = add_case(
            "The Missing Diamond", 
            "Theft", 
            "A rare diamond was stolen from the city museum during midnight.", 
            "City Museum, Dhaka", 
            "2026-10-15"
        )
        s1_id = add_suspect(c1_id, "Mr. David", 35, "Security Guard", "Gulshan, Dhaka")
        s2_id = add_suspect(c1_id, "Mr. Rahim", 40, "Cleaner", "Mirpur, Dhaka")
        
        add_statement(c1_id, s1_id, "I was on duty at the main gate.", "Claimed to be patrolling outside.", "2026-10-15")
        add_statement(c1_id, s2_id, "I was cleaning the second floor gallery.", "Claimed to be inside the cleaning closet.", "2026-10-15")
        
        add_evidence(c1_id, "Broken Glass", "Physical", "Found near the display case.", "2026-10-16")
        add_evidence(c1_id, "Security Badge", "Digital", "Found dropped near the back door belonging to Mr. David.", "2026-10-16")
        
        add_solution(c1_id, s1_id, "Mr. David used his security access to bypass alarms and dropped his badge at the crime scene.")

        # কেস ২
        c2_id = add_case(
            "The Cyber Breach", 
            "Cybercrime", 
            "Confidential bank database files were illegally accessed and downloaded.", 
            "Tech Park, Motijheel", 
            "2026-11-01"
        )
        s3_id = add_suspect(c2_id, "Alex", 28, "Software Engineer", "Dhanmondi, Dhaka")
        s4_id = add_suspect(c2_id, "Nusrat", 26, "System Admin", "Uttara, Dhaka")

        add_statement(c2_id, s3_id, "I left my office at 5 PM sharp.", "Was at a coffee shop.", "2026-11-01")
        add_statement(c2_id, s4_id, "I was troubleshooting server logs all night.", "In the server room.", "2026-11-01")

        add_evidence(c2_id, "IP Log", "Digital", "Traced to Alex's personal laptop MAC address.", "2026-11-02")
        
        add_solution(c2_id, s3_id, "Alex used a backdoor script to steal the files after hours, leaving behind his unique device IP.")

        print("Sample/Demo cases added successfully!")

if __name__ == "__main__":
    create_tables()
    seed_initial_data()
    print("Database is fully ready with sample cases!")