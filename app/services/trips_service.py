from __future__ import annotations

from typing import List, Optional
from uuid import UUID
from sqlalchemy.orm import Session
from sqlalchemy import and_, func

from app.models.trips import Trips
from app.schemas.trips import TripsCreate, TripsUpdate
from app.services.base_service import BaseService


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
