from __future__ import annotations

from typing import List, Optional
from uuid import UUID
from fastapi import APIRouter, Depends, HTTPException, Query
from sqlalchemy.orm import Session

from app.db.database import get_db
from app.services.stop_times_service import StopTimesService
from app.schemas.stop_times import StopTimesRead as StopTimesSchema, StopTimesCreate, StopTimesUpdate

router = APIRouter()


@router.get("/", response_model=List[StopTimesSchema], summary="List all stop times")
async def list_stop_times(
    snapshot_id: Optional[UUID] = Query(None), skip: int = Query(0, ge=0),
    limit: int = Query(100, ge=1, le=1000), db: Session = Depends(get_db)
):
    service = StopTimesService(db)
    return service.get_all(snapshot_id=snapshot_id, skip=skip, limit=limit)


@router.post("/", response_model=StopTimesSchema, summary="Create new stop time")
async def create_stop_time(
    stop_time: StopTimesCreate, snapshot_id: UUID = Query(...), db: Session = Depends(get_db)
):
    service = StopTimesService(db)
    return service.create(stop_time, snapshot_id)


@router.get("/trip/{trip_id}", response_model=List[StopTimesSchema], summary="Get stop times by trip")
async def get_stop_times_by_trip(
    trip_id: str, snapshot_id: Optional[UUID] = Query(None), db: Session = Depends(get_db)
):
    service = StopTimesService(db)
    return service.get_by_trip(trip_id, snapshot_id)


@router.get("/stop/{stop_id}", response_model=List[StopTimesSchema], summary="Get stop times by stop")
async def get_stop_times_by_stop(
    stop_id: str, snapshot_id: Optional[UUID] = Query(None), db: Session = Depends(get_db)
):
    service = StopTimesService(db)
    return service.get_by_stop(stop_id, snapshot_id)


@router.get("/stop/{stop_id}/schedule", response_model=List[StopTimesSchema], summary="Get stop schedule")
async def get_stop_schedule(
    stop_id: str,
    start_time: str = Query("00:00:00", description="Start time (HH:MM:SS)"),
    end_time: str = Query("23:59:59", description="End time (HH:MM:SS)"),
    snapshot_id: Optional[UUID] = Query(None), db: Session = Depends(get_db)
):
    service = StopTimesService(db)
    return service.get_schedule_for_stop(stop_id, start_time, end_time, snapshot_id)
