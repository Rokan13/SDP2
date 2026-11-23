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
                CHECK (status IN ('Unsolved', 'In Progress', 'Solved')),

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
        "Unsolved",
        "In Progress"
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


# ------------------------- DASHBOARD -------------------------

# ------------------------- USER DASHBOARD -------------------------

def update_user_progress(
    user_id: int,
    case_id: str,
    status: str
) -> bool:

    allowed_status = ("Unsolved", "In Progress", "Solved")

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
                ), 0) AS solved_cases,

                COALESCE(SUM(
                    CASE
                        WHEN p.status = 'In Progress'
                        THEN 1 ELSE 0
                    END
                ), 0) AS in_progress_cases

            FROM cases AS c

            LEFT JOIN user_case_progress AS p
                ON c.case_id = p.case_id
                AND p.user_id = ?

        """, (user_id,)).fetchone()

    solved = row["solved_cases"]
    in_progress = row["in_progress_cases"]
    total = row["total_cases"]

    return {
        "total_cases": total,
        "solved_cases": solved,
        "in_progress_cases": in_progress,
        "unsolved_cases": total - solved - in_progress
    }

if __name__ == "__main__":
    create_tables()
    print("CaseClosed database and tables are ready.")
    print(f"Database location: {DB_PATH}")
