from __future__ import annotations

from typing import List, Optional
from uuid import UUID
from fastapi import APIRouter, Depends, HTTPException, Query
from sqlalchemy.orm import Session

from app.db.database import get_db
from app.services.calendar_dates_service import CalendarDatesService
from app.schemas.calendar_dates import CalendarDatesRead as CalendarDatesSchema, CalendarDatesCreate, CalendarDatesUpdate

router = APIRouter()


@router.get("/", response_model=List[CalendarDatesSchema], summary="List all calendar dates")
async def list_calendar_dates(
    snapshot_id: Optional[UUID] = Query(None), skip: int = Query(0, ge=0),
    limit: int = Query(100, ge=1, le=1000), db: Session = Depends(get_db)
):
    service = CalendarDatesService(db)
    return service.get_all(snapshot_id=snapshot_id, skip=skip, limit=limit)


@router.post("/", response_model=CalendarDatesSchema, summary="Create new calendar date")
async def create_calendar_date(
    calendar_date: CalendarDatesCreate, snapshot_id: UUID = Query(...), db: Session = Depends(get_db)
):
    service = CalendarDatesService(db)
    return service.create(calendar_date, snapshot_id)


@router.get("/service/{service_id}", response_model=List[CalendarDatesSchema], summary="Get calendar dates by service")
async def get_calendar_dates_by_service(
    service_id: str, snapshot_id: Optional[UUID] = Query(None), db: Session = Depends(get_db)
):
    service = CalendarDatesService(db)
    return service.get_by_service(service_id, snapshot_id)


@router.get("/filter/exceptions", response_model=List[CalendarDatesSchema], summary="Get exception dates")
async def get_exception_dates(
    snapshot_id: Optional[UUID] = Query(None), db: Session = Depends(get_db)
):
    service = CalendarDatesService(db)
    return service.get_exceptions(snapshot_id)
