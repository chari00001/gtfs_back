from __future__ import annotations

from sqlalchemy import create_engine
# Base is now imported from models.base
from sqlalchemy.orm import sessionmaker

from app.core.config import get_settings

settings = get_settings()

# PostgreSQL veritabanı bağlantı URL'si
DATABASE_URL = settings.DATABASE_URL

# SQLAlchemy engine oluştur
engine = create_engine(DATABASE_URL)

# Session factory oluştur
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

# Base model sınıfı - will be imported separately to avoid circular imports


def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()
