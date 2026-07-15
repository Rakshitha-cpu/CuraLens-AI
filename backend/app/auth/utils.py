import bcrypt

# NOTE: This intentionally does NOT use passlib's CryptContext.
# passlib 1.7.4 (last released 2020) has a known, unpatched
# incompatibility with modern bcrypt (4.1+): its internal self-test
# (detect_wrap_bug) relies on a bcrypt.__about__ attribute that was
# removed in newer bcrypt releases. This causes passlib to throw
# "password cannot be longer than 72 bytes" on EVERY hash/verify call,
# regardless of actual password length - the error is misleading and
# unrelated to what the user typed. Using the bcrypt library directly
# avoids this broken compatibility layer entirely.


def _truncate_to_bcrypt_limit(password: str) -> bytes:
    """
    bcrypt has a genuine, real 72-BYTE limit on input length (not
    characters - multi-byte UTF-8 characters like emoji count as
    multiple bytes). Truncate consistently before hashing/verifying
    so an unusually long password degrades gracefully instead of
    raising an error.
    """
    return password.encode("utf-8")[:72]


def hash_password(password: str) -> str:
    truncated = _truncate_to_bcrypt_limit(password)
    hashed = bcrypt.hashpw(truncated, bcrypt.gensalt())
    return hashed.decode("utf-8")


def verify_password(password: str, hashed_password: str) -> bool:
    truncated = _truncate_to_bcrypt_limit(password)
    try:
        return bcrypt.checkpw(truncated, hashed_password.encode("utf-8"))
    except ValueError:
        # Malformed/corrupted stored hash (e.g. from an account created
        # during the earlier broken passlib period) - treat as a failed
        # login rather than crashing the request.
        return False
