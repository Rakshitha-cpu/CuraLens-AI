import random
from sqlalchemy.orm import Session

from app.auth.models import User
from app.auth.schemas import UserSignup
from app.auth.utils import hash_password, verify_password
from app.auth.email_service import send_verification_email


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

    # Send OTP to email
    send_verification_email(
        receiver_email=user.email,
        otp=otp,
    )

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

    if not verify_password(password, user.password):
        return None

    if not user.is_verified:
        raise Exception("Please verify your email first.")

    return user