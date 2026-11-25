import sqlite3
from contextlib import contextmanager
from pathlib import Path

DB_PATH = Path(__file__).resolve().parent / "caseclosed.db"


def connect_db() -> sqlite3.Connection:
    """Open a SQLite connection and enable foreign-key checks."""
    connection = sqlite3.connect(DB_PATH)
    connection.row_factory = sqlite3.Row
    connection.execute("PRAGMA foreign_keys = ON")
    return connection


@contextmanager
def db_connection():
    """Commit on success; roll back on error; always close the connection."""
    connection = connect_db()
    try:
        yield connection
        connection.commit()
    except Exception:
        connection.rollback()
        raise
    finally:
        connection.close()


def _row_to_dict(row):
    return dict(row) if row is not None else None


def _rows_to_dicts(rows):
    return [dict(row) for row in rows]


def create_tables() -> None:
    """Create all seven project tables."""
    with db_connection() as conn:
        conn.executescript("""
            CREATE TABLE IF NOT EXISTS users (
                user_id INTEGER PRIMARY KEY AUTOINCREMENT,
                username TEXT NOT NULL UNIQUE COLLATE NOCASE,
                email TEXT NOT NULL UNIQUE COLLATE NOCASE,
                password_hash TEXT NOT NULL,
                role TEXT NOT NULL DEFAULT 'user'
                    CHECK (role IN ('admin', 'user'))
            );

            CREATE TABLE IF NOT EXISTS cases (
                case_id TEXT PRIMARY KEY,
                case_title TEXT NOT NULL,
                case_type TEXT NOT NULL,
                description TEXT NOT NULL,
                location TEXT,
                incident_date TEXT,
                difficulty_level TEXT NOT NULL DEFAULT 'Medium'
            );

            CREATE TABLE IF NOT EXISTS suspects (
                suspect_id INTEGER PRIMARY KEY AUTOINCREMENT,
                case_id TEXT NOT NULL,
                name TEXT NOT NULL,
                age INTEGER,
                occupation TEXT,
                address TEXT,
                FOREIGN KEY (case_id) REFERENCES cases(case_id)
                    ON UPDATE CASCADE ON DELETE CASCADE
            );

            CREATE TABLE IF NOT EXISTS statements (
                statement_id INTEGER PRIMARY KEY AUTOINCREMENT,
                suspect_id INTEGER NOT NULL,
                statement TEXT NOT NULL,
                alibi TEXT,
                statement_date TEXT,
                FOREIGN KEY (suspect_id) REFERENCES suspects(suspect_id)
                    ON UPDATE CASCADE ON DELETE CASCADE
            );

            CREATE TABLE IF NOT EXISTS evidence (
                evidence_id INTEGER PRIMARY KEY AUTOINCREMENT,
                case_id TEXT NOT NULL,
                evidence_name TEXT NOT NULL,
                evidence_type TEXT,
                description TEXT,
                collected_date TEXT,
                FOREIGN KEY (case_id) REFERENCES cases(case_id)
                    ON UPDATE CASCADE ON DELETE CASCADE
            );

            CREATE TABLE IF NOT EXISTS case_solutions (
                solution_id INTEGER PRIMARY KEY AUTOINCREMENT,
                case_id TEXT NOT NULL UNIQUE,
                culprit_id INTEGER NOT NULL,
                explanation TEXT NOT NULL,
                FOREIGN KEY (case_id) REFERENCES cases(case_id)
                    ON UPDATE CASCADE ON DELETE CASCADE,
                FOREIGN KEY (culprit_id) REFERENCES suspects(suspect_id)
                    ON UPDATE CASCADE ON DELETE RESTRICT
            );

            CREATE TABLE IF NOT EXISTS user_case_progress (
                progress_id INTEGER PRIMARY KEY AUTOINCREMENT,

                user_id INTEGER NOT NULL,
                case_id TEXT NOT NULL,

                status TEXT NOT NULL DEFAULT 'Unsolved'
                CHECK (status IN ('Unsolved', 'Solved')),

                updated_at TEXT DEFAULT CURRENT_TIMESTAMP,

                UNIQUE(user_id, case_id),

                FOREIGN KEY (user_id) REFERENCES users(user_id)
                ON DELETE CASCADE,

                FOREIGN KEY (case_id) REFERENCES cases(case_id)
                ON DELETE CASCADE
            );
        """)


# ------------------------- CASES -------------------------

def add_case(case_data: dict) -> str | None:
    """
    Add a new case.
    Returns case_id, or None if the ID already exists.
    """
    required = (
        "case_id",
        "case_title",
        "case_type",
        "description"
    )

    if any(
        not str(case_data.get(key, "")).strip()
        for key in required
    ):
        raise ValueError(
            "Case ID, title, type and description are required."
        )

    case_id = str(case_data["case_id"]).strip()

    try:
        with db_connection() as conn:
            cursor = conn.execute("""
                INSERT INTO cases (
                    case_id,
                    case_title,
                    case_type,
                    description,
                    location,
                    incident_date,
                    difficulty_level
                )
                VALUES (?, ?, ?, ?, ?, ?, ?)
            """, (
                case_id,
                case_data["case_title"].strip(),
                case_data["case_type"].strip(),
                case_data["description"].strip(),
                case_data.get("location"),
                case_data.get("incident_date"),
                case_data.get("difficulty_level", "Medium")
            ))

            return case_id if cursor.rowcount > 0 else None

    except sqlite3.IntegrityError:
        return None


def get_all_cases() -> list[dict]:
    """Return all cases for the case-list screen."""
    with db_connection() as conn:
        rows = conn.execute(
            "SELECT * FROM cases ORDER BY case_id"
        ).fetchall()
    return _rows_to_dicts(rows)


def get_case_by_id(case_id: str) -> dict | None:
    """Return one case, or None if the ID does not exist."""
    with db_connection() as conn:
        row = conn.execute(
            "SELECT * FROM cases WHERE case_id = ?", (str(case_id),)
        ).fetchone()
    return _row_to_dict(row)


def update_case(case_id: str, case_data: dict) -> bool:
    """Update an existing case."""
    required = (
        "case_title",
        "case_type",
        "description"
    )

    if any(
        not str(case_data.get(key, "")).strip()
        for key in required
    ):
        raise ValueError(
            "Case title, type and description are required."
        )

    with db_connection() as conn:
        cursor = conn.execute("""
            UPDATE cases
            SET
                case_title = ?,
                case_type = ?,
                description = ?,
                location = ?,
                incident_date = ?,
                difficulty_level = ?
            WHERE case_id = ?
        """, (
            case_data["case_title"].strip(),
            case_data["case_type"].strip(),
            case_data["description"].strip(),
            case_data.get("location"),
            case_data.get("incident_date"),
            case_data.get("difficulty_level", "Medium"),
            str(case_id)
        ))

        return cursor.rowcount > 0


def delete_case(case_id: str) -> bool:
    """Delete a case and its dependent records using ON DELETE CASCADE."""
    with db_connection() as conn:
        cursor = conn.execute(
            "DELETE FROM cases WHERE case_id = ?", (str(case_id),)
        )
        return cursor.rowcount > 0


def filter_cases(
    user_id: int,
    case_type: str | None = None,
    status: str | None = None,
    difficulty_level: str | None = None
) -> list[dict]:

    if status and status not in (
        "Solved",
        "Unsolved"
    ):
        raise ValueError("Invalid status.")

    query = """
        SELECT
            c.*,
            COALESCE(p.status, 'Unsolved') AS user_status

        FROM cases AS c

        LEFT JOIN user_case_progress AS p
            ON c.case_id = p.case_id
            AND p.user_id = ?

        WHERE 1=1
    """

    params = [user_id]

    if case_type:
        query += " AND c.case_type = ? COLLATE NOCASE"
        params.append(case_type.strip())

    if status:
        query += """
            AND COALESCE(p.status, 'Unsolved') = ?
        """
        params.append(status.strip())

    if difficulty_level:
        query += """
            AND c.difficulty_level = ? COLLATE NOCASE
        """
        params.append(difficulty_level.strip())

    query += " ORDER BY c.case_id"

    with db_connection() as conn:
        rows = conn.execute(query, params).fetchall()

    return _rows_to_dicts(rows)


# ------------------------- SUSPECTS -------------------------

def add_suspect(case_id: str, suspect_data: dict) -> int | None:
    """Add a suspect to a case and return the new suspect_id."""
    name = str(suspect_data.get("name", "")).strip()
    if not name:
        raise ValueError("Suspect name is required.")

    with db_connection() as conn:
        cursor = conn.execute("""
            INSERT INTO suspects (case_id, name, age, occupation, address)
            VALUES (?, ?, ?, ?, ?)
        """, (
            str(case_id), name, suspect_data.get("age"),
            suspect_data.get("occupation"), suspect_data.get("address")
        ))
        return cursor.lastrowid


def get_suspects_by_case(case_id: str) -> list[dict]:
    """Return only suspects belonging to the selected case."""
    with db_connection() as conn:
        rows = conn.execute("""
            SELECT * FROM suspects
            WHERE case_id = ?
            ORDER BY suspect_id
        """, (str(case_id),)).fetchall()
    return _rows_to_dicts(rows)


def update_suspect(suspect_id: int, suspect_data: dict) -> bool:
    """Update a suspect. Returns True if a row changed."""
    name = str(suspect_data.get("name", "")).strip()
    if not name:
        raise ValueError("Suspect name is required.")

    with db_connection() as conn:
        cursor = conn.execute("""
            UPDATE suspects
            SET name = ?, age = ?, occupation = ?, address = ?
            WHERE suspect_id = ?
        """, (
            name, suspect_data.get("age"), suspect_data.get("occupation"),
            suspect_data.get("address"), suspect_id
        ))
        return cursor.rowcount > 0


def delete_suspect(suspect_id: int) -> bool:
    """Delete a suspect; linked statements cascade, linked culprit is restricted."""
    with db_connection() as conn:
        cursor = conn.execute(
            "DELETE FROM suspects WHERE suspect_id = ?", (suspect_id,)
        )
        return cursor.rowcount > 0


# ------------------------- STATEMENTS -------------------------

def add_statement(suspect_id: int, statement_data: dict) -> int | None:
    """Add a statement for a suspect and return statement_id."""
    statement_text = str(statement_data.get("statement", "")).strip()
    if not statement_text:
        raise ValueError("Statement text is required.")

    with db_connection() as conn:
        cursor = conn.execute("""
            INSERT INTO statements (
                suspect_id, statement, alibi, statement_date
            )
            VALUES (?, ?, ?, ?)
        """, (
            suspect_id, statement_text, statement_data.get("alibi"),
            statement_data.get("statement_date")
        ))
        return cursor.lastrowid


def get_statements_by_case(case_id: str) -> list[dict]:
    """Return statements for all suspects in the selected case."""
    with db_connection() as conn:
        rows = conn.execute("""
            SELECT
                st.statement_id, st.suspect_id, su.name AS suspect_name,
                st.statement, st.alibi, st.statement_date
            FROM statements AS st
            JOIN suspects AS su ON su.suspect_id = st.suspect_id
            WHERE su.case_id = ?
            ORDER BY st.statement_id
        """, (str(case_id),)).fetchall()
    return _rows_to_dicts(rows)


def update_statement(statement_id: int, statement_data: dict) -> bool:
    """Update a statement. Returns True if a row changed."""
    statement_text = str(statement_data.get("statement", "")).strip()
    if not statement_text:
        raise ValueError("Statement text is required.")

    with db_connection() as conn:
        cursor = conn.execute("""
            UPDATE statements
            SET statement = ?, alibi = ?, statement_date = ?
            WHERE statement_id = ?
        """, (
            statement_text, statement_data.get("alibi"),
            statement_data.get("statement_date"), statement_id
        ))
        return cursor.rowcount > 0


def delete_statement(statement_id: int) -> bool:
    """Delete one statement."""
    with db_connection() as conn:
        cursor = conn.execute(
            "DELETE FROM statements WHERE statement_id = ?", (statement_id,)
        )
        return cursor.rowcount > 0


# ------------------------- EVIDENCE -------------------------

def add_evidence(case_id: str, evidence_data: dict) -> int | None:
    """Add evidence to a case and return evidence_id."""
    evidence_name = str(evidence_data.get("evidence_name", "")).strip()
    if not evidence_name:
        raise ValueError("Evidence name is required.")

    with db_connection() as conn:
        cursor = conn.execute("""
            INSERT INTO evidence (
                case_id, evidence_name, evidence_type, description, collected_date
            )
            VALUES (?, ?, ?, ?, ?)
        """, (
            str(case_id), evidence_name, evidence_data.get("evidence_type"),
            evidence_data.get("description"), evidence_data.get("collected_date")
        ))
        return cursor.lastrowid


def get_evidence_by_case(case_id: str) -> list[dict]:
    """Return only evidence belonging to the selected case."""
    with db_connection() as conn:
        rows = conn.execute("""
            SELECT * FROM evidence
            WHERE case_id = ?
            ORDER BY evidence_id
        """, (str(case_id),)).fetchall()
    return _rows_to_dicts(rows)


def update_evidence(evidence_id: int, evidence_data: dict) -> bool:
    """Update evidence. Returns True if a row changed."""
    evidence_name = str(evidence_data.get("evidence_name", "")).strip()
    if not evidence_name:
        raise ValueError("Evidence name is required.")

    with db_connection() as conn:
        cursor = conn.execute("""
            UPDATE evidence
            SET evidence_name = ?, evidence_type = ?,
                description = ?, collected_date = ?
            WHERE evidence_id = ?
        """, (
            evidence_name, evidence_data.get("evidence_type"),
            evidence_data.get("description"),
            evidence_data.get("collected_date"), evidence_id
        ))
        return cursor.rowcount > 0


def delete_evidence(evidence_id: int) -> bool:
    """Delete one evidence record."""
    with db_connection() as conn:
        cursor = conn.execute(
            "DELETE FROM evidence WHERE evidence_id = ?", (evidence_id,)
        )
        return cursor.rowcount > 0


# ------------------------- CASE SOLUTIONS -------------------------

def add_solution(case_id: str, culprit_id: int, explanation: str) -> int | None:
    """Add one solution; ensure the culprit belongs to the same case."""
    if not explanation or not explanation.strip():
        raise ValueError("Solution explanation is required.")

    with db_connection() as conn:
        culprit = conn.execute("""
            SELECT 1 FROM suspects
            WHERE suspect_id = ? AND case_id = ?
        """, (culprit_id, str(case_id))).fetchone()

        if culprit is None:
            raise ValueError("Selected culprit does not belong to this case.")

        cursor = conn.execute("""
            INSERT INTO case_solutions (case_id, culprit_id, explanation)
            VALUES (?, ?, ?)
        """, (str(case_id), culprit_id, explanation.strip()))
        return cursor.lastrowid


def get_solution(case_id: str) -> dict | None:
    """Return the solution and culprit's name for one case."""
    with db_connection() as conn:
        row = conn.execute("""
            SELECT cs.solution_id, cs.case_id, cs.culprit_id,
                   su.name AS culprit_name, cs.explanation
            FROM case_solutions AS cs
            JOIN suspects AS su ON su.suspect_id = cs.culprit_id
            WHERE cs.case_id = ?
        """, (str(case_id),)).fetchone()
    return _row_to_dict(row)


def update_solution(case_id: str, culprit_id: int, explanation: str) -> bool:
    """Update a solution after validating the culprit belongs to the case."""
    if not explanation or not explanation.strip():
        raise ValueError("Solution explanation is required.")

    with db_connection() as conn:
        culprit = conn.execute("""
            SELECT 1 FROM suspects
            WHERE suspect_id = ? AND case_id = ?
        """, (culprit_id, str(case_id))).fetchone()

        if culprit is None:
            raise ValueError("Selected culprit does not belong to this case.")

        cursor = conn.execute("""
            UPDATE case_solutions
            SET culprit_id = ?, explanation = ?
            WHERE case_id = ?
        """, (culprit_id, explanation.strip(), str(case_id)))
        return cursor.rowcount > 0


def delete_solution(case_id: str) -> bool:
    """Delete the solution for one case."""
    with db_connection() as conn:
        cursor = conn.execute(
            "DELETE FROM case_solutions WHERE case_id = ?", (str(case_id),)
        )
        return cursor.rowcount > 0


# ------------------------- COMBINED CASE VIEW -------------------------

def get_complete_case(case_id: str) -> dict | None:
    """
    Return case, suspects, statements and evidence in one nested dictionary.
    The solution is deliberately excluded; call get_solution() only when
    the application is ready to reveal it.
    """
    case_info = get_case_by_id(case_id)
    if case_info is None:
        return None

    return {
        "case": case_info,
        "suspects": get_suspects_by_case(case_id),
        "statements": get_statements_by_case(case_id),
        "evidence": get_evidence_by_case(case_id)
    }


# ------------------------- USER DASHBOARD -------------------------

def update_user_progress(
    user_id: int,
    case_id: str,
    status: str
) -> bool:

    allowed_status = ("Unsolved", "Solved")

    if status not in allowed_status:
        raise ValueError("Invalid case status.")

    with db_connection() as conn:

        case = conn.execute(
            "SELECT 1 FROM cases WHERE case_id = ?",
            (str(case_id),)
        ).fetchone()

        if case is None:
            raise ValueError("Case does not exist.")

        user = conn.execute(
            "SELECT 1 FROM users WHERE user_id = ?",
            (user_id,)
        ).fetchone()

        if user is None:
            raise ValueError("User does not exist.")

        conn.execute("""
            INSERT INTO user_case_progress
                (user_id, case_id, status, updated_at)
            VALUES (?, ?, ?, CURRENT_TIMESTAMP)

            ON CONFLICT(user_id, case_id)
            DO UPDATE SET
                status = excluded.status,
                updated_at = CURRENT_TIMESTAMP
        """, (user_id, str(case_id), status))

    return True


def get_user_progress(user_id: int) -> list[dict]:

    with db_connection() as conn:

        rows = conn.execute("""
            SELECT
                c.case_id,
                c.case_title,
                COALESCE(p.status, 'Unsolved') AS status,
                p.updated_at

            FROM cases AS c

            LEFT JOIN user_case_progress AS p
                ON c.case_id = p.case_id
                AND p.user_id = ?

            ORDER BY c.case_id
        """, (user_id,)).fetchall()

    return _rows_to_dicts(rows)


def get_solved_cases(user_id: int) -> list[dict]:

    with db_connection() as conn:

        rows = conn.execute("""
            SELECT
                c.case_id,
                c.case_title,
                p.status,
                p.updated_at

            FROM user_case_progress AS p

            JOIN cases AS c
                ON p.case_id = c.case_id

            WHERE p.user_id = ?
              AND p.status = 'Solved'

            ORDER BY p.updated_at DESC
        """, (user_id,)).fetchall()

    return _rows_to_dicts(rows)


def get_dashboard_data(user_id: int) -> dict:
    """Return dashboard counts for one user only."""

    with db_connection() as conn:
        row = conn.execute("""
            SELECT
                COUNT(c.case_id) AS total_cases,

                COALESCE(SUM(
                    CASE
                        WHEN p.status = 'Solved'
                        THEN 1 ELSE 0
                    END
                ), 0) AS solved_cases

            FROM cases AS c

            LEFT JOIN user_case_progress AS p
                ON c.case_id = p.case_id
                AND p.user_id = ?

        """, (user_id,)).fetchone()

    solved = row["solved_cases"]
    total = row["total_cases"]

    return {
        "total_cases": total,
        "solved_cases": solved,
        "unsolved_cases": total - solved
    }


# ------------------------- DEFAULT SCENARIO LOADER -------------------------

def load_default_cases() -> None:
    """Insert all 10 default cases into SQLite if the cases table is empty."""
    create_tables()
    if get_all_cases():
        return

    default_data = [
        ("CASE-001", "The 11:47 PM Disappearance", "Theft",
         "A priceless antique necklace vanished from its locked gallery display case at 11:47 PM while the corridor CCTV was manually paused.",
         "National Heritage Gallery", "16 Oct 2026", "Medium",
         [("Samiha", 29, "Gallery Curator", "Dhanmondi, Dhaka"),
          ("Tasrif", 32, "Event Photographer", "Uttara, Dhaka"),
          ("Farhan", 35, "Security Supervisor", "Mirpur, Dhaka")],
         [("Samiha", "I left the gallery at 11:20 PM and never returned to the display room.", "Gallery exit log shows her card at 11:20 PM."),
          ("Tasrif", "I was taking photographs in the main hall until 11:35 PM.", "Camera timestamp shows photos at 11:30 PM."),
          ("Farhan", "I was patrolling the lower floor when the CCTV went offline.", "Claims routine patrol.")],
         [("Display Case Access Log", "Digital Record", "The display case was opened at 11:47 PM using Samiha's access card.", "16 Oct 2026"),
          ("CCTV Recording", "Video Record", "The corridor CCTV recording from 11:40 PM to 11:55 PM is missing.", "16 Oct 2026"),
          ("Security Console Audit", "Digital Record", "The CCTV system was manually paused at 11:42 PM using a session authenticated in the security room.", "16 Oct 2026"),
          ("Photographer's Image", "Digital Evidence", "A photograph recorded by Tasrif's camera at 11:30 PM shows the reflection of a person wearing Samiha's distinctive silver bracelet.", "16 Oct 2026"),
          ("Office Search", "Physical", "A replacement necklace box was found in a locked drawer assigned to Samiha, accessed with her staff code shortly after 11:50 PM.", "16 Oct 2026")],
         "Samiha", "Although Samiha's card logged an exit at 11:20 PM, Tasrif's 11:30 PM photo caught her silver bracelet reflection inside, and the replica box was found in her locked office drawer."),

        ("CASE-002", "The Last Message", "Murder",
         "A victim was found locked inside a home study room. A scheduled message was sent from the victim's laptop at 9:38 PM, after the estimated time of death.",
         "Gulshan Apartment", "22 Oct 2026", "Hard",
         [("Samira", 31, "Architect", "Gulshan, Dhaka"),
          ("Imran", 34, "Corporate Manager", "Banani, Dhaka"),
          ("Nusrat", 24, "Graduate Researcher", "Bashundhara, Dhaka")],
         [("Samira", "I came home late and went straight to my bedroom without opening the study.", "Elevator log shows return at 9:12 PM."),
          ("Imran", "I stayed late at my office finishing a presentation until 10:00 PM.", "Office CCTV confirms presence 8:50 PM - 10:00 PM."),
          ("Nusrat", "I was working in the university lab until 9:40 PM.", "Campus access log and lab camera confirm.")],
         [("Medical Report", "Medical Record", "The estimated time of death is between 9:05 PM and 9:25 PM.", "22 Oct 2026"),
          ("Laptop Message Metadata", "Digital Record", "The 9:38 PM message was scheduled earlier. The timestamp records delivery time, not typing time.", "23 Oct 2026"),
          ("Building Elevator Log", "Digital Record", "Samira's building access record shows her returning at 9:12 PM.", "23 Oct 2026"),
          ("Smart-Home Audit", "Digital Record", "The study-room door was manually locked at 9:18 PM using Samira's personal access code.", "23 Oct 2026")],
         "Samira", "Samira arrived at 9:12 PM—right inside the 9:05–9:25 PM death window—and used her personal access code to lock the study-room door at 9:18 PM."),

        ("CASE-003", "The Vanishing Diamond", "Heist",
         "The centerpiece diamond disappeared from the exhibition hall at 9:27 PM after the display case was unlocked with a master code.",
         "Grand Exhibition Center", "6 Nov 2026", "Easy",
         [("Ayesha Rahman", 36, "Chief Exhibition Officer", "Baridhara, Dhaka"),
          ("Rafi Ahmed", 33, "Head of Security", "Mohammadpur, Dhaka"),
          ("Meera Khan", 27, "Press Photographer", "Lalmatia, Dhaka")],
         [("Ayesha Rahman", "I was hosting VIP guests in the lounge and never touched the display case.", "No independent alibi at 9:27 PM."),
          ("Rafi Ahmed", "I was investigating a disturbance in the north corridor at 9:26 PM.", "Logged duty note in north corridor at 9:26 PM."),
          ("Meera Khan", "I was photographing the main hall clock and crowd around 9:28 PM.", "Camera photo timestamped 9:28 PM.")],
         [("Digital Lock Record", "Digital Record", "The master code opened the display case at 9:27 PM.", "6 Nov 2026"),
          ("Security Register", "Written Record", "Only Ayesha Rahman and Rafi Ahmed were authorized to use the master code.", "6 Nov 2026"),
          ("Security Duty Note", "Written Record", "Rafi Ahmed recorded a security issue in the north corridor at 9:26 PM, one minute before the display case opened.", "6 Nov 2026")],
         "Ayesha Rahman", "Only Ayesha Rahman and Rafi Ahmed knew the master code. Since Rafi was documented in the north corridor at 9:26 PM, Ayesha unlocked the case at 9:27 PM."),

        ("CASE-004", "The Missing Prototype", "Corporate Espionage",
         "A confidential hardware prototype was stolen from the institute project room around 6:42 PM.",
         "Tech Research Institute", "13 Oct 2026", "Easy",
         [("Tuhin Ahmed", 26, "Junior Engineer", "Uttara, Dhaka"),
          ("Sana", 28, "Systems Analyst", "Mirpur, Dhaka"),
          ("Imran", 31, "Network Admin", "Badda, Dhaka")],
         [("Tuhin Ahmed", "I left the institute early at 6:20 PM before anything happened.", "Claimed early departure."),
          ("Sana", "I was in the Room 105 project meeting from 6:35 PM to 7:00 PM.", "Confirmed by meeting organizer."),
          ("Imran", "I was working inside the server room from 6:30 PM to 7:02 PM.", "Confirmed by server room access log.")],
         [("Access Card Log", "Digital Record", "The project room door opened at 6:42 PM using temporary access card T-17 issued to Tuhin Ahmed.", "13 Oct 2026"),
          ("Torn Paper Piece", "Physical Evidence", "A small torn piece of green folder paper found beside the cabinet matched the missing corner of Tuhin Ahmed's green folder.", "13 Oct 2026"),
          ("Main Gate Register", "Written Record", "Tuhin left the institute at 7:05 PM, not 6:20 PM as claimed.", "13 Oct 2026")],
         "Tuhin Ahmed", "Tuhin lied about leaving at 6:20 PM (gate register shows 7:05 PM), his card T-17 opened the door at 6:42 PM, and a torn piece of his green folder was left at the scene."),

        ("CASE-005", "The Missing Blueprint", "Theft",
         "A classified engineering blueprint was taken from the exhibition display case at 8:24 PM.",
         "Innovation Expo Hall", "19 Oct 2026", "Medium",
         [("Nadia Karim", 27, "Pass Coordinator", "Dhanmondi, Dhaka"),
          ("Tania", 25, "Media Intern", "Farmgate, Dhaka"),
          ("Farhan", 34, "Security Guard", "Tejgaon, Dhaka")],
         [("Nadia Karim", "I stayed at the reception desk the whole evening managing staff passes.", "Receptionist noted she left briefly after 8:20 PM."),
          ("Tania", "I was taking photos of the exhibition stage in the main hall.", "Photos at 8:19 PM and 8:28 PM confirm."),
          ("Farhan", "I was stationed at the east entrance assisting visitors.", "Signed visitor assistance form at 8:23 PM.")],
         [("Display Case Log", "Digital Record", "The display case was opened at 8:24 PM using temporary staff access card E-17.", "19 Oct 2026"),
          ("Staff Pass Register", "Written Record", "Pass E-17 was issued to Nadia Karim and was not recorded returned before 8:40 PM.", "19 Oct 2026"),
          ("Reception Desk Note", "Written Record", "The receptionist noted that Nadia left the desk briefly to check a pass issue shortly after 8:20 PM.", "19 Oct 2026")],
         "Nadia Karim", "Pass E-17 was issued to Nadia Karim, and she left the reception desk right after 8:20 PM—matching the 8:24 PM breach."),

        ("CASE-006", "The Silent Server", "Cybercrime",
         "At 2:35 AM, a critical server was shut down and sensitive data was exfiltrated to an external IP address.",
         "Core Data Center", "28 Oct 2026", "Hard",
         [("Arman", 33, "Lead SysAdmin", "Uttara, Dhaka"),
          ("Rifat", 28, "Backend Developer", "Mirpur, Dhaka"),
          ("Maya", 30, "SOC Analyst", "Gulshan, Dhaka")],
         [("Arman", "I was asleep at home; my laptop was connected to my home Wi-Fi all night.", "Home router log confirms connection 2:15 AM - 2:50 AM."),
          ("Rifat", "I had no admin access to the server and was offline after midnight.", "No valid alibi."),
          ("Maya", "I saw a routine maintenance alert on the dashboard and cleared it.", "Cleared alert at 2:43 AM.")],
         [("Server Command Log", "Digital Record", "A shutdown command was executed at 2:35 AM using Arman's administrator account.", "28 Oct 2026"),
          ("Arman's Home Router Log", "Digital Record", "Arman's home router shows his laptop connected to his home Wi-Fi from 2:15 AM to 2:50 AM.", "29 Oct 2026"),
          ("Rifat's Workstation", "Digital Evidence", "A script capable of sending server commands using stored administrator credentials was found on Rifat's remote workstation.", "29 Oct 2026"),
          ("Script Execution History", "Digital Record", "The execution history records the malicious script running on Rifat's workstation initiating the shutdown and transfer.", "29 Oct 2026")],
         "Rifat", "Rifat used a malicious script on his workstation with Arman's stolen credentials to trigger the 2:35 AM shutdown and 2:41 AM data theft remotely."),

        ("CASE-007", "The 2-Minute Alibi", "Burglary",
         "A VIP hotel suite was burglarized at 10:08 PM after the balcony sensor was disabled and a remote keycard unlock occurred.",
         "Grand Regency Hotel", "30 Oct 2026", "Hard",
         [("Rayan", 30, "Hotel Guest", "Banani, Dhaka"),
          ("Tania", 26, "Front Desk Receptionist", "Khilgaon, Dhaka"),
          ("Shafin", 37, "Duty Manager", "Dhanmondi, Dhaka")],
         [("Rayan", "I walked out of the hotel lobby before 10:00 PM to meet a friend.", "Lobby CCTV shows Rayan leaving at 9:57 PM."),
          ("Tania", "I never left the reception desk and my keycard was in my pocket.", "Reception login active 9:45 PM - 10:20 PM."),
          ("Shafin", "I was only running routine maintenance tests on the seventh floor.", "Closed maintenance ticket as routine testing.")],
         [("Balcony Sensor Audit", "Digital Record", "The balcony door sensor was disabled at 9:50 PM using Shafin's maintenance credentials.", "31 Oct 2026"),
          ("Remote Transaction Audit", "Digital Record", "A backup access log shows the 10:08 PM keycard transaction was generated remotely by the access-control console.", "31 Oct 2026"),
          ("Administrator Session Log", "Digital Record", "The access-control console was logged in with Shafin's manager credentials when the remote transaction was generated.", "31 Oct 2026")],
         "Shafin", "Shafin disabled the balcony sensor at 9:50 PM and used his manager console login to spoof Tania's keycard remotely at 10:08 PM."),

        ("CASE-008", "The Deadly Prescription", "Murder",
         "Dr. Hasan suffered a fatal arrhythmia in his private clinic office at 7:34 PM caused by an unauthorized Potassium Chloride injection.",
         "City Care Medical Center", "8 Nov 2026", "Medium",
         [("Nurse Nusrat", 28, "Senior Duty Nurse", "Shyamoli, Dhaka"),
          ("Imran", 35, "Pharma Representative", "Motijheel, Dhaka"),
          ("Dr. Faisal", 41, "Consulting Physician", "Uttara, Dhaka")],
         [("Nurse Nusrat", "I only checked the medicine cabinet earlier and never entered Dr. Hasan's office.", "Keycard #04 accessed drug storage and office suite."),
          ("Imran", "I left Dr. Hasan's office at 7:28 PM after dropping off sample brochures.", "Corridor CCTV confirms exit at 7:28 PM."),
          ("Dr. Faisal", "I waited in the consultation anteroom from 7:30 PM for our scheduled review.", "Corridor CCTV confirms anteroom entry.")],
         [("Syringe & Vial", "Physical Evidence", "An empty 10ml syringe containing trace Potassium Chloride was recovered from the office hazardous bio-bin.", "8 Nov 2026"),
          ("Keycard Access Log", "Digital Record", "Keycard #04 (Nusrat) accessed the drug storage at 7:22 PM and the office suite at 7:31 PM.", "8 Nov 2026"),
          ("Dispensary Register", "Written Record", "Potassium Chloride ampoules were audited; one unit was unaccounted for under Nurse Nusrat's shift log.", "9 Nov 2026")],
         "Nurse Nusrat", "A Potassium Chloride ampoule went missing on Nurse Nusrat's shift, and her keycard accessed the drug storage at 7:22 PM and Dr. Hasan's office at 7:31 PM—three minutes before cardiac arrest."),

        ("CASE-009", "The Poisoned Birthday Slice", "Poisoning",
         "During a private birthday celebration, a slice of strawberry-glazed cake served to Lily was laced with agricultural pesticide.",
         "Rosewood Banquet Hall", "9 Nov 2026", "Easy",
         [("Samira", 30, "Head Pastry Chef", "Lalmatia, Dhaka"),
          ("Nadia Islam", 27, "Event Coordinator", "Banani, Dhaka"),
          ("Tariq Aziz", 32, "Catering Waiter", "Mirpur, Dhaka")],
         [("Samira", "I baked the cake fresh and sealed it properly before delivery.", "Bakery CCTV shows her packing a separate marked glaze container."),
          ("Nadia Islam", "I locked the cake inside the venue pantry right after delivery at 6:30 PM.", "Pantry log confirms locked until 7:25 PM."),
          ("Tariq Aziz", "I only served water glasses to the guests and never touched the cake.", "Fingerprints found only on water tumbler.")],
         [("Cake Residue Sample", "Forensic Sample", "Toxicology showed pesticide contamination concentrated in the strawberry glaze on the slice served to Lily.", "9 Nov 2026"),
          ("Bakery CCTV Footage", "Video Record", "Samira was recorded preparing strawberry glaze at 4:15 PM and placing the marked container separately in the delivery kit.", "9 Nov 2026"),
          ("Pesticide Container", "Physical Evidence", "An empty agricultural pesticide vial was recovered from the trash receptacle behind Samira's bakery shop.", "9 Nov 2026")],
         "Samira", "Samira prepared the poisoned strawberry glaze separately on bakery CCTV, and the empty pesticide vial was found in the trash behind her shop."),

        ("CASE-010", "The Stolen Land Deed", "Fraud & Theft",
         "Original family land deeds vanished from the locked study safe during an evening family dinner.",
         "Alam Estate Residence", "9 Nov 2026", "Medium",
         [("Khorshed Alam", 48, "Estate Caretaker", "Savar, Dhaka"),
          ("Zubair", 29, "Nephew", "Dhanmondi, Dhaka"),
          ("Asif", 34, "Family Lawyer", "Uttara, Dhaka")],
         [("Khorshed Alam", "I was busy cleaning the staff quarters and never went near the study safe.", "Duplicate safe key hidden in staff quarter supply locker."),
          ("Zubair", "I stepped out of the dining hall for 5 minutes to take a phone call.", "Estate CCTV confirms dining hall presence."),
          ("Asif", "I stayed at the dining table discussing estate matters the entire evening.", "Estate CCTV confirms dining hall presence.")],
         [("Safe Key Impression", "Forensic Sample", "Fresh jeweler's silicone wax was found inside the study desk drawer where the main safe key was stored.", "9 Nov 2026"),
          ("Dusting Cloth & Key", "Physical Evidence", "A duplicate safe key wrapped in a cleaning cloth was discovered hidden inside a supply locker in the staff quarter.", "9 Nov 2026"),
          ("Pawn Broker Contact Log", "Digital Record", "Phone records revealed multiple encrypted calls between an unlisted broker and Khorshed Alam over the past two weeks.", "9 Nov 2026")],
         "Khorshed Alam", "Khorshed Alam made a wax impression of the safe key, hid the duplicate key wrapped in a cleaning cloth in the staff quarter, and contacted an unlisted broker to sell the deed.")
    ]

    for cid, title, ctype, desc, loc, idate, diff, suspects, stmts, evs, culprit, exp in default_data:
        add_case({
            "case_id": cid, "case_title": title, "case_type": ctype,
            "description": desc, "location": loc, "incident_date": idate,
            "difficulty_level": diff
        })
        s_map = {}
        for name, age, occ, addr in suspects:
            s_map[name] = add_suspect(cid, {"name": name, "age": age, "occupation": occ, "address": addr})
        for s_name, st_text, alibi in stmts:
            add_statement(s_map[s_name], {"statement": st_text, "alibi": alibi, "statement_date": idate})
        for e_name, e_type, e_desc, e_date in evs:
            add_evidence(cid, {"evidence_name": e_name, "evidence_type": e_type, "description": e_desc, "collected_date": e_date})
        add_solution(cid, s_map[culprit], exp)


if __name__ == "__main__":
    load_default_cases()
    print("CaseClosed database and default cases are ready.")
    print(f"Database location: {DB_PATH}")