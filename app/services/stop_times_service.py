from __future__ import annotations

from typing import List, Optional
from uuid import UUID
from sqlalchemy.orm import Session
from sqlalchemy import and_, func

from app.models.stop_times import StopTimes
from app.schemas.stop_times import StopTimesCreate, StopTimesUpdate
from app.services.base_service import BaseService


class StopTimesService(BaseService[StopTimes, StopTimesCreate, StopTimesUpdate]):
    """StopTimes tablosu için özel servis"""
    
    def __init__(self, db: Session):
        super().__init__(StopTimes, db)
    
    def get_by_trip(self, trip_id: str, snapshot_id: Optional[UUID] = None) -> List[StopTimes]:
        """Trip ID'ye göre stop time'ları getir"""
        query = self.db.query(StopTimes).filter(StopTimes.trip_id == trip_id) \
                                       .order_by(StopTimes.stop_sequence)
        
        if snapshot_id:
            query = query.filter(StopTimes.snapshot_id == str(snapshot_id))
        
        return query.all()
    
    def get_by_stop(self, stop_id: str, snapshot_id: Optional[UUID] = None) -> List[StopTimes]:
        """Stop ID'ye göre stop time'ları getir"""
        query = self.db.query(StopTimes).filter(StopTimes.stop_id == stop_id) \
                                       .order_by(StopTimes.arrival_time)
        
        if snapshot_id:
            query = query.filter(StopTimes.snapshot_id == str(snapshot_id))
        
        return query.all()
    
    def get_schedule_for_stop(
        self, 
        stop_id: str, 
        start_time: str = "00:00:00",
        end_time: str = "23:59:59",
        snapshot_id: Optional[UUID] = None
    ) -> List[StopTimes]:
        """Belirli bir stop için zaman aralığındaki schedule'ı getir"""
        query = self.db.query(StopTimes).filter(
            and_(
                StopTimes.stop_id == stop_id,
                StopTimes.arrival_time >= start_time,
                StopTimes.arrival_time <= end_time
            )
        ).order_by(StopTimes.arrival_time)
        
        if snapshot_id:
            query = query.filter(StopTimes.snapshot_id == str(snapshot_id))
        
        return query.all()
