from __future__ import annotations

from typing import List, Optional
from uuid import UUID
from fastapi import APIRouter, Depends, HTTPException, Query
from sqlalchemy.orm import Session

from app.db.database import get_db
from app.services.shapes_service import ShapesService
from app.schemas.shapes import ShapesRead as ShapesSchema, ShapesCreate, ShapesUpdate

router = APIRouter()


@router.get("/", response_model=List[ShapesSchema], summary="List all shapes")
async def list_shapes(
    snapshot_id: Optional[UUID] = Query(None), skip: int = Query(0, ge=0),
    limit: int = Query(100, ge=1, le=1000), db: Session = Depends(get_db)
):
    service = ShapesService(db)
    return service.get_all(snapshot_id=snapshot_id, skip=skip, limit=limit)


@router.post("/", response_model=ShapesSchema, summary="Create new shape point")
async def create_shape(
    shape: ShapesCreate, snapshot_id: UUID = Query(...), db: Session = Depends(get_db)
):
    service = ShapesService(db)
    return service.create(shape, snapshot_id)


@router.get("/shape/{shape_id}", response_model=List[ShapesSchema], summary="Get all points for a shape")
async def get_shape_points(
    shape_id: str, snapshot_id: Optional[UUID] = Query(None), db: Session = Depends(get_db)
):
    service = ShapesService(db)
    return service.get_by_shape_id(shape_id, snapshot_id)


@router.get("/list/shape-ids", summary="Get all shape IDs")
async def get_shape_ids(
    snapshot_id: Optional[UUID] = Query(None), db: Session = Depends(get_db)
):
    service = ShapesService(db)
    return {"shape_ids": service.get_shape_ids(snapshot_id)}
