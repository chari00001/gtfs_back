from __future__ import annotations

from typing import List, Optional
from uuid import UUID
from fastapi import APIRouter, Depends, HTTPException, Query
from sqlalchemy.orm import Session

from app.db.database import get_db
from app.services.routes_service import RoutesService
from app.schemas.routes import RoutesRead as RoutesSchema, RoutesCreate, RoutesUpdate

router = APIRouter()


@router.get("/", response_model=List[RoutesSchema], summary="List all routes")
async def list_routes(
    snapshot_id: Optional[UUID] = Query(None, description="Filter by snapshot ID"),
    skip: int = Query(0, ge=0, description="Records to skip"),
    limit: int = Query(100, ge=1, le=1000, description="Max records to return"),
    db: Session = Depends(get_db)
):
    """Tüm route'ları listele"""
    service = RoutesService(db)
    return service.get_all(snapshot_id=snapshot_id, skip=skip, limit=limit)


@router.get("/{route_id}", response_model=RoutesSchema, summary="Get route by ID")
async def get_route(
    route_id: str,
    snapshot_id: Optional[UUID] = Query(None, description="Filter by snapshot ID"),
    db: Session = Depends(get_db)
):
    """ID ile route getir"""
    service = RoutesService(db)
    route = service.get_by_id(route_id, snapshot_id)
    
    if not route:
        raise HTTPException(status_code=404, detail="Route not found")
    
    return route


@router.post("/", response_model=RoutesSchema, summary="Create new route")
async def create_route(
    route: RoutesCreate,
    snapshot_id: UUID = Query(..., description="Snapshot ID"),
    db: Session = Depends(get_db)
):
    """Yeni route oluştur"""
    service = RoutesService(db)
    return service.create(route, snapshot_id)


@router.put("/{route_id}", response_model=RoutesSchema, summary="Update route")
async def update_route(
    route_id: str,
    route: RoutesUpdate,
    snapshot_id: Optional[UUID] = Query(None, description="Filter by snapshot ID"),
    db: Session = Depends(get_db)
):
    """Route güncelle"""
    service = RoutesService(db)
    updated_route = service.update(route_id, route, snapshot_id)
    
    if not updated_route:
        raise HTTPException(status_code=404, detail="Route not found")
    
    return updated_route


@router.delete("/{route_id}", summary="Delete route")
async def delete_route(
    route_id: str,
    snapshot_id: Optional[UUID] = Query(None, description="Filter by snapshot ID"),
    db: Session = Depends(get_db)
):
    """Route sil"""
    service = RoutesService(db)
    success = service.delete(route_id, snapshot_id)
    
    if not success:
        raise HTTPException(status_code=404, detail="Route not found")
    
    return {"message": "Route deleted successfully"}


@router.get("/agency/{agency_id}", response_model=List[RoutesSchema], summary="Get routes by agency")
async def get_routes_by_agency(
    agency_id: str,
    snapshot_id: Optional[UUID] = Query(None, description="Filter by snapshot ID"),
    db: Session = Depends(get_db)
):
    """Agency'ye göre route'ları getir"""
    service = RoutesService(db)
    return service.get_by_agency(agency_id, snapshot_id)


@router.get("/type/{route_type}", response_model=List[RoutesSchema], summary="Get routes by type")
async def get_routes_by_type(
    route_type: int,
    snapshot_id: Optional[UUID] = Query(None, description="Filter by snapshot ID"),
    db: Session = Depends(get_db)
):
    """Route tipine göre route'ları getir"""
    service = RoutesService(db)
    return service.get_by_route_type(route_type, snapshot_id)


@router.get("/search/advanced", response_model=List[RoutesSchema], summary="Advanced route search")
async def search_routes(
    short_name: Optional[str] = Query(None, description="Route short name"),
    long_name: Optional[str] = Query(None, description="Route long name"),
    route_type: Optional[int] = Query(None, ge=0, le=7, description="Route type"),
    agency_id: Optional[str] = Query(None, description="Agency ID"),
    snapshot_id: Optional[UUID] = Query(None, description="Filter by snapshot ID"),
    skip: int = Query(0, ge=0, description="Records to skip"),
    limit: int = Query(100, ge=1, le=1000, description="Max records to return"),
    db: Session = Depends(get_db)
):
    """Gelişmiş route arama"""
    service = RoutesService(db)
    return service.search_routes(
        short_name=short_name,
        long_name=long_name,
        route_type=route_type,
        agency_id=agency_id,
        snapshot_id=snapshot_id,
        skip=skip,
        limit=limit
    )


@router.get("/stats/types", summary="Get route types summary")
async def get_route_types_summary(
    snapshot_id: Optional[UUID] = Query(None, description="Filter by snapshot ID"),
    db: Session = Depends(get_db)
):
    """Route tiplerinin özeti"""
    service = RoutesService(db)
    return service.get_route_types_summary(snapshot_id)


@router.get("/filter/with-colors", response_model=List[RoutesSchema], summary="Get routes with colors")
async def get_routes_with_colors(
    snapshot_id: Optional[UUID] = Query(None, description="Filter by snapshot ID"),
    db: Session = Depends(get_db)
):
    """Rengi olan route'ları getir"""
    service = RoutesService(db)
    return service.get_routes_with_colors(snapshot_id)
