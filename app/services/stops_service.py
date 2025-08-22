from __future__ import annotations

from typing import List, Optional, Tuple
from uuid import UUID
from sqlalchemy.orm import Session
from sqlalchemy import and_, func, text

from app.models.stops import Stops
from app.schemas.stops import StopsCreate, StopsUpdate
from app.services.base_service import BaseService


class StopsService(BaseService[Stops, StopsCreate, StopsUpdate]):
    """Stops tablosu için özel servis"""
    
    def __init__(self, db: Session):
        super().__init__(Stops, db)
    
    # STOPS-SPESİFİK OPERASYONLAR
    
    def search_by_name(self, name: str, snapshot_id: Optional[UUID] = None) -> List[Stops]:
        """Stop adı ile ara"""
        query = self.db.query(Stops).filter(Stops.stop_name.ilike(f"%{name}%"))
        
        if snapshot_id:
            query = query.filter(Stops.snapshot_id == str(snapshot_id))
        
        return query.all()
    
    def get_stops_in_bounding_box(
        self,
        min_lat: float,
        max_lat: float, 
        min_lon: float,
        max_lon: float,
        snapshot_id: Optional[UUID] = None
    ) -> List[Stops]:
        """Belirli bir coğrafi alan içindeki stop'ları getir"""
        query = self.db.query(Stops).filter(
            and_(
                Stops.stop_lat >= min_lat,
                Stops.stop_lat <= max_lat,
                Stops.stop_lon >= min_lon,
                Stops.stop_lon <= max_lon
            )
        )
        
        if snapshot_id:
            query = query.filter(Stops.snapshot_id == str(snapshot_id))
        
        return query.all()
    
    def find_nearby_stops(
        self,
        latitude: float,
        longitude: float,
        radius_km: float = 1.0,
        snapshot_id: Optional[UUID] = None,
        limit: int = 50
    ) -> List[Tuple[Stops, float]]:
        """Belirli bir noktaya yakın stop'ları mesafe ile getir"""
        # Basit koordinat tabanlı filtre (yaklaşık)
        # Radius'u derece cinsine çevir (kabaca 1 derece = 111 km)
        degree_radius = radius_km / 111.0
        
        query = self.db.query(Stops).filter(
            and_(
                Stops.stop_lat >= latitude - degree_radius,
                Stops.stop_lat <= latitude + degree_radius,
                Stops.stop_lon >= longitude - degree_radius,
                Stops.stop_lon <= longitude + degree_radius
            )
        )
        
        if snapshot_id:
            query = query.filter(Stops.snapshot_id == str(snapshot_id))
        
        results = query.limit(limit).all()
        
        # Basit mesafe hesaplama (Euclidean distance yaklaşımı)
        nearby_stops = []
        for stop in results:
            # Kabaca mesafe hesaplama
            lat_diff = float(stop.stop_lat) - latitude
            lon_diff = float(stop.stop_lon) - longitude
            distance = (lat_diff**2 + lon_diff**2)**0.5 * 111  # km cinsine çevir
            
            if distance <= radius_km:
                nearby_stops.append((stop, round(distance, 3)))
        
        # Mesafeye göre sırala
        nearby_stops.sort(key=lambda x: x[1])
        return nearby_stops[:limit]
    
    def get_stops_by_zone(self, zone_id: str, snapshot_id: Optional[UUID] = None) -> List[Stops]:
        """Zone ID'ye göre stop'ları getir"""
        query = self.db.query(Stops).filter(Stops.zone_id == zone_id)
        
        if snapshot_id:
            query = query.filter(Stops.snapshot_id == str(snapshot_id))
        
        return query.all()
    
    def get_stops_with_urls(self, snapshot_id: Optional[UUID] = None) -> List[Stops]:
        """URL'si olan stop'ları getir"""
        query = self.db.query(Stops).filter(Stops.stop_url.isnot(None))
        
        if snapshot_id:
            query = query.filter(Stops.snapshot_id == str(snapshot_id))
        
        return query.all()
    
    def get_geographic_bounds(self, snapshot_id: Optional[UUID] = None) -> dict:
        """Tüm stop'ların coğrafi sınırlarını getir"""
        query = self.db.query(
            func.min(Stops.stop_lat).label('min_lat'),
            func.max(Stops.stop_lat).label('max_lat'),
            func.min(Stops.stop_lon).label('min_lon'),
            func.max(Stops.stop_lon).label('max_lon')
        )
        
        if snapshot_id:
            query = query.filter(Stops.snapshot_id == str(snapshot_id))
        
        result = query.first()
        
        return {
            "min_latitude": float(result.min_lat) if result.min_lat else None,
            "max_latitude": float(result.max_lat) if result.max_lat else None,
            "min_longitude": float(result.min_lon) if result.min_lon else None,
            "max_longitude": float(result.max_lon) if result.max_lon else None
        }
