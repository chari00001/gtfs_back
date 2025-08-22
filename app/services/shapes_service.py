from __future__ import annotations

from typing import List, Optional
from uuid import UUID
from sqlalchemy.orm import Session

from app.models.shapes import Shapes
from app.schemas.shapes import ShapesCreate, ShapesUpdate
from app.services.base_service import BaseService


class ShapesService(BaseService[Shapes, ShapesCreate, ShapesUpdate]):
    """Shapes tablosu için özel servis"""
    
    def __init__(self, db: Session):
        super().__init__(Shapes, db)
    
    def get_by_shape_id(self, shape_id: str, snapshot_id: Optional[UUID] = None) -> List[Shapes]:
        """Shape ID'ye göre tüm noktaları getir"""
        query = self.db.query(Shapes).filter(Shapes.shape_id == shape_id) \
                                    .order_by(Shapes.shape_pt_sequence)
        
        if snapshot_id:
            query = query.filter(Shapes.snapshot_id == str(snapshot_id))
        
        return query.all()
    
    def get_shape_ids(self, snapshot_id: Optional[UUID] = None) -> List[str]:
        """Tüm shape ID'leri getir"""
        from sqlalchemy import distinct
        
        query = self.db.query(distinct(Shapes.shape_id))
        
        if snapshot_id:
            query = query.filter(Shapes.snapshot_id == str(snapshot_id))
        
        return [r[0] for r in query.all()]
