
from passlib.context import CryptContext

pwd_context = CryptContext(
    schemes=["bcrypt"],
    deprecated="auto",
)

# bcrypt has a hard 72-BYTE limit (not characters - multi-byte UTF-8
# characters like emoji can hit this with fewer visible characters).
# Truncating consistently here, for both hashing and verification,
# means a long password never throws a raw library error up to the
# user - it just uses the first 72 bytes, same as bcrypt would do
# internally anyway.
def _truncate_to_bcrypt_limit(password: str) -> str:
    return password.encode("utf-8")[:72].decode("utf-8", errors="ignore")


def hash_password(password: str):
    return pwd_context.hash(_truncate_to_bcrypt_limit(password))


def verify_password(password: str, hashed_password: str):
    return pwd_context.verify(_truncate_to_bcrypt_limit(password), hashed_password)