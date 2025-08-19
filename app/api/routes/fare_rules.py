from __future__ import annotations

from typing import List, Optional
from uuid import UUID
from fastapi import APIRouter, Depends, HTTPException, Query
from sqlalchemy.orm import Session

from app.db.database import get_db
from app.services.fare_rules_service import FareRulesService
from app.schemas.fare_rules import FareRulesRead as FareRulesSchema, FareRulesCreate, FareRulesUpdate

router = APIRouter()


@router.get("/", response_model=List[FareRulesSchema], summary="List all fare rules")
async def list_fare_rules(
    snapshot_id: Optional[UUID] = Query(None), skip: int = Query(0, ge=0),
    limit: int = Query(100, ge=1, le=1000), db: Session = Depends(get_db)
):
    service = FareRulesService(db)
    return service.get_all(snapshot_id=snapshot_id, skip=skip, limit=limit)


@router.post("/", response_model=FareRulesSchema, summary="Create new fare rule")
async def create_fare_rule(
    fare_rule: FareRulesCreate, snapshot_id: UUID = Query(...), db: Session = Depends(get_db)
):
    service = FareRulesService(db)
    return service.create(fare_rule, snapshot_id)


@router.get("/route/{route_id}", response_model=List[FareRulesSchema], summary="Get fare rules by route")
async def get_fare_rules_by_route(
    route_id: str, snapshot_id: Optional[UUID] = Query(None), db: Session = Depends(get_db)
):
    service = FareRulesService(db)
    return service.get_by_route(route_id, snapshot_id)


@router.get("/fare/{fare_id}", response_model=List[FareRulesSchema], summary="Get fare rules by fare")
async def get_fare_rules_by_fare(
    fare_id: str, snapshot_id: Optional[UUID] = Query(None), db: Session = Depends(get_db)
):
    service = FareRulesService(db)
    return service.get_by_fare(fare_id, snapshot_id)
