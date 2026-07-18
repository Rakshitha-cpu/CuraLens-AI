import random
from datetime import datetime, timedelta

from sqlalchemy.orm import Session

from app.auth.models import User
from app.auth.schemas import UserSignup
from app.auth.utils import hash_password, verify_password
from app.auth.email_service import send_otp_email

MAX_FAILED_ATTEMPTS = 5
LOCKOUT_MINUTES = 5


def generate_otp():
    return str(random.randint(100000, 999999))


def register_user(db: Session, user: UserSignup):
    existing_user = (
        db.query(User)
        .filter(User.email == user.email)
        .first()
    )

    if existing_user:
        raise Exception("Email already registered.")

    otp = generate_otp()

    new_user = User(
        name=user.name,
        email=user.email,
        password=hash_password(user.password),
        otp=otp,
        is_verified=False,
    )

    db.add(new_user)
    db.commit()
    db.refresh(new_user)

    # Send OTP email
    try:
        send_otp_email(
            to_email=user.email,
            otp=otp,
        )
    except Exception as e:
        db.delete(new_user)
        db.commit()
        raise Exception(str(e))

    return {
        "message": "OTP sent to your email. Please verify your account."
    }


def login_user(db: Session, email: str, password: str):
    user = (
        db.query(User)
        .filter(User.email == email)
        .first()
    )

    if not user:
        return None

    # Check if currently locked out
    if user.locked_until and user.locked_until > datetime.utcnow():
        remaining = int(
            (user.locked_until - datetime.utcnow()).total_seconds() / 60
        ) + 1
        raise Exception(
            f"Too many failed login attempts. Try again in {remaining} minute(s)."
        )

    if not verify_password(password, user.password):
        user.failed_login_attempts = (user.failed_login_attempts or 0) + 1

        if user.failed_login_attempts >= MAX_FAILED_ATTEMPTS:
            user.locked_until = datetime.utcnow() + timedelta(
                minutes=LOCKOUT_MINUTES
            )
            db.commit()
            raise Exception(
                f"Too many failed login attempts. Account locked for {LOCKOUT_MINUTES} minutes."
            )

        db.commit()
        return None

    # Reset failed attempts on successful login
    if user.failed_login_attempts or user.locked_until:
        user.failed_login_attempts = 0
        user.locked_until = None
        db.commit()

    if not user.is_verified:
        raise Exception("Please verify your email first.")

    return user