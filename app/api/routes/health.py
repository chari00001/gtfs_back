from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from sqlalchemy import text

from app.db.database import get_db

router = APIRouter()


@router.get("/health", summary="Health check")
def health_check():
    return {"status": "ok"}


@router.get("/health/db", summary="Database health check")
def db_health_check(db: Session = Depends(get_db)):
    try:
        # Basit bir veritabanı sorgusu ile bağlantıyı test et
        db.execute(text("SELECT 1"))
        return {"status": "ok", "database": "connected"}
    except Exception as e:
        return {"status": "error", "database": "disconnected", "error": str(e)}


