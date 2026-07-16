from sqlalchemy import Column, Integer, String, Boolean, DateTime

from app.database import Base


class User(Base):
    __tablename__ = "users"

    id = Column(Integer, primary_key=True, index=True)

    name = Column(String, nullable=False)

    email = Column(String, unique=True, index=True)

    password = Column(String, nullable=False)

    is_verified = Column(Boolean, default=False)

    otp = Column(String, nullable=True)

    # Login rate limiting
    failed_login_attempts = Column(Integer, default=0)
    locked_until = Column(DateTime, nullable=True)