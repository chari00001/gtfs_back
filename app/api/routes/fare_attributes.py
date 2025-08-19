from __future__ import annotations

from typing import List, Optional
from uuid import UUID
from fastapi import APIRouter, Depends, HTTPException, Query
from sqlalchemy.orm import Session

from app.db.database import get_db
from app.services.fare_attributes_service import FareAttributesService
from app.schemas.fare_attributes import FareAttributesRead as FareAttributesSchema, FareAttributesCreate, FareAttributesUpdate

router = APIRouter()


@router.get("/", response_model=List[FareAttributesSchema], summary="List all fare attributes")
async def list_fare_attributes(
    snapshot_id: Optional[UUID] = Query(None), skip: int = Query(0, ge=0),
    limit: int = Query(100, ge=1, le=1000), db: Session = Depends(get_db)
):
    service = FareAttributesService(db)
    return service.get_all(snapshot_id=snapshot_id, skip=skip, limit=limit)


@router.get("/{fare_id}", response_model=FareAttributesSchema, summary="Get fare attribute by ID")
async def get_fare_attribute(
    fare_id: str, snapshot_id: Optional[UUID] = Query(None), db: Session = Depends(get_db)
):
    service = FareAttributesService(db)
    fare = service.get_by_id(fare_id, snapshot_id)
    if not fare:
        raise HTTPException(status_code=404, detail="Fare attribute not found")
    return fare


@router.post("/", response_model=FareAttributesSchema, summary="Create new fare attribute")
async def create_fare_attribute(
    fare: FareAttributesCreate, snapshot_id: UUID = Query(...), db: Session = Depends(get_db)
):
    service = FareAttributesService(db)
    return service.create(fare, snapshot_id)


@router.get("/agency/{agency_id}", response_model=List[FareAttributesSchema], summary="Get fare attributes by agency")
async def get_fare_attributes_by_agency(
    agency_id: str, snapshot_id: Optional[UUID] = Query(None), db: Session = Depends(get_db)
):
    service = FareAttributesService(db)
    return service.get_by_agency(agency_id, snapshot_id)


@router.get("/currency/{currency_type}", response_model=List[FareAttributesSchema], summary="Get fare attributes by currency")
async def get_fare_attributes_by_currency(
    currency_type: str, snapshot_id: Optional[UUID] = Query(None), db: Session = Depends(get_db)
):
    service = FareAttributesService(db)
    return service.get_by_currency(currency_type, snapshot_id)
