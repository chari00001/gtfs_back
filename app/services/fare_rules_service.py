from __future__ import annotations

from typing import List, Optional
from uuid import UUID
from sqlalchemy.orm import Session

from app.models.fare_rules import FareRules
from app.schemas.fare_rules import FareRulesCreate, FareRulesUpdate
from app.services.base_service import BaseService


class FareRulesService(BaseService[FareRules, FareRulesCreate, FareRulesUpdate]):
    """FareRules tablosu için özel servis"""
    
    def __init__(self, db: Session):
        super().__init__(FareRules, db)
    
    def get_by_route(self, route_id: str, snapshot_id: Optional[UUID] = None) -> List[FareRules]:
        """Route ID'ye göre ücret kurallarını getir"""
        query = self.db.query(FareRules).filter(FareRules.route_id == route_id)
        
        if snapshot_id:
            query = query.filter(FareRules.snapshot_id == str(snapshot_id))
        
        return query.all()
    
    def get_by_fare(self, fare_id: str, snapshot_id: Optional[UUID] = None) -> List[FareRules]:
        """Fare ID'ye göre kuralları getir"""
        query = self.db.query(FareRules).filter(FareRules.fare_id == fare_id)
        
        if snapshot_id:
            query = query.filter(FareRules.snapshot_id == str(snapshot_id))
        
        return query.all()
