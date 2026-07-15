from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from app.database import engine, Base
from app.auth import models
from app.history import models as history_models

from app.api.health import router as health_router
from app.api.prescription import router as prescription_router
from app.api.ai import router as ai_router
from app.api.history import router as history_router
from app.auth.router import router as auth_router

# ---------------------------------------
# Create Database Tables
# ---------------------------------------
Base.metadata.create_all(bind=engine)

# ---------------------------------------
# FastAPI App
# ---------------------------------------
app = FastAPI(
    title="CuraLens AI",
    version="1.0.0",
    description="AI-Powered Prescription Intelligence"
)

# ---------------------------------------
# Enable CORS
# ---------------------------------------
app.add_middleware(
    CORSMiddleware,
    allow_origins=[
        "http://localhost:5173",
        "http://127.0.0.1:5173"
    ],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# ---------------------------------------
# Home Route
# ---------------------------------------
@app.get("/")
def home():
    return {
        "project": "CuraLens AI",
        "status": "Running",
        "version": "1.0.0"
    }

# ---------------------------------------
# Register Routers
# ---------------------------------------
app.include_router(health_router)
app.include_router(prescription_router)
app.include_router(ai_router)
app.include_router(history_router)
app.include_router(auth_router)