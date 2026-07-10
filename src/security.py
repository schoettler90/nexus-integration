"""Password hashing helpers (bcrypt via passlib).

Stored passwords are bcrypt hashes. ``verify_password`` transparently accepts a
legacy plaintext record (pre-migration) so login keeps working until
``scripts/hash_passwords.py`` has run; new writes always hash.
"""

import hmac

from passlib.context import CryptContext

_pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")

_BCRYPT_PREFIXES = ("$2a$", "$2b$", "$2y$")


def is_bcrypt_hash(value: str) -> bool:
    """True if ``value`` already looks like a bcrypt hash."""
    return isinstance(value, str) and value.startswith(_BCRYPT_PREFIXES)


def hash_password(password: str) -> str:
    """Hash a plaintext password for storage."""
    return _pwd_context.hash(password)


def verify_password(plain: str, stored: str) -> bool:
    """Check ``plain`` against a stored bcrypt hash (or a legacy plaintext
    record that predates the hash_passwords.py migration)."""
    if is_bcrypt_hash(stored):
        return _pwd_context.verify(plain, stored)
    return hmac.compare_digest(plain.encode(), stored.encode())
