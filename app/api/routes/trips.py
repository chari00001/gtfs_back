from __future__ import annotations

from typing import List, Optional
from uuid import UUID
from fastapi import APIRouter, Depends, HTTPException, Query
from sqlalchemy.orm import Session

from app.db.database import get_db
from app.services.trips_service import TripsService
from app.schemas.trips import TripsRead as TripsSchema, TripsCreate, TripsUpdate

router = APIRouter()


@router.get("/", response_model=List[TripsSchema], summary="List all trips")
async def list_trips(
    snapshot_id: Optional[UUID] = Query(None, description="Filter by snapshot ID"),
    skip: int = Query(0, ge=0), limit: int = Query(100, ge=1, le=1000),
    db: Session = Depends(get_db)
):
    service = TripsService(db)
    return service.get_all(snapshot_id=snapshot_id, skip=skip, limit=limit)


@router.get("/{trip_id}", response_model=TripsSchema, summary="Get trip by ID")
async def get_trip(
    trip_id: str, snapshot_id: Optional[UUID] = Query(None), db: Session = Depends(get_db)
):
    service = TripsService(db)
    trip = service.get_by_id(trip_id, snapshot_id)
    if not trip:
        raise HTTPException(status_code=404, detail="Trip not found")
    return trip


@router.post("/", response_model=TripsSchema, summary="Create new trip")
async def create_trip(
    trip: TripsCreate, snapshot_id: UUID = Query(...), db: Session = Depends(get_db)
):
    service = TripsService(db)
    return service.create(trip, snapshot_id)


@router.get("/route/{route_id}", response_model=List[TripsSchema], summary="Get trips by route")
async def get_trips_by_route(
    route_id: str, snapshot_id: Optional[UUID] = Query(None), db: Session = Depends(get_db)
):
    service = TripsService(db)
    return service.get_by_route(route_id, snapshot_id)


@router.get("/service/{service_id}", response_model=List[TripsSchema], summary="Get trips by service")
async def get_trips_by_service(
    service_id: str, snapshot_id: Optional[UUID] = Query(None), db: Session = Depends(get_db)
):
    service = TripsService(db)
    return service.get_by_service(service_id, snapshot_id)


@router.get("/stats/by-route", summary="Get trips summary by route")
async def get_trips_summary_by_route(
    snapshot_id: Optional[UUID] = Query(None), db: Session = Depends(get_db)
):
    service = TripsService(db)
    return service.get_trips_summary_by_route(snapshot_id)
