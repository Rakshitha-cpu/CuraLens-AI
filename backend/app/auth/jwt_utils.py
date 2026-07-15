import os
from datetime import datetime, timedelta, timezone

import jwt
from fastapi import Depends, HTTPException, status
from fastapi.security import HTTPBearer, HTTPAuthorizationCredentials

SECRET_KEY = os.getenv("JWT_SECRET_KEY")

if not SECRET_KEY:
    raise ValueError(
        "JWT_SECRET_KEY not found in .env. "
        "Add a random secret string, e.g.:\n\n"
        "JWT_SECRET_KEY=your-long-random-string-here\n\n"
        "Generate one with: python -c \"import secrets; print(secrets.token_hex(32))\""
    )

ALGORITHM = "HS256"
ACCESS_TOKEN_EXPIRE_HOURS = 24

security = HTTPBearer()
optional_security = HTTPBearer(auto_error=False)


def create_access_token(user_id: int, email: str) -> str:
    """
    Creates a signed JWT for the given user. The token itself carries
    the user's identity (in 'sub') - the server verifies the signature
    on every request instead of trusting a client-supplied user_id,
    which could be tampered with in devtools/localStorage.
    """

    expire = datetime.now(timezone.utc) + timedelta(hours=ACCESS_TOKEN_EXPIRE_HOURS)

    payload = {
        "sub": str(user_id),
        "email": email,
        "exp": expire,
    }

    return jwt.encode(payload, SECRET_KEY, algorithm=ALGORITHM)


def decode_access_token(token: str) -> dict:
    """
    Verifies and decodes a JWT. Raises jwt exceptions on failure
    (expired, invalid signature, malformed) - callers should catch
    these or use get_current_user() which already does.
    """

    return jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])


def get_current_user(credentials: HTTPAuthorizationCredentials = Depends(security)) -> int:
    """
    FastAPI dependency: extracts and verifies the Bearer token from the
    Authorization header, returns the authenticated user's id as an int.
    Use this on any route that should only act on the logged-in user's
    own data - it replaces trusting a user_id sent from the frontend.
    """

    token = credentials.credentials

    try:
        payload = decode_access_token(token)
        user_id = payload.get("sub")

        if user_id is None:
            raise HTTPException(
                status_code=status.HTTP_401_UNAUTHORIZED,
                detail="Invalid token: missing subject",
            )

        return int(user_id)

    except jwt.ExpiredSignatureError:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Session expired. Please log in again.",
        )

    except jwt.InvalidTokenError:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Invalid authentication token.",
        )


def get_current_user_optional(
    credentials: HTTPAuthorizationCredentials = Depends(optional_security),
):
    """
    Like get_current_user(), but returns None instead of raising when
    no token is sent at all - for routes that work both logged-in and
    anonymously (e.g. prescription analysis still works without an
    account, it just won't be saved to History). If a token IS sent
    but is invalid/expired, this still raises 401 - a bad token should
    not be silently treated as "anonymous".
    """

    if credentials is None:
        return None

    return get_current_user(credentials)
