from __future__ import annotations

import uuid
from datetime import datetime
from sqlalchemy import Column, String, DateTime, inspect
from sqlalchemy.ext.declarative import declarative_base

Base = declarative_base()


class GTFSBase(Base):
    __abstract__ = True
    
    snapshot_id = Column(String, nullable=False, default=lambda: str(uuid.uuid4()))
    created_at = Column(DateTime, default=datetime.utcnow)
    updated_at = Column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)
    
    @classmethod
    def get_primary_key_column(cls):
        """Primary key sütununu döndür"""
        mapper = inspect(cls)
        return mapper.primary_key[0]
