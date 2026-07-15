import json

from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session

from app.database import get_db
from app.history.models import Prescription
from app.auth.jwt_utils import get_current_user

router = APIRouter(
    prefix="/history",
    tags=["Prescription History"],
)


@router.get("/me")
def get_my_history(
    db: Session = Depends(get_db),
    current_user_id: int = Depends(get_current_user),
):
    """
    List the logged-in user's past prescription analyses, most recent
    first. Requires a valid Bearer token - previously this endpoint
    took a user_id straight from the URL, so anyone could view any
    other user's prescription history just by changing the number.
    """

    records = (
        db.query(Prescription)
        .filter(Prescription.user_id == current_user_id)
        .order_by(Prescription.created_at.desc())
        .all()
    )

    return [
        {
            "id": r.id,
            "patient_name": r.patient_name,
            "doctor_name": r.doctor_name,
            "hospital": r.hospital,
            "medicine_count": r.medicine_count,
            "risk_level": r.risk_level,
            "score": r.score,
            "created_at": r.created_at.isoformat() if r.created_at else None,
        }
        for r in records
    ]


@router.get("/detail/{prescription_id}")
def get_prescription_detail(
    prescription_id: int,
    db: Session = Depends(get_db),
    current_user_id: int = Depends(get_current_user),
):
    """
    Fetch one saved prescription's full analysis - only if it belongs
    to the logged-in user.
    """

    record = (
        db.query(Prescription)
        .filter(
            Prescription.id == prescription_id,
            Prescription.user_id == current_user_id,
        )
        .first()
    )

    if not record:
        raise HTTPException(status_code=404, detail="Prescription not found")

    return json.loads(record.result_json)
