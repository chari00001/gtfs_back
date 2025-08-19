from __future__ import annotations

from typing import List, Optional
from uuid import UUID
from fastapi import APIRouter, Depends, HTTPException, Query
from sqlalchemy.orm import Session

from app.db.database import get_db
from app.services.feed_info_service import FeedInfoService
from app.schemas.feed_info import FeedInfoRead as FeedInfoSchema, FeedInfoCreate, FeedInfoUpdate

router = APIRouter()


@router.get("/", response_model=List[FeedInfoSchema], summary="List all feed info")
async def list_feed_info(
    snapshot_id: Optional[UUID] = Query(None), skip: int = Query(0, ge=0),
    limit: int = Query(100, ge=1, le=1000), db: Session = Depends(get_db)
):
    service = FeedInfoService(db)
    return service.get_all(snapshot_id=snapshot_id, skip=skip, limit=limit)


@router.post("/", response_model=FeedInfoSchema, summary="Create new feed info")
async def create_feed_info(
    feed_info: FeedInfoCreate, snapshot_id: UUID = Query(...), db: Session = Depends(get_db)
):
    service = FeedInfoService(db)
    return service.create(feed_info, snapshot_id)


@router.get("/latest", response_model=FeedInfoSchema, summary="Get latest feed info")
async def get_latest_feed_info(
    snapshot_id: Optional[UUID] = Query(None), db: Session = Depends(get_db)
):
    service = FeedInfoService(db)
    feed_info = service.get_latest_feed(snapshot_id)
    if not feed_info:
        raise HTTPException(status_code=404, detail="Feed info not found")
    return feed_info


@router.get("/publisher/{publisher_name}", response_model=List[FeedInfoSchema], summary="Get feed info by publisher")
async def get_feed_info_by_publisher(
    publisher_name: str, snapshot_id: Optional[UUID] = Query(None), db: Session = Depends(get_db)
):
    service = FeedInfoService(db)
    return service.get_by_publisher(publisher_name, snapshot_id)
