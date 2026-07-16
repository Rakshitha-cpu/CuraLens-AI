import os
import sqlite3

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
# Lightweight auto-migration
# ---------------------------------------
# create_all() only creates tables that don't exist yet - it never
# adds new columns to a table that's already there. Since this is a
# small SQLite-based project (not using Alembic), add any missing
# columns here manually so an existing local database picks up model
# changes without needing manual SQL. Safe to run on every startup -
# it only adds a column if it's actually missing.
def _run_lightweight_migrations():
    db_path = "scriptsense.db"

    if not os.path.exists(db_path):
        return  # fresh database, create_all() already handled it

    conn = sqlite3.connect(db_path)
    cursor = conn.cursor()

    cursor.execute("PRAGMA table_info(users)")
    existing_columns = {row[1] for row in cursor.fetchall()}

    if "failed_login_attempts" not in existing_columns:
        cursor.execute(
            "ALTER TABLE users ADD COLUMN failed_login_attempts INTEGER DEFAULT 0"
        )
        print("[migration] Added users.failed_login_attempts")

    if "locked_until" not in existing_columns:
        cursor.execute(
            "ALTER TABLE users ADD COLUMN locked_until DATETIME"
        )
        print("[migration] Added users.locked_until")

    conn.commit()
    conn.close()


_run_lightweight_migrations()

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
# FRONTEND_URL should be set in production to the deployed frontend's
# URL (e.g. https://curalens-ai.vercel.app). Localhost is always
# allowed for local development.
_extra_origin = os.getenv("FRONTEND_URL")

_allowed_origins = [
    "http://localhost:5173",
    "http://127.0.0.1:5173",
]

if _extra_origin:
    _allowed_origins.append(_extra_origin)

app.add_middleware(
    CORSMiddleware,
    allow_origins=_allowed_origins,
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