from fastapi import APIRouter, UploadFile, File, Depends
from fastapi.responses import FileResponse
from sqlalchemy.orm import Session
import os
import json
import shutil

from app.orchestrator.agent_manager import AgentManager
from app.utils.pdf_generator import generate_prescription_report
from app.database import get_db
from app.history.models import Prescription
from app.auth.jwt_utils import get_current_user_optional

router = APIRouter(
    prefix="/ai",
    tags=["AI Pipeline"]
)

UPLOAD_DIR = "app/uploads"
os.makedirs(UPLOAD_DIR, exist_ok=True)


@router.post("/test")
async def run_pipeline(
    file: UploadFile = File(...),
    db: Session = Depends(get_db),
    user_id: int = Depends(get_current_user_optional),
):
    """
    Upload a prescription image and run the complete AI pipeline.
    If a valid Bearer token is sent (i.e. the person is logged in),
    the result is saved to their History. The user_id comes from a
    verified JWT now, not a client-supplied form field - previously
    anyone could edit the user_id in devtools/localStorage and save
    analyses under someone else's account. Analysis still works with
    no token at all - it just won't be saved anywhere.
    """

    file_path = os.path.join(UPLOAD_DIR, file.filename)

    with open(file_path, "wb") as buffer:
        shutil.copyfileobj(file.file, buffer)

    result = AgentManager.process(file_path)

    if user_id:
        try:
            medicines = result.get("medicines", []) or []
            safety = result.get("safety", {}) or {}
            score = result.get("score", {}) or {}

            record = Prescription(
                user_id=user_id,
                patient_name=result.get("patient_name"),
                doctor_name=result.get("doctor_name"),
                hospital=result.get("hospital"),
                medicine_count=len(medicines),
                risk_level=safety.get("overall_risk"),
                score=score.get("score"),
                result_json=json.dumps(result),
            )

            db.add(record)
            db.commit()

        except Exception as e:
            # Never let a save failure block the user from seeing their
            # analysis result - just log it and move on.
            print("Failed to save prescription history:", e)
            db.rollback()

    return result


@router.post("/report")
async def download_report(prescription: dict):
    """
    Takes the AI analysis result (same JSON returned by /ai/test)
    and returns a downloadable PDF report.
    """

    pdf_path = generate_prescription_report(prescription)

    return FileResponse(
        path=pdf_path,
        media_type="application/pdf",
        filename=os.path.basename(pdf_path),
    )