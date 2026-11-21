"""Safe smoke test for CaseClosed database.py and user_management.py.

Run from the project folder:
    python test_caseclosed.py

This test uses a temporary database, so it does not change caseclosed.db.
"""

import tempfile
from pathlib import Path

import database
import user_management


def run_tests():
    with tempfile.TemporaryDirectory() as temp_dir:
        # Redirect both modules to a disposable test database.
        database.DB_PATH = Path(temp_dir) / "caseclosed_test.db"

        database.create_tables()
        print("[PASS] Database and all six tables created")

        # User management tests
        assert user_management.register_user(
            "test_user", "test_user@example.com", "TestPass123"
        ) is True
        print("[PASS] User registration")

        user = user_management.login_user(
            "test_user@example.com", "TestPass123"
        )
        assert user is not None
        assert user["username"] == "test_user"
        assert user["role"] == "user"
        assert "password_hash" not in user
        print("[PASS] Correct login and safe user data")

        assert user_management.login_user(
            "test_user@example.com", "WrongPass123"
        ) is None
        print("[PASS] Wrong password rejected")

        assert user_management.register_user(
            "another_user", "test_user@example.com", "AnotherPass123"
        ) is False
        print("[PASS] Duplicate email rejected")

        admin_id = user_management.create_initial_admin(
            "test_admin", "test_admin@example.com", "AdminPass123"
        )
        admin = user_management.login_user(
            "test_admin@example.com", "AdminPass123"
        )
        assert admin_id == admin["user_id"]
        assert admin["role"] == "admin"
        print("[PASS] Initial admin creation and login")

        # Case and related-record tests
        case_id = database.add_case({
            "case_id": "TEST-001",
            "case_title": "Test Case",
            "case_type": "Theft",
            "description": "A sample case used only for testing.",
            "location": "Dhaka",
            "incident_date": "2026-11-05",
            "status": "Unsolved",
            "difficulty_level": "Easy"
        })
        assert case_id == "TEST-001"
        print("[PASS] Add case with text Case ID")

        suspect_id = database.add_suspect("TEST-001", {
            "name": "Test Suspect",
            "age": 30,
            "occupation": "Test Occupation",
            "address": "Dhaka"
        })
        print("[PASS] Add suspect")

        database.add_statement(suspect_id, {
            "statement": "This is a test statement.",
            "alibi": "This is a test alibi.",
            "statement_date": "2026-11-06"
        })
        print("[PASS] Add statement")

        database.add_evidence("TEST-001", {
            "evidence_name": "Test Evidence",
            "evidence_type": "Written Record",
            "description": "Test evidence description.",
            "collected_date": "2026-11-06"
        })
        print("[PASS] Add evidence")

        complete_case = database.get_complete_case("TEST-001")
        assert complete_case is not None
        assert complete_case["case"]["case_id"] == "TEST-001"
        assert len(complete_case["suspects"]) == 1
        assert len(complete_case["statements"]) == 1
        assert len(complete_case["evidence"]) == 1
        assert "solution" not in complete_case
        print("[PASS] Complete case data returned in one dictionary")

        solution_id = database.add_solution(
            "TEST-001", suspect_id, "Test solution explanation."
        )
        assert solution_id is not None
        assert database.get_solution("TEST-001")["culprit_id"] == suspect_id
        print("[PASS] Add and retrieve case solution")

        dashboard = database.get_dashboard_data()
        assert dashboard == {
            "total_cases": 1,
            "solved_cases": 0,
            "unsolved_cases": 1
        }
        print("[PASS] Dashboard counts")

        filtered = database.filter_cases(
            case_type="Theft", status="Unsolved"
        )
        assert len(filtered) == 1
        print("[PASS] Case search/filter")

        assert database.update_case("TEST-001", {
            "case_title": "Updated Test Case",
            "case_type": "Theft",
            "description": "Updated test description.",
            "location": "Dhaka",
            "incident_date": "2026-11-05",
            "status": "Solved",
            "difficulty_level": "Hard"
        }) is True

        dashboard = database.get_dashboard_data()
        assert dashboard == {
            "total_cases": 1,
            "solved_cases": 1,
            "unsolved_cases": 0
        }
        print("[PASS] Update case and refreshed dashboard counts")

        assert database.delete_case("TEST-001") is True
        assert database.get_case_by_id("TEST-001") is None
        print("[PASS] Delete case and related records")

    print("\nSUCCESS: All tests passed.")
    print("Your original caseclosed.db was not changed.")


if __name__ == "__main__":
    run_tests()
