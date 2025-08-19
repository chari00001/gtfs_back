from __future__ import annotations

from typing import List, Optional
from uuid import UUID
from sqlalchemy.orm import Session

from app.models.calendar import Calendar
from app.schemas.calendar import CalendarCreate, CalendarUpdate
from app.services.base_service import BaseService


class CalendarService(BaseService[Calendar, CalendarCreate, CalendarUpdate]):
    """Calendar tablosu için özel servis"""
    
    def __init__(self, db: Session):
        super().__init__(Calendar, db)
    
    def get_active_services(self, snapshot_id: Optional[UUID] = None) -> List[Calendar]:
        """Aktif servisleri getir (en az bir gün çalışan)"""
        query = self.db.query(Calendar).filter(
            (Calendar.monday == 1) |
            (Calendar.tuesday == 1) |
            (Calendar.wednesday == 1) |
            (Calendar.thursday == 1) |
            (Calendar.friday == 1) |
            (Calendar.saturday == 1) |
            (Calendar.sunday == 1)
        )
        
        if snapshot_id:
            query = query.filter(Calendar.snapshot_id == snapshot_id)
        
        return query.all()
    
    def get_weekend_services(self, snapshot_id: Optional[UUID] = None) -> List[Calendar]:
        """Hafta sonu çalışan servisleri getir"""
        query = self.db.query(Calendar).filter(
            (Calendar.saturday == 1) | (Calendar.sunday == 1)
        )
        
        if snapshot_id:
            query = query.filter(Calendar.snapshot_id == snapshot_id)
        
        return query.all()
