from __future__ import annotations

from typing import List, Optional
from uuid import UUID
from fastapi import APIRouter, Depends, HTTPException, Query
from sqlalchemy.orm import Session

from app.db.database import get_db
from app.services.stops_service import StopsService
from app.schemas.stops import StopsRead as StopsSchema, StopsCreate, StopsUpdate

router = APIRouter()


@router.get("/", response_model=List[StopsSchema], summary="List all stops")
async def list_stops(
    snapshot_id: Optional[UUID] = Query(None, description="Filter by snapshot ID"),
    skip: int = Query(0, ge=0, description="Records to skip"),
    limit: int = Query(100, ge=1, le=1000, description="Max records to return"),
    db: Session = Depends(get_db)
):
    """Tüm stop'ları listele"""
    service = StopsService(db)
    return service.get_all(snapshot_id=snapshot_id, skip=skip, limit=limit)


@router.get("/{stop_id}", response_model=StopsSchema, summary="Get stop by ID")
async def get_stop(
    stop_id: str,
    snapshot_id: Optional[UUID] = Query(None, description="Filter by snapshot ID"),
    db: Session = Depends(get_db)
):
    """ID ile stop getir"""
    service = StopsService(db)
    stop = service.get_by_id(stop_id, snapshot_id)
    
    if not stop:
        raise HTTPException(status_code=404, detail="Stop not found")
    
    return stop


@router.post("/", response_model=StopsSchema, summary="Create new stop")
async def create_stop(
    stop: StopsCreate,
    snapshot_id: UUID = Query(..., description="Snapshot ID"),
    db: Session = Depends(get_db)
):
    """Yeni stop oluştur"""
    service = StopsService(db)
    return service.create(stop, snapshot_id)


@router.put("/{stop_id}", response_model=StopsSchema, summary="Update stop")
async def update_stop(
    stop_id: str,
    stop: StopsUpdate,
    snapshot_id: Optional[UUID] = Query(None, description="Filter by snapshot ID"),
    db: Session = Depends(get_db)
):
    """Stop güncelle"""
    service = StopsService(db)
    updated_stop = service.update(stop_id, stop, snapshot_id)
    
    if not updated_stop:
        raise HTTPException(status_code=404, detail="Stop not found")
    
    return updated_stop


@router.delete("/{stop_id}", summary="Delete stop")
async def delete_stop(
    stop_id: str,
    snapshot_id: Optional[UUID] = Query(None, description="Filter by snapshot ID"),
    db: Session = Depends(get_db)
):
    """Stop sil"""
    service = StopsService(db)
    success = service.delete(stop_id, snapshot_id)
    
    if not success:
        raise HTTPException(status_code=404, detail="Stop not found")
    
    return {"message": "Stop deleted successfully"}


@router.get("/search/by-name", response_model=List[StopsSchema], summary="Search stops by name")
async def search_stops_by_name(
    name: str = Query(..., description="Stop name to search"),
    snapshot_id: Optional[UUID] = Query(None, description="Filter by snapshot ID"),
    db: Session = Depends(get_db)
):
    """Stop adı ile ara"""
    service = StopsService(db)
    return service.search_by_name(name, snapshot_id)


@router.get("/search/nearby", summary="Find nearby stops")
async def find_nearby_stops(
    latitude: float = Query(..., ge=-90, le=90, description="Latitude"),
    longitude: float = Query(..., ge=-180, le=180, description="Longitude"),
    radius_km: float = Query(1.0, gt=0, le=50, description="Search radius in kilometers"),
    snapshot_id: Optional[UUID] = Query(None, description="Filter by snapshot ID"),
    limit: int = Query(50, ge=1, le=200, description="Max stops to return"),
    db: Session = Depends(get_db)
):
    """Yakındaki stop'ları bul"""
    service = StopsService(db)
    results = service.find_nearby_stops(latitude, longitude, radius_km, snapshot_id, limit)
    
    return [
        {
            "stop": stop,
            "distance_km": round(distance, 3)
        }
        for stop, distance in results
    ]


@router.get("/search/in-bounds", response_model=List[StopsSchema], summary="Get stops in bounding box")
async def get_stops_in_bounds(
    min_lat: float = Query(..., ge=-90, le=90, description="Minimum latitude"),
    max_lat: float = Query(..., ge=-90, le=90, description="Maximum latitude"),
    min_lon: float = Query(..., ge=-180, le=180, description="Minimum longitude"),
    max_lon: float = Query(..., ge=-180, le=180, description="Maximum longitude"),
    snapshot_id: Optional[UUID] = Query(None, description="Filter by snapshot ID"),
    db: Session = Depends(get_db)
):
    """Coğrafi sınırlar içindeki stop'ları getir"""
    service = StopsService(db)
    return service.get_stops_in_bounding_box(min_lat, max_lat, min_lon, max_lon, snapshot_id)


@router.get("/zone/{zone_id}", response_model=List[StopsSchema], summary="Get stops by zone")
async def get_stops_by_zone(
    zone_id: str,
    snapshot_id: Optional[UUID] = Query(None, description="Filter by snapshot ID"),
    db: Session = Depends(get_db)
):
    """Zone ID'ye göre stop'ları getir"""
    service = StopsService(db)
    return service.get_stops_by_zone(zone_id, snapshot_id)


@router.get("/stats/bounds", summary="Get geographic bounds")
async def get_geographic_bounds(
    snapshot_id: Optional[UUID] = Query(None, description="Filter by snapshot ID"),
    db: Session = Depends(get_db)
):
    """Tüm stop'ların coğrafi sınırlarını getir"""
    service = StopsService(db)
    return service.get_geographic_bounds(snapshot_id)
