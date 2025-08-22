from __future__ import annotations

from typing import List, Optional
from uuid import UUID
from sqlalchemy.orm import Session
from sqlalchemy import and_

from app.models.routes import Routes
from app.schemas.routes import RoutesCreate, RoutesUpdate
from app.services.base_service import BaseService


class RoutesService(BaseService[Routes, RoutesCreate, RoutesUpdate]):
    """Routes tablosu için özel servis"""
    
    def __init__(self, db: Session):
        super().__init__(Routes, db)
    
    # ROUTES-SPESİFİK OPERASYONLAR
    
    def get_by_agency(self, agency_id: str, snapshot_id: Optional[UUID] = None) -> List[Routes]:
        """Agency ID'ye göre route'ları getir"""
        query = self.db.query(Routes).filter(Routes.agency_id == agency_id)
        
        if snapshot_id:
            query = query.filter(Routes.snapshot_id == str(snapshot_id))
        
        return query.all()
    
    def get_by_route_type(self, route_type: int, snapshot_id: Optional[UUID] = None) -> List[Routes]:
        """Route tipi ile ara (0=Tram, 1=Metro, 2=Rail, 3=Bus, etc.)"""
        query = self.db.query(Routes).filter(Routes.route_type == route_type)
        
        if snapshot_id:
            query = query.filter(Routes.snapshot_id == str(snapshot_id))
        
        return query.all()
    
    def search_routes(
        self,
        short_name: Optional[str] = None,
        long_name: Optional[str] = None,
        route_type: Optional[int] = None,
        agency_id: Optional[str] = None,
        snapshot_id: Optional[UUID] = None,
        skip: int = 0,
        limit: int = 100
    ) -> List[Routes]:
        """Gelişmiş route arama"""
        query = self.db.query(Routes)
        
        if short_name:
            query = query.filter(Routes.route_short_name.ilike(f"%{short_name}%"))
        
        if long_name:
            query = query.filter(Routes.route_long_name.ilike(f"%{long_name}%"))
        
        if route_type is not None:
            query = query.filter(Routes.route_type == route_type)
        
        if agency_id:
            query = query.filter(Routes.agency_id == agency_id)
        
        if snapshot_id:
            query = query.filter(Routes.snapshot_id == str(snapshot_id))
        
        return query.offset(skip).limit(limit).all()
    
    def get_route_types_summary(self, snapshot_id: Optional[UUID] = None) -> List[dict]:
        """Route tiplerinin özeti (kaç tane bus, metro vs.)"""
        from sqlalchemy import func
        
        query = self.db.query(
            Routes.route_type,
            func.count(Routes.route_id).label('count')
        ).group_by(Routes.route_type)
        
        if snapshot_id:
            query = query.filter(Routes.snapshot_id == str(snapshot_id))
        
        results = query.all()
        
        # Route type açıklamaları
        type_names = {
            0: "Tram/Light Rail",
            1: "Metro/Subway", 
            2: "Rail",
            3: "Bus",
            4: "Ferry",
            5: "Cable Car",
            6: "Gondola",
            7: "Funicular"
        }
        
        return [
            {
                "route_type": r.route_type,
                "type_name": type_names.get(r.route_type, f"Unknown ({r.route_type})"),
                "count": r.count
            }
            for r in results
        ]
    
    def get_routes_with_colors(self, snapshot_id: Optional[UUID] = None) -> List[Routes]:
        """Rengi olan route'ları getir"""
        query = self.db.query(Routes).filter(Routes.route_color.isnot(None))
        
        if snapshot_id:
            query = query.filter(Routes.snapshot_id == str(snapshot_id))
        
        return query.all()
