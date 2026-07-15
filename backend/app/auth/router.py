from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session

from app.database import get_db
from app.auth.models import User
from app.auth.schemas import (
    UserSignup,
    UserLogin,
    VerifyOTP,
)
from app.auth.service import (
    register_user,
    login_user,
)
from app.auth.jwt_utils import create_access_token

router = APIRouter(
    prefix="/auth",
    tags=["Authentication"],
)


@router.post("/register")
def register(user: UserSignup, db: Session = Depends(get_db)):
    try:
        return register_user(db, user)
    except Exception as e:
        raise HTTPException(
            status_code=400,
            detail=str(e),
        )


@router.post("/verify-otp")
def verify_otp(data: VerifyOTP, db: Session = Depends(get_db)):
    user = (
        db.query(User)
        .filter(User.email == data.email)
        .first()
    )

    if not user:
        raise HTTPException(
            status_code=404,
            detail="User not found",
        )

    if user.otp != data.otp:
        raise HTTPException(
            status_code=400,
            detail="Invalid OTP",
        )

    user.is_verified = True
    user.otp = None

    db.commit()

    return {
        "message": "Email verified successfully"
    }


@router.post("/login")
def login(user: UserLogin, db: Session = Depends(get_db)):
    try:
        logged_user = login_user(
            db,
            user.email,
            user.password,
        )

        if logged_user is None:
            raise HTTPException(
                status_code=401,
                detail="Invalid email or password",
            )

        token = create_access_token(
            user_id=logged_user.id,
            email=logged_user.email,
        )

        return {
            "message": "Login Successful",
            "access_token": token,
            "token_type": "bearer",
            "user": {
                "id": logged_user.id,
                "name": logged_user.name,
                "email": logged_user.email,
            },
        }

    except Exception as e:
        raise HTTPException(
            status_code=400,
            detail=str(e),
        )