from __future__ import annotations

from typing import List, Optional
from uuid import UUID
from sqlalchemy.orm import Session

from app.models.feed_info import FeedInfo
from app.schemas.feed_info import FeedInfoCreate, FeedInfoUpdate
from app.services.base_service import BaseService


class FeedInfoService(BaseService[FeedInfo, FeedInfoCreate, FeedInfoUpdate]):
    """FeedInfo tablosu için özel servis"""
    
    def __init__(self, db: Session):
        super().__init__(FeedInfo, db)
    
    def get_latest_feed(self, snapshot_id: Optional[UUID] = None) -> Optional[FeedInfo]:
        """En güncel feed bilgisini getir"""
        query = self.db.query(FeedInfo)
        
        if snapshot_id:
            query = query.filter(FeedInfo.snapshot_id == snapshot_id)
        
        return query.order_by(FeedInfo.feed_start_date.desc()).first()
    
    def get_by_publisher(self, publisher_name: str, snapshot_id: Optional[UUID] = None) -> List[FeedInfo]:
        """Yayıncı adına göre feed'leri getir"""
        query = self.db.query(FeedInfo).filter(
            FeedInfo.feed_publisher_name.ilike(f"%{publisher_name}%")
        )
        
        if snapshot_id:
            query = query.filter(FeedInfo.snapshot_id == snapshot_id)
        
        return query.all()
