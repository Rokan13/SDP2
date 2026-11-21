import hashlib
import hmac
import secrets
import sqlite3
from getpass import getpass

from database import db_connection, create_tables

HASH_NAME = "sha256"
HASH_ITERATIONS = 260_000
SALT_LENGTH = 16


def _hash_password(password: str) -> str:
    """Create a salted PBKDF2 password hash."""
    if not isinstance(password, str) or len(password) < 8:
        raise ValueError("Password must contain at least 8 characters.")

    salt = secrets.token_bytes(SALT_LENGTH)
    digest = hashlib.pbkdf2_hmac(
        HASH_NAME, password.encode("utf-8"), salt, HASH_ITERATIONS
    )
    return (
        f"pbkdf2_{HASH_NAME}${HASH_ITERATIONS}"
        f"${salt.hex()}${digest.hex()}"
    )


def _verify_password(password: str, stored_hash: str) -> bool:
    """Verify a password against its stored PBKDF2 hash."""
    try:
        algorithm, iterations, salt_hex, digest_hex = stored_hash.split("$")
        if algorithm != "pbkdf2_sha256":
            return False

        salt = bytes.fromhex(salt_hex)
        expected = bytes.fromhex(digest_hex)
        actual = hashlib.pbkdf2_hmac(
            HASH_NAME, password.encode("utf-8"), salt, int(iterations)
        )
        return hmac.compare_digest(actual, expected)
    except (ValueError, TypeError, AttributeError):
        return False


def check_email_exists(email: str) -> bool:
    """Return True if the email is already registered."""
    with db_connection() as conn:
        row = conn.execute(
            "SELECT 1 FROM users WHERE email = ? COLLATE NOCASE",
            (email.strip(),)
        ).fetchone()
    return row is not None


def register_user(username: str, email: str, password: str) -> bool:
    """
    Register a normal user. Public registration always assigns role='user'.
    Returns True on success and False if the email already exists.
    """
    username = username.strip()
    email = email.strip().lower()

    if not username:
        raise ValueError("Username is required.")
    if not email:
        raise ValueError("Email is required.")

    password_hash = _hash_password(password)

    try:
        with db_connection() as conn:
            conn.execute("""
                INSERT INTO users (username, email, password_hash, role)
                VALUES (?, ?, ?, 'user')
            """, (username, email, password_hash))
        return True
    except sqlite3.IntegrityError:
        return False


def login_user(email: str, password: str) -> dict | None:
    """
    Return public user details on successful login; otherwise return None.
    The password hash is never returned to the GUI.
    """
    with db_connection() as conn:
        user = conn.execute("""
            SELECT user_id, username, email, password_hash, role
            FROM users
            WHERE email = ? COLLATE NOCASE
        """, (email.strip(),)).fetchone()

    if user is None or not _verify_password(password, user["password_hash"]):
        return None

    return {
        "user_id": user["user_id"],
        "username": user["username"],
        "email": user["email"],
        "role": user["role"]
    }


def get_user_by_id(user_id: int) -> dict | None:
    """Return public user details without the password hash."""
    with db_connection() as conn:
        user = conn.execute("""
            SELECT user_id, username, email, role
            FROM users
            WHERE user_id = ?
        """, (user_id,)).fetchone()

    return dict(user) if user is not None else None


def create_initial_admin(username: str, email: str, password: str) -> int:
    """
    Create the first admin only. This function refuses to create a second
    initial admin if an admin account already exists.
    """
    username = username.strip()
    email = email.strip().lower()

    if not username:
        raise ValueError("Admin username is required.")
    if not email:
        raise ValueError("Admin email is required.")

    password_hash = _hash_password(password)

    with db_connection() as conn:
        existing_admin = conn.execute("""
            SELECT 1 FROM users WHERE role = 'admin' LIMIT 1
        """).fetchone()

        if existing_admin:
            raise ValueError("An admin account already exists.")

        cursor = conn.execute("""
            INSERT INTO users (username, email, password_hash, role)
            VALUES (?, ?, ?, 'admin')
        """, (username, email, password_hash))

        return cursor.lastrowid


def create_admin_account(
    acting_admin_id: int,
    username: str,
    email: str,
    password: str
) -> int:
    """Allow an existing admin to create another admin account."""
    username = username.strip()
    email = email.strip().lower()

    if not username:
        raise ValueError("Admin username is required.")
    if not email:
        raise ValueError("Admin email is required.")

    password_hash = _hash_password(password)

    with db_connection() as conn:
        admin = conn.execute("""
            SELECT 1 FROM users
            WHERE user_id = ? AND role = 'admin'
        """, (acting_admin_id,)).fetchone()

        if admin is None:
            raise PermissionError("Only an existing admin can create an admin.")

        cursor = conn.execute("""
            INSERT INTO users (username, email, password_hash, role)
            VALUES (?, ?, ?, 'admin')
        """, (username, email, password_hash))

        return cursor.lastrowid


def setup_initial_admin() -> None:
    """Interactive first-admin setup from the terminal."""
    create_tables()

    print("\n=== CaseClosed: First Admin Setup ===")
    username = input("Admin username: ").strip()
    email = input("Admin email: ").strip()
    password = getpass("Admin password (minimum 8 characters): ")
    confirm_password = getpass("Confirm password: ")

    if password != confirm_password:
        print("Error: Passwords do not match.")
        return

    try:
        admin_id = create_initial_admin(username, email, password)
        print(f"First admin account created. User ID: {admin_id}")
    except (ValueError, sqlite3.IntegrityError) as error:
        print(f"Could not create admin account: {error}")


if __name__ == "__main__":
    setup_initial_admin()
