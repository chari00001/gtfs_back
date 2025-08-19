from __future__ import annotations

from typing import List, Optional
from uuid import UUID
from fastapi import APIRouter, Depends, HTTPException, Query
from sqlalchemy.orm import Session

from app.db.database import get_db
from app.services.calendar_service import CalendarService
from app.schemas.calendar import CalendarRead as CalendarSchema, CalendarCreate, CalendarUpdate

router = APIRouter()


@router.get("/", response_model=List[CalendarSchema], summary="List all calendar services")
async def list_calendar_services(
    snapshot_id: Optional[UUID] = Query(None), skip: int = Query(0, ge=0),
    limit: int = Query(100, ge=1, le=1000), db: Session = Depends(get_db)
):
    service = CalendarService(db)
    return service.get_all(snapshot_id=snapshot_id, skip=skip, limit=limit)


@router.get("/{service_id}", response_model=CalendarSchema, summary="Get calendar service by ID")
async def get_calendar_service(
    service_id: str, snapshot_id: Optional[UUID] = Query(None), db: Session = Depends(get_db)
):
    service = CalendarService(db)
    calendar = service.get_by_id(service_id, snapshot_id)
    if not calendar:
        raise HTTPException(status_code=404, detail="Calendar service not found")
    return calendar


@router.post("/", response_model=CalendarSchema, summary="Create new calendar service")
async def create_calendar_service(
    calendar: CalendarCreate, snapshot_id: UUID = Query(...), db: Session = Depends(get_db)
):
    service = CalendarService(db)
    return service.create(calendar, snapshot_id)


@router.get("/filter/active", response_model=List[CalendarSchema], summary="Get active services")
async def get_active_services(
    snapshot_id: Optional[UUID] = Query(None), db: Session = Depends(get_db)
):
    service = CalendarService(db)
    return service.get_active_services(snapshot_id)


@router.get("/filter/weekend", response_model=List[CalendarSchema], summary="Get weekend services")
async def get_weekend_services(
    snapshot_id: Optional[UUID] = Query(None), db: Session = Depends(get_db)
):
    service = CalendarService(db)
    return service.get_weekend_services(snapshot_id)
