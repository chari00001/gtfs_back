from __future__ import annotations

from typing import List, Optional
from uuid import UUID
from sqlalchemy.orm import Session
from sqlalchemy import distinct, and_, func, desc
from datetime import datetime

from app.models.trips import Trips
from app.schemas.trips import TripsCreate, TripsUpdate
from app.services.base_service import BaseService
from app.models.routes import Routes
from app.models.stop_times import StopTimes


class TripsService(BaseService[Trips, TripsCreate, TripsUpdate]):
    """Trips tablosu için özel servis"""
    
    def __init__(self, db: Session):
        super().__init__(Trips, db)
    
    def get_by_route(self, route_id: str, snapshot_id: Optional[UUID] = None) -> List[Trips]:
        """Route ID'ye göre trip'leri getir"""
        query = self.db.query(Trips).filter(Trips.route_id == route_id)
        
        if snapshot_id:
            query = query.filter(Trips.snapshot_id == str(snapshot_id))
        
        return query.all()
    
    def get_by_agency(self, agency_id: str, snapshot_id: Optional[UUID] = None) -> List[Trips]:
        query = self.db.query(Trips).join(Routes, Trips.route_id == Routes.route_id).filter(Routes.agency_id == agency_id)
        
        if snapshot_id:
            query = query.filter(Trips.snapshot_id == str(snapshot_id))

        return query.all()
    
    def get_active_trips_now(
        self,
        skip: int = 0, 
        limit: int = 100,
        snapshot_id: Optional[UUID] = None) -> List[Trips]:
        """Şu anda aktif olan seferleri getir"""
        now = datetime.now()
        current_time_str = now.strftime("%H:%M:%S")
        
        # Şu anda aktif seferler: departure geçmiş, arrival henüz olmamış
        query = self.db.query(Trips).join(
            StopTimes, StopTimes.trip_id == Trips.trip_id
        ).filter(
            StopTimes.departure_time <= current_time_str,
            StopTimes.arrival_time >= current_time_str
        ).order_by(desc(self.model.created_at)).offset(skip).limit(limit)
        
        if snapshot_id:
            query = query.filter(Trips.snapshot_id == str(snapshot_id))
        
        return query.all()       
        
    
    def get_by_service(self, service_id: str, snapshot_id: Optional[UUID] = None) -> List[Trips]:
        """Service ID'ye göre trip'leri getir"""
        query = self.db.query(Trips).filter(Trips.service_id == service_id)
        
        if snapshot_id:
            query = query.filter(Trips.snapshot_id == str(snapshot_id))
        
        return query.all()
    
    def get_by_direction(self, direction_id: int, snapshot_id: Optional[UUID] = None) -> List[Trips]:
        """Yön ID'ye göre trip'leri getir (0=gidiş, 1=dönüş)"""
        query = self.db.query(Trips).filter(Trips.direction_id == direction_id)
        
        if snapshot_id:
            query = query.filter(Trips.snapshot_id == str(snapshot_id))
        
        return query.all()
    
    def get_trips_summary_by_route(self, snapshot_id: Optional[UUID] = None) -> List[dict]:
        """Route'lara göre trip sayıları"""
        query = self.db.query(
            Trips.route_id,
            func.count(Trips.trip_id).label('trip_count')
        ).group_by(Trips.route_id)
        
        if snapshot_id:
            query = query.filter(Trips.snapshot_id == str(snapshot_id))
        
        results = query.all()
        return [{"route_id": r.route_id, "trip_count": r.trip_count} for r in results]
