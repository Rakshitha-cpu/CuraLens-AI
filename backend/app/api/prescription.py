from fastapi import APIRouter, UploadFile, File
import os
import shutil
from uuid import uuid4

router = APIRouter(
    prefix="/prescriptions",
    tags=["Prescriptions"]
)

UPLOAD_DIR = "app/uploads"

# Create upload folder automatically
os.makedirs(UPLOAD_DIR, exist_ok=True)


@router.post("/upload")
async def upload_prescription(file: UploadFile = File(...)):
    """
    Upload a prescription image.
    """

    # Validate file type
    if file.content_type not in [
        "image/jpeg",
        "image/png",
        "image/jpg"
    ]:
        return {
            "success": False,
            "message": "Only JPG, JPEG and PNG images are allowed."
        }

    # Generate unique filename
    unique_filename = f"{uuid4()}_{file.filename}"

    file_path = os.path.join(
        UPLOAD_DIR,
        unique_filename
    )

    # Save image
    with open(file_path, "wb") as buffer:
        shutil.copyfileobj(file.file, buffer)

    return {
        "success": True,
        "filename": unique_filename,
        "message": "Prescription uploaded successfully."
    }