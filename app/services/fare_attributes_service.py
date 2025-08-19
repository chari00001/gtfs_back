from __future__ import annotations

from typing import List, Optional
from uuid import UUID
from sqlalchemy.orm import Session

from app.models.fare_attributes import FareAttributes
from app.schemas.fare_attributes import FareAttributesCreate, FareAttributesUpdate
from app.services.base_service import BaseService


class FareAttributesService(BaseService[FareAttributes, FareAttributesCreate, FareAttributesUpdate]):
    """FareAttributes tablosu için özel servis"""
    
    def __init__(self, db: Session):
        super().__init__(FareAttributes, db)
    
    def get_by_agency(self, agency_id: str, snapshot_id: Optional[UUID] = None) -> List[FareAttributes]:
        """Agency ID'ye göre ücret tarifelerini getir"""
        query = self.db.query(FareAttributes).filter(FareAttributes.agency_id == agency_id)
        
        if snapshot_id:
            query = query.filter(FareAttributes.snapshot_id == snapshot_id)
        
        return query.all()
    
    def get_by_currency(self, currency_type: str, snapshot_id: Optional[UUID] = None) -> List[FareAttributes]:
        """Para birimi ile ücret tarifelerini getir"""
        query = self.db.query(FareAttributes).filter(FareAttributes.currency_type == currency_type)
        
        if snapshot_id:
            query = query.filter(FareAttributes.snapshot_id == snapshot_id)
        
        return query.all()
