from __future__ import annotations

from typing import List, Optional
from uuid import UUID
from sqlalchemy.orm import Session

from app.models.calendar import CalendarDates
from app.schemas.calendar_dates import CalendarDatesCreate, CalendarDatesUpdate
from app.services.base_service import BaseService


class CalendarDatesService(BaseService[CalendarDates, CalendarDatesCreate, CalendarDatesUpdate]):
    """CalendarDates tablosu için özel servis"""
    
    def __init__(self, db: Session):
        super().__init__(CalendarDates, db)
    
    def get_by_service(self, service_id: str, snapshot_id: Optional[UUID] = None) -> List[CalendarDates]:
        """Service ID'ye göre özel günleri getir"""
        query = self.db.query(CalendarDates).filter(CalendarDates.service_id == service_id)
        
        if snapshot_id:
            query = query.filter(CalendarDates.snapshot_id == str(snapshot_id))
        
        return query.all()
    
    def get_exceptions(self, snapshot_id: Optional[UUID] = None) -> List[CalendarDates]:
        """İstisna günleri getir (exception_type=2)"""
        query = self.db.query(CalendarDates).filter(CalendarDates.exception_type == 2)
        
        if snapshot_id:
            query = query.filter(CalendarDates.snapshot_id == str(snapshot_id))
        
        return query.all()
