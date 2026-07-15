from datetime import datetime

from sqlalchemy import Column, Integer, String, Text, DateTime, ForeignKey

from app.database import Base


class Prescription(Base):
    __tablename__ = "prescriptions"

    id = Column(Integer, primary_key=True, index=True)

    user_id = Column(Integer, ForeignKey("users.id"), nullable=False, index=True)

    patient_name = Column(String, nullable=True)
    doctor_name = Column(String, nullable=True)
    hospital = Column(String, nullable=True)

    medicine_count = Column(Integer, default=0)
    risk_level = Column(String, nullable=True)
    score = Column(Integer, nullable=True)

    # Full analysis result (same JSON shape /ai/test returns) so History
    # can reopen a past prescription without re-running OCR/AI.
    result_json = Column(Text, nullable=False)

    created_at = Column(DateTime, default=datetime.utcnow)
